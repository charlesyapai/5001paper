"""Stage durations and uptake milestones per product (research/methods/time_to_milestone.md; H1).

Inputs : data/cohort/first_in_human.csv, data/cohort/product_cohort.csv, data/uptake/patients_quarterly.csv,
         data/uptake/uptake_summary.csv, data/uptake/eligible_population.csv.
Output : data/uptake/milestones.csv, one row per product with revenue data:
         clinical stage (first-in-human to first approval, years); access-to-first-revenue (months from
         first approval and from FDA approval to the end of the first quarter with revenue); the eligible
         pool used as denominator (geography, family, low and high); cumulative and run-rate penetration
         ranges at the last quarter; months from first approval to a quarter and to half of the pool at
         both ends of the range, censored where not reached; and whether the post-approval stage already
         exceeds the clinical stage (H1) for that product.

Denominator rules. Prevalent-family products (one-time therapies in chronic or congenital disease):
pool(t) = prevalent range + annual incident range x years since first revenue, where an annual range
exists. Annual-family products (oncology cell therapies): run-rate penetration = patients in the last four
quarters / annual eligible; cumulative penetration uses annual eligible x years since first revenue.
Geography: US when the revenue series is US-only or a US split exists; otherwise US plus EU where both
ranges exist, else US with a flag that worldwide revenue is being divided by a US denominator.
Every penetration is a range: low = lower-bound patients / upper-bound pool, high = central patients /
lower-bound pool (conventions 4 and 7).

Label-dated pools (D012). Where data/uptake/label_events.csv holds verified label events for a product
(initial indication, extensions, restrictions; columns product_key, geography, event_date, action add|remove,
indication_key, replaces), the pool is rebuilt quarter by quarter from data/uptake/eligible_population_by_indication.csv:
only the indications in force on each day count, an extension that widens an existing population replaces
its narrower key (MM_2L replaces MM_5L), an added disease adds its own range, and a restriction removes the
key. Inflow is day-weighted within the quarter of a label change. The per-quarter pools are written to
data/uptake/pool_quarterly.csv. Products with no label events keep the static pool (all indications from
launch), so their rows are unchanged.

Run from research/findings:  python3 build_milestones_2026-09-05.py [--label-events PATH]
"""
import re, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
U = ROOT / "data/uptake"
US_ONLY_REVENUE = {"luxturna"}          # Spark and Roche report Luxturna as a US line
US_SPLIT_AVAILABLE = set()              # filled from patients_quarterly regions when a US series is built


def key(name):
    return re.split(r"[\s/(]", str(name).strip())[0].lower()


fih = pd.read_csv(ROOT / "data/cohort/first_in_human.csv", dtype=str).fillna("").set_index("product_key")
coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh["k"] = coh["product"].map(key)
coh = coh.drop_duplicates("k").set_index("k")
pq = pd.read_csv(U / "patients_quarterly.csv", dtype=str).fillna("")
sm = pd.read_csv(U / "uptake_summary.csv", dtype=str).fillna("").set_index("product")
el = pd.read_csv(U / "eligible_population.csv", dtype=str).fillna("") if (U / "eligible_population.csv").exists() else pd.DataFrame()
byk = pd.read_csv(U / "eligible_population_by_indication.csv") if (U / "eligible_population_by_indication.csv").exists() else pd.DataFrame()
LE_PATH = Path(sys.argv[sys.argv.index("--label-events") + 1]) if "--label-events" in sys.argv else U / "label_events.csv"
LE = pd.DataFrame()
if LE_PATH.exists():
    LE = pd.read_csv(LE_PATH, dtype=str).fillna("")
    bad = LE[~LE["status"].isin(["verified-from-source", "derived"])]
    if not bad.empty:
        print(f"label_events: {len(bad)} rows ignored (status not verified or derived): {sorted(set(bad['product_key']))}")
    LE = LE[LE["status"].isin(["verified-from-source", "derived"])].copy()
    LE["date"] = pd.to_datetime(LE["event_date"])
    LE = LE.sort_values("date")
LABEL_DATED = set(LE["product_key"]) if not LE.empty else set()
for c in ["revenue_usd_m", "patients_low", "patients_central", "cumulative_low", "cumulative_central"]:
    pq[c] = pd.to_numeric(pq[c], errors="coerce")
pq["qend"] = pd.to_datetime(pq["period_end"])
if "region" not in pq.columns:
    pq["region"] = "Total"
# a US series is usable only when it covers most of the product's quarters (Novartis and Krystal give a US split for a few quarters only)
_n_us = pq[(pq["region"] == "US") & pq["revenue_usd_m"].notna()].groupby("product").size()
_n_tot = pq[(pq["region"] == "Total") & pq["revenue_usd_m"].notna()].groupby("product").size()
US_SPLIT_AVAILABLE = {p for p, n in _n_us.items() if n >= 8 and n >= 0.7 * _n_tot.get(p, n)}


def rng(product, geo, fam):
    if el.empty:
        return None
    r = el[(el["product_key"] == product) & (el["geography"] == geo) & (el["family"] == fam)]
    if r.empty:
        return None
    r = r.iloc[0]
    lo, hi = r["low"], r["high"]
    if lo == "" or hi == "":
        return None                     # only provisional rows: not used for a figure (rule 3)
    return float(lo), float(hi), int(r["n_verified_or_derived"])


BORROWED = {}   # (product, geo, fam, key) -> product the range was borrowed from


def key_range(product, geo, fam, k):
    """(low, high) for one indication key from verified and derived rows, or None. An eligible population is a
    property of the indication and geography, not of the product: when the product has no row of its own for the
    key, the range of another product with the same key and geography is borrowed (Breyanzi's US large B-cell
    lymphoma flow is Yescarta's) and the borrowing is flagged."""
    if byk.empty:
        return None
    r = byk[(byk["product_key"] == product) & (byk["geography"] == geo) & (byk["family"] == fam) & (byk["indication_key"] == k)]
    if r.empty:
        r = byk[(byk["geography"] == geo) & (byk["family"] == fam) & (byk["indication_key"] == k)]
        if r.empty:
            return None
        BORROWED[(product, geo, fam, k)] = ",".join(sorted(set(r["product_key"])))
        return (float(r["low"].min()), float(r["high"].max()))
    return (float(r["low"].iloc[0]), float(r["high"].iloc[0]))


def keys_in_force(product, geo, date):
    """Indication keys on the label of `product` in `geo` on `date`, from the verified label events."""
    s = set()
    ev = LE[(LE["product_key"] == product) & (LE["geography"] == geo) & (LE["date"] <= date)]
    for _, e in ev.iterrows():
        keys = [x.strip() for x in e["indication_key"].split(";") if x.strip()]   # aliases of one population across source vocabularies
        if e["action"] == "add":
            s.update(keys)
            for old in [x.strip() for x in e["replaces"].split(";") if x.strip()]:
                s.discard(old)
        elif e["action"] == "remove":
            s.difference_update(keys)
    return s


def label_dated_pools(product, q, first_rev_start, us_only):
    """Per-quarter pool for a label-dated product. Returns (geo_label, family, table, flags) where table has one
    row per quarter: keys in force at quarter end, prevalent (lo, hi) at quarter end, day-weighted annual inflow
    (lo, hi) in the quarter, and the cumulative pool (lo, hi) counting inflow from the first revenue quarter."""
    flags = []
    geos = ["US"] if us_only else (["US", "EU"] if not byk[(byk["product_key"] == product) & (byk["geography"] == "EU")].empty else ["US"])
    if geos == ["US"] and not us_only:
        flags.append("worldwide revenue over a US-only denominator (no EU range): penetration overstated")
    has_prev = not byk[(byk["product_key"] == product) & (byk["geography"].isin(geos)) & (byk["family"] == "prevalent")].empty
    fam = "prevalent" if has_prev else "annual"
    missing = {}
    rows = []
    cum_lo = cum_hi = 0.0
    for _, r in q.iterrows():
        qend = r["qend"]
        qstart = qend - pd.DateOffset(months=3) + pd.Timedelta(days=1)
        inflow_lo = inflow_hi = 0.0
        prev_lo = prev_hi = 0.0
        keys_end = set()
        for g in geos:
            # day-weighted inflow: split the quarter at every label event inside it
            cuts = sorted(set([qstart] + [d for d in LE[(LE["product_key"] == product) & (LE["geography"] == g)]["date"] if qstart < d <= qend] + [qend + pd.Timedelta(days=1)]))
            for a, b in zip(cuts[:-1], cuts[1:]):
                frac = (b - a).days / 365.25
                for k in keys_in_force(product, g, a):
                    kr = key_range(product, g, "annual", k)
                    if kr:
                        inflow_lo += kr[0] * frac; inflow_hi += kr[1] * frac
            for k in keys_in_force(product, g, qend):
                keys_end.add(f"{g}:{k}")
                pr = key_range(product, g, "prevalent", k)
                if pr:
                    prev_lo += pr[0]; prev_hi += pr[1]
                if not pr and not key_range(product, g, "annual", k):
                    missing.setdefault(f"{g}:{k}", qend.date())
        counting = pd.notna(first_rev_start) and qend >= first_rev_start
        if counting:
            cum_lo += inflow_lo; cum_hi += inflow_hi
        if fam == "prevalent":
            pool_lo, pool_hi = prev_lo + cum_lo, prev_hi + cum_hi
        else:
            pool_lo, pool_hi = cum_lo, cum_hi
        rows.append({"product": product, "quarter_end": qend.date(), "keys_in_force": " ".join(sorted(keys_end)),
                     "prevalent_low": round(prev_lo), "prevalent_high": round(prev_hi),
                     "inflow_low": round(inflow_lo, 1), "inflow_high": round(inflow_hi, 1),
                     "pool_low": round(pool_lo), "pool_high": round(pool_hi), "counting_inflow": counting})
    for k, d in missing.items():
        flags.append(f"label indication {k} in force has no eligible row (first seen {d}): pool understated")
    for (pk, g, fm, k), src in BORROWED.items():
        if pk == product:
            flags.append(f"{fm} range for {g}:{k} borrowed from {src}")
    return "+".join(geos), fam, pd.DataFrame(rows), flags


def denominator(product):
    """Return (geo_label, family, prevalent_range, annual_range, flags).
    US-only revenue: US ranges. Worldwide revenue: US plus EU for each family where both exist, else US
    alone with a flag. Family: prevalent where a prevalent range exists (one-time therapies), else annual."""
    flags = []
    us_only = product in US_ONLY_REVENUE or product in US_SPLIT_AVAILABLE

    def combine(fam):
        us, eu = rng(product, "US", fam), rng(product, "EU", fam)
        if us_only or not eu:
            if us and not us_only:
                flags.append(f"{fam}: worldwide revenue over a US-only denominator (no EU range): penetration overstated")
            return us, "US"
        if us and eu:
            return (us[0] + eu[0], us[1] + eu[1], min(us[2], eu[2])), "US+EU"
        return None, ""
    prev, gp = combine("prevalent")
    ann, ga = combine("annual")
    if prev:
        return (gp if not ann else f"{gp}/{ga}"), "prevalent", prev, ann, flags
    if ann:
        return ga, "annual", None, ann, flags
    return "", "", None, None, ["no eligible range with a verified or derived row"]


rows = []
pool_tab_all = []
for product, s in sm.iterrows():
    series_region = "US" if product in US_SPLIT_AVAILABLE else "Total"
    q = pq[(pq["product"] == product) & (pq["region"] == series_region)].sort_values("qend")
    if q.empty:
        continue
    c = coh.loc[product] if product in coh.index else None
    f = fih.loc[product] if product in fih.index else None
    fda = pd.to_datetime(c["fda_approval_date"], errors="coerce") if c is not None else pd.NaT
    eu = pd.to_datetime(c["eu_authorisation_date"], errors="coerce") if c is not None else pd.NaT
    first_appr = min([d for d in [fda, eu] if pd.notna(d)], default=pd.NaT)
    fih_date = pd.to_datetime(f["first_in_human_date"], errors="coerce") if f is not None else pd.NaT
    clinical_years = (first_appr - fih_date).days / 365.25 if pd.notna(fih_date) and pd.notna(first_appr) else float("nan")
    rev_q = q[q["revenue_usd_m"] > 0]
    first_rev_end = rev_q["qend"].min() if not rev_q.empty else pd.NaT
    first_rev_start = first_rev_end - pd.DateOffset(months=3) + pd.Timedelta(days=1) if pd.notna(first_rev_end) else pd.NaT
    last = q.iloc[-1]
    last_end = last["qend"]
    if pd.isna(last["cumulative_low"]):
        continue                      # no price, so no patient counts (2026 launches without revenue)
    years_since_first_rev = (last_end - first_rev_start).days / 365.25 if pd.notna(first_rev_start) else float("nan")
    label_dated = product in LABEL_DATED
    if label_dated:
        geo, fam, pool_tab, flags = label_dated_pools(product, q, first_rev_start, product in US_ONLY_REVENUE or product in US_SPLIT_AVAILABLE)
        prev = ann = None
        pool_tab_all.append(pool_tab)
        pool_by_q = {pd.Timestamp(r["quarter_end"]): (r["pool_low"], r["pool_high"]) for _, r in pool_tab.iterrows()}
        last_row_pt = pool_tab.iloc[-1]
        prev = (last_row_pt["prevalent_low"], last_row_pt["prevalent_high"]) if fam == "prevalent" else None
        # annual range reported = the label in force at the last quarter, annualised from the last quarter's inflow
        last_infl = (last_row_pt["inflow_low"], last_row_pt["inflow_high"])
        qdays = (q.iloc[-1]["qend"] - (q.iloc[-1]["qend"] - pd.DateOffset(months=3) + pd.Timedelta(days=1))).days + 1
        ann = (round(last_infl[0] * 365.25 / qdays), round(last_infl[1] * 365.25 / qdays)) if last_infl[1] > 0 else None
    else:
        geo, fam, prev, ann, flags = denominator(product)
        pool_by_q = None
    regimen = s.get("regimen", "one-time") if hasattr(s, "get") else "one-time"
    if regimen == "chronic":
        flags.append("chronic dosing: counts are patient-years at the annual cost; cumulative penetration not meaningful, run-rate shown")

    def pool_at(t_years, end):   # (low, high) eligible pool after t years of sales
        if pool_by_q is not None:
            p = pool_by_q.get(pd.Timestamp(end))
            return p if p and p[1] > 0 else None
        if fam == "prevalent" and prev:
            lo, hi = prev[0], prev[1]
            if ann:
                lo, hi = lo + ann[0] * t_years, hi + ann[1] * t_years
            return lo, hi
        if fam == "annual" and ann:
            return ann[0] * max(t_years, 0.25), ann[1] * max(t_years, 0.25)
        return None

    pool = pool_at(years_since_first_rev, last_end) if geo else None
    cum_low, cum_cen = float(last["cumulative_low"]), float(last["cumulative_central"])
    pen_low = cum_low / pool[1] if pool and regimen != "chronic" else float("nan")
    pen_high = cum_cen / pool[0] if pool and regimen != "chronic" else float("nan")
    last4 = q.tail(4)
    rr_den = (prev or ann) if regimen == "chronic" else ann   # chronic therapies: patient-years on therapy over the prevalent pool
    if label_dated and regimen != "chronic":
        t4 = pool_tab.tail(4)
        rr_den = (t4["inflow_low"].sum(), t4["inflow_high"].sum()) if t4["inflow_high"].sum() > 0 else None   # label in force in each of the last four quarters
    rr_low = last4["patients_low"].sum() / rr_den[1] if rr_den else float("nan")
    rr_high = last4["patients_central"].sum() / rr_den[0] if rr_den else float("nan")

    def time_to(share, conservative):
        """Months from first approval to the first quarter end at which the cumulative count reaches
        the share of the pool. Conservative: lower-bound patients against the upper-bound pool."""
        if not geo or pd.isna(first_appr):
            return "", ""
        for _, r in q.iterrows():
            t = (r["qend"] - first_rev_start).days / 365.25 if pd.notna(first_rev_start) else 0
            p = pool_at(max(t, 0), r["qend"])
            if not p:
                if pool_by_q is not None:
                    continue          # label-dated pool empty in this quarter (no eligible row yet for the indications in force)
                return "", ""
            cnt = float(r["cumulative_low"]) if conservative else float(r["cumulative_central"])
            target = (p[1] if conservative else p[0]) * share
            if cnt >= target:
                return round((r["qend"] - first_appr).days / 30.44, 1), "reached"
        return round((last_end - first_appr).days / 30.44, 1), "censored"

    if regimen == "chronic":
        time_to = lambda share, conservative: ("", "not applicable")
    t25c, t25c_s = time_to(0.25, True)
    t25o, t25o_s = time_to(0.25, False)
    t50c, t50c_s = time_to(0.50, True)
    t50o, t50o_s = time_to(0.50, False)
    followup_years = (last_end - first_appr).days / 365.25 if pd.notna(first_appr) else float("nan")
    understated = any("no eligible row" in f for f in flags)
    if understated and t50o_s == "reached":
        h1 = "not decidable: pool understated (an indication in force has no eligible row), so reaching half of it is not informative"
    elif t50o_s == "reached" and t50c_s == "reached":
        h1 = "post-approval to half of eligible exceeds clinical stage" if (t50c / 12) > clinical_years else "post-approval to half of eligible is shorter than clinical stage"
    elif t50o_s == "censored" and followup_years > clinical_years:
        h1 = "half of eligible not reached and follow-up already exceeds clinical stage: post-approval stage is the longer one"
    elif geo:
        h1 = "not yet decidable: half of eligible not reached at either end of the range and follow-up shorter than clinical stage"
    else:
        h1 = ""
    if series_region == "US":
        flags.append("US revenue series over a US denominator")
    rows.append({"product": product, "platform_class": c["platform_class"] if c is not None else "", "series_region": series_region, "regimen": regimen,
                 "first_in_human": fih_date.date() if pd.notna(fih_date) else "", "first_approval": first_appr.date() if pd.notna(first_appr) else "",
                 "fda_approval": fda.date() if pd.notna(fda) else "", "clinical_stage_years": round(clinical_years, 2) if clinical_years == clinical_years else "",
                 "first_revenue_quarter_end": first_rev_end.date() if pd.notna(first_rev_end) else "",
                 "months_first_approval_to_first_revenue": round((first_rev_end - first_appr).days / 30.44, 1) if pd.notna(first_rev_end) and pd.notna(first_appr) else "",
                 "months_fda_to_first_revenue": round((first_rev_end - fda).days / 30.44, 1) if pd.notna(first_rev_end) and pd.notna(fda) else "",
                 "last_quarter_end": last_end.date(), "follow_up_years_from_first_approval": round(followup_years, 2) if followup_years == followup_years else "",
                 "cumulative_patients_low": round(cum_low), "cumulative_patients_central": round(cum_cen),
                 "denominator_geography": geo, "denominator_family": fam,
                 "prevalent_low": prev[0] if prev else "", "prevalent_high": prev[1] if prev else "",
                 "annual_low": ann[0] if ann else "", "annual_high": ann[1] if ann else "",
                 "pool_at_last_quarter_low": round(pool[0]) if pool else "", "pool_at_last_quarter_high": round(pool[1]) if pool else "",
                 "penetration_low": round(pen_low, 3) if pen_low == pen_low else "", "penetration_high": round(pen_high, 3) if pen_high == pen_high else "",
                 "runrate_penetration_low": round(rr_low, 3) if rr_low == rr_low else "", "runrate_penetration_high": round(rr_high, 3) if rr_high == rr_high else "",
                 "months_to_quarter_of_pool_conservative": t25c, "status_quarter_conservative": t25c_s,
                 "months_to_quarter_of_pool_optimistic": t25o, "status_quarter_optimistic": t25o_s,
                 "months_to_half_of_pool_conservative": t50c, "status_half_conservative": t50c_s,
                 "months_to_half_of_pool_optimistic": t50o, "status_half_optimistic": t50o_s,
                 "h1_reading": h1, "flags": "; ".join(flags),
                 "pool_basis": ("label-dated: " + pool_tab.iloc[-1]["keys_in_force"]) if label_dated else "static: all indications with a range, from launch"})

out = pd.DataFrame(rows)
out.to_csv(U / "milestones.csv", index=False)
if pool_tab_all:
    pd.concat(pool_tab_all, ignore_index=True).to_csv(U / "pool_quarterly.csv", index=False)
    print(f"label-dated pools for {len(pool_tab_all)} products written to pool_quarterly.csv (events from {LE_PATH.name})")
pd.set_option("display.width", 260); pd.set_option("display.max_colwidth", 40)
cols = ["product", "clinical_stage_years", "months_first_approval_to_first_revenue", "follow_up_years_from_first_approval", "cumulative_patients_central",
        "denominator_geography", "denominator_family", "pool_at_last_quarter_low", "pool_at_last_quarter_high", "penetration_low", "penetration_high",
        "runrate_penetration_low", "runrate_penetration_high", "months_to_half_of_pool_optimistic", "status_half_optimistic", "months_to_half_of_pool_conservative", "status_half_conservative"]
print(out[cols].to_string(index=False))
print()
for _, r in out.iterrows():
    if r["h1_reading"]:
        print(f"{r['product']}: {r['h1_reading']}" + (f" [{r['flags']}]" if r["flags"] else ""))
