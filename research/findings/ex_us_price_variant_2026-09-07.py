"""Ex-US price series and the ex-US price variant of the revenue-to-patients conversion (handover item B; extends D011 and F040).

The class factor of 0.76 on US launch list price (F024) stands in for two things: US list-price rises after launch and lower
ex-US prices. Public ex-US prices already sit in the access tables: Germany's G-BA Beschluss states the annual therapy cost
(Jahrestherapiekosten; the negotiated Erstattungsbetrag after the first year), France's CEPS publishes the tarif de
responsabilite, and NICE states the list price in pounds. This script (1) assembles those into a dated ex-US price series per
product, converted at ECB annual reference rates, (2) reports the ex-US to US-launch-list ratio per product and system, and (3)
reprices the Europe revenue of the five CAR-Ts with a Europe split at the German price in force, comparing the patient count
with the class-factor series (Europe revenue over 0.76 x US list).

Inputs : data/access/decisions.csv (F043), data/uptake/patients_quarterly.csv and uptake_summary.csv (F035), ECB reference rates
         (live fetch, saved to data/uptake/raw/ecb_fx_annual.csv; the saved file is used when the API is unreachable)
Outputs: data/uptake/ex_us_price_series.csv        product, system, date in force, price, currency, USD at the year's ECB rate, ratio to US launch list
         data/uptake/ex_us_price_summary.csv       per product: US launch list, first and latest German, French and English prices in USD, ratios
         data/uptake/patients_quarterly_exus_variant.csv   Europe quarters of the five CAR-Ts under both pricings
Run from research/findings:  python3 ex_us_price_variant_2026-09-07.py
"""
import io, re
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
U = ROOT / "data/uptake"
SYN = {"libmeldy": "lenmeldy", "upstaza": "kebilidi", "durveqtix": "beqvez"}


def key(name):
    k = re.split(r"[\s/(]", str(name).strip())[0].lower()
    return SYN.get(k, k)


# ---------------------------------------------------------------- ECB annual reference rates (USD and GBP per EUR)
fx_path = U / "raw/ecb_fx_annual.csv"
try:
    frames = []
    for cur in ["USD", "GBP"]:
        r = requests.get(f"https://data-api.ecb.europa.eu/service/data/EXR/A.{cur}.EUR.SP00.A", params={"format": "csvdata", "startPeriod": "2010"}, timeout=30)
        r.raise_for_status()
        d = pd.read_csv(io.StringIO(r.text))[["CURRENCY", "TIME_PERIOD", "OBS_VALUE"]]
        frames.append(d)
    fx = pd.concat(frames).rename(columns={"CURRENCY": "currency", "TIME_PERIOD": "year", "OBS_VALUE": "per_eur"})
    fx["source"] = "ECB reference exchange rate, annual average (data-api.ecb.europa.eu, EXR.A.<cur>.EUR.SP00.A)"; fx["fetched_date"] = date.today().isoformat()
    fx.to_csv(fx_path, index=False)
    print("ECB rates fetched")
except Exception as e:
    print("ECB fetch failed, using saved file:", e)
    fx = pd.read_csv(fx_path)
fx["year"] = fx["year"].astype(int)
USD_PER_EUR = fx[fx["currency"] == "USD"].set_index("year")["per_eur"].to_dict()
GBP_PER_EUR = fx[fx["currency"] == "GBP"].set_index("year")["per_eur"].to_dict()
last_year = max(USD_PER_EUR)


def to_usd(amount, cur, year):
    y = min(year, last_year)
    if cur == "EUR": return amount * USD_PER_EUR[y]
    if cur == "GBP": return amount / GBP_PER_EUR[y] * USD_PER_EUR[y]
    if cur == "USD": return amount
    return np.nan


# ---------------------------------------------------------------- ex-US prices from the decision tables
dec = pd.read_csv(ROOT / "data/access/decisions.csv", dtype=str).fillna("")
dec = dec[(dec["usable"].str.lower() == "true") & (dec["price_at_decision"] != "")].copy()
dec["decision_dt"] = pd.to_datetime(dec["decision_date"], errors="coerce")
ups = pd.read_csv(U / "uptake_summary.csv", dtype=str).fillna("")
ups["k"] = ups["product"].map(key); ups["list"] = pd.to_numeric(ups["list_price_usd"], errors="coerce")
US_LIST = ups.set_index("k")["list"].to_dict()
rows = []
for _, r in dec.iterrows():
    m = re.match(r"^\s*([\d.]+)(?:\s*-\s*([\d.]+))?", r["price_at_decision"].replace(",", ""))
    if not m or pd.isna(r["decision_dt"]):
        continue
    lo = float(m.group(1)); hi = float(m.group(2)) if m.group(2) else lo
    price = np.sqrt(lo * hi) if hi != lo else lo
    sysm = r["system"]; body = r["body"]
    if sysm == "Germany" and not body.startswith("G-BA"): continue
    if sysm == "France" and not body.startswith("CEPS"): continue
    if sysm == "England" and not body.startswith("NICE"): continue
    if sysm not in ["Germany", "France", "England", "Italy", "Canada", "Australia"]: continue
    usd = to_usd(price, r["price_currency"], r["decision_dt"].year)
    k = r["product_key"]
    rows.append({"product_key": k, "system": sysm, "body": body, "indication_key": r["indication_key"], "date_in_force": r["decision_dt"].date(), "price": price, "currency": r["price_currency"],
                 "price_basis": r["price_basis"], "price_usd_at_ecb_annual_rate": round(usd) if pd.notna(usd) else "", "us_launch_list_usd": US_LIST.get(k, np.nan),
                 "ratio_to_us_launch_list": round(usd / US_LIST[k], 3) if k in US_LIST and pd.notna(US_LIST.get(k)) and pd.notna(usd) and US_LIST[k] > 0 else "",
                 "range_in_source": hi != lo, "source_url": r["source_url"]})
ser = pd.DataFrame(rows).sort_values(["product_key", "system", "date_in_force"]).drop_duplicates(["product_key", "system", "date_in_force", "price"])
ser.to_csv(U / "ex_us_price_series.csv", index=False)

# ---------------------------------------------------------------- summary per product
summ = []
for k, g in ser.groupby("product_key"):
    row = {"product_key": k, "us_launch_list_usd": US_LIST.get(k, "")}
    for s in ["Germany", "France", "England", "Italy", "Canada", "Australia"]:
        gs = g[(g["system"] == s) & (g["ratio_to_us_launch_list"] != "")].sort_values("date_in_force")
        if gs.empty: continue
        row[f"{s}_first_usd"] = gs["price_usd_at_ecb_annual_rate"].iloc[0]; row[f"{s}_first_date"] = gs["date_in_force"].iloc[0]
        row[f"{s}_latest_usd"] = gs["price_usd_at_ecb_annual_rate"].iloc[-1]; row[f"{s}_latest_date"] = gs["date_in_force"].iloc[-1]
        row[f"{s}_ratio_first"] = gs["ratio_to_us_launch_list"].iloc[0]; row[f"{s}_ratio_latest"] = gs["ratio_to_us_launch_list"].iloc[-1]
    summ.append(row)
summ = pd.DataFrame(summ)
summ.to_csv(U / "ex_us_price_summary.csv", index=False)

# ---------------------------------------------------------------- Europe revenue of the CAR-Ts at the German price in force
pq = pd.read_csv(U / "patients_quarterly.csv", dtype=str).fillna("")
for c in ["revenue_usd_m", "patients_central", "list_price_usd", "class_factor"]:
    pq[c] = pd.to_numeric(pq[c], errors="coerce")
pq["qend"] = pd.to_datetime(pq["period_end"])
var_rows = []
for k in ["yescarta", "tecartus", "breyanzi", "abecma", "carvykti"]:
    e = pq[(pq["product"] == k) & (pq["region"] == "Europe")].sort_values("qend")
    de = ser[(ser["product_key"] == k) & (ser["system"] == "Germany") & (ser["price_usd_at_ecb_annual_rate"] != "")].copy()
    de["dt"] = pd.to_datetime(de["date_in_force"]); de = de.sort_values("dt")
    # one German price per date: the lowest stated (the negotiated amount applies across indications)
    de = de.groupby("dt")["price_usd_at_ecb_annual_rate"].min().astype(float)
    fr = ser[(ser["product_key"] == k) & (ser["system"] == "France") & (ser["price_usd_at_ecb_annual_rate"] != "")].copy()
    fr["dt"] = pd.to_datetime(fr["date_in_force"]); fr = fr.sort_values("dt").groupby("dt")["price_usd_at_ecb_annual_rate"].min().astype(float)
    cum_cf = cum_de = 0.0
    for _, q in e.iterrows():
        in_force = de[de.index <= q["qend"]]
        p_de = float(in_force.iloc[-1]) if not in_force.empty else float(de.iloc[0])   # before the first Beschluss: the launch price it states
        fr_force = fr[fr.index <= q["qend"]]; p_fr = float(fr_force.iloc[-1]) if not fr_force.empty else np.nan
        pat_cf = q["patients_central"]; pat_de = q["revenue_usd_m"] * 1e6 / p_de
        cum_cf += pat_cf; cum_de += pat_de
        var_rows.append({"product": k, "quarter": q["quarter"], "europe_revenue_usd_m": q["revenue_usd_m"], "class_factor_price_usd": round(q["list_price_usd"] * q["class_factor"]),
                         "german_price_in_force_usd": round(p_de), "french_tarif_in_force_usd": round(p_fr) if pd.notna(p_fr) else "",
                         "patients_class_factor": round(pat_cf, 1), "patients_german_price": round(pat_de, 1), "cumulative_class_factor": round(cum_cf), "cumulative_german_price": round(cum_de)})
var = pd.DataFrame(var_rows); var.to_csv(U / "patients_quarterly_exus_variant.csv", index=False)

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(f"\nex-US price rows: {len(ser)} for {ser['product_key'].nunique()} products; ECB rates {min(USD_PER_EUR)} to {last_year}")
rt = ser[ser["ratio_to_us_launch_list"] != ""].copy(); rt["ratio"] = rt["ratio_to_us_launch_list"].astype(float)
print("\nratio of ex-US price (USD at ECB annual rate) to US launch list, by system: median, IQR, n rows, n products")
print(rt.groupby("system")["ratio"].agg(median="median", q1=lambda s: s.quantile(0.25), q3=lambda s: s.quantile(0.75), n="size").round(2).join(rt.groupby("system")["product_key"].nunique().rename("products")).to_string())
print("\nfirst and latest German ratio per product")
print(summ[[c for c in summ.columns if c.startswith("product") or c.startswith("Germany_ratio") or c.startswith("France_ratio") or c.startswith("England_ratio")]].to_string(index=False))
print("\nEurope cumulative patients, five CAR-Ts: class factor versus German price in force")
print(var.groupby("product").agg(quarters=("quarter", "size"), cum_class_factor=("cumulative_class_factor", "last"), cum_german_price=("cumulative_german_price", "last")).assign(ratio=lambda d: (d["cum_german_price"] / d["cum_class_factor"]).round(2)).to_string())
