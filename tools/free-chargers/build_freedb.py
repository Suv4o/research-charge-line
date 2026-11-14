"""Merges OpenStreetMap and Open Charge Map chargers for Australia into one file in the app's
OpenChargeMapReply shape ({"sites": [...], "attributions": [...]}), for the coverage test only.

Usage: python3 -I build_freedb.py <osm.json> <ocm.json> <out.json>

The inputs, each downloaded into its own new folder (research note 2026-10-29-free-data-gaps-and-live-availability.md):
  osm.json: curl --data-urlencode "data@au-chargers.overpassql" https://lz4.overpass-api.de/api/interpreter
  ocm.json: https://api.openchargemap.io/v3/poi?output=json&countrycode=AU&maxresults=10000&compact=false&verbose=false
            with the X-API-Key header (OPEN_CHARGE_MAP_KEY in server/.env, never printed)

OSM is the base (fresher, better coverage); OCM fills sites OSM lacks, and plugs, kW and Tesla's
"open to other EVs" where OSM has none. Two records are one site within 150 m (300 m for two Tesla
sites) unless their networks differ, like the app's OpenChargeMapSites.isSameSite.
"""
import json
import math
import re
import sys

SAME_SITE_M = 150.0
SAME_SUPERCHARGER_M = 300.0


def distance(a, b):
    lat1, lng1, lat2, lng2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


# The app's ChargerSite.network(fromName:) and OpenChargeMapSites.network(operatorName:name:groups:)
def network_from_name(name):
    lower = (name or "").lower()
    if "tesla" in lower:
        return "tesla" if "supercharger" in lower else None
    for key, net in (("evie", "evie"), ("chargefox", "chargefox"), ("ampcharge", "ampol"), ("ampol", "ampol"),
                     ("bp pulse", "bppulse"), ("bppulse", "bppulse"), ("nrma", "nrma"), ("jolt", "jolt")):
        if key in lower:
            return net
    return None


def network(operator, name, connectors):
    label = operator or name or ""
    if "tesla" in label.lower():
        return "tesla" if any((c.get("kw") or 0) >= 50 for c in connectors) else None
    return network_from_name(label) or network_from_name(name)


# MARK: OpenStreetMap

SOCKETS = {
    "type2_combo": "ccs2", "tesla_supercharger_ccs": "ccs2",
    "chademo": "chademo",
    "type2": "type2", "type2_cable": "type2", "tesla_destination": "type2",
    "tesla_supercharger": "tesla",
}
SOCKET_TITLES = {
    "ccs2": "CCS (Type 2)", "chademo": "CHAdeMO", "type2": "Type 2", "tesla": "Tesla (Type 2 DC)",
}


def kw_values(text):
    """'50 kW', '350kW', '50 kW;350 kW', '7.4', '22000 W' → kW numbers."""
    values = []
    for part in re.split(r"[;,/]", text or ""):
        m = re.search(r"(\d+(?:\.\d+)?)\s*(kw|kva|w)?", part.strip().lower())
        if not m:
            continue
        value = float(m.group(1))
        unit = m.group(2) or "kw"
        if unit == "w" or value > 1000:
            value /= 1000
        if 0 < value <= 1000:
            values.append(value)
    return values


def count_of(value):
    if value is None:
        return 0
    try:
        return max(int(float(value.split(";")[0])), 1)
    except ValueError:
        return 1 if value.strip().lower() in ("yes",) else 0


def osm_label(tags):
    brand, op, net, name = tags.get("brand"), tags.get("operator"), tags.get("network"), tags.get("name")
    blob = " ".join(x for x in (brand, op, net, name) if x).lower()
    if "tesla" in blob:
        if "supercharger" in blob:
            return "Tesla Supercharger"
        return "Tesla Destination" if "destination" in blob else "Tesla"
    return brand or net or op


def osm_sites(path):
    data = json.load(open(path))
    sites, skipped = [], {"lifecycle": 0, "private": 0, "no_position": 0}
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        lat = el.get("lat") if el["type"] == "node" else (el.get("center") or {}).get("lat")
        lng = el.get("lon") if el["type"] == "node" else (el.get("center") or {}).get("lon")
        if lat is None or lng is None:
            skipped["no_position"] += 1
            continue
        if tags.get("amenity") != "charging_station" or any(k.startswith(("disused:", "abandoned:", "construction", "proposed", "planned")) for k in tags) \
                or tags.get("operational_status") in ("closed", "non-operational"):
            skipped["lifecycle"] += 1
            continue
        if tags.get("access") in ("private", "no"):
            skipped["private"] += 1
            continue
        label = osm_label(tags)
        is_tesla = label is not None and label.startswith("Tesla")
        station_kw = max(kw_values(tags.get("charging_station:output", "")) + kw_values(tags.get("maxpower", "")), default=None)
        connectors, estimated = [], False
        for socket, kind in SOCKETS.items():
            raw = tags.get(f"socket:{socket}")
            if raw is None or raw.strip().lower() == "no":
                continue
            count = count_of(raw) or 1
            kw = max(kw_values(tags.get(f"socket:{socket}:output", "")), default=None)
            if kw is None and kind in ("ccs2", "chademo", "tesla") and station_kw and station_kw >= 24:
                kw = station_kw
            connectors.append({"type": kind, "title": SOCKET_TITLES[kind], "kw": kw, "count": count})
        if not connectors and label == "Tesla Supercharger":
            stalls = count_of(tags.get("capacity")) or 4
            connectors.append({"type": "ccs2", "title": "CCS (Type 2)", "kw": None, "count": stalls})
        if not connectors and station_kw and station_kw >= 24:
            connectors.append({"type": "ccs2", "title": "CCS (Type 2), plug assumed", "kw": station_kw, "count": count_of(tags.get("capacity")) or 1})
            estimated = True
        address = ", ".join(x for x in (
            " ".join(x for x in (tags.get("addr:housenumber"), tags.get("addr:street")) if x),
            tags.get("addr:suburb") or tags.get("addr:city") or tags.get("addr:place")) if x)
        sites.append({
            "id": f"osm:{el['type']}/{el['id']}",
            "name": tags.get("name") or label or "Charger",
            "address": address,
            "lat": lat, "lng": lng,
            "operator": label,
            "connectors": connectors,
            "points": count_of(tags.get("capacity")) or None,
            "operational": None,
            "membershipRequired": None,
            "usageCost": None,
            "lastVerified": None,
            "provider": "OpenStreetMap",
            "licence": "ODbL",
            "_tesla": is_tesla,
            "_plugAssumed": estimated,
        })
    return sites, skipped


# MARK: Open Charge Map (the server's parsePoi)

def connector_kind(title, current_type_id):
    t = (title or "").lower()
    if "ccs" in t and "type 2" in t:
        return "ccs2"
    if "chademo" in t:
        return "chademo"
    if "tesla" in t or "nacs" in t or "j3400" in t:
        return "tesla"
    if "type 2" in t:
        return "tesla" if current_type_id == 30 else "type2"
    return "other"


def ocm_sites(path):
    data = json.load(open(path))
    sites = []
    for poi in data:
        info = poi.get("AddressInfo") or {}
        lat, lng = info.get("Latitude"), info.get("Longitude")
        if lat is None or lng is None:
            continue
        status = poi.get("StatusType") or {}
        operational = status.get("IsOperational") if isinstance(status.get("IsOperational"), bool) else None
        if operational is False:
            continue
        connectors = []
        for c in poi.get("Connections") or []:
            ctype = c.get("ConnectionType") or {}
            title = ctype.get("Title") or ctype.get("FormalName") or "Unknown"
            connectors.append({
                "type": connector_kind(title, c.get("CurrentTypeID")),
                "title": title,
                "kw": c.get("PowerKW"),
                "count": max(c.get("Quantity") or 1, 1),
            })
        op = (poi.get("OperatorInfo") or {}).get("Title")
        sites.append({
            "id": f"ocm:{poi['ID']}",
            "name": info.get("Title") or "Charger",
            "address": ", ".join(x for x in (info.get("AddressLine1"), info.get("Town")) if x),
            "lat": lat, "lng": lng,
            "operator": op,
            "connectors": connectors,
            "points": poi.get("NumberOfPoints"),
            "operational": operational,
            "membershipRequired": (poi.get("UsageType") or {}).get("IsMembershipRequired"),
            "usageCost": poi.get("UsageCost"),
            "lastVerified": poi.get("DateLastVerified"),
            "provider": (poi.get("DataProvider") or {}).get("Title") or "Open Charge Map",
            "licence": (poi.get("DataProvider") or {}).get("License"),
            "_tesla": bool(op and "tesla" in op.lower()),
        })
    return sites


# MARK: Merge

def same_site(a, b):
    na, nb = network(a["operator"], a["name"], a["connectors"]), network(b["operator"], b["name"], b["connectors"])
    if a["_tesla"] and b["_tesla"]:
        na = nb = "tesla"
    if na and nb and na != nb:
        return False
    limit = SAME_SUPERCHARGER_M if (a["_tesla"] and b["_tesla"]) else SAME_SITE_M
    return distance((a["lat"], a["lng"]), (b["lat"], b["lng"])) < limit


def grid_key(lat, lng):
    return (int(math.floor(lat * 100)), int(math.floor(lng * 100)))


# Typical kW when no source gives one, labelled as estimated (DC only; AC doesn't matter for planning)
TYPICAL_DC_KW = {"tesla": 150.0}
DEFAULT_DC_KW = 50.0
DEFAULT_AC_KW = 22.0


def main(osm_path, ocm_path, out_path):
    osm, skipped = osm_sites(osm_path)
    ocm = ocm_sites(ocm_path)
    grid = {}
    for site in osm:
        grid.setdefault(grid_key(site["lat"], site["lng"]), []).append(site)
    merged_count = 0
    added = []
    for o in ocm:
        gy, gx = grid_key(o["lat"], o["lng"])
        nearby = [s for dy in (-1, 0, 1) for dx in (-1, 0, 1) for s in grid.get((gy + dy, gx + dx), [])]
        match = min((s for s in nearby if same_site(s, o)), key=lambda s: distance((s["lat"], s["lng"]), (o["lat"], o["lng"])), default=None)
        if match is None:
            added.append(o)
            continue
        merged_count += 1
        if not match["connectors"] and o["connectors"]:
            match["connectors"] = [dict(c) for c in o["connectors"]]
        else:
            for c in match["connectors"]:
                if c["kw"] is None:
                    same = [x["kw"] for x in o["connectors"] if x["type"] == c["type"] and x["kw"]]
                    if same:
                        c["kw"] = max(same)
        if not match["operator"] and o["operator"]:
            match["operator"] = o["operator"]
        op = (o["operator"] or "").lower()
        if match["_tesla"] and ("tesla-only" in op or "non-tesla" in op):
            match["operator"] = o["operator"]
        match["lastVerified"] = o["lastVerified"]
        match["usageCost"] = match["usageCost"] or o["usageCost"]
        match["provider"] = "OpenStreetMap + Open Charge Map"
        match["_ocm"] = o["id"]
    sites = osm + added
    estimated_kw = 0
    for site in sites:
        for c in site["connectors"]:
            if c["kw"] is None:
                if c["type"] in ("ccs2", "chademo", "tesla"):
                    c["kw"] = TYPICAL_DC_KW.get("tesla" if site["_tesla"] else "", DEFAULT_DC_KW)
                    c["title"] += " (kW estimated)"
                    estimated_kw += 1
                elif c["type"] == "type2":
                    c["kw"] = DEFAULT_AC_KW
            c.setdefault("operational", None)
    def fast(site):
        return any(c["type"] in ("ccs2", "chademo", "tesla") and (c["kw"] or 0) >= 50 for c in site["connectors"])
    def dc(site):
        return any(c["type"] in ("ccs2", "chademo", "tesla") and (c["kw"] or 0) >= 24 for c in site["connectors"])
    out = {
        "sites": [{k: v for k, v in s.items() if not k.startswith("_")} for s in sites],
        "attributions": ["© OpenStreetMap contributors (ODbL)", "Open Charge Map contributors (CC BY 4.0)"],
    }
    json.dump(out, open(out_path, "w"))
    osm_fast = sum(1 for s in osm if fast(s))
    print(f"OSM stations kept {len(osm)} (skipped {skipped}); OCM operational {len(ocm)}; merged pairs {merged_count}; OCM-only added {len(added)}")
    print(f"Total sites {len(sites)}; DC 24 kW+ {sum(dc(s) for s in sites)}; fast 50 kW+ {sum(fast(s) for s in sites)} (OSM-based {osm_fast}, OCM-only {sum(fast(s) for s in added)})")
    print(f"DC connectors with kW estimated: {estimated_kw}; OSM sites with plugs assumed: {sum(1 for s in osm if s.get('_plugAssumed'))}; OSM sites with no plug data: {sum(1 for s in osm if not s['connectors'])}")
    teslas = [s for s in sites if s["_tesla"] and fast(s)]
    known_open = sum(1 for s in teslas if s["operator"] and ("tesla-only" in s["operator"].lower() or "non-tesla" in s["operator"].lower()))
    print(f"Tesla fast sites {len(teslas)}, of which OCM says who can charge: {known_open}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
