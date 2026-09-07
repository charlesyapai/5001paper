"""Cohen's kappa between the keyword coding (F045) and a human coder on the stratified validation sample (topic 02 task 3).

The sample (data/access/reason_validation_sample.csv, 10 rows per system drawn 2026-09-07 from stated_reasons.csv rows with
verbatim text) carries the verbatim committee text and blank human_<category> columns; the coder fills each with yes or no
(1/0, true/false accepted) without seeing the machine codes, which sit in reason_validation_key.csv. Run after coding:
    python3 reason_kappa_2026-09-07.py
Writes data/access/reason_kappa.csv: per category, n coded, agreement, Cohen's kappa, and the pooled kappa across categories.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "data/access"
CATS = ["uncertainty-durability", "cost-effectiveness", "budget-impact", "comparator-or-evidence", "price", "population-or-restriction", "capacity-or-delivery", "none stated"]
TRUE = {"1", "yes", "y", "true", "t", "x"}
h = pd.read_csv(A / "reason_validation_sample.csv", dtype=str).fillna("")
k = pd.read_csv(A / "reason_validation_key.csv", dtype=str).fillna("").set_index("sample_id")


def kappa(a, b):
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    po = float((a == b).mean())
    pe = float(a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean()))
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


rows, allh, allm = [], [], []
for c in CATS:
    coded = h[h["human_" + c].str.strip() != ""]
    if coded.empty:
        rows.append({"category": c, "n_coded": 0, "agreement": "", "kappa": "", "note": "no human codes yet"}); continue
    hv = coded["human_" + c].str.strip().str.lower().isin(TRUE).values
    mv = k.loc[coded["sample_id"], c].str.lower().eq("true").values
    po, kp = kappa(hv, mv); allh += list(hv); allm += list(mv)
    rows.append({"category": c, "n_coded": len(coded), "agreement": round(po, 3), "kappa": round(kp, 3), "human_positive": int(hv.sum()), "machine_positive": int(mv.sum())})
if allh:
    po, kp = kappa(allh, allm); rows.append({"category": "pooled over categories", "n_coded": len(allh), "agreement": round(po, 3), "kappa": round(kp, 3)})
out = pd.DataFrame(rows); out.to_csv(A / "reason_kappa.csv", index=False); print(out.to_string(index=False))
