"""Quarterly patients-treated series from product revenue (research/methods/revenue_to_patients.md).

Inputs : <dir>/<product>_revenue.csv and <dir>/<product>_disclosures.csv from the retrieval agents
         (same raw tables as calibrate_revenue_to_patients_2026-09-04.py), data/cohort/product_cohort.csv.
Outputs: data/uptake/patients_quarterly.csv   one row per product per calendar quarter from first sale:
                                              revenue (allocated evenly across quarters where only a
                                              half-year or annual figure exists, flagged), patients at
                                              US launch list price (lower bound) and at the class net-to-list
                                              factor (central), cumulative both ways, coverage flags.
         data/uptake/uptake_summary.csv       one row per product: approval dates, first-revenue quarter,
                                              months from approval to first revenue, quarters observed,
                                              cumulative revenue and patients, latest disclosed count.

Price convention. Patients are computed at the US wholesale acquisition cost at launch, held constant,
because the class factor (F024) was calibrated on that basis: the factor absorbs gross-to-net, later
list-price increases, ex-US prices and non-revenue doses together. A quarterly net price from the CMS
ASP file can replace this once that series is in hand.

Run from research/findings:  python3 build_uptake_series_2026-09-04.py <raw dir> [class_factor]
"""
import sys, re, glob
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/uptake"
src = Path(sys.argv[1])
FACTOR = float(sys.argv[2]) if len(sys.argv) > 2 else 0.76      # F024 class net-to-list factor
CUTOFF = pd.Timestamp("2026-06-30")                               # last complete quarter at 2026-09-04

FY_END_MONTH = {"hemgenix": 6, "ryoncil": 6}                      # CSL and Mesoblast fiscal years end 30 June
FX_TO_USD = {"CHF": 1.12, "AUD": 0.66, "EUR": 1.08, "GBP": 1.27, "JPY": 0.0067}  # rough; only where no USD figure
SYNONYM = {"libmeldy": "lenmeldy", "upstaza": "kebilidi", "durveqtix": "beqvez", "onasemnogene": "zolgensma"}
# Launch US list price per treatment course, used only when the disclosure file has no usable US row.
FALLBACK_PRICE = {"casgevy": 2_200_000, "hemgenix": 3_500_000, "yescarta": 373_000, "tecartus": 373_000,
                  "zolgensma": 2_125_000, "luxturna": 850_000, "kymriah": 475_000, "breyanzi": 410_300,
                  "abecma": 419_500, "carvykti": 465_000, "zynteglo": 2_800_000, "skysona": 3_000_000,
                  "lyfgenia": 3_100_000, "elevidys": 3_200_000, "roctavian": 2_900_000, "vyjuvek": 631_000,
                  "aucatzyl": 525_000, "tecelra": 727_000, "kebilidi": 3_800_000, "lenmeldy": 4_250_000,
                  "zevaskyn": 3_100_000, "amtagvi": 515_000, "imlygic": 65_000, "ryoncil": 1_552_000,
                  "omisirge": 338_000, "provenge": 93_000, "beqvez": 3_500_000, "papzimeos": 1_000_000}
# Vyjuvek and Adstiladrin fallbacks are annual costs per patient (chronic dosing), not one-time prices.


def product_key(name):
    k = re.split(r"[\s/(]", str(name).strip())[0].lower()
    return SYNONYM.get(k, k)


def parse_period(period, product):
    """(start, end) for 2021Q3, 2019H1, H1 2022, FY2022, 2022, FY2026H1, with optional parenthetical.
    Nine-month, calendar-year-proxy ('CY') and multi-year ranges are rejected."""
    p = str(period).strip().upper().split("(")[0].strip()
    if p.startswith("CY") or re.search(r"\b9M\b", p) or re.match(r"^\d{4}\s*-\s*\d{4}$", p):
        return pd.NaT, pd.NaT
    fy_end = FY_END_MONTH.get(product, 12)
    m = re.match(r"^(\d{4})\s*Q([1-4])$", p) or re.match(r"^Q([1-4])\s*(\d{4})$", p)
    if m:
        a, b = m.group(1), m.group(2)
        y, q = (int(a), int(b)) if len(a) == 4 else (int(b), int(a))
        end = pd.Timestamp(y, 3 * q, 1) + pd.offsets.MonthEnd(0)
        return (end + pd.Timedelta(days=1)) - pd.DateOffset(months=3), end
    m = re.match(r"^(?:FY)?(\d{4})\s*H([12])$", p) or re.match(r"^H([12])\s*(?:FY)?(\d{4})$", p)
    if m:
        a, b = m.group(1), m.group(2)
        y, h = (int(a), int(b)) if len(a) == 4 else (int(b), int(a))
        if fy_end == 12:
            end = pd.Timestamp(y, 6, 30) if h == 1 else pd.Timestamp(y, 12, 31)
        else:
            end = pd.Timestamp(y - 1, 12, 31) if h == 1 else pd.Timestamp(y, 6, 30)
        return (end + pd.Timedelta(days=1)) - pd.DateOffset(months=6), end
    m = re.match(r"^(?:FY)?\s*(\d{4})\s*(?:FY)?$", p)
    if m:
        y = int(m.group(1))
        end = pd.Timestamp(y, 12, 31) if fy_end == 12 else pd.Timestamp(y, 6, 30)
        return (end + pd.Timedelta(days=1)) - pd.DateOffset(years=1), end
    return pd.NaT, pd.NaT


def load(pattern):
    frames = []
    for f in sorted(glob.glob(str(src / pattern))):
        d = pd.read_csv(f, dtype=str).fillna("")
        d["source_file"] = Path(f).name
        frames.append(d)
    d = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    d["product_key"] = d["product"].map(product_key)
    return d


rev = load("*_revenue.csv")
dis = load("*_disclosures.csv")
for col in ["region", "notes", "status", "currency", "source_doc", "source_url"]:
    if col not in rev.columns:
        rev[col] = ""
rev["revenue_musd"] = pd.to_numeric(rev["revenue_musd"].astype(str).str.replace(",", ""), errors="coerce")
rev["currency"] = rev["currency"].str.upper().str.strip()
rev["fx_applied"] = rev["currency"].map(lambda c: 1.0 if c in ("USD", "") else FX_TO_USD.get(c, float("nan")))
rev["revenue_usd_m"] = rev["revenue_musd"] * rev["fx_applied"]
se = [parse_period(p, k) for p, k in zip(rev["period"], rev["product_key"])]
rev["period_start"] = [s for s, _ in se]
rev["period_end"] = [e for _, e in se]
TOTAL_REGION = {"luxturna": r"^US$|United States"}   # Spark and Roche report Luxturna as a US-only line
rev["is_total"] = rev["region"].str.contains(r"total|world|global", case=False) | (rev["region"].str.strip() == "")
for k, pat in TOTAL_REGION.items():
    rev.loc[(rev["product_key"] == k) & rev["region"].str.contains(pat, case=False), "is_total"] = True
rev["is_proxy"] = rev["region"].str.contains(r"royalt|receivable|proxy", case=False) | rev["notes"].str.contains(r"^PROXY", case=False)
rev["region_group"] = "Total"
rev.loc[rev["region"].str.contains(r"^US$|^U\.S\.|United States|^US\b(?! and)", case=False) & ~rev["is_total"], "region_group"] = "US"
rev.loc[rev["region"].str.contains(r"^Europe$|^EU$|European|^Ex-US$|International", case=False) & ~rev["is_total"], "region_group"] = "Europe"
rev.loc[rev["region"].str.contains(r"^Other|Rest of world|RoW", case=False) & ~rev["is_total"], "region_group"] = "Other"
rev["usable"] = rev["region_group"].isin(["Total", "US", "Europe"]) & ~rev["is_proxy"] & rev["revenue_usd_m"].notna() & rev["period_end"].notna() \
    & ~rev["status"].isin(["not-disclosed", "gap"])


def canonical_series(product, group="Total"):
    """Finest non-overlapping set of usable revenue intervals for one region group; verified rows beat derived ones."""
    r = rev[(rev["product_key"] == product) & rev["usable"] & (rev["region_group"] == group)].copy()
    r["length"] = (r["period_end"] - r["period_start"]).dt.days
    r["rank"] = r["status"].map(lambda s: 0 if s == "verified-from-source" else 1)
    r = r.sort_values(["length", "rank"])
    kept, rejected = [], []
    for _, row in r.iterrows():
        if all(row["period_end"] < k["period_start"] or row["period_start"] > k["period_end"] for k in kept):
            kept.append(row)
        else:
            rejected.append(row)
    # Remainders: a full-year or half-year row that overlaps finer kept rows yields the uncovered
    # quarters as one derived row (for example Roche's FY minus H1 gives H2), provided the uncovered
    # quarters are contiguous and the remainder is not negative.
    def qset(a, b):
        return set(pd.period_range(a, b, freq="Q"))
    for row in sorted(rejected, key=lambda x: x["length"]):
        inside = [k for k in kept if k["period_start"] >= row["period_start"] and k["period_end"] <= row["period_end"]]
        uncovered = qset(row["period_start"], row["period_end"]) - set().union(*[qset(k["period_start"], k["period_end"]) for k in inside]) if inside else set()
        if not inside or not uncovered:
            continue
        qs = sorted(uncovered)
        contiguous = all((qs[i + 1] - qs[i]).n == 1 for i in range(len(qs) - 1))
        remainder = row["revenue_usd_m"] - sum(k["revenue_usd_m"] for k in inside)
        # a remainder that falls before the finer rows is pre-launch rounding noise, not revenue
        after = qs[0] > max(pd.Period(k["period_end"], freq="Q") for k in inside)
        if contiguous and after and remainder >= 0.5:
            d = row.copy()
            d["period_start"], d["period_end"] = qs[0].start_time.normalize(), qs[-1].end_time.normalize()
            d["revenue_usd_m"] = remainder
            d["status"] = "derived"
            d["period"] = f"{row['period']} minus {' + '.join(k['period'] for k in inside)}"
            d["notes"] = f"remainder of {row['period']} after subtracting {[k['period'] for k in inside]}; " + str(row["notes"])
            kept.append(d)
    return pd.DataFrame(kept).sort_values("period_start") if kept else pd.DataFrame()


# Billing units per course where companies quote a per-unit price (source: label dosing; CMS ASP dosage descriptions)
PER_COURSE_UNITS = {"luxturna": 2, "ryoncil": 8, "provenge": 3}
# Dosing regimen: one-time (default), course (a fixed series of infusions priced per course) or chronic (repeated
# dosing; revenue / annual cost gives patient-years on therapy, not patients)
REGIMEN = {"vyjuvek": "chronic", "adstiladrin": "chronic", "imlygic": "course", "provenge": "course", "ryoncil": "course"}


def list_price(product):
    """US launch list price per treatment course from the disclosure file, else the fallback table.
    Rows priced per treatment, patient or course are preferred; a per-eye, per-vial, per-infusion or
    per-dose row is multiplied by PER_COURSE_UNITS. Returns (price, source, note)."""
    g = dis[(dis["product_key"] == product) & (dis["record_type"] == "list_price")].copy() if not dis.empty else pd.DataFrame()
    if not g.empty:
        g["v"] = pd.to_numeric(g["value"].astype(str).str.replace(",", "").str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
        g["d"] = pd.to_datetime(g["as_of_date"].astype(str).str[:10], errors="coerce")
        g = g[g["region"].str.contains(r"^US|United States|U\.S\.", case=False) & g["v"].notna() & (g["v"] > 0)
              & ~g["unit"].str.contains(r"payment limit|ASP|per year|annual", case=False)]
        g["per_course"] = g["unit"].str.contains(r"treatment|patient|course", case=False) & ~g["unit"].str.contains(r"per (?:eye|vial|dose|infusion)", case=False)
        g["rank"] = g["status"].map(lambda s: 0 if s == "verified-from-source" else 1)
        g = g.sort_values(["per_course", "d", "rank"], ascending=[False, True, True])
        if not g.empty:
            row = g.iloc[0]
            v = float(row["v"])
            v = v * 1e6 if v < 100 else v
            note = f"{row['status']}; {row['unit'][:40]}; {row['source_doc'][:60]}"
            if not row["per_course"]:
                n = PER_COURSE_UNITS.get(product)
                if n is None:
                    return float("nan"), row["source_url"], note + "; per-unit price with unknown units per course"
                return n * v, row["source_url"], note + f"; per-unit price x {n} units per course"
            return v, row["source_url"], note
    return FALLBACK_PRICE.get(product, float("nan")), "", "fallback table in build_uptake_series_2026-09-04.py (launch WAC from memory; replace with a sourced row)"


def quarters_between(start, end):
    q = pd.period_range(start, end, freq="Q")
    return list(q)


cohort = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
cohort["product_key"] = cohort["product"].map(product_key)
cohort = cohort.drop_duplicates("product_key").set_index("product_key")

rows, summary = [], []
us_cum = {}
for product in sorted(rev["product_key"].unique()):
  for group in ["US", "Europe", "Total"]:
    s = canonical_series(product, group)
    us_as_total = False
    if s.empty and group == "Total":
        s = canonical_series(product, "US")          # bluebird and Sarepta report a US-only business: the US series is the total
        us_as_total = not s.empty
    if s.empty:
        continue
    price, price_src, price_note = list_price(product)
    if not (price == price) or not price:
        price = float("nan")
        price_note = "NO PRICE: patients not computed; add a US list_price row to the disclosure file"
    r0 = lambda x: round(x) if x == x else ""
    r1 = lambda x: round(x, 1) if x == x else ""
    # allocate each canonical interval evenly across the calendar quarters it covers
    alloc = {}
    for _, r in s.iterrows():
        qs = quarters_between(r["period_start"], r["period_end"])
        for q in qs:
            alloc[q] = {"revenue_usd_m": r["revenue_usd_m"] / len(qs), "allocated": len(qs) > 1,
                        "period_as_reported": r["period"], "revenue_status": r["status"],
                        "source_doc": r["source_doc"], "source_url": r["source_url"], "fx": r["fx_applied"]}
    first_q, last_q = min(alloc), min(max(alloc), pd.Period(CUTOFF, freq="Q"))
    cum_low = cum_central = 0.0
    first_rev_q = None
    for q in pd.period_range(first_q, last_q, freq="Q"):
        a = alloc.get(q)
        if a is None:
            rows.append({"product": product, "region": group, "quarter": str(q), "period_start": q.start_time.date(), "period_end": q.end_time.date(),
                         "revenue_usd_m": "", "period_as_reported": "", "revenue_status": "not-covered", "allocated": "",
                         "list_price_usd": price, "class_factor": FACTOR, "patients_low": "", "patients_central": "",
                         "cumulative_low": round(cum_low, 1), "cumulative_central": round(cum_central, 1),
                         "coverage": "gap: no total revenue row covers this quarter", "source_doc": "", "source_url": ""})
            continue
        p_low = a["revenue_usd_m"] * 1e6 / price
        p_cen = p_low / FACTOR
        cum_low += p_low
        cum_central += p_cen
        if first_rev_q is None and a["revenue_usd_m"] > 0:
            first_rev_q = q
        rows.append({"product": product, "region": group, "quarter": str(q), "period_start": q.start_time.date(), "period_end": q.end_time.date(),
                     "regimen": REGIMEN.get(product, "one-time"), "revenue_usd_m": round(a["revenue_usd_m"], 2), "period_as_reported": a["period_as_reported"],
                     "revenue_status": a["revenue_status"], "allocated": a["allocated"],
                     "list_price_usd": price, "class_factor": FACTOR,
                     "patients_low": r1(p_low), "patients_central": r1(p_cen),
                     "cumulative_low": r1(cum_low), "cumulative_central": r1(cum_central),
                     "coverage": "allocated evenly from a longer reporting period" if a["allocated"] else "quarterly as reported",
                     "source_doc": a["source_doc"], "source_url": a["source_url"]})
    if group != "Total":
        us_cum[(product, group)] = (r0(cum_low), r0(cum_central), str(last_q))
        continue
    c = cohort.loc[product] if product in cohort.index else None
    fda = pd.to_datetime(c["fda_approval_date"], errors="coerce") if c is not None else pd.NaT
    eu = pd.to_datetime(c["eu_authorisation_date"], errors="coerce") if c is not None else pd.NaT
    first_any = min([d for d in [fda, eu] if pd.notna(d)], default=pd.NaT)
    frq_end = first_rev_q.end_time if first_rev_q is not None else pd.NaT
    latest = ""
    if not dis.empty:
        g = dis[(dis["product_key"] == product) & dis["record_type"].str.startswith("patients") & dis["region"].str.contains(r"global|world|total|^$", case=False)].copy()
        g["v"] = pd.to_numeric(g["value"].astype(str).str.replace(",", "").str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
        g["pref"] = g["record_type"].map(lambda t: 0 if t == "patients_cumulative" else 1)
        g = g[g["v"].notna() & g["status"].isin(["verified-from-source", "provisional-from-snippet", "derived"])].sort_values(["as_of_date", "pref", "v"], ascending=[True, False, True])
        if not g.empty:
            latest = f"{int(g.iloc[-1]['v'])} ({g.iloc[-1]['record_type']}, {g.iloc[-1]['as_of_date']}, {g.iloc[-1]['status']})"
    summary.append({"product": product, "cohort_product": c["product"] if c is not None else "", "platform_class": c["platform_class"] if c is not None else "",
                    "regimen": REGIMEN.get(product, "one-time"), "patient_unit": {"chronic": "patient-years at annual cost", "course": "courses"}.get(REGIMEN.get(product, "one-time"), "patients"),
                    "total_series_basis": "US series used as total (US-only reporting)" if us_as_total else "Total as reported",
                    "fda_approval_date": fda.date() if pd.notna(fda) else "", "eu_authorisation_date": eu.date() if pd.notna(eu) else "",
                    "first_revenue_quarter": str(first_rev_q) if first_rev_q is not None else "",
                    "months_fda_to_first_revenue_qend": round((frq_end - fda).days / 30.44, 1) if pd.notna(frq_end) and pd.notna(fda) else "",
                    "months_first_approval_to_first_revenue_qend": round((frq_end - first_any).days / 30.44, 1) if pd.notna(frq_end) and pd.notna(first_any) else "",
                    "quarters_with_revenue": sum(1 for q in alloc if q <= last_q), "quarters_allocated": sum(1 for q, a in alloc.items() if a["allocated"] and q <= last_q),
                    "last_quarter": str(last_q), "cumulative_revenue_usd_m": round(sum(a["revenue_usd_m"] for q, a in alloc.items() if q <= last_q), 1),
                    "list_price_usd": price, "price_source": price_src, "price_note": price_note,
                    "cumulative_patients_low": r0(cum_low), "cumulative_patients_central": r0(cum_central),
                    "latest_disclosed_count": latest,
                    "us_cumulative_low": us_cum.get((product, "US"), ("", "", ""))[0], "us_cumulative_central": us_cum.get((product, "US"), ("", "", ""))[1],
                    "europe_cumulative_central": us_cum.get((product, "Europe"), ("", "", ""))[1]})

pq = pd.DataFrame(rows)
sm = pd.DataFrame(summary)
pq.to_csv(OUT / "patients_quarterly.csv", index=False)
sm.to_csv(OUT / "uptake_summary.csv", index=False)
pd.set_option("display.width", 250)
print(f"products: {len(sm)} | quarterly rows: {len(pq)} ({pq['region'].value_counts().to_dict()}) | class factor {FACTOR}")
print(sm[["product", "fda_approval_date", "first_revenue_quarter", "months_fda_to_first_revenue_qend", "quarters_with_revenue",
          "last_quarter", "cumulative_revenue_usd_m", "list_price_usd", "cumulative_patients_low", "cumulative_patients_central", "us_cumulative_central", "latest_disclosed_count"]].to_string(index=False))
