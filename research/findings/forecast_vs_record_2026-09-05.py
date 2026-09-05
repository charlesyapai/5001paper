"""Forecast against record (topic 05; figure 6): the field's own projections against the realised counts.

Inputs : data/cohort/raw/projections_S16_S17.csv (S16 abstract figures, the NEWDIGS 2020 approvals brief that
         underlies S16, the S17 France series, the S20 Tufts pipeline page), data/cohort/product_cohort.csv
         (realised FDA approvals), data/uptake/raw/cart_registry_counts.csv (realised US CAR-T patients, CIBMTR),
         data/uptake/uptake_summary.csv.
Output : data/projection/forecast_vs_record.csv, one row per comparison year: projected value, realised value,
         ratio, definitions and caveats. Console summary.

Definitions. Realised approvals are first FDA approvals of cohort products by calendar year, counted two
ways: genetic products only, and genetic plus non-genetic durable cell therapies (Amtagvi, Ryoncil,
Omisirge, Lantidra, Tregzi, Provenge). The NEWDIGS brief counts product-indication approvals of durable
cell and gene therapies, so label expansions would raise the realised count somewhat; the comparison is
indicative. Realised US CAR-T patients per year are CIBMTR-reported infusions (S24), the largest realised
component of the "patients treated" projections.

Run from research/findings:  python3 forecast_vs_record_2026-09-05.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/projection"
OUT.mkdir(exist_ok=True)

pj = pd.read_csv(ROOT / "data/cohort/raw/projections_S16_S17.csv", dtype=str).fillna("")
pj["year"] = pd.to_numeric(pj["year"].str[:4], errors="coerce")
pj["v"] = pd.to_numeric(pj["value_point"], errors="coerce")

coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh = coh[(coh["fda_approval_date"] != "") & ~coh["notes"].str.contains("out of scope") & ~coh["fda_approval_date"].str.startswith("not")]
coh["yr"] = coh["fda_approval_date"].str[:4].astype(int)
gen = coh[coh["genetic_modification"] == "yes"].groupby("yr").size()
allc = coh.groupby("yr").size()
years = range(2010, 2027)
real_gen_cum = pd.Series({y: int(gen[gen.index <= y].sum()) for y in years})
real_all_cum = pd.Series({y: int(allc[allc.index <= y].sum()) for y in years})

reg = pd.read_csv(ROOT / "data/uptake/raw/cart_registry_counts.csv", dtype=str).fillna("")
us = reg[(reg["registry"].str.contains("CIBMTR")) & reg["geography"].str.contains("United States") & (reg["status"] == "verified-from-source")
         & reg["count_type"].isin(["patients", "infusions"]) & reg["product_or_class"].str.contains("all", case=False)].copy()
us["count"] = pd.to_numeric(us["count"], errors="coerce")
us["year"] = pd.to_numeric(us["year"], errors="coerce")
us_cart = us.groupby("year")["count"].max()

rows = []
# 1. NEWDIGS 2020 brief (pipeline snapshot 31 Dec 2019): mean cumulative US approvals
nd = pj[(pj["source_id"] == "S16-predecessor") & (pj["series"] == "approvals_cumulative") & pj["scenario"].str.startswith("base (excl. China") & pj["year"].notna()]
for _, r in nd.iterrows():
    y = int(r["year"])
    if y in real_gen_cum.index:
        rows.append({"comparison": "cumulative US approvals of durable CGT", "source": "NEWDIGS brief 2020F207 (S38), mean, pipeline at 31 Dec 2019", "geography": "US",
                     "year": y, "projected": r["v"], "realised_genetic_only": real_gen_cum[y], "realised_incl_nongenetic_cell": real_all_cum[y],
                     "ratio_realised_genetic_to_projected": round(real_gen_cum[y] / r["v"], 2), "ratio_realised_all_to_projected": round(real_all_cum[y] / r["v"], 2),
                     "caveat": "projection counts product-indication approvals; realised counts first product approvals (Provenge 2010 included in the all-products count)"})
# 2. S17 France: projected launches (not compared; no realised French launch series yet) and patients
s17 = pj[(pj["source_id"] == "S17") & (pj["series"].isin(["approvals_per_year", "patients_new_per_year"])) & (pj["scenario"] == "base (most expected launch scenario)") & pj["year"].notna()]
for _, r in s17.iterrows():
    rows.append({"comparison": f"France {r['series']}", "source": "Lee et al. 2024 (S17), most expected scenario, pipeline Dec 2022", "geography": "France",
                 "year": int(r["year"]), "projected": r["v"], "realised_genetic_only": "", "realised_incl_nongenetic_cell": "",
                 "ratio_realised_genetic_to_projected": "", "ratio_realised_all_to_projected": "",
                 "caveat": "realised French counts to come from the access layer (launches) and DESCAR-T (CAR-T patients)"})
# 3. S20 Tufts page: total US patients treated per year (figure 2) against realised CIBMTR CAR-T patients
s20 = pj[(pj["source_id"] == "S20") & (pj["series"] == "patients_new_per_year") & pj["scenario"].str.contains("Figure 2 total") & pj["year"].notna()]
onc = pj[(pj["source_id"] == "S20") & (pj["series"] == "patients_new_per_year") & pj["scenario"].str.contains("Incident cases - oncology") & pj["year"].notna()].set_index("year")["v"]
for _, r in s20.iterrows():
    y = int(r["year"])
    real = us_cart.get(y, float("nan"))
    rows.append({"comparison": "US patients treated per year with durable CGT", "source": "Tufts NEWDIGS pipeline deep dive (S20), figure 2 read from image, pipeline Dec 2023", "geography": "US",
                 "year": y, "projected": r["v"], "realised_genetic_only": "", "realised_incl_nongenetic_cell": "",
                 "ratio_realised_genetic_to_projected": "", "ratio_realised_all_to_projected": "",
                 "realised_us_cart_patients_cibmtr": real if real == real else "", "projected_oncology_component": onc.get(y, ""),
                 "ratio_cart_to_oncology_component": round(real / onc[y], 2) if real == real and y in onc.index and onc[y] else "",
                 "caveat": "realised column is CAR-T only (CIBMTR-reported patients); gene therapy patients (a few hundred per year in the US) would add to it"})
out = pd.DataFrame(rows)
out.to_csv(OUT / "forecast_vs_record.csv", index=False)
pd.set_option("display.width", 240)
print("realised cumulative FDA approvals (genetic | all durable):")
print(pd.DataFrame({"genetic": real_gen_cum, "all": real_all_cum}).loc[2017:2026].T.to_string())
print("\napprovals comparison:")
print(out[out["comparison"].str.startswith("cumulative")][["year", "projected", "realised_genetic_only", "realised_incl_nongenetic_cell", "ratio_realised_genetic_to_projected", "ratio_realised_all_to_projected"]].to_string(index=False))
print("\npatients comparison (US):")
print(out[out["comparison"].str.startswith("US patients")][["year", "projected", "projected_oncology_component", "realised_us_cart_patients_cibmtr", "ratio_cart_to_oncology_component"]].head(6).to_string(index=False))
