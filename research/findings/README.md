# Findings ledger

`findings_ledger.csv` is the single list of established facts. Columns:

| Column | Content |
|---|---|
| `id` | F001, F002, ... never reused |
| `date` | date established, ISO |
| `topic` | topic folder name |
| `statement` | the finding, with its numbers |
| `evidence` | file and script or command that regenerates it, or the document read |
| `source` | bibliography id or bundle path |
| `status` | one of the statuses in `research/README.md` |
| `confidence` | high, medium, low, with a reason if not high |
| `used_in` | where the finding is used |
| `notes` | anything a reader needs before reusing it |

`recompute_2026-09-04.py` regenerates F001 to F006 from the bundle's primary tables. Run it
from this folder:

```bash
python3 recompute_2026-09-04.py
```
