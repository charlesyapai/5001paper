"""Investment layer: sponsor commitment and retreat events per cohort product (topic 04 task 1; D005).

Inputs : data/investment/raw/events_by_product.csv   agent table (fixed header, status column), when present
         data/cohort/investment_events.csv            seed events with their verification status (F011, F020)
         data/cohort/product_cohort.csv               EU withdrawals and FDA post-approval events (F020), approval dates
         data/uptake/raw/*_disclosures.csv            statement rows that name a retreat (derived candidates, with URLs)
Output : data/investment/events.csv          one row per product x event, unified vocabulary, months from first approval
         data/investment/events_summary.csv  one row per cohort product: events by type, first retreat date and lag,
                                             whether the product was withdrawn anywhere, whether the sponsor changed hands

Event types: acquisition, asset-sale-or-licence, discontinuation-or-withdrawal, shipment-pause-or-restriction, restructuring,
sponsor-exit-from-modality, going-private-or-delisting, refusal, none-found. "Retreat" = discontinuation-or-withdrawal,
shipment-pause-or-restriction, restructuring, sponsor-exit-from-modality, going-private-or-delisting, asset-sale-or-licence.
Rows with status provisional-from-snippet or seeded-from-memory are kept in events.csv and excluded from the summary
counts (research/README.md rule 3).

Run from research/findings:  python3 build_investment_events_2026-09-05.py
"""
import glob, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/investment"
RETREAT = {"discontinuation-or-withdrawal", "shipment-pause-or-restriction", "restructuring", "sponsor-exit-from-modality",
           "going-private-or-delisting", "refusal"}   # asset sales and licences are reported separately (a sale can be commitment by the buyer)
SYN = {"libmeldy": "lenmeldy", "upstaza": "kebilidi", "durveqtix": "beqvez"}
HEADER = ["product", "sponsor_at_event", "event_date", "event_type", "event_title", "counterparty", "amount_usd_m", "manufacturing_model",
          "geography", "stated_reason_verbatim", "source_doc", "source_url", "fetched_date", "status", "notes"]


def key(name):
    k = re.split(r"[\s/(]", str(name).strip())[0].lower()
    return SYN.get(k, k)


coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh = coh[~coh["notes"].str.contains("out of scope")].copy()
coh["k"] = coh["product"].map(key)
coh["first_approval"] = [min([d for d in [pd.to_datetime(a, errors="coerce"), pd.to_datetime(b, errors="coerce")] if pd.notna(d)], default=pd.NaT)
                         for a, b in zip(coh["fda_approval_date"], coh["eu_authorisation_date"])]
cohi = coh.drop_duplicates("k").set_index("k")
ev = []

# 1. agent table
ap = OUT / "raw/events_by_product.csv"
if ap.exists():
    a = pd.read_csv(ap, dtype=str).fillna("")
    for _, r in a.iterrows():
        ev.append({**{c: r.get(c, "") for c in HEADER}, "origin": "agent events_by_product.csv"})

# 2. cohort withdrawals and FDA events (F020)
for _, c in coh.iterrows():
    if c["eu_withdrawn_date"]:
        ev.append({"product": c["product"], "sponsor_at_event": c["sponsor"], "event_date": c["eu_withdrawn_date"], "event_type": "discontinuation-or-withdrawal",
                   "event_title": "EU marketing authorisation withdrawn or expired", "geography": "EU", "manufacturing_model": c["platform_class"],
                   "source_doc": "EMA EPAR page", "source_url": c["eu_source_url"], "status": c["eu_status"] or "verified-from-source", "origin": "product_cohort.csv (F020)"})
    if c["eu_authorisation_type"].startswith("refused"):
        ev.append({"product": c["product"], "sponsor_at_event": c["sponsor"], "event_date": c["fda_event_date"] if False else "", "event_type": "refusal",
                   "event_title": "EU marketing authorisation refused", "geography": "EU", "manufacturing_model": c["platform_class"],
                   "source_doc": "EMA", "source_url": c["eu_source_url"], "status": c["eu_status"] or "verified-from-source", "origin": "product_cohort.csv (F020)",
                   "notes": c["eu_authorisation_type"]})
    if c["fda_post_approval_event"] and not c["fda_post_approval_event"].startswith("none") and re.search(r"restrict|discontinu|withdraw|pause", c["fda_post_approval_event"], re.I):
        ev.append({"product": c["product"], "sponsor_at_event": c["sponsor"], "event_date": c["fda_event_date"], "event_type": "shipment-pause-or-restriction",
                   "event_title": c["fda_post_approval_event"][:160], "geography": "US", "manufacturing_model": c["platform_class"],
                   "source_doc": "FDA product page", "source_url": c["fda_event_source_url"], "status": c["fda_status"] or "verified-from-source", "origin": "product_cohort.csv (F020)"})

# 3. seed events (verification status carried)
seed = pd.read_csv(ROOT / "data/cohort/investment_events.csv", dtype=str).fillna("")
TYPE = {"acquisition": "acquisition", "restructuring": "restructuring", "retreat": "discontinuation-or-withdrawal", "spin-off": "restructuring"}
for _, s in seed.iterrows():
    prods = [p.strip() for p in re.split(r"[;,]", s["products"]) if p.strip()] or [""]
    for p in prods:
        ev.append({"product": p, "event_date": s["year_seed"], "event_type": TYPE.get(s["event_type"], s["event_type"]), "event_title": s["event"],
                   "manufacturing_model": s["manufacturing_model"], "source_doc": s["source"], "status": s["status"], "fetched_date": s["verified_date"],
                   "origin": "investment_events.csv seed"})

# 4. disclosure statements naming a retreat (derived candidates)
PAT = r"discontinu|withdraw|paus|restructur|\bsold\b|sale of|divest|wind down|impairment|reduction in force|workforce|terminat|go private|going private|acquisition|Form 15|delist"
for f in glob.glob(str(ROOT / "data/uptake/raw/*_disclosures.csv")):
    d = pd.read_csv(f, dtype=str).fillna("")
    if "record_type" not in d.columns:
        continue
    st = d[(d["record_type"] == "statement") & d["verbatim"].str.contains(PAT, case=False, regex=True) & ~d["verbatim"].str.contains(r"coverage determination|payer coverage|commercial sale of", case=False)]
    for _, r in st.iterrows():
        v = r["verbatim"].lower()
        t = ("going-private-or-delisting" if re.search(r"form 15|delist|go private|going private", v) else
             "acquisition" if "acquisition" in v or "acquired" in v else
             "asset-sale-or-licence" if re.search(r"divest|out-licens|sale of|\bsold\b", v) else
             "shipment-pause-or-restriction" if "paus" in v else
             "restructuring" if re.search(r"restructur|reduction in force|workforce|impairment", v) else
             "discontinuation-or-withdrawal")
        ev.append({"product": r["product"], "event_date": r["as_of_date"], "event_type": t, "event_title": r["verbatim"][:160], "geography": r["region"],
                   "stated_reason_verbatim": r["verbatim"], "source_doc": r["source_doc"], "source_url": r["source_url"], "status": r["status"],
                   "origin": Path(f).name + " statement (type assigned by keyword)"})

E = pd.DataFrame(ev).fillna("")
for c in HEADER + ["origin"]:
    if c not in E.columns:
        E[c] = ""
E["product_key"] = E["product"].map(key)
E["date"] = pd.to_datetime(E["event_date"].str[:10], errors="coerce")
E.loc[E["date"].isna() & E["event_date"].str.fullmatch(r"\d{4}"), "date"] = pd.to_datetime(E.loc[E["date"].isna() & E["event_date"].str.fullmatch(r"\d{4}"), "event_date"] + "-07-01")
E["first_approval"] = E["product_key"].map(lambda k: cohi.loc[k, "first_approval"] if k in cohi.index else pd.NaT)
E["months_from_first_approval"] = ((E["date"] - E["first_approval"]).dt.days / 30.44).round(1)
E["usable"] = E["status"].isin(["verified-from-source", "derived"]) & E["date"].notna() & (E["event_type"] != "none-found")
# a class-wide safety labelling change (the 2024 CAR-T boxed warning for T-cell malignancies) is not a commercial retreat
E["is_retreat"] = E["event_type"].isin(RETREAT) & ~E["event_title"].str.contains("boxed warning|class-wide", case=False, regex=True)
E["is_prv_sale"] = E["event_title"].str.contains("priority review voucher|\bPRV\b", case=False, regex=True)   # a voucher sale is not a product event
E["after_approval"] = E["date"] >= E["first_approval"]
E = E.sort_values(["product_key", "date"])
E[["product", "product_key", "sponsor_at_event", "event_date", "event_type", "is_retreat", "event_title", "counterparty", "amount_usd_m", "manufacturing_model", "geography",
   "months_from_first_approval", "after_approval", "is_prv_sale", "stated_reason_verbatim", "source_doc", "source_url", "fetched_date", "status", "usable", "origin", "notes"]].to_csv(OUT / "events.csv", index=False)

rows = []
for k, c in cohi.iterrows():
    g = E[(E["product_key"] == k) & E["usable"]]
    ret = g[g["is_retreat"] & g["after_approval"]].sort_values("date")   # first retreat after first approval
    rows.append({"product": c["product"], "platform_class": c["platform_class"], "first_approval": c["first_approval"].date() if pd.notna(c["first_approval"]) else "",
                 "n_events_usable": len(g), "n_all_rows": int((E["product_key"] == k).sum()),
                 "types": ",".join(sorted(set(g["event_type"]))),
                 "first_retreat_date": ret["date"].iloc[0].date() if not ret.empty else "", "first_retreat_type": ret["event_type"].iloc[0] if not ret.empty else "",
                 "months_first_approval_to_first_retreat": ret["months_from_first_approval"].iloc[0] if not ret.empty else "",
                 "withdrawn_anywhere": bool((g["event_type"] == "discontinuation-or-withdrawal").any()),
                 "sponsor_acquired_or_asset_sold": bool((g["event_type"].isin(["acquisition", "asset-sale-or-licence", "going-private-or-delisting"]) & ~g["is_prv_sale"]).any()),
                 "product_sold_or_licensed_after_approval": bool(((g["event_type"] == "asset-sale-or-licence") & ~g["is_prv_sale"] & g["after_approval"]).any())})
S = pd.DataFrame(rows)
S.to_csv(OUT / "events_summary.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 40)
print(f"event rows: {len(E)} (usable {int(E['usable'].sum())}) from origins {E['origin'].str.split(' ').str[0].value_counts().to_dict()}")
print("types (usable):", E[E["usable"]]["event_type"].value_counts().to_dict())
print(f"products with a usable retreat event after approval: {int((S['first_retreat_date'] != '').sum())} of {len(S)}; withdrawn anywhere: {int(S['withdrawn_anywhere'].sum())}; sponsor acquired or asset sold: {int(S['sponsor_acquired_or_asset_sold'].sum())}; product sold or licensed after approval: {int(S['product_sold_or_licensed_after_approval'].sum())}")
print("retreat types (after approval):", E[E["usable"] & E["is_retreat"] & E["after_approval"]]["event_type"].value_counts().to_dict())
r = S[S["months_first_approval_to_first_retreat"] != ""]
print("months first approval to first retreat: median", pd.to_numeric(r["months_first_approval_to_first_retreat"]).median(), "n", len(r))
print(S[S["n_events_usable"] > 0][["product", "platform_class", "first_approval", "n_events_usable", "types", "first_retreat_date", "months_first_approval_to_first_retreat"]].to_string(index=False))
