"""Diffusion of approved products as Bass curves with empirical-Bayes partial pooling and leave-one-product-out checks
(handover item A3; replaces the class-pooled saturating exponential of D013 stage C).

Penetration y(t) at t years after the first revenue quarter is modelled as y = c F(t; p, q), where F is the Bass
cumulative adoption curve F(t) = (1 - exp(-(p+q) t)) / (1 + (q/p) exp(-(p+q) t)), p the coefficient of innovation
(external influence), q the coefficient of imitation (internal influence) and c the ceiling share of the eligible pool.
Two families with the same form and different denominators:
  one-time therapies   y = cumulative patients / label-dated eligible pool (prevalent stock plus inflow to date)
  CAR-T (flow)         y = patients in the trailing four quarters / annual eligible flow (US series against the US flow where
                       the sponsor reports a US split, else worldwide against the US flow, flagged)
Fitting. Stage 1: a pooled fit per family. Stage 2: per-product fits penalised toward the pooled values in log space
(empirical-Bayes shrinkage; penalty tau = 0.5 log units on p and q, c bounded on (0.02, 1]); the per-product tuples are the
family's parameter distribution for the projection. Leave-one-product-out: each product is predicted from the fit on the
other products and its own pool, and the log error of the predicted cumulative (or run-rate) at years 1, 2 and 3 is
reported, with coverage by the spread of the other products' tuples.

Inputs : data/uptake/patients_quarterly.csv, milestones.csv, pool_quarterly.csv, uptake_summary.csv
Outputs: data/projection/diffusion_bass_fits.csv   pooled and per-product (p, q, c), n points, rmse, flags
         data/projection/diffusion_loo.csv         leave-one-out errors per product and horizon
         data/projection/diffusion_paths.csv       observed and fitted penetration per product and quarter
Run from research/findings:  python3 fit_diffusion_2026-09-07.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/projection"
TAU = 0.5          # shrinkage scale in log units for p and q
C_BOUNDS = (0.02, 1.0)
CART = "autologous CAR-T"
ONE_TIME = {"AAV systemic", "AAV subretinal", "AAV intraputaminal", "AAV intrathecal", "lentiviral ex vivo", "CRISPR ex vivo"}


def bass(t, p, q):
    t = np.maximum(t, 0.0)
    e = np.exp(-(p + q) * t)
    return (1 - e) / (1 + (q / p) * e)


def qend(q):
    return pd.Period(q, freq="Q").end_time.normalize()


pq = pd.read_csv(ROOT / "data/uptake/patients_quarterly.csv", dtype=str).fillna("")
for c in ["patients_central", "revenue_usd_m"]:
    pq[c] = pd.to_numeric(pq[c], errors="coerce")
pq["qend"] = pq["quarter"].map(qend)
ms = pd.read_csv(ROOT / "data/uptake/milestones.csv", dtype=str).fillna("")
for c in ["annual_low", "annual_high", "pool_at_last_quarter_low", "pool_at_last_quarter_high", "prevalent_low", "prevalent_high"]:
    ms[c] = pd.to_numeric(ms[c], errors="coerce")
pool_q = pd.read_csv(ROOT / "data/uptake/pool_quarterly.csv", dtype=str).fillna("")
for c in ["pool_low", "pool_high", "inflow_low", "inflow_high"]:
    pool_q[c] = pd.to_numeric(pool_q[c], errors="coerce")
pool_q["qend"] = pd.to_datetime(pool_q["quarter_end"])
ups = pd.read_csv(ROOT / "data/uptake/uptake_summary.csv", dtype=str).fillna("")

# ---------------------------------------------------------------- observed penetration paths
paths = []
for _, r in ms.iterrows():
    p = r["product"]
    fam = "CAR-T" if r["platform_class"] == CART else ("one-time" if r["platform_class"] in ONE_TIME else None)
    if fam is None or not r["first_revenue_quarter_end"]:
        continue
    t0 = pd.Timestamp(r["first_revenue_quarter_end"]) - pd.Timedelta(days=91)
    n_tot = ((pq["product"] == p) & (pq["region"] == "Total")).sum()
    has_us = ((pq["product"] == p) & (pq["region"] == "US")).sum() >= max(4, 0.6 * n_tot)
    region = "US" if (fam == "CAR-T" and has_us) else "Total"
    s = pq[(pq["product"] == p) & (pq["region"] == region)].sort_values("qend")
    s = s[s["qend"] <= "2026-06-30"]
    if s.empty:
        continue
    lab = pool_q[pool_q["product"] == p].set_index("qend")
    for i, (_, q) in enumerate(s.iterrows()):
        t = (q["qend"] - t0).days / 365.25
        if fam == "CAR-T":
            if not lab.empty and q["qend"] in lab.index:
                flow = np.sqrt(lab.loc[q["qend"], "inflow_low"] * lab.loc[q["qend"], "inflow_high"])
            else:
                flow = np.sqrt(r["annual_low"] * r["annual_high"])
            trailing = s[(s["qend"] <= q["qend"]) & (s["qend"] > q["qend"] - pd.Timedelta(days=366))]["patients_central"].sum()
            trailing = trailing * (4 / max(len(s[(s["qend"] <= q["qend"]) & (s["qend"] > q["qend"] - pd.Timedelta(days=366))]), 1))
            y = trailing / flow if flow > 0 else np.nan
            pool = flow
        else:
            if not lab.empty and q["qend"] in lab.index:
                pool = np.sqrt(lab.loc[q["qend"], "pool_low"] * lab.loc[q["qend"], "pool_high"])
            else:
                pool = np.sqrt(r["pool_at_last_quarter_low"] * r["pool_at_last_quarter_high"])
            cum = s[s["qend"] <= q["qend"]]["patients_central"].sum()
            y = cum / pool if pool > 0 else np.nan
        paths.append({"family": fam, "product": p, "platform_class": r["platform_class"], "series_region": region, "denominator_geography": r["denominator_geography"],
                      "quarter_end": q["qend"].date(), "t_years": round(t, 3), "pool": round(pool), "penetration": y,
                      "flag": ("worldwide series over a US flow" if (fam == "CAR-T" and region == "Total") else "") + ("; label-dated pool" if not lab.empty else "; static pool")})
paths = pd.DataFrame(paths)
paths = paths[np.isfinite(paths["penetration"]) & (paths["t_years"] > 0)]


# ---------------------------------------------------------------- fitting
def fit(t, y, prior=None, tau=TAU):
    """least squares on the share scale; if prior=(p0, q0) is given, add log-space penalties toward it"""
    def resid(th):
        p, q, c = np.exp(th[0]), np.exp(th[1]), th[2]
        r = np.log(np.maximum(y, 1e-4)) - np.log(np.maximum(c * bass(t, p, q), 1e-4))   # multiplicative errors
        if prior is not None:
            r = np.concatenate([r, [(th[0] - np.log(prior[0])) / tau * 0.1, (th[1] - np.log(prior[1])) / tau * 0.1]])
        return r
    best = None
    for p0, q0, c0 in [(0.02, 0.5, 0.5), (0.05, 0.2, 0.3), (0.01, 1.0, 0.8), (0.1, 0.05, 0.2)]:
        try:
            s = least_squares(resid, x0=[np.log(p0), np.log(q0), c0], bounds=([np.log(1e-4), np.log(1e-3), C_BOUNDS[0]], [np.log(2.0), np.log(5.0), C_BOUNDS[1]]))
            if best is None or s.cost < best.cost:
                best = s
        except Exception:
            pass
    p, q, c = np.exp(best.x[0]), np.exp(best.x[1]), best.x[2]
    return p, q, c


fits, loo, fitted_paths = [], [], []
for fam, g in paths.groupby("family"):
    prods = sorted(g["product"].unique())
    P, Q, C = fit(g["t_years"].values, g["penetration"].values)
    res = g["penetration"].values - C * bass(g["t_years"].values, P, Q)
    fits.append({"family": fam, "level": "pooled", "product": "", "n_products": len(prods), "n_points": len(g), "p_innovation": round(P, 4), "q_imitation": round(Q, 4),
                 "c_ceiling_share": round(C, 3), "rmse_share": round(float(np.sqrt(np.mean(res ** 2))), 4), "rmse_log": round(float(np.sqrt(np.mean((np.log(np.maximum(g["penetration"].values, 1e-4)) - np.log(np.maximum(C * bass(g["t_years"].values, P, Q), 1e-4))) ** 2))), 3), "peak_year_of_adoption": round(float(np.log(Q / P) / (P + Q)), 2) if Q > P else 0.0,
                 "flags": "; ".join(sorted(set(f for f in g["flag"] if f)))})
    per = {}
    for p_ in prods:
        gp = g[g["product"] == p_]
        pp, qq, cc = fit(gp["t_years"].values, gp["penetration"].values, prior=(P, Q))
        per[p_] = (pp, qq, cc)
        res = gp["penetration"].values - cc * bass(gp["t_years"].values, pp, qq)
        fits.append({"family": fam, "level": "product (shrunk)", "product": p_, "n_products": 1, "n_points": len(gp), "p_innovation": round(pp, 4), "q_imitation": round(qq, 4),
                     "c_ceiling_share": round(cc, 3), "rmse_share": round(float(np.sqrt(np.mean(res ** 2))), 4), "rmse_log": round(float(np.sqrt(np.mean((np.log(np.maximum(gp["penetration"].values, 1e-4)) - np.log(np.maximum(cc * bass(gp["t_years"].values, pp, qq), 1e-4))) ** 2))), 3), "peak_year_of_adoption": round(float(np.log(qq / pp) / (pp + qq)), 2) if qq > pp else 0.0,
                     "flags": gp["flag"].iloc[0].strip("; ")})
        for _, row in gp.iterrows():
            fitted_paths.append({**row.to_dict(), "fitted_product": cc * bass(row["t_years"], pp, qq), "fitted_pooled": C * bass(row["t_years"], P, Q)})
    # leave-one-product-out
    for p_ in prods:
        rest = g[g["product"] != p_]
        Pr, Qr, Cr = fit(rest["t_years"].values, rest["penetration"].values)
        gp = g[g["product"] == p_].sort_values("t_years")
        others = [per[o] for o in prods if o != p_]
        for h in [1, 2, 3]:
            obs = gp[(gp["t_years"] >= h - 0.13) & (gp["t_years"] <= h + 0.13)]
            if obs.empty:
                continue
            yo = float(obs["penetration"].iloc[0])
            yp = Cr * bass(h, Pr, Qr)
            spread = np.array([cc * bass(h, pp, qq) for pp, qq, cc in others])
            loo.append({"family": fam, "product": p_, "horizon_years": h, "observed": round(yo, 4), "predicted_from_others_pooled": round(yp, 4),
                        "log_error": round(float(np.log(max(yp, 1e-6) / max(yo, 1e-6))), 3),
                        "others_p10": round(float(np.percentile(spread, 10)), 4), "others_p90": round(float(np.percentile(spread, 90)), 4),
                        "covered_by_others_p10_p90": bool(np.percentile(spread, 10) <= yo <= np.percentile(spread, 90))})

# ---------------------------------------------------------------- CAR-T as a class: Bass on the registry totals (patients per year), m in patients
cbc = pd.read_csv(ROOT / "data/uptake/cart_by_country.csv", dtype=str).fillna("")
cbc["count"] = pd.to_numeric(cbc["count"], errors="coerce"); cbc["year"] = pd.to_numeric(cbc["year"], errors="coerce")
us_flow = cbc[(cbc["country"] == "US") & (cbc["eligible_low"] != "")].iloc[0]
US_FLOW = (float(us_flow["eligible_low"]), float(us_flow["eligible_high"]))
CLASS_LAUNCH = {"US": 2017.8, "Europe": 2018.65}   # first CAR-T authorisation: FDA August 2017; EC August 2018
class_rows = []
for region, sel in [("US", (cbc["country"] == "US") & (cbc["count_type"] == "infusions")), ("Europe", (cbc["country"] == "EU") & (cbc["count_type"] == "patients"))]:
    g = cbc[sel & cbc["count"].notna()].drop_duplicates("year").sort_values("year")
    g = g[g["year"] >= 2018]
    t = g["year"].values + 0.5 - CLASS_LAUNCH[region]; y = g["count"].values
    keep = t > 0.25; t, y, g = t[keep], y[keep], g[keep]   # the launch-year fraction is not a full year of activity
    def resid_m(th):
        return np.log(y) - np.log(np.maximum(th[2] * bass(t, np.exp(th[0]), np.exp(th[1])), 1.0))
    best = None
    for p0, q0, m0 in [(0.02, 0.5, 10000), (0.05, 0.3, 8000), (0.01, 0.8, 20000), (0.1, 0.1, 6000)]:
        try:
            sol = least_squares(resid_m, x0=[np.log(p0), np.log(q0), m0], bounds=([np.log(1e-4), np.log(1e-3), 500], [np.log(2.0), np.log(5.0), 200000]))
            if best is None or sol.cost < best.cost:
                best = sol
        except Exception:
            pass
    P, Q, M = np.exp(best.x[0]), np.exp(best.x[1]), best.x[2]
    # parametric bootstrap on the log residuals for the spread of m
    res = np.log(y) - np.log(np.maximum(M * bass(t, P, Q), 1.0)); ms_boot = []
    rng = np.random.default_rng(7)
    for _ in range(300):
        yb = np.exp(np.log(np.maximum(M * bass(t, P, Q), 1.0)) + rng.choice(res, size=len(res), replace=True))
        def rb(th):
            return np.log(yb) - np.log(np.maximum(th[2] * bass(t, np.exp(th[0]), np.exp(th[1])), 1.0))
        try:
            x0 = np.clip(best.x, [np.log(1e-4) + 1e-6, np.log(1e-3) + 1e-6, 501], [np.log(2.0) - 1e-6, np.log(5.0) - 1e-6, 199999])
            sb = least_squares(rb, x0=x0, bounds=([np.log(1e-4), np.log(1e-3), 500], [np.log(2.0), np.log(5.0), 200000]))
            ms_boot.append((np.exp(sb.x[0]), np.exp(sb.x[1]), sb.x[2]))
        except Exception as e:
            print("bootstrap failure:", e)
    ms_boot = np.array(ms_boot) if ms_boot else np.array([[P, Q, M]])
    flow_mid = np.sqrt(US_FLOW[0] * US_FLOW[1]) * (1.0 if region == "US" else 1.5)
    class_rows.append({"family": "CAR-T class (registry totals)", "level": f"class-{region}", "product": region, "n_products": "", "n_points": len(y), "p_innovation": round(P, 4), "q_imitation": round(Q, 4),
                       "c_ceiling_share": round(M / flow_mid, 3), "rmse_share": "", "rmse_log": round(float(np.sqrt(np.mean(res ** 2))), 3), "peak_year_of_adoption": round(float(np.log(Q / P) / (P + Q)), 2) if Q > P else 0.0,
                       "flags": f"m (ceiling, patients per year) {M:.0f}; bootstrap p10 to p90 {np.percentile(ms_boot[:, 2], 10):.0f} to {np.percentile(ms_boot[:, 2], 90):.0f}; c over the class flow mid {flow_mid:.0f} (US flow {US_FLOW[0]:.0f} to {US_FLOW[1]:.0f}; Europe = 1.5 x US)",
                       "m_patients": round(M), "m_p10": round(float(np.percentile(ms_boot[:, 2], 10))), "m_p90": round(float(np.percentile(ms_boot[:, 2], 90))),
                       "boot_p_q_m": ";".join(f"{a:.4f},{b:.4f},{c:.0f}" for a, b, c in ms_boot)})
    for yy, tt, obs in zip(g["year"].values, t, y):
        fitted_paths.append({"family": "CAR-T class (registry totals)", "product": region, "platform_class": "autologous CAR-T", "series_region": region, "denominator_geography": region,
                             "quarter_end": f"{int(yy)}-12-31", "t_years": round(float(tt), 3), "pool": round(flow_mid), "penetration": obs / flow_mid, "flag": "registry total over the class flow mid",
                             "fitted_product": M * bass(tt, P, Q) / flow_mid, "fitted_pooled": M * bass(tt, P, Q) / flow_mid})
fits += class_rows
F = pd.DataFrame(fits); L = pd.DataFrame(loo); FP = pd.DataFrame(fitted_paths)
F.to_csv(OUT / "diffusion_bass_fits.csv", index=False)
L.to_csv(OUT / "diffusion_loo.csv", index=False)
FP.to_csv(OUT / "diffusion_paths.csv", index=False)

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print("FITS"); print(F.drop(columns=["flags", "boot_p_q_m"], errors="ignore").to_string(index=False)); print(F[F["family"].str.startswith("CAR-T class")]["flags"].to_string(index=False))
print("\nLEAVE-ONE-PRODUCT-OUT")
if not L.empty:
    print(L.groupby(["family", "horizon_years"]).agg(n=("product", "size"), median_abs_log_error=("log_error", lambda s: float(np.median(np.abs(s)))),
                                                  median_log_error=("log_error", "median"), coverage=("covered_by_others_p10_p90", "mean")).round(3).to_string())
    print(L.to_string(index=False))
