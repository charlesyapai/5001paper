"""Landscape projection 2027 to 2036 (topic 05; D013): a staged Monte Carlo that chains the measured stages.

Stage A, approvals. Industry programmes in the registry pipeline (one programme per sponsor per platform at its highest active
phase, from data/primary/trial_records.csv) survive phase transitions with the S06 probabilities (F027; rare-disease gene
therapy 55.0 / 49.2 / 68.4 percent, CAR-T 26.3 / 38.7 / 75.0) and reach approval after a clinical stage sampled from the
cohort's measured first-in-human-to-approval distribution for the class (F032, lognormal fit), scaled by the share of the
stage remaining at the programme's current phase. New programmes enter phase 1 each year at the 2021 to 2025 rate.
Backcast: the same model run on the pipeline as it stood at the end of 2019 is compared with the 2020 to 2025 record.
Stage B, access. Each approval draws a lag to the first positive funding step in each system from the measured lags
(F043; US: months to first revenue, F035).
Stage C, uptake. Class diffusion curves fitted to the observed penetration paths (annual patients over the label-dated
eligible flow for CAR-T; cumulative patients over the prevalent pool for one-time gene therapies) carry existing products
forward and start each projected approval at zero with an eligible pool drawn from the class's observed pools.
Capacity. CAR-T demand is set against qualified centres growing at the observed rate and the observed patients per
centre-year (F041 supplement).
Scenarios: baseline; compressed access (every system at the best observed median lag); capacity-constrained (centre growth
at trend, throughput at the observed maximum). Every output is a 10th, 50th and 90th percentile.

Outputs under data/projection/: pipeline_programmes.csv, projection_parameters.csv, approvals_projection.csv (with the
backcast rows), access_projection.csv, patients_projection.csv, capacity_projection.csv.
Run from research/findings:  python3 project_landscape_2026-09-06.py [n_runs]
"""
import re, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/projection"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
rng = np.random.default_rng(20260906)
YEARS = list(range(2027, 2037))
HORIZON = 2036

# ---------------------------------------------------------------- classes and parameters
SUBFAM = {"Engineered T-cell therapy (CAR-T)": "CAR-T", "AAV gene transfer": "AAV", "Lentiviral ex vivo gene therapy": "lentiviral ex vivo",
          "CRISPR nuclease editing": "CRISPR ex vivo", "In vivo LNP genetic medicine": "in vivo editing and LNP", "Base editing": "in vivo editing and LNP",
          "Prime editing": "in vivo editing and LNP", "Epigenome editing": "in vivo editing and LNP"}
CLASSES = ["CAR-T", "AAV", "lentiviral ex vivo", "CRISPR ex vivo", "in vivo editing and LNP"]
# S06 phase transition probabilities (F027) and the programme counts behind them, used as Beta priors
PTRANS = {"CAR-T": ([0.263, 0.387, 0.750], 402), "gene therapy": ([0.550, 0.492, 0.684], 195)}
PGROUP = {"CAR-T": "CAR-T", "AAV": "gene therapy", "lentiviral ex vivo": "gene therapy", "CRISPR ex vivo": "gene therapy", "in vivo editing and LNP": "gene therapy"}
# donor class for clinical-stage durations where the class has too few approved products (projection_model.md donor map)
DUR_DONOR = {"CRISPR ex vivo": "AAV", "in vivo editing and LNP": "AAV"}
# share of the clinical stage still ahead of a programme at its current highest phase (assumption; uniform range)
REMAINING = {1: (0.70, 1.00), 2: (0.40, 0.70), 3: (0.15, 0.40)}
PH = {"EARLY_PHASE1": 1, "PHASE1": 1, "PHASE1|PHASE2": 2, "PHASE2": 2, "PHASE2|PHASE3": 3, "PHASE3": 3}
ACTIVE = {"RECRUITING", "ACTIVE_NOT_RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION"}


def key(name):
    return re.split(r"[\s/(]", str(name).strip())[0].lower()


def cls_of(platform_class):
    p = str(platform_class)
    if "CAR-T" in p: return "CAR-T"
    if p.startswith("AAV"): return "AAV"
    if "lentiviral" in p or "retroviral" in p: return "lentiviral ex vivo"
    if "CRISPR" in p: return "CRISPR ex vivo"
    return "other"


# ---------------------------------------------------------------- inputs
t = pd.read_csv(ROOT / "data/primary/trial_records.csv", low_memory=False)
t = t[t["subfamily"].isin(SUBFAM) & (t["study_type"] == "INTERVENTIONAL")].copy()
t["cls"] = t["subfamily"].map(SUBFAM)
t["ph"] = t["phase"].map(PH)
coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh = coh[~coh["notes"].str.contains("out of scope")].copy()
coh["k"] = coh["product"].map(key)
coh["cls"] = coh["platform_class"].map(cls_of)
coh["first_approval"] = [min([d for d in [pd.to_datetime(a, errors="coerce"), pd.to_datetime(b, errors="coerce")] if pd.notna(d)], default=pd.NaT)
                         for a, b in zip(coh["fda_approval_date"], coh["eu_authorisation_date"])]
fih = pd.read_csv(ROOT / "data/cohort/first_in_human.csv", dtype=str).fillna("")
fih["years"] = pd.to_numeric(fih["years_fih_to_first_approval"], errors="coerce")
fih["cls"] = fih["platform_class"].map(cls_of)
acc = pd.read_csv(ROOT / "data/access/access_summary.csv", dtype=str).fillna("")
acc["m"] = pd.to_numeric(acc["months_approval_to_first_funding"], errors="coerce")
ups = pd.read_csv(ROOT / "data/uptake/uptake_summary.csv", dtype=str).fillna("")
ups["m_rev"] = pd.to_numeric(ups["months_first_approval_to_first_revenue_qend"], errors="coerce")
pq = pd.read_csv(ROOT / "data/uptake/patients_quarterly.csv", dtype=str).fillna("")
for c in ["revenue_usd_m", "patients_central", "cumulative_central"]:
    pq[c] = pd.to_numeric(pq[c], errors="coerce")
pq["year"] = pq["period_end"].str[:4].astype(int)
ms = pd.read_csv(ROOT / "data/uptake/milestones.csv", dtype=str).fillna("")
for c in ["pool_at_last_quarter_low", "pool_at_last_quarter_high", "annual_low", "annual_high", "prevalent_low", "prevalent_high", "clinical_stage_years"]:
    ms[c] = pd.to_numeric(ms[c], errors="coerce")
ms["cls"] = ms["platform_class"].map(cls_of)
sup = pd.read_csv(ROOT / "data/uptake/raw/cart_country_supplement.csv", dtype=str).fillna("")
cbc = pd.read_csv(ROOT / "data/uptake/cart_by_country.csv", dtype=str).fillna("")

params = []   # every fitted or assumed parameter, written out

# ---------------------------------------------------------------- Stage A inputs: pipeline and durations
def programmes(frame):
    ind = frame[(frame["sponsor_class"] == "INDUSTRY") & frame["ph"].notna()]
    return ind.groupby(["cls", "sponsor"])["ph"].max().reset_index()


pipe_now = programmes(t[t["status"].isin(ACTIVE)])
pipe_now["as_of"] = "2026-09"
# backcast pipeline: trials started by end-2019 (any later status), programme phase = highest phase among those trials;
# sponsors whose product was already approved before 2020 are removed
approved_pre2020 = set(coh[coh["first_approval"] < "2020-01-01"]["sponsor"].str.lower().str[:12])
t19 = t[(t["start_year"] <= 2019)]
pipe_19 = programmes(t19)
pipe_19 = pipe_19[~pipe_19["sponsor"].str.lower().str[:12].isin(approved_pre2020)]
pipe_19["as_of"] = "2019-12"
pd.concat([pipe_now, pipe_19]).to_csv(OUT / "pipeline_programmes.csv", index=False)
counts_now = pipe_now.groupby(["cls", "ph"]).size().unstack(fill_value=0).reindex(CLASSES).fillna(0)
counts_19 = pipe_19.groupby(["cls", "ph"]).size().unstack(fill_value=0).reindex(CLASSES).fillna(0)

# new programme entry rate: a sponsor's first phase-1 start in the class, averaged over 2021 to 2025
p1 = t[(t["sponsor_class"] == "INDUSTRY") & (t["ph"] == 1)]
first = p1.groupby(["cls", "sponsor"])["start_year"].min().reset_index()
entry = first[first["start_year"].between(2021, 2025)].groupby("cls").size().reindex(CLASSES).fillna(0) / 5
for c in CLASSES:
    params.append({"block": "pipeline", "class": c, "parameter": "industry programmes at phase 1 / 2 / 3 (2026-09)", "value": "/".join(str(int(counts_now.loc[c].get(k, 0))) for k in [1, 2, 3]), "source": "trial_records.csv, sponsor x platform at highest active phase"})
    params.append({"block": "pipeline", "class": c, "parameter": "new programmes entering phase 1 per year", "value": round(entry[c], 1), "source": "first industry phase-1 start per sponsor, 2021 to 2025"})

# clinical-stage duration per class: lognormal on the cohort's FIH-to-approval years (F032)
dur = {}
for c in CLASSES:
    donor = DUR_DONOR.get(c, c)
    y = fih[(fih["cls"] == donor) & fih["years"].notna() & (fih["years"] > 0)]["years"].values
    mu, sig = np.log(y).mean(), max(np.log(y).std(ddof=1), 0.15)
    dur[c] = (mu, sig, len(y), donor)
    params.append({"block": "clinical stage", "class": c, "parameter": f"FIH to approval, lognormal (median years, sigma, n, donor)", "value": f"{np.exp(mu):.1f}, {sig:.2f}, {len(y)}, {donor}", "source": "first_in_human.csv (F032)"})


def sample_probs(group, n):
    p, npr = PTRANS[group]
    return np.column_stack([rng.beta(pi * npr, (1 - pi) * npr, size=n) for pi in p])


def simulate_approvals(counts, start_year, end_year, entry_rate, n=N, entrants=True):
    """approvals[n, years] per class; a programme at phase k succeeds with prod(p[k-1:]) and approves after remaining share x T."""
    years = np.arange(start_year, end_year + 1)
    out = {c: np.zeros((n, len(years))) for c in CLASSES}
    for c in CLASSES:
        probs = sample_probs(PGROUP[c], n)
        mu, sig, _, _ = dur[c]
        for ph in [1, 2, 3]:
            k = int(counts.loc[c].get(ph, 0))
            if k == 0:
                continue
            succ = rng.random((n, k)) < np.prod(probs[:, ph - 1:], axis=1)[:, None]
            T = rng.lognormal(mu, sig, size=(n, k))
            share = rng.uniform(*REMAINING[ph], size=(n, k))
            elapsed_offset = rng.uniform(0.0, 1.0, size=(n, k))   # programmes are observed part-way through a year
            yr = np.floor(start_year - 0.75 + T * share + elapsed_offset).astype(int)
            for i in range(n):
                ys = yr[i][succ[i]]
                ys = ys[(ys >= start_year) & (ys <= end_year)]
                np.add.at(out[c][i], ys - start_year, 1)
        if entrants and entry_rate.get(c, 0) > 0:
            for j, y0 in enumerate(years):
                k = rng.poisson(entry_rate[c], size=n)
                kmax = k.max()
                if kmax == 0:
                    continue
                succ = (rng.random((n, kmax)) < np.prod(probs, axis=1)[:, None]) & (np.arange(kmax)[None, :] < k[:, None])
                T = rng.lognormal(mu, sig, size=(n, kmax))
                yr = np.floor(y0 + rng.uniform(0, 1, size=(n, kmax)) + T).astype(int)
                for i in range(n):
                    ys = yr[i][succ[i]]
                    ys = ys[(ys >= start_year) & (ys <= end_year)]
                    np.add.at(out[c][i], ys - start_year, 1)
    return years, out


def pct(a, axis=0):
    return np.percentile(a, [10, 50, 90], axis=axis)


# ---------------------------------------------------------------- Stage A: backcast, calibrate, forecast
rows = []
years_b, back = simulate_approvals(counts_19, 2020, 2025, entry.to_dict(), n=N)
real = coh[(coh["first_approval"] >= "2020-01-01") & (coh["first_approval"] <= "2025-12-31") & (coh["genetic_modification"] == "yes")]
real_by = real.groupby([real["first_approval"].dt.year, "cls"]).size().unstack(fill_value=0)
OTHER_GENETIC_RATE = float((real["cls"] == "other").sum()) / 6.0   # oncolytic, adenoviral, TCR-T and other vectors: outside the projected classes
params.append({"block": "pipeline", "class": "other genetic", "parameter": "approvals per year outside the five projected classes, historical 2020 to 2025 rate (Poisson)", "value": round(OTHER_GENETIC_RATE, 2), "source": "product_cohort.csv"})
real_by = real_by.drop(columns=[c for c in real_by.columns if c == "other"]) if "other" in real_by.columns else real_by
tot_b = sum(back[c] for c in CLASSES)
for j, y in enumerate(years_b):
    p = pct(tot_b[:, j])
    rows.append({"block": "backcast uncalibrated (pipeline at 2019-12)", "year": int(y), "class": "five projected classes", "p10": p[0], "p50": p[1], "p90": p[2], "realised": int(real_by.loc[y].sum()) if y in real_by.index else 0})
pc = pct(tot_b.sum(axis=1))
rows.append({"block": "backcast uncalibrated (pipeline at 2019-12)", "year": "2020-2025 cumulative", "class": "five projected classes", "p10": pc[0], "p50": pc[1], "p90": pc[2], "realised": int(real_by.values.sum())})
# calibration: realised over predicted median per class; classes with no realised approvals take the pooled gene-therapy ratio
calib = {}
gt_real = gt_pred = 0.0
for c in CLASSES:
    pc = pct(back[c].sum(axis=1))
    r = int(real_by[c].sum()) if c in real_by.columns else 0
    rows.append({"block": "backcast uncalibrated (pipeline at 2019-12)", "year": "2020-2025 cumulative", "class": c, "p10": pc[0], "p50": pc[1], "p90": pc[2], "realised": r})
    if c != "CAR-T":
        gt_real += r; gt_pred += pc[1]
    calib[c] = (r / pc[1]) if (pc[1] > 0 and r > 0) else None
gt_ratio = gt_real / gt_pred if gt_pred > 0 else 1.0
for c in CLASSES:
    if calib[c] is None:
        calib[c] = gt_ratio
    calib[c] = min(calib[c], 1.0)
    params.append({"block": "calibration", "class": c, "parameter": "registry-to-approval calibration factor (realised 2020-2025 / backcast median; capped at 1)", "value": round(calib[c], 2), "source": "this script; the sponsor-level programme proxy overcounts programmes that never seek FDA or EMA approval"})


def thin(appr, factors):
    """apply the calibration as binomial thinning of each year's approvals"""
    return {c: rng.binomial(appr[c].astype(int), factors[c]) for c in appr}


back_c = thin(back, calib)
tot_bc = sum(back_c[c] for c in CLASSES)
for j, y in enumerate(years_b):
    p = pct(tot_bc[:, j])
    rows.append({"block": "backcast calibrated", "year": int(y), "class": "five projected classes", "p10": p[0], "p50": p[1], "p90": p[2], "realised": int(real_by.loc[y].sum()) if y in real_by.index else 0})
pc = pct(tot_bc.sum(axis=1))
rows.append({"block": "backcast calibrated", "year": "2020-2025 cumulative", "class": "five projected classes", "p10": pc[0], "p50": pc[1], "p90": pc[2], "realised": int(real_by.values.sum())})

years_f, fwd_u = simulate_approvals(counts_now, 2027, HORIZON, entry.to_dict(), n=N)
fwd = thin(fwd_u, calib)
other_g = rng.poisson(OTHER_GENETIC_RATE, size=(N, len(years_f)))
for label, F in [("forecast uncalibrated", fwd_u), ("forecast", fwd)]:
    T5 = sum(F[c] for c in CLASSES)
    for j, y in enumerate(years_f):
        for name, T in [("five projected classes", T5), ("other genetic (historical rate)", other_g), ("all genetic", T5 + other_g)]:
            p = pct(T[:, j]); pcum = pct(T[:, :j + 1].sum(axis=1))
            rows.append({"block": label, "year": int(y), "class": name, "p10": p[0], "p50": p[1], "p90": p[2], "cum_p10": pcum[0], "cum_p50": pcum[1], "cum_p90": pcum[2]})
        for c in CLASSES:
            p = pct(F[c][:, j]); pcum = pct(F[c][:, :j + 1].sum(axis=1))
            rows.append({"block": label, "year": int(y), "class": c, "p10": p[0], "p50": p[1], "p90": p[2], "cum_p10": pcum[0], "cum_p50": pcum[1], "cum_p90": pcum[2]})
tot_f = sum(fwd[c] for c in CLASSES)
appr_df = pd.DataFrame(rows)
appr_df.to_csv(OUT / "approvals_projection.csv", index=False)

# ---------------------------------------------------------------- Stage B: access lags and funding probability per system
dec = pd.read_csv(ROOT / "data/access/decisions.csv", dtype=str).fillna("")
lags = {s: g["m"].dropna().values for s, g in acc.groupby("system") if g["m"].notna().sum() >= 5}
lags["United States (first revenue)"] = ups["m_rev"].dropna().values
best = min(np.median(v) for v in lags.values())
pfund = {}
for s in lags:
    if s.startswith("United States"):
        auth = coh[(coh["fda_approval_date"] != "") & (coh["fda_approval_date"] < "2025-01-01")]["k"]
        funded = ups[ups["m_rev"].notna()]["product"]
    else:
        d = dec[(dec["system"] == s) & ~dec["outcome"].isin(["not-submitted", "not-found"])]
        auth = d["product_key"].unique()
        auth = [k for k in auth if k in set(coh[coh["first_approval"] < "2025-01-01"]["k"])]
        funded = acc[(acc["system"] == s) & acc["m"].notna()]["product_key"]
    pfund[s] = len(set(funded) & set(auth)) / max(len(set(auth)), 1)
    params.append({"block": "access", "class": "all", "parameter": f"{s}: months to first positive funding step (median, n); share of products authorised before 2025 that reached it", "value": f"{np.median(lags[s]):.1f}, {len(lags[s])}; {pfund[s]:.2f}", "source": "access_summary.csv, decisions.csv (F043); uptake_summary.csv (F035) for the US"})
params.append({"block": "access", "class": "all", "parameter": "compressed-access scenario lag (best observed system median, months)", "value": round(best, 1), "source": "min over systems"})
funded_today = {s: int(acc[(acc["system"] == s) & acc["m"].notna()].shape[0]) for s in lags if s in set(acc["system"])}
funded_today["United States (first revenue)"] = int(ups["m_rev"].notna().sum())
acc_rows = []
for s, v in lags.items():
    for scen, lagpool in [("baseline", v), ("compressed access", np.array([best]))]:
        cum = np.zeros((N, len(years_f)))
        for j, y in enumerate(years_f):
            k = tot_f[:, j].astype(int)
            kmax = int(k.max()) if k.size else 0
            if kmax == 0:
                continue
            lag = rng.choice(lagpool, size=(N, kmax)) / 12.0
            mask = (np.arange(kmax)[None, :] < k[:, None]) & (rng.random((N, kmax)) < pfund[s])
            yr = np.floor(y + rng.uniform(0, 1, size=(N, kmax)) + np.maximum(lag, 0)).astype(int)
            for i in range(N):
                ys = yr[i][mask[i]]
                ys = ys[(ys >= 2027) & (ys <= HORIZON)]
                np.add.at(cum[i], ys - 2027, 1)
        cum = np.cumsum(cum, axis=1) + funded_today.get(s, 0)
        for j, y in enumerate(years_f):
            p = pct(cum[:, j])
            acc_rows.append({"system": s, "scenario": scen, "year": int(y), "products_with_funded_access_p10": p[0], "p50": p[1], "p90": p[2], "funded_today": funded_today.get(s, 0), "share_of_approvals_funded": round(pfund[s], 2)})
pd.DataFrame(acc_rows).to_csv(OUT / "access_projection.csv", index=False)

# ---------------------------------------------------------------- Stage C: class diffusion fits
def sat(tt, S, tau):
    return S * (1 - np.exp(-np.maximum(tt, 0) / tau))


tot = pq[pq["region"] == "Total"].copy()
annual = tot.groupby(["product", "year"])["patients_central"].sum().reset_index()
launch = ups.set_index("product")["first_revenue_quarter"].map(lambda q: int(str(q)[:4]) if str(q)[:4].isdigit() else np.nan)
fits, fit_rows = {}, []
for fam, products, smax in [("CAR-T", ms[(ms["cls"] == "CAR-T") & (ms["denominator_family"] == "annual")]["product"].tolist(), 1.0),
                            ("one-time gene therapy", ms[(ms["cls"].isin(["AAV", "lentiviral ex vivo", "CRISPR ex vivo"])) & (ms["denominator_family"] == "prevalent")]["product"].tolist(), 1.0)]:
    X, Y, W = [], [], []
    for p in products:
        r = ms[ms["product"] == p].iloc[0]
        a = annual[(annual["product"] == p) & (annual["year"] < 2026)]
        if a.empty or pd.isna(launch.get(p)):
            continue
        if fam == "CAR-T":
            pool = np.sqrt(r["annual_low"] * r["annual_high"]) if r["annual_low"] > 0 else np.nan
            for _, q in a.iterrows():
                X.append(q["year"] - launch[p] + 0.5); Y.append(q["patients_central"] / pool); W.append(p)
        else:
            pool = np.sqrt(r["pool_at_last_quarter_low"] * r["pool_at_last_quarter_high"])
            cum = a.sort_values("year")["patients_central"].cumsum()
            for (_, q), cval in zip(a.sort_values("year").iterrows(), cum):
                X.append(q["year"] - launch[p] + 1.0); Y.append(min(cval / pool, 1.0)); W.append(p)
    X, Y = np.array(X), np.array(Y)
    ok = np.isfinite(X) & np.isfinite(Y)
    X, Y, W = X[ok], Y[ok], np.array(W)[ok]
    (S, tau), _ = curve_fit(sat, X, Y, p0=[0.3, 3], bounds=([0.01, 0.5], [smax, 40]))
    prods = np.unique(W)
    boots = []
    for _ in range(300):
        pick = rng.choice(prods, size=len(prods), replace=True)
        idx = np.concatenate([np.where(W == p)[0] for p in pick])
        try:
            b, _ = curve_fit(sat, X[idx], Y[idx], p0=[S, tau], bounds=([0.01, 0.5], [smax, 40]))
            boots.append(b)
        except Exception:
            pass
    boots = np.array(boots)
    fits[fam] = (S, tau, boots)
    resid = Y - sat(X, S, tau)
    fit_rows.append({"family": fam, "n_products": len(prods), "n_points": len(X), "S_saturation_share": round(S, 3), "tau_years": round(tau, 2),
                     "initial_rate_S_over_tau_per_year": round(S / tau, 3),
                     "S_p10": round(np.percentile(boots[:, 0], 10), 3), "S_p90": round(np.percentile(boots[:, 0], 90), 3),
                     "tau_p10": round(np.percentile(boots[:, 1], 10), 2), "tau_p90": round(np.percentile(boots[:, 1], 90), 2),
                     "rmse_share": round(float(np.sqrt(np.mean(resid ** 2))), 3), "products": ", ".join(prods),
                     "note": "S and tau trade off on early curves; the initial rate S/tau is the identified quantity" if fam != "CAR-T" else ""})
    params.append({"block": "diffusion", "class": fam, "parameter": "saturating curve S(1-exp(-t/tau)) on penetration (S, tau years)", "value": f"{S:.3f}, {tau:.2f}", "source": "patients_quarterly.csv over label-dated pools (F039); bootstrap over products"})
pd.DataFrame(fit_rows).to_csv(OUT / "diffusion_fits.csv", index=False)

# region split for one-time therapies: US share of worldwide revenue where a true split exists, else 0.6 (assumption)
shares = []
for p in ms[ms["cls"].isin(["AAV", "lentiviral ex vivo", "CRISPR ex vivo"])]["product"]:
    u = pq[(pq["product"] == p) & (pq["region"] == "US")]["revenue_usd_m"].sum()
    tt = pq[(pq["product"] == p) & (pq["region"] == "Total")]["revenue_usd_m"].sum()
    if tt > 0 and 0 < u < 0.98 * tt:
        shares.append(u / tt)
US_SHARE_GT = float(np.median(shares)) if shares else 0.6
params.append({"block": "region", "class": "one-time gene therapy", "parameter": "US share of worldwide patients (median over products with a real US split, else 0.6)", "value": f"{US_SHARE_GT:.2f} (n={len(shares)})", "source": "patients_quarterly.csv; assumption where no split"})
EU_SHARE_EXUS = 0.75
params.append({"block": "region", "class": "all", "parameter": "Europe share of ex-US patients (assumption)", "value": EU_SHARE_EXUS, "source": "Gilead and BMS report Europe as most of ex-US CAR-T revenue; assumption for gene therapies"})

# ---- CAR-T as a class: penetration of the class eligible flow, anchored on registry totals
cart_us_2024 = float(cbc[(cbc["country"] == "US") & (cbc["year"] == "2024")]["count"].iloc[0])
cart_eu_2024 = float(cbc[(cbc["country"] == "EU") & (cbc["year"] == "2024") & (cbc["count_type"] == "patients")]["count"].iloc[0])
us_elig = cbc[(cbc["country"] == "US") & (cbc["eligible_low"] != "")].iloc[0]
US_CART_POOL = (float(us_elig["eligible_low"]), float(us_elig["eligible_high"]))
EU_POP_RATIO = 1.5   # EU plus UK population over US population; Europe class pool = US pool x ratio (assumption: similar incidence)
CART_LAUNCH = 2017.8
NEW_DISEASE_SHARE = 0.25   # share of projected CAR-T approvals that open a disease not already served (assumption)
NEW_DISEASE_POOL = (400.0, 9678.0)   # observed non-myeloma indication flows: paediatric ALL to third-line LBCL (F034, F039)
params += [{"block": "CAR-T class", "class": "CAR-T", "parameter": "2024 anchors: US CIBMTR infusions; Europe EBMT patients", "value": f"{cart_us_2024:.0f}; {cart_eu_2024:.0f}", "source": "cart_by_country.csv (F041)"},
           {"block": "CAR-T class", "class": "CAR-T", "parameter": "US class eligible flow per year (low, high); Europe = US x 1.5", "value": f"{US_CART_POOL[0]:.0f}, {US_CART_POOL[1]:.0f}", "source": "cart_by_country.csv eligible columns (F041); population ratio assumption"},
           {"block": "CAR-T class", "class": "CAR-T", "parameter": "share of projected CAR-T approvals opening a new disease, and its pool range", "value": f"{NEW_DISEASE_SHARE}; {NEW_DISEASE_POOL[0]:.0f} to {NEW_DISEASE_POOL[1]:.0f}", "source": "assumption; observed indication flows"}]


def cart_class_paths(approvals, lag_exus):
    S, tau, boots = fits["CAR-T"]
    res = {"US": np.zeros((N, len(YEARS))), "Europe": np.zeros((N, len(YEARS)))}
    for i in range(N):
        b = boots[rng.integers(len(boots))] if len(boots) else (S, tau)
        pool_us = np.exp(rng.uniform(np.log(US_CART_POOL[0]), np.log(US_CART_POOL[1])))
        pool_eu = pool_us * EU_POP_RATIO
        for region, anchor, pool in [("US", cart_us_2024, pool_us), ("Europe", cart_eu_2024, pool_eu)]:
            base = sat(2024.5 - CART_LAUNCH, b[0], b[1])
            scale = (anchor / pool) / base if base > 0 else 1.0
            scale = min(scale, 1.0 / b[0])   # penetration cannot exceed 1 of the flow
            for j, y in enumerate(YEARS):
                res[region][i, j] += scale * sat(y + 0.5 - CART_LAUNCH, b[0], b[1]) * pool
        # new-disease approvals add their own pool from the approval year, lagged ex-US
        for j, y in enumerate(YEARS):
            k = int(approvals["CAR-T"][i, j])
            for _ in range(k):
                if rng.random() >= NEW_DISEASE_SHARE:
                    continue
                pool = np.exp(rng.uniform(np.log(NEW_DISEASE_POOL[0]), np.log(NEW_DISEASE_POOL[1])))
                lu = rng.choice(lags["United States (first revenue)"]) / 12.0
                le = rng.choice(lag_exus) / 12.0
                for jj, yy in enumerate(YEARS[j:], start=j):
                    res["US"][i, jj] += sat(yy - (y + lu) + 0.5, b[0], b[1]) * pool
                    res["Europe"][i, jj] += sat(yy - (y + le) + 0.5, b[0], b[1]) * pool * EU_POP_RATIO
    return res


# ---- one-time therapies: product level, pools additive across diseases
pool_range = {}
for c in ["AAV", "lentiviral ex vivo", "CRISPR ex vivo", "in vivo editing and LNP"]:
    r = ms[(ms["cls"] == c) & (ms["denominator_family"] == "prevalent")]
    vals = np.concatenate([r["pool_at_last_quarter_low"].dropna().values, r["pool_at_last_quarter_high"].dropna().values])
    vals = vals[vals > 0]
    if len(vals) < 4:
        r = ms[(ms["cls"].isin(["AAV", "lentiviral ex vivo", "CRISPR ex vivo"])) & (ms["denominator_family"] == "prevalent")]
        vals = np.concatenate([r["pool_at_last_quarter_low"].values, r["pool_at_last_quarter_high"].values])
        vals = vals[vals > 0]
    pool_range[c] = (float(np.min(vals)), float(np.max(vals)))
    params.append({"block": "pools", "class": c, "parameter": "prevalent pool for a projected approval, log-uniform min to max of observed one-time therapy pools", "value": f"{pool_range[c][0]:.0f} to {pool_range[c][1]:.0f}", "source": "milestones.csv (F039)"})


def existing_gt_paths():
    paths = {}
    S, tau, _ = fits["one-time gene therapy"]
    for _, r in ms.iterrows():
        p, c = r["product"], r["cls"]
        if c not in ["AAV", "lentiviral ex vivo", "CRISPR ex vivo"] or pd.isna(launch.get(p)) or r["denominator_family"] != "prevalent":
            continue
        a = annual[(annual["product"] == p) & (annual["year"] < 2026)].sort_values("year")
        if a.empty:
            continue
        pool = np.sqrt(r["pool_at_last_quarter_low"] * r["pool_at_last_quarter_high"])
        cum_last, last_y = a["patients_central"].sum(), a["year"].iloc[-1]
        base = sat(last_y - launch[p] + 1.0, S, tau)
        scale = min((cum_last / pool) / base if base > 0 else 1.0, 1.0 / S)
        cums = [scale * sat(y - launch[p] + 1.0, S, tau) * pool for y in [last_y] + YEARS]
        paths[(p, c)] = np.maximum(np.diff(cums), 0)
    return paths


gt_paths = existing_gt_paths()
exist_gt = {c: sum(v for (p, cc), v in gt_paths.items() if cc == c) if any(cc == c for (_, cc) in gt_paths) else np.zeros(len(YEARS)) for c in CLASSES}


def new_gt_paths(approvals, lag_exus):
    res = {c: {"US": np.zeros((N, len(YEARS))), "ex-US": np.zeros((N, len(YEARS)))} for c in CLASSES if c != "CAR-T"}
    S, tau, boots = fits["one-time gene therapy"]
    for c in res:
        lo, hi = pool_range[c]
        for i in range(N):
            b = boots[rng.integers(len(boots))] if len(boots) else (S, tau)
            for j, y in enumerate(YEARS):
                k = int(approvals[c][i, j])
                if k == 0:
                    continue
                pools = np.exp(rng.uniform(np.log(lo), np.log(hi), size=k))
                lag_us = rng.choice(lags["United States (first revenue)"], size=k) / 12.0
                lag_ex = rng.choice(lag_exus, size=k) / 12.0
                for pool, lu, le in zip(pools, lag_us, lag_ex):
                    for jj, yy in enumerate(YEARS[j:], start=j):
                        tu, te = yy - (y + lu) + 1.0, yy - (y + le) + 1.0
                        res[c]["US"][i, jj] += US_SHARE_GT * (sat(tu, b[0], b[1]) - sat(tu - 1, b[0], b[1])) * pool
                        res[c]["ex-US"][i, jj] += (1 - US_SHARE_GT) * (sat(te, b[0], b[1]) - sat(te - 1, b[0], b[1])) * pool
    return res


exus_lags = np.concatenate([v for s, v in lags.items() if not s.startswith("United States")])
cart_base, cart_fast = cart_class_paths(fwd, exus_lags), cart_class_paths(fwd, np.array([best]))
gt_base, gt_fast = new_gt_paths(fwd, exus_lags), new_gt_paths(fwd, np.array([best]))

# capacity: CAR-T centres and throughput
eu_centres = {int(r["year"]): float(r["count"]) for _, r in sup[(sup["geography"].str.startswith("Europe")) & (sup["count_type"] == "centres_reporting_CAR-T") & (sup["count"] != "")].iterrows()}
c_years = sorted(eu_centres)
growth = (eu_centres[c_years[-1]] / eu_centres[c_years[0]]) ** (1 / (c_years[-1] - c_years[0])) - 1
thr_avg = cart_eu_2024 / eu_centres[2024]
thr_max = 1439 / 39   # Germany 2024: DRST patients over treating centres
us_centres_2026 = 160  # Kite: more than 160 US authorised treatment centres (kitepharma.com, 2026-09-04)
params += [{"block": "capacity", "class": "CAR-T", "parameter": "European CAR-T centres reporting to EBMT (2021 to 2024) and annual growth", "value": f"{eu_centres}; {growth:.1%}", "source": "cart_country_supplement.csv (F041)"},
           {"block": "capacity", "class": "CAR-T", "parameter": "patients per centre-year: Europe average 2024; Germany 2024 (used as maximum)", "value": f"{thr_avg:.1f}; {thr_max:.1f}", "source": "cart_by_country.csv (F041)"},
           {"block": "capacity", "class": "CAR-T", "parameter": "US authorised CAR-T treatment centres 2026 (Kite network)", "value": us_centres_2026, "source": "yescarta_disclosures.csv"}]

# ---------------------------------------------------------------- assemble
pat_rows, cap_rows = [], []
for scen in ["baseline", "compressed access", "capacity-constrained"]:
    cart = cart_fast if scen == "compressed access" else cart_base
    gtn = gt_fast if scen == "compressed access" else gt_base
    us_c, eu_c = cart["US"].copy(), cart["Europe"].copy()
    if scen == "capacity-constrained":
        cap_eu = np.array([eu_centres[2024] * (1 + growth) ** (y - 2024) * thr_max for y in YEARS])
        cap_us = np.array([us_centres_2026 * (1 + growth) ** (y - 2026) * thr_max for y in YEARS])
        us_c, eu_c = np.minimum(us_c, cap_us[None, :]), np.minimum(eu_c, cap_eu[None, :])
    row_c = (1 - EU_SHARE_EXUS) / EU_SHARE_EXUS * eu_c
    for region, arr in [("US", us_c), ("Europe", eu_c), ("rest of world", row_c), ("worldwide", us_c + eu_c + row_c)]:
        p = pct(arr)
        for j, y in enumerate(YEARS):
            pat_rows.append({"scenario": scen, "class": "CAR-T", "region": region, "year": y, "patients_p10": round(p[0][j]), "patients_p50": round(p[1][j]), "patients_p90": round(p[2][j])})
    if scen == "baseline":
        for region, arr, cen0, y0 in [("US", us_c, us_centres_2026, 2026), ("Europe", eu_c, eu_centres[2024], 2024)]:
            p = pct(arr)
            for j, y in enumerate(YEARS):
                cap_rows.append({"region": region, "year": y, "cart_patients_p50": round(p[1][j]), "centres_at_trend": round(cen0 * (1 + growth) ** (y - y0)),
                                 "centres_needed_at_avg_throughput": round(p[1][j] / thr_avg), "centres_needed_at_max_throughput": round(p[1][j] / thr_max),
                                 "capacity_at_trend_and_max_throughput": round(cen0 * (1 + growth) ** (y - y0) * thr_max)})
    for c in [x for x in CLASSES if x != "CAR-T"]:
        us = gtn[c]["US"] + (exist_gt[c] * US_SHARE_GT)[None, :]
        exus = gtn[c]["ex-US"] + (exist_gt[c] * (1 - US_SHARE_GT))[None, :]
        for region, arr in [("US", us), ("Europe", exus * EU_SHARE_EXUS), ("rest of world", exus * (1 - EU_SHARE_EXUS)), ("worldwide", us + exus)]:
            p = pct(arr)
            for j, y in enumerate(YEARS):
                pat_rows.append({"scenario": scen, "class": c, "region": region, "year": y, "patients_p10": round(p[0][j]), "patients_p50": round(p[1][j]), "patients_p90": round(p[2][j])})
pat = pd.DataFrame(pat_rows)
tot_rows = []
for scen in pat["scenario"].unique():
    for region in pat["region"].unique():
        g = pat[(pat["scenario"] == scen) & (pat["region"] == region)].groupby("year")[["patients_p10", "patients_p50", "patients_p90"]].sum()
        for y, r in g.iterrows():
            tot_rows.append({"scenario": scen, "class": "all classes", "region": region, "year": y, "patients_p10": r["patients_p10"], "patients_p50": r["patients_p50"], "patients_p90": r["patients_p90"]})
pat = pd.concat([pat, pd.DataFrame(tot_rows)], ignore_index=True)
pat.to_csv(OUT / "patients_projection.csv", index=False)
pd.DataFrame(cap_rows).to_csv(OUT / "capacity_projection.csv", index=False)
pd.DataFrame(params).to_csv(OUT / "projection_parameters.csv", index=False)

# ---------------------------------------------------------------- report
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(f"runs: {N}")
print("\nBACKCAST 2020 to 2025 from the pipeline at end-2019 (uncalibrated, then calibrated)")
print(appr_df[appr_df["block"].str.startswith("backcast")][["block", "year", "class", "p10", "p50", "p90", "realised"]].to_string(index=False))
print("\ncalibration factors:", {c: round(v, 2) for c, v in calib.items()})
print("\nFORECAST (calibrated): approvals per year, all genetic, and cumulative")
f = appr_df[(appr_df["block"] == "forecast") & (appr_df["class"] == "all genetic")]
print(f[["year", "p10", "p50", "p90", "cum_p10", "cum_p50", "cum_p90"]].to_string(index=False))
last = appr_df[(appr_df["block"] == "forecast") & (appr_df["year"] == HORIZON)]
print("\ncumulative 2027 to 2036 by class:"); print(last[["class", "cum_p10", "cum_p50", "cum_p90"]].to_string(index=False))
print("\nDIFFUSION FITS"); print(pd.DataFrame(fit_rows).drop(columns=["products"]).to_string(index=False))
print("\nPATIENTS PER YEAR worldwide, all classes (p50 by year; p10 to p90 at 2031 and 2036)")
for scen in ["baseline", "compressed access", "capacity-constrained"]:
    g = pat[(pat["scenario"] == scen) & (pat["class"] == "all classes") & (pat["region"] == "worldwide")].set_index("year")
    print(f"{scen:22s}", {y: int(g.loc[y, "patients_p50"]) for y in [2027, 2029, 2031, 2033, 2036]}, "| 2031:", int(g.loc[2031, "patients_p10"]), "to", int(g.loc[2031, "patients_p90"]), "| 2036:", int(g.loc[2036, "patients_p10"]), "to", int(g.loc[2036, "patients_p90"]))
g = pat[(pat["scenario"] == "baseline") & (pat["class"] != "all classes") & (pat["region"].isin(["US", "Europe"]))]
print("\nbaseline p50 by class and region"); print(g[g["year"].isin([2027, 2031, 2036])].pivot_table(index=["class", "region"], columns="year", values="patients_p50").to_string())
print("\nCAPACITY (CAR-T, baseline demand)"); C = pd.DataFrame(cap_rows); print(C[C["year"].isin([2027, 2029, 2031, 2034, 2036])].to_string(index=False))
A = pd.DataFrame(acc_rows)
print("\nACCESS: products with funded access, baseline p50 (share of approvals ever funded in brackets)")
print(A[(A["scenario"] == "baseline") & (A["year"].isin([2027, 2031, 2036]))].pivot_table(index=["system", "share_of_approvals_funded"], columns="year", values="p50").to_string())
