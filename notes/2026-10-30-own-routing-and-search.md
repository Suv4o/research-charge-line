# Our Own Routing and Address Search (Step 5) on Top of the Hybrid, Tested Against Google

**Date:** 2026-10-30
**For:** the user, choosing between the hybrid and the hybrid plus step 5 of [2026-10-29-cutting-google-costs.md](2026-10-29-cutting-google-costs.md): "do the exact same research but with hybrid + step 5 … that we only pay for the server … compare how it is comparing with Google API (the current implementation)".
**Step 5** replaces Google's routes with our own Valhalla and Google's address search with our own Photon, both running on OpenStreetMap on our server.

## Bottom line

- **Plans from our own routes work, but only after tuning.** Valhalla as it comes out of the box gets Australian driving speeds wrong, and the energy estimate with them.
  - **Its default speed table is too slow on highways.** It drives the Barrier Highway at 72 km/h although it's signed 110. Energy came out **10% low on the median trip, up to 27% low**, so plans stopped less often than they should. Unsafe.
  - **The posted limits are too fast.** Energy came out **10% high**; three Atto 3 plans to Broken Hill failed, and ETAs were 23 minutes short.
  - **Capped at 110 km/h, it found a shortcut over 99 km of dirt** (Ernest Giles Road to Uluru), past the only charger. Our router must stay on sealed roads.
- **Tuned (typical speeds, sealed roads), it's close to Google:**
  - The tuning:
    - each road timed at the speed drivers average on its limit, from Main Roads WA's surveys (101.9 km/h on 110 roads, 95.6 on 100);
    - 110 km/h at most;
    - no unsealed roads.
  - **Every one of the 252 test plans worked**, and none bent the driver's settings where today's didn't.
  - **81%** had the same number of stops as today's Google plans. The hybrid gets 90%.
  - **63%** took the same time (within 10 minutes or 3%). The hybrid gets 89%. Our ETAs are **8 minutes shorter on the median trip**: driving time is 2.6% shorter than Google's on the median route.
  - Energy is **3.8% higher than with Google's route** on the median trip: slightly cautious.
- **Address search (Photon) is good for places, weaker for street addresses:**
  - Tuned, its first answer matched Google's on **51 of 63** searches (81%), and the right place was among its five on **55** (87%).
  - Towns, typed prefixes, landmarks and businesses do well.
  - On street addresses it's 9 of 16 within 150 m, or 14 of 16 within 500 m. OpenStreetMap lacks some house numbers (250 High Street, **Kew**, came back as Thomastown), and a few places go by other names (the Penguin Parade).
- **The server: about US$34 a month (A$52)** on Fly in Sydney, measured:
  - Valhalla needs 600 MB of memory and 1.4 GB of tiles for Australia, rebuilt weekly in 6 minutes.
  - Photon needs about 1.2 GB of memory and 2.5 GB of data.
- **Money: step 5 pays only beyond about 2,100 active users** (about 9,000 trips a month). Below that, Google's free tiers already cover routes and address search, so the server is an extra cost.
  - At 10,000 users the Google bill is **US$968 a month for the hybrid**, against **US$472 for the hybrid plus step 5** (server included).
  - Without Premium's live checks, step 5 would cost **US$85**.
- **"Only pay for the server" is possible only without Google's live availability.** With step 5, the only Google costs left are:
  - Premium's live checks (one Place Details call per stop);
  - the safety net (Google's search when a free plan fails or bends). It changed no plan in this test, so it can go.
  - The map stays Google's, and it's free.
- **Recommendation:**
  - Ship the hybrid now. It has the better plan quality, and it cuts Google's bill by more than 90% at any size.
  - Keep step 5, as configured here, ready for when trips pass about 9,000 a month or Google's prices change. Before then it costs more than it saves, and its ETAs and street addresses are a step below Google's.

## 1. What changes

| | Today | Hybrid (steps 1–4) | Hybrid + step 5 |
| --- | --- | --- | --- |
| Chargers for planning, Chargers tab, CarPlay | Google search (US$40 per 1,000) | Our file on the phone | Our file on the phone |
| Route | Google (US$5 per 1,000, 10,000 free) | Google | **Our Valhalla** |
| Address search | Google (sessions + US$5 per 1,000 lookups, 10,000 free) | Google | **Our Photon** |
| Elevation | AWS terrain tiles (free) | same | same |
| Map | Google (free) | Google (free) | Google (free) |
| Live availability | Everyone, from Google | Premium, Google per stop; Tesla owners from the car | Same as the hybrid, or none |
| Send to Tesla place IDs | Google's free IDs-only search | same | same |

Step 5 also settles a terms question raised in the 29 October note: checking our own chargers against a Google route is an interpretation of Google's terms, and our own route removes it.

## 2. The test

**Method.** The same as 29 October, extended (app commit "Trial: our own routing and search", then removed; `-compare-own`).
- **Routes, cars and settings:** the same 21 routes, 4 cars and 3 "Plan for" settings, starting at 90%.
- **The free charger file** was rebuilt the same day: 2,213 sites, 1,130 of them fast.
- **Valhalla 3.9.1** ran in Docker with Geofabrik's Australia extract (2026-10-30), exactly as it would run on our server. It was set up five ways (§3).
- **Photon 1.3.0** ran in Docker with GraphHopper's Australia–Oceania 1.x database (built 2026-10-28), limited to Australia.
- **Each trip was planned by the app's own planner three ways:**
  - **today:** Google's route and Google's search along it, plus Open Charge Map within 2 km;
  - **hybrid:** Google's route and the free file within 10 km;
  - **own:** Valhalla's route and the free file within 10 km, for each Valhalla setup.
- **Elevation** came from the same AWS terrain tiles in every case.
- **Address search:** 63 searches, as a driver in Melbourne would type them:
  - 15 towns;
  - 8 town names half typed ("Wodo", "Goulb");
  - 12 landmarks;
  - 12 businesses and venues;
  - 16 street addresses.

  Google's first autocomplete answer, located with the app's own Place Details call, was the reference. Photon's answer counts as the same place within 5 km for a town, 1–25 km for a landmark (by its size), 0.5–3 km for a business and 150 m for an address.
- **Google calls used:**
  - 172 paid searches over two full runs (at most about US$6.90, or free within the month's 1,000);
  - 126 routes, and 126 autocomplete sessions with one Place Details call each, all inside Google's free tiers.
- Google's results stayed in the app's memory and console, and the logs were deleted. This note has aggregates only.

## 3. Routes: Valhalla against Google

Valhalla gets the roads right. On 15 of 21 routes, at least 95% of each route is within 1 km of the other. The differences are real alternatives:
- **Perth → Geraldton:** the coast road instead of the Brand Highway.
- **Sydney → Eden:** down the coast, 65 km shorter than Google's inland way.
- **Sydney → Dubbo:** past Mudgee, Valhalla takes Goolma Road. About half the route differs.
- **Melbourne → Lakes Entrance:** a different road for part of Gippsland (71% the same).
- **Hobart → Strahan:** part of the way.

Distance is within 0.2% on the median route.

**Speed is the problem.** The energy model reads speed from the route's times, so the times decide the plan. Five setups:

| Valhalla setup | Driving time vs Google (median, range) | Energy vs Google's route (median, range) | Plans that failed |
| --- | --- | --- | --- |
| As its Docker image builds it (OpenStreetMapSpeeds table) | +8.7% (−1 to +33%) | **−10% (−27 to +3%)**: too optimistic | 0 |
| Posted limits | −9.8% (−19 to −7%) | +10% (−16 to +26%) | 3 (Atto 3 to Broken Hill) |
| Posted limits, 110 at most | −8.4% | +9% | 15 (dirt road to Uluru; Atto 3 to Broken Hill) |
| Typical speeds (110 at most) | −2.6% (−16 to +8%) | +3.8% (−17 to +14%) | 6 (dirt road to Uluru) |
| **Typical speeds, sealed roads only** | **−2.6% (−14 to +8%); within 5% on 17 of 21** | **+3.8% (−17 to +21%)** | **0** |

- **Why the default is slow:** the image uses OpenStreetMapSpeeds' table, which overrides posted limits. For rural Australia that table gives 102 km/h on motorways and 79 or less on other highways. The Barrier Highway is tagged 110 km/h for 96% of its length, but Valhalla drove it at 72.
- **Typical speeds:** Main Roads WA's surveys of free-flowing traffic (2000–2018, over a million vehicles each) give mean speeds by speed limit:

  | Limit (km/h) | 60 | 70 | 80 | 90 | 100 | 110 |
  | --- | --- | --- | --- | --- | --- | --- |
  | Mean free speed (km/h) | 57.6 | 65.8 | 74.6 | 85.5 | 95.6 | 101.9 |

  - Each road on the route is timed at the speed for its limit. Roads without a limit, or under 60, keep Valhalla's speed.
  - 130 roads count as 110, since EV drivers rarely hold 130.
  - This uses independent data, not Google's: Google's times were used only to judge the result.
- **Sealed roads only** is Valhalla's `exclude_unpaved` option. Without it, capping speeds at 110 made Alice Springs → Uluru 99 km of Ernest Giles Road dirt, past the only charger (Erldunda).
- **The largest remaining differences:**
  - **Hobart → Strahan:** our time is 14% short, and energy 17–21% high. The Lyell Highway is signed 100 but winds; speed limits can't show curves.
  - **Sydney → Eden:** 17% less energy, because the coast route is 12% shorter. The plan is consistent with the route it uses. "Navigate in Google Maps" passes the stops, which keeps Google on the same road.
  - **Darwin → Katherine:** 7.5% slower than Google's time.
- **Speed:** a long route took Valhalla 120 ms on the median (233 ms at most) on a Mac. It would be a few times slower on a small server, still well under a second.
- **Alternatives:** Valhalla offered 19 alternative routes on 11 routes; Google offered 20 on 14.

## 4. Plans

Same 252 plans as the 29 October test (21 routes × 4 cars × 3 "Plan for").

| | Hybrid vs today | Own (tuned) vs today | Own (tuned) vs hybrid |
| --- | --- | --- | --- |
| Plans that worked | 252 / 252 | **252 / 252** | 252 / 252 |
| Bends the driver's settings where the other doesn't | 0 | **0** | 0 |
| Same number of stops | 226 (90%) | **204 (81%)**; 18 more, 30 fewer | 219 (87%) |
| Same time (within 10 min or 3%) | 225 (89%) | **160 (63%)**; 75 quicker, 17 slower | 189 (75%) |
| Total time, median (range) | 0 min (−43 to +34) | **−8 min (−57 to +32)** | −8 min (−35 to +34) |
| Driving time, median (range) | 0 (−18 to +30) | −9 (−35 to +11) | −9 (−35 to +14) |
| Charging and stop time, median (range) | 0 (−46 to +27) | **0 (−48 to +36)** | 0 (−20 to +31) |
| Stops at sites Google doesn't list | 21 of 373 (6%) | 32 of 376 (9%) | |

- **The plans agree; the clocks differ.** Charging time is the same on the median trip. Most of the time difference is our driving times running about 3% under Google's.
  - Routes where our ETA is clearly shorter: Melbourne → Sydney (29 min), Sydney → Eden (28 min, the coast road), Hobart → Strahan (35 min, the winding road).
  - Routes where it's longer: Alice Springs → Uluru (12 min) and Darwin → Katherine.
- **Different stops** come mostly from different roads (Sydney → Eden: 12 stops over the 12 plans against 18) and from speed:
  - Darwin → Katherine: 6 against 14;
  - Brisbane → Rockhampton: 24 against 27;
  - Perth → Kalgoorlie: 29 against 25.
- **The untuned setups:**
  - **Default table:** 72% the same stops, 69 plans with fewer stops, 36% the same time, 18 minutes slower on the median.
  - **Posted limits:** 72% the same stops, 48 plans with more, 11% the same time, 23 minutes quicker.
- **Safety net:** the tuned plans had a problem (no plan, or bending the driver's settings) in 3 of 252 cases (1.2%). Google's search along our route changed none of them, so a server-only version can drop it.

## 5. Address search: Photon against Google

**63 searches.** Each cell gives the first answer matching Google's, then (in brackets) whether the right place was among Photon's five.

| | Photon's defaults | Tuned (`zoom=6`, `location_bias_scale=0.6`) |
| --- | --- | --- |
| Towns (15) | 11 (12) | **13 (14)** |
| Typed prefixes (8) | 4 (5) | **8 (8)** |
| Landmarks (12) | 8 (10) | **10 (11)** |
| Businesses and venues (12) | 11 (11) | **11 (11)** |
| Street addresses (16) | 10 (11) | 9 (11); **14 within 500 m** |
| **All (63)** | **44 (49), 70%** | **51 (55), 81%** |

- **Why the tuning:** with the defaults, a searcher in Melbourne gets Melbourne streets before towns: "Esperance" gave Esperance Avenue, "Albu" Albury Road, "Australia Zoo" Melbourne Zoo. More weight on how important a place is fixes that.
- **Where tuned Photon still differs from Google:**
  - **Different answer, arguably better:** "Katherine" and "Bright" give the towns; Google gave Katherine Place (Melbourne) and Brighton.
  - **Right place, pin a little off:** "Twelve Apostles" gives the marine park, 4.5 km away (the lookout is in its five).
  - **Missing names:** OSM has no "Penguin Parade" under that name, and no "BIG4 Bright Holiday Park".
  - **Addresses at big sites:**
    - 1341 Dandenong Road (Chadstone), 352 Princes Highway (Fountain Gate), 159 Church Street (Westfield Parramatta) and 100 Barnard Street (Bendigo Hospital) land 180–470 m from Google's pin. That's the same place for a driver.
    - 300 Unley Road gives the street (190 m).
  - **Wrong:** "250 High Street Kew" gives 250 High Street in Thomastown, because OSM lacks the Kew one. "120 Collins Street Melbourne" puts Thornbury's first; the city one is second.
- **Labels must show the suburb.** Photon calls every Melbourne suburb "Melbourne". Its `district` and `postcode` fields carry the suburb ("250 High Street, Thomastown VIC 3074"), and the app should show those.
- **Speed:** 16 ms per search on the median (64 ms at most) on a Mac.
- **Fixes for addresses, if needed:**
  - a "Search Google" row when Photon's answers aren't right. It would cost only for those searches, inside Google's 10,000 free lookups for a long time.
  - Addressr, which is self-hosted search over G-NAF (Australia's open address file, 15+ million addresses, CC BY 4.0). It's another OpenSearch, needing about 1.4 GB of memory.

## 6. The server

Measured on this Mac in Docker:

| | Valhalla (Australia) | Photon (Australia–Oceania DB) |
| --- | --- | --- |
| Download | 972 MB OSM extract, daily from Geofabrik | 1.9 GB database, weekly from GraphHopper |
| Build | 5.5–6 min on 6 threads, **about 6 GB memory at peak** | none: unpack (100 s) |
| On disk | 1.4 GB of tiles | 2.5 GB (less, imported for Australia only) |
| Memory serving | about 600 MB | about 1.2 GB (Java heap capped at 2 GB) |
| Start | 18 s (the image checks its files first) | 4 s |

- **Fly, Sydney (prices × 1.269 for `syd`):** two shared-cpu-1x machines with 2 GB each, US$16.10 a month each, plus about 9 GB of volumes (US$1.35). **About US$34 a month.**
  - One shared-cpu-2x machine with 4 GB costs the same.
  - Both should stay running; neither starts fast enough to wake on a driver's first request.
  - Our existing Tesla server stays as it is.
- **Weekly update:**
  - **Valhalla:** rebuild the tiles on a short-lived 8 GB machine (about 15 minutes, a few cents), then swap them in.
  - **Photon:** download the weekly database, or import Australia only from GraphHopper's JSON dump.
  - **Charger file:** built daily, as in the hybrid.
- **Server code the tuning needs:** Valhalla's route, then `trace_attributes` on it, to time each road at the typical speed for its limit. Requests ask for `top_speed: 110` and `exclude_unpaved: true`. Valhalla must be built **without** the OpenStreetMapSpeeds table.
- **If our server is down,** fall back to Google's route and search for those requests. They stay inside Google's free tiers.

## 7. Cost per month

Same assumptions as the 29 October note:
- 5% Premium;
- free users make 4 charging trips a month, Premium users 8;
- each trip needs 1.5 routes and 1.5 destination lookups;
- Premium live checks are 3.5 per trip plus 5 tapped chargers;
- the safety net runs on 1.2% of trips.

US$:

| Active users | Hybrid | Hybrid + step 5 (incl. US$34 server) | Hybrid + step 5, no live availability | Premium revenue |
| --- | --- | --- | --- | --- |
| 500 | ~0 | ~34 | ~34 | ~90 |
| 2,000 | ~84 | ~92 | ~34 | ~350 |
| 10,000 | ~968 | ~472 | ~85 | ~1,755 |
| 50,000 | ~5,500 | ~2,485 | ~450 (~34 without the safety net) | ~8,775 |

- In the hybrid, Google's bill at scale is about half routes and address search, and half Premium's live checks. Step 5 removes the first half for a flat US$34.
- **Break-even is about 2,100 active users** (about 9,000 trips a month), where routes and address search outgrow Google's free 10,000 calls each.
- The 29 October note estimated US$45 for hosting; measured, it's about US$34.

## 8. Licences and terms

- **OpenStreetMap (ODbL):**
  - OSMF's guidelines: "Routing engines that use OpenStreetMap data must credit OpenStreetMap", and so must geocoders and apps that use them.
  - The app adds "© OpenStreetMap" where routes and search results show, as it will for the charger file.
- **Software:** Valhalla is MIT, Photon is Apache 2.0, and the survey speeds are a published Main Roads WA report.
- **Public servers:** the free public Valhalla and Photon servers (FOSSGIS's, komoot's) are shared, best-effort services, not something to build an app on. This is why step 5 means our own server.
- **Google:**
  - Our route and our chargers on Google's free map are fine.
  - Premium's live availability stays Google content next to a Google map, as in the hybrid.

## 9. Risks

- **ETA and energy depend on our speed model.**
  - Winding roads (Tasmania) look faster than they are, which is cautious for energy but optimistic for arrival time.
  - Check the model against real drives: the user's Tesla trips and "Learn from my trips".
- **Route choices** differ from Google's on about a quarter of routes. They're sealed and plausible, but sometimes slower in reality.
- **Street addresses** depend on OpenStreetMap's house numbers. Add a Google fallback or G-NAF if users report misses.
- **Running a server:** weekly updates, monitoring, and memory for Photon. Google stays as the fallback.
- **Work:** about 1–1.5 weeks on top of the hybrid.
  - Server: Valhalla with the speed tuning, Photon, the weekly builds and fallbacks.
  - App: a route source and search source that can switch between ours and Google's, suburb labels, and OSM credit.
  - Then this test again.

## 10. Decision

| | Hybrid | Hybrid + step 5 |
| --- | --- | --- |
| Plans that work | 100% | 100% |
| Same stops as today | 90% | 81% |
| Same time as today | 89% | 63% (ETAs 3% shorter on the median) |
| Address search | Google, as today | 81% the same first answer (87% in its five); addresses weaker |
| Google bill, 10,000 users | ~US$968 | ~US$438 + US$34 server, or ~US$85 without live checks |
| Work | 2–3 weeks | +1–1.5 weeks |
| New upkeep | the daily charger file | plus a routing and search server, updated weekly |

**Recommended:** the hybrid now, with step 5 configured as above and switched on when trips approach 9,000 a month. If the goal is a bill that's only the server from day one, choose the hybrid + step 5 without live availability, and accept the lower ETA and address quality above.

## Sources

- Valhalla: [speeds](https://valhalla.github.io/valhalla/concepts/speeds/) · [releases](https://github.com/valhalla/valhalla/releases) · OpenStreetMapSpeeds table: `https://raw.githubusercontent.com/OpenStreetMapSpeeds/schema/master/default_speeds.json`
- Photon: [API (location bias)](https://github.com/komoot/photon/blob/master/docs/api-v1.md) · [releases](https://github.com/komoot/photon/releases) · [GraphHopper's Photon dumps](https://download1.graphhopper.com/public/)
- OpenStreetMap: [Geofabrik Australia extract](https://download.geofabrik.de/australia-oceania/australia.html) · [OSMF attribution guidelines](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines)
- Speeds: [Main Roads WA, Trends in driver speed behaviours on rural road network 2000 to 2018](https://wa.gov.au/system/files/2021-08/RSC_Rural-General-Speed-Survey-FINAL.PDF) (March 2019)
- Addresses: [Addressr (G-NAF)](https://github.com/mountain-pass/addressr)
- Hosting: [Fly pricing](https://fly.io/pricing.md) (Sydney multiplier 1.269; volumes US$0.15 per GB-month)
- Google prices: as quoted in [2026-10-13-trip-planner-data.md](2026-10-13-trip-planner-data.md) §1.5–1.6
