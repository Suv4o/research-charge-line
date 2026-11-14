# Free Charger Data: How Much It Misses, Google Only for the Gaps, and Live Availability

**Date:** 2026-10-29
**For:** the user, before choosing the hybrid in [2026-10-29-cutting-google-costs.md](2026-10-29-cutting-google-costs.md):
- "test how bad those 5% of missing chargers are on various trips";
- "bring the live availability to most of the chargers … Tesla Superchargers … NRMA";
- "if those 5% are missing, can we only search for that 5%, so we pay little money for Google?"

## Bottom line

- **The missing chargers barely change the plans.** The test covered 21 Australian routes, 4 cars and the 3 "Plan for" settings, 252 plans in all.
  - Planning from the free data alone (OpenStreetMap + Open Charge Map), **every plan worked**. None failed, and none had to bend the driver's settings where today's didn't.
  - **90%** had the same number of stops as today's Google-based plan.
  - **89%** took the same time, within 10 minutes or 3%.
  - The median difference was **0 minutes**.
- **Coverage is 90%, not 95%.** The free data has 290 of Google's 321 fast chargers within 10 minutes of these routes, against 76% for Open Charge Map alone on 23 October.
  - The 31 missing sites are mostly at the city ends of trips, side towns 14–29 minutes off the highway, and new 2025–26 builds.
  - Today's plans stopped at one of them 12 times in 391 stops (3%). One of those (Eneabba) is in the free data under Chargefox's name, and the free plan used the same charger.
- **The bigger risk is the other way round.** 6% of free-plan stops are at sites Google doesn't list, which may be gone. And 499 DC plugs in the free data have no kW figure, so their speed is a guess.
  - Most of the plan differences came from this guesswork, not from missing sites.
  - Fix it before switching (§4).
- **Searching Google "only for the missing 5%" doesn't pay.** We can't know which chargers we're missing without asking Google.
  - Google's free IDs-only search does list them, but it also lists many chargers far off the route, and each unknown one costs a paid lookup.
  - Measured: about **7.8 lookups a trip**, which costs about the same as today's search, for almost no change in the plans.
  - Searching only where our data looks thin doesn't help either: 61% of the route counts as thin, because Australian highways really do have long gaps.
- **What does pay: a safety net.** If the free data can't plan a trip properly (no plan, or it bends the driver's settings), run today's Google search for that one trip.
  - That happened in **1.2%** of the test plans, costing about 0.05 searches a trip on average.
- **Live availability:** Google's API has it for almost every network except the two you named.
  - Evie 94%, Chargefox 98%, bp pulse 100%, Ampol 100%, Exploren 94%.
  - **Tesla 0 of 78** Superchargers and **NRMA 1 of 35** sites, even though Tesla has given Google Maps its live data since November 2025.
  - Closing that gap needs Tesla owners' own cars (already in the app), a feed from NRMA, and a test of TomTom's API (§5).

## 1. The test

**Method.** This is the 23 October trial harness, extended (app commit "Trial: free charger data", then removed; `-compare-free`).
- **Routes:**
  - the trial's 10 routes;
  - 11 regional and remote ones: Perth → Kalgoorlie, Perth → Geraldton, Adelaide → Coober Pedy, Darwin → Katherine, Alice Springs → Uluru, Sydney → Dubbo, Dubbo → Broken Hill, Sydney → Eden, Brisbane → Roma, Townsville → Cairns, Hobart → Strahan.
- **Cars:** Model Y Long Range, Ioniq 5 Long Range, MG4 Long Range and Atto 3 Extended Range, all at 94% battery health.
- **Settings:** each "Plan for" setting, starting at 90%.
- **Four ways to find chargers, each planned by the app's own planner:**
  - **today:** Google's search along the route, plus Open Charge Map within 2 km (the app now);
  - **free:** the free file alone, within 10 km of the route (about Google's 30-minute detour limit);
  - **gap-fill:** the free file plus Google's fast chargers it lacks, as flagged by Google's free IDs-only search;
  - **Google only where thin, or only when the free plan has a problem:** (§3).
- **The free file**, built for the test (2026-10-29), merges OpenStreetMap and Open Charge Map: 2,213 sites, 1,130 of them fast (50 kW or more).
  - OSM is the base. OCM fills sites OSM lacks, plus kW and Tesla's "open to other EVs".
  - Two records count as one site within 150 m (300 m for Superchargers) unless their networks differ.
  - 499 DC plugs had no kW in either source. The test used 50 kW for those, or 150 kW at Superchargers.
- **"Fast"** means 50 kW or more for a CCS2 car or a Tesla. **"Within 10 min"** means a detour of 10 minutes or less by Google's routing.
- **Google calls used:**
  - 95 paid searches (at most about US$3.80, or free within the month's 1,000);
  - 170 free IDs-only searches;
  - 209 Place Details Essentials (inside the 10,000 free a month);
  - about 43 routes.
- Results stayed in the app's memory and console, and the logs were deleted. This note has aggregates only.

## 2. How bad the missing sites are

**Coverage of Google's fast chargers:**

| | Free file has it | Share |
| --- | --- | --- |
| All of Google's fast sites along the 21 routes (30-min detour) | 401 of 473 | 85% |
| Within 10 min of the route | 290 of 321 | **90%** |
| Within 10 min, and listed as fast in the free file | 275 of 321 | 86% |
| For comparison: Open Charge Map alone, 23 October (10 routes) | — | 76% |

**What's missing within 10 min (31 sites).** By network: Evie 6, Chargefox 6, Exploren 6, Ampol 3, bp pulse 3, OTR 2, NRMA 2, and one each for Charge Hub, Everty and Bolt.
- **Trip ends in big cities:** Brisbane, the Gold Coast, Adelaide. Plans rarely stop there.
- **Side towns** (Beechworth, Rutherglen, Corowa, Bendigo, Robinvale, Bordertown, Gympie): 14–29 minutes off the highway, and never used by today's plans.
- **New builds the volunteers haven't caught up with:** NRMA Napperby (SA), Exploren and Evie in south-east Queensland.
- **Naming:** Eneabba (WA) is an NRMA site on Google and a Chargefox site in OSM. NRMA chargers can be started from the Chargefox app, so a merge should treat the two as possibly the same site.

**What it does to plans (252 plans):**

| | Free file only | Free + gap-fill |
| --- | --- | --- |
| Plans that worked | **252 of 252** (today: 252) | 252 |
| Bends the driver's settings where today doesn't | **0** | 0 |
| Same number of stops as today | 226 (90%); 21 fewer, 5 more | 231 (92%) |
| Time within max(10 min, 3%) of today | 225 (89%); 13 slower, 14 quicker | 225 (89%) |
| Time difference, median (range) | 0 min (−43 to +34) | 0 min (−43 to +34) |
| Stops at sites Google doesn't list | 21 of 373 (6%) | 21 of 368 |
| Today's stops at sites the free file lacks | 12 of 391 (3%), on 3 routes | — |

- **The time differences mostly come from the data, not from missing sites.**
  - Superchargers listed at our guessed 150 kW, where Google says 250–300 kW.
  - OSM pins a few hundred metres from Google's, which changes the detour estimate.
  - A 350 kW site the free file lists as working, which today's plan avoided. Google's live status may have shown it down, and that's exactly what free data can't know.
  - The worst case was Melbourne → Broken Hill: same stops, about 30 minutes slower on paper.
- **The 12 missing stops:**
  - Perth → Geraldton, 8: Eneabba under Chargefox's name, so it's the same charger. Plus Jurien Bay, where the free plan stopped elsewhere at no extra time.
  - Adelaide → Coober Pedy, 3: the Atto 3 used NRMA Napperby. Without it, the free plan took another route: 6 minutes quicker, or 11–19 minutes slower.
  - Brisbane → Rockhampton, 1: Evie Glass House Mountains.
- **The 23 October gate isn't met as written.**
  - It asked for at least 95% coverage: measured 90%.
  - It asked for a Melbourne → Broken Hill plan for the Atto 3: met. The plan works, bending like today's.
  - A better gate is the plan test above: no extra failures, no extra bends, and at least 85% of plans within 10 minutes or 3% of today. **That's met.**

## 3. Google only for the gaps: three ways, measured

| Way | How | Google cost per trip | Plans vs free data alone |
| --- | --- | --- | --- |
| **A. Look up each missing charger** (your idea) | Google's **free** IDs-only search along the route, filtered to fast chargers, lists every place ID. Unknown IDs get one Place Details call each (US$25 per 1,000) | **~7.8 lookups ≈ US$0.19**: unknown IDs can't be placed without paying, and most are far off the route. Today's search: ~4.1 searches ≈ US$0.17 | 5 more plans with today's number of stops; time no better |
| **B. Search only where the free data is thin** (over 100 km without a fast charger) | Today's search, in those 200 km windows only | **61% of windows** count as thin (43 of 70), so about US$0.10 | About the same as free data alone |
| **C. Safety net:** search only when the free plan has a problem (no plan, or bends the driver's settings) | Today's search, for that trip only | **1.2% of trips** (3 of 252) ≈ US$0.002 a trip on average | Same as free; in those 3 cases today's plan bends too |

- **A is a dead end for cost.** We could narrow it with many small boxed IDs-only searches along the route. Even then, the plan gain is close to nothing.
- **The free IDs-only search is still useful elsewhere.**
  - It returned 97% of the places the paid search did (717 of 737), at no cost.
  - That makes it the right tool for matching our database's sites to Google place IDs, which Premium needs for live checks of chosen stops (§5).
- **Recommendation: C**, plus fixing the data (§4).

## 4. Fixing the free data before switching

1. **kW for the 499 DC plugs without it.**
   - Superchargers: ask Supercharge.info for permission (it has power for all 155), or add the power tags in OSM.
   - Everything else: the network's typical figure, labelled as an estimate in the app.
2. **Add the missing sites to OSM.** Fill the 31 found here, and new builds as they open, from sources OSM allows: our own or users' visits, or networks that agree.
   - Copying from Google is not allowed, by Google or by OSM.
   - A "Report a charger" button in the app feeds this.
3. **Matching names:** treat NRMA / Chargefox and RAA / Chargefox as possibly the same site when the pins are within about 150 m.
4. **Stale sites:**
   - prefer sites checked recently;
   - show "last checked" to free users;
   - Premium checks chosen stops live (§5);
   - drop sites that users report gone.
5. **The safety net (§3 C)** for remote trips.

## 5. Live availability: who has it, and how to close the gap

**Measured through Google's API on these routes (473 fast sites, 2026-10-29):**

| Network | Sites with live status |
| --- | --- |
| Evie | 138 of 147 (94%) |
| Chargefox | 102 of 104 (98%) |
| bp pulse | 38 of 38 |
| Ampol AmpCharge | 27 of 27 |
| Exploren | 17 of 18 |
| Yurika (Queensland) | 7 of 7 |
| **Tesla Supercharger** | **0 of 78** |
| **NRMA** | **1 of 35** |
| Smaller networks (Bolt, OTR, eLu and others) | 2 of 10 |
| **All** | 338 of 473 (71%); **94% without Tesla and NRMA** |

**Tesla Superchargers:**
- **Google:** Tesla began sharing live stall data with Google Maps in November 2025. Tesla's support page says "globally" ([The Driven](https://thedriven.io/2025/11/13/tesla-finally-shares-supercharger-availability-data-with-google-maps-but-what-took-so-long/), [Not a Tesla App](https://www.notateslaapp.com/news/3318/tesla-supercharger-live-availability-added-to-google-maps)).
  - But Google's Places API returns none for Australian Superchargers today, so it isn't available to apps like ours.
  - The app already reads Google's live counts, so it would pick them up the day Google adds them. Re-check monthly.
- **Tesla owners:** the Fleet API's nearby Superchargers, with live stalls, for about 30 sites near the car. It's already in the app.
  - It could also show the next Supercharger stops' stalls during a trip, once they're in range.
  - Each call is Tesla API usage, so keep the rate low (the $20 a month cap).
- **Other EVs at Superchargers:** only Tesla's own app has the data. There's no public Tesla API.
  - HERE and PlugShare didn't have Tesla's live data as of November 2025 ([The Driven](https://thedriven.io/2025/11/13/tesla-finally-shares-supercharger-availability-data-with-google-maps-but-what-took-so-long/)).
  - Until then, the planner keeps treating Superchargers as very reliable. It already halves their failure chance.

**NRMA:**
- Live status is in NRMA's own app. NRMA said its co-funded sites would show live status on PlugShare too ([NRMA](https://www.mynrma.com.au/open-road/news/archived/introducing-the-nrma-app)).
- It isn't on Google's API (1 of 35).
- **Ask NRMA** for a data feed. OCPI 2.2.1 has a role for this, "navigation service provider", where a network sends its locations and live status. NRMA's members are its road-trippers, and it already publishes EV road-trip advice. A short email is worth sending.

**Other routes to live data:**
- **TomTom EV Charging Stations Availability API:**
  - **Coverage:** lists Australia with live ("EV Dynamic") data ([market coverage](https://docs.tomtom.com/ev-search-api/documentation/tomtom-orbis-maps/product-information/market-coverage)), refreshed every 3 minutes ([docs](https://docs.tomtom.com/ev-charging-stations-availability-api/documentation/product-information/introduction)).
  - **Price:** the 2026 pricing page shows free requests by the month (2,500 for Search) and no per-call price for EV availability ([pricing](https://docs.tomtom.com/pricing)). Older community posts quote US$0.75 per 1,000.
  - **Unknown:** which Australian networks it covers, and whether its terms allow showing the data on a Google map.
  - **Next step:** a free TomTom key from you, then a 30-minute test on a few Superchargers, NRMA and Evie sites.
- **Charge@Large (Electric Vehicle Council):**
  - Live status from smaller networks: Exploren, ChargeN'Go, Wevolt, Charge Hub, Sonic Charge, AGL, Charge Boss, Noodoe.
  - Shared with the NSW and WA governments. No public API, and at launch it didn't include Chargefox, Evie or Tesla ([Medianet](https://newshub.medianet.com.au/2025/03/real-time-ev-app-set-to-improve-charging-experience-coverage-and-reliability/91103), [The Driven](https://thedriven.io/2025/03/07/ev-lobby-launches-new-charging-app-to-displace-plugshare-with-real-time-availability)).
  - Worth asking for app access later. It would mostly add the small networks Google already misses.
- **HERE, Eco-Movement, PlugShare:** commercial, priced by quote, and Eco-Movement covers Oceania live ([Eco-Movement](https://www.eco-movement.com/)). Not worth it before there's revenue.
- **No government open data:** Australia has no live-data mandate. NSW's grants ask networks for operational and uptime reports; I found no requirement to publish live status ([NSW round 4 guidelines](https://www.energy.nsw.gov.au/sites/default/files/2025-12/202512-NSW-DCCEEW-EV-fast-charging-grants-round-4-funding-guidelines.pdf)).

**Recommended for the hybrid:**
- **Premium:** live status for each chosen stop, from Google by place ID (one Place Details call, US$25 per 1,000). Covers 94% of fast sites outside Tesla and NRMA.
- **Tesla owners:** their car's Supercharger stalls.
- **Free users:** network, plugs and "last checked", as on ABRP.
- **In parallel:** email NRMA, test TomTom, re-check Google for Tesla monthly.

## 6. Decisions for the user

1. **Hybrid:** go ahead? The free data plans as well as Google's in about 9 of 10 trips here, with no failures.
2. **Gap-fill:** drop the per-charger lookup (A). Keep only the safety net (C).
3. **Before switching:** fix kW, names and the missing sites (§4). Email Supercharge.info and NRMA.
4. **TomTom test:** create a free TomTom developer key and put it in `server/.env` as `TOMTOM_KEY` (not in the chat). Then I'll run the test.

## Sources

- **Measured here:** Google Places Text Search (along the route, full and IDs-only) and Place Details Essentials; Routes; OpenStreetMap via Overpass (`amenity=charging_station`, AU); Open Charge Map `/v3/poi?countrycode=AU` (2026-10-29).
- **Google pricing:** Text Search Essentials (IDs Only) and Place Details Essentials (IDs Only) are unlimited and free ([pricing](https://developers.google.com/maps/billing-and-pricing/pricing)). Field-to-SKU mapping on the [Text Search page](https://developers.google.com/maps/documentation/places/web-service/text-search).
- **Tesla and Google Maps:** [The Driven, 2025-11-13](https://thedriven.io/2025/11/13/tesla-finally-shares-supercharger-availability-data-with-google-maps-but-what-took-so-long/) · [9to5Google](https://9to5google.com/2025/11/12/google-maps-now-shows-live-tesla-supercharger-availability/) · [Tesla support page](https://www.tesla.com/support/charging/supercharger/google-map-integration) (not readable by the fetcher; quoted from search results)
- **NRMA:** [NRMA app](https://www.mynrma.com.au/open-road/news/archived/introducing-the-nrma-app) · [charging network](https://www.mynrma.com.au/cars-and-driving/electric-vehicles/charging-network)
- **Charge@Large:** [Medianet, 2025-03](https://newshub.medianet.com.au/2025/03/real-time-ev-app-set-to-improve-charging-experience-coverage-and-reliability/91103) · [The Driven, 2025-03-07](https://thedriven.io/2025/03/07/ev-lobby-launches-new-charging-app-to-displace-plugshare-with-real-time-availability)
- **TomTom:** [EV availability API](https://docs.tomtom.com/ev-charging-stations-availability-api/documentation/product-information/introduction) · [market coverage](https://docs.tomtom.com/ev-search-api/documentation/tomtom-orbis-maps/product-information/market-coverage) · [pricing](https://docs.tomtom.com/pricing)
- **HERE:** [EV Charge Points one-pager](https://assets.here.com/x7rx8ayph7ee/32b79353-8f28-4728-8a39-8f3dd91cd0bd/a942a7fadb8ea82c49e70f28e2c5db16/HERE_EVChargePoints_product_one_pager_2025.pdf)
- **Eco-Movement:** [site](https://www.eco-movement.com/)
- **NSW:** [EV fast charging grants, round 4 guidelines](https://www.energy.nsw.gov.au/sites/default/files/2025-12/202512-NSW-DCCEEW-EV-fast-charging-grants-round-4-funding-guidelines.pdf) · [TfNSW EV charging locations](https://opendata.transport.nsw.gov.au/dataset/ev-charging-locations)
