# Cohort and seed tables

Seed tables for the flagship's new layers. Every row carries a status. `seeded-from-memory` rows
were written on 4 September 2026 without a source and must be verified before use; the
`membership_source`, `source` and `verified_date` columns are where the verification is recorded.

| File | Rows | Status |
|---|---|---|
| `product_cohort.csv` | FDA-listed cellular and gene therapy products as of 18 August 2026, plus EU-only history | membership sourced from the FDA list; **approval dates verified from FDA and EMA pages on 4 September 2026** (`dates_verified`, `fda_source_url`, `eu_source_url`); 41 of 43 in-scope rows fully verified, Imlygic and Provenge provisional, seven tissue products out of scope; disagreements and gaps in `product_cohort_verification_report.csv` |
| `policy_events.csv` | Policy and market events for event studies | seeded |
| `countries_gatekeepers.csv` | Systems, gatekeepers, registries | seeded |
| `investment_events.csv` | Acquisitions, restructurings and retreats to code by manufacturing model | seeded; three 2025 to 2026 retreat rows verified with sources |
| `first_in_human.csv` | Earliest registered interventional trial per product (NCT id, start date, sponsor) and years to first approval | verified-from-data, ClinicalTrials.gov API 2026-09-04 (F032); 14 rows flagged |
| `diagnostic_codes.csv` | Test codes and coverage events | code descriptors verified 2026-09-05 (F031), coverage events still seeded |
| `raw/` | Agent batches for approval dates (batch_A to D), `s06_success_rates.csv` (F027), `projections_S16_S17.csv` (F033), `fih_candidates.csv` (every registry match behind F032) | |

Later extracted data goes under `data/access/`, `data/uptake/`, `data/investment/`,
`data/projection/` and `data/audit/` as specified in `research/methods/`.
