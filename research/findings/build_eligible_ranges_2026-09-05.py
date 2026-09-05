"""Eligible-population ranges per product and geography (topic 03 task 3; convention 7: always a range).

Inputs : data/uptake/raw/eligible_*.csv from the retrieval agents (one row per estimate per source),
         plus the eligible_population rows in data/uptake/raw/luxturna_disclosures.csv (older format).
Outputs: data/uptake/eligible_population_rows.csv   every estimate, normalised (product_key, geography,
                                                    family, low, point, high, status, source)
         data/uptake/eligible_population_by_indication.csv  range per product x geography x family x
                                                    indication_key over verified and derived rows, for the
                                                    label-dated pools (D012)
         data/uptake/eligible_population.csv        one row per product x geography x family with the
                                                    range over verified and derived rows, the range
                                                    including provisional rows, counts and sources.

Family. "annual" = new eligible patients per year (incident flow, or a gatekeeper's per-year count);
"prevalent" = patients alive who meet the label criteria at a point in time (the stock a one-time
therapy can treat). Rows whose unit does not say which are classed "unspecified" and listed for review;
they enter neither family range. Rates and label rows are kept in the rows file but not ranged.

Run from research/findings:  python3 build_eligible_ranges_2026-09-05.py
"""
import glob, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/uptake/raw"
OUT = ROOT / "data/uptake"
SYN = {"libmeldy": "lenmeldy", "upstaza": "kebilidi", "durveqtix": "beqvez"}
GEO = [("US", r"^(us|u\.s\.|usa|united states)"), ("England", r"england|nhs england|nice"), ("UK", r"^(uk|united kingdom|great britain|scotland|wales)"),
       ("Germany", r"german"), ("France", r"france|french"), ("Italy", r"ital"), ("Spain", r"spain|spanish"), ("Japan", r"japan"),
       ("Canada", r"canada"), ("Australia", r"australia"), ("Gulf", r"gulf|saudi|bahrain|uae|emirates|qatar|kuwait"),
       ("EU5", r"eu5|eu-5|big five"), ("EU", r"^(eu|eea)\b|europe|european union"), ("global", r"global|world|worldwide")]


def key(name):
    k = re.split(r"[\s/(]", str(name).strip())[0].lower()
    return SYN.get(k, k)


def geo(g):
    s = str(g).strip().lower()
    hits = [name for name, pat in GEO if re.search(pat, s)]
    if len(hits) > 1 and "England" not in hits[1:] and not (hits == ["UK", "England"] or hits == ["England", "UK"]):
        return "multi: " + "+".join(hits)     # a combined region such as "US, Europe and Japan" is not a single denominator
    return hits[0] if hits else "other: " + str(g).strip()[:30]


def num(x):
    x = str(x).replace(",", "").strip()
    m = re.search(r"-?\d+\.?\d*", x)
    return float(m.group()) if m else float("nan")


def family(mt, unit, notes):
    """Explicit unit words first, then the agent's measure_type, then the notes."""
    u = str(unit).lower()
    if re.search(r"per year|per annum|annual|each year|/yr|a year|per licence|per 5 years|births|incident|newly", u):
        return "annual"
    if re.search(r"prevalen|living with|alive|pool|stock|^people|people eligible|individuals|addressable|have vision loss", u):
        return "prevalent"
    if mt == "annual_incident_eligible":
        return "annual"
    if mt == "prevalent_eligible":
        return "prevalent"
    n = f"{u} {str(notes).lower()}"
    if re.search(r"per year|per annum|annual|each year|gkv|target population|incident|initiating|new patients", n):
        return "annual"   # G-BA target-population counts are stated per year
    if re.search(r"prevalen|living with|alive|pool|stock|patients with|addressable", n):
        return "prevalent"
    return "unspecified"


frames = []
for f in sorted(glob.glob(str(RAW / "eligible_*.csv"))):
    d = pd.read_csv(f, dtype=str).fillna("")
    d["source_file"] = Path(f).name
    frames.append(d)
# older format: Luxturna eligible_population rows in the pilot disclosure file
lux = pd.read_csv(RAW / "luxturna_disclosures.csv", dtype=str).fillna("")
lux = lux[lux["record_type"] == "eligible_population"].copy()
if not lux.empty:
    rng = lux["value"].str.extract(r"(\d[\d,]*)\s*-\s*(\d[\d,]*)")
    lux2 = pd.DataFrame({"product": lux["product"], "indication_key": "RPE65", "indication_label": "biallelic RPE65 mutation-associated retinal dystrophy",
                         "geography": lux["region"], "measure_type": lux["unit"].map(lambda u: "prevalence_rate" if "1 in" in str(u) or "prevalence" in str(u) else ("gatekeeper_eligible" if "eligible" in str(u) else "company_addressable")),
                         "value_low": rng[0].fillna(""), "value_point": lux["value"].where(rng[0].isna(), ""), "value_high": rng[1].fillna(""),
                         "unit": lux["unit"], "estimate_year": lux["as_of_date"].str[:4], "as_of_date": lux["as_of_date"], "verbatim": lux["verbatim"],
                         "source_doc": lux["source_doc"], "source_url": lux["source_url"], "status": lux["status"], "notes": lux["notes"], "source_file": "luxturna_disclosures.csv"})
    lux2.loc[lux2["value_point"].str.contains("1 in", na=False), "value_point"] = ""
    frames.append(lux2)
rows = pd.concat(frames, ignore_index=True)
rows["product_key"] = rows["product"].map(key)
rows["geography_norm"] = rows["geography"].map(geo)
for c in ["value_low", "value_point", "value_high"]:
    rows[c + "_n"] = rows[c].map(num)
rows["family"] = [family(m, u, n) for m, u, n in zip(rows["measure_type"], rows["unit"], rows["notes"])]
countable = rows["measure_type"].isin(["annual_incident_eligible", "prevalent_eligible", "company_addressable", "gatekeeper_eligible"])
rows["lo"] = rows["value_low_n"].where(rows["value_low_n"].notna(), rows["value_point_n"])
rows["hi"] = rows["value_high_n"].where(rows["value_high_n"].notna(), rows["value_point_n"])
rows["has_number"] = countable & rows["lo"].notna() & rows["hi"].notna()
rows["grade"] = rows["status"].map(lambda s: "A" if s in ("verified-from-source", "derived") else ("B" if s == "provisional-from-snippet" else "X"))
# Documented exclusions: rows whose number is not the label population (data/uptake/eligible_overrides.csv)
ov_path = OUT / "eligible_overrides.csv"
rows["excluded"] = ""
if ov_path.exists():
    ov = pd.read_csv(ov_path, dtype=str).fillna("")
    for _, o in ov.iterrows():
        m = (rows["product_key"] == o["product_key"]) & (rows["geography_norm"] == o["geography"]) & (rows["measure_type"] == o["measure_type"]) \
            & (rows["lo"] == float(o["value_low"])) & (rows["hi"] == float(o["value_high"]))
        if o["action"] == "exclude":
            rows.loc[m, "excluded"] = o["reason"]
        elif o["action"].startswith("key="):
            rows.loc[m, "indication_key"] = o["action"].split("=", 1)[1]
            rows.loc[m, "notes"] = rows.loc[m, "notes"] + " | indication key set by override: " + o["reason"]
        elif o["action"].startswith("family="):
            rows.loc[m, "family"] = o["action"].split("=", 1)[1]
            rows.loc[m, "notes"] = rows.loc[m, "notes"] + " | family set by override: " + o["reason"]
rows["has_number"] = rows["has_number"] & (rows["excluded"] == "")
rows.to_csv(OUT / "eligible_population_rows.csv", index=False)

out = []
use = rows[rows["has_number"] & rows["family"].isin(["annual", "prevalent"])].copy()
use["disease"] = use["indication_key"].str.split("_").str[0].str.upper()
for (pk, g, fam), grp in use.groupby(["product_key", "geography_norm", "family"]):
    # per disease: the range across sources and lines of therapy; across distinct diseases: the sum
    def agg(sub):
        lo = hi = 0.0
        parts = []
        for dz, d in sub.groupby("disease"):
            lo += d["lo"].min(); hi += d["hi"].max()
            parts.append(f"{dz}:{d['lo'].min():g}-{d['hi'].max():g}")
        return lo, hi, "; ".join(parts)
    a = grp[grp["grade"] == "A"]
    ab = grp[grp["grade"].isin(["A", "B"])]
    la, ha, pa = agg(a) if not a.empty else ("", "", "")
    lb, hb, pb = agg(ab)
    out.append({"product_key": pk, "geography": g, "family": fam, "n_estimates": len(ab), "n_verified_or_derived": len(a),
                "low": la, "high": ha, "low_incl_provisional": lb, "high_incl_provisional": hb,
                "by_disease": pa or pb, "n_diseases": ab["disease"].nunique(),
                "estimate_years": ",".join(sorted(set(ab["estimate_year"].astype(str)))),
                "measure_types": ",".join(sorted(set(ab["measure_type"]))),
                "indications": ",".join(sorted(set(ab["indication_key"]))),
                "sources": " | ".join(sorted(set(ab["source_doc"].str[:60])))[:600]})
el = pd.DataFrame(out).sort_values(["product_key", "geography", "family"])
el.to_csv(OUT / "eligible_population.csv", index=False)

# Per-indication ranges (verified and derived rows only) for the label-dated pools in build_milestones
# (data/uptake/label_events.csv, D012): one row per product x geography x family x indication_key.
byk = []
for (pk, g, fam, k), grp in use[use["grade"] == "A"].groupby(["product_key", "geography_norm", "family", "indication_key"]):
    byk.append({"product_key": pk, "geography": g, "family": fam, "indication_key": k, "disease": grp["disease"].iloc[0],
                "low": grp["lo"].min(), "high": grp["hi"].max(), "n_verified_or_derived": len(grp),
                "estimate_years": ",".join(sorted(set(grp["estimate_year"].astype(str)))),
                "measure_types": ",".join(sorted(set(grp["measure_type"]))),
                "sources": " | ".join(sorted(set(grp["source_doc"].str[:60])))[:600]})
pd.DataFrame(byk).sort_values(["product_key", "geography", "family", "indication_key"]).to_csv(OUT / "eligible_population_by_indication.csv", index=False)

pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 50)
print(f"rows: {len(rows)} from {rows['source_file'].nunique()} files; countable with a number: {int(rows['has_number'].sum())}; products: {rows['product_key'].nunique()}")
print("family of countable rows:", rows[rows["has_number"]]["family"].value_counts().to_dict())
unspec = rows[rows["has_number"] & (rows["family"] == "unspecified")]
if not unspec.empty:
    print("\nunspecified family (review the unit):")
    print(unspec[["product_key", "geography_norm", "measure_type", "lo", "hi", "unit"]].to_string(index=False))
print("\nranges (US and England first):")
show = el[el["geography"].isin(["US", "England", "UK", "Germany", "France", "EU", "global"])]
print(show[["product_key", "geography", "family", "n_estimates", "n_verified_or_derived", "low", "high", "low_incl_provisional", "high_incl_provisional"]].to_string(index=False))
coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh = coh[~coh["notes"].str.contains("out of scope")]
missing = sorted(set(coh["product"].map(key)) - set(el[el["geography"] == "US"]["product_key"]))
print("\ncohort products with no US range yet:", missing)
