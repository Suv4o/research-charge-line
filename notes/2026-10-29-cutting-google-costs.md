# Cutting Google Costs: How ABRP Does It, and a Plan for Charge Line

**Date:** 2026-10-29
**For:** the user: "too pricey … ABRP offers unlimited free plans … they don't use Google Maps"
**Question:** What would it take for Charge Line's per-trip cost to be near zero, like ABRP's free plan? Which parts must change, what do we lose, and in what order?

## Bottom line

- **The map isn't the cost.** Google's Maps SDK for iOS is free and unlimited. Almost all of the bill comes from one call: **Places Text Search with live availability** (US$40 per 1,000 after 1,000 free). It runs about 5 times per trip that needs charging, and once per Chargers-tab search.
- **Today that's about US$1.20–1.30 per active user per month**, about 40% of what a Premium subscriber brings in. Every free user costs it too. At 10,000 users that's about US$13,000 a month.
- **ABRP doesn't use Google for chargers.** It uses community data:
  - OpenStreetMap, Open Charge Map, Supercharge.info and GoingElectric, plus feeds from networks it partners with;
  - its own routing on OpenStreetMap.
  - Live availability, CarPlay, traffic and weather are its paid features (US$4.99 a month or US$49.99 a year).
- **The same free data covers most of Australia:**
  - OpenStreetMap: 867 fast (DC) sites.
  - Open Charge Map: 820, of which only 138 were checked in the last year.
  - **Merged: 1,170**, about three quarters of the roughly 1,560 fast-charging locations the Electric Vehicle Council counts.
  - Supercharge.info: 155 open Superchargers with stall counts and power, and which are open to other EVs (115).
  - OpenStreetMap fills most of the gaps that sank the 23 October trial (Wangaratta, Wandong, Wodonga). It doesn't fill Mildura → Broken Hill.
- **Recommendation: a hybrid in four steps.**
  1. Plan from **our own Australian charger database**, built daily from the free sources and searched on the phone.
  2. Keep Google only for **live availability on the stops a Premium trip uses**.
  3. Keep the Google map, which is free.
  4. Make planning **unlimited for free users**, like ABRP.
- **Result:** Google's monthly bill at 10,000 users drops from about US$13,000 to about US$400–900, almost all of it from Premium users' live checks. Self-hosting routing and address search later brings it lower.
- **What free users lose:** live availability. In exchange, free planning has no monthly limit.

## 1. Where the money goes today

From the 2026-10-13 pricing and the 2026-10-23 measurements (US$, per 1,000 after the monthly free calls):

| Call | When | SKU | Price |
| --- | --- | --- | --- |
| Search along the route, with live availability | ~4.8 per trip that needs charging | Text Search Enterprise + Atmosphere | $40 (1,000 free) |
| Chargers tab / CarPlay search | each new search (reused for 5 min since app 9ef7e9f) | same | $40 |
| Route | 1–2 per trip | Compute Routes Essentials | $5 (10,000 free) |
| Destination's location | 1–2 per trip | Place Details Essentials | $5 (10,000 free) |
| Places to eat (Premium) | per stop | Nearby Search Pro | $32 (5,000 free) |
| Map display | always | Maps SDK for iOS | **free, unlimited** |

## 2. How ABRP does it

- **Chargers:** ABRP's help pages say chargers added to OpenStreetMap "appear in ABRP within a day or two." Its blog names Supercharge.info and Open Charge Map as the main editable sources, plus GoingElectric. Tesla, IONITY, Allego and Rivian come from partner feeds ([help](https://abrp.featurebase.app/help/articles/1441732-how-to-have-new-chargers-added-to-abrp), [blog](https://forum.abetterrouteplanner.com/blogs/entry/33-helping-abrp-charge-networks/)).
- **Map and routing:** OpenStreetMap, including speed limits and elevation ([CleanTechnica, 2019, secondary](https://cleantechnica.com/2019/05/11/abrp-other-open-source-projects-need-our-help/)). ABRP is owned by Rivian, and Rivian's data feeds its charger scores.
- **Paid tier:** CarPlay and Android Auto, real-time traffic, weather, live charger availability, history and multiple cars, at US$4.99 a month or US$49.99 a year. Free: planning, the charger map, navigation ([Premium](https://abetterrouteplanner.com/premium/)).
- **Takeaway:** ABRP's free plan costs it almost nothing per trip because the data is its own copy of community data, and live data is the paid feature.

## 3. Free charger data in Australia (measured 2026-10-29)

Each source was downloaded once and the copy deleted after counting. "Fast" means a DC plug or 50 kW or more. Two sites are the same if they're within 200 m.

| Source | Licence | AU fast sites | Notes |
| --- | --- | --- | --- |
| OpenStreetMap (Overpass) | ODbL | **867** (of 1,651 charging stations) | Operators: Evie 183, Chargefox 159, Tesla 140, NRMA 85, AmpCharge 63, Yurika 47, bp pulse 49, Exploren 34, Jolt 20. Many sites lack a kW figure |
| Open Charge Map (API) | CC BY 4.0 | **820** (of 1,356 operational) | Only **138** of the fast sites checked in the last 12 months |
| Both, merged | — | **1,170** | 511 in both, 356 only in OSM, ~300 only in OCM |
| Supercharge.info | none stated, **ask first** | 155 open Superchargers | Stall count and kW for all 155; `otherEVs` true for 115. 150 are already in OSM |
| VIC and NSW government data | CC BY | government-funded sites only | From the 2026-10-13 note |
| Reference: all of Australia | — | ~1,560 fast or ultra-fast locations, June 2026 | Electric Vehicle Council's State of EVs 2026, via [The Conversation](https://theconversation.com/ev-charging-deserts-in-regional-australia-are-slowing-the-shift-to-clean-transport-269102) (secondary) |

**The towns that sank the 23 October trial** (within 10 km):

| Town | Open Charge Map | OpenStreetMap adds |
| --- | --- | --- |
| Wangaratta | Evie only (checked 2023) | **Tesla Supercharger, NRMA** |
| Wandong | nothing nearby | **NRMA 180 kW**, Tesla and Evie at Wallan |
| Wodonga | stale Supercharger (2019) | **Evie, NRMA, Tesla** |
| Yass, Gundagai | covered | covered |
| Mildura | Evie, NRMA | Tesla, NRMA |
| Wentworth, Coombah | nothing | nothing |
| Broken Hill | NRMA 50 kW (checked 2021) | nothing; no Supercharger either |

Still missing from both: bp pulse Wangaratta, Charge Hub Wodonga, and anything new between Mildura and Broken Hill. **Coverage must be measured against Google on the trial's 10 routes before switching** (§6, step 1).

**Live availability without Google:** there is no Australian open data for it. There's no national mandate; reporting is voluntary ([The Conversation](https://theconversation.com/ev-charging-deserts-in-regional-australia-are-slowing-the-shift-to-clean-transport-269102)). The Electric Vehicle Council's Charge@Large has no public API that I found. Sources:
- **Tesla's Fleet API**, for Superchargers near the car (owners only).
- **Google** (`evChargeOptions`).
- **OCPI feeds** by agreement with each network or a roaming hub.

## 4. Options

| | A. Today | B. Hybrid (recommended) | C. No Google at all |
| --- | --- | --- | --- |
| Chargers for planning, Chargers tab, CarPlay | Google search | **Own database on the phone** | Own database |
| Live availability | Everyone, from Google | **Premium: Google, for the chosen stops and tapped chargers.** Tesla owners: their car | Tesla owners only, until network feeds |
| Map | Google (free) | Google (free) | Apple MapKit or MapLibre with OpenFreeMap tiles (free) |
| Route | Google | Google; self-hosted Valhalla later | Self-hosted Valhalla (Apple's directions have no waypoints, and can't go on a Google map) |
| Address search | Google | Google; self-hosted Photon later | Self-hosted Photon (OSM) |
| Places to eat | Google, Premium | **OSM, precomputed per charger, everyone** | OSM |
| Free plan | 3 trips that need charging a month | **Unlimited planning, without live status** | Unlimited |
| Work | — | ~2–3 weeks for steps 1–4 | ~4–5 weeks, and the map is rebuilt |

**Google's terms allow B.**
- Google's content (live availability) stays on Google's map.
- Our own data (OCM, OSM) may be drawn on a Google map.
- Place IDs may be stored indefinitely (Service Specific Terms §A.3), so a site in our database can keep its Google place ID. It's found with the **free** IDs-only Text Search, then asked for live availability with one Place Details call.
- **C** can't use Google's live data anywhere: it's banned "with or near" a non-Google map (§3.2.3(e)).

**Monthly cost at 5% Premium.** Assumptions:
- Free users: 4 charging trips and 10 charger searches a month.
- Premium users: 8 trips and 30 searches.
- Live checks: 3.5 per Premium trip, plus 5 tapped chargers.
- Hosting is an estimate: about US$45 a month for Valhalla and Photon on Fly.

| Active users | A. Today | B. Hybrid | B + own routing and search | C. No Google | Premium revenue |
| --- | --- | --- | --- | --- | --- |
| 500 | US$583 | ~US$5 | ~US$45 | ~US$45 | ~US$75 |
| 2,000 | US$2,466 | ~US$76 | ~US$102 | ~US$45 | ~US$300 |
| 10,000 | US$13,115 | ~US$860 | ~US$430 | ~US$45 | ~US$1,500 |
| 50,000 | US$66,775 | ~US$4,780 | ~US$2,080 | ~US$45 | ~US$7,500 |

In B, at scale, the remaining Google cost is half routes and address search (both free tiers run out) and half Premium's live checks. Moving routes and search to our own servers removes the first half.

## 5. Licences and terms to respect

- **OpenStreetMap (ODbL):**
  - Show "© OpenStreetMap contributors".
  - Merging OSM charger data with other sources and shipping the result to phones probably counts as "publicly using" a derivative database. Plan to **publish the merged Australian charger dataset under ODbL**, for example on GitHub, with each record's source. Ask for a quick legal check ([OSM licence use cases](https://wiki.openstreetmap.org/wiki/License/Use_Cases)).
- **Open Charge Map (CC BY 4.0):** attribution, as today.
- **Supercharge.info:** no licence published. **Ask permission** before using its data, or rely on OSM's Tesla sites (150 of 155) plus the car's own data.
- **Google:**
  - Live availability only next to a Google map.
  - Place IDs may be stored; Google's coordinates for at most 30 days, and we don't need them.
  - Comparing our chargers with a Google route on the phone is our data checked against our route request, with nothing stored. Self-hosted routing removes even that question.
- **Apple MapKit (option C only):** Apple's map data only on Apple's map.

## 6. Plan

1. **Our charger database (biggest saving, about 1–1.5 weeks).**
   - **Server, daily:** merge OSM, OCM and VIC/NSW data (and Supercharge.info if allowed).
     - Remove duplicates by distance and network.
     - Normalise network, plugs, kW, stalls and open-to-other-EVs, keeping the source and last-checked date.
     - Publish one compressed file, about 100–300 KB.
   - **App:** download the file weekly and use it on the phone for chargers along the route, the Chargers tab, CarPlay and Swap charger. Answers are instant, work offline and cost nothing.
   - **Missing kW:** use a typical figure for the network and plug, labelled as an estimate.
   - **Measure before switching:** rerun the 23 October comparison (10 routes × 4 cars × 3 "Plan for", about 50 Google searches) against the merged data. **Switch only if** it finds at least 95% of Google's fast sites within 10 minutes of the route and plans Melbourne → Broken Hill for the Atto 3. Otherwise fix the gaps first, by contributing verified sites to OSM or adding our own records.
   - **Measured the same day** on 21 routes ([2026-10-29-free-data-gaps-and-live-availability.md](2026-10-29-free-data-gaps-and-live-availability.md)): coverage 90%, but every free-data plan worked and 89% matched today's time. That note replaces the 95% gate with a plan test, and drops searching Google for each missing charger.
2. **Live availability as a Premium feature (about 2–3 days).**
   - After a Premium plan, check its stops' live status: one Place Details call each, using place IDs matched for free.
   - If a stop is all out of service, plan again without it.
   - In the Chargers tab, show live status when a charger is tapped.
   - Tesla owners keep live Supercharger stalls from the car.
   - Free users see the network, the plugs and when the site was last checked, as on ABRP.
3. **Places to eat from OSM (about 1 day):** cafés, food, toilets and playgrounds within about 300 m of each charger, precomputed in the daily file. Free for everyone, at no cost.
4. **Change the free plan (about 1 day plus App Store text):**
   - Unlimited planning for free users, keeping a fair-use guard.
   - Premium becomes live availability, CarPlay, the whole trip sent to a Tesla, your own stops, changing the plan, charging costs, learning and unlimited saved trips.
   - Update the Premium screen, the listing and the support page.
5. **Later, when Google's free tiers run out** (about 10,000 trips a month): self-host Valhalla (routing on OSM) and Photon (address search on OSM) for Australia on Fly (about 1 week). This removes Google's route and search costs.
   - **Measured 2026-10-30** ([2026-10-30-own-routing-and-search.md](2026-10-30-own-routing-and-search.md)): every plan works once Valhalla is tuned for Australia (typical speeds by speed limit, sealed roads only). 81% of plans matched today's stops and 63% today's time, against the hybrid's 90% and 89%. Photon's first answer matched Google's on 81% of searches. Hosting is about US$34 a month, which pays off beyond about 2,100 active users.
6. **In parallel, data partnerships:**
   - Ask Evie, Chargefox, NRMA, bp pulse, Ampol, Jolt, Exploren and the Electric Vehicle Council (Charge@Large) for location and live feeds (OCPI). ABRP gets live data the same way.
   - Ask Supercharge.info for permission.
   - Add "Report a charger" in the app, feeding OSM or OCM.

**Option C** (no Google at all) is worth reconsidering only if Google's terms or prices change. It costs Google's live data for non-Tesla networks, with no replacement today, and means rebuilding every map screen.

## 7. Risks

- **Coverage in remote areas.** Mildura → Broken Hill has no fast sites in the free data. Step 1's measurement decides.
- **Stale or wrong data.** Only 138 of OCM's fast sites were checked in the last year, and OSM often lacks kW. Mitigations:
  - prefer OSM when both have a site;
  - show when a site was last checked;
  - use Premium live checks;
  - add user reports.
- **No live status for free users** might make their plans stop at a broken charger. Plan B warnings and the arrival battery stay free.
- **ODbL obligations** for the merged dataset (§5).
- **Google interpretation:** using a Google route against our own data is an interpretation of the terms. Self-hosted routing removes it.

## Sources

- ABRP: [help, adding chargers](https://abrp.featurebase.app/help/articles/1441732-how-to-have-new-chargers-added-to-abrp) · [blog, charge networks](https://forum.abetterrouteplanner.com/blogs/entry/33-helping-abrp-charge-networks/) · [Premium](https://abetterrouteplanner.com/premium/) · [CleanTechnica, 2019](https://cleantechnica.com/2019/05/11/abrp-other-open-source-projects-need-our-help/) · [OCM forum on ABRP's sources](https://community.openchargemap.org/t/abrp-a-better-route-planner-no-longer-using-open-charge-map-information/1089)
- Australian charging: [EVC State of EVs 2026 media release](https://electricvehiclecouncil.com.au/wp-content/uploads/2026/09/Media-Release_State-of-Electric-Vehicles-Report-2026-1.pdf) · [The Conversation, charging deserts](https://theconversation.com/ev-charging-deserts-in-regional-australia-are-slowing-the-shift-to-clean-transport-269102)
- Data measured: OpenStreetMap via Overpass API (`amenity=charging_station`, AU, 2026-10-29) · Open Charge Map `/v3/poi?countrycode=AU` · Supercharge.info `service/supercharge/allSites`
- Licences: [OSM licence use cases](https://wiki.openstreetmap.org/wiki/License/Use_Cases) · [OSM collective database guideline (summary)](https://www.williamsmullen.com/news/openstreetmap-publishes-collective-database-guidelines-examples-included) · [OCM data licence](https://openchargemap.org/develop)
- Self-hosting: [Valhalla](https://valhalla.github.io/valhalla/mjolnir/getting_started_guide) · [Photon](https://github.com/komoot/photon) · [OpenFreeMap](https://openfreemap.org)
- Google pricing and terms: as quoted in [2026-10-13-trip-planner-data.md](2026-10-13-trip-planner-data.md) §1.5, §1.6
