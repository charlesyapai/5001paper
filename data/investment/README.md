# Investment layer tables

Built 5 September 2026 by `research/findings/build_investment_events_2026-09-05.py`.

| File | Content | Finding |
|---|---|---|
| `raw/events_by_product.csv` | Agent table: 102 dated sponsor events per cohort product (acquisition, asset sale or licence, discontinuation or withdrawal, shipment pause or restriction, restructuring, sponsor exit, going private) with verbatim reasons, amounts where stated, per-row URL and status; 14 none-found rows | F042 |
| `events.csv` | Unified event rows from the agent table, the seed list (`data/cohort/investment_events.csv`), the cohort's EU withdrawals (F020) and disclosure statements; months from first approval; `is_retreat`, `after_approval`, `is_prv_sale`, `usable` flags | F042 |
| `events_summary.csv` | One row per cohort product: usable events by type, first retreat after approval and its lag, withdrawn anywhere, sponsor acquired or asset sold, product sold or licensed after approval | F042 |

Conventions: rows with status provisional-from-snippet or seeded-from-memory stay in `events.csv` and are excluded from
the summary; a class-wide safety labelling change and a priority-review-voucher sale are not retreats; asset sales and
licences are reported separately from retreats.
