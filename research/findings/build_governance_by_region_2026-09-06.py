"""Governance and blockers by region (topic 02 task 3 first pass; the regional differentiation the flagship needs).

Inputs : data/access/decisions.csv and access_summary.csv (six systems, F043); data/access/raw/governance_{us,singapore,china}.csv
         when present (agent tables with a fixed header: system, product, event_type, event_date, body, outcome, detail, amount,
         currency, stated_reason_verbatim, source_doc, source_url, fetched_date, status, notes).
Outputs: data/access/governance_by_region.csv   one row per system: bodies, funding step, median lag, share of approvals funded,
                                                 share not recommended or terminated or deferred, arrangement types, the
                                                 stated-reason categories with counts, eligible counts stated or not
         data/access/stated_reasons.csv          every usable decision row with its keyword-coded reason categories

Reason categories (keyword coding of the verbatim committee text, several may apply): uncertainty-durability (long-term
effect, immature data, single-arm), cost-effectiveness (ICER, QALY, cost per, willingness to pay, wirtschaftlich), budget-impact,
comparator-or-evidence (comparator, indirect, non-randomised, Zusatznutzen nicht belegt), price (price reduction, prix,
Preis, negotiation), population-or-restriction (subgroup, restricted, eligible), capacity-or-delivery (centres, manufacturing,
supply). A row with none of these is coded "none stated". Human coding of a validation sample remains task 3 of topic 02.

Run from research/findings:  python3 build_governance_by_region_2026-09-06.py
"""
import re, glob
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "data/access"
CATS = {
    "uncertainty-durability": r"durab|long[- ]term|immatur|uncertain|unsicher|incertitude|single[- ]arm|einarmig|follow[- ]up|maturity|ungewiss|non comparat",
    "cost-effectiveness": r"\bICER\b|QALY|cost[- ]effective|cost per|willingness|wirtschaftlich|coût[- ]efficacité|value for money|rapport coût",
    "budget-impact": r"budget|affordab|expenditure|spending|dépense|Ausgaben|financial impact|impatto",
    "comparator-or-evidence": r"comparator|indirect|non[- ]?randomi|nicht belegt|Zusatznutzen|no evidence|insufficient evidence|limited evidence|ASMR|SMR insuffisant|quality of evidence|GRADE|données|Daten",
    "price": r"\bprice\b|prix|Preis|prezzo|negotiat|discount|rebate|Erstattungsbetrag|tarif",
    "population-or-restriction": r"subgroup|restrict|eligible|population|Teilpopulation|line of therapy|only for|limited to|criteri",
    "capacity-or-delivery": r"cent(re|er)s?|manufactur|supply|capacity|logisti|infrastructure|qualified|accredit",
}
dec = pd.read_csv(A / "decisions.csv", dtype=str).fillna("")
summ = pd.read_csv(A / "access_summary.csv", dtype=str).fillna("")
usable = dec[dec["usable"].astype(str).str.lower() == "true"].copy()
txt = usable["stated_reasons_verbatim"] + " " + usable["arrangement_detail"] + " " + usable["notes"]
for c, pat in CATS.items():
    usable[c] = txt.str.contains(pat, case=False, regex=True)
usable["none stated"] = ~usable[list(CATS)].any(axis=1)
usable[["system", "body", "product_key", "indication_key", "decision_date", "outcome", "arrangement_type"] + list(CATS) + ["none stated", "stated_reasons_verbatim", "source_url"]].to_csv(A / "stated_reasons.csv", index=False)

rows = []
for s, g in usable.groupby("system"):
    sm = summ[summ["system"] == s]
    lag = pd.to_numeric(sm["months_approval_to_first_funding"], errors="coerce").dropna()
    neg = g["outcome"].isin(["not-recommended", "terminated-or-withdrawn"]).mean()
    defer = dec[(dec["system"] == s) & (dec["outcome"] == "under-assessment")].shape[0]
    arr = g[g["arrangement_type"].isin(["managed-access-agreement", "outcomes-based", "cancer-drugs-fund", "price-volume", "confidential-discount", "instalment"])]["arrangement_type"].value_counts()
    cats = {c: int(g[c].sum()) for c in CATS}
    top = sorted(cats.items(), key=lambda x: -x[1])[:3]
    elig = g["notes"].str.contains(r"eligible|Patienten:|population cible|patients per year|per year", case=False, regex=True).mean()
    rows.append({"system": s, "bodies": ", ".join(sorted(g["body"].unique())), "n_decision_rows_usable": len(g), "n_products_with_funding": int(lag.shape[0]),
                 "median_months_approval_to_funding": round(lag.median(), 1) if len(lag) else "", "iqr_months": f"{lag.quantile(.25):.1f} to {lag.quantile(.75):.1f}" if len(lag) else "",
                 "share_rows_not_recommended_or_terminated": round(neg, 2), "n_deferrals_or_under_assessment": defer,
                 "arrangement_types": "; ".join(f"{k} {v}" for k, v in arr.items()), "share_rows_with_arrangement": round(len(g[g["arrangement_type"].isin(arr.index)]) / len(g), 2) if len(g) else "",
                 "top_stated_reason_categories": "; ".join(f"{k} {v}" for k, v in top), "share_rows_with_no_stated_reason": round(g["none stated"].mean(), 2),
                 "share_rows_stating_an_eligible_count": round(elig, 2), "source": "decisions.csv (F043)"})
# systems from the agent governance tables (US, Singapore, China): summarise what exists
for f in sorted(glob.glob(str(A / "raw/governance_*.csv"))):
    d = pd.read_csv(f, dtype=str).fillna("")
    if d.empty:
        continue
    s = d["system"].iloc[0]
    v = d[d["status"] == "verified-from-source"]
    rows.append({"system": s, "bodies": ", ".join(sorted(set(v["body"]) - {""}))[:200], "n_decision_rows_usable": len(v),
                 "n_products_with_funding": int(v[v["event_type"].isin(["subsidy-listing", "insurance-coverage", "reimbursement-decision", "coverage-determination", "access-model", "state-coverage"]) & v["outcome"].str.contains("covered|listed|subsidised|recommended", case=False)]["product"].nunique()),
                 "median_months_approval_to_funding": "", "iqr_months": "", "share_rows_not_recommended_or_terminated": "", "n_deferrals_or_under_assessment": "",
                 "arrangement_types": "; ".join(f"{k} {n}" for k, n in v["event_type"].value_counts().items()),
                 "share_rows_with_arrangement": "", "top_stated_reason_categories": "", "share_rows_with_no_stated_reason": "", "share_rows_stating_an_eligible_count": "",
                 "source": Path(f).name + " (agent table; see the regional notes)"})
out = pd.DataFrame(rows)
out.to_csv(A / "governance_by_region.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_colwidth", 60)
print(out[["system", "n_decision_rows_usable", "median_months_approval_to_funding", "share_rows_not_recommended_or_terminated", "n_deferrals_or_under_assessment", "share_rows_with_arrangement", "top_stated_reason_categories", "share_rows_with_no_stated_reason", "share_rows_stating_an_eligible_count"]].to_string(index=False))
print("\nreason categories by system (counts of usable rows):")
print(usable.groupby("system")[list(CATS) + ["none stated"]].sum().astype(int).to_string())
