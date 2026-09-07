"""Provenance audit of agent-retrieved rows (handover item F). A 5 percent random sample of rows with a verified status was drawn
from every raw table that carries status and source_url columns (data/audit/audit_sample_2026-09-07.csv, 171 rows, seed 20260907),
split into four batches, and each batch's sources were re-opened by an independent agent that recorded reachability and a
verdict (agree, minor-discrepancy, disagree, not-verifiable) with a note. This script merges the batches and reports the error
rate overall, per data layer and per raw table.

Outputs: data/audit/audit_results.csv (sample rows with verdicts), data/audit/audit_summary.csv (per layer and per table)
Run from research/findings:  python3 build_audit_2026-09-07.py
"""
import glob
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "data/audit"
sample = pd.read_csv(A / "audit_sample_2026-09-07.csv", dtype=str).fillna("")
res = pd.concat([pd.read_csv(f, dtype=str).fillna("") for f in sorted(glob.glob(str(A / "raw/audit_*.csv")))], ignore_index=True)
res["verdict"] = res["verdict"].str.strip().str.lower(); res["reachable"] = res["reachable"].str.strip().str.lower()
out = sample.merge(res[["sample_id", "reachable", "values_checked", "verdict", "discrepancy_note", "fetched_date"]], on="sample_id", how="left")
out["verdict"] = out["verdict"].replace("", "not-returned").fillna("not-returned")
out["layer"] = out["raw_file"].str.split("/").str[1]
out.to_csv(A / "audit_results.csv", index=False)


def summarise(g):
    n = len(g); v = g["verdict"].value_counts()
    checked = int(v.get("agree", 0) + v.get("minor-discrepancy", 0) + v.get("disagree", 0))
    return pd.Series({"rows_sampled": n, "reached": int(g["reachable"].isin(["reached", "reached-via-wayback"]).sum()), "agree": int(v.get("agree", 0)),
                      "minor_discrepancy": int(v.get("minor-discrepancy", 0)), "disagree": int(v.get("disagree", 0)), "not_verifiable": int(v.get("not-verifiable", 0) + v.get("not-returned", 0)),
                      "checked": checked, "disagree_rate_among_checked": round(v.get("disagree", 0) / checked, 3) if checked else np.nan,
                      "any_discrepancy_rate_among_checked": round((v.get("disagree", 0) + v.get("minor-discrepancy", 0)) / checked, 3) if checked else np.nan})


summ = pd.concat([out.groupby("layer").apply(summarise, include_groups=False).assign(level="layer").reset_index().rename(columns={"layer": "group"}),
                  out.groupby("raw_file").apply(summarise, include_groups=False).assign(level="table").reset_index().rename(columns={"raw_file": "group"}),
                  pd.DataFrame([summarise(out)]).assign(level="all", group="all rows")], ignore_index=True)
summ = summ[["level", "group", "rows_sampled", "reached", "checked", "agree", "minor_discrepancy", "disagree", "not_verifiable", "disagree_rate_among_checked", "any_discrepancy_rate_among_checked"]]
summ.to_csv(A / "audit_summary.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120)
print(summ[summ["level"] != "table"].to_string(index=False))
print("\nDISAGREE rows:")
print(out[out["verdict"] == "disagree"][["sample_id", "raw_file", "row_index", "values_checked", "discrepancy_note"]].to_string(index=False))
print("\nMINOR discrepancies:")
print(out[out["verdict"] == "minor-discrepancy"][["sample_id", "raw_file", "discrepancy_note"]].to_string(index=False))
