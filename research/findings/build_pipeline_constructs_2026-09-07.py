"""Industry pipeline at construct level (handover item A1; replaces the sponsor x platform proxy of D013).

A construct is one named intervention of one sponsor within one platform class. Names come from the registry's
intervention field (data/projection/raw/trial_interventions.csv, fetched 2026-09-07): conditioning, comparator and
supportive agents are dropped by a stoplist; each trial is then keyed by the first development code in its names (for
example JNJ-4528, CTX001, ADVM-022), else by its target tokens (CD19, BCMA, GPC3 ...), else pooled as the sponsor's one
unnamed construct in that class, because trials named only "CAR-T cells" cannot be told apart. Trials of a construct that became
an approved product are matched with the per-product regex in data/cohort/first_in_human.csv and carry its approval date,
so approved constructs leave the pipeline at approval and post-marketing trials do not count as programmes.

Per construct: class, sponsor, key, number of trials, first trial start, earliest phase-3 start, highest phase among
active trials today (the forward pipeline), highest phase among trials started by end-2019 (the backcast pipeline),
whether any trial has a site in the United States, the EU, the EEA, Switzerland or the United Kingdom, and the approved
product it became, if any.

Also written: data/projection/phase_durations.csv, the cohort's own durations from the earliest registered phase-2 and
phase-3 trial of each product's construct to first approval (from data/cohort/raw/fih_candidates.csv), which replace the
assumed remaining-share ranges of D013.

Outputs: data/projection/pipeline_constructs.csv, data/projection/phase_durations.csv
Run from research/findings:  python3 build_pipeline_constructs_2026-09-07.py
"""
import re
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/projection"
SUBFAM = {"Engineered T-cell therapy (CAR-T)": "CAR-T", "AAV gene transfer": "AAV", "Lentiviral ex vivo gene therapy": "lentiviral ex vivo",
          "CRISPR nuclease editing": "CRISPR ex vivo", "In vivo LNP genetic medicine": "in vivo editing and LNP", "Base editing": "in vivo editing and LNP",
          "Prime editing": "in vivo editing and LNP", "Epigenome editing": "in vivo editing and LNP"}
PH = {"EARLY_PHASE1": 1, "PHASE1": 1, "PHASE1|PHASE2": 2, "PHASE2": 2, "PHASE2|PHASE3": 3, "PHASE3": 3}
ACTIVE = {"RECRUITING", "ACTIVE_NOT_RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION"}
STOP = re.compile(r"fludarabine|cyclophosphamide|bendamustine|placebo|lymphodeplet|chemotherap|tocilizumab|rituximab|pembrolizumab|nivolumab|"
                  r"aflibercept|prednis|levetiracetam|dexamethasone|methylpredni|standard|supportive|no intervention|busulfan|melphalan|"
                  r"g-csf|filgrastim|plerixafor|lenalidomide|pomalidomide|bortezomib|daratumumab|carboplatin|cisplatin|etoposide|gemcitabine|"
                  r"oxaliplatin|doxorubicin|vincristine|ifosfamide|folfox|folfiri|sham|observation|best supportive|apheresis|leukapheresis|"
                  r"bridging|conditioning|steroid|antibiotic|acyclovir|hydroxyurea|interleukin|il-2|aldesleukin|ibrutinib|acalabrutinib|"
                  r"blinatumomab|inotuzumab|ranibizumab|bevacizumab|corticosteroid|imaging|biopsy|questionnaire|test\b|assay|blood draw|"
                  r"mrd|survey|control group|usual care|natural history|saline|vehicle|diluent", re.I)
TARGETS = re.compile(r"\b(cd\d{1,3}[a-z]?|bcma|gpc3|gprc5d|cldn18\.?2|claudin ?18\.?2|msln|mesothelin|cea|her2|egfr|egfrviii|psma|muc1|muc16|"
                     r"nkg2d|gd2|b7-?h3|ror1|il13r[a-z0-9]*|dll3|fap|lewis ?y|cd19/cd22|cd19-cd22|tcr|ny-?eso|mage-?a4|wt1|hbv|hiv|"
                     r"rpe65|rpgr|cnga3|smn1?|fviii|fix|f8|f9|factor ?(viii|ix)|dmd|dystrophin|sma|ttr|pcsk9|angptl3|hbb|bcl11a|"
                     r"cftr|ush2a|abca4|chm|rep1|cln[0-9]|gba|gaa|idua|ids|sgsh|naglu|mps ?[ivx]+[a-z]?|otof|otoferlin|aspa|aadc|"
                     r"gad|nrtn|neurturin|gdnf|lpl|ada|ottc|otc|pah|g6pc|gsd|hemophilia [ab]|haemophilia [ab])\b", re.I)
CODE = re.compile(r"\b([A-Za-z]{1,7}[- ]?\d{2,6}[A-Za-z]{0,3}|[A-Za-z]{2,5}\d{1,2}[- ]?\d{2,5}|rAAV[\w.-]*|AAV\d[\w.-]*|[A-Za-z]{2,}-\d{1,3}-\d{1,4})\b")
GENERIC = re.compile(r"chimeric antigen receptor|car[- ]?t|car[- ]?nk|t[- ]?cells?|nk[- ]?cells?|autologous|allogeneic|injection|infusion|cells?\b|"
                     r"gene therapy|gene transfer|vector|adeno-?associated|lentivir\w*|targeting|targeted|anti-|therapy|product|suspension|"
                     r"intravenous|intrathecal|subretinal|intravitreal|dose|cohort|arm|low|high|mid|single|escalation|expansion|"
                     r"\d+(\.\d+)?\s?(e\d+|x ?10\^?\d+)?\s?(vg|cells?|gc)(/kg|/eye|/ml)?|\(.*?\)", re.I)


def construct_key(names):
    """reduce a trial's intervention list to one construct key: a code if any name carries one, else a target, else 'unnamed'
    (trials whose intervention name carries neither a code nor a target cannot be told apart and are pooled per sponsor)"""
    codes, targets = [], set()
    for raw in str(names).split("|"):
        n = raw.strip()
        if not n or STOP.search(n):
            continue
        cs = [c.lower().replace(" ", "-") for c in CODE.findall(n) if not re.match(r"^(phase|cohort|arm|group|day|week|month|year|part|dose|level)\s?\d", c, re.I)]
        cs = [c for c in cs if not re.match(r"^\d", c) and not re.match(r"^(cd\d+[a-z]?|il\d+|mps\d+|cln\d+)$", c)]
        codes += cs
        targets |= {m[0].lower().replace(" ", "") for m in TARGETS.findall(n)}
    if codes:
        return codes[0]
    if targets:
        return "target:" + "+".join(sorted(targets))
    return "unnamed"


# ---------------------------------------------------------------- inputs
t = pd.read_csv(ROOT / "data/primary/trial_records.csv", low_memory=False)
t = t[t["subfamily"].isin(SUBFAM) & (t["study_type"] == "INTERVENTIONAL")].drop_duplicates("nct").copy()
t["cls"] = t["subfamily"].map(SUBFAM)
ti = pd.read_csv(OUT / "raw/trial_interventions.csv", dtype=str).fillna("")
t = t.merge(ti[["nct", "intervention_names", "intervention_other_names", "countries", "has_us_or_eu_site", "start_date"]], on="nct", how="left")
t["has_us_or_eu_site"] = t["has_us_or_eu_site"].astype(str).str.lower().eq("true")
t["ph"] = t["phase"].map(PH)
t["start_dt"] = pd.to_datetime(t["start_date"].astype(str).str[:7], format="%Y-%m", errors="coerce")
t["start_y"] = t["start_dt"].dt.year + (t["start_dt"].dt.month - 0.5) / 12
ind = t[(t["sponsor_class"] == "INDUSTRY") & t["ph"].notna()].copy()
ind["keys"] = (ind["intervention_names"] + "|" + ind["intervention_other_names"].str.replace(";", "|")).map(construct_key)

# approved constructs: the per-product regex of first_in_human.csv on names and title
fih = pd.read_csv(ROOT / "data/cohort/first_in_human.csv", dtype=str).fillna("")
coh = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
coh["k"] = coh["product"].map(lambda s: re.split(r"[\s/(]", str(s).strip())[0].lower())
fa = {}
for _, r in fih.iterrows():
    fa[r["product_key"]] = pd.to_datetime(r["first_approval_date"], errors="coerce")


def approved_match(row):
    text = f'{row["intervention_names"]} {row["intervention_other_names"]} {row["title"]}'
    for _, r in fih.iterrows():
        if r["regex"] and re.search(r["regex"], text, re.I):
            return r["product_key"]
    return ""


ind["approved_product"] = ind.apply(approved_match, axis=1)
ind.loc[ind["approved_product"] != "", "keys"] = "approved:" + ind.loc[ind["approved_product"] != "", "approved_product"]

# ---------------------------------------------------------------- constructs
rows = []
ind_x = ind
for (c, sp, k), g in ind_x.groupby(["cls", "sponsor", "keys"]):
    act = g[g["status"].isin(ACTIVE)]
    by19 = g[g["start_year"] <= 2019]
    ap = [a for a in g["approved_product"].unique() if a]
    ap_key = ap[0] if ap else ""
    rows.append({"cls": c, "sponsor": sp, "construct_key": k, "n_trials": len(g), "ncts": "|".join(sorted(g["nct"])),
                 "first_start": round(float(g["start_y"].min()), 2) if g["start_y"].notna().any() else np.nan,
                 "phase3_start": round(float(g[g["ph"] == 3]["start_y"].min()), 2) if (g["ph"] == 3).any() else np.nan,
                 "highest_phase_ever": int(g["ph"].max()),
                 "phase_active_2026": int(act["ph"].max()) if not act.empty else np.nan,
                 "phase_by_2019": int(by19["ph"].max()) if not by19.empty else np.nan,
                 "first_start_by_2019": round(float(by19["start_y"].min()), 2) if by19["start_y"].notna().any() else np.nan,
                 "phase3_start_by_2019": round(float(by19[by19["ph"] == 3]["start_y"].min()), 2) if (by19["ph"] == 3).any() else np.nan,
                 "has_us_or_eu_site": bool(g["has_us_or_eu_site"].any()),
                 "approved_product": ap_key, "approval_date": fa.get(ap_key, pd.NaT).date() if ap_key and pd.notna(fa.get(ap_key, pd.NaT)) else ""})
pc = pd.DataFrame(rows).sort_values(["cls", "sponsor", "construct_key"])
pc.to_csv(OUT / "pipeline_constructs.csv", index=False)

# ---------------------------------------------------------------- the cohort's own phase durations
cand = pd.read_csv(ROOT / "data/cohort/raw/fih_candidates.csv", dtype=str).fillna("")
cand["ph"] = cand["phases"].map(PH)
cand["sd"] = pd.to_datetime(cand["start_date"].str[:7], format="%Y-%m", errors="coerce")
cand = cand[(cand["study_type"] == "INTERVENTIONAL") & cand["ph"].notna()]
dur_rows = []
for _, r in fih.iterrows():
    k = r["product_key"]
    g = cand[cand["product_key"] == k]
    fa_dt = pd.to_datetime(r["first_approval_date"], errors="coerce"); fih_dt = pd.to_datetime(r["first_in_human_date"], errors="coerce")
    p2 = g[g["ph"] >= 2]["sd"].min(); p3 = g[g["ph"] == 3]["sd"].min()
    yT = (fa_dt - fih_dt).days / 365.25 if pd.notna(fa_dt) and pd.notna(fih_dt) else np.nan
    y2 = (fa_dt - p2).days / 365.25 if pd.notna(p2) else np.nan
    y3 = (fa_dt - p3).days / 365.25 if pd.notna(p3) else np.nan
    dur_rows.append({"product_key": k, "platform_class": r["platform_class"], "first_in_human": r["first_in_human_date"], "first_approval": r["first_approval_date"],
                     "earliest_phase2_or_1_2_start": p2.date() if pd.notna(p2) else "", "earliest_phase3_start": p3.date() if pd.notna(p3) else "",
                     "years_fih_to_approval": round(yT, 2), "years_phase2_start_to_approval": round(y2, 2) if pd.notna(y2) else "",
                     "years_phase3_start_to_approval": round(y3, 2) if pd.notna(y3) else "",
                     "share_remaining_at_phase2": round(y2 / yT, 2) if pd.notna(y2) and yT > 0 else "", "share_remaining_at_phase3": round(y3 / yT, 2) if pd.notna(y3) and yT > 0 else "",
                     "note": "phase-3 start after approval (approval on phase 1/2 data; confirmatory trial)" if pd.notna(y3) and y3 < 0 else ("phase-2 start after approval" if pd.notna(y2) and y2 < 0 else "")})
pdur = pd.DataFrame(dur_rows)
pdur.to_csv(OUT / "phase_durations.csv", index=False)

# ---------------------------------------------------------------- report
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(f"industry interventional trials with a phase in the eight subfamilies: {len(ind)}; constructs: {len(pc)}; sponsors: {pc['sponsor'].nunique()}")
print("construct key type:", pc["construct_key"].map(lambda k: k.split(":")[0] if ":" in k else ("unnamed" if k == "unnamed" else "code")).value_counts().to_dict())
print("sponsors with the most constructs:", pc.groupby("sponsor").size().sort_values(ascending=False).head(12).to_dict())
print("approved constructs matched:", pc[pc["approved_product"] != ""].groupby("approved_product").size().to_dict())
for label, frame in [("sponsor x platform (D013 proxy)", None), ("construct level", pc), ("construct level, US or EU site", pc[pc["has_us_or_eu_site"]])]:
    if frame is None:
        now = ind[ind["status"].isin(ACTIVE)].groupby(["cls", "sponsor"])["ph"].max().reset_index()
        b19 = ind[ind["start_year"] <= 2019].groupby(["cls", "sponsor"])["ph"].max().reset_index()
        cn = now.groupby(["cls", "ph"]).size().unstack(fill_value=0); c19 = b19.groupby(["cls", "ph"]).size().unstack(fill_value=0)
    else:
        f_now = frame[frame["phase_active_2026"].notna() & (frame["approved_product"] == "")]
        f_19 = frame[frame["phase_by_2019"].notna() & ~((frame["approved_product"] != "") & (pd.to_datetime(frame["approval_date"], errors="coerce") < "2020-01-01"))]
        cn = f_now.groupby(["cls", "phase_active_2026"]).size().unstack(fill_value=0); c19 = f_19.groupby(["cls", "phase_by_2019"]).size().unstack(fill_value=0)
    print(f"\n{label}: programmes at phase 1 / 2 / 3, today (active) and as of end-2019")
    print(pd.concat({"2026": cn, "2019": c19}, axis=1).fillna(0).astype(int).to_string())
print("\nPHASE DURATIONS from the cohort's own trials (years to first approval): phase-2 start, phase-3 start")
print(pdur[["years_phase2_start_to_approval", "years_phase3_start_to_approval", "share_remaining_at_phase2", "share_remaining_at_phase3"]].apply(pd.to_numeric, errors="coerce").describe().round(2).to_string())
print(pdur[pdur["note"] != ""][["product_key", "years_phase3_start_to_approval", "note"]].to_string(index=False))
