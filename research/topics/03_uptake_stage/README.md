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

## Sources
Company 10-K, 10-Q, annual reports and earnings releases; disclosed patient counts; S11, S12, S13, S24 for CAR-T counts; FDA and EMA safety communications for restriction events.

## Method
`research/methods/revenue_to_patients.md`, `diffusion_fits.md`, `time_to_milestone.md`, `cross_country_design.md`.

## Tasks
1. Week 1: pilot revenue-to-patients on Zolgensma, Yescarta, Hemgenix, Casgevy and Luxturna, and calibrate against disclosed counts.
2. Week 1: download the last three EBMT activity-survey reports and the latest CIBMTR summary; confirm country-level CAR-T counts.
3. Month 1: eligible-population estimates with ranges for each product, from label, epidemiology and company guidance; record every assumption in the table.
4. Month 2: full quarterly series for the cohort; `data/uptake/patients_quarterly.csv`.
5. Month 3: country-level CAR-T table; fits and milestone times.

## Open questions
- Net versus list price: how much of the sales-derived count moves under plausible net-price assumptions, and whether disclosed counts pin it down.
- Whether per-capita or per-eligible denominators change the cross-country ranking (gate for month 3).
