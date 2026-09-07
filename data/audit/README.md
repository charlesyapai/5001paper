# Provenance audit

| File | Content | Finding |
|---|---|---|
| `audit_sample_2026-09-07.csv` | 5 percent random sample of verified rows per raw table (171 rows, seed 20260907), four batches | F053 |
| `raw/audit_1.csv` to `audit_4.csv` | One agent per batch: reachability, values checked, verdict, note | F053 |
| `audit_results.csv` | The sample joined to the verdicts | F053 |
| `audit_summary.csv` | Counts and discrepancy rates per layer and per table | F053 |

Result: 167 agree, 3 minor discrepancies, 0 disagree, 1 not verifiable. Regenerate the merge with `research/findings/build_audit_2026-09-07.py`.
