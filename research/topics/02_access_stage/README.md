# 02 · Access stage: approval to reimbursement

## Scope
For each approved product and each system, the time from regulatory approval to the first
reimbursement decision, the decision outcome, the arrangement type, the price where public,
and the reasons the gatekeeper states.

## Questions
- How long does the access stage take, by product class and by system?
- What share of decisions are restricted, rejected or conditional, and on what stated grounds?
- Do managed-entry or outcomes-based arrangements shorten the stage or change the outcome?

## What we know
- European median time to national recommendation for advanced therapies was 9 to 17 months across eight countries, mostly with managed entry agreements (F012, provisional).
- Zynteglo was withdrawn from Germany in 2021 after price negotiations failed; it is the one documented price failure among the six retreat cases (F011).
- EU joint clinical assessments for advanced therapies began in January 2025 (seeded, verify).

- Gatekeeper documents state eligible patient counts per year and were reachable for NICE (PDFs via curl; pages return 403), G-BA (Beschluss and Tragende Gruende) and CDA-AMC; HAS pages abort fetches. Counts extracted for 41 products as a by-product of the eligible-population task (F034).
- NICE has no eligible count for BCMA CAR-T (appraisals for Abecma and Carvykti terminated; a Carvykti second-line appraisal is deferred to 2027) (F034).

- Decision table for six systems (F043): months from authorisation to the first positive funding step, England 9.4, Germany 9.8, France 5.2 with early access (23.4 without), Italy 17.4, Canada 21.0 to a pCPA letter of intent, Australia 3.7 from TGA registration to MSAC or PBAC support (funding start dates mostly unpublished). Germany's first resolutions are almost all "not quantifiable"; a third of England's first appraisals were terminated; half of Italy's use a managed-entry agreement. Tables: `data/access/decisions.csv`, `access_summary.csv`.

## Sources
NICE technology appraisals and highly specialised technologies guidance; G-BA resolutions and IQWiG dossiers; HAS transparency committee opinions and CEPS prices; AIFA decisions; CDA-AMC reimbursement reviews and pCPA outcomes; PBAC and MSAC outcomes; S07, S08, S09, S10, S23.

## Method
Per product per system: approval date, submission date where public, decision date, outcome, arrangement, price. Stated reasons classified under the schema in `research/methods/reason_classification.md`. See `research/methods/data_sources.md` for document locations.

## Tasks
1. Month 1: confirm each body's document archive is searchable by product and yields decision dates. **Done 2026-09-05: NICE (curl), G-BA, AIFA (Gazzetta Ufficiale and TrovaNormeFarmaco), CDA-AMC (via NCBI Bookshelf and CJHT; cda-amc.ca returns 403) and HAS (via the BDPM bulk extracts; has-sante.fr returns 403) all yield dates; PBAC and MSAC via pbs.gov.au PSDs and Wayback (msac.gov.au and tga.gov.au unreachable).**
2. Month 2: build `data/access/decisions.csv` for the cohort across six systems. **First pass done 2026-09-05 for six systems (F043); extension-indication approval dates and Australian funding start dates still to fill.**
3. Month 2: draft and pilot the reason schema on 30 documents; human-code a validation sample.
4. Month 2: compute approval-to-decision durations by class and system. **By system done 2026-09-05 (F043); by class next.**

## Open questions
- Whether to treat the United States as a system with a decision date (Medicare NCD or first major payer policy) or as uptake-only.
- Language handling for German, French and Italian documents: classify from the original with the model, validate a translated sample by hand.
