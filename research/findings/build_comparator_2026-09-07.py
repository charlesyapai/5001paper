"""Non-molecular comparator result for the companion paper (OPEN_ITEMS item 2; D003).

Joins the fixed-schema labels of the comparator's reason strings (data/companion/raw/comparator_labels_*.csv, classified under the
same system instruction and label set as code/02_classify_halts.py) to the matched sample (comparator_matched.csv) and compares
the business-cited share with the 144 industry-therapeutic halts of the study, overall, by stratum and by start-year bin, with
Wilson intervals and a two-proportion z test. Also writes the human-coding sheet status.

Outputs: data/companion/comparator_result.csv (one row per comparison), comparator_labelled.csv (the matched sample with labels)
Run from research/findings:  python3 build_comparator_2026-09-07.py
"""
import glob
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
C = ROOT / "data/companion"
BIZ = "Funding, business or strategic decision"
ROLL = "Administrative rollover or transfer (not a failure)"

labs = pd.concat([pd.read_csv(f, dtype=str) for f in sorted(glob.glob(str(C / "raw/comparator_labels_*.csv")))], ignore_index=True)
labs["why"] = labs["why"].astype(str).str.strip()
lab = labs.drop_duplicates("why").set_index("why")["category"].to_dict()
m = pd.read_csv(C / "comparator_matched.csv", dtype=str).fillna("")
m["why_s"] = m["why"].astype(str).str.strip()
m["blocker"] = [lab.get(w, "No reason stated" if not w else "Unclear") for w in m["why_s"]]
m["biz"] = m["blocker"] == BIZ
m.to_csv(C / "comparator_labelled.csv", index=False)
halted = pd.read_csv(ROOT / "data/primary/halted_trials_dedup.csv", low_memory=False)
cell = halted[(halted["sponsor_class"] == "INDUSTRY") & (halted["modality"] == "Therapeutic")].copy()
cell["biz"] = cell["blocker"] == BIZ


def bucket(ph):
    ph = str(ph)
    if ph in ("", "nan", "NA"): return "phase missing"
    if ph in ("EARLY_PHASE1", "PHASE1"): return "phase 1"
    if ph == "PHASE1|PHASE2": return "phase 1/2"
    return "phase 2 or later"


def ybin(y):
    y = float(y) if pd.notna(y) and str(y) not in ("", "nan") else np.nan
    if np.isnan(y): return "year missing"
    return "2015-2018" if y <= 2018 else ("2019-2021" if y <= 2021 else "2022-2025")


cell["stratum"] = cell["phase"].map(bucket) + " x " + cell["start_year"].map(ybin)
cell["ybin"] = cell["start_year"].map(ybin); m["ybin"] = pd.to_numeric(m["start_year"], errors="coerce").map(ybin)
matched_strata = set(m["stratum"])
cellm = cell[cell["stratum"].isin(matched_strata)]   # the cell trials with a comparator stratum (phase-missing trials have none)


def wilson(k, n):
    if n == 0: return (np.nan, np.nan)
    p = k / n; z = 1.96; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def ztest(k1, n1, k2, n2):
    p = (k1 + k2) / (n1 + n2); se = np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (k1 / n1 - k2 / n2) / se if se > 0 else np.nan
    return z, 2 * (1 - norm.cdf(abs(z))) if np.isfinite(z) else np.nan


rows = []
def add(label, a, b, exclude_rollover=False):
    if exclude_rollover:
        a = a[a["blocker"] != ROLL]; b = b[b["blocker"] != ROLL]
    k1, n1, k2, n2 = int(a["biz"].sum()), len(a), int(b["biz"].sum()), len(b)
    lo1, hi1 = wilson(k1, n1); lo2, hi2 = wilson(k2, n2); z, p = ztest(k1, n1, k2, n2) if n1 and n2 else (np.nan, np.nan)
    rows.append({"comparison": label, "cell_business": k1, "cell_n": n1, "cell_share": round(k1 / n1, 3) if n1 else "", "cell_ci": f"{lo1:.2f} to {hi1:.2f}" if n1 else "",
                 "comparator_business": k2, "comparator_n": n2, "comparator_share": round(k2 / n2, 3) if n2 else "", "comparator_ci": f"{lo2:.2f} to {hi2:.2f}" if n2 else "",
                 "difference": round(k1 / n1 - k2 / n2, 3) if n1 and n2 else "", "z": round(z, 2) if np.isfinite(z) else "", "p_two_sided": round(p, 4) if np.isfinite(p) else ""})


add("all matched strata (business share of halts)", cellm, m)
add("all matched strata, rollover transfers excluded", cellm, m, exclude_rollover=True)
add("full cell of 144 against the comparator", cell, m)
for yb in ["2015-2018", "2019-2021", "2022-2025"]:
    add(f"start {yb}", cellm[cellm["ybin"] == yb], m[m["ybin"] == yb])
for st in sorted(matched_strata):
    add(f"stratum {st}", cellm[cellm["stratum"] == st], m[m["stratum"] == st])
# CAR-T only, the cell's dominant subfamily
cart = cellm[cellm["subfamily"].str.contains("CAR-T")]
add("CAR-T trials of the cell against all comparators", cart, m)
res = pd.DataFrame(rows); res.to_csv(C / "comparator_result.csv", index=False)
pd.set_option("display.width", 250)
print("label distribution, comparator:"); print(m["blocker"].value_counts().to_string())
print("\nlabel distribution, cell (matched strata):"); print(cellm["blocker"].value_counts().to_string())
print("\n" + res.to_string(index=False))
