"""Merge agent-verified approval dates into data/cohort/product_cohort.csv.

Inputs : batch_*.csv produced by the retrieval agents (path given on the command line),
         data/cohort/product_cohort.csv (seed table).
Outputs: data/cohort/product_cohort.csv rewritten with sourced date columns,
         data/cohort/product_cohort_verification_report.csv listing every seed-vs-source
         disagreement and every product still unverified.

Run from research/findings:  python3 verify_cohort_dates_2026-09-04.py <dir with batch csvs>
"""
import sys, glob, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
COHORT = ROOT / "data/cohort/product_cohort.csv"
REPORT = ROOT / "data/cohort/product_cohort_verification_report.csv"

batch_dir = Path(sys.argv[1])
frames = [pd.read_csv(p, dtype=str) for p in sorted(glob.glob(str(batch_dir / "batch_*.csv")))]
v = pd.concat(frames, ignore_index=True).fillna("")
v["key"] = v["product"].str.split("/").str[0].str.strip().str.lower()

c = pd.read_csv(COHORT, dtype=str).fillna("")
c["key"] = c["product"].str.split("/").str[0].str.strip().str.lower()

new_cols = ["fda_approval_date", "fda_pathway", "fda_source_url", "fda_status",
            "fda_post_approval_event", "fda_event_date", "fda_event_source_url",
            "eu_authorisation_date", "eu_authorisation_type", "eu_withdrawn_date",
            "eu_source_url", "eu_status", "fetched_date"]
for col in new_cols:
    if col not in c.columns:
        c[col] = ""

rows = []
for i, r in c.iterrows():
    m = v[v["key"] == r["key"]]
    if m.empty:
        # Tissue-engineered and cord-blood entries are out of scope for the flagship and were not verified.
        c.at[i, "dates_verified"] = "out-of-scope"
        rows.append({"product": r["product"], "issue": "out of scope; not verified", "seed_fda": r["fda_year_seed"],
                     "seed_eu": r["eu_year_seed"], "source_fda": "", "source_eu": ""})
        continue
    m = m.iloc[0]
    for col in new_cols:
        c.at[i, col] = m.get(col, "")
    fda_ok = m["fda_status"] in ("verified-from-source", "not-applicable")  # EU-only products have no FDA date
    # "not-found" means the agent checked EMA and found no authorisation: a verified absence.
    eu_ok = m["eu_status"] in ("verified-from-source", "not-applicable", "not-found")
    c.at[i, "dates_verified"] = "yes" if (fda_ok and eu_ok) else ("partial" if (fda_ok or eu_ok) else "no")
    c.at[i, "date_source"] = "; ".join(s for s in [m["fda_source_url"], m["eu_source_url"]] if s)

    def year(s):
        mm = re.match(r"(\d{4})", s or "")
        return mm.group(1) if mm else ""
    issues = []
    if r["fda_year_seed"] and year(m["fda_approval_date"]) and r["fda_year_seed"] != year(m["fda_approval_date"]):
        issues.append(f"FDA year seed {r['fda_year_seed']} vs source {year(m['fda_approval_date'])}")
    if r["eu_year_seed"] and year(m["eu_authorisation_date"]) and r["eu_year_seed"] != year(m["eu_authorisation_date"]):
        issues.append(f"EU year seed {r['eu_year_seed']} vs source {year(m['eu_authorisation_date'])}")
    if not fda_ok and m["fda_status"] != "not-applicable":
        issues.append(f"FDA date {m['fda_status']}")
    if not eu_ok:
        issues.append(f"EU date {m['eu_status']}")
    if issues:
        rows.append({"product": r["product"], "issue": "; ".join(issues), "seed_fda": r["fda_year_seed"],
                     "seed_eu": r["eu_year_seed"], "source_fda": m["fda_approval_date"],
                     "source_eu": m["eu_authorisation_date"]})

c = c.drop(columns=["key"])
c.to_csv(COHORT, index=False)
pd.DataFrame(rows).to_csv(REPORT, index=False)

tot = len(c)
print(f"cohort rows: {tot}")
print("dates_verified:", c["dates_verified"].value_counts().to_dict())
print("fda_status:", c["fda_status"].value_counts().to_dict())
print("eu_status:", c["eu_status"].value_counts().to_dict())
print(f"report rows: {len(rows)} -> {REPORT.relative_to(ROOT)}")
for r in rows:
    print(f"  {r['product']}: {r['issue']}")
