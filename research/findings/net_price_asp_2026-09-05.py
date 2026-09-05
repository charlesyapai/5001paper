"""US net price from Medicare Part B ASP payment limits, compared with list price (topic 03 open question).

Inputs : data/uptake/raw/cms_asp_payment_limits.csv (payment limit per HCPCS code per quarterly file),
         data/uptake/raw/*_disclosures.csv and verification_*.csv (list_price rows, US, by date or year).
Method : implied ASP = payment limit / 1.06. The ASP in the file for quarter Q reflects manufacturer
         sales two quarters earlier, so each file quarter is matched to the list price in force two
         quarters before the file date (and, as a check, in the same calendar year). Ratio = ASP / WAC.
Output : data/uptake/net_price_asp.csv  one row per product per file quarter with the matched list
         price and the ratio; console summary per product.

Run from research/findings:  python3 net_price_asp_2026-09-05.py
"""
import glob, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/uptake/raw"
SYN = {"beqvez / durveqtix": "beqvez"}


def key(name):
    k = re.split(r"[\s/(]", str(name).strip())[0].lower()
    return SYN.get(k, k)


asp = pd.read_csv(RAW / "cms_asp_payment_limits.csv", dtype=str).fillna("")
asp = asp[asp["status"] == "verified-from-source"].copy()
asp["product_key"] = asp["product"].map(key)
asp["pl"] = pd.to_numeric(asp["payment_limit_usd"], errors="coerce")
asp["asp"] = asp["pl"] / 1.06
asp["file_q"] = pd.PeriodIndex(asp["asp_file_quarter"], freq="Q")
asp["sales_q"] = asp["file_q"] - 2

frames = []
for f in glob.glob(str(RAW / "*_disclosures.csv")) + glob.glob(str(RAW / "verification_*.csv")):
    d = pd.read_csv(f, dtype=str).fillna("")
    frames.append(d)
dis = pd.concat(frames, ignore_index=True)
lp = dis[(dis["record_type"] == "list_price") & dis["region"].str.contains(r"^US|United States|U\.S\.", case=False)].copy()
lp["product_key"] = lp["product"].map(key)
lp["v"] = pd.to_numeric(lp["value"].astype(str).str.replace(",", "").str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
lp = lp[lp["v"].notna() & lp["unit"].str.contains(r"treatment|patient|course|WAC|acquisition|list", case=False)
        & ~lp["unit"].str.contains(r"payment limit|ASP", case=False)]
lp["v"] = lp["v"].where(lp["v"] >= 100, lp["v"] * 1e6)
# effective date: a bare year means 1 January of that year
lp["eff"] = pd.to_datetime(lp["as_of_date"].str.extract(r"^(\d{4}(?:-\d{2}(?:-\d{2})?)?)")[0].map(lambda s: s if s is None or len(str(s)) > 7 else (str(s) + "-01" if len(str(s)) == 7 else str(s) + "-01-01")), errors="coerce")
lp = lp[lp["eff"].notna()].sort_values(["product_key", "eff"])


def wac_at(product, date):
    g = lp[(lp["product_key"] == product) & (lp["eff"] <= date)]
    if g.empty:
        return float("nan"), ""
    r = g.iloc[-1]
    return float(r["v"]), f"{r['eff'].date()} {r['status']} {r['source_doc'][:50]}"


rows = []
for _, r in asp.iterrows():
    w, wsrc = wac_at(r["product_key"], r["sales_q"].end_time)
    rows.append({"product": r["product_key"], "hcpcs": r["hcpcs"], "asp_file_quarter": r["asp_file_quarter"], "sales_quarter": str(r["sales_q"]),
                 "payment_limit_usd": r["pl"], "implied_asp_usd": round(r["asp"]), "dosage_unit": r["dosage_unit"],
                 "list_price_usd_at_sales_quarter": w, "list_price_source": wsrc,
                 "asp_over_list": round(r["asp"] / w, 3) if w == w and w else ""})
out = pd.DataFrame(rows)
out.to_csv(ROOT / "data/uptake/net_price_asp.csv", index=False)
pd.set_option("display.width", 220)
have = out[out["asp_over_list"] != ""].copy()
have["asp_over_list"] = have["asp_over_list"].astype(float)
print("products with an ASP series:", sorted(out["product"].unique()))
print("products with both ASP and a dated US list price:", sorted(have["product"].unique()))
print(have.groupby("product")["asp_over_list"].agg(["count", "min", "median", "max"]).round(3).to_string())
print()
print(have[["product", "asp_file_quarter", "sales_quarter", "implied_asp_usd", "list_price_usd_at_sales_quarter", "asp_over_list"]].to_string(index=False))
