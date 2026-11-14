# New EV Discovery: How the Catalogue Agent Finds Cars New to Australia

**Date:** 2026-11-14
**For:** the catalogue agent planned in `2026-11-12-maintenance-agents.md` §4.1, and the public `charge-line-data` repo.
**Question:** Which sources show EVs (and whole brands) that are new to Australia, how should a monthly agent turn them into pull requests, and can the result be published openly?
**How to read it:** every fact is followed by the page that owns it, read on 14 November 2026. "Not verified" marks what I could not confirm. This is not legal advice.

## Bottom line

- **The catalogue is already behind.** Four of the twelve cars the 22 October note left out as "announced but not confirmed" are on sale now: Deepal E07, Xpeng X9, Leapmotor B05 and MG U9 EV (§5). Two new brands announced Australian launches this week: Hongqi (sold as "HQ", deliveries from 18 January 2027) and Avatr (website live, deliveries in the first half of 2027). Nothing in the current process would catch any of them.
- **Use three free government signals, in this order:**
  1. **ROVER's public list of vehicle type approvals** (make, model, category, holder, "last updated"). In the one case I could date, the Xpeng X9, the approval was reported about two months before orders opened (May → July). Needs a browser.
  2. **BITRE's monthly "Road vehicle entry and recall statistics"** XLSX: every vehicle entered on the Register of Approved Vehicles (RAV) last month, by make, by model and by motive power (EV, PHEV, HEV…). "All road vehicles must be entered on the RAV before they are provided to the Australian market." The September issue's page is dated 29 October (one data point).
  3. **The Green Vehicle Guide's "Newly added vehicles" page**: dated list of models makers just uploaded, each with its official WLTP range and Wh/km. Voluntary, so it misses brands (no IM, Cadillac or Skywell).
- **Then one news site: The Driven.** Its RSS feed is EV-only, tagged by brand and model, and pages back a month; its monthly "EV sales by model and by brand" article is the free per-brand sales table that FCAI sells. Its terms don't restrict automated reading. This week its feed carried both new brands, and October's sales table shows a make the catalogue lacks (Chery, 279 sales).
- **Leave out of the agent entirely:** CarExpert (news included), CarsGuide, Chasing Cars, WhichCar, Drive and ANCAP. Their terms ban robots, scraping or "systematic or automated data collection", or they block automated readers. EV Central's robots.txt blocks ClaudeBot and says `ai-train=no`. EVDB Australia stays out, as before.
- **How early each signal is** (Xpeng X9): reported on ROVER's approval list 16 May 2026 → orders opened 21 July → RAV entries almost all from August (264 of 315 this year) → in BITRE's August tables, published about four weeks after month end.
- **No government source gives battery size or charging power.** Those still come from the maker's Australian page first, then launch coverage. The GVG gives the official WLTP range and Wh/km, which is a useful check on the maker's claim.
- **Publishing:** in Australia, plain facts such as a range or a battery size aren't protected by copyright, and there is no separate database right ([HWL Ebsworth](https://hwlebsworth.com.au/protecting-your-data-just-how-far-does-copyright-protect-the-value-of-data/), [MinterEllison](https://www.minterellison.com/articles/no-copyright-in-white-and-yellow-pages-directories-in-australia-telstras-appeal-fails)). The real risk is a website's terms, which is why the do-not-use list matters. Suggested licence: **ODbL 1.0**, matching the charger file (§4).

## 1. Sources that list new vehicles

| Source | What it shows | Machine-readable? | How early | Terms for automated reading | Use for |
| --- | --- | --- | --- | --- | --- |
| ROVER list of vehicle type approvals | Approval no., make, model, market designation, category, holder, status, last updated | Web grid, 10 rows a page, loads by JavaScript | Earliest: weeks to months before sale | No robots.txt; department copyright and disclaimer, no scraping clause | New brands and models (a) (b) |
| BITRE Road vehicle entry and recall statistics | Monthly RAV entries by make, model and motive power | XLSX, 48 tables | Entries start with first deliveries; the September issue's page is dated 29 October | © Commonwealth; department copyright page | Confirms on sale, volume, fading models (a) (b) (d) |
| Green Vehicle Guide | Each model's WLTP Wh/km, electric range, body, drive, test cycle | HTML; CSV export of searches (top 50); "third party web service" on request | Days to weeks around launch (not verified) | Department copyright (CC BY 4.0 where marked) | New variants, official WLTP (b) (c) |
| RAV public search | One vehicle, by VIN | No | — | Disclaimer only | Not useful |
| NVES published data | Yearly results per supplier (entity), not per model | XLSX | Yearly, February | Government site | Cross-check only |
| FCAI VFACTS release | Market total, top-10 brands and models as images | No (detail is paid) | Month + about 5 days | "All rights reserved" | Not useful |
| EVC Vehicle Sales Report | Monthly deliveries | Report to subscribers | Month + 4 business days | No redistribution without permission | Human reading only |
| Makers' Australian sites | Model pages, specs, "available now" | Sitemaps (XML) | At or before launch | Varies; check per maker | Confirm on sale, specs (b) (c) (d) |
| The Driven RSS and monthly sales article | EV news tagged by brand and model; EV sales by brand and model each month | RSS (10 items a page, pageable); sales tables as page text | Approvals, reveals, launches; sales about 5 days after month end | No automated-access clause; robots.txt allows, crawl-delay 10 | All four (a)–(d) |

### 1.1 ROVER: the published list of vehicle type approvals

- **It exists and is public.** ROVER's home page links "Lists of approvals" for vehicle types and says "Lists of approvals and the RAV Public Search will remain available throughout the outage" ([ROVER](https://www.rover.infrastructure.gov.au/)).
- **The vehicle type list** is at [/PublishedApprovals/VTAApprovals](https://www.rover.infrastructure.gov.au/PublishedApprovals/VTAApprovals/). Its filters: approval number, make, model, market designation, category, approval holder name, status (in force, revoked, suspended, expired) and "Updated since". Its columns: approval number, make, model, market designation, category, approval holder, approval status, last updated. Rows come from a JavaScript grid, 10 per page (read from the page's own layout definition).
- **It leads sales.** The Driven reported the Xpeng X9 "spotted on the ROVER approval-for-sale register" on 16 May 2026 ([The Driven](https://thedriven.io/2026/05/16/xpengs-next-ev-approved-for-sale-in-australia-a-fast-charging-electric-people-mover/)); orders opened on 21 July 2026 ([The Driven](https://thedriven.io/2026/07/21/xpeng-launches-x9-luxury-people-mover-in-australia-priced-from-89900/)).
- **What it doesn't show:** motive power (EV or not) isn't a column. A type approval for a new model name from a known EV maker is a strong hint; for a mixed maker it needs a check.
- **Terms:** ROVER has no robots.txt (the address returns an HTML page). Its footer links the department's copyright and disclaimer pages; neither mentions automated access ([copyright](https://www.infrastructure.gov.au/copyright), [disclaimer](https://www.infrastructure.gov.au/disclaimers)).
- **Approval detail documents:** enthusiasts share approval documents with battery size, motor power and tare mass (The Driven on a Leapmotor hatch: "39.8 kWh pack and a 53 kWh pack", [The Driven](https://thedriven.io/2026/09/28/leapmotors-new-affordable-electric-hatch-approved-for-sale-in-australia/)). Whether those details are on the public list's detail view is not verified.

### 1.2 BITRE: monthly RAV entries by make, model and motive power

- **What it is:** "monthly counts of all road vehicles entered on the Register of Approved Vehicles (RAV)", published as a PDF and an XLSX each month ([BITRE](https://www.bitre.gov.au/resource/roads-vehicles/road-vehicle-entry-and-recall-statistics)). The September 2026 issue (re-issued; page release date 29 October 2026) is the latest.
- **Why it matters:** "All road vehicles must be entered on the RAV before they are provided to the Australian market" (the workbook's notes, [September 2026 XLSX](https://www.bitre.gov.au/sites/default/files/documents/Transport%20-%20road%20vehicle%20entry%20and%20recall%20statistics%20-%20Sep%202026%20-%20re-issue.xlsx)).
- **Useful tables (September 2026 XLSX):**
  - Table 12: passenger vehicles, top makes and models, with the month, the previous month, the same month last year, year to date and last 12 months. It names about 60 makes, including small ones (Forthing Taikon 5, GMC Yukon, McLaren), then "All other makes".
  - Table 25: passenger vehicles by motive power, top 30 makes (EV, PHEV, HEV, petrol, diesel), then "Other makes" (905 EVs in September).
  - Table 13 / 26: the same for light commercial vehicles (utes and vans).
- **What it showed for September 2026** (Table 12, entries in September / August / same month 2025 / year to date):
  - XPeng X9: 50 / 264 / 0 / 315. Orders opened 21 July, so here RAV entries began with the first deliveries, after the launch.
  - Leapmotor B05: 59 / 29 / 0 / 90 (in dealers from late August).
  - Forthing Taikon 5: 40 / 75 / 0 / 282 (a new brand, but not an EV; see §2).
  - Denza HT: 14 / 3 / 0 / 17; Denza B5: 2 / 318 / 0 / 2,763 (motive power not stated per model).
  - Light commercials (Table 13): Kia PV5 215 / 71 / 0 / 642; LDV eDeliver 5 45 / 76 / 0 / 122.
- **Limits:**
  - Model names are as entered on the RAV, sometimes chassis codes ("H243", "X248" under Mercedes-Benz) or groupings ("X SERIES", "ID.4/ID.5"). Leapmotor shows "A12" (963 this year), "B05" and "C10" but no "B10", which is on sale; "A12" is probably the B10's internal name (not verified).
  - Table 12 has no motive power per model; Table 25 has motive power per make only. A new make with only EVs in Table 25 is clear; a new model of a mixed maker needs a check.
  - "Estimates from 1 July 2026 onwards reflect motive power entered on the RAV by vehicle suppliers"; before that, partly BITRE's estimates (Table 25 note).
  - Revisions happen ("Re-issue - October 2026 … to correct for formatting issues in Tables 6 and 12").
- **Terms:** "© Commonwealth of Australia 2026"; BITRE's footer links the department's copyright page ([copyright](https://www.infrastructure.gov.au/copyright)). Its robots.txt allows everything but site internals ([robots.txt](https://www.bitre.gov.au/robots.txt)).

### 1.3 Green Vehicle Guide (GVG)

- **What it lists:** "new light vehicles … sold in Australia since 2004", run by the Department of Infrastructure ([About](https://www.greenvehicleguide.gov.au/Home/About)).
- **Where the data comes from:** "supplied by authorised representatives of vehicle manufacturers … verified against certification data", and makers upload it "voluntarily. For this reason, data for some vehicle models sold in Australia may not be available" ([FAQ](https://www.greenvehicleguide.gov.au/pages/About/FAQ)).
- **Newly added vehicles** ([page](https://www.greenvehicleguide.gov.au/Home/NewlyAddedVehicles)): a dated list, 11 models from 28 October to 5 November 2026 (BMW iX3, BYD Atto 2, Sealion 5, 6 and 8, Volvo EX90, among others). No fuel type on the list; each links to a detail page.
- **Fields per variant** (for example [BMW iX3, 38039](https://www.greenvehicleguide.gov.au/Vehicle/ViewVehicle?vehicleDisplayIdList=38039) and [BYD Atto 2](https://www.greenvehicleguide.gov.au/Vehicle/ViewVehicle?vehicleDisplayIdList=38038%3A38029%3A38027%3A38026)): make, model, variant, release year, body, engine ("Pure Electric"), drive, energy consumption (Wh/km), electric range (km), test cycle ("WLTP (4-Phase)"), CO2, annual fuel cost. **No battery size and no charging power.**
- **Search:** filter by fuel type "Pure Electric" and make; "display the top 50 vehicles"; results "Download as CSV" ([How-to guide](https://www.greenvehicleguide.gov.au/pages/ToolsAndCalculators/HowToGuide)). The search is a POST form with an anti-forgery token, so it's a browser job.
- **Bulk access:** "The Green Vehicle Guide has a third party web service that can be used to analyse our data for business or research purposes. To request access to this service, please contact us" ([FAQ](https://www.greenvehicleguide.gov.au/pages/About/FAQ)). The government's VESR site says its data is "drawn under license" from the GVG ([VESR example](https://vesr.gov.au/vehicle/mg-zs-ev-suv-2022), via search).
- **Make list as a signal:** the search's make dropdown lists 65 makes. It has Farizon, Leapmotor, Deepal and XPENG, but no IM, Cadillac, Skywell or Forthing ([search](https://www.greenvehicleguide.gov.au/Vehicle/Search)). A new make appearing there is a strong "on sale" signal; its absence proves nothing.
- **"Newly added" isn't only launches.** It also carries updates to cars long on sale: the Volvo EX90 (in the catalogue since 2025) was added on 2 November 2026. Treat it as a new-variant and spec-change signal as much as a new-model one.
- **Terms:** no robots.txt (404). Copyright and disclaimer redirect to the department's pages: "Where identified by a CC logo, the material is licensed under CC" (CC BY 4.0), attributed "© Commonwealth of Australia" ([copyright](https://www.infrastructure.gov.au/copyright)).

### 1.4 RAV public search, NVES, VFACTS, EVC

- **RAV public search is VIN-only:** "The Register of Approved Vehicles (RAV) is searchable using the vehicle's permanently marked Vehicle Identification Number (VIN)" ([RAV public search](https://www.rover.infrastructure.gov.au/RAVPublicSearch/)). It can't list models.
- **NVES:** the regulator publishes yearly results per "regulated entity" (the approval holder, for example "Guangzhou Xiaopeng Motors Technology Co. Ltd"), in an XLSX "as at 1 February 2026" for the 2025 period ([NVES 2025 results](https://www.nvesregulator.gov.au/reporting-and-data/2025-nves-performance-period-results)). No models. Too slow for monthly use; a new entity next February is a late cross-check.
- **FCAI VFACTS:** the free release has totals and the top-10 brands and models as images. October 2026: 103,325 sales, BEVs 23.1% "from all sources" ([FCAI](https://www.fcai.com.au/competition-drives-strong-new-vehicle-market/)). Detail is ordered from VFACTS. Not a useful signal for new brands.
- **Electric Vehicle Council:**
  - The EVC Vehicle Sales Report is monthly, "released publicly to non-members on the 4th business day of each month". Its subscription terms: the subscriber "shall not distribute, reproduce or copy the reports … without the prior written permission of the EVC", but may adapt information with the notice "Based on information provided by and with the permission of the Electric Vehicle Council of Australia" ([EVC](https://electricvehiclecouncil.com.au/evc-vehicle-sales-report/)). Fine for the owner to read; not for the agent.
  - State of EVs 2026 is behind a registration form ("Register to download"); a Vehicles factsheet PDF is linked ([EVC](https://electricvehiclecouncil.com.au/state-of-evs-2026)). Whether it lists models is not verified.

### 1.5 Makers' Australian sites

- **Sitemaps are the cheap, polite signal.** Most makers publish one (robots.txt lists sitemaps for Kia, Hyundai, Toyota Australia, Xpeng, MG Australia, Polestar, Leapmotor). MG Australia's has one URL per model, including `/vehicles/mgu9-ev`, and every `lastmod` is today ([sitemap](https://mgmotor.com.au/sitemap.xml)). A new `/vehicles/…` or `/au/…/models/…` URL is a new model; a removed one hints at a discontinued model.
- **Hyundai explicitly allows Claude's fetchers** (`User-agent: Claude-User` … `Allow: /`, [robots.txt](https://www.hyundai.com/robots.txt)).
- **Newsrooms with RSS:** not surveyed maker by maker (see Not verified). Sitemaps cover the same need with one rule for all makers.

### 1.6 News sites and their terms

| Site | Feed | Terms on automated reading | Verdict |
| --- | --- | --- | --- |
| The Driven | [thedriven.io/feed/](https://thedriven.io/feed/): 10 items a page, pageable with `?paged=N`; summaries only; categories name brand and model | Licence to "access and use the Site … in the normal manner"; no scraping clause ([terms](https://thedriven.io/terms-of-use)); robots.txt allows all, crawl-delay 10 ([robots](https://thedriven.io/robots.txt)) | **Use** (feed, plus single articles it links) |
| EV Central | [evcentral.com.au/feed/](https://evcentral.com.au/feed/) | No terms page found. robots.txt: `ClaudeBot` disallowed; `Content-Signal: search=yes,ai-train=no,use=reference`, stated as a condition of access ([robots](https://evcentral.com.au/robots.txt)) | **Don't use in the agent** |
| CarExpert (news too) | `/feed` | Bans "spidering, screen scraping, database scraping, or any other activity with the purpose of obtaining lists of users or any other information available through the Wesbite" (cl. 4(i)(b)); covers the whole site ([terms](https://www.carexpert.com.au/terms-and-conditions)) | **Don't use** |
| CarsGuide | — | "copy, scrape, data-mine … (whether manually or by any automated process)" banned ([conditions](https://www.carsguide.com.au/conditions-of-use)) | **Don't use** |
| Chasing Cars | `/feed.xml` | Bans "data scraping, collection or accumulation tool, robot, spider" ([terms](https://www.chasingcars.com.au/terms/)) | **Don't use** |
| WhichCar | — | Returned 403 to automated readers; its terms prohibit reproduction "by automated or manual means (including any so-called robot, spider, scraper …)" (search excerpt of [terms](https://www.whichcar.com.au/terms-and-conditions); page not readable) | **Don't use** |
| Drive | — | Cloudflare challenge on robots.txt; 403 on its terms page | **Don't use** |
| ANCAP (ratings of new models) | — | Users must not "conduct any systematic or automated data collection activities" (cl. 2.2, [terms](https://www.ancap.com.au/privacy-and-terms-of-use)) | **Don't use** |

- **The Driven's [Compare EVs](https://thedriven.io/compare-evs/) page** is a useful names-only cross-check: about 159 entries across 50 brands, and it says 110 models are available new with about 20 more coming soon. It names makes the catalogue lacks (Chery, Nio, Honda, Mitsubishi, Blade, Farizon, Rolls-Royce, Skyworth); most are old, commercial, exotic or another name for a known make (Skyworth/Skywell), so each needs checking. Use it to find names, never to copy its figures: the compilation is EV Media's.

## 2. Detection pipeline

Each run starts from the catalogue and a small state file, `discovery/seen.json`, so it only reports what's new since last run.

### (a) Brand-new brands

1. **ROVER type approvals:** filter "Updated since" = last run, and passenger cars, SUVs and light goods (presumably the ADR categories MA, MC and NA; I didn't see the filter's values). Any make not in `vehicles.json` and not in `seen.json` → candidate.
2. **BITRE latest XLSX:** makes in Table 12, 13, 25 and 26 not in the catalogue. In Table 25, a make with EV > 0 is an EV maker.
3. **GVG:** makes in the search dropdown not seen before; models on "Newly added" with engine "Pure Electric".
4. **The Driven:** RSS categories that are brand names not in the catalogue; brands with sales in the monthly sales article but no catalogue entry.
5. **Confirm:** the brand has an Australian website with a model page showing price, "order" or "test drive", or a launch article with a price. Add only then.

### (b) New models or variants of known brands

- Same four signals, comparing make + model (normalised) instead of make.
- Variant-level: GVG detail pages list every variant with its range (for example "iX3 40 Wagon Auto", 500 km); compare with the catalogue's variants for that model.
- Maker sitemaps: new model URLs.

### (c) Spec changes

- Monthly, for each model on sale (no `untilYear`): re-read the maker's Australian model or specs page and compare usable kWh, WLTP km, DC kW, AC kW and the charge claim.
- Use the GVG's range as an independent check of the WLTP figure. A mismatch of more than 3% is flagged, not auto-changed (wheel size and variant often explain it).
- A new model year on the GVG (the "released" year) for a model already listed is a prompt to re-check.

### (d) Discontinued models

- Four signals, none decisive alone: the model's page leaves the maker's sitemap; BITRE RAV entries for that model fall to zero for three months in a row; The Driven's monthly sales show zero for three months; the maker's model list no longer shows it. (October's zeros include Cadillac, which still had 26 Lyriqs entered on the RAV in September, so sales alone prove nothing.)
- Two of the four → propose `untilYear` = the current year. Never delete.

### Avoiding false positives

- **Not an EV:** RAV and BITRE include petrol, hybrids and PHEVs. Forthing's Taikon 5 is on the RAV and reported as a "long-range hybrid SUV" ([carsales](https://business.carsales.com.au/news-room/news/forthing-car-brand-locked-in-for-oz-with-longrange-hybrid-suv/), via search). Only add with "Pure Electric" on the GVG, an EV split in BITRE Table 25, or the maker's page.
- **Approved but not on sale:** a type approval or a reveal isn't a launch. Hold the candidate in `seen.json` with status `approved` or `announced`, and add it only when there is an Australian price or "available now".
- **Overseas specs:** Chinese and European figures (CLTC, NEDC, EPA, European WLTP) differ from the Australian claim. Avatr is the live example: the only battery figures so far are Chinese ("89.33 kWh CATL LFP"), and "Australian pricing, variants and WLTP range figures are yet to be announced" ([The Driven](https://thedriven.io/2026/11/13/avatrs-australian-website-goes-live-with-07l-electric-suv-and-06t-wagon/)). Use only an Australian page or an Australian launch report; label anything else "European WLTP" as the catalogue already does.
- **Name noise:** RAV model names can be chassis codes ("H243"), groups ("X SERIES") or internal names (Leapmotor "A12", probably the B10). Map them in `discovery/aliases.json` once, by hand.
- **Commercial vans and exotics:** keep the 22 October rules (left out on purpose). Record them in `seen.json` as `excluded` so they're not proposed every month.

### Deduplication against existing ids

- Key = `normalise(make) + normalise(model)`, lower case, spaces and punctuation removed, brand prefix stripped from the model ("MG4 EV" → "mg4"; "POLESTAR 4" → "4").
- Keep make aliases: GWM / Great Wall / Haval / Ora / Tank; Chery / Omoda / Jaecoo / Lepas; Changan / Deepal / Avatr; Geely / Zeekr / Lynk & Co; BYD / Denza; Dongfeng / Forthing; FAW / Hongqi / "HQ" (its Australian brand name, [The Driven](https://thedriven.io/2026/11/12/chinese-luxury-ev-brand-hongqi-launches-in-australia-with-massive-six-seat-electric-suv/)); SAIC / MG / IM / LDV; Skywell / Skyworth; XPENG / XPeng / Xpeng.
- A match on make + model but not variant → candidate variant, never a new model.
- New ids follow the existing pattern `make-model-variant-year` (for example `xpeng-g6-lr-2026`). The validator rejects a new id that equals an existing one, and never lets an existing id change.

## 3. Verifying specs for a new model

| Field | First source | Second source | Notes |
| --- | --- | --- | --- |
| WLTP km | Maker's Australian page | GVG electric range (official, test cycle shown) | GVG gives one figure per variant; maker pages often give "up to" |
| Wh/km | — | GVG energy consumption | Not in the catalogue today; worth storing as a check |
| Usable kWh | Maker's Australian page if it says "usable" or "net" | Launch coverage quoting the maker | Most pages give one unlabelled number (MG U9 EV: "102.2kWh LFP", [MG](https://mgmotor.com.au/vehicles/mgu9-ev)); then × 0.95 marked "est.", as before |
| DC peak kW | Maker's Australian page | Launch coverage | Australian and overseas figures differ (Xpeng X9: 537 kW reported for Europe in May, [The Driven](https://thedriven.io/2026/05/16/xpengs-next-ev-approved-for-sale-in-australia-a-fast-charging-electric-people-mover/); 542 kW at the Australian launch, [The Driven](https://thedriven.io/2026/07/21/xpeng-launches-x9-luxury-people-mover-in-australia-priced-from-89900/)) |
| AC kW | Maker's Australian page | — | |
| Charge claim | Maker's Australian page | Launch coverage | Keep the maker's from–to (MG U9 EV: 20–80% in 42 min) |
| Connectors | Assume CCS2 + Type 2 for new Australian EVs | Maker page | CHAdeMO only on old Leaf and UX 300e |

- **What no public source gives reliably:** usable versus gross, and the shape of the charge curve.
- **What not to use:** EVDB Australia and CarExpert spec pages (terms), and the other sites in §1.6.

## 4. Data and licensing

### Can facts be published?

- **Facts aren't protected; their expression can be.** "copyright does not protect the idea or information; rather, it protects the expression of that idea or information" ([HWL Ebsworth, 2023](https://hwlebsworth.com.au/protecting-your-data-just-how-far-does-copyright-protect-the-value-of-data/)).
- **Effort alone doesn't create copyright in a compilation.** In *Telstra v Phone Directories* (Full Federal Court, 2010), copyright did not subsist even though Telstra spent "considerable time, effort and cost" collecting the facts; a work must "originate from some independent intellectual effort" of a human author ([MinterEllison](https://www.minterellison.com/articles/no-copyright-in-white-and-yellow-pages-directories-in-australia-telstras-appeal-fails)). This followed the High Court's *IceTV* (2009).
- **No database right.** "Unlike the EU where a database can be protected through database rights … a database in Australia can be considered a 'literary work' but is still subject to the requirement of 'originality'", and "the law does not recognise nor confer proprietary rights in data in its own right" ([HWL Ebsworth](https://hwlebsworth.com.au/protecting-your-data-just-how-far-does-copyright-protect-the-value-of-data/)).
- **Contract is the real risk.** A breach of contract "tends to be more straightforward compared to a case of copyright infringement, which requires the party asserting copyright infringement to first demonstrate that copyright subsists in the work" ([HWL Ebsworth](https://hwlebsworth.com.au/protecting-your-data-just-how-far-does-copyright-protect-the-value-of-data/)). After *Telstra*, database owners were expected to adopt "ever more onerous contractual measures (to proscribe users from data mining)" ([MinterEllison](https://www.minterellison.com/articles/no-copyright-in-white-and-yellow-pages-directories-in-australia-telstras-appeal-fails)). Website terms that ban scraping are those measures; whether they bind a reader who never clicked "agree" is untested here, so the safe course is to obey them.

### What that means in practice

- Take individual numbers (range, kWh, kW, minutes) from allowed sources, and write the `source` text in your own words. Don't copy sentences, tables or another site's whole list.
- Never take anything from a site whose terms ban automated collection (§1.6), even for one field.
- Government data: attribute "© Commonwealth of Australia" (Green Vehicle Guide, BITRE) in the repo's `SOURCES.md`. The department's CC BY 4.0 applies "where identified by a CC logo" ([copyright](https://www.infrastructure.gov.au/copyright)). Strictly, "use of the facts and ideas embedded within the contents will not require attribution" under a CC licence ([CC FAQ](https://creativecommons.org/faq/)), but attributing costs nothing and is the polite course.
- US EPA test-car data (road loads) is a US Government work and public domain (not re-checked here).

### Suggested licence

- **ODbL 1.0 for `vehicles.json`, same as the charger file.** One licence to explain; anyone who publicly uses an adapted version "must also offer that adapted database under the ODbL" ([ODbL summary](https://opendatacommons.org/licenses/odbl/summary/)), so a competitor can't take the curation and close it.
- **Alternative: CC BY 4.0** if the aim is the widest reuse. CC 4.0 licenses cover databases, and "sui generis database rights are licensed alongside copyright" ([CC FAQ](https://creativecommons.org/faq/#can-i-use-a-cc-license-for-data-and-databases)).
- **Code (validator, scripts): MIT.**
- Since the owner is the licensor, neither licence limits the Charge Line app.

## 5. Recent and upcoming entries (pipeline test set)

**New brands**

| Brand | Status | Source |
| --- | --- | --- |
| Hongqi, sold as "HQ" (FAW) | Launched 12 Nov 2026. E-HS9 six-seat SUV: 120 kWh NMC, 548 km WLTP, 140 kW DC, 11 kW AC, 10–80% in 48 min; just under A$150,000 (not final); deliveries from 18 Jan 2027. A smaller E-HS4 to be unveiled in December | [The Driven, 12 Nov 2026](https://thedriven.io/2026/11/12/chinese-luxury-ev-brand-hongqi-launches-in-australia-with-massive-six-seat-electric-suv/) |
| Avatr (Changan JV) | Site live at avatr.au. 07L SUV: pre-orders before end of 2026, deliveries first half of 2027; 06T wagon second half of 2027. No Australian specs yet | [The Driven, 13 Nov 2026](https://thedriven.io/2026/11/13/avatrs-australian-website-goes-live-with-07l-electric-suv-and-06t-wagon/) |
| Forthing (Dongfeng) | On the RAV (BITRE Table 12: Taikon 5); reported as a hybrid. **Should be rejected as not an EV** | [BITRE Sep 2026](https://www.bitre.gov.au/resource/roads-vehicles/road-vehicle-entry-and-recall-statistics); [carsales](https://business.carsales.com.au/news-room/news/forthing-car-brand-locked-in-for-oz-with-longrange-hybrid-suv/) (search) |
| Lepas (Chery) | L6 priced at A$47,990 in October 2026, 440 km WLTP from a 65 kWh LFP pack (a September preview said 67.1 kWh: sources disagree) | [The Driven, 15 Oct 2026](https://thedriven.io/2026/10/15/cherys-lepas-prices-first-electric-suv-at-47990-with-440km-range/) (search result) |
| Luxeed (Chery) | Announced for Australia in 2027 | [The Driven, 26 Oct 2026](https://thedriven.io/2026/10/26/another-luxury-ev-brand-to-enter-australia-in-2027-with-cherys-luxeed-to-bring-high-end-performance-electric-suv/) (search result) |
| Chery (as a make) | 279 EVs sold in October (The Driven's sales table); the car is the Chery E5 (58.9 kWh LFP, 430 km WLTP). The catalogue has an "Omoda E5" (430 km) and no Chery: probably a rebadge, so an alias, not a new car | [The Driven sales](https://thedriven.io/2026/11/05/australian-electric-vehicle-sales-by-month-in-2026-by-model-and-by-brand-3/); [The Driven E5 review](https://thedriven.io/2026/09/29/video-is-cherys-37990-driveaway-e5-electric-suv-still-good/) (search result) |

**New models of known brands**

| Model | Status | Source |
| --- | --- | --- |
| Xpeng X9 | On sale since July 2026: 94.8 kWh LFP 535 km WLTP (2WD), 110 kWh NCM 580 km (AWD), up to 542 kW DC | [The Driven](https://thedriven.io/2026/07/21/xpeng-launches-x9-luxury-people-mover-in-australia-priced-from-89900/) |
| Leapmotor B05 | In dealers from late August 2026: 56.2 / 67.1 kWh LFP, WLTP up to 401 / 482 km | [The Driven](https://thedriven.io/2026/07/02/new-leapmotor-b05-electric-hatchback-to-land-in-australia-from-35990-driveway/) |
| A further Leapmotor hatch (name not given) | Approved for sale 28 Sep 2026, with 39.8 / 53 kWh packs and 130 / 145 kW motors; not on sale yet. Should be held as `approved` | [The Driven](https://thedriven.io/2026/09/28/leapmotors-new-affordable-electric-hatch-approved-for-sale-in-australia/) |
| Kia PV5 | On the RAV as a light commercial (215 in September). The Cargo van is out by the catalogue's rules; the Passenger version should be watched | [BITRE](https://www.bitre.gov.au/resource/roads-vehicles/road-vehicle-entry-and-recall-statistics) Table 13 |
| Deepal E07 | On sale since 2025: 89.98 kWh NMC, WLTP up to 550 km (RWD) / 510 km (AWD) | [The Driven](https://thedriven.io/2025/04/06/deepal-unveils-pricing-of-its-unique-ute-like-e07-electric-suv/) |
| MG U9 EV (ute) | "Available Now": 102.2 kWh LFP, up to 430 km WLTP, 115 kW DC, 20–80% in 42 min, 11 kW AC | [MG Australia](https://mgmotor.com.au/vehicles/mgu9-ev) |
| BMW iX3 40 | GVG newly added 29 Oct 2026: 500 km, 182 Wh/km, WLTP (4-Phase). Catalogue has only the iX3 50 | [GVG](https://www.greenvehicleguide.gov.au/Vehicle/ViewVehicle?vehicleDisplayIdList=38039) |
| GAC Aion UT | 5-star ANCAP, October 2026 | [The Driven](https://thedriven.io/2026/10/13/xpeng-x9-mpv-and-gac-aion-ut-hatch-get-5-star-ancap-safety-scores-under-tougher-new-test/) (headline) |

- **Deepal E07, Xpeng X9, Leapmotor B05 and MG U9** are on the 22 October note's "announced but not confirmed" list. The agent should re-check that list every run.
- **Not EVs, but will show up:** BYD Sealion 5, 6 and 8 and Atto 2 DM-i (GVG newly added; Atto 2 DM-i is "Plug-in Electric/Petrol 95RON"), Denza B5 (RAV), GAC Emzoom (RAV).

## 6. Recommended pipeline

**Cadence:** one run on the first Sunday after BITRE's release (about the 4th week of the month), so the XLSX is fresh. The weekly maker re-checks from the 12 November note (§4.1) can stay for spec changes.

**Steps:**

1. Load `vehicles.json`, `discovery/seen.json`, `discovery/aliases.json`.
2. **ROVER VTA list** (browser): filter "Updated since" the last run; record make, model, approval number, category.
3. **BITRE XLSX** (one download): Tables 12, 13, 25, 26.
4. **GVG** (browser): Newly added page; the "Pure Electric" search CSV.
5. **The Driven** (about 13 fetches, 10 seconds apart as its robots.txt asks):
   - the RSS feed, paged back to the last run. It holds 10 items a page, about four days' news; `?paged=4` reached 3–5 November ([page 4](https://thedriven.io/feed/?paged=4)). Keep categories (brand, model) and titles;
   - the monthly "Australian electric vehicle sales by month … by model and by brand" article (about the 5th): every brand's EV sales for the month, from "VFacts", the EVC and "individual companies" ([October 2026](https://thedriven.io/2026/11/05/australian-electric-vehicle-sales-by-month-in-2026-by-model-and-by-brand-3/)). A brand with sales but no catalogue entry is a gap (Chery, October); a model at zero for months is a discontinuation hint.
6. **Maker sitemaps** for the 47 known makes plus any new ones (one fetch each).
7. **Re-check the "announced but not confirmed" list** from the 22 October note and `seen.json` items marked `approved` or `announced`.
8. Build candidates; drop known ids, aliases and `excluded`; classify as new brand, new model, new variant, spec change, discontinued.
9. For each candidate that is on sale: read the maker's Australian page, then one launch article; fill the fields per §3.
10. Validate (`node scripts/validate-catalogue.mjs`): schema, ranges (Wh/km 100–300), unique and stable ids, no deletions.
11. Open one pull request. Stop and open an issue instead if more than about 25 entries change.

**Budget:** about 80–100 page reads a run (47 sitemaps, about 13 for The Driven, a handful for ROVER and the GVG, one XLSX, then two per candidate). The 12 November note's concern about long runs applies; splitting makers across weeks still works, but the discovery steps 2–5 should run together once a month.

**Pull request description:**

- **New brands** (each: evidence links from at least two signals, the Australian price page).
- **New models and variants** (table: id, make, model, variant, each field with its value, source link and the quoted sentence).
- **Spec changes** (model, field, old → new, source, quoted sentence).
- **Proposed discontinued** (`untilYear`, with the signals that agreed).
- **Watching, not added** (approved or announced, with the date first seen).
- **Rejected** (not EV, commercial, exotic).
- **Couldn't read** (sites that failed or blocked).

## 7. Data shape for `vehicles.json`

Keep the app's fields unchanged; add provenance fields the app ignores.

```json
{
  "id": "mg-u9-ev-2026",
  "make": "MG",
  "model": "U9 EV",
  "variant": "AWD",
  "year": 2026,
  "body": "ute",
  "usableKWh": 97.1,
  "wltpKm": 430,
  "maxDCkW": 115,
  "maxACkW": 11,
  "connectors": ["ccs2", "type2"],
  "charge": { "from": 20, "to": 80, "minutes": 42 },
  "source": "MG Australia (102.2 kWh LFP, up to 430 km WLTP, 115 kW DC, 20-80% 42 min, 11 kW AC); usable est.",
  "sources": {
    "usableKWh": { "url": "https://mgmotor.com.au/vehicles/mgu9-ev", "kind": "maker-au", "estimate": true },
    "wltpKm":    { "url": "https://mgmotor.com.au/vehicles/mgu9-ev", "kind": "maker-au" },
    "maxDCkW":   { "url": "https://mgmotor.com.au/vehicles/mgu9-ev", "kind": "maker-au" },
    "maxACkW":   { "url": "https://mgmotor.com.au/vehicles/mgu9-ev", "kind": "maker-au" },
    "charge":    { "url": "https://mgmotor.com.au/vehicles/mgu9-ev", "kind": "maker-au" },
    "connectors": { "kind": "assumed" }
  },
  "gvg": { "rangeKm": null, "whPerKm": null, "checked": "2026-11-14" },
  "firstSeen": { "date": "2026-11-14", "signal": "maker-sitemap" },
  "onSaleFrom": null,
  "checked": "2026-11-14"
}
```

The figures are from MG's page as read today; usable is 102.2 × 0.95 under the existing rule, the year is a guess, and `gvg` is empty because I didn't look the U9 up on the GVG. It's an illustration of the shape, not a reviewed entry.

- **`sources`**: one entry per field, with `kind` one of `maker-au`, `gvg`, `news`, `epa`, `estimate`. Keeps the free-text `source` for the app and humans.
- **`gvg`**: the official range and Wh/km, as a cross-check.
- **`firstSeen`**: when and where the agent first saw the model (ROVER, BITRE, GVG, news). Shows how early each signal is, over time.
- **`onSaleFrom`** and **`untilYear`**: lifecycle.
- **`checked`**: the last date every field was re-read. The validator can warn when it's older than 90 days.
- **Separate file `discovery/seen.json`**: candidates not yet in the catalogue, with status `approved`, `announced`, `on-sale`, `excluded` and the date.

## Not verified

- Whether ROVER's approvals grid loads for an anonymous browser and whether its detail view shows battery or motor data. I read the page's layout definition but did not run a browser or call its data endpoint.
- How long after launch a model appears on the GVG (no stated update frequency).
- BITRE's usual release lag; I saw one release date (29 October 2026 for the September re-issue).
- WhichCar's full terms (403 to automated readers; quoted from a search excerpt). Drive's terms (blocked).
- EV Central's terms page (not found).
- Whether The Driven's terms would object to a monthly automated read of its RSS feed; nothing in them forbids it.
- Makers' newsroom RSS feeds, maker by maker.
- That Leapmotor "A12" on the RAV is the B10, and the name of the further Leapmotor hatch approved in September.
- That the Chery E5 is the Omoda E5 rebadged (same 430 km WLTP; different battery figures: 58.9 vs 61.1 kWh).
- Lepas L6's battery (65 or 67.1 kWh), Luxeed's timing and Chery Q's Australian plans: search results only, articles not opened.
- Forthing's motive power (headline only); GAC Aion UT's Australian specs (headline only).
- Hongqi E-HS9 figures are from one news report, and its price is "not yet confirmed"; Avatr has no Australian specs at all.
- Whether The Driven's monthly sales tables are complete: some makers don't give EV splits, and October's model total was 483 short of the FCAI and EVC combined figure ([The Driven](https://thedriven.io/2026/11/05/australian-electric-vehicle-sales-by-month-in-2026-by-model-and-by-brand-3/)).
- Which makes on The Driven's Compare EVs page (Nio, Honda, Mitsubishi, Blade) are current Australian EVs.
- Whether CC BY 4.0 material can be mixed into an ODbL database without extra permission; avoided here by taking only facts.
- Whether a site's terms bind an automated reader who never agreed to them (Australian law not checked); the note assumes they do and obeys them.
- The legal sources are law-firm commentary from 2010 and 2023, not the judgments themselves, and I didn't check for later cases or reforms.
- ROVER's category filter values (assumed to be ADR codes MA, MC, NA).
- That RAV entries never start before a launch in general; the X9 and B05 are the only two cases checked.
- Whether the EVC's State of EVs Vehicles factsheet lists models.
- US EPA data's public-domain status (not re-checked today).

## Sources

- Government: [ROVER](https://www.rover.infrastructure.gov.au/), [ROVER VTA list](https://www.rover.infrastructure.gov.au/PublishedApprovals/VTAApprovals/), [RAV public search](https://www.rover.infrastructure.gov.au/RAVPublicSearch/), [RAV information](https://www.infrastructure.gov.au/infrastructure-transport-vehicles/vehicles/vehicle-design-regulation/rav), [BITRE statistics](https://www.bitre.gov.au/resource/roads-vehicles/road-vehicle-entry-and-recall-statistics), [BITRE Sep 2026 XLSX](https://www.bitre.gov.au/sites/default/files/documents/Transport%20-%20road%20vehicle%20entry%20and%20recall%20statistics%20-%20Sep%202026%20-%20re-issue.xlsx), [GVG home](https://www.greenvehicleguide.gov.au/), [GVG FAQ](https://www.greenvehicleguide.gov.au/pages/About/FAQ), [GVG newly added](https://www.greenvehicleguide.gov.au/Home/NewlyAddedVehicles), [GVG how-to](https://www.greenvehicleguide.gov.au/pages/ToolsAndCalculators/HowToGuide), [NVES 2025 results](https://www.nvesregulator.gov.au/reporting-and-data/2025-nves-performance-period-results), [department copyright](https://www.infrastructure.gov.au/copyright), [department disclaimer](https://www.infrastructure.gov.au/disclaimers)
- Industry: [FCAI October 2026](https://www.fcai.com.au/competition-drives-strong-new-vehicle-market/), [EVC sales report](https://electricvehiclecouncil.com.au/evc-vehicle-sales-report/), [EVC State of EVs 2026](https://electricvehiclecouncil.com.au/state-of-evs-2026)
- News and their terms: [The Driven feed](https://thedriven.io/feed/), [The Driven EV sales, October 2026](https://thedriven.io/2026/11/05/australian-electric-vehicle-sales-by-month-in-2026-by-model-and-by-brand-3/), [The Driven Compare EVs](https://thedriven.io/compare-evs/), [The Driven terms](https://thedriven.io/terms-of-use), [CarExpert terms](https://www.carexpert.com.au/terms-and-conditions), [CarsGuide conditions](https://www.carsguide.com.au/conditions-of-use), [Chasing Cars terms](https://www.chasingcars.com.au/terms/), [WhichCar terms](https://www.whichcar.com.au/terms-and-conditions), [ANCAP terms](https://www.ancap.com.au/privacy-and-terms-of-use), robots.txt of [The Driven](https://thedriven.io/robots.txt) and [EV Central](https://evcentral.com.au/robots.txt)
- Law and licences: [HWL Ebsworth (2023)](https://hwlebsworth.com.au/protecting-your-data-just-how-far-does-copyright-protect-the-value-of-data/), [MinterEllison (2010)](https://www.minterellison.com/articles/no-copyright-in-white-and-yellow-pages-directories-in-australia-telstras-appeal-fails), [ODbL summary](https://opendatacommons.org/licenses/odbl/summary/), [CC FAQ](https://creativecommons.org/faq/)
- Makers and models: [MG Australia sitemap](https://mgmotor.com.au/sitemap.xml), [MG U9 EV](https://mgmotor.com.au/vehicles/mgu9-ev), [Hyundai robots.txt](https://www.hyundai.com/robots.txt), The Driven articles linked in §5
