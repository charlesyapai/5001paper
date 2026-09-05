"""Access-stage decisions across health systems (topic 02 task 2).

Inputs : data/access/raw/decisions_<system>.csv from the retrieval agents (one row per product x indication x
         decision; fixed header, status column), data/cohort/product_cohort.csv for approval dates.
Outputs: data/access/decisions.csv        every decision row, normalised (product_key, system, body, dates parsed,
                                          months from regulatory approval to decision, outcome, arrangement, status)
         data/access/access_summary.csv   one row per product x system: first decision date and outcome, months from
                                          EU or national approval to first decision, from FDA approval to first decision,
                                          latest outcome, arrangement, whether any decision is verified

Rules. Rows with status provisional-from-snippet or not-found are kept in decisions.csv and excluded from the
summary durations (research/README.md rule 3). The duration uses regulatory_approval_date as stated by the agent
(EU or national authorisation for that indication); where blank, the cohort's EU authorisation date, else FDA date,
with the basis recorded. Outcome vocabulary: recommended, recommended-restricted, recommended-managed-access,
not-recommended, terminated-or-withdrawn, under-assessment, not-submitted, not-found.

Run from research/findings:  python3 build_access_decisions_2026-09-05.py
"""
import glob, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/access/raw"
OUT = ROOT / "data/access"
HEADER = ["product", "system", "country", "body", "indication_key", "indication_text", "regulatory_approval_date", "submission_or_start_date",
          "decision_date", "outcome", "arrangement_type", "arrangement_detail", "added_benefit_or_rating", "price_at_decision", "price_currency",
          "price_basis", "stated_reasons_verbatim", "document_title", "document_id", "source_url", "fetched_date", "status", "notes"]
OUTCOMES = {"recommended", "recommended-restricted", "recommended-managed-access", "not-recommended", "terminated-or-withdrawn",
            "under-assessment", "not-submitted", "not-found"}
SYN = {"libmeldy": "lenmeldy", "upstaza": "kebilidi", "durveqtix": "beqvez"}


def key(name):
    k = re.split(r"[\s/(]", str(name).strip())[0].lower()
    return SYN.get(k, k)


def date(x):
    return pd.to_datetime(str(x).strip()[:10], errors="coerce") if str(x).strip() else pd.NaT


frames = []
for f in sorted(glob.glob(str(RAW / "decisions_*.csv"))):
    d = pd.read_csv(f, dtype=str).fillna("")
    missing = [c for c in HEADER if c not in d.columns]
    if missing:
        print(f"{Path(f).name}: missing columns {missing}; skipped")
        continue
    d = d[HEADER].copy()
    d["source_file"] = Path(f).name
    frames.append(d)
if not frames:
    raise SystemExit("no data/access/raw/decisions_*.csv yet")
dec = pd.concat(frames, ignore_index=True)
dec["product_key"] = dec["product"].map(key)
# HAS avis rows read from the French government's Base de donnees publique des medicaments bulk extracts (CIS_HAS_SMR, CIS_HAS_ASMR):
# an official extract of the avis conclusion, not a search snippet, so graded verified-from-source here with the basis recorded.
bdpm = (dec["body"] == "HAS-CT") & (dec["status"] == "provisional-from-snippet") & dec["notes"].str.contains("BDPM|Base de donn", case=False, regex=True)
dec.loc[bdpm, "status"] = "verified-from-source"
dec.loc[bdpm, "notes"] = dec.loc[bdpm, "notes"] + " | status set to verified-from-source in the merge: official BDPM extract of the avis"
print(f"HAS-CT rows upgraded from the BDPM extract: {int(bdpm.sum())}")
dec["outcome"] = dec["outcome"].str.strip().str.lower()
bad = dec[~dec["outcome"].isin(OUTCOMES)]
if not bad.empty:
    print("outcomes outside the vocabulary (kept, review):", bad["outcome"].value_counts().to_dict())
coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh["k"] = coh["product"].map(key)
coh = coh.drop_duplicates("k").set_index("k")
dec["approval_dt"] = dec["regulatory_approval_date"].map(date)
dec["approval_basis"] = "stated by agent"
for i, r in dec.iterrows():
    if pd.isna(r["approval_dt"]) and r["product_key"] in coh.index:
        c = coh.loc[r["product_key"]]
        if c["eu_authorisation_date"]:
            dec.loc[i, "approval_dt"], dec.loc[i, "approval_basis"] = date(c["eu_authorisation_date"]), "cohort EU authorisation"
        elif c["fda_approval_date"]:
            dec.loc[i, "approval_dt"], dec.loc[i, "approval_basis"] = date(c["fda_approval_date"]), "cohort FDA approval"
dec["decision_dt"] = dec["decision_date"].map(date)
dec["fda_dt"] = dec["product_key"].map(lambda k: date(coh.loc[k, "fda_approval_date"]) if k in coh.index else pd.NaT)
dec["months_approval_to_decision"] = ((dec["decision_dt"] - dec["approval_dt"]).dt.days / 30.44).round(1)
dec["months_fda_to_decision"] = ((dec["decision_dt"] - dec["fda_dt"]).dt.days / 30.44).round(1)
dec["usable"] = dec["status"].isin(["verified-from-source", "derived"]) & dec["decision_dt"].notna() & dec["outcome"].isin(OUTCOMES - {"not-found", "not-submitted", "under-assessment"})
dec.to_csv(OUT / "decisions.csv", index=False)

# The body whose positive decision opens funded access in each system (the HTA opinion alone does not, in Canada and France)
FUNDING_BODY = {"Canada": ["pCPA"], "England": ["NICE"], "Germany": ["G-BA"], "France": ["JO", "CEPS", "ANSM"], "Italy": ["AIFA"], "Australia": ["Funding", "PBAC", "MSAC"]}
FUNDING_BODY_NO_EARLY = {"France": ["JO", "CEPS"]}   # France without the paid early-access route (acces precoce, ATU)


def body_in(b, names):
    return any(str(b).startswith(n) for n in names)
POSITIVE = {"recommended", "recommended-restricted", "recommended-managed-access"}
rows = []
for (pk, sysm), g in dec.groupby(["product_key", "system"]):
    u = g[g["usable"]].sort_values("decision_dt")
    fb = FUNDING_BODY.get(sysm, [])
    fund = u[u["body"].map(lambda b: body_in(b, fb)).astype(bool) & u["outcome"].isin(POSITIVE)] if fb else u[u["outcome"].isin(POSITIVE)]
    fund = fund.sort_values("decision_dt")
    f0 = fund.iloc[0] if not fund.empty else None
    fb2 = FUNDING_BODY_NO_EARLY.get(sysm)
    f1 = None
    if fb2:
        fund2 = u[u["body"].map(lambda b: body_in(b, fb2)).astype(bool) & u["outcome"].isin(POSITIVE)].sort_values("decision_dt")
        f1 = fund2.iloc[0] if not fund2.empty else None
    first = u.iloc[0] if not u.empty else None
    latest = u.iloc[-1] if not u.empty else None
    rows.append({"product_key": pk, "system": sysm, "n_rows": len(g), "n_usable": len(u),
                 "first_decision_date": first["decision_dt"].date() if first is not None else "",
                 "first_outcome": first["outcome"] if first is not None else (g["outcome"].iloc[0] if len(g) else ""),
                 "first_body": first["body"] if first is not None else "",
                 "months_approval_to_first_decision": first["months_approval_to_decision"] if first is not None else "",
                 "approval_basis": first["approval_basis"] if first is not None else "",
                 "months_fda_to_first_decision": first["months_fda_to_decision"] if first is not None else "",
                 "first_funding_body": f0["body"] if f0 is not None else "",
                 "first_funding_date": f0["decision_dt"].date() if f0 is not None else "",
                 "months_approval_to_first_funding": f0["months_approval_to_decision"] if f0 is not None else "",
                 "months_approval_to_first_funding_excl_early_access": (f1["months_approval_to_decision"] if f1 is not None else "") if fb2 else (f0["months_approval_to_decision"] if f0 is not None else ""),
                 "latest_outcome": latest["outcome"] if latest is not None else "",
                 "latest_decision_date": latest["decision_dt"].date() if latest is not None else "",
                 "arrangement_types": ",".join(sorted(set(u["arrangement_type"]) - {""})) if not u.empty else "",
                 "any_not_recommended": bool((u["outcome"] == "not-recommended").any()) if not u.empty else False,
                 "statuses": ",".join(sorted(set(g["status"])))})
summ = pd.DataFrame(rows).sort_values(["product_key", "system"])
summ.to_csv(OUT / "access_summary.csv", index=False)

pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 40)
print(f"decision rows: {len(dec)} from {dec['source_file'].nunique()} files; usable for durations: {int(dec['usable'].sum())}; products: {dec['product_key'].nunique()}")
print("status:", dec["status"].value_counts().to_dict())
print("outcome:", dec["outcome"].value_counts().to_dict())
u = summ[summ["months_approval_to_first_decision"] != ""].copy()
u["m"] = pd.to_numeric(u["months_approval_to_first_decision"])
print("\nmonths from regulatory approval to first usable decision, by system (median, IQR, n):")
print(u.groupby("system")["m"].describe()[["count", "25%", "50%", "75%"]].round(1).to_string())
print("\nmonths from regulatory approval to first positive funding step (body per system: NICE, G-BA, pCPA, JO/CEPS, AIFA, PBAC/MSAC/Funding):")
f = summ[summ["months_approval_to_first_funding"] != ""].copy()
f["m"] = pd.to_numeric(f["months_approval_to_first_funding"])
print(f.groupby("system")["m"].describe()[["count", "25%", "50%", "75%"]].round(1).to_string())
f2 = summ[summ["months_approval_to_first_funding_excl_early_access"] != ""].copy()
f2["m"] = pd.to_numeric(f2["months_approval_to_first_funding_excl_early_access"])
print("\nsame, France without early access (JO inscription or CEPS price):")
print(f2[f2["system"] == "France"]["m"].describe()[["count", "25%", "50%", "75%"]].round(1).to_string())
print("\nmonths from approval to decision, by body (usable rows):")
print(dec[dec["usable"]].groupby(["system", "body"])["months_approval_to_decision"].describe()[["count", "25%", "50%", "75%"]].round(1).to_string())
print("\nfirst outcome by system:")
print(pd.crosstab(u["system"], u["first_outcome"]).to_string())
