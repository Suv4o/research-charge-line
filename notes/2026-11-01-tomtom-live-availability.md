# TomTom live availability: does it fill the Tesla and NRMA gap?

**Date:** 2026-11-01
**Question:** Google's API has no live status for Tesla Superchargers (0 of 78) or NRMA (1 of 35)
([2026-10-29-free-data-gaps-and-live-availability.md](2026-10-29-free-data-gaps-and-live-availability.md) §5).
TomTom lists Australia with live "EV Dynamic" data. Does it have those two networks?
**Answer: no.** TomTom lists the sites, but has no live status for any Supercharger or NRMA site in the
sample. For the other networks it has live status at every site it found, as Google does.

## The test

- **Key:** the user's free TomTom key ("Evaluation" billing), in `server/.env` as `TOMTOM_KEY`.
- **Sample:** 65 fast sites from Charge Line's charger file (production, 2026-10-31), spread across
  Australia: 20 Tesla, 15 NRMA, 10 Evie, 10 Chargefox, 5 Ampol AmpCharge, 5 bp pulse.
- **Calls:**
  - Search API `nearbySearch` within 300 m, category 7309 (EV charging stations), nearest by the network's
    name.
  - Then, if the result carries `dataSources.chargingAvailability.id`, the EV Charging Stations
    Availability API (`/search/2/chargingAvailability.json`).
  - About 100 requests in all, within the free daily allowance.
- **Harness:** a script in the session scratchpad, not kept.

| Network | Sampled | Found on TomTom | With an availability ID | With live counts |
| --- | --- | --- | --- | --- |
| **Tesla Supercharger** | 20 | 20 | **0** | **0** |
| **NRMA** | 15 | 13 | **0** | **0** |
| Evie | 10 | 10 | 10 | 10 |
| Chargefox | 10 | 9 | 9 | 9 |
| Ampol AmpCharge | 5 | 5 | 5 | 5 |
| bp pulse | 5 | 5 | 5 | 5 |

**What the results show:**
- **Live counts look real.** For example, "bp pulse Glenrowan South: 2 free, 1 in use, 1 out of service of
  4", and "Evie Bundamba: 2 of 4 out of service".
- **Superchargers and NRMA have no `dataSources` at all.** TomTom has their static data only.
- **TomTom's static data has every Supercharger's power** (250 or 300 kW for V3/V4, 125–130 kW for older
  sites), where our file estimates 250 kW.
  - That power can't simply be copied into our file: TomTom's terms on storing its data weren't checked.
  - Supercharge.info (the email draft) remains the way to get it.
- **A few name matches went to a neighbouring network** (Chargefox → Exploren, Evie → EVUp). A real
  integration would match by distance and network, as `LiveStatus` does for Google.

## What it means

1. **TomTom doesn't close the Tesla and NRMA gap.** No provider we can reach has their live status:
   - not Google;
   - not TomTom;
   - not HERE or PlugShare as of November 2025.
   The NRMA email is still the way for NRMA. For Superchargers, a Tesla owner's own car stays the only
   source.
2. **TomTom could replace Google for Premium's live checks on the other networks**, at a lower cost:
   - **Today with Google:** about US$25 per 1,000 checks after the free calls.
   - **With TomTom:** a free daily allowance (2,500 non-tile requests a day on its FAQ), and each check is
     two calls (search, then availability).
   - **Not worth switching yet:**
     - Google's free monthly Place Details calls cover early use.
     - TomTom's terms weren't verified: the page needs a browser to read. The open questions are showing
       its data on a Google map, keeping its IDs, and what "Evaluation" billing allows in production.
       TomTom's key docs describe "Evaluation" as billing under an evaluation agreement.
   - **Revisit** if live checks grow past Google's free calls.
3. **Nothing changes in the app.**

## Sources

- [EV Charging Stations Availability API](https://docs.tomtom.com/ev-charging-stations-availability-api/documentation/ev-charging-stations-availability-api/ev-charging-stations-availability): request, parameters, response, and "updates ... typically within minutes".
- [EV Search API introduction](https://docs.tomtom.com/ev-search-api/documentation/tomtom-orbis-maps/product-information/introduction) and [FAQ](https://developer.tomtom.com/ev-search-api/documentation/product-information/faq): the newer EV Search (Nearby) isn't part of the free evaluation or Pay As You Grow.
- [API key management](https://developer.tomtom.com/knowledgebase/platform/articles/api-key-management): billing types, including Evaluation.
- [Platform FAQ](https://docs.tomtom.com/platform/documentation/faqs): commercial use, daily free requests, QPS limits.
