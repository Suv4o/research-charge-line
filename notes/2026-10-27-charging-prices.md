# Charging Prices: Where They Can Come From

**Date:** 2026-10-27
**For:** Charge Line 0.2.0 Premium: each charger's price, and what a trip's charging will cost
**Question:** Is there a source of per-site charging prices for Australian networks? If not, what's the most honest estimate a trip planner can give?

## Bottom line

- **No source gives real per-site prices.** Every network sets prices per site, and some by the time of day. Only its own app shows the price, and none has a public API.
  - Google Places has no price field for chargers (only `fuelOptions.fuelPrices` for petrol), as the 2026-10-13 note found.
  - Tesla's Fleet API shows no Supercharger prices. Tesla prices "dynamically" per site, shown in the Tesla app.
  - OCPI tariffs (the roaming standard) are the long-term route, but that means a business deal with each network.
- **Open Charge Map has a price for 71% of fast sites, but most are old.**
  - In a sample of 125 fast sites around Melbourne, Sydney and the Hume (via Charge Line's server), 89 had a `UsageCost`.
  - 59 of those were last checked in 2023. Prices have risen since: Evie listings say 40c, and one checked in September 2026 says 62c at night and 71c by day.
- **What the app does:** it gives an **estimate**, labelled as one, from the best price it has.
  1. The driver's own price for the network, set in Settings › Charging prices.
  2. The site's price on Open Charge Map, if it was checked in the last 12 months.
  3. The network's typical price (below).
  4. A typical Australian price: 65c for a fast charger, 40c for an AC post.

## 1. What the networks say

| Network | What they publish | Typical price used |
| --- | --- | --- |
| Tesla Supercharger | Prices vary by site ("dynamic pricing"), shown in the Tesla app; a Supercharging Membership lowers the price for other EVs ([Tesla AU](https://www.tesla.com/en_au/support/charging/supercharging)) | 55c for Teslas, 65c for other EVs |
| Evie | Varies by site: "around $0.40" at a 50 kW highway site to "up to $0.75" ultra-fast in Melbourne; $0.64 as an example ([Evie help](https://support.goevie.com.au/hc/en-us/articles/7389896864911-How-much-does-it-cost-to-charge)). OCM listing (Sep 2026): $0.62 9pm–9am, $0.71 9am–9pm | 69c |
| Chargefox | Site owners set the price ([Chargefox help](https://support.chargefox.com/hc/en-au/articles/7835561201167-How-much-does-it-cost-to-charge)); fast DC "40–60c per kWh on average" ([Chargefox](https://www.chargefox.com/news/public-charging-myths-busted)) | 60c |
| Ampol AmpCharge | Varies by location, shown in the Ampol app ([AmpolCard terms](https://ampcharge.ampol.com.au/policies/ampolcard-with-ev-charging-terms-and-conditions)). OCM listings: $0.60–0.75 | 69c |
| BP Pulse | "Pricing may vary between bp pulse locations", some with peak and off-peak ([bp pulse FAQs](https://www.bp.com/en_au/australia/home/products-services/bppulse/faqs.html)) | 65c |
| NRMA | Location-based; site prices $0.69–0.99 in the My NRMA app, members 5c/kWh less ([NRMA](https://www.mynrma.com.au/electric-vehicles/charging)) | 79c |
| Jolt | 7 kWh free a day at fast chargers, then paid ([Jolt fair use](https://jolt.com.au/fair-use-policy)). OCM listings: $0.40–0.46 after the free 7 kWh | 45c, first 7 kWh free once a trip |

Third-party guides for 2026 put public DC fast charging at about 45c–80c per kWh. They disagree on individual networks, so they were used only as a cross-check.

## 2. Open Charge Map's `UsageCost`

- **Coverage (fast sites, 2026-10-27):** Chargefox 32 of 35, Evie 18 of 37, BP Pulse 9 of 11, Tesla 12 of 16, Ampol 6 of 11, Jolt 5 of 7, NRMA 2 of 2.
- **When checked:** 2019 (1), 2020 (2), 2021 (2), 2022 (5), 2023 (59), 2024 (8), 2025 (3), 2026 (9).
- **Formats:** free text, for example "55c/kWh", "AUD 0.42/kWh", "$0.45 per kWh", "80c kWh", "69c / KwH" and "0.30c/kWh" (meaning $0.30).
  - Time of use: "$0.62/kWh 9pm-9am, $0.71/kWh 9am-9pm".
  - Free energy first: "First 7kWh free, then $0.40 per kWh", "$0.00/kWh up to 7 kWh then $0.40/kWh".
  - Free: "Free", "Charging is free".
  - No price: "Supercharger rates".
- **How it's read:** every amount next to "kWh" is a price, and per-hour amounts (idle and overstay fees) are left out. With several prices (time of day, members and others, a range), the **highest** is used, so a plan never promises less than the driver pays.

## 3. The estimate

- **Energy billed** = (leave % − arrive %) × usable kWh ÷ 0.92 for a fast charger, or ÷ 0.88 for AC. Chargers bill the energy they deliver, and some of it is lost before it reaches the cells.
- **Not counted:** session and idle fees, time-of-use (except the highest listed price), membership discounts the driver hasn't entered, and the charge the car leaves home with.
- **Shown where:**
  - the trip's "Charging cost" (Premium) and its breakdown;
  - each stop's detail;
  - each charger on the Chargers tab;
  - CarPlay's stop details.
