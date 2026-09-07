"""Access stage as time-to-event (topic 02; supersedes the naive funded share used in D013 stage B).

Unit: product x health system. Origin: the regulatory authorisation that puts the product at risk of a funding decision
in that system (EU authorisation for England, Germany, France and Italy; Health Canada notice of compliance as stated in
the Canadian rows; TGA registration for Australia; FDA approval for the United States). Every authorised product is at
risk from its origin, including products never submitted (they are censored, not excluded).

Primary endpoint, defined once for every system: the first decision that makes the product available at public expense to
at least part of its label population. Body per system: NICE guidance (including Cancer Drugs Fund and managed access);
G-BA Beschluss; a pCPA letter of intent; for France, paid early access (ANSM acces precoce or ATU), JO inscription or a
CEPS price, whichever comes first; an AIFA determination; MSAC or PBAC support or a funding start; for the United States,
the first quarter with product revenue (no funding decision exists; F035). Routine-listing sensitivity: France without
early access (JO or CEPS only); England without managed access (routine recommendation only); other systems unchanged.

Competing events: a refusal or an appraisal terminated or withdrawn by the sponsor that is not followed by a positive step
or a live resubmission; withdrawal of the marketing authorisation. Estimators: Aalen-Johansen cumulative incidence of
funding with the competing events (primary); Kaplan-Meier with the competing events censored (upper bound, the naive
view); bootstrap over products for the 10th to 90th percentile of the share funded by 60 months.

Extension indications: where a decision row's indication carries a verified label event for the product in the EU
(data/uptake/label_events.csv), the indication-level duration is recomputed from the extension's authorisation date and
written to access_indication_durations.csv. The product-level analysis keeps the initial authorisation as origin.

Inputs : data/access/decisions.csv, data/cohort/product_cohort.csv, data/uptake/uptake_summary.csv, data/uptake/label_events.csv
Outputs: data/access/access_time_to_event.csv     one row per product x system x endpoint (origin, event, time)
         data/access/access_survival_curves.csv   step functions per system and endpoint (months, CIF funded, CIF competing, KM)
         data/access/access_survival_summary.csv  the numbers used in the paper and the projection
         data/access/access_indication_durations.csv
Run from research/findings:  python3 access_time_to_event_2026-09-07.py
"""
import re
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/access"
CUTOFF = pd.Timestamp("2026-09-05")   # last fetch date of the decision tables
rng = np.random.default_rng(20260907)
SYN = {"libmeldy": "lenmeldy", "upstaza": "kebilidi", "durveqtix": "beqvez"}


def key(name):
    k = re.split(r"[\s/(]", str(name).strip())[0].lower()
    return SYN.get(k, k)


def date(x):
    return pd.to_datetime(str(x).strip()[:10], errors="coerce") if str(x).strip() else pd.NaT


POSITIVE = {"recommended", "recommended-restricted", "recommended-managed-access"}
NEGATIVE = {"not-recommended", "terminated-or-withdrawn"}
# bodies whose positive decision opens funded access (primary) and, for the sensitivity, routine listing only
FUND = {"Canada": ["pCPA"], "England": ["NICE"], "Germany": ["G-BA"], "France": ["JO", "CEPS", "ANSM"], "Italy": ["AIFA"], "Australia": ["Funding", "PBAC", "MSAC"]}
FUND_ROUTINE = {"France": ["JO", "CEPS"]}
ROUTINE_OUTCOMES = {"England": {"recommended", "recommended-restricted"}}
# bodies whose refusal or termination closes the route (a refusal by the HTA body blocks funding in France and Canada)
CHAIN = {"Canada": ["CADTH", "CDA-AMC", "pCPA"], "England": ["NICE"], "Germany": ["G-BA"], "France": ["HAS-CT", "JO", "CEPS", "ANSM"], "Italy": ["AIFA"], "Australia": ["MSAC", "PBAC", "Funding"]}
EU_SYSTEMS = ["England", "Germany", "France", "Italy"]


def body_in(b, names):
    return any(str(b).startswith(n) for n in names)


dec = pd.read_csv(ROOT / "data/access/decisions.csv", dtype=str).fillna("")
dec["decision_dt"] = dec["decision_date"].map(date)
dec["reg_dt"] = dec["regulatory_approval_date"].map(date)
dec["usable"] = dec["usable"].astype(str).str.lower().eq("true")
coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh = coh[~coh["notes"].str.contains("out of scope")].copy()
coh["k"] = coh["product"].map(key)
coh["eu_dt"] = coh["eu_authorisation_date"].map(date)
coh["eu_wd"] = coh["eu_withdrawn_date"].map(date)
coh["fda_dt"] = coh["fda_approval_date"].map(date)
coh = coh.drop_duplicates("k").set_index("k")
ups = pd.read_csv(ROOT / "data/uptake/uptake_summary.csv", dtype=str).fillna("")
ups["k"] = ups["product"].map(key)


def qend(q):
    q = str(q)
    if not re.match(r"^\d{4}Q[1-4]$", q):
        return pd.NaT
    return pd.Period(q, freq="Q").end_time.normalize()


ups["first_rev_dt"] = ups["first_revenue_quarter"].map(qend)

# ---------------------------------------------------------------- one row per product x system x endpoint
rows = []
for endpoint in ["primary", "routine"]:
    for k, c in coh.iterrows():
        # origin per system
        origins = {}
        if pd.notna(c["eu_dt"]):
            for s in EU_SYSTEMS:
                origins[s] = (c["eu_dt"], "EU authorisation")
        for s in ["Canada", "Australia"]:
            g = dec[(dec["product_key"] == k) & (dec["system"] == s) & dec["reg_dt"].notna()]
            if s == "Australia":
                g = g[g["body"] == "TGA"] if (g["body"] == "TGA").any() else g
            if not g.empty:
                origins[s] = (g["reg_dt"].min(), "Health Canada notice of compliance (stated in the row)" if s == "Canada" else "TGA registration")
        if pd.notna(c["fda_dt"]) and k in set(ups["k"]):
            origins["United States"] = (c["fda_dt"], "FDA approval; at risk only if the sponsor reports product revenue")
        for s, (t0, basis) in origins.items():
            if t0 > CUTOFF:
                continue
            g = dec[(dec["product_key"] == k) & (dec["system"] == s) & dec["usable"]].sort_values("decision_dt")
            if s == "United States":
                fr = ups[ups["k"] == k]["first_rev_dt"].iloc[0]
                funded_dt, neg_dt, live = (fr if pd.notna(fr) else pd.NaT), pd.NaT, False
            else:
                fb = FUND_ROUTINE.get(s, FUND[s]) if endpoint == "routine" else FUND[s]
                pos_ok = ROUTINE_OUTCOMES.get(s, POSITIVE) if endpoint == "routine" else POSITIVE
                pos = g[g["body"].map(lambda b: body_in(b, fb)) & g["outcome"].isin(pos_ok)]
                funded_dt = pos["decision_dt"].min() if not pos.empty else pd.NaT
                neg = g[g["body"].map(lambda b: body_in(b, CHAIN[s])) & g["outcome"].isin(NEGATIVE)]
                neg_dt = neg["decision_dt"].min() if not neg.empty else pd.NaT
                # a refusal followed by a live resubmission (latest row under assessment) does not close the route
                latest_any = dec[(dec["product_key"] == k) & (dec["system"] == s) & dec["decision_dt"].notna()].sort_values("decision_dt")
                live = (not latest_any.empty) and latest_any.iloc[-1]["outcome"] == "under-assessment" and pd.notna(neg_dt) and latest_any.iloc[-1]["decision_dt"] > neg_dt
            wd = c["eu_wd"] if s in EU_SYSTEMS else pd.NaT
            if pd.notna(funded_dt):
                ev, ev_dt = "funded", funded_dt
            elif pd.notna(neg_dt) and not live and (pd.isna(wd) or neg_dt <= wd):
                ev, ev_dt = "refused-or-terminated", neg_dt
            elif pd.notna(wd) and wd <= CUTOFF:
                ev, ev_dt = "withdrawn-from-market", wd
            else:
                ev, ev_dt = "censored", CUTOFF
            months = max((ev_dt - t0).days / 30.44, 0.0)
            rows.append({"endpoint": endpoint, "product_key": k, "product": c["product"], "platform_class": c["platform_class"], "genetic_modification": c["genetic_modification"],
                         "system": s, "origin_date": t0.date(), "origin_basis": basis, "event": ev, "event_date": ev_dt.date(), "months": round(months, 1),
                         "n_usable_rows": int(len(g)), "first_negative_reversed": bool(pd.notna(funded_dt) and pd.notna(neg_dt) and neg_dt < funded_dt)})
tte = pd.DataFrame(rows)
tte.to_csv(OUT / "access_time_to_event.csv", index=False)


# ---------------------------------------------------------------- estimators
def aalen_johansen(times, events, grid):
    """cumulative incidence of 'funded' and of the competing events on a grid; KM of funding with competing events censored"""
    t = np.asarray(times, float); e = np.asarray(events, object)
    order = np.argsort(t); t, e = t[order], e[order]
    uniq = np.unique(t[e != "censored"])
    S, cif_f, cif_c, km = 1.0, 0.0, 0.0, 1.0
    out = []
    j = 0
    for x in grid:
        while j < len(uniq) and uniq[j] <= x:
            u = uniq[j]
            n = int((t >= u).sum())
            df = int(((t == u) & (e == "funded")).sum()); dc = int(((t == u) & (e != "funded") & (e != "censored")).sum())
            if n > 0:
                cif_f += S * df / n; cif_c += S * dc / n
                S *= (1 - (df + dc) / n)
                km *= (1 - df / n)   # competing events censored: they have already left the risk set at their own time
            j += 1
        out.append((x, cif_f, cif_c, 1 - km, int((t > x).sum())))
    return out


def km_only(times, events, grid):
    """Kaplan-Meier of funding treating every non-funding exit as censoring (the naive upper bound)"""
    t = np.asarray(times, float); e = np.asarray(events, object)
    uniq = np.unique(t[e == "funded"])
    km, out, j = 1.0, [], 0
    for x in grid:
        while j < len(uniq) and uniq[j] <= x:
            u = uniq[j]; n = int((t >= u).sum()); d = int(((t == u) & (e == "funded")).sum())
            km *= (1 - d / n) if n > 0 else 1.0
            j += 1
        out.append(1 - km)
    return out


GRID = np.arange(0, 121, 1)
curves, summary = [], []
for (endpoint, s), g in tte.groupby(["endpoint", "system"]):
    aj = aalen_johansen(g["months"].values, g["event"].values, GRID)
    kmv = km_only(g["months"].values, g["event"].values, GRID)
    for (x, cf, cc, _, nr), kv in zip(aj, kmv):
        curves.append({"endpoint": endpoint, "system": s, "months": int(x), "cif_funded": round(cf, 4), "cif_competing": round(cc, 4), "km_funded_competing_censored": round(kv, 4), "n_at_risk_after": nr})
    cf = {x: c for x, c, _, _, _ in aj}
    kmd = dict(zip(GRID, kmv))
    med = next((x for x, c, _, _, _ in aj if c >= 0.5), None)
    # bootstrap over products for the 60-month share
    b60, bmed = [], []
    prods = g["product_key"].values
    for _ in range(500):
        pick = rng.choice(len(prods), size=len(prods), replace=True)
        gb = g.iloc[pick]
        ajb = aalen_johansen(gb["months"].values, gb["event"].values, GRID)
        b60.append(ajb[60][1]); m = next((x for x, c, _, _, _ in ajb if c >= 0.5), np.nan); bmed.append(m)
    b60 = np.array(b60); bmed = np.array(bmed, float)
    summary.append({"endpoint": endpoint, "system": s, "n_at_risk": len(g), "n_funded": int((g["event"] == "funded").sum()),
                    "n_refused_or_terminated": int((g["event"] == "refused-or-terminated").sum()), "n_withdrawn": int((g["event"] == "withdrawn-from-market").sum()),
                    "n_censored": int((g["event"] == "censored").sum()), "n_first_negative_reversed": int(g["first_negative_reversed"].sum()),
                    "median_months_to_funding_aj": med if med is not None else "not reached", "median_months_p10": np.nanpercentile(bmed, 10) if np.isfinite(bmed).any() else "", "median_months_p90": np.nanpercentile(bmed, 90) if np.isfinite(bmed).any() else "",
                    "median_months_among_funded": round(float(g[g["event"] == "funded"]["months"].median()), 1) if (g["event"] == "funded").any() else "",
                    "cif_funded_12m": round(cf[12], 3), "cif_funded_24m": round(cf[24], 3), "cif_funded_36m": round(cf[36], 3), "cif_funded_60m": round(cf[60], 3),
                    "cif_funded_60m_p10": round(float(np.percentile(b60, 10)), 3), "cif_funded_60m_p90": round(float(np.percentile(b60, 90)), 3),
                    "cif_competing_60m": round({x: c for x, _, c, _, _ in aj}[60], 3), "km_funded_60m_competing_censored": round(kmd[60], 3),
                    "naive_share_funded": round(float((g["event"] == "funded").mean()), 3)})
pd.DataFrame(curves).to_csv(OUT / "access_survival_curves.csv", index=False)
summ = pd.DataFrame(summary)
summ.to_csv(OUT / "access_survival_summary.csv", index=False)

# ---------------------------------------------------------------- extension indications: durations from the extension's own authorisation
le = pd.read_csv(ROOT / "data/uptake/label_events.csv", dtype=str).fillna("")
le = le[(le["geography"] == "EU") & (le["action"] == "add") & le["status"].isin(["verified-from-source", "derived"])].copy()
le["event_dt"] = le["event_date"].map(date)
ind_rows = []
for _, r in dec[dec["usable"] & dec["system"].isin(EU_SYSTEMS)].iterrows():
    k = r["product_key"]
    init = coh.loc[k, "eu_dt"] if k in coh.index else pd.NaT
    ev = le[(le["product_key"] == k)]
    match = ev[ev["indication_key"].map(lambda s: r["indication_key"] in [a.strip() for a in s.split(";")])]
    ext_dt = match["event_dt"].min() if not match.empty else pd.NaT
    basis = "label event (EMA procedural steps)" if pd.notna(ext_dt) else "initial EU authorisation"
    origin = ext_dt if pd.notna(ext_dt) else init
    if pd.isna(origin) or pd.isna(r["decision_dt"]):
        continue
    ind_rows.append({"product_key": k, "system": r["system"], "body": r["body"], "indication_key": r["indication_key"], "decision_date": r["decision_dt"].date(), "outcome": r["outcome"],
                     "indication_authorisation_date": origin.date(), "authorisation_basis": basis, "months_stated_by_agent": r["months_approval_to_decision"],
                     "months_from_indication_authorisation": round((r["decision_dt"] - origin).days / 30.44, 1),
                     "is_extension": bool(pd.notna(ext_dt) and pd.notna(init) and ext_dt > init)})
ind = pd.DataFrame(ind_rows)
ind.to_csv(OUT / "access_indication_durations.csv", index=False)

# ---------------------------------------------------------------- report
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print("product x system rows per endpoint:", tte.groupby("endpoint").size().to_dict())
print("\nPRIMARY endpoint: events by system")
print(pd.crosstab(tte[tte["endpoint"] == "primary"]["system"], tte[tte["endpoint"] == "primary"]["event"]).to_string())
print("\nSUMMARY (primary)")
cols = ["system", "n_at_risk", "n_funded", "n_refused_or_terminated", "n_withdrawn", "n_censored", "median_months_to_funding_aj", "median_months_among_funded", "cif_funded_12m", "cif_funded_24m", "cif_funded_60m", "cif_funded_60m_p10", "cif_funded_60m_p90", "cif_competing_60m", "km_funded_60m_competing_censored", "naive_share_funded"]
print(summ[summ["endpoint"] == "primary"][cols].to_string(index=False))
print("\nSUMMARY (routine listing)")
print(summ[summ["endpoint"] == "routine"][cols].to_string(index=False))
print("\nEXTENSION INDICATIONS: rows re-dated from a label event")
if not ind.empty:
    x = ind[ind["is_extension"]]
    print(f"{len(x)} of {len(ind)} usable EU-system rows concern an extension with a verified EU label event")
    x2 = x.copy(); x2["m_agent"] = pd.to_numeric(x2["months_stated_by_agent"], errors="coerce")
    print(x2.groupby("system").agg(rows=("product_key", "size"), months_as_stated=("m_agent", "median"), months_from_extension=("months_from_indication_authorisation", "median")).round(1).to_string())
