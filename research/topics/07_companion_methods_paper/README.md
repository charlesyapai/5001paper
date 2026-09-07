# 07 · Companion methods paper

## Scope
The v7 manuscript reframed around what the ClinicalTrials.gov stated-reason field can and
cannot show: usable for attributing discontinuation, blind to payment, censored on scientific
failure, boundary-sensitive, contradicted by a behavioural instrument, and, if the audit shows
it, uninformative for industry sponsors specifically. Molecular precision medicine is the case
study.

## Questions
- Is the industry-therapeutic elevation specific to molecular precision medicine or generic to industry early-phase trials?
- What share of "sponsor decision" halts have an externally disclosed scientific or competitive cause?
- How reliable is the machine classification against human coders?

## What we know
- The interaction survives restriction to interventional trials (F001).
- The headline cell is two-thirds CAR-T with a 2022+ spike; gene therapy rows are flat to falling (F002, F003).
- Nine of 95 industry-therapeutic business halts name a financial cause (F004).
- The imaging-AI subset cannot serve as the comparator (F005; D003).
- Published phase 1 oncology baselines put sponsor or strategic reasons at about half of terminations across all sponsors and about 60% implied for industry (F007, F008); industry terminations rarely cite accrual (F009).
- Business reasons and non-disclosure differ by sponsor type in an all-phase cancer analysis (F010, provisional).
- The manuscript header said v3 until 5 September 2026 (F018, fixed). AAV is uniquely the earliest genetic modality to reach pivotal trials; the N-of-1 subfamily's 2000 Phase 3 year is a query artefact (F038).

- The non-molecular comparator (F052): 378 industry drug halts matched on phase and start year give a business-cited share of 0.60 against the cell's 0.64 (p 0.34); by the pre-registered ten-point rule the elevation is generic to industry-sponsored early-phase drug trials. Tables: `data/companion/comparator_result.csv`.

## Sources
S01 to S05; the bundle's review record.

## Method
- Comparator: fresh pull of industry-sponsored Phase 1 and Phase 1/2 oncology small molecules and antibodies started 2015 or later, same regex re-filter and same classifier; stratified contrast against the industry-therapeutic cell. Decision rule: within ten points means the specificity claim is dead.
- Disclosure audit: for each of the 95 industry-therapeutic business halts, search press releases, 8-K and 10-K filings and earnings transcripts within twelve months of the halt; code the disclosed cause under the existing 11-label schema; report the share with a scientific or competitive cause. Protocol in `research/methods/reason_classification.md`.
- Kappa: `02_classify_halts.py --sample 200`, two human coders, Cohen's kappa by label.

## Tasks
1. Fix the two v7 defects in OPEN_ITEMS item 1 and the v3 header (F018). **Done 2026-09-05 (F038); v7 revision note added to the manuscript.**
2. Run the comparator pull. **Done 2026-09-07 (F052): specificity claim dead by the pre-registered rule.**
3. Run the disclosure audit and the kappa. **Kappa sheet and script prepared 2026-09-07 (`data/companion/halt_human_coding_sheet.csv`, `halt_kappa_2026-09-07.py`); coding and the disclosure audit outstanding.**
4. Rewrite the abstract and title around the instrument.

## Open questions
- Whether to publish the companion before or alongside the flagship. Proposal: preprint it first; it is the methodological foundation the flagship's classification step cites.
