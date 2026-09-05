"""Curated label events for the label-dated pools (D012).

Input : data/uptake/raw/label_events.csv (agent table: every FDA and EC label event with verbatim indication text)
Output: data/uptake/label_events.csv, the rows build_milestones_2026-09-05.py applies: product_key, geography (US or EU),
        event_date, action (add or remove), indication_key (aliases separated by semicolons), replaces (narrower keys the
        new population supersedes), source_url, status, notes.

Rules, all explicit below. REPLACES: an earlier line of therapy supersedes later lines of the same disease (a second-line
label covers the patients who would have reached fifth line); a wider age or ambulatory range supersedes the narrower one.
ALIAS: keys that name the same population in another source vocabulary and family (the annual inflow key DMD_4plus is the
births-reaching-four flow into any Duchenne label from age four). SKIP: label changes that do not move the eligible
population (a limitation-of-use removal for primary CNS lymphoma; an age-wording clarification) and the Elevidys EU refusal
(no label). Casgevy's 2026 paediatric extension is keyed SCD_TDT_2to11 because the only count is Vertex's combined figure.

Run from research/findings:  python3 curate_label_events_2026-09-05.py
"""
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
U = ROOT / "data/uptake"
REPLACES = {"MM_2L": "MM_3L;MM_4L;MM_5L", "MM_3L": "MM_4L;MM_5L", "MM_4L": "MM_5L", "LBCL_2L": "LBCL_3L",
            "DMD_4plus_amb": "DMD_4to5_amb"}
ALIAS = {"DMD_4to5_amb": "DMD_4to5_amb;DMD_4plus", "DMD_4plus_amb": "DMD_4plus_amb;DMD_4plus",
         "SCD_VOC_2to11": "SCD_TDT_2to11", "TDT_2to11": "SCD_TDT_2to11"}
SKIP = {"LBCL_PCNSL_LoU_removed": "limitation of use removed; no change to the eligible population",
        "DMD_3to7_amb": "EU refusal: no label"}
raw = pd.read_csv(U / "raw/label_events.csv", dtype=str).fillna("")
rows = []
for _, r in raw.iterrows():
    k = r["indication_key"]
    note = r["notes"][:160]
    if k in SKIP or r["event_type"] in ("refusal", "withdrawal"):
        continue
    if r["product"] == "Kymriah" and r["geography"] == "EU" and r["event_date"] == "2021-03-04":
        continue   # age-wording clarification, same population
    action = "remove" if r["event_type"] == "restriction" else "add"
    rows.append({"product_key": re.split(r"[\s/(]", r["product"].strip())[0].lower(), "geography": r["geography"], "event_date": r["event_date"],
                 "action": action, "indication_key": ALIAS.get(k, k), "replaces": REPLACES.get(k, "") if action == "add" else "",
                 "event_type_raw": r["event_type"], "pathway": r["pathway"], "source_url": r["source_url"], "status": r["status"],
                 "notes": (f"raw key {k}; " if ALIAS.get(k, k) != k else "") + note})
out = pd.DataFrame(rows).drop_duplicates(["product_key", "geography", "event_date", "action", "indication_key"]).sort_values(["product_key", "geography", "event_date"])
out.to_csv(U / "label_events.csv", index=False)
print(f"{len(out)} curated events for {out['product_key'].nunique()} products from {len(raw)} raw rows; statuses {out['status'].value_counts().to_dict()}")
print(out[["product_key", "geography", "event_date", "action", "indication_key", "replaces"]].to_string(index=False))
