# Charging Prices per Network and per Site: What Can Be Kept Current

**Date:** 2026-11-14
**For:** the owner, deciding whether the planned price agent can do more than keep one typical price per network
**Question:** Can Charge Line keep each network's price current, and ideally each site's price, from published sources? Or is that too much, or not possible?
**How to read it:** every fact is followed by the page that owns it, read on 14 November 2026. I read each network's terms of use before any of its price pages, and stopped at any site whose terms forbid automated reading or which refused an automated reader. "Search result" marks a fact taken from a search engine's summary of a page I did not open. "Not verified" marks what I could not confirm from a primary source. Costs marked "estimate" are my arithmetic, not measurements.

## Bottom line

- **Per-site prices for every network: not possible.** Almost every network shows a site's price only in its own app, and none has a public price feed.
  - The one exception among the big networks is **NRMA**. Its public charging page has a table of location, state and price (85 priced rows) ([NRMA charging](https://www.mynrma.com.au/electric-vehicles/charging)). Its terms let you read it, but not copy it into an app without permission (§1.6).
  - Google Places still has no EV price field. `evChargeOptions` holds connectors, power and live availability; the only price fields are `priceLevel`, `priceRange` and petrol's `fuelOptions` ([Places API reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places)).
  - The NSW, Victorian and Queensland charger datasets have no price field (§2.3).
  - Roaming feeds (OCPI) carry tariffs, but only to partners with a commercial roaming agreement (§2.2).
- **The planned weekly agent has less to read than §4.2 of the 12 November note assumed.** Of the seven networks whose pages the 27 October note cites, only NRMA's page is both readable by an agent and holds prices:
  - **Chargefox and Jolt forbid robots or scraping in their terms.** Chargefox: no "robot, spider, scraper or other automated measures" ([Chargefox terms, cl. 6](https://www.chargefox.com/terms-and-conditions)). Jolt: "not attempt to scrape… data-mine" ([Jolt terms, cl. 4.1(f)](https://joltcharge.com/au/terms/)). So does Exploren, which the agent was meant to add: no "data mining, robots, screen scraping" ([Exploren terms, cl. 3.7(d)](https://exploren.com.au/terms-and-conditions)).
  - **Tesla, bp pulse and Evie's old help centre refuse automated readers** (HTTP 403). I did not try to get around that.
  - **Ampol and Evie publish no prices on their websites.** Both send drivers to the app.
  - That leaves NRMA's table, news coverage of announced price changes, a few government pages, and Open Charge Map.
- **What is realistically possible:**
  - **(a) A typical price per network, checked monthly or weekly: yes, with a narrower method.** The agent reads only allowed sources, and opens a pull request only when one of them supports a change. Otherwise it opens an issue for you to check in the network's app. Running cost: about 5–10 page reads and a few searches a week, on the Claude plan (A$0 extra).
  - **(b) Per-site prices: for a small share of sites only.**
    - Open Charge Map entries checked in the last 12 months (CC BY, already used): about 1 fast site in 10 (27 October sample).
    - NRMA's 85 sites (about 7% of the ~1,190 fast sites in Charge Line's file), **only with NRMA's written permission**.
    - Prices drivers report in Charge Line. These are legally clean, and they grow with users.
  - **(c) Not possible:** per-site prices for Tesla, Chargefox and its site owners (including RAC, Electric Highway Tasmania and the Queensland Electric Super Highway), Evie, Ampol, bp pulse, Jolt and Exploren. Also not possible: time-of-day or live prices for any network.
- **Recommendation:** keep the current approach: the driver's own price first, then Open Charge Map when recent, then the network's typical price. Add three things:
  1. A `prices.json` with a source, a checked date and a basis (`published`, `survey` or `estimate`) on every number. Per-site entries go in only from sources that allow reuse (§6).
  2. A "price you paid" field in the existing charger report, so drivers fill in per-site prices.
  3. An email to NRMA asking for permission to use its published table. Later, after the Ampol–Evie merger, ask Ampol the same.
- **A cross-check worth acting on now:** CarsGuide's Sydney peak survey (15 July 2026) found several networks above Charge Line's typical prices. Evie was $0.70–0.75 against 0.69, bp pulse $0.66–0.79 against 0.65, and Tesla $0.79 at 300 kW+ against 0.55/0.65 ([CarsGuide in the Canberra Times](https://www.canberratimes.com.au/story/9318653/cost-of-fast-charging-your-electric-car/)). Sydney at peak is the dear end, so it isn't a reason to change the numbers by itself. But under the "never promise less than the driver pays" rule, it is worth a check in the apps.

## 1. Network by network

### 1.1 Tesla Supercharger (about 150–155 sites)

- **Where prices are:** the Tesla app, per site and by the time of day. The 27 October note found Tesla prices "dynamically" per site.
  - Tesla's support page "Understanding Live Pricing at Our Charging Sites" describes prices that follow how busy a site is (search result, [Tesla](https://www.tesla.com/support/charging/understanding-live-pricing)). The coverage found is about US sites. **Not verified** for Australia.
  - Example of the spread: before 8am at Braybrook, $0.27 per kWh for Teslas and $0.37 for other EVs; at Osborne Park, "as low as $0.32" for Teslas ([The Driven, 22 Apr 2026](https://thedriven.io/2026/04/22/tesla-opens-two-new-supercharger-stations-as-fast-charging-costs-hit-new-low-of-27c-kwh/)).
- **Per-site public without logging in:** no source found. tesla.com returned HTTP 403 to my reader for the Australian terms page and the Supercharging support page, so I stopped.
- **Machine-readable:**
  - The Fleet API has no public price list. `charging_sessions` "Returns the charging session information including pricing and energy data", but "is only available for business accounts that own a fleet of vehicles" ([Fleet API charging endpoints](https://developer.tesla.com/docs/fleet-api/endpoints/charging-endpoints)).
  - `charging_history` returns a car's own past sessions. The `vehicle_charging_cmds` scope covers "Vehicle charging history, billed amount, charging location" ([Fleet API scopes](https://developer.tesla.com/docs/fleet-api/authentication/overview)). Charge Line's Tesla app doesn't request that scope today.
  - So a Tesla driver who links their car could have their own past Supercharger prices filled in. That is per driver, not a public source. **Not verified:** whether the history includes kWh, so a price per kWh can be worked out.
- **Terms:** not readable by an automated reader (403).
- **Number of sites:** "over 150" after the 150th opened in April 2026, about 155 by June (search result, third-party guides via [Gridly](https://www.gridly.com.au/blog/ev-charging-networks-australia)). **Not verified.**
- **Verdict:** per-network typical only, from news and surveys. No per-site prices.

### 1.2 Evie Networks (322 sites; being bought by Ampol)

- **Terms:** updated 29 September 2026. They limit what you may do with the app, not the website. The price is "Evie's rates… as shown on its Website, in the App" (cl. 5.3(b)), and "Evie may amend the standard rates… from time to time" (cl. 5.3(c)), with no notice period stated. Idle fees are "at the rate set out on our Website and in the App" (cl. 5.4(a)) ([Evie terms](https://evie.com.au/terms-of-service/)).
- **robots.txt:** allows everything except admin paths, with `Crawl-delay: 10` ([robots.txt](https://evie.com.au/robots.txt)).
- **Where prices are:** in practice, only the app.
  - The charger finder and the city pages list sites but no prices ([find a charger](https://evie.com.au/find-a-charger/), [Melbourne](https://evie.com.au/ev-charging-stations-melbourne/)).
  - The finder's results appear to come from a WordPress store-locator plugin. Its data endpoint is undocumented, so I didn't call it.
  - The cost FAQ (dated 12 July 2023) gives dollars per session, not per kWh, and says "Always check the Evie app for up-to-date pricing by clicking on a site to view specific pricing for each connector" ([Evie FAQ](https://evie.com.au/faq/how-much-does-it-cost-to-charge/)).
  - The old help article cited on 27 October (support.goevie.com.au) now returns 403. goevie.com.au redirects to evie.com.au.
- **Per-site public:** no.
- **Changes:**
  - Rises in July 2023 and on 18 January 2024: 50 kW from 50c to 58c, 350 kW from 65c to 73c (search result, [The Driven](https://thedriven.io/2024/01/14/evie-increases-public-charger-pricing-by-an-average-of-21/)). No 2025–26 network-wide change found.
  - On 1 October 2026 Ampol agreed to buy Evie for A$225 million: 322 sites and 1,031 bays. Completion is expected in the first half of 2027, subject to approval (search result, [electrive](https://www.electrive.com/2026/10/01/ampol-to-acquire-evie-networks-in-au225m-deal/)). Expect pricing changes after completion (inference).
- **ACT:** ActewAGL partners with Evie. Its FAQ says ACT drivers "can typically expect to pay $0.50/kWh to $0.80/kWh" for fast DC (search result, [ActewAGL FAQ](https://www.actewagl.com.au/news-and-info/information/electric-vehicle-faq)).
- **Verdict:** per-network typical only. The website could legally be read, but it holds no current price.

### 1.3 Chargefox and the sites it runs for others (often called the largest network; site count not verified)

- **Terms** (end user terms, PDF dated 16 February 2026), cl. 6: users must not "use any robot, spider, scraper or other automated measures to access or use the Chargefox App or the Chargefox Website", nor "modify, copy, distribute, transmit, display, reproduce, publish… any information contained on, or obtained from, the Chargefox App or the Chargefox Website" ([Chargefox terms](https://www.chargefox.com/terms-and-conditions), which redirects to the PDF). **I stopped reading chargefox.com here.**
- **Where prices are:** cl. 3(c): "Usage Fees are set by charging station owners / operators (CPOs) and are typically based on a 'cents per kWh' rate. Usage Fees can be found on the 'Location details' screen on the Chargefox App." Idle fees are on signage or the same app screen (cl. 3(d)).
- **Sites whose prices sit only in the Chargefox app:**
  - **RAC (WA):** "we're bringing the project to an end"; the remaining RAC stations "are part of Chargefox", and members save 20% ([RAC](https://rac.com.au/about-rac/community-programs/ev-charging-stations)).
  - **Electric Highway Tasmania:** NRMA has owned it since 1 September 2025; for prices "please refer to the Chargefox app" ([NRMA](https://www.mynrma.com.au/electric-vehicles/charging/electric-highway-tasmania)).
  - **Queensland Electric Super Highway** (Yurika, Energy Queensland): pricing "can be found on the Chargefox App" (search result, [Yurika](https://www.yurika.com.au/qld-electric-super-highway)). The Queensland government's EV snapshot reported that on 30 June 2024 the 50 and 75 kW rate rose from 30c to 55c per kWh (search result, [Qld EV snapshot March 2025](https://www.qld.gov.au/transport/projects/electricvehicles/electric-vehicle-snapshot/electric-vehicle-snapshot-march-2025)). **Not verified:** a later URL on the same site returned 404.
  - **EnergyAustralia's 7-Eleven sites** (10 planned) are reached through Chargefox (search result, [EnergyAustralia](https://www.energyaustralia.com.au/about-us/media/news/ultra-fast-ev-charging-set-become-more-convenient-7-eleven-stores)).
  - Partner networks (bp pulse, EVX, AGL, NRMA) show in the Chargefox app through roaming (search result, [Chargefox](https://www.chargefox.com/news/innovation-finalist)).
- **Changes:** site owners can change prices at any time. The last widely reported Chargefox-owned rises were in 2023: 20 of its 50 kW stations went from 40c to 45c in March, and ultra-rapid from 40c to 60c in May (search result, [CarExpert](https://carexpert.com.au/car-news/australias-biggest-ev-charge-network-ups-prices-at-a-raft-of-locations), [carsales](https://business.carsales.com.au/news-room/archive/chargefox-ev-fast-charging-prices-rise-by-50-per-cent/)).
- **Machine-readable:** an OCPI interface for roaming partners. A third-party API catalogue lists a "Chargefox OCPI CPO API" with locations and tariffs, with access by commercial roaming agreement and no developer sign-up (search result, [apis.io](https://apis.io/apis/chargefox/chargefox-ocpi-cpo-api/)). **Not verified** from Chargefox.
- **Verdict:** can't, either per site or by reading Chargefox's pages. Per-network typical only, from news, surveys and Open Charge Map.
  - A caution: copying a price out of the Chargefox app into Charge Line is also "information… obtained from… the Chargefox App". Use typical figures from other sources.

### 1.4 Ampol AmpCharge (over 120 sites; about 400 with Evie)

- **Website terms:** "You may only use the material on the Website for personal non-commercial purposes", and "You must not reproduce, adapt, distribute, store in a retrieval system, transmit, print, publish, commercialise… any material on the Website". No date and no clause about robots ([Ampol website terms](https://ampcharge.ampol.com.au/policies/website-terms-and-conditions)).
- **App terms** (7 July 2023): no "data mining, gathering or extraction tools" with the app (cl. 14.3(c)) ([app terms](https://ampcharge.ampol.com.au/policies/app-terms-and-conditions)).
- **Where prices are:** the app. The site finder shows no prices ([find a charging station](https://ampcharge.ampol.com.au/find-a-charging-station)).
- **Changes:** from 19 October 2026, business AmpolCard holders get 4c per kWh off at AmpCharge (search result, [Finder](https://www.finder.com.au/news/ampolcard-now-includes-ampcharge-oct-2026)). That's a fleet discount and doesn't change the typical price.
- **Verdict:** per-network typical only, from news and surveys.

### 1.5 bp pulse (about 290 bays)

- **Where prices are:** the bp pulse app. Some NSW sites have time-of-day prices (search result, [CarExpert](https://carexpert.com.au/car-news/when-its-cheaper-to-charge-your-electric-car-at-bp-pulse-stations)).
- **Terms and site:** the bp.com FAQ cited on 27 October now redirects to bppulse.com, which returned HTTP 403. I stopped there.
  - bp.com's legal notice says "You may download material displayed on this website for your use only", and you "may not distribute, modify, transmit, reuse, repost, or use the content of this website for public or commercial purposes" ([bp legal notice](https://www.bp.com/en_au/australia/home/legal-notice.html)).
  - **Not verified:** bppulse.com's own Australian terms.
- **Verdict:** per-network typical only.

### 1.6 NRMA (85 priced rows on its page; a few sites appear in more than one table)

- **Terms:** "You must not reproduce any of the material contained on this web site", except a copy on your own computer or printed extracts "for your personal use" (cl. 2.1). Nor may you "incorporate into or store in any other web site, electronic retrieval system" (cl. 2.2). There's no clause about robots or automated access ([NRMA general conditions](https://www.mynrma.com.au/general-conditions)).
- **Where prices are: on the public page, per site.**
  - Tables with columns "Location | State | Price": 85 priced rows. $0.69 at 50 sites, $0.75 at 24, $0.79 at 9, and one each at $0.89 and $0.99.
  - There are also tables without prices ("Coming very soon", Tap&Pay, upgraded sites).
  - "Location-based variable pricing is now live across all chargers on the network."
  - The page also says: "Please refer to the My NRMA app to view charger-specific pricing."
  - Members get "5c/kWh off when paying through the My NRMA app".
  - The displayed price is the one paid "as a Lite member" or by tapping a card. Prices in the Chargefox app may differ.
  - ([NRMA charging](https://www.mynrma.com.au/electric-vehicles/charging))
- **Format:** one price per site. No kW, no DC/AC column and no time of day. Locations are names ("Bankstown RSL", "Camooweal") without coordinates, so matching them to Charge Line's chargers means matching names, which needs review.
- **Changes:**
  - Location-based pricing "Starting in April 2025".
  - "In August 2025", network-wide rate changes, and the 10% member discount became 5c per kWh ([network updates](https://www.mynrma.com.au/electric-vehicles/charging/network-updates), [price update, 28 July 2025](https://www.mynrma.com.au/open-road/advice-and-how-to/ev-charging-price-update)).
  - The page has a "Brand new locations and price updates" table, so per-site changes are ongoing.
- **Verdict:**
  - **Per-network typical: yes.** The table supports "usual range $0.69–0.79", so 79c under the rule (§5), which matches today's figure.
  - **Per site: possible only with NRMA's permission.** Storing and showing 85 prices is the "store… in any… electronic retrieval system" the terms forbid.

### 1.7 Jolt (about 100 sites)

- **Terms:** "not attempt to scrape, decompile, data-mine, reverse engineer" (cl. 4.1(f)); "Competitors are not permitted to use or access any information or content on the JOLT Website or the JOLT App" (cl. 11.1) ([Jolt terms](https://joltcharge.com/au/terms/)). I stopped reading Jolt's site here.
- **Where prices are:** the app. Per the terms, "Any charging in addition to the free daily 7 kWh usage is subject to payment of fees" (cl. 3.4). Jolt says the app shows each station's rate (search result, [Jolt support](https://support.joltcharge.com/hc/en-us/articles/16605135373847-Charging-Costs-Fees)).
- **Changes:** Jolt dropped its unlimited plan and raised its 10 kWh plan by 50%; the free 7 kWh "remains unchanged, for now" (search result, [Zecar](https://zecar.com/reviews/jolt-surprises-ev-owners-unlimited-plan-axed-50-price-rise-10kwh-plan), undated).
- **Verdict:** per-network typical only, from news and Open Charge Map. The agent must not read Jolt's site.

### 1.8 Exploren (about 400 locations, mostly AC; 300 fast ports bought from ENGIE)

- **Terms** (header "Last updated 2 September 2026"): drivers must not use "data mining, robots, screen scraping or similar data gathering and extraction tools on the Platform" (cl. 3.7(d)).
  - Site hosts set the tariff, "by time spent or energy used" (cl. 11.3), and "have full control over the setting of the Tariff" (cl. 11.8(a)).
  - The tariff is shown in the Exploren app (cl. 9.3).
  - ([Exploren terms](https://exploren.com.au/terms-and-conditions))
- **Related:** "EVSE" (evse.com.au) is the same company, EVE Australia Pty Ltd (search result, [Uber](https://www.uber.com/au/en/blog/evse-terms-and-conditions/)).
- **Verdict:** can't, per site or by reading Exploren's site. Count its sites as "other fast" or "other slow".

### 1.9 Smaller networks

| Network | What I found | Verdict |
| --- | --- | --- |
| Ausgrid / EVX (kerbside AC) | $0.50 per kWh "As of December 2023"; the EVX app is needed (search result, [Wollongong council](https://wollongong.nsw.gov.au/places/parking-transport/parking/kerbside-ev-chargers/faq-accordions/how-much-does-it-cost-and-how-do-i-pay)) | "Other slow" covers it |
| Everty (AGL since January 2025) | Software for hosts, who "fix their own pricing" (search result, [iTWire](https://itwire.com/science-news/automotive/ev-software-specialist-everty-charged-up-for-the-years-ahead)) | Per-site hosts; can't |
| Origin | No public fast network found; its offers are home charging (search result, [The New Daily](https://www.thenewdaily.com.au/finance/consumer/2024/05/14/origin-energy-ev-power-up)) | Not a network |
| EnergyAustralia × 7-Eleven | 10 sites planned, through Chargefox (§1.3) | As Chargefox |
| Queensland Electric Super Highway | Chargefox app; occasional price news in Queensland government snapshots (§1.3) | Per-network typical from government reports |

## 2. Machine-readable sources

### 2.1 Google Places

- No price per kWh. `EVChargeOptions` has `connectorCount` and `connectorAggregation[]`; each aggregation has `type`, `maxChargeRateKw`, `count`, `availableCount`, `outOfServiceCount` and `availabilityLastUpdateTime`.
- The only prices are `priceLevel`, `priceRange` and `fuelOptions.fuelPrices` ("per liter elsewhere") ([Places API reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places)).
- **Not verified:** whether the Google Maps app shows EV prices in Australia. Even if it does, the API doesn't expose them.

### 2.2 Roaming (OCPI, Hubject, Gireve)

- OCPI carries locations and tariffs between networks and the apps their drivers pay through.
- In Australia, Chargefox roams with "bp pulse, EVX, AGL, and the NRMA" (search result, [Chargefox](https://www.chargefox.com/news/innovation-finalist)), behind roaming agreements (§1.3).
- No Australian Hubject or Gireve connection found. Hubject's recent announcements are about other regions (search result, [Hubject](https://www.hubject.com/blog-posts/road-expands-international-charging-coverage-via-hubject)).
- **Verdict:** OCPI tariffs reach a trip planner only through a business deal with each network, as the 27 October note found. Not a route for a sole developer now.

### 2.3 State and federal open data

| Dataset | What's in it | Price field? |
| --- | --- | --- |
| NSW "EV Charging Locations" (TfNSW) | "the number of chargers, plug types, and power specifications"; "Chargers are only government funded chargers"; quarterly; updated 13 October 2026; CC BY ([TfNSW](https://opendata.transport.nsw.gov.au/dataset/ev-charging-locations)) | No |
| Victoria "Government Funded Public EV Chargers" | "locations, sizes (kW), plug types, and owners"; updated 11 November 2026; CC BY 4.0 ([DataVic](https://discover.data.vic.gov.au/dataset/government-funded-public-ev-chargers)) | No |
| Queensland "Find a charging station" | Super Highway locations; last updated 16 September 2022 (search result, [data.qld.gov.au](https://data.qld.gov.au/dataset/find-a-charging-station-electric-vehicle)) | No |
| EV Council national charging road map | A$1.43 million project announced 13 October 2026, due mid-2027; about where demand will be ([CommBank](https://www.commbank.com.au/articles/newsroom/2026/10/national-plan-to-put-electric-vehicle-charging-on-a-map.html)) | Not stated |

- **Price display rules:** no national price-transparency rule was found. NSW and federal minimum operating standards for funded chargers are said to expect charge point operators to share "availability status and pricing" data (search result, [DCCEEW](https://www.dcceew.gov.au/sites/default/files/documents/minimum-operating-standards-electric-vehicles-charging-infrastructure.pdf)). **Not verified:** the DCCEEW PDF timed out, and NSW's round 4 guidelines PDF couldn't be read as text. If true, it may one day give a reason for networks to publish prices, but there's no feed today.

### 2.4 OpenStreetMap

- OSM has a `charge=*` key for prices, with no set format ([OSM wiki](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dcharging_station)).
- In Australia, OSM has 1,654 charging stations, and `charge` is not among the tags taginfo lists with them (`fee=yes` is on 410) ([Geofabrik taginfo, data to 13 Nov 2026](https://taginfo.geofabrik.de/australia-oceania:australia/tags/amenity=charging_station)).
- **Verdict:** OSM holds almost no Australian charging prices. **Not verified:** the exact count (Overpass was at capacity).

### 2.5 Open Charge Map (already used)

- Licence: user-contributed data is CC BY 4.0, and "Use of our API or data in an application or service requires that the appropriate Data Provider attribution… be provided in a way which is visible the end user." Imported data is "copyright the original Data Provider" ([OCM terms](https://openchargemap.org/site/about/terms)).
- `UsageCost` is free text, and most of it is old: 89 of 125 fast sites had one, and 59 of those were last checked in 2023 (27 October note).
- **Verdict:** the only per-site source that is machine-readable, allowed, and already wired in. Keep using it within 12 months of its check date.

## 3. Third-party aggregators

| Source | Prices? | Terms on reuse | Verdict |
| --- | --- | --- | --- |
| PlugShare | Per-site, from drivers and operators | Forbids "scraping" and "any automated system, including… robots, spiders" (§1.C); API by paid licence only, as the 3 November note found ([PlugShare terms](https://company.plugshare.com/terms.html)) | No |
| Open Charge Map | Per-site free text, often old | CC BY 4.0 with attribution | Yes, as now |
| Gridly (comparison blog) | Network tables, dated Sept–Oct 2026 | Returned HTTP 402 to my reader; terms dated 4 April 2026 (search result, [Gridly terms](https://www.gridly.com.au/terms)) | Cross-check only, by a person |
| CarsGuide survey (syndicated) | Network × power band, Sydney peak, 15 July 2026 | News article; quote and cite, don't copy tables | Cross-check only |
| EVSE (evse.com.au) | Guides | Same company as Exploren (§1.8) | No |
| ROLLiN' (IAG) study, April 2026 | Says "the two networks in the dataset that publish structured $/kWh pricing" cover "over 1,200 stations"; networks not named ([Mirage News](https://www.miragenews.com/ev-friendly-cities-1680241/)) | Not stated | **Not verified** which two networks. Worth asking IAG; it may point to a feed I didn't find |
| EV Council | Counts of sites and connectors, not prices (4,268 locations at June 2026, search result, [EV Infrastructure News](https://www.evinfrastructurenews.com/ev-technology/australia-s-ev-market-achieves-record-h1-in-2026-as-evc-report-flags-widening-gap-to-2035-target)) | Not checked | No prices to use |

## 4. Summary table

| Network | Where prices are | Per-site public? | Machine-readable? | Terms allow automated reading? | Verdict for the agent |
| --- | --- | --- | --- | --- | --- |
| Tesla Supercharger | Tesla app; live, by site and time | No | No (Fleet API: own car's history only) | Site refuses readers (403) | Per-network typical from news and surveys |
| Evie | App only; website FAQ from 2023 | No | No | Yes for the website; nothing there to read | Per-network typical from news and surveys |
| Chargefox (+ RAC, EHT, QESH, 7-Eleven) | Chargefox app, set by each site owner | No | OCPI to partners only | **No** (cl. 6) | Per-network typical from news, surveys and OCM; never read chargefox.com |
| Ampol AmpCharge | App only | No | No | No robots clause; personal non-commercial use only | Per-network typical from news and surveys |
| bp pulse | App; some sites time-of-day | No | No | bppulse.com refuses readers (403); bp.com: "your use only" | Per-network typical from news and surveys |
| NRMA | **Public page table**, plus app | **Yes, 85 sites** | No (HTML table) | No robots clause; no reproduction or storing | **Typical: yes. Per site: only with permission** |
| Jolt | App; 7 kWh free daily | No | No | **No** (cl. 4.1(f), 11.1) | Per-network typical from news and OCM; never read Jolt's site |
| Exploren | App, set by hosts | No | No | **No** (cl. 3.7(d)) | "Other" typical |
| EVX / Ausgrid, Everty | App, set by hosts | No | No | Not checked | "Other slow" |
| Open Charge Map | Per site, free text | Yes | Yes (API) | Yes, CC BY 4.0 with attribution | **Per site when recent (as now)** |
| PlugShare | Per site | Behind its app | Paid API | **No** | Can't |
| Google Places | No EV price field | – | – | – | Can't |

## 5. What is realistically possible

### (a) The typical price per network, kept current: yes, with a narrower method

- **How changes happen:**
  - Network-wide changes come about once or twice a year per network, announced in the press. Examples: Evie in July 2023 and January 2024; Chargefox in March and May 2023; NRMA in April and August 2025; Queensland's Super Highway in June 2024 (sources in §1).
  - Per-site and time-of-day changes are continuous (Tesla's live pricing, NRMA's per-location prices).
  - So a monthly check is enough for a typical price. Weekly costs little more, and most runs find nothing.
- **What the agent may read** (an allow-list in `agents/prices.md`):
  - NRMA's charging page. Reading it to set one typical figure is reading, not reproducing the table.
  - Evie's terms and FAQ, which are allowed but usually say nothing new.
  - Queensland government EV snapshots.
  - Open Charge Map, through Charge Line's server or its public API.
  - News search for "price increase" plus a network name (The Driven, CarExpert, WhichCar, CarsGuide, electrive).
- **What it must not read** (a block-list): chargefox.com and support.chargefox.com, joltcharge.com and jolt.com.au, exploren.com.au, plugshare.com, tesla.com, bppulse.com, support.goevie.com.au, gridly.com.au. Either the terms forbid robots, or the site refused an automated reader.
- **What it does:**
  - A change backed by a published source on the allow-list (NRMA's table, a government page) opens a **pull request**.
  - A change seen only in the news or in Open Charge Map opens an **issue**: "Evie reported at 75c in the Sydney survey; check in the app." You confirm, then edit the number. That keeps the "third-party guides are a cross-check only" rule from the 12 November note.
- **Effort:** 1–2 hours for the allow-list, the block-list and the rule. The validator and JSON move from the 12 November note are needed anyway.
- **Running cost:** about 5–10 page reads and 3–5 searches a week, on the Claude plan. A$0 extra.
- **Terms risk:** low.
  - The agent reads only sites without a robots ban, and publishes one number per network in Charge Line's own words.
  - Ampol, NRMA, RAC and bp.com allow "personal non-commercial" use, and Charge Line is commercial. Deriving one typical figure from a page is not copying it, but this is my reading, not legal advice.

### (b) Per-site prices, where possible and allowed

| Source | Sites covered (rough) | Allowed? | Effort | Running cost |
| --- | --- | --- | --- | --- |
| Open Charge Map, checked in the last 12 months | At most 1 in 10 fast sites (12 of 125 in the 27 October sample were checked in 2025 or 2026) | Yes (CC BY, attribution shown) | None: already built | None extra: the server already reads OCM daily |
| Drivers' reported prices (a "price you paid" field in the existing charger report) | Grows with users; any network | Yes: the driver's own observation. Ask consent before passing it to OCM | 1–2 days (app field, server storage, a simple check against the network's typical price) | Storage trivial; your review time grows with users |
| NRMA's table | 85 sites, about 7% of the ~1,190 fast sites in Charge Line's file | **Only with NRMA's written permission** | Half a day to parse and match names, plus a manual review of matches | 1 page read a week |
| Tesla drivers' own history (`vehicle_charging_cmds`) | The linked car's own past Supercharger visits | Yes, the driver's own data, with consent | 1–2 days; needs a new scope, the Purpose of Usage text and the privacy page | Fleet API calls are billed by category (search result, [billing](https://developer.tesla.com/docs/fleet-api/billing-and-limits)) |

- **Coverage:** with NRMA's permission and today's Open Charge Map, about 15% of fast sites would have a site price (estimate; overlap unknown). Driver reports could raise that over time.
- **Per-site time-of-day prices** are not possible from any allowed source.

### (c) What can't be done

- Per-site prices for Tesla, Chargefox and its hosts (RAC, Electric Highway Tasmania, Queensland's Super Highway, 7-Eleven), Evie, Ampol, bp pulse, Jolt and Exploren. The prices are in apps, and the terms forbid robots or the sites refuse automated readers.
- Live and time-of-day prices for any network.
- Using PlugShare's prices without a paid licence.
- Any route through private app APIs or around bot protection. These are excluded by the terms, and by Apple's guideline 5.2.2, as the 3 November note found.

## 6. Recommended approach and data shape

### The approach

1. **Keep the current order:**
   1. the driver's own price;
   2. a per-site price from `prices.json`, when there is one and it hasn't expired;
   3. Open Charge Map, when checked within 12 months;
   4. the network's typical price;
   5. 65c for fast, 40c for AC.
   Always labelled as an estimate.
2. **Move the numbers into `prices.json` in the public `charge-line-data` repo**, and let the server serve it. A merged change then reaches drivers at the next `fly deploy`, not the next App Store release (12 November note, §4.4).
3. **Price agent:** monthly (or weekly), with the allow-list and block-list above. A pull request only for changes backed by allowed published sources; issues for everything else.
4. **Add a "price you paid" field** to the charger report. Store reports on the server, not in the public repo. Show a site price once two reports in 90 days agree, or one report from the last 30 days (a starting rule for you to set).
5. **Email NRMA** for permission to use its per-location table, with attribution. After the Ampol–Evie merger, ask Ampol whether it will share AmpCharge and Evie prices. Both cost nothing.
6. **Optional, later:** the Tesla charging-history scope, so a Tesla driver's own price fills in by itself.

### `prices.json`

```json
{
  "schemaVersion": 1,
  "currency": "AUD",
  "unit": "kWh",
  "updated": "2026-11-14",
  "rule": {
    "id": "nonmember-daytime-upper-v1",
    "text": "The price a non-member pays at a fast charger in the daytime. For a published range, the upper end of the usual range, not the dearest single site. Whole cents. Change only when the figure moves by 3c or more. No published figure: leave the number and say so."
  },
  "defaults": {
    "fast": { "price": 0.65, "basis": "estimate", "checked": "2026-10-27", "source": { "url": "research/notes/2026-10-27-charging-prices.md" } },
    "slow": { "price": 0.40, "basis": "estimate", "checked": "2026-10-27", "source": { "url": "research/notes/2026-10-27-charging-prices.md" } }
  },
  "networks": [
    {
      "id": "tesla",
      "name": "Tesla Supercharger",
      "match": { "names": ["Tesla"], "ocmOperatorIds": [], "osmOperatorWikidata": [] },
      "prices": [
        { "vehicles": "tesla", "price": 0.55 },
        { "vehicles": "other", "price": 0.65, "note": "without a Supercharging membership" }
      ],
      "freeKwhPerDay": 0,
      "basis": "estimate",
      "agentMayRead": false,
      "source": { "url": "https://thedriven.io/2026/04/22/…", "quote": "…", "checked": "2026-11-14" },
      "reviewBy": "2027-02-14"
    },
    {
      "id": "nrma",
      "name": "NRMA",
      "match": { "names": ["NRMA"], "ocmOperatorIds": [], "osmOperatorWikidata": [] },
      "prices": [{ "vehicles": "all", "price": 0.79 }],
      "freeKwhPerDay": 0,
      "basis": "published",
      "agentMayRead": true,
      "source": { "url": "https://www.mynrma.com.au/electric-vehicles/charging", "quote": "Location | State | Price … $0.69 (50 sites) to $0.79 (9 sites); outliers $0.89, $0.99", "checked": "2026-11-14" },
      "reviewBy": "2027-02-14"
    }
  ],
  "sites": [
    {
      "chargerId": "ocm:000000",
      "network": "nrma",
      "price": 0.75,
      "basis": "published",
      "licence": "permission:NRMA:2026-12-01",
      "source": { "url": "https://www.mynrma.com.au/electric-vehicles/charging", "checked": "2026-11-14" },
      "expires": "2027-02-14"
    }
  ]
}
```

- **Fields:**
  - `basis` is one of `published` (the network's own page), `survey` (dated press survey), `estimate` (reasoned figure) or `driver` (reports). The app can word the label to match.
  - `agentMayRead` writes the block-list into the data, so the validator can fail a pull request whose `source.url` is on a blocked domain.
  - `sites[].licence` must be `CC-BY-4.0` (with the OCM attribution), `driver`, or `permission:<who>:<date>`. The validator rejects anything else, so nothing copied without permission can reach the public repo.
  - `expires` makes a stale site price fall back to the network's typical price by itself.
- **Validator additions** (on top of the 12 November note's range and 25% checks):
  - every number has `source.url` and `checked`;
  - `checked` is not in the future;
  - no source on a blocked domain;
  - `rule.id` unchanged unless you changed it;
  - `sites` only with an allowed `licence`.

### Cost at scale (estimate)

`prices.json` is a few kilobytes gzipped. The app fetches it at most daily, with an ETag, so most requests are "not modified".

| Users | Worst case, every user downloads daily | Cost |
| --- | --- | --- |
| 2,000 | ~0.2 GB a month | Cents (Fly bandwidth; rate not re-checked today) |
| 10,000 | ~1 GB a month | Cents |
| 50,000 | ~5 GB a month | Under A$1 |

Driver price reports add a few bytes per report to the server's store. The cost that grows is your review time, not money.

## 7. Not verified

- **Tesla:**
  - Tesla's Australian terms of use and Supercharging page: tesla.com refused my reader (403).
  - Whether Tesla's live (occupancy-based) pricing applies in Australia.
  - Whether `charging_history` returns kWh, so a driver's price per kWh can be worked out.
- **bp pulse:** its Australian terms, and whether bppulse.com shows per-site prices (403).
- **Evie:** whether its map's store-locator data includes prices. Not checked, because the endpoint is undocumented.
- **ROLLiN' (IAG) study:** which "two networks… publish structured $/kWh pricing".
- **Charge point operators' data duties:** the DCCEEW and NSW wording on sharing "availability status and pricing" (search result only; PDFs unreadable or timed out).
- **Chargefox's OCPI interface:** from a third-party catalogue only.
- **Site counts for Tesla, Chargefox, Ampol, bp pulse, Jolt and Exploren:** from third-party guides and search results.
- **Queensland's Super Highway:** the 30 June 2024 rise from 30c to 55c (search result; the Queensland government page I tried returned 404).
- **Jolt:** the support-page statement on per-station rates (search result; I didn't open the page because Jolt's terms forbid scraping).
- **ActewAGL:** the $0.50–0.80 range (search result).
- **EVX:** the $0.50 figure, which dates from December 2023 (search result).
- **OpenStreetMap:** the exact number of Australian charging stations with `charge` set (Overpass was at capacity; taginfo lists no such combination).
- **Exploren:** whether its robots ban covers its website as well as its "Platform"; the wording is ambiguous, and I treated it as covering both.
- **Gridly:** its terms (HTTP 402 to my reader).
- **RAC:** the end date of its Electric Highway program.
- **Electric Highway Tasmania:** its number of sites.
- **CarsGuide survey:** whether its Tesla $0.79 was the price for Teslas or for other EVs.
- **Legal reading:** whether deriving one typical number from a "personal non-commercial" page is allowed. That is my reading, not legal advice; NRMA's and Ampol's permission would settle it.
