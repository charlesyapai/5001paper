# 06 · Diagnostics: coverage and uptake

## Scope
Molecular diagnostics in the taxonomy: comprehensive genomic profiling, liquid biopsy, molecular
residual disease, pharmacogenomics, exome and genome sequencing. Coverage decisions, Medicare
volumes after coverage, and the interventional evidence base at the time of coverage.

## Questions
- How long from first interventional utility trial to a coverage decision?
- How fast does uptake rise after coverage, compared with therapies after reimbursement?
- Does the assay-as-intervention trial count predict coverage timing?

## What we know
- Assay-as-intervention counts per subfamily are in `data/derived/platform_lookup.csv` (`tech_as_intervention`, `ph3plus`): liquid biopsy 278 with 23 at Phase 3 or later; affinity proteomics 1 and 0 (referee pitch section 4).
- Diagnostic programs halt for recruitment and feasibility rather than business reasons (manuscript section 2.1; OR 2.69).

- The Part B National Summary Data File gives annual allowed services by code from 2000 (2023 missing); 2024 volumes pulled for every seed code. 81228 and 81229 were wrong (cytogenomic microarray); VKORC1 is 81355 (F031).

## Sources
S25 for Medicare volumes; CMS national coverage determinations and MolDX local coverage determinations for coverage dates; `data/cohort/diagnostic_codes.csv` for the code list.

## Method
Annual volumes by code from the public use files; coverage date from the determination; time from coverage to volume milestones; comparison with therapy uptake curves on the same normalised axis where an eligible population can be defined.

## Tasks
1. Week 1: pull one year of Part B volumes for the seed codes and confirm the series exists. **Done 2026-09-05 (F031).**
2. Month 1: verify every code assignment and coverage date in `diagnostic_codes.csv`. **Codes verified 2026-09-05 (F031); coverage dates still seeded.**
3. Month 3: full series 2015 to latest; figure 5.

## Open questions
- Eligible population for a diagnostic is less well defined than for a therapy. Proposal: use annual incident cases in the covered indication as the denominator, with a range.
