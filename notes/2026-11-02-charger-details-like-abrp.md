# Charger Details Like ABRP's: Photos, Payment, Prices and "Last Successful Charge", Cheaply

**Date:** 2026-11-02
**For:** the user. ABRP's charger screen shows photos, payment methods, prices per membership, "Last successful charge: 2 hours ago", ratings, amenity votes and nearby places with links. "My bill from Google came and I spend $31.55 AUD so far and that is only me … all implementation we need to make sure is cost effective."
**Question:** Where does ABRP get each of those details? How can Charge Line show the same in Australia at the lowest running cost?

## Bottom line

- **Most of ABRP's details come from its own users, not from a paid feed.**
  - Photos: users upload them (since ABRP 4.7, December 2023).
  - Ratings and amenity votes: users.
  - "Last successful charge": "reported from a user, charger, or vehicle live data" (ABRP 6.0, May 2025).
  - Prices: ABRP doesn't say. The "Direct payment" price plus roaming-membership prices is how OCPI tariff data is structured, as sold by data companies or exchanged in network partnerships. That is an inference.
- **What's free in Australia today is thin** (measured below):
  - Open Charge Map has photos for 10% of our fast sites, and recent ones for only 4%.
  - Its check-ins give a successful charge in the last 90 days at only 16 fast sites.
  - OpenStreetMap has payment methods for 5% of fast sites and prices for 3%.
- **Google has the most, and two parts of it are free or already paid for:**
  - **The photo list is free.** Place Details' `photos` field is in the free "IDs Only" tier. Google has photos for **87%** of the fast chargers it found (sample of 142).
    - Each image downloaded costs US$7 per 1,000, after 1,000 free a month.
    - Images can't be cached.
  - **Payment options, rating, hours and website cost nothing extra for Premium.** They're billed in the same tier as `evChargeOptions` (or a lower one), and Premium's live-status call already pays for that tier. Adding them to the same call is free.
  - Google had payment flags for 36 of 36 sampled sites, a rating for 31, and hours for 30.
- **Recommendation, cheapest first:**
  1. **Free data, now (A$0 a month):**
     - Open Charge Map photos and check-ins in our daily file.
     - OpenStreetMap hours, payment, price and nearby-place website links.
     - Each network's usual payment methods, from a table we keep.
     - A free "Photos on Google Maps" button.
  2. **Premium: Google's photos, payment options, rating, hours and website** from the calls Premium already makes. The only new cost is images: about **US$6 a month at 2,000 users and US$60 at 10,000**.
  3. **Check-ins from our users:** "Charged here?" ✓/✗, plus optionally the price paid and how they paid. This gives "Last successful charge", real prices and payment methods for everyone. It runs on our existing server (A$0 extra).
  4. **Our own photo uploads,** as ABRP does. Cloudflare R2's free 10 GB holds about 20,000 photos. The cost is moderation work, not money.
  5. **A data deal with Chargefox.** It's the roaming hub for NRMA, AGL and EVX, and has direct access to RAA, WA EV Network, Yurika and RACV chargers. One OCPI feed would give real prices, payment methods, "last used" and NRMA's live status, which no provider we can reach has today.
- **Don't** show Google photos, ratings or payment options to free users:
  - photos for everyone would cost about **US$700 a month at 10,000 users**;
  - payment, rating and hours for everyone, about **US$1,400**.
  - Street View in the app costs twice as much per view as a photo.
- **The A$31.55 bill** was most likely October's per-trip charger searches (US$40 per 1,000), which the hybrid removed on 31 October (§6).

## 1. ABRP's charger screen, detail by detail

From the user's screenshots (Chargefox, 1 Pine St, Keith SA) and ABRP's own release notes:

| What ABRP shows | Where it comes from | Evidence |
| --- | --- | --- |
| Photos (3 shown, "+1") | **ABRP users' uploads**: "you can now upload and view photos of charger locations … community-driven" | [ABRP 4.7](https://abetterrouteplanner.com/resources/article/2023-12-22_abrp-4-7) (22 Dec 2023); "real photos" on charger cards in [ABRP 7.1](https://abetterrouteplanner.com/resources/article/2026-05-12_abrp-7-1) (12 May 2026) |
| Rating 4.5 (20 ratings), "Your rating", "Add photo" | ABRP users | ABRP 4.7 ("Building on our ratings and characteristics features") |
| "Last successful charge: 2 hours ago" | "the time of the most recent successful charging session (reported from a user, charger, or vehicle live data)" | [ABRP 6.0](https://abetterrouteplanner.com/resources/article/2025-05-09_abrp-6-0) (9 May 2025) |
| "Open 24 hours" | ABRP 6.0 shows "opening hours (if not 24/7)". The source isn't named | ABRP 6.0 |
| "Your rates: Direct payment A$0.79/kWh" with contactless and card icons; "ChargeFox Roaming A$0.87/kWh" | **Not published.** The user adds charge cards and "the prices associated with the card will be shown in the plan" ([help](https://abrp.featurebase.app/help/articles/5884894-charge-cards)). The split (operator's price for paying on the spot, plus each membership's price) and the payment icons match OCPI tariffs and capabilities. That's what data companies such as Eco-Movement sell and what network partnerships exchange (*inference*). Users report wrong prices ([example](https://abrp.featurebase.app/p/inconsistent-pricing-within-ionity)) | — |
| Amenities "Food nearby", "Restroom" with "Show votes" | ABRP users' votes ("characteristics") | ABRP 4.7 |
| Nearby: "bp", "Shell SELECT", "BP Shop" with link icons, 40–50 m | Not named. The names and links look like OpenStreetMap places with `website` tags (*inference*) | — |
| Chargers themselves | OpenStreetMap, Open Charge Map, Supercharge.info, GoingElectric, partner feeds | [2026-10-29-cutting-google-costs.md](2026-10-29-cutting-google-costs.md) §2 |
| Reliability scores (US) | Rivian vehicles' charging sessions, shown in ABRP | [SlashGear, 20 Jun 2024](https://www.slashgear.com/1606691/rivian-better-route-planner-reliability-scores) (secondary) |

**Takeaway:** ABRP's rich screen is mostly community data it collects itself, at almost no per-view cost. Prices are the exception, and ABRP doesn't say where they come from.

## 2. What's available in Australia (measured 2026-11-02)

"Fast" means a DC plug or 50 kW or more. Our file is production's `/v1/chargers/au` (1,832 sites, 1,242 fast).

### 2.1 Open Charge Map: free, CC BY 4.0, photos and check-ins included

- **Licence:** "All information you submit (including charging equipment information, comments, check-ins and photos)" is "redistributed under an Open Data license" ([guidance](https://openchargemap.org/about/guidance)). That licence is CC BY 4.0, with the data provider credited where users see it ([terms](https://beta.openchargemap.org/about/terms), updated 01/04/2022).
- **The API already has it:** `includecomments=true` adds `MediaItems` (photo and thumbnail URLs, the uploader's name, date) and `UserComments`. Comments carry a check-in status such as "Charged Successfully" or "Failed to Charge", a 1–5 rating and a date. Our server asks with `verbose=false` and no comments today.
- **Coverage, all operational AU sites (1,356; 820 fast):**

| | All | Fast |
| --- | --- | --- |
| Sites with a photo | 177 (520 photos) | **109** |
| … a photo from the last 3 years | — | **43** |
| Sites with a positive check-in in the last 90 days | 17 | **15** |
| … in the last 365 days | 30 | 24 |
| Ratings (1–5 stars) | 189, among the 142 sites with comments | — |

- **Matched to our file** (within 200 m, the merge's rule):
  - 125 of 1,242 fast sites (**10%**) would get a photo, and 48 (**4%**) a photo from the last 3 years.
  - 16 (**1%**) would get a successful check-in from the last 90 days.
  - Photos are mostly Chargefox (57 sites), Tesla (24), Evie (14) and NRMA (8). Most date from 2020–2024.
- **Verdict:** free and worth adding, but too thin to carry the feature. Check-ins are too sparse for "last successful charge".

### 2.2 OpenStreetMap: free, ODbL

1,631 public charging stations, 879 fast:

| Tag | Fast sites | Share |
| --- | --- | --- |
| `fee` (yes/no) | 269 | 31% |
| `opening_hours` | 175 | 20% |
| `website` / `contact:website` | 130 | 15% |
| `authentication:*` (app, NFC, membership card…) | 68 | 8% |
| `payment:*` (app 33, contactless 13, credit cards 13) | 45 | 5% |
| `charge` (price, e.g. "$0.66/kWh", "51c/kWh $1/min idle fee") | 24 | 3% |
| `image`, `wikimedia_commons`, `mapillary`, `panoramax` | 0 | 0% |
| `brand:wikidata` / `network:wikidata` | 834 | 95% |

- **Nearby places with links** (the "link" icons in ABRP's list):
  - Of 70,373 named food, fuel and shop places in Australia, 18,006 (**26%**) have a `website`, and 19,550 (28%) a `brand:wikidata`.
  - Our weekly nearby query can add the website for little cost.
- **Verdict:** add `opening_hours`, `payment:*`/`authentication:*`, `charge` and nearby websites to the file. They cost nothing, but no photos are available here.

### 2.3 Google Places: the most coverage, priced per call

**Which fields cost what** ([data fields](https://developers.google.com/maps/documentation/places/web-service/data-fields), [pricing](https://developers.google.com/maps/billing-and-pricing/pricing)). A call is billed at the highest tier among the fields it asks for:

| Field | Place Details tier | Price per 1,000 (free a month) | Text Search tier |
| --- | --- | --- | --- |
| `photos` (list of photos) | **Essentials (IDs Only)** | **free, unlimited** | Pro |
| `rating`, `userRatingCount`, `regularOpeningHours`, `websiteUri` | Enterprise | US$20 (1,000) | Enterprise |
| `paymentOptions` (credit, debit, NFC, cash only), `evChargeOptions`, `evChargeAmenitySummary`, `restroom` | Enterprise + Atmosphere | US$25 (1,000) | Enterprise + Atmosphere (US$40) |
| Each photo image (Place Photos) | Place Details Photos | **US$7 (1,000)** | — |
| Street View panorama in the iOS SDK | Dynamic Street View | US$14 (5,000) | — |

- **Premium already pays for the top tier:**
  - `LiveStatus` asks Place Details for `displayName,evChargeOptions` (Enterprise + Atmosphere).
  - The Premium Chargers tab's area search asks for `evChargeOptions` too.
  - So adding `photos,paymentOptions,rating,userRatingCount,regularOpeningHours,websiteUri` to those calls is **free**.
- **Rules for photos** ([Place Photos](https://developers.google.com/maps/documentation/places/web-service/place-photos), [policies](https://developers.google.com/maps/documentation/places/web-service/policies)):
  - "You cannot cache a photo name … the name can expire."
  - Credit each photo's authors wherever it's shown. A thumbnail can skip this if tapping it opens a larger version that has the credit.
  - People must be able to see the photo on Google Maps: each photo has a `googleMapsUri` and a `flagContentUri`.
  - Ratings need Google's review-policy notice.
  - Each image is downloaded again each time it's shown, and each download is billed.
- **Sample** (142 fast sites spread across networks and states; 304 calls, all within free tiers):

| Network | Sampled | Found (same network) | With photos | Median photos | Payment flags* | Card / NFC true* | Rating* | Hours* |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tesla | 20 | 19 | 17 | 10 | 4/4 | 0 / 0 | 4/4 | 4/4 |
| Evie | 20 | 18 | 18 | 5 | 4/4 | 0 / 0 | 3/4 | 4/4 |
| Chargefox | 20 | 20 | 16 | 2 | 4/4 | 2 / 1 | 4/4 | 3/4 |
| NRMA | 15 | 15 | 13 | 5 | 4/4 | 1 / 1 | 2/4 | 2/4 |
| Ampol AmpCharge | 15 | 15 | 15 | 5 | 4/4 | 3 / 2 | 4/4 | 4/4 |
| bp pulse | 12 | 11 | 11 | 10 | 4/4 | 4 / 4 | 4/4 | 4/4 |
| Jolt | 10 | 10 | 7 | 1 | 4/4 | 2 / 2 | 3/4 | 3/4 |
| Exploren | 10 | 10 | 5 | 2 | 4/4 | 2 / 2 | 4/4 | 3/4 |
| Other | 20 | 8 | 7 | 9 | 4/4 | 1 / 1 | 3/4 | 3/4 |
| **All** | **142** | **126 (89%)** | **109 (87% of found)** | | **36/36** | **15 / 13** | **31/36** | **30/36** |

\* Four sites per network, from one Place Details (Enterprise + Atmosphere) call each.

- **What the sample says:**
  - Google has photos almost everywhere, Superchargers included.
  - Payment flags exist for every site. The card/NFC values match expectations (bp pulse and Ampol take cards; Tesla is app-only) but weren't checked on site.
  - `evChargeAmenitySummary` (Google's AI summary of amenities) was empty for all 36: not offered in Australia yet.
  - Every site's `websiteUri` is the network's home page (tesla.com, evie.com.au…), so it adds nothing.
- **Nothing was kept:** the script held Google's answers in memory and printed counts only.

### 2.4 Government guidance: card payment and published prices, not an open feed

The Energy and Climate Ministerial Council's [minimum operating standards for government-supported public EV charging](https://www.dcceew.gov.au/sites/default/files/documents/minimum-operating-standards-electric-vehicles-charging-infrastructure.pdf) (under the April 2023 National EV Strategy; guidance, not retrospective):

- **Payment:** "DC charging sites should provide an option for payment that: supports credit and debit card transactions; does not require registration or app download prior to arriving at the charging station; does not require a payee's mobile or internet signal."
- **Pricing:** fees (per kWh, per minute, session, idle, surcharges) "clearly displayed" at the site.
- **Data:** "CPOs should provide timely and accurate data that publicly shows the availability status and pricing of a charging station's charging bays via an online platform."
- **Meaning for us:**
  - Newer funded DC sites should take cards. That's a reasonable default label for them, but we can't tell which sites were funded.
  - "Via an online platform" means the network's own app or website, not an open API.
  - It is useful leverage when asking networks for a feed.

### 2.5 Partnerships and commercial data

- **Chargefox is a roaming hub.** NRMA was the first network to roam onto it ([CarExpert, 31 May 2024](https://carexpert.com.au/car-news/this-ev-charging-provider-wants-to-help-you-find-a-charger-even-if-it-isnt-theirs)).
  - By December 2025 it roamed NRMA, AGL and EVX, with direct access to RAA (SA), WA EV Network, Yurika (QLD) and RACV ([Carloop, 14 Dec 2025](https://carloop.com.au/charging/more-charging-networks-roaming-onto-chargefox-simplifies-public-ev-charging-experience/), secondary).
  - Chargefox's sites, NRMA, Yurika and RAA are about **550 of our 1,832 sites**.
  - One OCPI data agreement with Chargefox could give locations, live status, tariffs and payment capabilities for all of them. That includes NRMA's live status, which neither Google (1/35) nor TomTom (0/13) has ([2026-11-01-tomtom-live-availability.md](2026-11-01-tomtom-live-availability.md)).
- **Eco-Movement** sells charging data over OCPI (locations, availability, tariffs) to navigation apps and lists Australia among its countries. Its price is a quote on request, and Dow Jones bought it in September 2025 ([Eco-Movement](https://eco-movement.com/), vendor claims). Not affordable now; ask for a quote once revenue supports it.
- **PlugShare, ABRP, the networks' apps:** scraping is against their terms. Not an option.

### 2.6 Our own users: check-ins and photos

- **Check-ins** ("Charged here?" ✓/✗, optionally the price paid and how):
  - **Server:** the existing Fly machine and volume (SQLite), with no extra hosting. The daily file carries each site's last successful and failed check-in.
  - **No free text,** so moderation is light: rate limits and outlier checks.
  - **Value grows with users:** sparse at launch, like OCM's.
  - **App Privacy needs updating:** "Other User Content", not linked to the user. So does the privacy policy.
- **Photos:**
  - **Storage:** Cloudflare R2's free tier is 10 GB-month, 1 million writes and 10 million reads a month, with **free egress**. After that, US$0.015 per GB-month ([R2 pricing](https://developers.cloudflare.com/r2/pricing/)). 10 GB is about 20,000 photos at 500 KB.
  - **Apple guideline 1.2** applies to user-generated content: "A method for filtering objectionable material from being posted", "A mechanism to report offensive content and timely responses", "The ability to block abusive users", "Published contact information" ([App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)).
  - **Cheapest compliant setup:** photos stay hidden until approved (the user approves them), plus a report button, a per-install block list, and the support email that's already published.
  - **Licence:** uploaders agree to CC BY 4.0, matching the open file. The photos could also go to Open Charge Map.

## 3. Cost by option

**Assumptions** (as in the 2026-10-29 note):
- 5% of users are Premium.
- A free user opens 6 stop or charger details a month, a Premium user 12.
- 1.6 photo images per opening (one shown, more if they swipe).
- US$ at Google's first-tier price, after the monthly free calls.

| Option | Covers | 2,000 users | 10,000 users | 50,000 users |
| --- | --- | --- | --- | --- |
| OCM photos and check-ins, OSM hours, payment, price and links, network payment table | 10% photos; hours 20%; payment from the network table | **$0** | **$0** | **$0** |
| "Photos on Google Maps" button (free IDs-only lookup + [Maps URL](https://developers.google.com/maps/documentation/urls/get-started), no key) | All found places, in the Google Maps app | **$0** | **$0** | **$0** |
| **Premium:** payment, rating, hours from the call already made | Premium's checked stops and chargers | **$0** | **$0** | **$0** |
| **Premium:** Google photos (images only) | 87% of fast sites | ~$6 | ~$60 | ~$330 |
| Everyone: Google photos | 87% | ~$135 | ~$700 | ~$3,500 |
| Everyone: payment, rating, hours from Google | ~90% | ~$285 | ~$1,400 | ~$7,100 |
| Everyone: Street View panorama instead of photos | Roadside view only | ~$105 | ~$810 | ~$4,300 |
| Check-ins on our server | Grows with users | $0 | $0 | ~$5 (bigger machine) |
| Our own photos on R2 | Grows with users | $0 | $0 | ~$0–1 |
| Chargefox / NRMA OCPI feed | ~550 sites, real prices and live status | $0 (by agreement) | $0 | $0 |

For scale, the 2026-10-29 note puts Premium revenue at about US$300 a month at 2,000 users and US$1,500 at 10,000. Premium photos cost about 4% of it.

## 4. Plan

1. **Free data in the file (about 2–3 days, A$0 a month).**
   - **Server:**
     - Ask Open Charge Map with `includecomments=true`. Keep up to 3 photos per site (thumbnail, full, uploader, date), plus the latest successful and failed check-in dates.
     - Read OSM's `opening_hours`, `payment:*`, `authentication:*` and `charge`.
     - Add `website` (or the brand's site) to nearby places.
     - Bump the file `format`. The file grows by about 50 KB gzipped (214 KB today).
   - **App, charger and stop details:**
     - a photo strip, credited "Photo: name · Open Charge Map (CC BY 4.0)";
     - "Open 24 hours" when known;
     - "Pay with: app, RFID card, contactless…". This comes from the site's tags, else the network's usual methods from a table we keep, labelled "usually".
     - "Last successful charge: 3 weeks ago (Open Charge Map)" when known;
     - links on nearby places;
     - **"Photos on Google Maps"** for everyone.
   - The network table needs each network's help page checked (Tesla, Evie, Chargefox, NRMA, Ampol, bp pulse, Jolt, Exploren…).
2. **Premium details from Google (about 1–2 days; +US$6–60 a month).**
   - Add `photos,paymentOptions,rating,userRatingCount,regularOpeningHours` to `LiveStatus`'s Place Details call and to the Premium Chargers search. This adds nothing to the per-call price.
   - **Photos:**
     - Load one image when a detail opens, and more only on swipe.
     - Size it to the screen. Don't prefetch or cache.
     - Credit the author with a link, plus "Google Maps".
     - Tapping a photo opens it on Google Maps (`googleMapsUri`).
   - **Tesla and NRMA stops** (Google has no live status, so they get no Details call): fetch the photo list with the free `photos`-only Details call. Payment comes from the network table.
   - **Set a Google Cloud quota** on Place Photos (e.g. 300 a day) and a budget alert.
3. **Check-ins for everyone (about 1 week).**
   - **The prompt:** "Charged here?" ✓/✗ on a stop during or after the trip, and on any charger's detail.
   - **Optional extras:** the price paid per kWh and how they paid (chips).
   - **Server:** stores them anonymously. The file shows "Last successful charge", "Price reported by drivers" and "Pay with" per site.
   - **Also:** update App Privacy and the privacy policy. Optionally send failures to Open Charge Map as well.
4. **Photo uploads (about 1–2 weeks, plus approving photos).**
   - **Storage:** Cloudflare R2.
   - **Moderation:** photos go public only after approval; a report button; a per-install block list.
   - **Licence:** CC BY 4.0.
   - **When:** once check-ins show people engage.
5. **Partnership emails, in parallel (free; weeks to months).**
   - **Chargefox:** a data feed for a navigation app (locations, status, tariffs, payment capabilities), citing the government standard's "data" outcome.
   - **The NRMA email:** already drafted.
   - **Later:** Evie, Ampol, bp pulse, Jolt and Exploren.
   - A feed gives real "Direct payment" and membership prices like ABRP's, and live status for NRMA.

**Free product features from ABRP's screen** (no data cost): prefer or avoid a network, bookmark, share, "Report issue" (feeds check-ins) and "Avoid in planning".

## 5. Terms to respect

- **Google:**
  - Photos and ratings are shown only where they're fetched, never stored.
  - Photo names expire.
  - Author credit and "Google Maps" attribution; ratings need the review-policy notice.
  - Content only with our Google map, as today.
  - **Place IDs** may be stored on the phone, as `LiveStatus` already does.
  - Don't put them in the public ODbL file. Publishing Google identifiers to everyone is a different question from storing them.
- **Open Charge Map:**
  - Credit the data provider, as today.
  - Photos are loaded from OCM's media server, as its own apps do. If traffic grows, mirror the thumbnails or ask OCM.
- **OpenStreetMap:** ODbL, as today. Website links are OSM data.
- **Our users' content:** Apple guideline 1.2 (§2.6), and the privacy label.

## 6. The A$31.55 bill

- **Before 31 October,** each trip that needed charging ran about 4.8 Text Searches with live availability (US$40 per 1,000 after 1,000 free a month). Chargers-tab searches and Google's places nearby added more.
- **A$31.55 is roughly US$20,** about 500 searches past the free 1,000, or about 300 test trips. That fits a month of testing.
- **Since the hybrid,** a free user's trip makes only calls inside free monthly allowances:
  - the route (10,000 free);
  - address search (10,000 free; sessions free);
  - the destination's location (10,000 free).
  - Premium's live checks and area searches get 1,000 free a month each.
- **To confirm:** Google Cloud console → Billing → Reports, group by SKU, and compare October with November.
- **Still to set** (from 2026-10-29): a budget alert and daily quotas on Text Search and Place Photos, so a bug can't run up a bill.

## Method

- **Open Charge Map:** `/v3/poi?countrycode=AU&includecomments=true&compact=false&verbose=false` (5.7 MB). Counted, then deleted.
- **OpenStreetMap:** Overpass, `amenity=charging_station` in Australia with tags (0.6 MB), and counts of named food, fuel and shop places with `website` or `brand:wikidata`.
- **Google:** with the app's key and bundle ID, for 142 fast sites from production's file:
  - an IDs-and-name Text Search within 250 m (Text Search Pro: 142 calls, 5,000 free a month);
  - a `photos`-only Place Details call (126 calls, free);
  - for 4 sites per network, one Place Details call with `paymentOptions,rating,userRatingCount,regularOpeningHours,websiteUri,evChargeAmenitySummary` (36 calls, 1,000 free a month).
  - Only counts were printed.
- **Scripts:** in the session scratchpad, not kept.

## Sources

- **ABRP:**
  - releases: [4.7](https://abetterrouteplanner.com/resources/article/2023-12-22_abrp-4-7) · [6.0](https://abetterrouteplanner.com/resources/article/2025-05-09_abrp-6-0) · [7.1](https://abetterrouteplanner.com/resources/article/2026-05-12_abrp-7-1)
  - [Charge cards help](https://abrp.featurebase.app/help/articles/5884894-charge-cards) · [price feedback example](https://abrp.featurebase.app/p/inconsistent-pricing-within-ionity) · [Rivian scores in ABRP (SlashGear)](https://www.slashgear.com/1606691/rivian-better-route-planner-reliability-scores)
- **Google:** [Places data fields and SKUs](https://developers.google.com/maps/documentation/places/web-service/data-fields) · [pricing list](https://developers.google.com/maps/billing-and-pricing/pricing) · [Place Photos](https://developers.google.com/maps/documentation/places/web-service/place-photos) · [Places policies](https://developers.google.com/maps/documentation/places/web-service/policies) · [Place and Photo reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places) · [Maps SDK for iOS billing](https://developers.google.com/maps/documentation/ios-sdk/usage-and-billing) · [Maps URLs](https://developers.google.com/maps/documentation/urls/get-started)
- **Open Charge Map:** [terms](https://beta.openchargemap.org/about/terms) · [contributor guidance](https://openchargemap.org/about/guidance)
- **Australia:**
  - [Minimum operating standards for government-supported public EV charging](https://www.dcceew.gov.au/sites/default/files/documents/minimum-operating-standards-electric-vehicles-charging-infrastructure.pdf)
  - Chargefox roaming: [CarExpert](https://carexpert.com.au/car-news/this-ev-charging-provider-wants-to-help-you-find-a-charger-even-if-it-isnt-theirs) · [Carloop (secondary)](https://carloop.com.au/charging/more-charging-networks-roaming-onto-chargefox-simplifies-public-ev-charging-experience/)
- **Other:** [Eco-Movement](https://eco-movement.com/) · [Cloudflare R2 pricing](https://developers.cloudflare.com/r2/pricing/) · [App Review Guidelines 1.2](https://developer.apple.com/app-store/review/guidelines/)
