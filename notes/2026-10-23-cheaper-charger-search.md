# A Cheaper Charger Search: Open Charge Map First

**Date:** 2026-10-23
**For:** pricing Charge Line 0.2.0 (Premium); the user asked to try the cheaper search before building the subscription
**Question:** Can Open Charge Map supply the chargers for a plan, with Google asked only about the stops the plan uses, and plan as well as Google's search along the route?

## Bottom line

- **No. We keep Google's search along the route.**
  - Open Charge Map (OCM) has **76% of the fast chargers Google finds within 10 minutes of the route**.
  - It **can't plan Melbourne → Broken Hill for a BYD Atto 3** in any "Plan for", while Google's search can.
  - **15% of its plans need more stops.**
- **The cheaper search would cost about a third as much.** It averages 2.4 paid Google calls per plan (Place Details, US$0.025 each), against about 5 searches per trip (US$0.04 each).
- **Google's search costs less than the 2026-10-13 estimate:**
  - Melbourne → Sydney took 9 searches (US$0.36, about A$0.55), not about 10 plus availability refreshes;
  - the 10 trips averaged 4.8 searches (US$0.19, about A$0.29).

## 1. What was compared

- **Google, as the app does it now:**
  - Places Text Search along the route in 200 km windows, up to 2 pages each;
  - merged with OCM's sites within 2 km of the route;
  - live status, plugs, ratings and Google's detour times for every site.
- **The cheaper search, which was built for the trial:**
  1. Plan with OCM's sites near the route (free through Charge Line's server). The detour is estimated from the distance off the route.
  2. Ask Google about each stop the plan uses: a free IDs-only lookup, then one Place Details call.
  3. Plan again with what Google says (plugs, live status, rating).
  4. Repeat while the plan picks stops Google hasn't been asked about, up to 3 rounds.
- **The test set:**
  - Routes (Google's own route for each): Melbourne → Sydney, Melbourne → Adelaide, Sydney → Brisbane, Melbourne → Broken Hill, Sydney → Canberra, Brisbane → Rockhampton, Perth → Albany, Hobart → Launceston, Melbourne → Lakes Entrance, Adelaide → Mount Gambier.
  - Cars: Model Y Long Range, Ioniq 5 Long Range, MG4 Long Range, Atto 3 Extended Range, each at 94% battery health.
  - Every "Plan for", from 90%, with default trip options: 120 cases.
- **Saving Google calls:** the cheaper search's Place Details answers were taken from Google's own search results for the same place, which hold the same fields. So the trial cost only the 48 searches and 10 route requests for the baseline, run twice.
- **Matching:** a Google site and an OCM site are the same place within 150 m (300 m for Superchargers), unless they name different networks.
- **Where it ran:** a debug harness in the app, `-compare-search` (commit `7a60268` in `app/`; removed in `3cfa71c`). The output stayed on the console and was deleted, because Places content can't be stored.

## 2. Results

| | OCM within 5 km | OCM within 10 km (server maximum) |
| --- | --- | --- |
| Google's fast sites (50 kW+) found in OCM | 183 of 340 (53%) | 215 of 341 (63%) |
| Of those within 10 min of the route | — | 167 of 217 (76%) |
| Fast sites only OCM lists | 93 | 172 |
| Cases both plan / only Google plans | 117 / 3 | 117 / 3 |
| Same number of stops | 94 of 117 | 98 of 117 |
| More stops than Google | 21 | 17 |
| Total time within 10 min or 3% | 108 of 117 | 108 of 117 |
| Goes under targets where Google's doesn't | 9 | 9 |
| Stops at sites Google has no charger for | 41 | 36 |
| Detour estimate vs Google's (median) | 2.3 min shorter | 2.0 min shorter |
| Paid Google calls | 2.5 per plan | 2.4 per plan |

**Where the gaps are.** I checked OCM directly around four towns on the Hume (8 km radius, 2026-10-23):

- **Wangaratta:** OCM has only Evie (50 kW, last verified 2023-07-10). Google also lists a Tesla Supercharger (250 kW) and bp pulse (150 kW).
- **Wandong:** OCM has nothing. Google lists NRMA (180 kW).
- **Wodonga:** OCM's Tesla-only Supercharger was last verified 2019-03-22. Google lists a Charge Hub site OCM doesn't have.
- **Yass:** OCM has the Supercharger, NRMA and Chargefox, but more than 5 km off the Hume. A 10 km corridor finds them.

So some of the gap is the corridor, which is fixable, but most of it is missing data. That matches the 2026-10-13 finding that OCM's Australian data is often years out of date.

**Why it fails to Broken Hill.** Mildura → Broken Hill is about 300 km with almost nothing between. With fewer fast sites along the way, the Atto 3 (about 60 kWh) has no mix of stops that gets there, even going under its targets. Broken Hill is the route the user tests coverage with against ABRP.

**OCM-only sites aren't a gain.** Some OCM-only sites are real; Google's search returned no NRMA site at Dog on the Tuckerbox, Gundagai. Others look stale, and a plan that stops at a removed charger is worse than one with an extra stop. In the trial, 36 stops in cheaper plans were at sites Google has no charger for.

## 3. Decision

The user's rule was: use the cheaper search only if it's as good, otherwise keep the current one. It isn't as good on coverage, on plans, or on the route the user cares about most. **Charge Line keeps Google's search along the route, merged with OCM.**

**What this means for Premium pricing (A$6.99 a month, A$59.99 a year):**

- **Cost per trip:** at the measured cost, a trip that needs charging costs about A$0.30 on average and A$0.55 for Melbourne → Sydney.
  - Add a little for Google's alternative routes, which only search the stretches they don't share.
  - Places near each stop is Premium only.
- **Heavy users:** a subscriber planning 8 interstate trips a month costs about A$4.40, under the A$5.40 a month earns after GST and Apple.
- **Fair use:** the cap on Premium still matters for heavier users.

## 4. Worth trying again if

- **OCM's Australian data improves:** check the share of sites verified in the last year.
- **A national dataset of chargers becomes available.**
- **A hybrid is wanted:** OCM first, with Google searching only the stretches where OCM has few fast sites. That wasn't tested.

The harness in `7a60268` reruns the comparison in about two minutes, for about 48 Google searches.
