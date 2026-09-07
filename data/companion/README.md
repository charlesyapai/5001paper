# Companion paper tables (registry methods paper)

| File | Content | Finding |
|---|---|---|
| `raw/comparator_pull.csv` | 4,136 industry-sponsored halted drug trials, phase 1 or 2, started 2015 to 2025, with reason text, precision-medicine flag and overlap flag (fetched 2026-09-07) | F052 |
| `raw/comparator_labels_1.csv` to `_3.csv` | Fixed-schema labels of the 305 distinct comparator reason strings, assigned under the `02_classify_halts.py` system instruction | F052 |
| `comparator_matched.csv` | 378 comparators matched three per cell trial within phase and start-year strata, with the keyword flags | F052 |
| `comparator_labelled.csv` | The matched sample with its labels | F052 |
| `comparator_result.csv` | Business-cited share, cell against comparators, overall, by start year and by stratum, with Wilson intervals and z tests | F052 |
| `halt_human_coding_sheet.csv` | Blank 200-string sheet for human coding of the halt classification (`02_classify_halts.py --sample 200`) | OPEN_ITEMS 3 |

Regenerate: `research/findings/fetch_comparator_2026-09-07.py [--no-fetch]`, the classification of `comparator_strings_to_code.csv`
under the published instruction, then `build_comparator_2026-09-07.py`; `halt_kappa_2026-09-07.py` after the sheet is coded.
