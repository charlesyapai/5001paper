# 03 · Uptake stage: reimbursement to patients treated

## Scope
Patients treated per quarter for every approved product with public data, normalised to the
eligible population; CAR-T infusions by country; withdrawal, restriction and discontinuation
events after approval.

## Questions
- How long from approval, and from reimbursement, to a quarter and to half of the eligible population?
- Where does uptake plateau, and how far below eligibility?
- Does the same product diffuse at different speeds in different systems?
- What share of approved products were withdrawn, restricted or discontinued, and after how long?

## What we know
- The FDA list dated 18 August 2026 has 53 entries; cohort membership is now sourced, dates are not (F016).
- Product-level uptake notes exist in consultancy reviews: fewer than 20 Hemgenix patients through August 2024, tens of Lyfgenia and Zynteglo patients, near-complete Luxturna uptake (F014, provisional).
- EBMT reported 4,888 CAR-T patients treated in Europe in 2023, up 52.5% (F013, provisional).
- Post-approval events already documented: Zynteglo and Skysona EU withdrawals, Beqvez discontinuation, Roctavian restricted access, Hemgenix slow rollout (F011).

- Quarterly revenue series are complete from filings for Zolgensma, Yescarta, Tecartus and Casgevy, partial for Luxturna and Hemgenix (F023). Revenue at list recovers 63 to 86 percent of disclosed patients; class factor 0.76; month-1 gate passed (F024). Disclosed counts are heterogeneous and mostly floors (F025). Hemgenix stockout March to April 2026 (F026).

- CSL primary statements confirm the Hemgenix stockout (17 March 2026) and the more-than-100 commercial patients (24 July 2026); FY2026 Hemgenix sales USD 118m (F028). Tecartus launch price confirmed at USD 373,000 with later WAC to 462,000 (F029).
- US CAR-T net price equals list price: Medicare ASP payment limits divided by 1.06 match the WAC for Yescarta and Tecartus (median ratio 1.00); no Medicare price exists for 18 gene therapies (F030; D011).
- Eligible-population ranges exist for 41 products (40 with a US range), built from 481 source rows with 51 documented overrides (F034; D010).
- Quarterly revenue series cover 27 products; median first approval to first revenue 4.7 months, with the slow launches all one-time gene therapies (Zynteglo, Skysona, Lenmeldy, Roctavian, Hemgenix, Casgevy, Lyfgenia) (F035).
- CAR-T patients by country and year are published by EBMT, CIBMTR and national registries; Europe 6,082 and US 5,266 in 2024 (F036).
- First H1 reading: Yescarta and Kymriah have not reached half of the US eligible flow after 8.7 years, longer than their clinical stages; Luxturna has reached 8 to 32% of its US prevalent pool after 8.5 years; other products are not yet decidable (F037).
- Label-dated pools for eight products (D012, F039): Carvykti's cumulative penetration range narrows from 7 to 89% to 10 to 27% once the pool follows the label (fifth line to April 2024, second line after); Elevidys moves to the ambulatory 4-and-older pool (6 to 23%); Breyanzi joins Yescarta and Kymriah in not reaching half of the eligible flow within a follow-up longer than its clinical stage. Tables: `data/uptake/label_events.csv`, `pool_quarterly.csv`.
- Cross-country CAR-T table with both denominators (F041): 2024 patients per million Germany 17.2, France 15.9, US 15.5, Spain 15.3, Italy 12.8, UK 8.2; per 100 eligible France 50 to 81, US 13 to 84, Germany 16 to 70, UK 14 to 62; the per-eligible ranking cannot yet separate the US from Germany. Table: `data/uptake/cart_by_country.csv`.
- Product-level net-price variant (US CAR-T at ASP or WAC in force, ex-US at the class factor) recovers 81 to 90% of Kite's disclosed cumulative floors against 103 to 110% for the class-factor series; the class factor stays primary (F040; D011 confirmed).

## Sources
Company 10-K, 10-Q, annual reports and earnings releases; disclosed patient counts; S11, S12, S13, S24 for CAR-T counts; FDA and EMA safety communications for restriction events.

## Method
`research/methods/revenue_to_patients.md`, `diffusion_fits.md`, `time_to_milestone.md`, `cross_country_design.md`.

## Tasks
1. Week 1: pilot revenue-to-patients on Zolgensma, Yescarta, Hemgenix, Casgevy and Luxturna, and calibrate against disclosed counts. **Done 2026-09-04 (F023 to F025); gate passed.**
2. Week 1: download the last three EBMT activity-survey reports and the latest CIBMTR summary; confirm country-level CAR-T counts. **Done 2026-09-05 (F036); raw table `data/uptake/raw/cart_registry_counts.csv`.**
3. Month 1: eligible-population estimates with ranges for each product, from label, epidemiology and company guidance; record every assumption in the table. **First pass done 2026-09-05 (F034); label expansions done 2026-09-05 (F039, D012); Japan, Italy and Spain remain, and US flows for Breyanzi CLL, FL, MCL and Tecartus MCL.**
4. Month 2: full quarterly series for the cohort; `data/uptake/patients_quarterly.csv`. **First pass done 2026-09-05 for 27 products (F035).**
5. Month 3: country-level CAR-T table; fits and milestone times. **Country table first pass done 2026-09-05 (F041); fits and per-eligible ranking wait on Italy, Spain and Japan eligible flows.**

## Open questions
- Net versus list price: answered in first pass by F040 (the product-level variant moves counts down 17 to 28% and falls below the disclosed floors); what remains is an ex-US price series.
- Whether per-capita or per-eligible denominators change the cross-country ranking (gate for month 3). First look (F041): same top three on four countries, but the US eligible range is too wide to decide; needs Italy and Spain eligible flows and a narrower US myeloma flow.
