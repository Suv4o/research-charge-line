# Australian EV Catalog: Cars, Figures and Estimates

**Date:** 2026-10-22
**For:** Charge Line's car list (`app/ChargeLine/Resources/Vehicles.json`)
**Question:** Which electric cars are sold in Australia, and what does the planner need for each?

## Bottom line

- **The catalog went from 9 to 226 variants across 47 makes.** It covers every passenger EV sold new in Australia since 2019 that I could find, plus older cars still common on the road (pre-2024 Teslas, Leaf, Kona, ZS EV, Ioniq Electric).
- **Every entry names its sources** in its `source` field. "est." marks figures the maker doesn't publish or that I couldn't confirm.
- **Figures come from makers and launch coverage.** That means maker spec sheets and pages (Volvo, Hyundai, Skoda, Audi, Polestar Australia) and news reporting of maker claims (The Driven, WhichCar, GoAuto, CarExpert and CarAdvice news, Chasing Cars, Cars24, RACV, RACQ, myNRMA, EV Central, AEVA fact sheets). The US EPA Test Car Lists 2019–2026 supplied road loads.
- **Two spec databases were not used,** because their terms forbid automated collection or reuse:
  - EVDB Australia (evdbau.com): "Scraping or Automated Data Harvesting is prohibited", and use needs permission.
  - CarExpert's spec pages: "spidering, screen scraping, database scraping" are banned.
  - Before reading their terms I had fetched one EVDB page and about 16 CarExpert spec pages. None of those figures went in unless news coverage reported the same number.
  - Zecar's public listing pages were used only to enumerate models and as a labelled fallback ("Zecar listing").
- **Drivers can now add a missing car themselves and edit their range** (app commit cf6ee9c), so gaps and errors here can be corrected without waiting for an update.

## 1. What each entry holds

- **Published figures:**
  - make, model, variant, first and last model year, shape;
  - usable kWh, WLTP range, peak DC kW, AC kW, plugs;
  - a fast-charge claim (from–to % in minutes, or Tesla's km in 15 minutes);
  - optionally EPA road load or a kerb weight.
- **Usable kWh:** the maker's net figure where published (VW Group, BMW, Mercedes, Polestar, Volvo, Mini, some Chinese makers). Otherwise the quoted figure × 0.95, marked est. BYD's Blade figures are used as quoted (they track usable). Tesla doesn't publish usable kWh, so all Tesla figures are estimates.
- **WLTP:** the Australian WLTP claim. Where only a European WLTP figure was found, the source says so.
  - Several listings mix in NEDC or ADR 81/02 figures. Two were clearly not WLTP and were replaced with Audi's European WLTP:
    - e-tron 55: 369 → 436 km;
    - e-tron GT: 433 → 472 km.
- **Charge claim:** the maker's 10–80% (or 0/5/15/20/30–80%) time. 22 of the 226 entries have none, and the planner then assumes the car averages 70% of its peak.

## 2. What the app works out (VehicleCatalog.swift)

- **Mixed Wh/km** = usable kWh ÷ WLTP range (unchanged from the 9-car catalog).
- **Highway Wh/km (110 km/h):**
  - With EPA road load: the physics at 110 km/h. That applies to 69 entries, matched by model year, power, drive and wheel size.
  - Without it: mixed × a ratio for the car's shape (§3).
- **Test mass:** EPA equivalent test weight if available, else kerb + 136 kg. Without a kerb weight, it's estimated from the battery (§3).

## 3. Constants derived from the catalog itself

| Constant | Value | How |
| --- | --- | --- |
| Highway ÷ mixed, car | 1.27 | Median over 25 EPA cars (1.10–1.44) |
| Highway ÷ mixed, SUV | 1.29 | Median over 44 EPA SUVs (1.05–1.54) |
| Highway ÷ mixed, people mover / ute | 1.42 / 1.45 | No EPA data; SUV plus about 10% / 12% (est.) |
| Kerb weight, car | 935 + 14.5 × kWh | Least-squares fit of (EPA test weight − 136 kg) against usable kWh |
| Kerb weight, SUV | 850 + 16.5 × kWh | Same fit. Runs about 5% heavy for Chinese-built cars (Atto 3 1845 vs 1750 published) |
| Rolling coefficient A/(m·g) | 0.0070 | Median over the 69 EPA entries (was 0.0073 over 7) |

**What the ratio spread shows.** Boxy SUVs (EX40 1.54, SQ6 1.49) lose much more at highway speed than WLTP suggests, and slippery sedans (i4 M50, Model 3 Performance about 1.1–1.14) lose less. A single ratio per shape is the main error source for cars without EPA data. The learned factor from the driver's trips, and the editable range, cover it.

**One override: the Model Y L.** Its WLTP figure (681 km on about 84 kWh) would make it more efficient than the Model Y Long Range, so it uses the Model Y Long Range's EPA road load at its own weight class.

## 4. Coverage

- **Tesla:**
  - Model 3: Standard Range Plus 2019–21, RWD 2021–23, Long Range AWD 2019–23 and 2024–25, Performance 2019–23 and 2024 on, Premium Long Range RWD 2026.
  - Model Y: RWD, Long Range and Performance for 2022–25 and for 2025 on, plus the Model Y L.
- **BYD:**
  - Atto 1, Atto 2;
  - Atto 3: Standard and Extended 2022–26, and the Atto 3 Evo Dynamic and Premium;
  - Dolphin (2), Seal (3), Sealion 7 (2).
  - Denza D9: FWD and AWD.
- **MG and IM:**
  - MG4 (6 variants), MG4 Urban (2), ZS EV (3 generations), MGS5 (2), MGS6 (2), Cyberster (2);
  - IM5 and IM6 (3 each).
- **Kia:** EV3 (3), EV4 (2), EV5 (4), EV6 (5, both batteries), EV9 (2), Niro EV, e-Niro.
- **Hyundai and Genesis:**
  - Hyundai: Ioniq 5 (4) and Ioniq 5 N, Ioniq 6 (3), Ioniq 9, Kona Electric (3), Ioniq Electric, Inster (2), Elexio.
  - Genesis: GV60 (2), Electrified GV70, Electrified G80.
- **Other Chinese makes:**
  - Geely: EX2 (2), EX5 (2).
  - Zeekr: X (4), 7X (3), 001.
  - GWM: Ora (4), Ora 5.
  - Leapmotor: C10, B10 (2).
  - Xpeng: G6 (5).
  - Deepal S07, Omoda E5, Jaecoo J5 EV.
  - Smart: #1 (2), #3 (2), #5 (2).
  - KGM: Torres EVX, Musso EV.
  - GAC Aion V, Skywell BE11.
  - LDV: Mifa 9, eT60.
- **European makes:**
  - Polestar: 2 (5), 3, 4 (2).
  - Volvo: EX30 (2), XC40 and C40 Recharge, EX40 (2), EC40, EX90.
  - BMW: i4 (2), i5 (2), i7, iX (2), iX1, iX2, iX3 (2 generations).
  - Mercedes-Benz: EQA (2), EQB, EQC, EQE, EQS, CLA (2).
  - Audi: Q4 (2), Q6, SQ6, Q8 e-tron, e-tron, e-tron GT.
  - Porsche: Taycan (2), Macan Electric.
  - Volkswagen: ID.4 (2), ID.5 (2), ID. Buzz.
  - Skoda: Enyaq (2), Elroq.
  - Cupra: Born, Tavascan (2).
  - Renault: Megane, Scenic (2), Zoe.
  - Peugeot: e-2008, e-208.
  - Jeep Avenger, Alfa Romeo Junior, Fiat 500e, Abarth 500e.
  - Mini: Cooper SE (2 generations), Aceman, Countryman.
  - Jaguar I-Pace, Lotus Eletre.
- **Japanese and US makes:**
  - Nissan: Leaf (2, CHAdeMO), Ariya.
  - Toyota: bZ4X (4), HiLux BEV.
  - Subaru Solterra.
  - Lexus: RZ (3), UX 300e (CHAdeMO).
  - Mazda: MX-30, 6e, CX-6e (2).
  - Suzuki e Vitara (2).
  - Ford Mustang Mach-E (3).
  - Cadillac: Lyriq, Optiq.

**Left out on purpose:**
- **Commercial vans:** eDeliver, e-Transit, eSprinter, e-Transporter, Kangoo, e-Partner, Master, Supervan, Transit City, Staria Load, PV5 Cargo.
- **Exotics:** Rolls-Royce, Ferrari, Maserati, G580.
- **Announced but not confirmed for Australia:** new Leaf, Kia PV5 Passenger, MG U9, Xpeng X9/G9/L03, Deepal E07, Leapmotor B05, Volvo ES90, iX 2025 facelift, Ioniq 6 facelift, Cayenne Electric, Cadillac Vistiq, BMW i3.

Drivers can add any of these by hand.

## 5. Least certain entries

Check these first if a driver reports a plan that's off:

- **All Teslas' usable kWh** and most Tesla 10–80% times (est.). The 2026 Model Y Long Range may now be rated 600 km WLTP (the catalog keeps the 551 km launch figure).
- **Kia EV5 peak DC** (est. 140 kW) and its 10–80% time, which sources give as 27 or 36–38 min.
- **Audi Q4 e-tron 45 WLTP** (est. 530 km) and the Q6 e-tron's (Zecar 625 km).
- **Porsche Taycan 2025** (range est. 600 km; up to 678 km for the best variant).
- **Zeekr 001** (European WLTP and usable; Australian DC not found).
- **Cadillac Optiq:** sources disagree (75, 79 or 85 kWh; 110 or 150 kW).
- **Ioniq 6 Standard Range WLTP** (429 km est.).
- **Mazda 6e peak DC:** taken from the CX-6e, because 165 kW can't meet its 30–80% claim.

## Sources

- **EPA:** Test Car List data files, model years 2019–2026 ([EPA](https://www.epa.gov/compliance-and-fuel-economy-data/data-cars-used-testing-fuel-economy); 2025 and 2026 files dated 2026-01-21).
- **Maker pages:**
  - [polestar.com/au Polestar 2 (2023)](https://www.polestar.com/au/polestar-2-2023/standard-range-single-motor/)
  - [volvocars.com/au EX40 specifications](https://www.volvocars.com/au/cars/ex40-electric/specifications/)
  - [Hyundai Elexio specification sheet](https://www.hyundai.com/content/dam/hyundai/au/en/models/elexio/docs/Hyundai_ELEXIO_Specification_Sheet.pdf)
  - [skoda.com.au FAQ](https://www.skoda.com.au/about/faqs)
  - [audi.com.au Q8 e-tron](https://www.audi.com.au/au/web/en/models/q8/q8-e-tron.html)
  - [MG Australia MG4 range](https://mgmotor.com.au/mg4-range)
  - [Xpeng G6 configurator](https://store.xpeng.com/au/configurator/NEW_G6R)
- **Launch coverage and reviews:**
  - The Driven, WhichCar, GoAuto, CarExpert and CarAdvice news, Chasing Cars, Cars24, RACV, RACQ, myNRMA, EV Central, carsales editorial, Canberra Times / ACM, evee, Man of Many, The Beep, AEVA fact sheets.
  - Each entry's `source` field names the ones used.
- **Model enumeration:** [Zecar EV listing](https://zecar.com/electric-vehicles) (public pages).
