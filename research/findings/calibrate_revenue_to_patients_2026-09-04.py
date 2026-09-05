"""Revenue-to-patients calibration pilot (research/methods/revenue_to_patients.md).

Inputs : <dir>/<product>_revenue.csv and <dir>/<product>_disclosures.csv from the retrieval
         agents (raw, every row they found).
Outputs: data/uptake/pilot_revenue.csv          every revenue row, with parsed period start and end
         data/uptake/pilot_disclosures.csv      every disclosure row
         data/uptake/pilot_calibration.csv      one row per curated calibration point:
                                                cumulative revenue to that date, implied patients at
                                                list price, ratio to disclosed, implied net-to-list,
                                                and whether the 30 percent gate passes at list price
                                                and after class-level calibration.

Period handling. Sources report quarters, halves and fiscal years, sometimes all three. Each
row is parsed to a (start, end) interval and the finest non-overlapping set is kept, so an
annual row is used only where no quarterly or half-year rows cover it. CSL (Hemgenix) reports
to 30 June; everything else is calendar.

Calibration points. The raw disclosure files contain in-period counts, regional subsets, free
managed-access doses and funnel metrics (referrals, initiations, cell collections). Only
cumulative, global counts of treated or infused patients are calibration targets. They are
listed explicitly in CALIBRATION_POINTS below with the reason each was chosen, so the choice is
auditable. Yescarta milestones after 2019 pool Yescarta and Tecartus, so Tecartus revenue is
added to the numerator for those points.

Run from research/findings:  python3 calibrate_revenue_to_patients_2026-09-04.py <dir>
"""
import sys, re, glob
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/uptake"
OUT.mkdir(exist_ok=True)
src = Path(sys.argv[1])
GATE = 0.30

FY_END_MONTH = {"hemgenix": 6}          # CSL fiscal year ends 30 June
FX_TO_USD = {"CHF": 1.12, "AUD": 0.66, "EUR": 1.08}   # rough; only used where the source gave no USD

# Curated calibration targets: (product, as_of_date, disclosed_patients, numerator products, reason)
CALIBRATION_POINTS = [
    ("casgevy", "2025-06-30", 29, ["casgevy"], "cumulative infusions since launch, Vertex Q2 2025 release; revenue recognised at infusion"),
    ("casgevy", "2025-09-30", 39, ["casgevy"], "cumulative infusions since launch, Vertex Q3 2025 release"),
    ("casgevy", "2025-12-31", 69, ["casgevy"], "derived: 64 infusions in 2025 (Vertex FY2025) + 5 in 2024 (29 cumulative at Q2 2025 minus 16 in Q2 minus 8 in Q1 2025)"),
    ("hemgenix", "2024-06-30", 12, ["hemgenix"], "12 patients in the 12 months to June 2024, FiercePharma snippet; provisional"),
    ("hemgenix", "2026-06-30", 100, ["hemgenix"], "'more than 100 people' treated commercially worldwide, CSL letter 2026-07-28; floor; matched to revenue through FY2026 (30 June 2026)"),
    ("yescarta", "2019-12-31", 2500, ["yescarta"], "about 2,500 commercial patients, Yescarta only, Cryoport 10-K"),
    ("yescarta", "2022-12-11", 11000, ["yescarta", "tecartus"], "more than 11,000 patients, all Kite CAR-T (Yescarta + Tecartus), Gilead release; floor"),
    ("yescarta", "2024-01-30", 17700, ["yescarta", "tecartus"], "more than 17,700 patients, all Kite CAR-T, Kite release; floor"),
    ("yescarta", "2025-01-10", 25000, ["yescarta", "tecartus"], "more than 25,000 patients, all Kite CAR-T, Kite statement; floor"),
    ("zolgensma", "2021-06-18", 1200, ["zolgensma"], "more than 1,200 patients worldwide incl. trials and managed access, Novartis; floor"),
    ("zolgensma", "2022-06-17", 2000, ["zolgensma"], "more than 2,000 patients worldwide incl. trials and managed access, Novartis; floor"),
    ("zolgensma", "2023-03-20", 3000, ["zolgensma"], "more than 3,000 patients worldwide, Novartis; floor"),
    ("zolgensma", "2024-04-23", 4000, ["zolgensma"], "more than 4,000 patients worldwide, Novartis; floor"),
    ("zolgensma", "2025-01-31", 4500, ["zolgensma"], "more than 4,500 patients worldwide, Novartis; floor"),
    ("zolgensma", "2025-10-28", 5000, ["zolgensma"], "more than 5,000 patients worldwide, Novartis; floor"),
    ("zolgensma", "2026-07-21", 5500, ["zolgensma"], "more than 5,500 patients worldwide since launch, Novartis; floor; revenue through 2026Q2"),
    ("luxturna", "2018-12-31", 75, ["luxturna"], "75 vials shipped in the US in 2018 (Spark FY2018 10-K); unit is vials, priced at USD 425,000 per vial; Spark disclosed no patient counts after 2018"),
]
# Per-point price override where the disclosed unit is not a per-patient treatment.
PRICE_OVERRIDE = {("luxturna", "2018-12-31"): 425_000}

# US list price at launch per product (USD per treatment); overridden by the disclosure file if present.
LIST_PRICE = {"casgevy": 2_200_000, "hemgenix": 3_500_000, "yescarta": 373_000, "tecartus": 373_000,
              "zolgensma": 2_125_000, "luxturna": 850_000}


def parse_period(period, product):
    """Return (start, end) timestamps for a period string, or (NaT, NaT).
    Accepts 2021Q3, 2019H1, H1 2022, FY2022, 2022, FY2026H1, and the same with a
    parenthetical suffix. Nine-month and 'CY' (calendar-year royalty proxy) periods are rejected."""
    p = period.strip().upper().split("(")[0].strip()
    if p.startswith("CY") or re.search(r"\b9M\b", p):
        return pd.NaT, pd.NaT
    fy_end = FY_END_MONTH.get(product, 12)
    m = re.match(r"^(\d{4})\s*Q([1-4])$", p)
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        end = pd.Timestamp(y, 3 * q, 1) + pd.offsets.MonthEnd(0)
        return (end + pd.Timedelta(days=1)) - pd.DateOffset(months=3), end
    m = re.match(r"^(?:FY)?(\d{4})\s*H([12])$", p) or re.match(r"^H([12])\s*(\d{4})$", p)
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
        d["product_key"] = Path(f).name.split("_")[0]
        frames.append(d)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


rev = load("*_revenue.csv")
dis = load("*_disclosures.csv")

rev["revenue_musd"] = pd.to_numeric(rev["revenue_musd"].str.replace(",", ""), errors="coerce")
rev["currency"] = rev["currency"].str.upper().str.strip()
rev["fx_applied"] = rev["currency"].map(lambda c: 1.0 if c in ("USD", "") else FX_TO_USD.get(c, float("nan")))
rev["revenue_usd_m"] = rev["revenue_musd"] * rev["fx_applied"]
se = [parse_period(p, k) for p, k in zip(rev["period"], rev["product_key"])]
rev["period_start"] = [s for s, _ in se]
rev["period_end"] = [e for _, e in se]
# Luxturna is reported by Spark and Roche as a US-only product line, so its US rows are the totals.
TOTAL_REGION = {"luxturna": r"^US$|United States"}
rev["is_total"] = rev["region"].str.contains(r"total|world|global", case=False) | (rev["region"].str.strip() == "")
for k, pat in TOTAL_REGION.items():
    rev.loc[(rev["product_key"] == k) & rev["region"].str.contains(pat, case=False), "is_total"] = True
rev["is_proxy"] = rev["region"].str.contains(r"royalt|receivable|proxy", case=False) | rev["notes"].str.contains(r"^PROXY", case=False)
rev["usable"] = rev["is_total"] & ~rev["is_proxy"] & rev["revenue_usd_m"].notna() & rev["period_end"].notna() \
    & ~rev["status"].isin(["not-disclosed", "gap"])


def canonical_series(product):
    """Finest non-overlapping set of usable total-revenue intervals for a product."""
    r = rev[(rev["product_key"] == product) & rev["usable"]].copy()
    r["length"] = (r["period_end"] - r["period_start"]).dt.days
    # prefer verified over derived at equal length
    r["rank"] = r["status"].map(lambda s: 0 if s == "verified-from-source" else 1)
    r = r.sort_values(["length", "rank"])
    kept = []
    for _, row in r.iterrows():
        if all(row["period_end"] < k["period_start"] or row["period_start"] > k["period_end"] for k in kept):
            kept.append(row)
    return pd.DataFrame(kept).sort_values("period_start") if kept else pd.DataFrame()


def cumulative_to(products, date):
    total, n, last = 0.0, 0, pd.NaT
    for p in products:
        s = canonical_series(p)
        if s.empty:
            continue
        s = s[s["period_end"] <= date]
        total += s["revenue_usd_m"].sum()
        n += len(s)
        if not s.empty:
            last = max(last, s["period_end"].max()) if pd.notna(last) else s["period_end"].max()
    return total, n, last


def list_price(product):
    g = dis[(dis["product_key"] == product) & (dis["record_type"] == "list_price")].copy()
    g["v"] = pd.to_numeric(g["value"].str.replace(",", "").str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
    g["d"] = pd.to_datetime(g["as_of_date"], errors="coerce")
    g = g[g["region"].str.contains(r"US|United States", case=False) & g["v"].notna()].sort_values("d")
    if not g.empty:
        v = float(g["v"].iloc[0])
        return v * 1e6 if v < 100 else v   # tolerate values recorded in millions
    return LIST_PRICE.get(product, float("nan"))


rows = []
for product, as_of, disclosed, nums, reason in CALIBRATION_POINTS:
    if as_of is None:
        g = dis[(dis["product_key"] == product) & (dis["record_type"] == "patients_cumulative")
                & dis["region"].str.contains(r"world|global", case=False)].copy()
        if g.empty:
            continue
        g["v"] = pd.to_numeric(g["value"].str.replace(",", "").str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
        g["d"] = pd.to_datetime(g["as_of_date"], errors="coerce")
        g = g[g["v"].notna() & g["d"].notna()]
        pts = [(product, d.date().isoformat(), v, nums, f"{reason}: {vb[:80]}") for d, v, vb in zip(g["d"], g["v"], g["verbatim"])]
    else:
        pts = [(product, as_of, disclosed, nums, reason)]
    for product, as_of, disclosed, nums, reason in pts:
        date = pd.Timestamp(as_of)
        cum, n, last = cumulative_to(nums, date)
        price = PRICE_OVERRIDE.get((product, as_of), list_price(product))
        implied = cum * 1e6 / price
        ratio = implied / disclosed
        rows.append({
            "product": product, "as_of_date": as_of, "disclosed_patients": disclosed,
            "numerator_products": "+".join(nums), "cumulative_revenue_usd_m": round(cum, 1),
            "periods_used": n, "last_period_end": last.date().isoformat() if pd.notna(last) else "",
            "list_price_usd": price, "implied_patients_at_list": round(implied),
            "implied_over_disclosed": round(ratio, 2), "implied_net_to_list": round(1 / ratio, 2) if ratio else "",
            "gate_pass_at_list": abs(ratio - 1) <= GATE, "reason": reason,
        })

cal = pd.DataFrame(rows)
if not cal.empty:
    # Class-level calibration: one net-to-list factor across all products, the median of the
    # per-point implied factors. Products with disclosed counts that include free or trial
    # doses (Zolgensma) will sit low; floors ("more than X") bias the ratio up.
    factor = cal["implied_over_disclosed"].median()
    cal["class_factor_applied"] = round(factor, 2)
    cal["implied_patients_calibrated"] = (cal["implied_patients_at_list"] / factor).round()
    cal["calibrated_over_disclosed"] = (cal["implied_patients_calibrated"] / cal["disclosed_patients"]).round(2)
    cal["gate_pass_calibrated"] = (cal["calibrated_over_disclosed"] - 1).abs() <= GATE

rev.to_csv(OUT / "pilot_revenue.csv", index=False)
dis.to_csv(OUT / "pilot_disclosures.csv", index=False)
cal.to_csv(OUT / "pilot_calibration.csv", index=False)

pd.set_option("display.width", 220)
print("revenue rows:", len(rev), "| usable totals:", int(rev["usable"].sum()), "| status:", rev["status"].value_counts().to_dict())
for p in sorted(rev["product_key"].unique()):
    s = canonical_series(p)
    if not s.empty:
        print(f"  {p}: {len(s)} periods {s['period_start'].min().date()} to {s['period_end'].max().date()}, cumulative USD {s['revenue_usd_m'].sum():,.0f}m")
print("disclosure rows:", len(dis))
print()
cols = ["product", "as_of_date", "disclosed_patients", "numerator_products", "cumulative_revenue_usd_m", "list_price_usd",
        "implied_patients_at_list", "implied_over_disclosed", "gate_pass_at_list", "implied_patients_calibrated", "calibrated_over_disclosed", "gate_pass_calibrated"]
print(cal[cols].to_string(index=False) if not cal.empty else "no calibration rows")
if not cal.empty:
    print(f"\nclass net-to-list factor (median implied/disclosed): {cal['implied_over_disclosed'].median():.2f}")
    print("per product median ratio at list:", cal.groupby("product")["implied_over_disclosed"].median().round(2).to_dict())
    print(f"gate at list: {int(cal['gate_pass_at_list'].sum())}/{len(cal)} points; after class calibration: {int(cal['gate_pass_calibrated'].sum())}/{len(cal)}")
