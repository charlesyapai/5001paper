"""Product-level net-price variant of the patient counts (D011 consequence; topic 03 open question).

The main series (build_uptake_series_2026-09-04.py) divides all revenue by the US launch list price and applies
one class factor of 0.76 (F024). The CMS ASP files show that for US CAR-T the net price equals the wholesale
acquisition cost in force (F030), so for the products with an ASP series this variant prices US revenue at the
price in force in each quarter (implied ASP where the CMS file gives it, else the WAC for that year from the
disclosure tables, else the launch price) with no factor, and ex-US revenue (Total minus US) at the launch
list price times the class factor as before. Products without an ASP series or without a US split are not
changed; they are listed so the scope of the variant is explicit.

Inputs : data/uptake/patients_quarterly.csv, data/uptake/net_price_asp.csv, data/uptake/raw/*_disclosures.csv
         (list_price rows), data/uptake/raw/verification_hemgenix_tecartus.csv (Tecartus WAC 2022 to 2025, F029),
         data/uptake/pilot_calibration.csv and the patients_cumulative disclosure rows (disclosed counts).
Outputs: data/uptake/patients_quarterly_variant.csv  per product and quarter: US revenue, price in force and its
                                                     basis, US patients at that price, ex-US patients at the
                                                     calibrated factor, total variant, cumulative variant, and the
                                                     main series' cumulative central for comparison
         data/uptake/net_price_variant_summary.csv   per product: cumulative central (main) and variant, ratio,
                                                     and the disclosed counts with both implied-over-disclosed ratios

Run from research/findings:  python3 net_price_variant_2026-09-05.py
"""
import glob, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
U = ROOT / "data/uptake"
FACTOR = 0.76
pq = pd.read_csv(U / "patients_quarterly.csv", dtype=str).fillna("")
for c in ["revenue_usd_m", "list_price_usd", "patients_central", "cumulative_central", "cumulative_low"]:
    pq[c] = pd.to_numeric(pq[c], errors="coerce")
asp = pd.read_csv(U / "net_price_asp.csv", dtype=str).fillna("")
asp["implied_asp_usd"] = pd.to_numeric(asp["implied_asp_usd"], errors="coerce")
asp_by = {(r["product"], r["sales_quarter"]): r["implied_asp_usd"] for _, r in asp.iterrows() if r["implied_asp_usd"] == r["implied_asp_usd"]}
ASP_PRODUCTS = set(asp["product"])


def key(name):
    return re.split(r"[\s/(]", str(name).strip())[0].lower()


# WAC by year from the disclosure tables (US rows priced per treatment in USD), plus the Tecartus verification rows
frames = []
for f in glob.glob(str(U / "raw/*_disclosures.csv")):
    d = pd.read_csv(f, dtype=str).fillna("")
    if "record_type" in d.columns:
        frames.append(d[d["record_type"] == "list_price"])
ver = pd.read_csv(U / "raw/verification_hemgenix_tecartus.csv", dtype=str).fillna("")
ver = ver[(ver.iloc[:, 1] == "Tecartus") & (ver.iloc[:, 2] == "list_price")].copy()
ver.columns = ["task"] + list(ver.columns[1:])
ver = ver.rename(columns={ver.columns[1]: "product", ver.columns[2]: "record_type", ver.columns[3]: "as_of_date", ver.columns[4]: "region", ver.columns[5]: "value", ver.columns[6]: "unit"})
frames.append(ver[["product", "record_type", "as_of_date", "region", "value", "unit"]])
lp = pd.concat(frames, ignore_index=True)
lp = lp[lp["region"].str.contains("US", case=False) & lp["unit"].str.contains("USD", case=False) & lp["unit"].str.contains("treatment|course|patient|WAC|wholesale", case=False)].copy()
lp["product_key"] = lp["product"].map(key)
lp["year"] = lp["as_of_date"].str[:4]
lp["price"] = pd.to_numeric(lp["value"].str.replace(",", "").str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
lp = lp[lp["price"].notna()]
wac = lp.groupby(["product_key", "year"])["price"].max().to_dict()   # the WAC in force at year end where several rows exist


def price_in_force(product, quarter, launch):
    """(price, basis) for a US sales quarter: implied ASP, else WAC for the year (carried forward), else launch."""
    if (product, quarter) in asp_by:
        return asp_by[(product, quarter)], "implied ASP (CMS payment limit / 1.06)"
    y = int(quarter[:4])
    for yy in range(y, 2009, -1):
        if (product, str(yy)) in wac:
            return wac[(product, str(yy))], f"WAC {yy}" + (" carried forward" if yy != y else "")
    return launch, "launch list price"


rows, summ = [], []
for product in sorted(pq["product"].unique()):
    tot = pq[(pq["product"] == product) & (pq["region"] == "Total")].sort_values("quarter")
    us = pq[(pq["product"] == product) & (pq["region"] == "US")].set_index("quarter")
    if tot.empty:
        continue
    launch = tot["list_price_usd"].iloc[0]
    in_scope = product in ASP_PRODUCTS and len(us) >= 8 and launch == launch
    cum_var = 0.0
    for _, r in tot.iterrows():
        q = r["quarter"]
        rev_tot = r["revenue_usd_m"]
        rev_us = us.loc[q, "revenue_usd_m"] if q in us.index else float("nan")
        if not in_scope or rev_tot != rev_tot:
            p_var = r["patients_central"]
            price, basis = launch, "not in scope: class factor central kept"
            p_us = p_ex = float("nan")
        else:
            rev_us = rev_us if rev_us == rev_us else 0.0
            price, basis = price_in_force(product, q, launch)
            p_us = rev_us * 1e6 / price
            p_ex = max(rev_tot - rev_us, 0.0) * 1e6 / (launch * FACTOR)
            p_var = p_us + p_ex
        cum_var += p_var if p_var == p_var else 0.0
        rows.append({"product": product, "quarter": q, "revenue_total_usd_m": rev_tot, "revenue_us_usd_m": rev_us if rev_us == rev_us else "",
                     "launch_list_price_usd": launch, "us_price_in_force_usd": round(price) if price == price else "", "price_basis": basis,
                     "patients_us_at_price_in_force": round(p_us, 1) if p_us == p_us else "", "patients_ex_us_at_factor": round(p_ex, 1) if p_ex == p_ex else "",
                     "patients_variant": round(p_var, 1) if p_var == p_var else "", "cumulative_variant": round(cum_var, 1),
                     "patients_central_main": r["patients_central"], "cumulative_central_main": r["cumulative_central"], "in_scope": in_scope})
    last = tot.iloc[-1]
    summ.append({"product": product, "in_scope": in_scope, "us_quarters": len(us), "asp_quarters": sum(1 for (p, q) in asp_by if p == product),
                 "wac_years": " ".join(sorted(y for (p, y) in wac if p == product)),
                 "last_quarter": last["quarter"], "cumulative_central_main": round(last["cumulative_central"]) if last["cumulative_central"] == last["cumulative_central"] else "",
                 "cumulative_variant": round(cum_var), "variant_over_main": round(cum_var / last["cumulative_central"], 3) if in_scope and last["cumulative_central"] else ""})

var = pd.DataFrame(rows)
var.to_csv(U / "patients_quarterly_variant.csv", index=False)
sm = pd.DataFrame(summ)

# Disclosed counts: the pilot calibration points (Kite pooled Yescarta plus Tecartus) and patients_cumulative rows for in-scope products
cal = pd.read_csv(U / "pilot_calibration.csv", dtype=str).fillna("")
checks = []
for _, c in cal.iterrows():
    prods = c["numerator_products"].split("+")
    if not all(p in set(sm[sm["in_scope"]]["product"]) for p in prods):
        continue
    end = pd.Period(pd.Timestamp(c["last_period_end"]), freq="Q")
    v = var[var["product"].isin(prods)]
    v = v[v["quarter"].map(lambda q: pd.Period(q, freq="Q") <= end)]
    main = v.groupby("product")["cumulative_central_main"].max().sum()
    variant = v.groupby("product")["cumulative_variant"].max().sum()
    disclosed = float(c["disclosed_patients"])
    checks.append({"products": c["numerator_products"], "as_of_date": c["as_of_date"], "through_quarter": str(end), "disclosed_patients": int(disclosed),
                   "implied_main_class_factor": round(main), "main_over_disclosed": round(main / disclosed, 2),
                   "implied_variant": round(variant), "variant_over_disclosed": round(variant / disclosed, 2), "disclosure": c["reason"][:120]})
chk = pd.DataFrame(checks)
sm.to_csv(U / "net_price_variant_summary.csv", index=False)
chk.to_csv(U / "net_price_variant_checks.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print("in scope (ASP series and a US split):", sorted(sm[sm["in_scope"]]["product"]))
print(sm[sm["in_scope"]][["product", "us_quarters", "asp_quarters", "wac_years", "last_quarter", "cumulative_central_main", "cumulative_variant", "variant_over_main"]].to_string(index=False))
print("\nprice basis used for in-scope US quarters:", var[var["in_scope"]]["price_basis"].str.split(" carried").str[0].value_counts().to_dict())
print("\nagainst disclosed counts:")
print(chk.to_string(index=False))
