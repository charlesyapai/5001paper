# Cohort and seed tables

Seed tables for the flagship's new layers. Every row carries a status. `seeded-from-memory` rows
were written on 4 September 2026 without a source and must be verified before use; the
`membership_source`, `source` and `verified_date` columns are where the verification is recorded.

| File | Rows | Status |
|---|---|---|
| `product_cohort.csv` | FDA-listed cellular and gene therapy products as of 18 August 2026, plus EU-only history | membership sourced from the FDA list; approval years and events seeded, unverified |
| `policy_events.csv` | Policy and market events for event studies | seeded |
| `countries_gatekeepers.csv` | Systems, gatekeepers, registries | seeded |
| `diagnostic_codes.csv` | Test codes and coverage events for the diagnostics layer | seeded |
| `investment_events.csv` | Acquisitions, restructurings and retreats to code by manufacturing model | seeded |

Later extracted data goes under `data/access/`, `data/uptake/`, `data/investment/`,
`data/projection/` and `data/audit/` as specified in `research/methods/`.
