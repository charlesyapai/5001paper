"""Cohen's kappa between the machine labels of the halt classification and a human coder (OPEN_ITEMS item 3).

The blank sheet data/companion/halt_human_coding_sheet.csv (200 distinct reason strings drawn by code/02_classify_halts.py
--sample 200, seed 0) is coded by hand in its human_category column with one of the labels listed in categories_allowed. This
script joins the machine label for the same string from data/primary/halted_trials_blockers.csv and reports agreement, kappa
over all labels, and kappa for the binary business-versus-other split that the paper's headline uses.
Run from research/findings:  python3 halt_kappa_2026-09-07.py   ->  data/companion/halt_kappa.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
C = ROOT / "data/companion"
BIZ = "Funding, business or strategic decision"
sheet = pd.read_csv(C / "halt_human_coding_sheet.csv", dtype=str).fillna("")
coded = sheet[sheet["human_category"].str.strip() != ""].copy()
if coded.empty:
    print("no human codes yet"); pd.DataFrame([{"n_coded": 0}]).to_csv(C / "halt_kappa.csv", index=False); raise SystemExit
blk = pd.read_csv(ROOT / "data/primary/halted_trials_blockers.csv", low_memory=False)
blk["why_s"] = blk["why"].astype(str).str.strip()
machine = blk.drop_duplicates("why_s").set_index("why_s")["blocker"].to_dict()
coded["machine"] = coded["why"].astype(str).str.strip().map(machine)
coded = coded[coded["machine"].notna()]
h, m = coded["human_category"].str.strip(), coded["machine"]


def kappa(a, b):
    cats = sorted(set(a) | set(b)); a = pd.Categorical(a, cats); b = pd.Categorical(b, cats)
    ct = pd.crosstab(a, b).reindex(index=cats, columns=cats, fill_value=0).values.astype(float); n = ct.sum()
    po = np.trace(ct) / n; pe = (ct.sum(0) * ct.sum(1)).sum() / n / n
    return po, (po - pe) / (1 - pe) if pe < 1 else np.nan


po, k = kappa(h, m); pob, kb = kappa(h == BIZ, m == BIZ)
out = pd.DataFrame([{"n_coded": len(coded), "agreement_all_labels": round(po, 3), "kappa_all_labels": round(k, 3), "agreement_business_vs_other": round(pob, 3), "kappa_business_vs_other": round(kb, 3)}])
out.to_csv(C / "halt_kappa.csv", index=False); print(out.to_string(index=False))
print(pd.crosstab(h, m).to_string())
