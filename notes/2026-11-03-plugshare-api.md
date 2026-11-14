# Can Charge Line use PlugShare's chargers? (2026-11-03)

The user asked whether PlugShare, the popular charger app, has an API Charge Line can use for its many chargers.

## Summary

- **PlugShare has an API, but only under a paid commercial licence.**
  - PlugShare says "we do not support personal or non-commercial licenses to use our data. … our API license is priced for EV industry stakeholders" ([help article, updated 2024-10-16](https://help.plugshare.com/hc/en-us/articles/4418950880659-PlugShare-Charging-Stations-API-Documentation-Access)).
  - No price is published anywhere. You apply through a form that asks how many users the app has and "What is your budget …?" ([access form](https://developer.plugshare.com/access)).
  - The licence is aimed at carmakers' navigation systems and branded apps ([business page](https://company.plugshare.com/business.html)).
  - Charge Line sells Premium, so it counts as commercial and could apply.
- **Taking PlugShare's data without a licence is not an option.** This includes scraping the website, calling the app's private API, or buying from the Apify "PlugShare scraper" sellers.
  - PlugShare's terms forbid it (§1.C, §5).
  - Apple's App Review Guideline 5.2.2 needs permission to use another service's content, and "Authorization must be provided upon request."
- **Free and allowed: link to PlugShare.** PlugShare documents a link that opens its map at a given place ([permalinks](https://developer.plugshare.com/permalink)).
  - A "See it on PlugShare" button on a charger's details would show drivers PlugShare's check-ins, photos and reviews, in PlugShare's own site or app.
  - Costs nothing, copies nothing, and needs no licence. This is the one PlugShare feature worth building now.
- **PlugShare's size is mostly chargers a road trip doesn't need**: wall sockets, slow AC chargers, home chargers drivers share.
  - For fast chargers, Charge Line's free data already has 1,193 Australian sites with DC charging at 24 kW or more (file built 2026-11-02).
  - The EV Council counted about 1,272 such sites in mid-2025 ([State of EVs 2025](https://electricvehiclecouncil.com.au/wp-content/uploads/2025/10/State-of-EVs_2025_141025-2.pdf), p. 59).
  - On 21 real routes, the free data had 90% of Google's fast chargers, and the missing ones barely changed the plans ([2026-10-29 note](2026-10-29-free-data-gaps-and-live-availability.md)).
  - PlugShare would mainly add check-ins, photos and reviews, not many chargers.
- **Recommendation:**
  1. Add the PlugShare link (free).
  2. Keep closing the fast-charger gap with free sources and network feeds.
  3. Ask PlugShare for a quote only once Premium revenue can pay for it. Every A$1,000 a year of licence needs about 22 yearly subscribers (§5).

## 1. What PlugShare offers developers

PlugShare has belonged to EVgo, the US charging network, since EVgo bought Recargo in July 2021 for US$25 million ([The Driven](https://thedriven.io/2021/07/15/plugshare-owner-bought-out-by-us-charging-network-evgo/); [Wikipedia](https://en.wikipedia.org/wiki/PlugShare)). No sale since was found. The [Developer Center](https://developer.plugshare.com/) has three things.

| What | Who it's for | Cost | Usable by Charge Line? |
|---|---|---|---|
| **Charging Stations API** (`api.plugshare.com`) | "EV industry players for incorporation into vehicle head units/nav systems, branded apps, and for direct feeds into analytic systems" ([business](https://company.plugshare.com/business.html)) | Not published; "priced for EV industry stakeholders" | Only with a commercial licence (§3) |
| **Embeddable map** (an iframe from `plugshare.com/widget2.html`) | "any article, blog, or website" ([embed](https://developer.plugshare.com/embed)) | Free, after accepting the terms | Not really: it's PlugShare's own map in a web page, apart from the planner (§4) |
| **Permalinks** (a link to a place or location on PlugShare) | Anyone ([permalink](https://developer.plugshare.com/permalink)) | Free | **Yes** (§4) |

**The API**
- It "currently serves millions of requests per month." Its data comes from "charge point operators, industry partners" and drivers, checked by an "editorial integrity team" ([API page](https://company.plugshare.com/api.html)).
- It includes "driver reviews, user photos, and PlugScore ratings" ([business](https://company.plugshare.com/business.html)).
- The field-level documentation is shown only after access is granted. A third-party listing says it uses HTTP Basic authentication ([RapidAPI directory](https://rapidapi.com/blog/directory/?p=10640)).
- The form calls the first stage an "evaluation license" ([access form](https://developer.plugshare.com/access)).
- Its questions are:
  - the proposed use;
  - the app type (Mobile App, Website, In-Vehicle Navigation App, Multiple Platforms);
  - "How many users will there be?";
  - "Where will the data be used?";
  - "What is your budget for acquiring and using data for this project?";
  - the timeline.
  - It also asks for a business phone and email.

**Other paid products:** advertising to EV drivers, driver research and surveys, and DataTool (a Tableau database for planners). None are relevant ([business](https://company.plugshare.com/business.html)).

## 2. Why scraping or the app's private API is out

**PlugShare's Terms of Use** ([terms](https://company.plugshare.com/terms.html), last modified 4 September 2018) forbid:
- "using any automated system, including without limitation "robots," "spiders," "offline readers,"" (§1.C(ii));
- "accessing any content on the Service through any technology or means other than those provided or authorized by the Service" (§1.C(xi));
- "bypassing the measures we may use to prevent or restrict access to the Service" (§1.C(xii)).

The service is "for your personal, noncommercial use only" (§4.1). Its content "are the exclusive property of Company and its licensors (including other Users who post User Content…)". You may not "sell, license, rent, modify, distribute, copy, reproduce, transmit, … create derivative works" from it (§5). The terms are governed by Californian law.

**Apple** (App Review Guideline 5.2.2): "If your app uses, accesses, monetizes access to, or displays content from a third-party service, ensure that you are specifically permitted to do so under the service's terms of use. Authorization must be provided upon request" ([guidelines](https://developer.apple.com/app-store/review/guidelines/)). Without a licence there is nothing to show Apple, so the app risks rejection or removal.

**Scraper services:** Apify sells PlugShare scrapers from about US$2.45–4.00 per 1,000 stations ([Apify](https://apify.com/solidcode/plugshare-scraper), [Apify](https://apify.com/parseforge/plugshare-scraper)). One reads "PlugShare's public v3 REST API (api.plugshare.com/v3)". That is the app's own API, not a licensed one. One scraper's changelog mentions working around blocked access. Paying a third party doesn't change PlugShare's terms. The earlier notes already ruled this out ([2026-11-02 note](2026-11-02-charger-details-like-abrp.md)).

## 3. What a licence would mean for Charge Line

**Eligible:** Charge Line is a commercial app (Premium in-app purchases), on mobile, used in Australia. Those are exactly the form's questions.

**Price: unknown.**
- Nothing is published ([Datarade](https://datarade.ai/data-providers/plugshare/profile) says the same).
- The help article's wording, "priced for EV industry stakeholders", and the carmaker customers suggest a price set for companies, not a sole developer. That is an inference.
- The only way to know is to ask.

**The public charger file can't hold PlugShare data.**
- Charge Line's charger file is public under the ODbL, because OpenStreetMap's licence asks that the derived database be offered to users (server `GET /v1/chargers/au`).
- Licensed PlugShare data couldn't go into it. It would need its own key-protected route, and almost certainly the licence's own limits on storing and showing the data.
- The licence text isn't public, so its exact limits are unknown.

**What it would add**
- Check-ins and reviews: what ABRP shows as "last successful charge".
- Photos, PlugScore, and the chargers the free data misses.
- Not live status for Australian networks: no PlugShare live feed from Evie, Chargefox or NRMA could be confirmed.
  - NRMA says only that its chargers are listed on PlugShare ([NRMA](https://www.mynrma.com.au/electric-vehicles/charging/ev-charging-stations-australia)).
  - The EV Council calls PlugShare "crowd-sourced and often outdated" ([State of EVs 2025](https://electricvehiclecouncil.com.au/wp-content/uploads/2025/10/State-of-EVs_2025_141025-2.pdf), p. 63). That's a competitor's view: the Council runs its own app, Charge@Large.

## 4. The free option: link to PlugShare

**PlugShare's documented permalinks** ([permalink](https://developer.plugshare.com/permalink)):
- A location: `https://api.plugshare.com/view/location/[location_id]`. Needs PlugShare's own ID, which Charge Line doesn't have.
- A map region: `https://api.plugshare.com/view/map?latitude=…&longitude=…&spanLat=…&spanLng=…`. "When viewed on a computer, links will direct to PlugShare.com. On a mobile device, links will direct to the appropriate app."

**Checked on 2026-11-03**
- The map link redirects (302) to `https://www.plugshare.com/?latitude=-35.270000&longitude=149.130000&spanLat=0.010000&spanLng=0.010000`.
- The location link redirects (301) to `https://www.plugshare.com/location/20840`.
- PlugShare's iOS app-link file on both `api.plugshare.com` and `www.plugshare.com` lists `/location/*`, `/view/location/*` and `/map`. It doesn't list `/view/map` or the bare `/` the map link redirects to.
- So on an iPhone the documented map link probably opens PlugShare's website, not the app. `https://www.plugshare.com/map?…` is on the list and may open the app, but it isn't documented.
- **Needs a test on an iPhone with PlugShare installed** before choosing the link.

**In Charge Line:** a row on the charger details, next to "Photos on Google Maps": "Check-ins and reviews on PlugShare". It opens the map link centred on the site with a span of about 0.005° (≈500 m), and the driver taps the pin.

**Rules**
- PlugShare's terms say nothing against linking to it.
- Use the name in plain text only, not PlugShare's logo (Guideline 5.2.1 covers trademarks).
- Nothing is copied, stored or shown inside Charge Line, so neither the terms nor Guideline 5.2.2 come into it.

**Cost:** A$0 at any number of users. It's one URL built from the site's coordinates.

**The embeddable map isn't worth it**
- It's PlugShare's own map in a web page, for "any article, blog, or website". NRMA uses it on its charging page.
- In the app it would be a separate web map, unconnected to the plan. The link gives the same content in PlugShare's own, better app.

## 5. Coverage: how many chargers would PlugShare add?

**The counts**

| Source | Fast-charging sites in Australia | Definition |
|---|---|---|
| Charge Line's charger file (OSM + Open Charge Map, built 2026-11-02) | **1,193** with DC ≥ 24 kW (1,126 with ≥ 50 kW; 412 with ≥ 100 kW), of 1,832 sites | Highest DC plug, kW from the sources or the network's typical figure |
| EV Council, *State of EVs 2025*, mid-2025 | "around 1272" "high-power public charging locations" | "fast (24-99kW) and DC ultra-fast (100kW+)" (pp. 57–59) |
| Federal government, June 2025 | 1,324 "fast and ultra-fast charging sites" | ([NEV Strategy update 2024-25](https://www.dcceew.gov.au/sites/default/files/documents/national-electric-vehicle-strategy-annual-update-2024-25.pdf), as quoted in search results) |

**What the counts mean**
- Fast sites grew about 20% a year to mid-2025 (EV Council). At that rate there would be about 1,500 by now. That is an estimate, not a count.
- At about 1,500, the file would have roughly 80% of all fast sites in the country.
- On the highways it does better: 90% of Google's fast chargers within 10 minutes of 21 routes. The 31 missing sites were mostly at the city ends of trips, in side towns 14–29 minutes off the highway, and new 2025–26 builds. Every plan still worked ([2026-10-29 note](2026-10-29-free-data-gaps-and-live-availability.md)).
- PlugShare would likely fill much of that gap. So would free routes that are already planned.

**Free ways to close the gap**
- **Network feeds (OCPI)** from Chargefox, Evie or NRMA, as already planned ([2026-11-02 note](2026-11-02-charger-details-like-abrp.md), step 5).
- **Drivers adding chargers to Open Charge Map or OpenStreetMap.** The server rebuilds the file daily, so a charger added there reaches Charge Line within a day. ABRP relies on the same thing ([2026-10-29 note](2026-10-29-cutting-google-costs.md)).
  - A "Missing a charger? Add it to Open Charge Map" link costs nothing.

**Break-even for a licence** (if PlugShare ever quotes)
- Premium yearly is A$59.99 including GST.
- After GST (1/11) and Apple's 15% small-business commission, each yearly subscriber brings in about A$46.
- So every A$1,000 a year of licence needs about 22 yearly subscribers just to cover it. Across users that is:

| Users | Subscribers needed per A$1,000 of licence | Share of users |
|---|---|---|
| 2,000 | 22 | 1.1% |
| 10,000 | 22 | 0.2% |
| 50,000 | 22 | 0.04% |

The table is only useful once there's a real quote.

## 6. Open questions

- What PlugShare would actually charge an Australian app with Charge Line's user numbers, and what its licence allows: storing, caching, showing alongside other data.
- Whether `www.plugshare.com/map?latitude=…` opens the PlugShare app on iOS. Test on a phone.
- How many fast sites the file misses nationally, not just along the 21 routes. Re-run the 2026-10-29 route comparison after format 5 is live.

## Sources

- PlugShare:
  - [API](https://company.plugshare.com/api.html)
  - [Developer Center](https://developer.plugshare.com/)
  - [Access form](https://developer.plugshare.com/access)
  - [Permalinks](https://developer.plugshare.com/permalink)
  - [Embeddable map](https://developer.plugshare.com/embed)
  - [Business](https://company.plugshare.com/business.html)
  - [Terms of Use](https://company.plugshare.com/terms.html)
  - [Help: API documentation & access](https://help.plugshare.com/hc/en-us/articles/4418950880659-PlugShare-Charging-Stations-API-Documentation-Access): read through the help centre's public article API, because the page blocks automated reading.
  - App-link files: `https://api.plugshare.com/.well-known/apple-app-site-association`, `https://www.plugshare.com/.well-known/apple-app-site-association` (fetched 2026-11-03).
  - [App Store listing (AU)](https://apps.apple.com/au/app/plugshare/id421788217): 4.7 from 18K ratings; seller PlugShare LLC.
- Ownership: [The Driven, 2021-07-15](https://thedriven.io/2021/07/15/plugshare-owner-bought-out-by-us-charging-network-evgo/) · [Wikipedia: PlugShare](https://en.wikipedia.org/wiki/PlugShare)
- Apple: [App Review Guidelines 5.2.1, 5.2.2](https://developer.apple.com/app-store/review/guidelines/)
- Third parties: [Apify PlugShare scraper (solidcode)](https://apify.com/solidcode/plugshare-scraper) · [Apify (parseforge)](https://apify.com/parseforge/plugshare-scraper) · [RapidAPI directory](https://rapidapi.com/blog/directory/?p=10640) · [Datarade](https://datarade.ai/data-providers/plugshare/profile)
- Australian counts:
  - [EV Council, State of EVs 2025](https://electricvehiclecouncil.com.au/wp-content/uploads/2025/10/State-of-EVs_2025_141025-2.pdf): pp. 57–59 for counts and definitions; p. 63 for Charge@Large.
  - [DCCEEW NEV Strategy annual update 2024-25](https://www.dcceew.gov.au/sites/default/files/documents/national-electric-vehicle-strategy-annual-update-2024-25.pdf)
  - [The Driven, 2024-07-12](https://thedriven.io/2024/07/12/major-milestone-australia-now-has-more-than-1000-fast-charging-sites/): 1,011 sites, from carloop.
  - [NRMA charging stations page](https://www.mynrma.com.au/electric-vehicles/charging/ev-charging-stations-australia)
- Charge Line's own measurements: the charger file of 2026-11-02 (1,832 sites); [2026-10-29 coverage test](2026-10-29-free-data-gaps-and-live-availability.md).
