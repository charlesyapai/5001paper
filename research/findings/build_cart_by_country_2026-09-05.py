"""CAR-T patients by country and year with per-capita and per-eligible denominators (topic 03 task 5;
research/methods/cross_country_design.md; convention 10: report both denominators side by side).

Inputs : data/uptake/raw/cart_registry_counts.csv and, when present, raw/cart_country_supplement.csv (same header)
         data/uptake/raw/country_population.csv (country, year, population, source_doc, source_url, status), when present
         data/uptake/eligible_population_by_indication.csv (annual eligible flows per geography and indication)
Output : data/uptake/cart_by_country.csv  one row per country x year x registry x class row ("CAR-T all"): count, count type,
         population, patients per million, CAR-T eligible flow range for the country (sum over the diseases the approved
         CAR-Ts treat, each disease ranged across products and lines), patients per 100 eligible (range), status, source.

Eligible denominator. For each geography, the CAR-T eligible flow is the sum over diseases (LBCL, MM, ALL, MCL, FL, CLL)
of the range across all CAR-T products' verified or derived annual rows for that disease. The pool is the broadest line
of therapy with a row, so per-eligible uptake is a lower bound where only a late-line count exists. England rows serve
the United Kingdom denominator with a flag (England is 84 percent of the UK population).

Run from research/findings:  python3 build_cart_by_country_2026-09-05.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
U = ROOT / "data/uptake"
CART = {"kymriah", "yescarta", "tecartus", "breyanzi", "abecma", "carvykti", "aucatzyl"}
DISEASES = {"LBCL", "MM", "ALL", "MCL", "FL", "CLL"}
COUNTRY = {"United States": "US", "Germany": "Germany", "France": "France", "United Kingdom": "UK", "Italy": "Italy", "Spain": "Spain",
           "Japan": "Japan", "Australia/New Zealand": "Australia", "Netherlands": "Netherlands", "Canada": "Canada",
           "Europe (EBMT survey area)": "EU", "Europe by country": None, "Israel": None, "Switzerland": None}

frames = [pd.read_csv(U / "raw/cart_registry_counts.csv", dtype=str).fillna("")]
sup = U / "raw/cart_country_supplement.csv"
if sup.exists():
    frames.append(pd.read_csv(sup, dtype=str).fillna(""))
reg = pd.concat(frames, ignore_index=True)
reg["count_n"] = pd.to_numeric(reg["count"].str.replace(",", ""), errors="coerce")
reg["rate_10m"] = pd.to_numeric(reg["per_10m_population"], errors="coerce")
reg = reg[(reg["count_n"].notna() | reg["rate_10m"].notna()) & reg["count_type"].isin(["patients", "infusions"]) & (reg["product_or_class"] == "CAR-T all")]
reg["year_n"] = pd.to_numeric(reg["year"], errors="coerce")
reg = reg[reg["year_n"].notna()].copy()
reg["year_n"] = reg["year_n"].astype(int)
reg["geo"] = reg["geography"].map(lambda g: COUNTRY.get(g, g))

pop = pd.DataFrame()
pp = U / "raw/country_population.csv"
if pp.exists():
    pop = pd.read_csv(pp, dtype=str).fillna("")
    pop = pop[pop["status"].isin(["verified-from-source", "derived"])].copy()
    pop["year_n"] = pd.to_numeric(pop["year"], errors="coerce")
    pop["pop_n"] = pd.to_numeric(pop["population"].str.replace(",", ""), errors="coerce")
    pop["geo"] = pop["country"].map(lambda g: COUNTRY.get(g, g))
    pop = pop.dropna(subset=["year_n", "pop_n"]).drop_duplicates(["geo", "year_n"]).set_index(["geo", "year_n"])["pop_n"]

byk = pd.read_csv(U / "eligible_population_by_indication.csv")
byk = byk[byk["product_key"].isin(CART) & (byk["family"] == "annual") & byk["disease"].isin(DISEASES)]
elig = {}
for g, grp in byk.groupby("geography"):
    lo = hi = 0.0
    parts = []
    for dz, d in grp.groupby("disease"):
        lo += d["low"].min(); hi += d["high"].max()
        parts.append(f"{dz}:{d['low'].min():g}-{d['high'].max():g}")
    elig[g] = (lo, hi, "; ".join(parts))
if "England" in elig and "UK" not in elig:
    lo, hi, parts = elig["England"]
    elig["UK"] = (lo, hi, parts + " (England rows used for the UK: denominator understated by about 16 percent)")

rows = []
for _, r in reg.sort_values(["geo", "year_n", "registry"]).iterrows():
    g, y = r["geo"], r["year_n"]
    if g is None or (isinstance(g, float) and g != g):
        continue
    p = pop.get((g, y)) if not pop.empty else None
    e = elig.get(g)
    has_p = p is not None and p == p
    per_m = round(r["count_n"] / p * 1e6, 2) if has_p and r["count_n"] == r["count_n"] else (round(r["rate_10m"] / 10, 2) if r["rate_10m"] == r["rate_10m"] else "")
    rows.append({"country": g, "year": y, "registry": r["registry"], "count": int(r["count_n"]) if r["count_n"] == r["count_n"] else "", "count_type": r["count_type"],
                 "population": int(p) if has_p else "", "per_million": per_m,
                 "per_million_basis": "count / World Bank population" if has_p and r["count_n"] == r["count_n"] else ("EBMT published rate per 10 million / 10" if r["rate_10m"] == r["rate_10m"] else ""),
                 "eligible_low": round(e[0]) if e else "", "eligible_high": round(e[1]) if e else "", "eligible_by_disease": e[2] if e else "",
                 "per_100_eligible_low": round(r["count_n"] / e[1] * 100, 1) if e and e[1] and r["count_n"] == r["count_n"] else "",
                 "per_100_eligible_high": round(r["count_n"] / e[0] * 100, 1) if e and e[0] and r["count_n"] == r["count_n"] else "",
                 "status": r["status"], "source_doc": r["source_doc"][:120], "source_url": r["source_url"], "notes": r["notes"][:200]})
out = pd.DataFrame(rows)
out.to_csv(U / "cart_by_country.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 40)
print(f"rows: {len(out)}; countries: {sorted(out['country'].unique())}; population file: {'yes' if not pop.empty else 'no'}; supplement: {'yes' if sup.exists() else 'no'}")
print("eligible flows per geography:", {k: (round(v[0]), round(v[1])) for k, v in elig.items()})
v = out[(out["status"] == "verified-from-source") & (out["count"] != "")]
show = v.sort_values(["year", "country"])[["country", "year", "registry", "count", "count_type", "per_million", "per_100_eligible_low", "per_100_eligible_high"]]
print(show[show["year"] >= 2023].to_string(index=False))
# 2024 ranking on both denominators: one row per country (national registry preferred over the EBMT survey where both exist; patients over infusions)
y24 = v[(v["year"] == 2024)].copy()
y24["pref"] = (y24["registry"] == "EBMT activity survey").astype(int) * 2 + (y24["count_type"] == "infusions").astype(int)   # national registry, patients first
y24 = y24.sort_values("pref").drop_duplicates("country")
y24 = y24[y24["per_million"] != ""]
y24["per_million"] = pd.to_numeric(y24["per_million"])
print("\n2024 ranking, patients per million (one row per country):")
print(y24.sort_values("per_million", ascending=False)[["country", "registry", "count", "per_million", "per_100_eligible_low", "per_100_eligible_high"]].to_string(index=False))
both = y24[y24["per_100_eligible_low"] != ""].copy()
if len(both) >= 3:
    both["mid"] = (pd.to_numeric(both["per_100_eligible_low"]) + pd.to_numeric(both["per_100_eligible_high"])) / 2
    print("\nSpearman rank correlation, per million vs per eligible (midpoint), countries with both:", len(both), round(both["per_million"].rank().corr(both["mid"].rank()), 2))
    print(both[["country", "per_million", "mid"]].sort_values("per_million", ascending=False).to_string(index=False))
