# Trip Planner Data: Chargers, Routing, Vehicles, Energy and Planning

- **Date researched:** 2026-10-13
- **Question:** What data sources, models and algorithm should Charge Line's phase 2 trip planner use in Australia? Where do charger locations, live stall availability, routes, elevation, vehicle specs and charging curves come from? What do the terms allow us to store? What does one planned trip cost?
- **Status:** Answered from first-party docs, terms, dataset repositories and peer-reviewed papers. Seven live Places API (New) requests on 2026-10-13 confirmed what Google actually returns for Australian chargers. Prices and limits were checked on 2026-10-13 (Google's pricing list says "Last updated 2026-10-08 UTC").
- **Scope note:** Phase 2 is the on-device planner (SwiftUI, iOS 26, Google Maps SDK for iOS, Places API (New) and Routes API called from the app with an iOS-restricted key). Each section ends with what changes once the phase 3 Node/TypeScript server exists.

**Jargon used throughout.** *SoC* is state of charge, the battery %. *SKU* is Google's billing line item. A *field mask* is the list of response fields you ask Google for; it decides which SKU you pay. A *polyline* is a route shape as a list of points. *Regen* is regenerative braking, which puts energy back into the battery. *DP* is dynamic programming. *CPO* is a charge point operator (Evie, Chargefox and so on).

---

## Field results

**2026-10-14: the phase 2 planner built from this note, run live in the app** (iPhone 17 simulator at
Melbourne CBD, Model Y Long Range at 94% health, default preferences, Fastest).

- **Melbourne → Sydney Opera House from 90%.** Route 895 km. The per-window search (five overlapping
  200 km windows, up to 2 pages each) found **104 unique sites**; 31 were usable for this car and these
  networks. Plan: 4 stops (Tesla Euroa, Evie at km 334, Tesla Coolac, Ampol AmpCharge Pheasants Nest),
  38 min charging, 9 h 21 min driving, arriving with 25%. The run made 1 route call and about 10 Text
  Search calls, as §6 estimated. Live status came back for AmpCharge ("5 of 6 free") and not for the Tesla
  sites, as in §1.2.
- **A trip that needs no charge** (Geelong, 75 km) made only the route call: the app checks the energy
  first and skips the charger search.
- **Terrain Tiles** at z10, decoded on the device: Melbourne CBD 29 m, Wangaratta 151 m, Gundagai 228 m,
  Goulburn 641 m, Marulan 643 m, Sydney Opera House 4 m. That's within 4 m of the z11 samples in §2.4.
- **Charging curves (§3.4 affected).** To meet each car's published claim, the generic shape needed a
  scale of 0.6–0.9 for all 9 cars. Open EV Data's default shape is optimistic. Tesla doesn't publish
  10–80% times, so Teslas are tuned to Tesla's "km added in 15 minutes" at 100 km/h (Tesla AU pages, via
  search results).
- **Energy model (§4.3 affected).** Back-solving A and C from the highway *and* mixed figures gives an
  unrealistic A, because "mixed" includes stop-start losses that a steady 60 km/h doesn't have. The app
  uses A = 0.0073·m·g instead (the median A/(m·g) of the 7 EPA cars), B = 0, and solves C from the
  highway figure. Grade is applied on the net wheel energy, so a gentle descent saves energy at full
  value and only real braking is reduced to the regen share.
- **Planner (§5.2 affected).** The first live plan included a 48% → 50% one-minute stop: it was optimal
  under the cost model, but no driver would make it. The DP now charges at least 10 points per stop, or up
  to the limit, which can't make a feasible trip infeasible. The 140-charger, 1,500 km test plans in
  0.14 s in a debug build.

**2026-10-15: Tesla `nearby_charging_sites` on the user's Model Y** (car online and charging, parked in
Melbourne's east; through the new server and directly; no wake-ups). This answers most of open question 10.

- **Response shape** (REST, Fleet API NA/AP host): `response.superchargers[]` with `location {lat, long}`,
  `name` ("Box Hill, VIC"), `type`, `distance_miles`, `available_stalls`, `total_stalls`, `site_closed`, plus
  `amenities` and `billing_info` when asked for detail; also `destination_charging[]`,
  `congestion_sync_time_utc_secs` and `timestamp`.
- **Reach.** With no parameters Tesla returned the nearest **4** Superchargers (within 18 km). `radius` and
  `count` (as in car_server.proto's `GetNearbyChargingSites`) work over REST, but `radius=600&count=100`
  returned the same as `radius=200&count=50`: at most the **nearest 30**, reaching 157 km (Colac) from
  Melbourne. So live Tesla stalls cover the first part of a trip, or the stops near the car while driving.
- **Stall counts can be missing.** Twice, the first call after a gap returned the sites without
  `available_stalls`/`total_stalls`; the same call a few seconds later had them for all 30. The server now
  asks again once when every count is missing.
- **Cost and wake.** Each call is a data request (US$1 per 500). Not yet seen: what it returns while the
  car is asleep.
- **Battery** (`vehicle_data?endpoints=charge_state`) read the same way: 83%, charge limit 100%, charging.

**2026-10-15: "Plan for" and amenities, after the owner's first real use.**

- **The three priorities barely differed** on Melbourne → Sydney from 90% (80% limit, 15%/25% targets):
  Fastest and Fewest stops gave the identical 3 stops, and Most reliable only charged more at the first
  stop. Three stops is already the fewest within an 80% limit, and the reliability penalty (failure chance
  × 30 min) was small. Now Fewest stops may pass the limit to cut a stop (2 stops, 6 minutes slower), and
  Most reliable uses × 60 min and a 10% backup.
- **Amenities near Australian chargers aren't in Places.** One Text Search on the Hume (20 chargers) with
  `restroom`, `goodForChildren`, `servesCoffee` and `evChargeAmenitySummary` in the mask: `restroom` on 13,
  the other three on none. So cafés, food and playgrounds near a stop need a Nearby Search (§1.1's Table A
  types); the app runs one per stop shown.

---

## Bottom line up front

1. **Charger candidates: use Google Places Text Search (New) with search-along-route, run per route window.** Send the route polyline in `searchAlongRouteParameters`, with `includedType: electric_vehicle_charging_station` and `strictTypeFiltering: true`. Use one field mask with `evChargeOptions`, the amenity booleans and `routingSummaries`. All of those sit in a single SKU, Text Search Enterprise + Atmosphere: 1,000 free a month, then US$40 per 1,000. **Split the route into windows of about 150–200 km and fetch up to 2 pages per window.** One search over the whole Melbourne→Sydney route returned only 34 places and missed most of the highway Superchargers (§1.2).

2. **Live availability exists in Australia for most third-party networks, but not for Tesla or NRMA.** In the live check (71 sites), `availableCount`, `outOfServiceCount` and `availabilityLastUpdateTime` came back for Chargefox, Evie, Ampol AmpCharge, bp pulse, Jolt, Exploren and Everty. They were absent for all 12 Tesla Superchargers and all 7 NRMA sites. Timestamps were 2–13 minutes old, on 5-minute marks. For v1, Google is the only live source we need. For Tesla stalls, the Fleet API's `nearby_charging_sites` returns `available_stalls`/`total_stalls`, but only near the car's current position. That makes it a phase 3 feature for Tesla owners.

3. **We can't build our own charger database from Places.** The Maps Platform Terms forbid pre-fetching, indexing or storing Places content. Place IDs may be stored indefinitely, and Places lat/lng for up to 30 days. So the phone keeps Places results in memory for the planning session and saves only place IDs with a trip. A durable charger database (phase 3 server) has to come from **Open Charge Map** and state open data, both licensed CC BY, and gets linked to Google place IDs.

4. **Routing: use Routes API `computeRoutes` with `TRAFFIC_UNAWARE`.** That stays on the Essentials SKU: 10,000 free a month, then US$5 per 1,000. Ask for the default encoded polyline at `HIGH_QUALITY` (search-along-route only accepts encoded polylines). Ask for `legs.steps`, whose distance and static duration give an average speed for each step. Keep at most 10 intermediate stops to stay on Essentials. The Routes API returns **no elevation, no speed limits and no battery or charging options**. `emissionType: ELECTRIC` only feeds a preview eco-route and fuel-estimate feature, which bills at Pro and allows no intermediate stops.

5. **Elevation: use AWS Terrain Tiles on the device, with Google's Elevation API as the fallback.** The tiles are free, need no key, include Geoscience Australia data, and may be cached with attribution. Google's Elevation API is 5,000 free a month then US$5 per 1,000, but it may not be cached. I also couldn't confirm that it accepts an iOS-restricted key.

6. **Vehicle data: hand-curate the 9 profiles. Don't ship Open EV Data as the source of truth.** It is MIT-licensed with attribution required, but it was **archived in April 2025**. Some of the 9 cars are missing: there is no 2025 Model Y RWD, and the 2024 Model 3 RWD appears only as a suspect entry. Many entries are clearly wrong: 567 of 1,321 list a DC maximum equal to the battery's kWh. EV Database sells data only to registered companies and covers only DE/NL/UK. **For charging curves:** use a generic piecewise-linear shape, multiply it by the car's max DC kW and cap it at the charger's kW. Then tune the shape so it reproduces the manufacturer's official 10–80% time.

7. **Energy model v1: road-load physics on each route step.** Use Wh/km = (A + B·v + C·v²) ÷ drivetrain efficiency, plus a grade term (m·g·Δh, with only part of it recovered on descents), plus a temperature/HVAC multiplier, payload and optional headwind. Seed it from EPA road-load coefficients where they exist (Model Y/3, Ioniq 5, EV6, Polestar 2). Otherwise seed it from the profile's highway and mixed Wh/km. Learn **one correction factor per car** from actual vs planned energy, using a bounded, distance-weighted moving average.

8. **Planner: on the device, DP over the candidate chargers ordered by route distance, with a 1% SoC grid.** This is the fixed-path problem Sweda et al. (2017) solve. The full road-network algorithm of Baum et al. (2019) is overkill when we already have one route. "Fewest stops" compares (stops, time) in that order. "Most reliable" combines a filter, an expected-delay penalty and a rule that a backup charger must stay reachable. The 80% "charge up to" limit is soft: relax it with a warning only when no plan exists otherwise.

9. **Cost: about US$0.50 per Melbourne→Sydney plan once free usage runs out. Free usage covers about 100 plans a month.** The plan uses 2 route calls, ~10 along-route searches and ~3 availability refreshes. The binding limit is the 1,000 free Text Search Enterprise + Atmosphere requests. A lean variant uses Open Charge Map for candidates and Google only for the shortlisted stops: about US$0.17 per plan and about 160 free plans a month.

10. **Terms traps to design around now.** (a) Google Places and Routes content may never appear on Apple's map, and Apple Map Data only on Apple's map. The current Apple-map stand-in therefore must not show Google results, and an "MKDirections fallback" means a whole separate Apple mode. (b) Logging Google's live availability over time to draw "usually busy" charts would be creating content from Google data, which the Terms forbid. Busy times and reliability % (screens 09, 17, 18) need our own check-ins (phase 4). (c) Places has **no price per kWh field**. Prices come from Open Charge Map's free-text `UsageCost`, or from operator data.

---

## 1. Chargers in Australia

### 1.1 What Places API (New) returns for EV chargers

**Place types.** `electric_vehicle_charging_station` is in Table A, so it can be used as a search filter. The automotive group also has `gas_station`, `rest_stop`, `parking` and `truck_stop`, plus `ebike_charging_station`, `parking_garage` and `parking_lot`, which were added on 2026-02-12 ([Place types](https://developers.google.com/maps/documentation/places/web-service/place-types)). For amenities near a stop, Table A also has `public_bathroom`, `cafe`, `coffee_shop`, `playground`, `dog_park`, `shopping_mall` and `rest_stop`, so a Nearby Search can look for them.

**`evChargeOptions`** ([Place reference → EVChargeOptions](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places)):

| Field | Type | Meaning (Google's words, shortened) |
| --- | --- | --- |
| `connectorCount` | int | Connectors at the station. Can exceed the number of cars that can charge at once, because one port can have several connectors |
| `connectorAggregation[]` | list | Connectors grouped by `[type, maxChargeRateKw]` |
| `…type` | enum `EVConnectorType` | See the list below |
| `…maxChargeRateKw` | number | "The static max charging rate in kw of each connector in the aggregation" |
| `…count` | int | Connectors in this group |
| `…availableCount` | int | "currently available" |
| `…outOfServiceCount` | int | "currently out of service" |
| `…availabilityLastUpdateTime` | RFC 3339 timestamp | When availability in this group was last updated |

Connector enum values: `EV_CONNECTOR_TYPE_OTHER`, `J1772`, `TYPE_2`, `CHADEMO`, `CCS_COMBO_1`, `CCS_COMBO_2`, `TESLA`, `UNSPECIFIED_GB_T`, `UNSPECIFIED_WALL_OUTLET` and `NACS`. Google warns that `EV_CONNECTOR_TYPE_TESLA` "is less representative of an actual connector type, and more represents the ability to charge a Tesla brand vehicle at a Tesla owned charging station" (same reference).

**Related fields.** `evChargeAmenitySummary` is an AI-written summary of nearby coffee, restaurants and stores, and only applies to EV stations. The amenity booleans are `restroom`, `goodForChildren`, `allowsDogs` and `servesCoffee`. There are also `accessibilityOptions`, `parkingOptions`, `paymentOptions`, `regularOpeningHours` and `containingPlaces`, the place a charger sits inside, such as a shopping centre ([Place reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places)).

**What Places does not have.** I searched the Place reference and found no operator or network field, no price per kWh (only `fuelOptions.fuelPrices` for petrol stations, and `priceLevel`/`priceRange` for venues) and no popular-times or busy-hours field. The network has to be inferred from `displayName`, for example "Evie Charging Station", "AmpCharge Charging Station" or "NRMA".

**Filters on the request.** Text Search has `evOptions.connectorTypes[]` and `evOptions.minimumChargingRateKw` ([Text Search (New)](https://developers.google.com/maps/documentation/places/web-service/text-search)). **Don't use this request filter.** In the live check, `minimumChargingRateKw: 50` silently dropped sites that have no EV data at all, such as Chargefox Gundagai. Filter on the device instead, and show unknown-power sites as "power unknown".

### 1.2 What the API actually returned in Australia (live check, 2026-10-13)

**Method.** I made 7 requests with the server key from `poc/tesla-send-route/.env`. A shell command read the key into a variable, and it was never printed or written anywhere:

1. Text Search for "EV charging station Goulburn NSW"
2. Search along route, page 1
3. Search along route, page 2
4. Search along route on the Albury→Yass window, with `evOptions.minimumChargingRateKw: 50`
5. Place Details for the Goulburn Tesla Supercharger
6. Place Details for Evie Wangaratta
7. Nearby Search around Southbank, Melbourne, with `routingParameters`

I was limited to Places calls, so the route polyline was **hand-encoded**: 22 points along the Hume, using Google's polyline algorithm, rather than a Routes API polyline. All 7 requests returned HTTP 200. Every request included `evChargeOptions`, so all of them billed as Enterprise + Atmosphere, within the free monthly usage.

**What came back, by network** (71 unique sites):

| Network (from `displayName`) | Sites seen | With `evChargeOptions` | With live availability |
| --- | --- | --- | --- |
| Chargefox | 13 | 10 | 10 |
| Evie | 7 | 7 | 6 |
| Exploren | 7 | 4 | 3 |
| bp pulse | 3 | 3 | 3 |
| Jolt | 2 | 2 | 2 |
| Everty | 2 | 2 | 2 |
| Ampol AmpCharge | 1 | 1 | 1 |
| NRMA | 7 | 7 | **0** |
| Tesla Supercharger | 12 | 12 | **0** |
| Tesla Destination | 12 | 9 | 0 |
| Others (Charge Hub, generic, health hub, …) | 5 | 1 | 0 |

**Examples, verbatim from the responses:**

- **Chargefox, 179–183 Hume St, Goulburn.** `CCS_COMBO_2`, 75 kW × 2, `availableCount: 2`, `outOfServiceCount: 0`, `availabilityLastUpdateTime: "2026-10-13T10:30:00Z"`. The query ran at 10:32 UTC.
- **Evie, 32 Sydney St, Tarcutta.** CCS2 350 kW × 2 and CHAdeMO 184 kW × 2, **all 4 out of service**. A planner without live data would have routed someone there.
- **Tesla Supercharger, Goulburn.** `EV_CONNECTOR_TYPE_TESLA` 300 kW × 20 **and** `CCS_COMBO_2` 300 kW × 20, `connectorCount: 40`, and no availability fields, in Place Details too. The two groups probably describe the same 20 stalls (inference).
- **Evie Wangaratta, the POC's stop.** This is a **50 kW** site: CCS2 × 1 and CHAdeMO × 1. The trip-plan design's "Evie Wangaratta 350 kW" is sample data.
- `evChargeAmenitySummary` came back for **none** of the 71 sites. `restroom` was present on 17 of the 52 sites fetched with it in the field mask.
- **Freshness.** All 7 requests ran between 10:32:08 and 10:33:17 UTC. Every `availabilityLastUpdateTime` fell on a 5-minute mark (10:20, 10:25 or 10:30), so the data was 2–13 minutes old.

**A useful pattern, not documented by Google.** Tesla sites that Open Charge Map lists as "Tesla (including non-tesla)" (Coolac, Yass, Goulburn South) come back from Google with **both** `TESLA` and `CCS_COMBO_2` groups. Sites OCM lists as Tesla-only (Gundagai, Euroa, Holbrook) come back with `TESLA` only. That matches in all 6 sites I compared, which suggests "has a CCS2 group" means "open to non-Teslas". This is a hypothesis to verify (Open questions).

**Search along route misses sites on long routes.** The whole-route search returned 20 + 14 = 34 places, ranked by detour, not by position along the route. Many of them were city chargers in Melbourne and Sydney, and it missed the Albury, Holbrook, Coolac, Gundagai and Yass Superchargers and bp pulse Gumly Gumly. A single ~280 km window (Albury→Yass) returned all of those on page 1, and still had a `nextPageToken`. That window request also had `minimumChargingRateKw: 50`, which removes slow sites, so it isn't a perfectly clean comparison. Even so, it found six fast-charging sites the whole-route search had missed. Hence the per-window recommendation.

**Network names found:** Chargefox appears as "Chargefox Charging Station" and also "ChargeFox", NRMA as "NRMA" or "NRMA Charging Station", Ampol as "AmpCharge Charging Station", bp as "bp pulse Charging Station" and Jolt as "JOLT Charging Station". Matching on these names is fragile. Open Charge Map's explicit `OperatorID` is a useful cross-check (§1.7).

### 1.3 Searching along a route

- **How it works.** Pass `searchAlongRouteParameters.polyline.encodedPolyline` to Text Search (New). Only an encoded polyline is accepted ([Search along route](https://developers.google.com/maps/documentation/places/web-service/search-along-route)). Google says results "are not guaranteed to be along the route provided, but rather are ranked within the search area defined by the polyline … based on minimal detour times from origin to destination" ([searchText reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places/searchText)). If the origin and destination are close together, it may return nothing.
- **Overriding the origin.** `routingParameters.origin` overrides the polyline's origin, which is useful when you're already partway along the route ([Search along route](https://developers.google.com/maps/documentation/places/web-service/search-along-route)).
- **`routingSummaries`.** Put it in the field mask to get one entry per place, in the same order. With search-along-route, each entry has **two legs**: origin→place and place→destination, each with `duration` and `distanceMeters` ([Routing summary + search along route](https://developers.google.com/maps/documentation/places/web-service/routing-summary-sar)). So **detour = leg 1 + leg 2 − the route's own duration**, with no extra call. The live check returned these legs, for example Evie Wangaratta at 269 km / 10,435 s and then 625 km / 22,946 s. `routingParameters` can also set `travelMode`, `routingPreference` and `routeModifiers` (avoid tolls, highways or ferries) ([Routing summary](https://developers.google.com/maps/documentation/places/web-service/routing-summary)). Asking for `routingSummaries` without an origin or polyline is an error.
- **Limits.** `pageSize` is 1–20 (default 20). Pages chain through `nextPageToken`/`pageToken`, and every other parameter must be identical on the next page. **"Text Search (New) returns a maximum of 60 results across all pages"** ([Text Search (New)](https://developers.google.com/maps/documentation/places/web-service/text-search)). Nearby Search returns at most 20 (`maxResultCount` 1–20, radius ≤ 50 km), and its guide documents no page token ([Nearby Search](https://developers.google.com/maps/documentation/places/web-service/nearby-search)). **I found no documented limit on polyline length or point count.**
- **On iOS.** The Places SDK for iOS also supports search-along-route and has `GMSPlaceEVChargeOptions` ([iOS release notes](https://developers.google.com/maps/documentation/places/ios-sdk/release-notes), [iOS search along route](https://developers.google.com/maps/documentation/places/ios-sdk/search-along-route)). Calling the REST endpoints with `URLSession` is the alternative. For REST, Google says to send `X-Ios-Bundle-Identifier` and to "verify that requests with incorrect … iOS application identifiers are rejected", because iOS restrictions "may not be fully supported on older legacy … services" ([API security best practices](https://developers.google.com/maps/api-security-best-practices)).

**Recommended request for each route window:**

```http
POST https://places.googleapis.com/v1/places:searchText
X-Goog-FieldMask: places.id,places.displayName,places.location,places.shortFormattedAddress,
  places.types,places.businessStatus,places.evChargeOptions,places.restroom,places.goodForChildren,
  places.allowsDogs,places.accessibilityOptions,places.regularOpeningHours,places.containingPlaces,
  routingSummaries,nextPageToken
{ "textQuery": "EV charging station", "includedType": "electric_vehicle_charging_station",
  "strictTypeFiltering": true, "pageSize": 20, "regionCode": "AU",
  "searchAlongRouteParameters": { "polyline": { "encodedPolyline": "<window polyline>" } } }
```

Cut the route polyline into overlapping windows of about 150–200 km, simplifying each one. Merge the results by place ID. Use the routing-summary legs, or a projection onto our own route, to put each site in order along the route.

### 1.4 Field masks and SKU tiers

You pay for the **highest** SKU any field in the mask belongs to ([Places usage and billing](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing)). Tiers from [Place Data Fields (New)](https://developers.google.com/maps/documentation/places/web-service/data-fields) (updated 2026-10-08) and [SKU details](https://developers.google.com/maps/billing-and-pricing/sku-details):

| Field we need | Text Search SKU | Place Details SKU |
| --- | --- | --- |
| `id`, `nextPageToken`, `attributions` | Essentials (IDs Only), **free** | Essentials (IDs Only) |
| `location`, `formattedAddress`, `shortFormattedAddress`, `types`, `photos` | Pro | Essentials (except photos: IDs Only) |
| `displayName`, `primaryType`, `businessStatus`, `googleMapsUri`, `accessibilityOptions`, `containingPlaces`, `timeZone` | Pro | Pro |
| `regularOpeningHours`, `currentOpeningHours`, `rating`, `userRatingCount`, `websiteUri` | Enterprise | Enterprise |
| **`evChargeOptions`**, `evChargeAmenitySummary`, `restroom`, `goodForChildren`, `allowsDogs`, `servesCoffee`, `parkingOptions`, `paymentOptions`, **`routingSummaries`** (Text/Nearby only) | **Enterprise + Atmosphere** | Enterprise + Atmosphere |

Consequence: once `evChargeOptions` is in the mask, every other field is free to add. Asking for amenities and routing summaries in the same request costs nothing extra.

### 1.5 Pricing and free monthly usage (checked 2026-10-13)

Since 1 March 2025, Google has "replaced the USD $200 monthly credit with free monthly calls per SKU across Essentials, Pro and Enterprise" ([Maps Platform pricing](https://mapsplatform.google.com/pricing/)). That's 10,000 free a month for Essentials SKUs, 5,000 for Pro and 1,000 for Enterprise. Usage counts per calendar month, summed over all projects on the billing account ([core services pricing list](https://developers.google.com/maps/billing-and-pricing/pricing), "Last updated 2026-10-08"). Prices are in USD, per 1,000 billable events, for the first paid tier (up to 100,000 a month):

| SKU | Free / month | Price per 1,000 after that |
| --- | --- | --- |
| Places Text Search Essentials (IDs Only) | Unlimited | free |
| Places Text Search Pro | 5,000 | $32.00 |
| Places Text Search Enterprise | 1,000 | $35.00 |
| **Places Text Search Enterprise + Atmosphere** | **1,000** | **$40.00** |
| Places Nearby Search Pro / Enterprise / Ent.+Atmosphere | 5,000 / 1,000 / 1,000 | $32 / $35 / $40 |
| Places Place Details Essentials | 10,000 | $5.00 |
| Places Place Details Pro / Enterprise | 5,000 / 1,000 | $17 / $20 |
| **Places Place Details Enterprise + Atmosphere** | **1,000** | **$25.00** |
| Place Details Photos | 1,000 | $7.00 |
| Autocomplete Requests / Autocomplete Session Usage | 10,000 / unlimited | $2.83 / free |
| **Routes: Compute Routes Essentials** | **10,000** | **$5.00** |
| Routes: Compute Routes Pro | 5,000 | $10.00 |
| Routes: Compute Routes Enterprise | 1,000 | $15.00 |
| Elevation (a Pro SKU) | 5,000 | $5.00 |
| Weather Usage (Essentials) | 10,000 | $0.15 |
| Maps SDK (iOS/Android) map loads | Unlimited | free |

Google also sells monthly subscription bundles (for example "Starter, $100/month") ([pricing](https://mapsplatform.google.com/pricing/)). They don't matter at our volume. Each page of a paged Text Search is its own successful request, so each page is billed (inference from the SKU's billable event, "Successful request").

### 1.6 Terms: what we may store

From the [Google Maps Platform Terms of Service](https://cloud.google.com/maps-platform/terms) (last modified 2026-08-26), §3.2.3:

- **(a) No scraping.** "Customer will not … pre-fetch, index, store, reshare, or rehost Google Maps Content outside the services; … bulk download … places information, elevation values …; copy and save business names, addresses, or user reviews."
- **(b) No caching** "except as expressly permitted under the Maps Service Specific Terms."
- **(c) No creating content.** Examples include "build terrain models based on elevation values from the Elevation API", "use latitude/longitude values from the Places API as an input for point-in-polygon analysis", and using the content to train ML models.
- **(d) No re-creating Google products.** The product "must contain substantial, independent value and features beyond the Google products". Real-time navigation built from Directions data is given as an example of what's not allowed.
- **(e) No use with non-Google maps.** "Customer will not … display or use Places content on a non-Google Map."

From the [Service Specific Terms](https://cloud.google.com/maps-platform/terms/maps-service-terms) (last modified 2026-06-10):

- **§A.3 Google ID caching.** We may cache "place_id from Places API, Directions API, Geolocation API and Routes API".
- **§14.3 Places.** Lat/lng may be cached "for up to 30 consecutive calendar days". **§19.3 Routes** says the same. §14.2 and §19.2: no use with a non-Google map.
- **Elevation.** There is no caching clause, and the [Elevation policies](https://developers.google.com/maps/documentation/elevation/policies) say content "should not be pre-fetched, cached, or stored".
- **Place IDs.** They can be stored indefinitely, but Google recommends refreshing any older than 12 months. The refresh is a free Place Details call that asks only for the ID. `NOT_FOUND` means the ID is obsolete ([Place IDs](https://developers.google.com/maps/documentation/places/web-service/place-id), [Places policies](https://developers.google.com/maps/documentation/places/web-service/policies)).

**What this means for Charge Line:**

- ✅ Use Places live, on the phone. Persist only place IDs with saved trips, and lat/lng for up to 30 days, then re-fetch details when a trip is reopened.
- ❌ We can't build a charger database from Places, or sync Places results to a server.
- ❌ We can't record `availableCount` over time to build "usual busy times". That is storing content and creating new content from it. The busy-times chart and reliability % in screens 17–18 need our own check-ins, or a source that licenses that data.
- ⚠️ **In-memory reuse within a session is not defined in the Terms.** An example is re-running the planner when the user changes "arrive with at least 15%". I'm treating it as part of using the service, not as caching. That's an interpretation, listed in Open questions.
- ⚠️ Working out where each charger sits along our own route polyline from Places lat/lng is not "point-in-polygon analysis" as written. Even so, the routing-summary legs give the same order without doing any geometry on Places coordinates.
- ⚠️ Google Maps itself plans EV charging stops in cars with Google built-in. Charge Line's own value (car-specific energy model, sending the route to a Tesla, check-ins) should clear §3.2.3(d), but it needs a careful read before public release.

### 1.7 Alternatives and complements

**Open Charge Map (OCM).**

- **API.** `https://api.openchargemap.io/v3/poi`. A bare request returned *"You must specify an API key using the key query parameter or x-api-key header."* (tested 2026-10-13). Keys are free: "Sign In … choose 'my apps' … Register An Application". Useful parameters are `countrycode`, `latitude`/`longitude`/`distance`, `boundingbox`, `operatorid` and `connectiontypeid`, plus **`polyline`**: "Filter results along an encoded polyline, use with distance param … expanded into a polygon" ([OCM OpenAPI spec](https://github.com/openchargemap/ocm-docs/blob/master/Model/schema/ocm-openapi-spec.yaml)).
- **Fair use.** The API is free "with no warranty or service level agreement". Callers should debounce queries, can be banned for "excessive/indiscriminate use", and should "host your own API mirror" or clone the data for high volume (same spec).
- **Licence.** User-contributed data is **CC BY 4.0** (the switch from CC BY-SA happened 2022-04-01). Imported data "is copyright the original Data Provider", and apps must show "the appropriate Data Provider attribution (including license terms) … visible to the end user" ([OCM develop/terms](https://openchargemap.org/develop), [licence announcement](https://community.openchargemap.org/t/announcing-our-new-simpler-data-license-for-ocm-data-cc-by-4-0-international/565)). There is no share-alike requirement, and commercial use is allowed under CC BY. Each POI carries its data provider and licence.
- **Australian coverage, from OCM's own GitHub export** ([ocm-export](https://github.com/openchargemap/ocm-export), commit `8e3bedc`, 2026-04-22). I couldn't call the live API without a key, so the live counts may be higher. Findings:
  - 1,298 AU POIs, of which 1,297 are from "Open Charge Map Contributors" under CC BY 4.0. That makes AU licensing simple.
  - By operator (excluding removed or planned sites): Chargefox 304, Evie 174, Tesla Tesla-only 75, Tesla "including non-tesla" 55, NRMA 60, BP Pulse 35, Ampol AmpCharge 26 and Jolt 23.
  - **Freshness is weak.** Only 221 of 1,298 have a status update since 2025-01-01, and the latest is 2026-04-13.
  - **Accuracy is mixed.** OCM lists Goulburn's Tesla Supercharger as "120 kW × 8" (Google: 130 kW × 8) and Goulburn South as "250 kW × 12" (Google: 300 kW, 20 + 20 connectors).
  - **Useful extras:** an explicit `OperatorID`, a Tesla-only vs "including non-tesla" operator split, and a free-text `UsageCost` (for example "60c/kWh" or "$0.52/kWh"), which is often stale.
- **No live status** in practice. The schema has "Currently Available (Automated Status)" types, but the AU export uses static statuses (1,240 "Operational").

**Tesla Fleet API `nearby_charging_sites`.**

- `GET /api/1/vehicles/{vin}/nearby_charging_sites` "Returns the charging sites near the current location of the vehicle" ([Vehicle endpoints](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-endpoints)). The web docs show no parameters or response.
- **Tesla's own proto** ([`car_server.proto`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/protocol/protobuf/car_server.proto), commit `a4b43c1`, 2026-09-25) defines the request `GetNearbyChargingSites { include_meta_data, radius, count }`. The response is `Superchargers { id, amenities, available_stalls, billing_info, billing_time, city, distance_miles, location, name, site_closed, total_stalls, within_range, max_power_kw, out_of_order_stalls_number, out_of_order_stalls_names }` plus `congestion_sync_time_utc_secs`.
- **Scope.** `vehicle_device_data` explicitly covers "nearby Superchargers" ([Authentication overview](https://developer.tesla.com/docs/fleet-api/authentication/overview)). The Charge Line Tesla app already has that scope.
- **Cost and limits.** It's a per-vehicle data call. Tesla prices data requests at 500 per US$1 and wakes at 50 per US$1, with a US$10 monthly credit (see the [2026-09-21 note](2026-09-21-tesla-send-route-to-vehicle.md) §5). Tesla says to "ensure the vehicle is online before requesting device data" ([Billing and limits](https://developer.tesla.com/docs/fleet-api/billing-and-limits)). Which billing category this endpoint falls in isn't stated per endpoint.
- **Verdict.** It gives live Supercharger stalls, but only around the car's position, only for Tesla owners, and only with a paired car. It's useful during a drive in phase 3, not for planning ahead. I made no Tesla calls for this research.

**Australian government open data.**

- **Victoria, "Government Funded Public EV Chargers".** CC BY 4.0, updated monthly (last 2026-07-30), with location, kW, plug types and owner. It covers **only state-supported sites** ([DataVic](https://discover.data.vic.gov.au/dataset/government-funded-public-ev-chargers)).
- **NSW, "EV Charging Locations" (Transport for NSW).** CC BY, refreshed quarterly (CSV dated 2026-10-13). "Chargers are only government funded chargers", and TfNSW is "not responsible for the collection or validation" ([TfNSW Open Data](https://opendata.transport.nsw.gov.au/dataset/ev-charging-locations)).
- I found **no national, all-network dataset**. These two are good for seeding a server database, but neither has live status.

**Operator APIs, Charge@Large and PlugShare.**

- I found no public developer API for Evie, Chargefox, AmpCharge, bp pulse, NRMA or Jolt (web search 2026-10-13). This is a negative result, not proof.
- **Charge@Large**, the Electric Vehicle Council's live-status app (launched March 2025), started with Exploren, ChargeN'Go, Wevolt, Charge Hub and Sonic Charge. Chargefox, Evie and Tesla were "not yet on the app", and no third-party API was mentioned ([The Driven, 2025-03-07](https://thedriven.io/2025/03/07/ev-lobby-launches-new-charging-app-to-displace-plugshare-with-real-time-availability/), **secondary/trade press**).
- **PlugShare** licenses its API commercially only: "we do not provide personal or non-commercial licenses to use our data at this time" ([PlugShare API](https://company.plugshare.com/api.html)).

**OCPI** (Open Charge Point Interface, v2.3.0, EVRoaming Foundation).

- It's a peer-to-peer protocol. Registration starts when one party creates `CREDENTIALS_TOKEN_A` and sends it "in a secure way that is outside the scope of this protocol" ([credentials module](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/credentials.asciidoc)). In practice that means **a bilateral agreement with each CPO, or with a roaming hub**.
- OCPI defines a role that fits us, the **NSP (Navigation Service Provider)**: "Provides EV drivers with location information of Charge Points. Usually only interested in Location information" ([terminology](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/terminology.asciidoc)). The Locations module carries live EVSE status (`AVAILABLE`, `CHARGING`, `OUTOFORDER`, …) ([locations module](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_locations.asciidoc)), and the Tariffs module carries prices.
- This is the long-term route to live NRMA data, prices and stall-level status. It's a business-development task, not a v1 engineering task.

**Secondary context.** Trade press reports that Google Maps began showing live Tesla Supercharger availability in Australia in November 2025, and that Evie, Exploren, Chargefox, BP Pulse and Ampol share live data "to mapping platforms" ([The Driven, 2025-11-13](https://thedriven.io/2025/11/13/tesla-finally-shares-supercharger-availability-data-with-google-maps-but-what-took-so-long/), **secondary**). The live check found Tesla availability **absent from the Places API**, whatever the Maps app shows.

### 1.8 Recommended source mix

| Need | v1 (phase 2, phone only) | With the phase 3 server |
| --- | --- | --- |
| Candidate chargers along a route | Google Text Search along route, per window (§1.3) | Own database from OCM + VIC/NSW open data, linked to Google place IDs found with **free** IDs-only Text Search. The server returns candidates, and the phone uses Google only for the shortlist |
| Connector types and kW | Google `evChargeOptions` | Same, plus OCM for sites where Google has none |
| Live availability | Google `evChargeOptions` (non-Tesla networks), refreshed by Place Details on the chosen stops before arrival | Plus Tesla `nearby_charging_sites` for Tesla owners while driving. Plus OCPI feeds if a CPO agreement happens |
| Tesla open to non-Teslas? | Hypothesis: a CCS2 group at a Tesla site (§1.2). Cross-check OCM operator 3534 | Nightly server cross-check |
| Price per kWh | OCM `UsageCost` text, labelled "may be out of date" | OCPI Tariffs, or our own check-ins |
| Busy times, reliability % | None (can't be derived from Google data) | Our own check-ins (phase 4) |

---

## 2. Routing

### 2.1 Routes API `computeRoutes`

([computeRoutes reference](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRoutes), [usage and billing](https://developers.google.com/maps/documentation/routes/usage-and-billing), [intermediate waypoints](https://developers.google.com/maps/documentation/routes/intermed_waypoints))

- **Polyline.** `polylineEncoding` is `ENCODED_POLYLINE` (default) or `GEO_JSON_LINESTRING`. `polylineQuality` is `OVERVIEW` (default, fewer points, lower latency) or `HIGH_QUALITY`. Encoded polylines store coordinates rounded to 5 decimal places, about 1.1 m ([polyline algorithm](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)). Use encoded, because search-along-route needs it.
- **Distance and duration.** The route has `distanceMeters`, `duration` and `staticDuration` (without traffic). Each leg has the same plus a polyline, start and end locations, steps and `travelAdvisory`. Each step has `distanceMeters`, `staticDuration`, a polyline and a navigation instruction. A field mask is mandatory ("There is no default list of returned fields", [choose fields](https://developers.google.com/maps/documentation/routes/choose_fields)).
- **Waypoints.** "Up to 25 intermediate waypoints". Stopovers add legs, and `via: true` pass-through points don't. "Requests with 11 or more are billed at a higher rate" (Pro). `computeAlternativeRoutes` gives "No alternative routes … for requests that have intermediate waypoints". The rate limit is 3,000 queries per minute.
- **Traffic.** `routingPreference` is `TRAFFIC_UNAWARE` (default, fastest response), `TRAFFIC_AWARE` or `TRAFFIC_AWARE_OPTIMAL`. The last two bill at Pro ([traffic preferences](https://developers.google.com/maps/documentation/routes/config_trade_offs)). `departureTime` defaults to now. `trafficModel` applies only with `TRAFFIC_AWARE_OPTIMAL`.
- **`extraComputations`:** `TOLLS`, `FUEL_CONSUMPTION`, `TRAFFIC_ON_POLYLINE`, `HTML_FORMATTED_NAVIGATION_INSTRUCTIONS`, and `FLYOVER_`, `NARROW_ROAD_`, `TUNNEL_`, `BRIDGE_` and `SKYWAY_INFO_ON_POLYLINE`. Tolls and traffic on polylines bill at **Enterprise** ([SKU details](https://developers.google.com/maps/billing-and-pricing/sku-details)).

### 2.2 Elevation, speed and EV options

- **No elevation or grade.** I searched the computeRoutes reference: the only "elevation" mentions are menu links.
- **Speed per segment: only indirectly.** Use step `distanceMeters ÷ staticDuration`, which is an average speed per step and good enough for an energy model. `speedReadingIntervals` (with `TRAFFIC_ON_POLYLINE`, Enterprise) only gives traffic **categories**: `NORMAL`, `SLOW` or `TRAFFIC_JAM` ([SpeedReadingInterval](https://developers.google.com/maps/documentation/routes/reference/rest/v2/SpeedReadingInterval)). There are no speed limits. Roads API speed limits are "limited access" ([pricing list](https://developers.google.com/maps/billing-and-pricing/pricing)).
- **EV options are minimal.** `routeModifiers.vehicleInfo` has `emissionType` (`GASOLINE`, `ELECTRIC`, `HYBRID` or `DIESEL`) plus truck dimensions, weight and trailers. **There is no battery, consumption or charging input** ([RouteModifiers](https://developers.google.com/maps/documentation/routes/reference/rest/v2/RouteModifiers)).
- **Eco routes.** These use `emissionType` with `requestedReferenceRoutes: FUEL_EFFICIENT` and `FUEL_CONSUMPTION`, which returns `fuelConsumptionMicroliters`. The feature is **Preview (pre-GA)**, needs `TRAFFIC_AWARE_OPTIMAL` (billed as Compute Routes Pro), and "The route cannot contain an intermediate waypoint". Australia is a supported region ([eco-friendly routes](https://developers.google.com/maps/documentation/routes/eco-routes)). The docs describe the output only in microlitres, and Google says to use it "to compare different routes, not as explicit fuel usage estimates". **Not useful for SoC.**

### 2.3 Pricing

Essentials: 10,000 free, then $5 per 1,000. Pro (traffic-aware, 11–25 stops, waypoint optimisation, side-of-road/heading/stopover modifiers): 5,000 free, then $10. Enterprise (tolls, traffic on polylines, two-wheeler, large vehicle): 1,000 free, then $15 ([SKU details](https://developers.google.com/maps/billing-and-pricing/sku-details), [pricing list](https://developers.google.com/maps/billing-and-pricing/pricing), checked 2026-10-13). **For v1:** plan with `TRAFFIC_UNAWARE` (Essentials). Make one `TRAFFIC_AWARE` call (Pro) only when the user taps "Leave now" to refresh arrival times.

### 2.4 Elevation along the route

| Option | How it works | Limits | Cost | Can we cache? | Verdict |
| --- | --- | --- | --- | --- | --- |
| **AWS Terrain Tiles** (Terrarium PNG) | Fetch the z10–z11 tiles the route crosses, decode `R·256 + G + B/256 − 32768` metres | No key. AWS Open Data with no SLA | Free | **Yes**, with attribution. AU data is "© Commonwealth of Australia (Geoscience Australia) 2017" ([registry](https://registry.opendata.aws/terrain-tiles/), [attribution](https://github.com/tilezen/joerd/blob/master/docs/attribution.md)) | **Use in v1** |
| Google Elevation API | `path=enc:<polyline>&samples=N` returns evenly spaced samples | 512 points per request, 6,000 QPM, URL ≤ 16,384 characters. The returned `resolution` gets coarser when many points are requested ([requests](https://developers.google.com/maps/documentation/elevation/requests-elevation), [usage](https://developers.google.com/maps/documentation/elevation/usage-and-billing)) | 5,000 free, then $5 per 1,000 | **No**, and no terrain models (§1.6) | Fallback. iOS key restriction not verified |
| Geoscience Australia 1″ SRTM DEM (~30 m) | Download the grid | About 27 GB for DEM-H | Free, CC BY 4.0 | Yes | Phase 3 server: pre-compute highway profiles (**search-result level**: licence seen in eCat/DEA listings, not opened) |
| Open-Meteo Elevation | Copernicus GLO-90, up to 100 coordinates per call | Free tier is "non-commercial" only, < 10,000 calls a day ([docs](https://open-meteo.com/en/docs/elevation-api), [terms](https://open-meteo.com/en/terms)) | Paid for commercial use | — | Not needed |
| OpenTopoData public API | SRTM etc. | 100 locations per request, 1 call per second, 1,000 calls a day ([opentopodata.org](https://www.opentopodata.org/)) | Free | — | Too limited |

**Tested.** I sampled 6 points from Terrain Tiles at z11 (2026-10-13): Melbourne CBD 25 m, Wangaratta 152 m, Gundagai 223 m, Goulburn 643 m, Marulan 642 m and Sydney Opera House 5 m. Six tile fetches, all of them worked. A route of about 870 km crosses roughly 30–60 tiles of ~100 KB at z10–z11 (estimate).

### 2.5 Apple MapKit as a fallback

- `MKDirections` computes walking and driving directions, and "Apps may receive a `loadingThrottled` error if the device makes too many requests in too short a time period" ([MKDirections](https://developer.apple.com/documentation/mapkit/mkdirections)). `MKDirections.Request` has a source, a destination, highway and toll preferences, alternate routes and departure/arrival dates, **with no intermediate waypoints** ([Request](https://developer.apple.com/documentation/mapkit/mkdirections/request)). `MKRoute` returns a `polyline`, `steps` (instructions, distance, polyline), `distance`, `expectedTravelTime`, `hasTolls`, `hasHighways` and `advisoryNotices` ([MKRoute](https://developer.apple.com/documentation/mapkit/mkroute)). There is no elevation, no traffic categories and no EV options. `MKPointOfInterestCategory.evCharger` (iOS 13+) finds chargers, but with no connector or availability data ([evCharger](https://developer.apple.com/documentation/mapkit/mkpointofinterestcategory/evcharger)).
- **Cost.** I found no published fee or quota for native MapKit. Apple "may impose restrictions on Your usage … (e.g., limiting the number of transactions)" ([ADPLA Attachment 6 §2.7](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)).
- **Terms.** Map Data may be displayed on a map "only on an Apple map", and you "may not surface Map Data … without displaying the corresponding Apple map" (§2.4). There is no caching beyond "temporary and limited" use (§2.5). Combined with Google's §3.2.3(e), **you can't mix the two**: an MKDirections route can't be drawn on the Google map, and Google chargers can't be drawn on the Apple map. A MapKit fallback means a separate Apple-only mode with no Google charger data. That's a poor trade for a charging planner. Keep it as "outage mode: route only".

---

## 3. Vehicle data and DC charging curves

### 3.1 Open EV Data (KilowattApp/open-ev-data)

- **Status.** The GitHub repo is **archived**. The last commit is `32d7dc5` (2025-04-12), and `meta.updated_at` is 2025-04-12 with 1,321 vehicles ([repo](https://github.com/KilowattApp/open-ev-data)).
- **Licence.** "MIT License with Attribution Requirement": any public-facing use must show "Open EV Data (https://github.com/KilowattApp/open-ev-data)" in an About page, the docs or similar ([LICENSE](https://github.com/KilowattApp/open-ev-data/blob/master/LICENSE)). Commercial use is fine.
- **File contents** (`data/ev-data.json`, v1 format, and `data/v2/models/*.json`). Each vehicle has `id`, `brand`, `model`, `variant`, `release_year`, `vehicle_type`, `usable_battery_size` (kWh) and `energy_consumption.average_consumption`, which is **kWh/100 km** per the v2 README. It also has `ac_charger { ports, usable_phases, max_power }`, `dc_charger { ports ["ccs","chademo","tesla_suc"…], max_power, charging_curve [{percentage, power}], is_default_charging_curve }` and `charging_voltage` (400/800). An example is Abarth 500E: 42.2 kWh, 85 kW, curve 0%: 80.75, 50%: 85, 80%: 42.5, 100%: 17.
- **How curves are made.** When a contributor picks the default, the generator multiplies max kW by fixed factors ([charging_details.rb](https://github.com/KilowattApp/open-ev-data/blob/master/lib/vehicle_creator/charging_details.rb)). For 400 V packs over 30 kWh: 0–30% 1.0, 60% 0.9, 80% 0.5, 100% 0.2. **It has no 800 V case.**
- **Quality problems I measured:**
  - 567 of 1,321 entries list a DC `max_power` equal to `usable_battery_size`, for example Tesla Model Y 2022 "57.5 kWh / 57.5 kW". That looks like a placeholder bug.
  - `is_default_charging_curve: false` doesn't mean "measured". Many "false" curves are just 4 points (0/50/80/100) in round ratios.
  - Duplicates conflict, for example MG4 "Long Range" at 61.7 kWh/135 kW vs "Electric 64 kWh" at 64 kWh/142 kW.
  - The voltage is inconsistent: EV6 2021 is listed at 800 V, but EV6 LR AWD 2024 at 400 V.

**The nine Phase 1 models in Open EV Data:**

| Charge Line model | Closest Open EV Data entry | Usable kWh | DC max kW | Curve | Note |
| --- | --- | --- | --- | --- | --- |
| Model Y LR AWD 2025 | Model Y "Long Range AWD Launch Series" (2025) | 75 | 250 | 4 pts: 250/250/100/25 at 0/50/80/100% | Looks like a template |
| Model Y RWD 2025 | **None for 2025**. Only "Model Y" (2022, no variant) | 57.5 | 57.5 ⚠️ | 4 pts | Suspect entry |
| Model 3 LR AWD 2024 | Model 3 "Long Range Dual Motor" (2023) | 75 | 250 | 9 pts | Best of the Teslas |
| Model 3 RWD 2024 | "Model 3" (2023, no variant), or "RWD" (2022) | 57.5 / 62.3 | 57.5 ⚠️ / 170 | 4 / 2 pts | Conflicting |
| BYD Atto 3 Extended Range | "ATTO 3" (2022) | 60.5 | 89 | 4 pts | AU variant not confirmed |
| Hyundai Ioniq 5 Long Range | "IONIQ 5 Long Range 2WD/AWD" (2021) | 74 / 72.6 | 233 / 221 | 9 pts | 2021 model year only |
| Kia EV6 Long Range | "EV6 Long Range 2WD" (2021); "EV6 Long Range AWD" (2024) | 77.4 / 80 | 250 / 263 | default 3 / 6 pts | Default curves |
| MG4 Long Range | "MG4 EV Long Range" (2022); "MG4 Electric 64 kWh" (2022) | 61.7 / 64 | 135 / 142 | default / 4 pts | Duplicates conflict |
| Polestar 2 LR Single Motor | "2 Long Range Single Motor" (2021) | 75 | 150 | 10 pts | 2024 model year only as "Long Range Performance" (79 kWh, 205 kW) |

I did **not** check these against Australian manufacturer spec sheets.

### 3.2 EV Database (ev-database.org)

Free use requires prior permission and manual copying only: "Data exports or API access is not available under the Free Use tier", and "no automated data collection". The paid API is a nightly JSON dump that is "only available to registered companies, private applications will not be accepted". Its markets are Germany, the Netherlands and the UK, with **no Australian market data** ([EV Database data services](https://ev-database.org/data-services-api)). That doesn't fit a solo developer with no company, today.

### 3.3 Better first-party anchors

- **EPA Test Car List** (US EPA, xlsx files by model year; 2025 file dated 2026-01-21). It gives coastdown road-load coefficients **Target Coef A (lbf), B (lbf/mph), C (lbf/mph²)** and equivalent test weight for every tested US variant ([EPA test car data](https://www.epa.gov/compliance-and-fuel-economy-data/data-cars-used-testing-fuel-economy)). The 2025 file has Model Y LR AWD/RWD, Model 3 LR/Standard, Ioniq 5, EV6 and Polestar 2 Single/Dual Motor. It has **no** BYD Atto 3 or MG4, which aren't sold in the US. US variants may differ from Australian ones (wheels, tyres).
- **Green Vehicle Guide** (Australian Government). It lists energy consumption and electric range for EVs sold in Australia ([how-to guide](https://greenvehicleguide.gov.au/pages/Help/HowToGuide)). A search snippet describes the figure as Wh/km "as measured in the official laboratory test"; I couldn't confirm that wording or the test standard on the page itself. It's good for a sanity check of the placeholder "mixed Wh/km". I found no bulk download.
- **Manufacturers' Australian sites** for usable kWh, peak DC kW and the official 10–80% time, which tunes the curve (§3.4). Not collected in this research.

### 3.4 When a car has no curve

1. **Shape.** Use a piecewise-linear, concave function of SoC. This is how the literature models CC-CV charging (constant current, then constant voltage): power holds flat, then tapers. [Montoya et al. 2017](https://doi.org/10.1016/j.trb.2017.02.004) fit piecewise-linear functions to measured charging data. [Baum et al. 2019](https://doi.org/10.1287/trsc.2018.0889) note that charging functions are "typically … concave" and use piecewise-linear concave ones in their examples. A default for 400 V cars is Open EV Data's own: `f(s)` = 1.0 at 0–30%, 0.9 at 60%, 0.5 at 80% and 0.2 at 100%.
2. **Scale by the car, cap by the charger.** P(s) = min(Pmax_car · f(s), P_charger). Don't multiply the shape by the charger's kW: the car's taper comes from the battery, and the charger only caps it.
3. **Tune to the official claim.** Model time from 10% to 80% is t = Σ (C_eff · 1%) / P(s). Move the knee (where the taper starts) or a single scale factor until t matches the manufacturer's 10–80% minutes. That folds the real taper into a curve we never saw.
4. **Effective capacity** C_eff = usable kWh × battery health %.
5. **Per-stop overhead.** Add a fixed time for parking, plugging in and the session handshake, as an assumption: 3–5 minutes.
6. **Not modelled in v1:**
   - **Cold-battery derating.** Arrival without preconditioning, especially at third-party sites where a Tesla may not precondition.
   - **Shared-power cabinets.** Places doesn't expose them.
   - **Grid-side vs battery-side kW.** Open EV Data doesn't say which side its curve kW are measured on.
   - **800 V cars on some 400 V sites.** Community reports say these charge slowly; unverified.

   Flag all four in the UI as "estimate".

**With a server (phase 3):** fit real curves from Tesla charging sessions (Fleet Telemetry) and from user check-ins ("charged at 186 kW").

---

## 4. Energy model

### 4.1 Established approaches (peer-reviewed or official)

- **Power-based physics models.** Fiori, Ahn & Rakha (2016) estimate EV power second by second from "vehicle speed, acceleration and roadway grade". They compute regen efficiency from instantaneous operating variables rather than a constant, and report "an average error of 5.9% relative to empirical data". They find EVs recover more energy in urban than in high-speed driving, and that heating and air conditioning cut range significantly ([Applied Energy 168:257–268](https://doi.org/10.1016/j.apenergy.2016.01.097), abstract via [IDEAS](https://ideas.repec.org/a/eee/appene/v168y2016icp257-268.html)). The force balance is the standard road-load equation: F = A + B·v + C·v² + m·g·sinθ + m·a.
- **Data-driven calibration on top of physics.** De Cauwer, Van Mierlo & Coosemans (2015) fit multiple linear regression on real-world EV data, "based on the vehicle dynamics equation as underlying physical model" ([Energies 8(8):8573](https://doi.org/10.3390/en8088573)). De Cauwer et al. (2017) predict consumption per road segment before departure, with a mean absolute error of 12–14% of trip consumption ([Energies 10(5):608](https://doi.org/10.3390/en10050608)).
- **Temperature and HVAC.** Yuksel & Michalek (2015) show that annual BEV energy use rises about 15% in hot or cold US regions vs the Pacific Coast ([ES&T 49(6):3974](https://doi.org/10.1021/es505621s), abstract via PubMed). Liu et al. (2018) find the most efficient range is **21.8–25.2 °C**, and that temperature and auxiliary loads interact ([Applied Energy 227:324](https://doi.org/10.1016/j.apenergy.2017.08.074)). Official US guidance: at −7 °C (20 °F), EV economy "can drop roughly 39% in mixed city and highway driving … About two-thirds of the extra energy consumed is used to heat the cabin". Without the heater it is "8% lower" ([fueleconomy.gov, cold weather](https://www.fueleconomy.gov/feg/coldweather.shtml)). Air conditioning's effect on EVs "can be even larger on a percentage basis" than on petrol cars ([hot weather](https://www.fueleconomy.gov/feg/hotweather.shtml)).
- **Not read for this note**, but relevant: Genikomsakis & Mitrentsis (2017), a computationally efficient EV energy simulation for route planning ([TR-D 50:98](https://doi.org/10.1016/j.trd.2016.10.014)). Title and metadata only.

### 4.2 Worked numbers (physics, using EPA coefficients)

**Example car.** EPA 2025 Test Car List, Tesla "Model Y Long Range AWD": A = 37.77 lbf, B = −0.1538 lbf/mph, C = 0.02044 lbf/mph², equivalent test weight 4,750 lb (2,155 kg). In SI units that's A = 168.0 N, B = −1.53 N·s/m and C = 0.455 N·s²/m² (×4.448, ×9.950 and ×22.26).

**Wheel energy at steady speed:**

| Speed | Road-load force | Wheel energy |
| --- | --- | --- |
| 90 km/h | 414 N | 115 Wh/km |
| 100 km/h | 477 N | 132 Wh/km |
| 110 km/h | 546 N | 152 Wh/km (+15% vs 100 km/h) |

At 110 km/h the C·v² (mostly aero) term is 425 N of the 546 N, about 78%. That's why speed dominates highway consumption.

**From wheel to battery.** Divide by a drivetrain efficiency of about 0.85–0.90 (an assumption, to be calibrated), then add the auxiliary load. At 110 km/h that gives about 170–190 Wh/km, depending on the efficiency and auxiliary load assumed.

**Grade.** From the Terrain Tiles samples, Melbourne CBD (25 m) → Goulburn (643 m) is +618 m net. m·g·Δh = 2,155 × 9.81 × 618 = 13.1 MJ = **3.6 kWh at the wheels, about 4.1 kWh from the battery**, roughly 5% of a 75 kWh pack. The −638 m descent from Goulburn to Sydney gives back maybe 2.2–2.6 kWh if 60–70% is recovered. That recovery fraction is an assumption, to be calibrated.

### 4.3 Pragmatic v1

For each Routes API step, split into chunks of ≤ 2 km:

```
v      = step.distanceMeters / step.staticDuration          // average speed
F_road = A + B·v + C·(v + v_headwind)²                       // N; headwind optional (forecast)
E_road = F_road · d / η_drive                                // J
E_grade = m·g·Δh / η_drive        if Δh > 0
        = m·g·Δh · η_recover      if Δh < 0                  // η_recover ≈ 0.6–0.7 (assumption)
E_aux  = P_hvac(T_ambient) · d / v                           // P_hvac from a small table (assumption)
E_chunk = k_car · (E_road + E_grade + E_aux)                 // k_car = learned correction (§4.4)
```

- **Mass** m = test weight (or curb weight + 75 kg) + payload. The payload is a trip input, as a "people and luggage" picker.
- **Cars with no EPA A/B/C** (Atto 3, MG4, Australian-only variants): back-solve A and C from the profile's highway Wh/km at ~100–110 km/h and mixed Wh/km at ~60 km/h. Assume B = 0 and η_drive = 0.88. This is an assumption; calibration absorbs the error.
- **Temperature and wind.** Google Weather API's hourly forecast covers Australia, gives up to 240 hours, and includes temperature and wind ([overview](https://developers.google.com/maps/documentation/weather/overview), [coverage](https://developers.google.com/maps/documentation/weather/coverage)). At US$0.15 per 1,000 after 10,000 free, 3–5 points per trip is effectively free. Its caching rules are in SST §21 ([SST](https://cloud.google.com/maps-platform/terms/maps-service-terms)). Phase 2 can start with no weather input (assume 22 °C and no wind), then add the forecast once the core works.
- **Battery health** scales C_eff only.

### 4.4 Calibrating from the user's own trips

**What to log per completed leg:**

- planned energy E_plan, from the model
- actual energy E_act = (SoC_start − SoC_end) × C_eff
- distance, average speed, net Δh and temperature

In v1 the start and end SoC come from the user typing the arrival %, or from a "how much did you arrive with?" prompt. Phase 3 can read them from Tesla.

**The update:**

- Keep one multiplicative factor per car, k_car, starting at 1.0. After each leg longer than 30 km, update it in log space with a distance weight: `ln k ← ln k + α·w·(ln(E_act/E_plan) − ln k)`, with `w = min(1, d/200 km)` and α ≈ 0.3.
- Clamp k to 0.8–1.3. Show "learned from N trips".
- This is the one-parameter version of the regression calibration in De Cauwer et al. ([2015](https://doi.org/10.3390/en8088573), [2017](https://doi.org/10.3390/en10050608)). After about 10 trips, a small least-squares fit can split k into a speed term and a temperature term. Exact constants are design choices, not taken from a paper.
- Also learn a separate arrival-SoC bias (planned vs actual arrival %) for the warning thresholds.

**With a server (phase 3):** pool anonymised factors per model to set better priors for new users. Tesla Fleet Telemetry gives exact SoC and energy without asking the user.

---

## 5. Planning algorithm

### 5.1 Published approaches

- **Baum, Dibbelt, Gemsa, Wagner & Zündorf (2019), "Shortest Feasible Paths with Charging Stops for Battery Electric Vehicles"** ([Transportation Science 53(6):1627–1655](https://doi.org/10.1287/trsc.2018.0889); [arXiv:1910.09812](https://arxiv.org/abs/1910.09812)).
  - Minimises overall trip time, including charging, on a road graph with realistic charging functions.
  - The problem is NP-hard.
  - Their **CFP (charging function propagation)** label-setting search keeps labels of (driving time, SoC). Its labels "represent all possible tradeoffs between charging time and resulting SoC induced by the last visited charging station … but still [have] constant size". Labels are pruned by Pareto dominance.
  - Their **CHArge** variant uses contraction hierarchies and A* to reach optimal routes "within seconds" at country scale, and has heuristics "well below a second".
  - They note that forbidding charging above 80% "drastically deteriorates reachability in regions with few stations".
- **Sweda, Dolinskaya & Klabjan (2017), "Optimal Recharging Policies for Electric Vehicles"** ([Transportation Science 51(2):457–479](https://doi.org/10.1287/trsc.2015.0638)). They solve exactly our v1 setting: "finding an optimal recharging policy for an electric vehicle along a given path … the driver must decide where to stop and how much to recharge at each stop". There's a fixed per-stop cost and nonlinear charging, and they give efficient algorithms, heuristics and a stochastic variant.
- **Montoya, Guéret, Mendoza & Villegas (2017)** ([TR-B 103:87–110](https://doi.org/10.1016/j.trb.2017.02.004)) show that assuming linear charging "may lead to infeasible or overly expensive solutions". They use piecewise-linear charging functions.
- **Resource-constrained shortest path.** This is the general framework, where SoC is the resource ([Irnich & Desaulniers 2005](https://doi.org/10.1007/0-387-25486-2_2)).

### 5.2 What v1 runs on the device

**Inputs:**

- the route (one polyline, steps with distance and duration)
- the energy per chunk (§4.3)
- N candidate chargers. Each has: position x_k along the route, detour time and energy (from the routing-summary legs), a charge-time table T_k[a][b] for SoC a→b built from the car curve capped at the site kW (§3.4), a stall count and live availability.

**DP over chargers sorted by x_k, with a 1% SoC grid:**

```
best[node][s] = min cost to ARRIVE at node with SoC s   (node 0 = origin, s = battery % now)
for node k in route order:
  for each arrival SoC a with best[k][a] < ∞:
    for each departure SoC d in a…cap (d = a if k is not a charger):
      c = best[k][a] + (d > a ? overhead + T_k[a][d] : 0)
      for each later node j while energy(k→j) ≤ (d − hardFloor)/100 · C_eff:
        a' = floor(d − 100 · energy(k→j)/C_eff)      // in %, rounded down = conservative
        need = (j is destination) ? arriveDest% : arriveCharger%
        if a' ≥ need: relax best[j][a'] with c + driveTime(k→j) + detour(j)
answer = best[destination][*]; follow back-pointers
```

**Size.** With N ≈ 60 candidates, 101 × 101 SoC pairs and ~25 reachable next nodes, that's about 15 million relaxations, which should finish well under a second in Swift. This is an estimate, not measured.

**Reuse.** When the user changes targets, re-run on the same in-memory candidates without calling Google again (§1.6 ⚠️).

**Extra stops** (user waypoints) are nodes that can't charge. Destination-like stops may allow charging if a charger sits there.

**Rounding.** 1% of a 75 kWh pack is 0.75 kWh, about 4–5 km. Always round arrival SoC down.

### 5.3 The three "Plan for" modes

- **Fastest.** Minimise drive + detour + charging + overhead time.
- **Fewest stops.** Compare the pair (stops, time) in that order in the same DP: fewer stops first, then less time. It's the same table with a two-number cost.
- **Most reliable.** Three layers:
  1. **Filter.** Drop sites with `outOfServiceCount == count`, and optionally sites below a stall or reliability threshold.
  2. **Penalty.** Add an expected-delay cost: p_fail(k) × (time to the nearest backup + its charge-time difference). p_fail comes from live status, stall count and network, and later from check-ins. **In v1 this is a heuristic, not a measured probability.**
  3. **Backup rule.** On arriving at k, the SoC must still reach the next viable charger after k with a hard floor of about 5%. That's an extra feasibility test on the DP edge.
  - The "All reliable" badge and "99% reliable" in the designs need check-in data (phase 4). In v1, show "live status: 4 of 6 free" instead of a percentage.

### 5.4 Arrival targets and the 80% cap

- **Hard constraints:** arrive at chargers with ≥ "minimum arrival" (default 15%) and at the destination with ≥ the destination target (default 25%).
- **Soft constraint:** "charge up to" (default 80%). Run with cap = 80%. If there's no plan, re-run with cap = 100%, mark the stops that exceed 80% and explain why, following the reachability point from Baum et al. above.
- **The car's own number.** If the Tesla integration sends the route (2026-09-21 note), pass the destination target as `destination_arrival_soe`. The 2026-10-13 field test shows the car honours it only while its own Trip Planner plans charging.

### 5.5 Where a server changes this

The DP stays on the phone; it's cheap. The server would supply the candidate set from its own database (§1.8), pre-computed elevation profiles for major highways, and nightly cross-checks of Tesla non-Tesla access. It could also run a full-network search in the style of CFP to suggest different routes, not just stops on one route. That's not needed for v1.

---

## 6. Cost per planned trip (Melbourne → Sydney, ≈ 870 km)

Prices are as of 2026-10-13, in USD. "After free" means after the monthly free usage for that SKU runs out.

| Call | SKU | Per plan | Free / month | After free, per plan |
| --- | --- | --- | --- | --- |
| From/To autocomplete (sessions) | Autocomplete Session Usage | ~2 sessions | unlimited | $0 |
| Place Details for the chosen To (location) | Place Details Essentials | 1–2 | 10,000 | ~$0.01 |
| `computeRoutes`: initial route, `TRAFFIC_UNAWARE` | Compute Routes Essentials | 1 | 10,000 | $0.005 |
| `computeRoutes`: final route with chosen stops as intermediates (≤ 10) | Compute Routes Essentials | 1 | (shared) | $0.005 |
| Search along route: ~5 windows × 2 pages | Text Search Enterprise + Atmosphere | **~10** | **1,000** | **$0.40** |
| Elevation | Terrain Tiles (free); fallback Elevation API ×2 | 0 (2) | — (5,000) | $0 ($0.01) |
| Availability refresh for 3 stops (before departure or arrival) | Place Details Enterprise + Atmosphere | 3 | 1,000 | $0.075 |
| *Optional:* amenities near each stop (cafe, toilets, playground, within 400 m) | Nearby Search Pro (no `routingSummaries`) | 0–3, on demand | 5,000 | ≤ $0.10 |
| *Optional:* weather at 5 points | Weather Usage | 5 | 10,000 | ~$0.001 |
| **Total** | | | | **≈ $0.50** (≈ $0.60 with amenities) |

- **Plans per month within free usage:** about **100**, set by Text Search Enterprise + Atmosphere (1,000 ÷ 10). Next come Place Details Enterprise + Atmosphere (about 333 plans) and Compute Routes Essentials (about 5,000). Re-planning with different targets on the same route costs nothing extra.
- **Lean variant** (needs the phase 3 server, or OCM called from the phone): OCM supplies the candidates, and Google is used only for availability on the 3 stops plus 3 backups. That's 6 Place Details Enterprise + Atmosphere ($0.15) + 2 routes ($0.01) ≈ **$0.17 per plan**, and about **160 plans a month** within free usage.
- **Guardrails:** set per-API daily quotas in the Cloud console, for example 30 a day for Text Search Enterprise + Atmosphere, so the free usage can't be exceeded by a bug. Check which currency the billing account uses: Google lists prices in USD.
- **This research used** 7 Enterprise + Atmosphere requests (4 Text Search, 2 Place Details, 1 Nearby Search), all within free usage.

---

## Decision table for phase 2

| Area | Use | Why | Cost (2026-10-13) | Risks |
| --- | --- | --- | --- | --- |
| Charger candidates | Places Text Search along route, per 150–200 km window, `includedType` + `strictTypeFiltering`, no `evOptions` request filter | Best Australian coverage seen. Connectors, kW and live status in one call. Detour legs included | $40 / 1,000 after 1,000 free (~$0.40 per plan) | Coverage per window is tuned by trial. 60-result cap. No operator field (match on `displayName`) |
| Live availability | Places `evChargeOptions`, refreshed with Place Details on chosen stops | Live for Chargefox, Evie, AmpCharge, bp pulse, Jolt, Exploren, Everty | $25 / 1,000 after 1,000 free | **None for Tesla or NRMA.** Data was 2–13 min old in the test. Can't be logged over time |
| Tesla access for non-Teslas | Hypothesis: a CCS2 group at a Tesla site, cross-checked with OCM operator 3534 | Matched 6 of 6 sites checked | Free | Undocumented. Could change |
| Routing | `computeRoutes` `TRAFFIC_UNAWARE`, encoded `HIGH_QUALITY` polyline, steps. ≤ 10 intermediates | Essentials SKU, and gives the polyline search-along-route needs | $5 / 1,000 after 10,000 free | No elevation or speed limits. Traffic-aware ETA costs Pro |
| Elevation | AWS Terrain Tiles (Terrarium), cached on the device | Free, cacheable, includes Geoscience Australia data | Free | No SLA. Attribution needed. Fall back to the Elevation API (not cacheable) |
| Vehicle profiles | Hand-curated JSON for the 9 cars. Open EV Data and EPA as references | Open EV Data is archived and has errors. EPA gives real road-load data | Free (attribution if any Open EV Data values ship) | AU variants not verified. BYD and MG lack EPA data |
| Charging curves | Generic piecewise-linear shape × car kW, capped by site kW, tuned to the official 10–80% time | Works for every car, even without measured curves | Free | Cold battery, shared cabinets and 800 V vs 400 V not modelled |
| Energy model | Road-load + grade + HVAC table, step speeds, payload. Optional weather | Peer-reviewed physics. Few inputs | Weather ~free | Constants are assumptions until calibrated |
| Calibration | Per-car log-space moving-average factor from actual vs planned, clamped 0.8–1.3 | Simple and robust with few trips | Free | Needs the user to enter arrival % (Tesla telemetry in phase 3) |
| Planner | On-device DP over chargers in route order, 1% SoC grid. Modes as in §5.3 | Fits the fixed-path problem exactly. Fast | Free | Reliability is heuristic until check-ins exist |
| Map display | Google Maps SDK only for anything showing Places or Routes content | Terms §3.2.3(e). Apple ADPLA Att. 6 §2.4 | Free | The Apple-map stand-in must not show Google data |
| Prices, busy times | OCM `UsageCost` (labelled stale). No busy times in v1 | Not in Places, and can't be derived from Google data | Free | Prices may be wrong. Feature gap vs screens 17–18 |

---

## Open questions

1. **Does Places ever expose Tesla Supercharger availability in Australia?** It was absent at all 12 sites on 2026-10-13, even though trade press says Google Maps shows it.
   **Resolves by:** repeating the Goulburn and Yass Place Details check monthly, and comparing with the Google Maps app on the same day.
2. **Is a CCS2 group at a Tesla site a reliable sign that non-Teslas can charge there?**
   **Resolves by:** a phase 3 server job comparing every Australian Supercharger in Places with OCM operators 23 and 3534, and with Tesla's own non-Tesla site list.
3. **What window size and page count give complete coverage on long routes?** Is there a polyline length or point limit for search-along-route? No limit is documented.
   **Resolves by:** an experiment of about 20 requests, using real Routes polylines at 100, 150, 200 and 300 km windows on Melbourne→Sydney and Sydney→Brisbane, counting unique fast chargers against OCM.
4. **Does the iOS-restricted key work for Places REST, Routes REST and the Elevation API via `X-Ios-Bundle-Identifier`?** And are wrong bundle IDs rejected?
   **Resolves by:** one call per API with the correct and a wrong bundle ID once the iOS key exists. Expect 403 on the wrong one.
   **Resolved 2026-10-13 for Places and Routes.** With the app's iOS-restricted key and `X-Ios-Bundle-Identifier: io.github.suv4o.chargeline`, Places Text Search (New) and `computeRoutes` both returned 200. Without the header, both returned 403 `PERMISSION_DENIED`. The Elevation API is not enabled on that key and wasn't tested; it isn't needed if AWS Terrain Tiles are used.
5. **Is reusing Places results in memory within one planning session acceptable under "No Caching"?** Is a server-side table mapping OCM IDs to place IDs (built with IDs-only Text Search) acceptable?
   **Resolves by:** asking Google Maps Platform support in writing before phase 3. SST §A.3 explicitly permits caching place IDs.
6. **What is OCM's live Australian coverage, beyond the April 2026 export snapshot of 1,298 POIs?**
   **Resolves by:** registering a free OCM key and counting AU POIs by operator through `/v3/poi?countrycode=AU`.
7. **Are any Open EV Data curves measured?** And what are the correct Australian specs for the 9 cars (usable kWh, peak DC kW, official 10–80% time)?
   **Resolves by:** manufacturers' Australian spec sheets and the Green Vehicle Guide, then later real sessions from Tesla telemetry and check-ins.
8. **Do 800 V cars (Ioniq 5, EV6) charge slowly at some 400 V Tesla sites?** This is community-reported only.
   **Resolves by:** Hyundai/Kia or Tesla Australian documentation, or check-ins once phase 4 exists.
9. **What values fit the user's own Model Y for drivetrain efficiency (0.85–0.90) and recovery on descents (0.6–0.7)?** Both are assumptions here.
   **Resolves by:** two or three calibrated legs on the Hume (Melbourne→Goulburn climbing, Goulburn→Sydney descending), comparing planned and actual SoC.
10. **What does `nearby_charging_sites` cost, and does it need the car awake?** Also its exact REST response shape, which only the proto shows.
    **Partly resolved 2026-10-15** (Field results): the shape, the 30-site reach and the missing-counts quirk. Still open: the answer while the car is asleep.
11. **Will any Australian operator, Charge@Large or a roaming hub give an NSP-style OCPI feed** (locations, live status, tariffs) to a small app?
    **Resolves by:** emailing Evie, Chargefox and the EVC once the app is on TestFlight.
12. **Does Charge Line clear Terms §3.2.3(d) ("No Re-Creating Google Products")?** Google Maps has its own EV stop planning.
    **Resolves by:** a careful read or legal advice before public release. Keep in-app turn-by-turn navigation out of scope.

---

## Sources

**Google Maps Platform: Places (fetched 2026-10-13)**

1. [Places API (New): Place resource reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places). `EVChargeOptions`, `ConnectorAggregation` (all six fields), the `EVConnectorType` enum including the TESLA caveat, `EvChargeAmenitySummary` and the amenity booleans. Shows there is no price, operator or popular-times field.
2. [Place Data Fields (New)](https://developers.google.com/maps/documentation/places/web-service/data-fields). Which SKU tier each field triggers for Text Search, Nearby Search and Place Details (updated 2026-10-08).
3. [Text Search (New)](https://developers.google.com/maps/documentation/places/web-service/text-search). `evOptions`, `pageSize` 1–20, the 60-result maximum, paging rules, `includedType`/`strictTypeFiltering`, and the EV example response.
4. [searchText REST reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places/searchText). `SearchAlongRouteParameters`: encoded polyline only, results "ranked … based on minimal detour times".
5. [Search along route](https://developers.google.com/maps/documentation/places/web-service/search-along-route). How to pass the polyline, and overriding the origin with `routingParameters.origin`.
6. [Calculate routing summary](https://developers.google.com/maps/documentation/places/web-service/routing-summary). `routingSummaries` alignment, `routingParameters` (travel mode, preference, modifiers), error without an origin.
7. [Combine routing summaries with search along route](https://developers.google.com/maps/documentation/places/web-service/routing-summary-sar). Two legs per place (origin→place, place→destination).
8. [Nearby Search (New)](https://developers.google.com/maps/documentation/places/web-service/nearby-search). `maxResultCount` 1–20, radius ≤ 50 km, `rankPreference`.
9. [Place types (New)](https://developers.google.com/maps/documentation/places/web-service/place-types). `electric_vehicle_charging_station` and the amenity types in Table A; the 2026-02-12 additions.
10. [Places API usage and billing](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing). Billing at the highest SKU in the field mask; the list of Places SKUs.
11. [Places SDK for iOS: search along route](https://developers.google.com/maps/documentation/places/ios-sdk/search-along-route) and [release notes](https://developers.google.com/maps/documentation/places/ios-sdk/release-notes). Search-along-route and `GMSPlaceEVChargeOptions` on iOS.
12. [Policies and attributions for Places API](https://developers.google.com/maps/documentation/places/web-service/policies). The place ID caching exemption; attribution rules.
13. [Place IDs](https://developers.google.com/maps/documentation/places/web-service/place-id). Store indefinitely, refresh after 12 months for free, `NOT_FOUND` means obsolete.

**Google Maps Platform: pricing and terms**

14. [Core services pricing list](https://developers.google.com/maps/billing-and-pricing/pricing) ("Last updated 2026-10-08"). Free caps and per-1,000 prices for every SKU in §1.5 and §2.3; Maps SDK unlimited.
15. [SKU details](https://developers.google.com/maps/billing-and-pricing/sku-details). Compute Routes Essentials/Pro/Enterprise triggers; Text Search Enterprise + Atmosphere fields including `routingSummaries` and `evChargeOptions`; Elevation as a Pro SKU.
16. [Maps Platform pricing overview](https://mapsplatform.google.com/pricing/). The change of 2025-03-01 from the $200 credit to free calls per SKU; subscription plans.
17. [Google Maps Platform Terms of Service](https://cloud.google.com/maps-platform/terms) (last modified 2026-08-26). §3.2.3 (a)–(g): no scraping, caching, creating content, re-creating Google products or use with non-Google maps.
18. [Maps Service Specific Terms](https://cloud.google.com/maps-platform/terms/maps-service-terms) (last modified 2026-06-10). §A.3 place ID caching; §14 Places and §19 Routes (30-day lat/lng, no non-Google map); §21 Weather.
19. [API security best practices](https://developers.google.com/maps/api-security-best-practices). `X-Ios-Bundle-Identifier`; verify that iOS restrictions really reject; legacy services may not support them.

**Google Maps Platform: Routes, Elevation, Weather**

20. [computeRoutes reference](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRoutes). Polyline quality and encoding, 25 intermediates, `departureTime`, `trafficModel`, `ExtraComputation` values, Route/Leg/Step fields; no elevation field.
21. [RouteModifiers](https://developers.google.com/maps/documentation/routes/reference/rest/v2/RouteModifiers). `VehicleInfo.emissionType`; no battery or charging inputs.
22. [SpeedReadingInterval](https://developers.google.com/maps/documentation/routes/reference/rest/v2/SpeedReadingInterval). Traffic categories only.
23. [Routes API usage and billing](https://developers.google.com/maps/documentation/routes/usage-and-billing). 3,000 queries per minute, 25 waypoints, >10 waypoints billed higher.
24. [Intermediate waypoints](https://developers.google.com/maps/documentation/routes/intermed_waypoints). Stopovers vs `via`, legs.
25. [Eco-friendly routes](https://developers.google.com/maps/documentation/routes/eco-routes). Preview status, `TRAFFIC_AWARE_OPTIMAL`/Pro, no intermediates, Australia supported, microlitres.
26. [Traffic preferences](https://developers.google.com/maps/documentation/routes/config_trade_offs) and [choose fields](https://developers.google.com/maps/documentation/routes/choose_fields). Traffic options and billing; field mask required.
27. [Encoded polyline algorithm](https://developers.google.com/maps/documentation/utilities/polylinealgorithm). Precision ×1e5 (5 decimal places).
28. [Elevation API requests](https://developers.google.com/maps/documentation/elevation/requests-elevation), [usage and billing](https://developers.google.com/maps/documentation/elevation/usage-and-billing) and [policies](https://developers.google.com/maps/documentation/elevation/policies). `path`/`samples`, 512 points, 16,384-character URLs, 6,000 QPM, resolution, no caching.
29. [Weather API overview](https://developers.google.com/maps/documentation/weather/overview) and [coverage](https://developers.google.com/maps/documentation/weather/coverage). Hourly forecast for up to 240 hours with temperature and wind; Australia supported.

**Live check (primary, this research)**

30. Seven Places API (New) responses on 2026-10-13, 10:32–10:34 UTC, with a hand-encoded Hume polyline. They establish which fields and networks return availability, the result counts for whole-route vs window searches, the Tesla CCS2/TESLA pattern and the routing-summary legs. Raw responses are not committed: storing Places content is prohibited.

**Other charger data**

31. [Open Charge Map develop page and licence terms](https://openchargemap.org/develop) and [terms](https://openchargemap.org/about/terms). CC BY 4.0 for contributed data; data provider attribution required; third-party data stays with its owner.
32. [OCM OpenAPI spec](https://github.com/openchargemap/ocm-docs/blob/master/Model/schema/ocm-openapi-spec.yaml). API key required, `polyline`/`distance` filters, fair-use policy, mirroring advice. The `api.openchargemap.io/v3/` "must specify an API key" response was observed on 2026-10-13.
33. [OCM licence change announcement (2022-04-01)](https://community.openchargemap.org/t/announcing-our-new-simpler-data-license-for-ocm-data-cc-by-4-0-international/565). CC BY-SA → CC BY 4.0; check each POI's provider licence.
34. [openchargemap/ocm-export](https://github.com/openchargemap/ocm-export) (commit `8e3bedc`, 2026-04-22) and its `referencedata.json`. Australian POI counts, operators, freshness, `UsageCost`, operator IDs 23 and 3534.
35. [Tesla Fleet API: vehicle endpoints](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-endpoints). `nearby_charging_sites` path and description.
36. [teslamotors/vehicle-command `car_server.proto`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/protocol/protobuf/car_server.proto) (commit `a4b43c1`, 2026-09-25). `GetNearbyChargingSites` and the `Superchargers` message fields.
37. [Tesla Fleet API: authentication overview](https://developer.tesla.com/docs/fleet-api/authentication/overview) and [billing and limits](https://developer.tesla.com/docs/fleet-api/billing-and-limits). `vehicle_device_data` covers "nearby Superchargers"; rate limits; "ensure the vehicle is online".
38. [DataVic: Government Funded Public EV Chargers](https://discover.data.vic.gov.au/dataset/government-funded-public-ev-chargers). CC BY 4.0, monthly, government-supported sites only.
39. [TfNSW Open Data: EV Charging Locations](https://opendata.transport.nsw.gov.au/dataset/ev-charging-locations). CC BY, quarterly, government-funded only, not validated.
40. [PlugShare API](https://company.plugshare.com/api.html). Commercial licences only.
41. [OCPI 2.3.0 spec](https://github.com/ocpi/ocpi/tree/2.3.0/release/core) ([credentials](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/credentials.asciidoc), [terminology](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/terminology.asciidoc), [locations](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_locations.asciidoc)). Out-of-band credentials (bilateral), the NSP role, EVSE status values.
42. [The Driven, 2025-11-13](https://thedriven.io/2025/11/13/tesla-finally-shares-supercharger-availability-data-with-google-maps-but-what-took-so-long/). **Secondary.** Claims Google Maps shows Tesla availability in Australia and that other networks share live data with mapping platforms.
43. [The Driven, 2025-03-07](https://thedriven.io/2025/03/07/ev-lobby-launches-new-charging-app-to-displace-plugshare-with-real-time-availability/). **Secondary.** Charge@Large launch networks; Chargefox, Evie and Tesla absent; no API mentioned.

**Elevation alternatives**

44. [AWS Open Data: Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) and [Joerd attribution](https://github.com/tilezen/joerd/blob/master/docs/attribution.md). Free tiles; Geoscience Australia attribution. Six tiles were fetched successfully on 2026-10-13.
45. [Open-Meteo Elevation API](https://open-meteo.com/en/docs/elevation-api) and [terms](https://open-meteo.com/en/terms). Copernicus GLO-90, 100 coordinates per call, free tier non-commercial only.
46. [OpenTopoData](https://www.opentopodata.org/). Public API: 100 locations per request, 1 call per second, 1,000 calls a day.
47. Geoscience Australia 1″ SRTM-derived DEM ([eCat record](https://ecat.ga.gov.au/geonetwork/srv/api/records/22be4b55-24a9-4320-e053-10a3070a5236)). **Search-result level only:** CC BY 4.0 and the ~27 GB size come from listings, not a page I opened.

**Apple**

48. [MKDirections](https://developer.apple.com/documentation/mapkit/mkdirections), [MKDirections.Request](https://developer.apple.com/documentation/mapkit/mkdirections/request), [MKRoute](https://developer.apple.com/documentation/mapkit/mkroute) and [MKPointOfInterestCategory.evCharger](https://developer.apple.com/documentation/mapkit/mkpointofinterestcategory/evcharger). What MapKit returns; throttling; no waypoints.
49. [Apple Developer Program License Agreement, Attachment 6](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/). Apple Map Data only on an Apple map, no caching beyond temporary use, Apple may limit transactions.

**Vehicle data**

50. [KilowattApp/open-ev-data](https://github.com/KilowattApp/open-ev-data) (archived; commit `32d7dc5`, 2025-04-12), its LICENSE and `data/ev-data.json`. Fields, units, licence, model coverage and the data-quality counts in §3.1.
51. [open-ev-data `charging_details.rb`](https://github.com/KilowattApp/open-ev-data/blob/master/lib/vehicle_creator/charging_details.rb). The default curve factors, and that there's no 800 V case.
52. [EV Database: data services](https://ev-database.org/data-services-api). Free-use conditions; companies only; DE/NL/UK.
53. [US EPA: Data on cars used for testing fuel economy](https://www.epa.gov/compliance-and-fuel-economy-data/data-cars-used-testing-fuel-economy) (2025 Test Car List, file dated 2026-01-21). Road-load coefficients A/B/C and test weights for Model Y/3, Ioniq 5, EV6 and Polestar 2.
54. [Green Vehicle Guide how-to](https://greenvehicleguide.gov.au/pages/Help/HowToGuide). Australian Government listing of energy consumption and electric range per model.

**Energy and planning papers (metadata verified via Crossref; abstracts read unless noted)**

55. Baum, Dibbelt, Gemsa, Wagner, Zündorf (2019). "Shortest Feasible Paths with Charging Stops for Battery Electric Vehicles". *Transportation Science* 53(6):1627–1655. [doi:10.1287/trsc.2018.0889](https://doi.org/10.1287/trsc.2018.0889), [arXiv:1910.09812](https://arxiv.org/abs/1910.09812). Introduction and §3 (the CFP labels) read.
56. Sweda, Dolinskaya, Klabjan (2017). "Optimal Recharging Policies for Electric Vehicles". *Transportation Science* 51(2):457–479. [doi:10.1287/trsc.2015.0638](https://doi.org/10.1287/trsc.2015.0638). Abstract and introduction read from the authors' preprint.
57. Montoya, Guéret, Mendoza, Villegas (2017). "The electric vehicle routing problem with nonlinear charging function". *TR Part B* 103:87–110. [doi:10.1016/j.trb.2017.02.004](https://doi.org/10.1016/j.trb.2017.02.004). HAL preprint read: CC-CV shape, piecewise-linear fits.
58. Irnich, Desaulniers (2005). "Shortest Path Problems with Resource Constraints". In *Column Generation*, 33–65. [doi:10.1007/0-387-25486-2_2](https://doi.org/10.1007/0-387-25486-2_2). Metadata only.
59. Fiori, Ahn, Rakha (2016). "Power-based electric vehicle energy consumption model: Model development and validation". *Applied Energy* 168:257–268. [doi:10.1016/j.apenergy.2016.01.097](https://doi.org/10.1016/j.apenergy.2016.01.097). Abstract via IDEAS.
60. De Cauwer, Van Mierlo, Coosemans (2015). "Energy Consumption Prediction for Electric Vehicles Based on Real-World Data". *Energies* 8(8):8573–8593. [doi:10.3390/en8088573](https://doi.org/10.3390/en8088573).
61. De Cauwer, Verbeke, Coosemans, Faid, Van Mierlo (2017). "A Data-Driven Method for Energy Consumption Prediction and Energy-Efficient Routing of Electric Vehicles in Real-World Conditions". *Energies* 10(5):608. [doi:10.3390/en10050608](https://doi.org/10.3390/en10050608).
62. Yuksel, Michalek (2015). "Effects of Regional Temperature on Electric Vehicle Efficiency, Range, and Emissions in the United States". *ES&T* 49(6):3974–3980. [doi:10.1021/es505621s](https://doi.org/10.1021/es505621s).
63. Liu, Wang, Yamamoto, Morikawa (2018). "Exploring the interactive effects of ambient temperature and vehicle auxiliary loads on electric vehicle energy consumption". *Applied Energy* 227:324–331. [doi:10.1016/j.apenergy.2017.08.074](https://doi.org/10.1016/j.apenergy.2017.08.074).
64. Genikomsakis, Mitrentsis (2017). "A computationally efficient simulation model for estimating energy consumption of electric vehicles in the context of route planning applications". *TR Part D* 50:98–118. [doi:10.1016/j.trd.2016.10.014](https://doi.org/10.1016/j.trd.2016.10.014). **Metadata only, not read.**
65. [fueleconomy.gov: cold weather](https://www.fueleconomy.gov/feg/coldweather.shtml) and [hot weather](https://www.fueleconomy.gov/feg/hotweather.shtml) (US DOE/EPA). The EV −39% economy at −7 °C with heating (−8% without), and the air conditioning effect.
