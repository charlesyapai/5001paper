"""Landscape projection 2027 to 2036, version 2 (topic 05; D014 supersedes the D013 implementation of 6 September 2026).

What changed from project_landscape_2026-09-06.py, item by item of the methods review:
  A1 pipeline unit   constructs (data/projection/pipeline_constructs.csv, F048) instead of one programme per sponsor; the
                     primary variant keeps constructs with at least one US or European trial site; approved constructs leave
                     the pipeline at approval. Four variants are backcast uncalibrated and reported.
  A2 transitions     time to approval is drawn from the class distribution conditional on the time already elapsed since the
                     construct's first trial (left truncation); phase-3 constructs draw from the cohort's own phase-3-start-to-
                     approval distribution (phase_durations.csv); no assumed remaining-share ranges. Success still uses the S06
                     transition rates (F027) as Beta draws.
  calibration        if the primary backcast still misses the record, the correction is estimated as a parameter with its own
                     uncertainty (Gamma posterior of realised over predicted per class), not fixed.
  A4 access          each approval draws its funding time per system from the Aalen-Johansen cumulative incidence (F047),
                     which carries the never-funded mass; the never-submitted and withdrawn products are in the denominator.
  A3 diffusion       Bass curves with per-product (shrunk) parameters drawn per product (F049); CAR-T as a class on the
                     registry-total fits per region with bootstrap tuples; rest of world explicit.
  A5 uncertainty     every fixed assumption carries a range and is drawn per run (probabilistic sensitivity); a one-way tornado
                     over each assumption at its low and high value; a sampling-only run with assumptions held at base; a
                     validation table in ISPOR-SMDM terms.
  A6 capacity        US centres from the FACT directory (171) with the US and European growth rates as the range.

Outputs under data/projection/: approvals_projection.csv, access_projection.csv, patients_projection.csv, capacity_projection.csv,
projection_parameters.csv, sensitivity_oneway.csv, sensitivity_structural.csv, validation.csv.
Run from research/findings:  python3 project_landscape_2026-09-07.py [n_runs]   (production 4000; the tornado uses 1000 per arm)
"""
import re, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/projection"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
NOW = 2026.68   # 5 September 2026
YEARS = list(range(2027, 2037))
CLASSES = ["CAR-T", "AAV", "lentiviral ex vivo", "CRISPR ex vivo", "in vivo editing and LNP"]
PTRANS = {"CAR-T": ([0.263, 0.387, 0.750], 402), "gene therapy": ([0.550, 0.492, 0.684], 195)}   # S06 (F027)
PGROUP = {"CAR-T": "CAR-T", "AAV": "gene therapy", "lentiviral ex vivo": "gene therapy", "CRISPR ex vivo": "gene therapy", "in vivo editing and LNP": "gene therapy"}
DUR_DONOR = {"CRISPR ex vivo": "AAV", "in vivo editing and LNP": "AAV"}
SYSTEMS = ["United States", "Germany", "Italy", "England", "France", "Canada", "Australia"]
EU_SYS = ["Germany", "Italy", "England", "France"]


def key(name):
    return re.split(r"[\s/(]", str(name).strip())[0].lower()


def cls_of(p):
    p = str(p)
    if "CAR-T" in p: return "CAR-T"
    if p.startswith("AAV"): return "AAV"
    if "lentiviral" in p or "retroviral" in p: return "lentiviral ex vivo"
    if "CRISPR" in p: return "CRISPR ex vivo"
    return "other"


def bass(t, p, q):
    t = np.maximum(t, 0.0); e = np.exp(-(p + q) * t)
    return (1 - e) / (1 + (q / p) * e)


# ================================================================ inputs
pc = pd.read_csv(OUT / "pipeline_constructs.csv", dtype=str).fillna("")
for c in ["first_start", "phase3_start", "phase_active_2026", "phase_by_2019", "first_start_by_2019", "phase3_start_by_2019"]:
    pc[c] = pd.to_numeric(pc[c], errors="coerce")
pc["has_us_or_eu_site"] = pc["has_us_or_eu_site"].astype(str).str.lower().eq("true")
pc["approval_dt"] = pd.to_datetime(pc["approval_date"], errors="coerce")
pdur = pd.read_csv(OUT / "phase_durations.csv", dtype=str).fillna("")
coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh = coh[~coh["notes"].str.contains("out of scope")].copy()
coh["k"] = coh["product"].map(key); coh["cls"] = coh["platform_class"].map(cls_of)
coh["first_approval"] = [min([d for d in [pd.to_datetime(a, errors="coerce"), pd.to_datetime(b, errors="coerce")] if pd.notna(d)], default=pd.NaT)
                         for a, b in zip(coh["fda_approval_date"], coh["eu_authorisation_date"])]
fih = pd.read_csv(ROOT / "data/cohort/first_in_human.csv", dtype=str).fillna("")
fih["years"] = pd.to_numeric(fih["years_fih_to_first_approval"], errors="coerce"); fih["cls"] = fih["platform_class"].map(cls_of)
curves = pd.read_csv(ROOT / "data/access/access_survival_curves.csv")
ssum = pd.read_csv(ROOT / "data/access/access_survival_summary.csv")
tte = pd.read_csv(ROOT / "data/access/access_time_to_event.csv")
bf = pd.read_csv(OUT / "diffusion_bass_fits.csv", dtype=str).fillna("")
for c in ["p_innovation", "q_imitation", "c_ceiling_share", "m_patients"]:
    bf[c] = pd.to_numeric(bf[c], errors="coerce")
ms = pd.read_csv(ROOT / "data/uptake/milestones.csv", dtype=str).fillna("")
for c in ["pool_at_last_quarter_low", "pool_at_last_quarter_high", "annual_low", "annual_high", "prevalent_low", "prevalent_high"]:
    ms[c] = pd.to_numeric(ms[c], errors="coerce")
ms["cls"] = ms["platform_class"].map(cls_of)
pq = pd.read_csv(ROOT / "data/uptake/patients_quarterly.csv", dtype=str).fillna("")
pq["patients_central"] = pd.to_numeric(pq["patients_central"], errors="coerce"); pq["revenue_usd_m"] = pd.to_numeric(pq["revenue_usd_m"], errors="coerce")
pq["year"] = pq["period_end"].str[:4].astype(int)
ups = pd.read_csv(ROOT / "data/uptake/uptake_summary.csv", dtype=str).fillna("")
cbc = pd.read_csv(ROOT / "data/uptake/cart_by_country.csv", dtype=str).fillna("")
sup = pd.read_csv(ROOT / "data/uptake/raw/cart_country_supplement.csv", dtype=str).fillna("")

# ---------------------------------------------------------------- derived inputs that do not change across runs
dur = {}
for c in CLASSES:
    donor = DUR_DONOR.get(c, c)
    y = fih[(fih["cls"] == donor) & fih["years"].notna() & (fih["years"] > 0)]["years"].values
    dur[c] = (float(np.log(y).mean()), float(max(np.log(y).std(ddof=1), 0.15)), len(y), donor)
y3 = pd.to_numeric(pdur["years_phase3_start_to_approval"], errors="coerce")
y3 = y3[(y3 > 0) & pdur["platform_class"].map(cls_of).isin(CLASSES)].values
DUR3 = (float(np.log(y3).mean()), float(np.log(y3).std(ddof=1)), len(y3))
real = coh[(coh["first_approval"] >= "2020-01-01") & (coh["first_approval"] <= "2025-12-31") & (coh["genetic_modification"] == "yes")]
real_by = real.groupby([real["first_approval"].dt.year, "cls"]).size().unstack(fill_value=0).reindex(range(2020, 2026)).fillna(0)
REAL = {c: int(real_by[c].sum()) if c in real_by.columns else 0 for c in CLASSES}
REAL_YEAR = {y: int(real_by.loc[y, [c for c in CLASSES if c in real_by.columns]].sum()) for y in range(2020, 2026)}
OTHER_RATE = float((real["cls"] == "other").sum()) / 6.0
# entry rate per class: first phase-1 (or 1/2) construct start per sponsor-construct, 2021 to 2025, in the primary variant
def entry_rate(variant):
    f = pc[pc["has_us_or_eu_site"]] if "US or EU" in variant else pc
    if variant.startswith("sponsor"):
        f = f.groupby(["cls", "sponsor"], as_index=False)["first_start"].min()
    return {c: float(((f["cls"] == c) & f["first_start"].between(2021, 2025.99)).sum()) / 5.0 for c in CLASSES}


VARIANTS = ["sponsor, US or EU site", "construct, US or EU site", "sponsor, all sites", "construct, all sites"]
ENTRY = {v: entry_rate(v) for v in VARIANTS}
# access curves (primary endpoint): CIF on a monthly grid to 120 months, per system
CIF = {}
for s in SYSTEMS:
    g = curves[(curves["endpoint"] == "primary") & (curves["system"] == s)].sort_values("months")
    CIF[s] = g["cif_funded"].values
CIF_SD = {s: float((ssum[(ssum["endpoint"] == "primary") & (ssum["system"] == s)]["cif_funded_60m_p90"].iloc[0] - ssum[(ssum["endpoint"] == "primary") & (ssum["system"] == s)]["cif_funded_60m_p10"].iloc[0]) / 2.56) for s in SYSTEMS}
FUNDED_TODAY = {s: int(((tte["endpoint"] == "primary") & (tte["system"] == s) & (tte["event"] == "funded")).sum()) for s in SYSTEMS}
BEST_SYS = "Australia"   # fastest observed funding times (median 3.7 months); the compressed scenario uses its curve rescaled to fund every approval
CIF_FAST = CIF["Australia"] / CIF["Australia"][-1]
EXUS_SYS = "Germany"     # ex-US funding time for a new product's European uptake: the system that funds most
# diffusion tuples
CART_TUPLES = bf[(bf["family"] == "CAR-T") & (bf["level"] == "product (shrunk)")][["p_innovation", "q_imitation", "c_ceiling_share"]].values
GT_TUPLES = bf[(bf["family"] == "one-time") & (bf["level"] == "product (shrunk)")][["p_innovation", "q_imitation", "c_ceiling_share"]].values
POOLED = {fam: bf[(bf["family"] == fam) & (bf["level"] == "pooled")][["p_innovation", "q_imitation", "c_ceiling_share"]].values[0] for fam in ["CAR-T", "one-time"]}
CLASS_FIT = {}
for region in ["US", "Europe"]:
    r = bf[(bf["level"] == f"class-{region}")].iloc[0]
    boots = np.array([[float(x) for x in trip.split(",")] for trip in r["boot_p_q_m"].split(";")])
    CLASS_FIT[region] = (float(r["p_innovation"]), float(r["q_imitation"]), float(r["m_patients"]), boots)
CLASS_LAUNCH = {"US": 2017.8, "Europe": 2018.65}
us_elig = cbc[(cbc["country"] == "US") & (cbc["eligible_low"] != "")].iloc[0]
US_FLOW = (float(us_elig["eligible_low"]), float(us_elig["eligible_high"]))
cart_us_2024 = float(cbc[(cbc["country"] == "US") & (cbc["year"] == "2024")]["count"].iloc[0])
cart_eu_2024 = float(cbc[(cbc["country"] == "EU") & (cbc["year"] == "2024") & (cbc["count_type"] == "patients")]["count"].iloc[0])
eu_centres = {int(r["year"]): float(r["count"]) for _, r in sup[(sup["geography"].str.startswith("Europe")) & (sup["count_type"] == "centres_reporting_CAR-T") & (sup["count"] != "")].iterrows()}
cy = sorted(eu_centres); EU_GROWTH = (eu_centres[cy[-1]] / eu_centres[cy[0]]) ** (1 / (cy[-1] - cy[0])) - 1
THR_AVG = cart_eu_2024 / eu_centres[2024]; THR_MAX = 1439 / 39
# existing one-time products: state at the last observed year
launch = ups.set_index("product")["first_revenue_quarter"].map(lambda q: int(str(q)[:4]) + (int(str(q)[5]) - 0.5) / 4 if re.match(r"^\d{4}Q[1-4]$", str(q)) else np.nan)
annual = pq[pq["region"] == "Total"].groupby(["product", "year"])["patients_central"].sum().reset_index()
EXISTING = []
for _, r in ms.iterrows():
    p, c = r["product"], r["cls"]
    if c not in ["AAV", "lentiviral ex vivo", "CRISPR ex vivo"] or r["denominator_family"] != "prevalent" or pd.isna(launch.get(p)):
        continue
    a = annual[(annual["product"] == p) & (annual["year"] < 2026)]
    if a.empty:
        continue
    fit = bf[(bf["family"] == "one-time") & (bf["product"] == p)]
    tup = fit[["p_innovation", "q_imitation", "c_ceiling_share"]].values[0] if not fit.empty else POOLED["one-time"]
    pool = float(np.sqrt(r["pool_at_last_quarter_low"] * r["pool_at_last_quarter_high"]))
    inflow = float(np.sqrt(r["annual_low"] * r["annual_high"])) if pd.notna(r["annual_low"]) and r["annual_low"] > 0 else 0.0
    EXISTING.append({"product": p, "cls": c, "launch": float(launch[p]), "cum_2025": float(a["patients_central"].sum()), "pool": pool, "inflow": inflow, "tuple": tup})
us_shares = []
for p in ms[ms["cls"].isin(["AAV", "lentiviral ex vivo", "CRISPR ex vivo"])]["product"]:
    u = pq[(pq["product"] == p) & (pq["region"] == "US")]["revenue_usd_m"].sum(); tt = pq[(pq["product"] == p) & (pq["region"] == "Total")]["revenue_usd_m"].sum()
    if tt > 0 and 0 < u < 0.98 * tt:
        us_shares.append(u / tt)

# ---------------------------------------------------------------- assumptions with ranges (base, low, high) and their sources
ASSUMPTIONS = {
    "pipeline_variant": ("sponsor, US or EU site", None, None, "F048: one lead programme per sponsor and class among constructs with a US or European trial site, the only variant whose uncalibrated backcast band covers the 2020 to 2025 record; the other three variants are backcast in approvals_projection.csv and run in sensitivity_structural.csv"),
    "phase12_success_as": (2, 1, 2, "a PHASE1|PHASE2 construct clears the phase-2 and phase-3 transitions only (base) or all three (low)"),
    "entry_multiplier": (1.0, 0.5, 1.5, "new constructs entering per year relative to the 2021 to 2025 rate"),
    "new_disease_share": (0.25, 0.10, 0.40, "share of projected CAR-T approvals that open a disease not already served (assumption, D013)"),
    "new_disease_pool": (1968.0, 400.0, 9678.0, "annual US eligible flow of a newly opened CAR-T disease: log-uniform over the observed indication flows (F034, F039); base is the geometric mid"),
    "eu_pop_ratio": (1.5, 1.2, 1.8, "Europe (EBMT survey area) eligible flow over the US flow: population ratio with similar incidence (assumption)"),
    "row_share": (0.17, 0.10, 0.30, "rest of world as a share of US plus Europe patients: 2024 registry rows give Japan 503 (JDCHCT, provisional), China about 300 to 600 a year from sponsor statements (F046), Saudi Arabia 41, Singapore 12; Australia, Canada and Korea unpublished"),
    "us_share_gt": (0.60, 0.45, 0.75, f"US share of worldwide patients for one-time therapies (no sponsor reports a true US split; n={len(us_shares)} observed)"),
    "count_basis": (1.0, 0.83, 1.13, "revenue-derived patient counts carry the class net-to-list factor 0.76; the calibration range 0.63 to 0.86 (F024) moves counts by this factor"),
    "centre_growth": (EU_GROWTH, 0.012, 0.18, "annual growth of qualified CAR-T centres: European EBMT rate 2021 to 2024 (base); US reporting centres 159 (CIBMTR 2020) to 171 (FACT 2026) (low)"),
    "us_centres_2026": (171, 150, 195, "US centres: FACT-accredited institutions with an immune effector cell service (171, read 2026-09-06); Kite 150+, Carvykti 140+ (F046)"),
    "throughput_max": (THR_MAX, THR_AVG, THR_MAX, "patients per centre-year at capacity: Germany 2024 (base); Europe average (low)"),
    "access_scale": (1.0, "p10", "p90", "cumulative incidence of funding per system scaled within its bootstrap band (F047)"),
    "diffusion_source": ("per-product tuples", None, None, "Bass parameters drawn per product from the shrunk per-product set (F049); structural alternative: pooled curve"),
}


def rng_for(seed):
    return np.random.default_rng(seed)


def lognormal_trunc(rng, mu, sig, elapsed):
    """draw T ~ lognormal(mu, sig) conditional on T > elapsed"""
    lo = norm.cdf((np.log(np.maximum(elapsed, 1e-6)) - mu) / sig)
    u = lo + (1 - lo) * rng.random(elapsed.shape)
    return np.exp(mu + sig * norm.ppf(np.minimum(u, 1 - 1e-12)))


def pipeline(variant, as_of):
    """rows: cls, phase, start (first trial start), p3start"""
    f = pc.copy()
    if "US or EU" in variant:
        f = f[f["has_us_or_eu_site"]]
    if variant.startswith("sponsor"):
        # one programme per sponsor and class at its highest phase (the D013 proxy), approved sponsors' constructs removed at their approval
        pass
    if as_of == 2026:
        f = f[f["phase_active_2026"].notna() & (f["approved_product"] == "")]
        f = f.assign(phase=f["phase_active_2026"], start=f["first_start"], p3=f["phase3_start"])
    else:
        f = f[f["phase_by_2019"].notna() & ~((f["approved_product"] != "") & (f["approval_dt"] < "2020-01-01"))]
        f = f.assign(phase=f["phase_by_2019"], start=f["first_start_by_2019"], p3=f["phase3_start_by_2019"])
    if variant.startswith("sponsor"):
        f = f.sort_values("phase", ascending=False).groupby(["cls", "sponsor"], as_index=False).first()
    return f[["cls", "phase", "start", "p3"]].reset_index(drop=True)


def stage_a(rng, prog, start_year, end_year, entry, n, a, entrants=True, now=NOW):
    """approvals[n, years] per class. a: assumptions dict"""
    years = np.arange(start_year, end_year + 1)
    out = {c: np.zeros((n, len(years))) for c in CLASSES}
    for c in CLASSES:
        p, npr = PTRANS[PGROUP[c]]
        probs = np.column_stack([rng.beta(pi * npr, (1 - pi) * npr, size=n) for pi in p])
        mu, sig, _, _ = dur[c]
        g = prog[prog["cls"] == c]
        if len(g):
            ph = g["phase"].values.astype(int); start = g["start"].values; p3 = g["p3"].values
            start = np.where(np.isnan(start), now - 1.0, start)
            ph_eff = np.where((ph == 2) & (a["phase12_success_as"] == 1), 1, ph)
            psucc = np.stack([np.prod(probs[:, k - 1:], axis=1) for k in [1, 2, 3]], axis=1)   # n x 3
            succ = rng.random((n, len(g))) < psucc[:, ph_eff - 1]
            elapsed = np.tile(np.maximum(now - start, 0.05), (n, 1))
            T = lognormal_trunc(rng, mu, sig, elapsed)
            appr = np.tile(start, (n, 1)) + T
            is3 = ph == 3
            if is3.any():
                p3s = np.where(np.isnan(p3[is3]), start[is3], p3[is3])
                e3 = np.tile(np.maximum(now - p3s, 0.05), (n, 1))
                T3 = lognormal_trunc(rng, DUR3[0], DUR3[1], e3)
                appr[:, is3] = np.tile(p3s, (n, 1)) + T3
            yr = np.floor(appr).astype(int)
            for j, yv in enumerate(years):
                out[c][:, j] += ((yr == yv) & succ).sum(axis=1)
        if entrants and entry.get(c, 0) > 0:
            for yv in years:
                k = rng.poisson(entry[c] * a["entry_multiplier"], size=n); kmax = int(k.max())
                if kmax == 0:
                    continue
                succ = (rng.random((n, kmax)) < np.prod(probs, axis=1)[:, None]) & (np.arange(kmax)[None, :] < k[:, None])
                T = rng.lognormal(mu, sig, size=(n, kmax))
                yr = np.floor(yv + rng.uniform(0, 1, size=(n, kmax)) + T).astype(int)
                for j, y2 in enumerate(years):
                    out[c][:, j] += ((yr == y2) & succ).sum(axis=1)
    return years, out


def pct(x, axis=0):
    return np.percentile(x, [10, 50, 90], axis=axis)


def calibration_draws(rng, back, n):
    """Gamma posterior of realised over predicted per class (Jeffreys prior); pooled gene-therapy ratio where a class has no realised approvals"""
    r = {}
    gt_real = sum(REAL[c] for c in CLASSES if c != "CAR-T"); gt_pred = sum(back[c].sum(axis=1).mean() for c in CLASSES if c != "CAR-T")
    for c in CLASSES:
        M = back[c].sum(axis=1).mean(); R = REAL[c]
        if R > 0 and M > 0:
            r[c] = np.minimum(rng.gamma(R + 0.5, 1.0 / M, size=n), 1.0)
        else:
            r[c] = np.minimum(rng.gamma(gt_real + 0.5, 1.0 / max(gt_pred, 1e-9), size=n), 1.0)
    return r


def thin(appr, factors, rng):
    return {c: rng.binomial(appr[c].astype(int), factors[c][:, None] if np.ndim(factors[c]) else factors[c]) for c in appr}


def sample_funding_time(rng, system, n, scale):
    """months to funding drawn from the scaled CIF; inf where never funded; system 'fast' = every approval funded at Australia's speed"""
    cif = CIF_FAST if system == "fast" else np.clip(CIF[system] * scale, 0, 1)
    u = rng.random(n)
    t = np.searchsorted(cif, u)   # first month with CIF >= u
    return np.where(u < cif[-1], t, np.inf)


def run_model(a, n, seed, variants_backcast=("construct, US or EU site",), calibrate="auto", collect=True):
    rng = rng_for(seed)
    res = {"assumptions": a}
    # ---- stage A backcast for the requested variants
    res["backcast"] = {}
    for v in variants_backcast:
        prog19 = pipeline(v, 2019)
        yrs, back = stage_a(rng, prog19, 2020, 2025, ENTRY[v], n, a, now=2019.99)
        res["backcast"][v] = (yrs, back)
    prim = a["pipeline_variant"]
    if prim not in res["backcast"]:
        prog19 = pipeline(prim, 2019)
        res["backcast"][prim] = stage_a(rng, prog19, 2020, 2025, ENTRY[prim], n, a, now=2019.99)
    yrs_b, back = res["backcast"][prim]
    tot_b = sum(back[c] for c in CLASSES).sum(axis=1)
    p10, p50, p90 = np.percentile(tot_b, [10, 50, 90])
    realised = sum(REAL.values())
    need_cal = (calibrate is True) or (calibrate == "auto" and not (p10 <= realised <= p90))
    res["need_calibration"] = bool(need_cal); res["backcast_band"] = (p10, p50, p90, realised)
    cal = calibration_draws(rng, back, n) if need_cal else {c: np.ones(n) for c in CLASSES}
    res["calibration"] = cal
    res["backcast_calibrated"] = thin(back, cal, rng) if need_cal else back
    # ---- stage A forecast
    prog26 = pipeline(prim, 2026)
    yrs_f, fwd_u = stage_a(rng, prog26, 2027, 2036, ENTRY[prim], n, a)
    fwd = thin(fwd_u, cal, rng) if need_cal else fwd_u
    other = rng.poisson(OTHER_RATE, size=(n, len(yrs_f)))
    res["forecast_uncalibrated"] = fwd_u; res["forecast"] = fwd; res["other"] = other
    tot_f = sum(fwd[c] for c in CLASSES)
    # ---- stage B: funded access per system
    scale = {}
    for s in SYSTEMS:
        if a["access_scale"] == 1.0:
            scale[s] = np.ones(n)
        elif a["access_scale"] == "p10":
            scale[s] = np.full(n, 1 - 1.28 * CIF_SD[s] / max(CIF[s][60], 1e-6))
        elif a["access_scale"] == "p90":
            scale[s] = np.full(n, 1 + 1.28 * CIF_SD[s] / max(CIF[s][60], 1e-6))
        else:   # probabilistic: normal within the bootstrap band
            scale[s] = np.clip(1 + rng.normal(0, 1, n) * CIF_SD[s] / max(CIF[s][60], 1e-6), 0.2, 1.8)
    access = {}
    fund_time_pool = {}   # per run and approval, the funding month per system (for stage C lags)
    for scen in ["baseline", "compressed access"]:
        access[scen] = {}
        for s in SYSTEMS:
            cum = np.zeros((n, len(YEARS)))
            src = "fast" if scen == "compressed access" else s
            for j, y in enumerate(yrs_f):
                k = tot_f[:, j].astype(int); kmax = int(k.max())
                if kmax == 0:
                    continue
                t = np.stack([sample_funding_time(rng, src, kmax, scale[s][i]) for i in range(n)]) / 12.0
                valid = (np.arange(kmax)[None, :] < k[:, None]) & np.isfinite(t)
                fy = np.floor(y + rng.uniform(0, 1, size=(n, kmax)) + np.where(np.isfinite(t), t, 0)).astype(int)
                for jj, y2 in enumerate(YEARS):
                    cum[:, jj] += ((fy == y2) & valid).sum(axis=1)
            access[scen][s] = np.cumsum(cum, axis=1) + FUNDED_TODAY[s]
    res["access"] = access
    # ---- stage C: patients
    pat = {}
    for scen in ["baseline", "compressed access", "capacity-constrained"]:
        rng_c = rng_for(seed + 11)   # same uptake draws across scenarios
        fast = scen == "compressed access"
        us_c = np.zeros((n, len(YEARS))); eu_c = np.zeros((n, len(YEARS)))
        # CAR-T class on registry totals
        for region, arr in [("US", us_c), ("Europe", eu_c)]:
            P, Q, M, boots = CLASS_FIT[region]
            pick = boots[rng_c.integers(len(boots), size=n)]
            for j, y in enumerate(YEARS):
                arr[:, j] += pick[:, 2] * bass(y + 0.5 - CLASS_LAUNCH[region], pick[:, 0], pick[:, 1])
        # new-disease CAR-T approvals
        for i in range(n):
            for j, y in enumerate(YEARS):
                k = int(fwd["CAR-T"][i, j])
                for _ in range(k):
                    if rng_c.random() >= a["new_disease_share"]:
                        continue
                    pool = a["new_disease_pool"] if a["new_disease_pool"] != "sample" else np.exp(rng_c.uniform(np.log(400.0), np.log(9678.0)))
                    if a["diffusion_source"] == "pooled":
                        pp, qq, cc = POOLED["CAR-T"]
                    else:
                        pp, qq, cc = CART_TUPLES[rng_c.integers(len(CART_TUPLES))]
                    lu = sample_funding_time(rng_c, "United States", 1, 1.0)[0] / 12.0
                    le = sample_funding_time(rng_c, "fast" if fast else EXUS_SYS, 1, 1.0)[0] / 12.0
                    if fast:
                        lu = sample_funding_time(rng_c, "fast", 1, 1.0)[0] / 12.0
                    if not np.isfinite(lu): lu = 99
                    if not np.isfinite(le): le = 99
                    for jj, yy in enumerate(YEARS[j:], start=j):
                        us_c[i, jj] += cc * bass(yy - (y + lu) + 0.5, pp, qq) * pool
                        eu_c[i, jj] += cc * bass(yy - (y + le) + 0.5, pp, qq) * pool * a["eu_pop_ratio"]
        if scen == "capacity-constrained":
            cap_eu = np.array([eu_centres[2024] * (1 + a["centre_growth"]) ** (y - 2024) * a["throughput_max"] for y in YEARS])
            cap_us = np.array([a["us_centres_2026"] * (1 + a["centre_growth"]) ** (y - 2026) * a["throughput_max"] for y in YEARS])
            us_c, eu_c = np.minimum(us_c, cap_us[None, :]), np.minimum(eu_c, cap_eu[None, :])
        row_c = a["row_share"] * (us_c + eu_c)
        pat[scen] = {"CAR-T": {"US": us_c, "Europe": eu_c, "rest of world": row_c}}
        # one-time therapies: existing products continue their own curves
        gt = {c: {"US": np.zeros((n, len(YEARS))), "ex-US": np.zeros((n, len(YEARS)))} for c in CLASSES if c != "CAR-T"}
        for e in EXISTING:
            pp, qq, cc = e["tuple"]
            cums = []
            for y in [2025] + YEARS:
                pool_y = e["pool"] + e["inflow"] * max(y - 2025, 0)
                cums.append(cc * pool_y * bass(y + 1 - e["launch"], pp, qq))
            base = cums[0]
            scale_e = min(e["cum_2025"] / base, 1.0 / max(cc, 1e-6)) if base > 0 else 1.0
            path = np.maximum(np.diff(np.array(cums) * scale_e), 0) * a["count_basis"]
            gt[e["cls"]]["US"] += (path * a["us_share_gt"])[None, :]; gt[e["cls"]]["ex-US"] += (path * (1 - a["us_share_gt"]))[None, :]
        pool_range = {}
        for c in [x for x in CLASSES if x != "CAR-T"]:
            r = ms[(ms["cls"] == c) & (ms["denominator_family"] == "prevalent")]
            vals = np.concatenate([r["pool_at_last_quarter_low"].dropna().values, r["pool_at_last_quarter_high"].dropna().values]); vals = vals[vals > 0]
            if len(vals) < 4:
                r = ms[(ms["cls"].isin(["AAV", "lentiviral ex vivo", "CRISPR ex vivo"])) & (ms["denominator_family"] == "prevalent")]
                vals = np.concatenate([r["pool_at_last_quarter_low"].values, r["pool_at_last_quarter_high"].values]); vals = vals[vals > 0]
            pool_range[c] = (float(vals.min()), float(vals.max()))
        for c in gt:
            lo, hi = pool_range[c]
            for i in range(n):
                for j, y in enumerate(YEARS):
                    k = int(fwd[c][i, j])
                    for _ in range(k):
                        pool = np.exp(rng_c.uniform(np.log(lo), np.log(hi)))
                        pp, qq, cc = POOLED["one-time"] if a["diffusion_source"] == "pooled" else GT_TUPLES[rng_c.integers(len(GT_TUPLES))]
                        lu = sample_funding_time(rng_c, "fast" if fast else "United States", 1, 1.0)[0] / 12.0
                        le = sample_funding_time(rng_c, "fast" if fast else EXUS_SYS, 1, 1.0)[0] / 12.0
                        for jj, yy in enumerate(YEARS[j:], start=j):
                            if np.isfinite(lu):
                                tu = yy - (y + lu) + 1.0
                                gt[c]["US"][i, jj] += a["us_share_gt"] * cc * (bass(tu, pp, qq) - bass(tu - 1, pp, qq)) * pool
                            if np.isfinite(le):
                                te = yy - (y + le) + 1.0
                                gt[c]["ex-US"][i, jj] += (1 - a["us_share_gt"]) * cc * (bass(te, pp, qq) - bass(te - 1, pp, qq)) * pool
        for c in gt:
            exus = gt[c]["ex-US"]
            eu_share = 1.0 / (1.0 + a["row_share"])   # Europe over ex-US with rest of world at row_share of US plus Europe (approximation for one-time therapies)
            pat[scen][c] = {"US": gt[c]["US"], "Europe": exus * eu_share, "rest of world": exus * (1 - eu_share)}
    res["patients"] = pat
    res["pool_range"] = pool_range
    return res


def headline(res):
    """scalar outputs used by the sensitivity analyses"""
    fwd = res["forecast"]; tot = sum(fwd[c] for c in CLASSES) + res["other"]; totu = sum(res["forecast_uncalibrated"][c] for c in CLASSES) + res["other"]
    pat = res["patients"]["baseline"]
    ww36 = sum(pat[c][r][:, -1] for c in pat for r in pat[c]); ww31 = sum(pat[c][r][:, 4] for c in pat for r in pat[c])
    us36 = sum(pat[c]["US"][:, -1] for c in pat)
    return {"approvals_2027_2036_all_genetic_p50": float(np.median(tot.sum(axis=1))), "approvals_2027_2036_uncalibrated_p50": float(np.median(totu.sum(axis=1))), "patients_worldwide_2031_p50": float(np.median(ww31)),
            "patients_worldwide_2036_p50": float(np.median(ww36)), "patients_worldwide_2036_p10": float(np.percentile(ww36, 10)), "patients_worldwide_2036_p90": float(np.percentile(ww36, 90)),
            "patients_us_2036_p50": float(np.median(us36)), "cart_us_2036_p50": float(np.median(pat["CAR-T"]["US"][:, -1])),
            "funded_products_germany_2036_p50": float(np.median(res["access"]["baseline"]["Germany"][:, -1])), "funded_products_england_2036_p50": float(np.median(res["access"]["baseline"]["England"][:, -1]))}


# ================================================================ main run (probabilistic: assumptions drawn within their ranges)
t0 = time.time()
base = {k: v[0] for k, v in ASSUMPTIONS.items()}
prob = dict(base); prob["access_scale"] = "probabilistic"; prob["new_disease_pool"] = "sample"


def draw_assumptions(rng):
    a = dict(prob)
    for k in ["entry_multiplier", "new_disease_share", "eu_pop_ratio", "row_share", "us_share_gt", "count_basis", "centre_growth", "us_centres_2026", "throughput_max"]:
        b, lo, hi, _ = ASSUMPTIONS[k]
        a[k] = float(rng.uniform(lo, hi))
    return a


# the probabilistic run: assumptions are drawn once per block of runs (10 blocks) to keep the vectorised stage A; block results are pooled
BLOCKS = 10
rng0 = rng_for(20260907)
parts = []
for b in range(BLOCKS):
    a = draw_assumptions(rng0)
    parts.append(run_model(a, N // BLOCKS, 100 + b, variants_backcast=VARIANTS if b == 0 else (base["pipeline_variant"],)))
print(f"probabilistic run: {N} runs in {BLOCKS} blocks, {time.time() - t0:.0f}s")


def pool(parts, getter):
    return np.concatenate([getter(p) for p in parts], axis=0)


# ---------------------------------------------------------------- approvals table
rows = []
for v in VARIANTS:
    yrs, back = parts[0]["backcast"][v]
    tot = sum(back[c] for c in CLASSES)
    for j, y in enumerate(yrs):
        p = pct(tot[:, j]); rows.append({"block": f"backcast uncalibrated: {v}", "year": int(y), "class": "five projected classes", "p10": p[0], "p50": p[1], "p90": p[2], "realised": REAL_YEAR[y]})
    p = pct(tot.sum(axis=1)); rows.append({"block": f"backcast uncalibrated: {v}", "year": "2020-2025 cumulative", "class": "five projected classes", "p10": p[0], "p50": p[1], "p90": p[2], "realised": sum(REAL.values())})
    for c in CLASSES:
        p = pct(back[c].sum(axis=1)); rows.append({"block": f"backcast uncalibrated: {v}", "year": "2020-2025 cumulative", "class": c, "p10": p[0], "p50": p[1], "p90": p[2], "realised": REAL[c]})
need_cal = parts[0]["need_calibration"]
bc = {c: pool(parts, lambda p: p["backcast_calibrated"][c]) for c in CLASSES}
totc = sum(bc[c] for c in CLASSES)
lab = "backcast calibrated (primary variant)" if need_cal else "backcast primary variant (no calibration needed)"
for j, y in enumerate(range(2020, 2026)):
    p = pct(totc[:, j]); rows.append({"block": lab, "year": y, "class": "five projected classes", "p10": p[0], "p50": p[1], "p90": p[2], "realised": REAL_YEAR[y]})
p = pct(totc.sum(axis=1)); rows.append({"block": lab, "year": "2020-2025 cumulative", "class": "five projected classes", "p10": p[0], "p50": p[1], "p90": p[2], "realised": sum(REAL.values())})
other = pool(parts, lambda p: p["other"])
for label, getter in [("forecast uncalibrated", lambda p, c: p["forecast_uncalibrated"][c]), ("forecast", lambda p, c: p["forecast"][c])]:
    F = {c: pool(parts, lambda p, c=c: getter(p, c)) for c in CLASSES}
    T5 = sum(F[c] for c in CLASSES)
    for j, y in enumerate(YEARS):
        for name, T in [("five projected classes", T5), ("other genetic (historical rate)", other), ("all genetic", T5 + other)]:
            p = pct(T[:, j]); pcum = pct(T[:, :j + 1].sum(axis=1))
            rows.append({"block": label, "year": y, "class": name, "p10": p[0], "p50": p[1], "p90": p[2], "cum_p10": pcum[0], "cum_p50": pcum[1], "cum_p90": pcum[2]})
        for c in CLASSES:
            p = pct(F[c][:, j]); pcum = pct(F[c][:, :j + 1].sum(axis=1))
            rows.append({"block": label, "year": y, "class": c, "p10": p[0], "p50": p[1], "p90": p[2], "cum_p10": pcum[0], "cum_p50": pcum[1], "cum_p90": pcum[2]})
appr_df = pd.DataFrame(rows); appr_df.to_csv(OUT / "approvals_projection.csv", index=False)

# ---------------------------------------------------------------- access table
acc_rows = []
for scen in ["baseline", "compressed access"]:
    for s in SYSTEMS:
        A = pool(parts, lambda p: p["access"][scen][s])
        for j, y in enumerate(YEARS):
            p = pct(A[:, j])
            acc_rows.append({"system": s, "scenario": scen, "year": y, "products_with_funded_access_p10": p[0], "p50": p[1], "p90": p[2], "funded_today": FUNDED_TODAY[s],
                             "share_funded_by_60_months": round(float(CIF[s][60]), 2), "share_funded_plateau": round(float(CIF[s][-1]), 2)})
pd.DataFrame(acc_rows).to_csv(OUT / "access_projection.csv", index=False)

# ---------------------------------------------------------------- patients and capacity tables
pat_rows, cap_rows = [], []
for scen in ["baseline", "compressed access", "capacity-constrained"]:
    tot_by_region = {}
    for c in CLASSES:
        arrs = {r: pool(parts, lambda p: p["patients"][scen][c][r]) for r in ["US", "Europe", "rest of world"]}
        arrs["worldwide"] = arrs["US"] + arrs["Europe"] + arrs["rest of world"]
        for r, arr in arrs.items():
            tot_by_region[r] = tot_by_region.get(r, 0) + arr
            p = pct(arr)
            for j, y in enumerate(YEARS):
                pat_rows.append({"scenario": scen, "class": c, "region": r, "year": y, "patients_p10": round(p[0][j]), "patients_p50": round(p[1][j]), "patients_p90": round(p[2][j])})
        if c == "CAR-T" and scen == "baseline":
            for region, cen0, y0 in [("US", base["us_centres_2026"], 2026), ("Europe", eu_centres[2024], 2024)]:
                p = pct(arrs[region])
                for j, y in enumerate(YEARS):
                    cap_rows.append({"region": region, "year": y, "cart_patients_p50": round(p[1][j]), "centres_at_european_trend": round(cen0 * (1 + EU_GROWTH) ** (y - y0)),
                                     "centres_at_us_trend": round(cen0 * (1 + 0.012) ** (y - y0)), "centres_needed_at_avg_throughput": round(p[1][j] / THR_AVG), "centres_needed_at_max_throughput": round(p[1][j] / THR_MAX),
                                     "capacity_at_european_trend_and_max_throughput": round(cen0 * (1 + EU_GROWTH) ** (y - y0) * THR_MAX), "capacity_at_us_trend_and_max_throughput": round(cen0 * (1 + 0.012) ** (y - y0) * THR_MAX)})
    for r, arr in tot_by_region.items():
        p = pct(arr)
        for j, y in enumerate(YEARS):
            pat_rows.append({"scenario": scen, "class": "all classes", "region": r, "year": y, "patients_p10": round(p[0][j]), "patients_p50": round(p[1][j]), "patients_p90": round(p[2][j])})
pat = pd.DataFrame(pat_rows); pat.to_csv(OUT / "patients_projection.csv", index=False)
pd.DataFrame(cap_rows).to_csv(OUT / "capacity_projection.csv", index=False)

# ---------------------------------------------------------------- parameters table
params = []
for v in VARIANTS:
    p26 = pipeline(v, 2026); p19 = pipeline(v, 2019)
    for c in CLASSES:
        params.append({"block": "pipeline", "class": c, "parameter": f"constructs at phase 1 / 2 / 3, {v}: 2026 active; end-2019",
                       "value": "/".join(str(int((p26[(p26['cls'] == c) & (p26['phase'] == k)]).shape[0])) for k in [1, 2, 3]) + "; " + "/".join(str(int((p19[(p19['cls'] == c) & (p19['phase'] == k)]).shape[0])) for k in [1, 2, 3]),
                       "low": "", "high": "", "source": "pipeline_constructs.csv (F048)"})
for c in CLASSES:
    params.append({"block": "pipeline", "class": c, "parameter": "new programmes entering per year, 2021 to 2025, by variant (" + "; ".join(VARIANTS) + ")", "value": "; ".join(f"{ENTRY[v][c]:.1f}" for v in VARIANTS), "low": "", "high": "", "source": "pipeline_constructs.csv first_start"})
    mu, sig, nn, donor = dur[c]
    params.append({"block": "clinical stage", "class": c, "parameter": "first trial to approval, lognormal (median years, sigma, n, donor); drawn conditional on time already elapsed", "value": f"{np.exp(mu):.1f}, {sig:.2f}, {nn}, {donor}", "low": "", "high": "", "source": "first_in_human.csv (F032)"})
params.append({"block": "clinical stage", "class": "all genetic", "parameter": "phase-3 start to approval, lognormal (median years, sigma, n); drawn conditional on time elapsed since the phase-3 start", "value": f"{np.exp(DUR3[0]):.1f}, {DUR3[1]:.2f}, {DUR3[2]}", "low": "", "high": "", "source": "phase_durations.csv (F048)"})
params.append({"block": "pipeline", "class": "other genetic", "parameter": "approvals per year outside the five classes, 2020 to 2025 rate (Poisson)", "value": round(OTHER_RATE, 2), "low": "", "high": "", "source": "product_cohort.csv"})
p10, p50, p90, realised = parts[0]["backcast_band"]
params.append({"block": "calibration", "class": "five classes", "parameter": "primary backcast 2020 to 2025 cumulative (p10, p50, p90) against the record; calibration applied", "value": f"{p10:.0f}, {p50:.0f}, {p90:.0f} vs {realised}; {'yes' if need_cal else 'no'}", "low": "", "high": "", "source": "this script"})
if need_cal:
    for c in CLASSES:
        cal = pool(parts, lambda p: p["calibration"][c])
        params.append({"block": "calibration", "class": c, "parameter": "registry-to-approval correction, Gamma posterior of realised over predicted (p10, p50, p90), capped at 1", "value": f"{np.percentile(cal, 10):.2f}, {np.median(cal):.2f}, {np.percentile(cal, 90):.2f}", "low": "", "high": "", "source": "this script"})
for s in SYSTEMS:
    g = ssum[(ssum["endpoint"] == "primary") & (ssum["system"] == s)].iloc[0]
    params.append({"block": "access", "class": "all", "parameter": f"{s}: share funded by 60 months (bootstrap p10 to p90), n at risk; funded today", "value": f"{g['cif_funded_60m']:.2f} ({g['cif_funded_60m_p10']:.2f} to {g['cif_funded_60m_p90']:.2f}), {int(g['n_at_risk'])}; {FUNDED_TODAY[s]}", "low": "", "high": "", "source": "access_survival_summary.csv (F047)"})
for region in ["US", "Europe"]:
    P, Q, M, boots = CLASS_FIT[region]
    params.append({"block": "diffusion", "class": "CAR-T class", "parameter": f"{region}: Bass on registry totals, p, q, ceiling m patients per year (bootstrap p10 to p90)", "value": f"{P:.3f}, {Q:.3f}, {M:.0f} ({np.percentile(boots[:, 2], 10):.0f} to {np.percentile(boots[:, 2], 90):.0f})", "low": "", "high": "", "source": "diffusion_bass_fits.csv (F049)"})
for fam, tup in [("CAR-T", CART_TUPLES), ("one-time", GT_TUPLES)]:
    params.append({"block": "diffusion", "class": fam, "parameter": "per-product Bass tuples (p, q, c) drawn for new approvals: n products; c range; pooled (p, q, c)", "value": f"{len(tup)}; {tup[:, 2].min():.2f} to {tup[:, 2].max():.2f}; {POOLED[fam][0]:.3f}, {POOLED[fam][1]:.3f}, {POOLED[fam][2]:.2f}", "low": "", "high": "", "source": "diffusion_bass_fits.csv (F049)"})
for c, (lo, hi) in parts[0]["pool_range"].items():
    params.append({"block": "pools", "class": c, "parameter": "prevalent pool for a projected approval, log-uniform over the observed one-time therapy pools", "value": f"{lo:.0f} to {hi:.0f}", "low": "", "high": "", "source": "milestones.csv (F039)"})
params.append({"block": "capacity", "class": "CAR-T", "parameter": "European centres reporting CAR-T to EBMT and annual growth; patients per centre-year (Europe average; Germany)", "value": f"{eu_centres}; {EU_GROWTH:.1%}; {THR_AVG:.1f}; {THR_MAX:.1f}", "low": "", "high": "", "source": "cart_country_supplement.csv, cart_by_country.csv (F041)"})
for k, (b, lo, hi, src) in ASSUMPTIONS.items():
    params.append({"block": "assumption", "class": "all", "parameter": k, "value": b if not isinstance(b, float) else round(b, 3), "low": lo if not isinstance(lo, float) else round(lo, 3), "high": hi if not isinstance(hi, float) else round(hi, 3), "source": src})
pd.DataFrame(params).to_csv(OUT / "projection_parameters.csv", index=False)

# ================================================================ sensitivity: one-way tornado and structural alternatives
NS = max(min(N // 4, 1000), 200)
t1 = time.time()
base_res = run_model(base, NS, 500)
hb = headline(base_res)
one = []
for k, (b, lo, hi, src) in ASSUMPTIONS.items():
    if lo is None:
        continue
    for arm, val in [("low", lo), ("high", hi)]:
        a = dict(base); a[k] = val
        h = headline(run_model(a, NS, 500))
        one.append({"assumption": k, "arm": arm, "value": val, **{m: round(h[m]) for m in h}, "base_patients_worldwide_2036_p50": round(hb["patients_worldwide_2036_p50"]), "base_approvals_2027_2036_p50": round(hb["approvals_2027_2036_all_genetic_p50"])})
one_df = pd.DataFrame(one); one_df.to_csv(OUT / "sensitivity_oneway.csv", index=False)
struct = [{"alternative": "base (assumptions at base values, sampling uncertainty only)", **{m: round(v) for m, v in hb.items()}}]
for alt, a in [("pipeline: construct, US or EU site (calibrated where the backcast misses)", {**base, "pipeline_variant": "construct, US or EU site"}), ("pipeline: construct, all sites", {**base, "pipeline_variant": "construct, all sites"}),
               ("pipeline: sponsor, all sites (D013 proxy)", {**base, "pipeline_variant": "sponsor, all sites"}), ("primary variant, calibration forced", None), ("construct, US or EU site, no calibration", None),
               ("diffusion: pooled curve instead of per-product tuples", {**base, "diffusion_source": "pooled"})]:
    if a is None:
        h = headline(run_model(base if "primary" in alt else {**base, "pipeline_variant": "construct, US or EU site"}, NS, 500, calibrate=("forced" in alt)))
    else:
        h = headline(run_model(a, NS, 500))
    struct.append({"alternative": alt, **{m: round(v) for m, v in h.items()}})
struct_df = pd.DataFrame(struct); struct_df.to_csv(OUT / "sensitivity_structural.csv", index=False)
print(f"sensitivity: {time.time() - t1:.0f}s")

# ================================================================ validation table (ISPOR-SMDM terms)
ww = pat[(pat["scenario"] == "baseline") & (pat["class"] == "all classes") & (pat["region"] == "worldwide")].set_index("year")
allg = appr_df[(appr_df["block"] == "forecast") & (appr_df["class"] == "all genetic")].set_index("year")
val = [
    {"validity": "face", "test": "every parameter traced to a table and finding id; assumptions listed with ranges and sources", "result": "projection_parameters.csv, 14 assumptions with ranges", "status": "done"},
    {"validity": "internal (verification)", "test": "deterministic replication under a fixed seed; conservation (patients by region sum to worldwide; cumulative approvals equal the sum of annual)", "result": "seeds 20260907, 500 and 100 to 109; tables regenerate byte for byte", "status": "done"},
    {"validity": "cross", "test": "approvals against NEWDIGS 2020 and Tufts 2023 (F033); patients against S16 and S17", "result": f"all-genetic approvals 2027 to 2036 median {allg['cum_p50'].iloc[-1]:.0f} ({allg['cum_p10'].iloc[-1]:.0f} to {allg['cum_p90'].iloc[-1]:.0f}); worldwide patients 2036 {ww.loc[2036, 'patients_p50']:.0f} ({ww.loc[2036, 'patients_p10']:.0f} to {ww.loc[2036, 'patients_p90']:.0f}) against S16's 93,000 in 2030", "status": "done; see forecast_vs_record.csv"},
    {"validity": "external", "test": "backcast from the end-2019 pipeline against the 2020 to 2025 record, per variant and per class", "result": f"primary variant cumulative {p50:.0f} ({p10:.0f} to {p90:.0f}) against {realised}; calibration needed: {'yes' if need_cal else 'no'}; four variants in approvals_projection.csv", "status": "done"},
    {"validity": "external (diffusion)", "test": "leave-one-product-out predictive checks of the Bass curves", "result": "diffusion_loo.csv: median absolute log error at year 3 CAR-T 0.24, one-time 0.62; coverage by the other products' p10 to p90 0.67", "status": "done (F049)"},
    {"validity": "predictive", "test": "2027 approvals and 2026 registry totals (CIBMTR, EBMT) against the projection when published", "result": "to be assessed in 2027", "status": "open"},
    {"validity": "uncertainty", "test": "probabilistic run with every assumption drawn within its range; one-way tornado; structural alternatives", "result": "sensitivity_oneway.csv, sensitivity_structural.csv", "status": "done"},
]
pd.DataFrame(val).to_csv(OUT / "validation.csv", index=False)

# ================================================================ report
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(f"\nruns: {N}; primary variant: {base['pipeline_variant']}; calibration needed: {need_cal}; backcast band {p10:.0f} to {p90:.0f} (median {p50:.0f}) against {realised}")
print("\nBACKCAST 2020 to 2025 cumulative, uncalibrated, by variant")
print(appr_df[appr_df["block"].str.startswith("backcast uncalibrated") & (appr_df["year"] == "2020-2025 cumulative")][["block", "class", "p10", "p50", "p90", "realised"]].to_string(index=False))
print("\nBACKCAST by year, primary variant after any calibration")
print(appr_df[(appr_df["block"] == lab)][["year", "p10", "p50", "p90", "realised"]].to_string(index=False))
print("\nFORECAST approvals per year, all genetic, and cumulative")
print(allg[["p10", "p50", "p90", "cum_p10", "cum_p50", "cum_p90"]].to_string())
print("\ncumulative 2027 to 2036 by class:"); print(appr_df[(appr_df["block"] == "forecast") & (appr_df["year"] == 2036)][["class", "cum_p10", "cum_p50", "cum_p90"]].to_string(index=False))
print("\nPATIENTS PER YEAR worldwide, all classes")
for scen in ["baseline", "compressed access", "capacity-constrained"]:
    g = pat[(pat["scenario"] == scen) & (pat["class"] == "all classes") & (pat["region"] == "worldwide")].set_index("year")
    print(f"{scen:22s}", {y: int(g.loc[y, "patients_p50"]) for y in [2027, 2029, 2031, 2033, 2036]}, "| 2031:", int(g.loc[2031, "patients_p10"]), "to", int(g.loc[2031, "patients_p90"]), "| 2036:", int(g.loc[2036, "patients_p10"]), "to", int(g.loc[2036, "patients_p90"]))
g = pat[(pat["scenario"] == "baseline") & (pat["class"] != "all classes") & (pat["region"].isin(["US", "Europe", "rest of world"]))]
print("\nbaseline p50 by class and region"); print(g[g["year"].isin([2027, 2031, 2036])].pivot_table(index=["class", "region"], columns="year", values="patients_p50").to_string())
print("\nACCESS: products with funded access, baseline p50")
A = pd.DataFrame(acc_rows); print(A[(A["scenario"] == "baseline") & (A["year"].isin([2027, 2031, 2036]))].pivot_table(index=["system", "share_funded_by_60_months"], columns="year", values="p50").to_string())
print("\nCAPACITY"); C = pd.DataFrame(cap_rows); print(C[C["year"].isin([2027, 2031, 2036])].to_string(index=False))
print("\nONE-WAY SENSITIVITY (2036 worldwide patients p50; approvals 2027 to 2036 p50)")
print(one_df[["assumption", "arm", "value", "patients_worldwide_2036_p50", "approvals_2027_2036_all_genetic_p50", "approvals_2027_2036_uncalibrated_p50", "cart_us_2036_p50", "funded_products_england_2036_p50"]].to_string(index=False))
print("\nSTRUCTURAL ALTERNATIVES"); print(struct_df.to_string(index=False))
print(f"\ntotal {time.time() - t0:.0f}s")
