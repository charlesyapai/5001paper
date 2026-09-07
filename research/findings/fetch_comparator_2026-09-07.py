"""Non-molecular comparator for the companion paper (D003; OPEN_ITEMS item 2): industry-sponsored halted drug trials that are
not precision-medicine trials, matched to the 144 industry-therapeutic halts on phase and start year.

Pull: ClinicalTrials.gov v2, industry lead sponsor, interventional, intervention type DRUG, status TERMINATED, WITHDRAWN or
SUSPENDED, phase 1 or 2 (early phase 1 included through the phase filter), start 2015 to 2025. Records whose title, conditions,
interventions or reason text match any genetic-medicine or AI regex of code/filter_regex.csv are excluded, as are records already in
the study's halted set. Matching: within each stratum of phase bucket (early phase 1 or phase 1; phase 1/2; phase 2 or later;
phase missing) and start-year bin (2015 to 2018, 2019 to 2021, 2022 to 2025) up to three comparators are drawn at random without
replacement for each halted-cell trial (seed 20260907).

Outputs: data/companion/raw/comparator_pull.csv          every eligible record with its reason text
         data/companion/comparator_matched.csv           the matched sample with stratum, keyword flags (same patterns as 02_classify_halts.py)
         data/companion/comparator_strings_to_code.csv   distinct reason strings of the matched sample, for the fixed-schema classification
Run from research/findings:  python3 fetch_comparator_2026-09-07.py [--no-fetch]   (--no-fetch reuses the saved pull)
"""
import re, sys, time
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/companion"; (OUT / "raw").mkdir(parents=True, exist_ok=True)
API = "https://clinicaltrials.gov/api/v2/studies"
QUERY = ("AREA[LeadSponsorClass]INDUSTRY AND AREA[StudyType]INTERVENTIONAL AND AREA[InterventionType]DRUG AND "
         "(AREA[OverallStatus]TERMINATED OR AREA[OverallStatus]WITHDRAWN OR AREA[OverallStatus]SUSPENDED) AND "
         "AREA[StartDate]RANGE[2015-01-01,2025-12-31] AND (AREA[Phase]PHASE1 OR AREA[Phase]PHASE2)")
FIELDS = "NCTId|BriefTitle|OverallStatus|Phase|StartDate|LeadSponsorName|LeadSponsorClass|Condition|InterventionName|WhyStopped|EnrollmentCount"
# the audit patterns are imported from code/02_classify_halts.py so the flags are identical to the published ones
import importlib.util
_spec = importlib.util.spec_from_file_location("classify_halts", ROOT / "code/02_classify_halts.py"); _m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
PAT_FINANCIAL, PAT_FIN_OR_BIZ, PAT_DENIES_SAFETY, CATEGORIES = _m.PAT_FINANCIAL, _m.PAT_FIN_OR_BIZ, _m.PAT_DENIES_SAFETY, _m.CATEGORIES
NO_FETCH = "--no-fetch" in sys.argv   # reuse data/companion/raw/comparator_pull.csv

rx = pd.read_csv(ROOT / "code/filter_regex.csv")
EXCLUDE = re.compile("|".join(f"(?:{r})" for r in rx["retained_if_regex_matches"]) + r"|gene therap|cell therap|CAR-?T|T-?cell|antisense|siRNA|mRNA|oligonucleotide|biomarker-selected|mutation-positive", re.I)

rows, token = [], None
while not NO_FETCH:
    params = {"filter.advanced": QUERY, "fields": FIELDS, "pageSize": 1000, "countTotal": "true"}
    if token:
        params["pageToken"] = token
    for attempt in range(4):
        try:
            r = requests.get(API, params=params, timeout=90); r.raise_for_status(); break
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(5 * (attempt + 1))
    else:
        raise SystemExit("fetch failed")
    js = r.json()
    for s in js.get("studies", []):
        p = s["protocolSection"]
        rows.append({"nct": p["identificationModule"]["nctId"], "title": p["identificationModule"].get("briefTitle", ""),
                     "status": p["statusModule"].get("overallStatus"), "start_date": (p["statusModule"].get("startDateStruct") or {}).get("date", ""),
                     "why": p["statusModule"].get("whyStopped", ""), "phase": "|".join((p.get("designModule") or {}).get("phases", []) or []),
                     "enrollment": ((p.get("designModule") or {}).get("enrollmentInfo") or {}).get("count", ""),
                     "sponsor": (p.get("sponsorCollaboratorsModule", {}).get("leadSponsor") or {}).get("name", ""),
                     "sponsor_class": (p.get("sponsorCollaboratorsModule", {}).get("leadSponsor") or {}).get("class", ""),
                     "conditions": "|".join((p.get("conditionsModule") or {}).get("conditions", []) or []),
                     "interventions": "|".join(iv.get("name", "") for iv in (p.get("armsInterventionsModule") or {}).get("interventions", []) or [])})
    print(f"{len(rows)} / {js.get('totalCount')}", end="\r")
    token = js.get("nextPageToken")
    if not token:
        break
    time.sleep(0.5)
if NO_FETCH:
    pull = pd.read_csv(OUT / "raw/comparator_pull.csv", dtype=str).fillna("")
else:
    pull = pd.DataFrame(rows).drop_duplicates("nct")
    pull["fetched_date"] = date.today().isoformat()
text = pull["title"] + " " + pull["conditions"] + " " + pull["interventions"] + " " + pull["why"].fillna("")
pull["precision_medicine_match"] = text.str.contains(EXCLUDE)
halted = pd.read_csv(ROOT / "data/primary/halted_trials_dedup.csv", low_memory=False)
pull["in_study_halted_set"] = pull["nct"].isin(halted["nct"])
if not NO_FETCH:
    pull.to_csv(OUT / "raw/comparator_pull.csv", index=False)
elig = pull[~pull["precision_medicine_match"] & ~pull["in_study_halted_set"]].copy()


def bucket(ph):
    ph = str(ph)
    if ph in ("", "nan", "NA"): return "phase missing"
    if ph in ("EARLY_PHASE1", "PHASE1"): return "phase 1"
    if ph == "PHASE1|PHASE2": return "phase 1/2"
    return "phase 2 or later"


def ybin(y):
    y = float(y) if pd.notna(y) and str(y) not in ("", "nan") else np.nan
    if np.isnan(y): return "year missing"
    return "2015-2018" if y <= 2018 else ("2019-2021" if y <= 2021 else "2022-2025")


elig["start_year"] = pd.to_numeric(elig["start_date"].str[:4], errors="coerce")
elig["stratum"] = elig["phase"].map(bucket) + " x " + elig["start_year"].map(ybin)
cell = halted[(halted["sponsor_class"] == "INDUSTRY") & (halted["modality"] == "Therapeutic")].copy()
cell["stratum"] = cell["phase"].map(bucket) + " x " + cell["start_year"].map(ybin)
rng = np.random.default_rng(20260907)
picks = []
for st, n in cell["stratum"].value_counts().items():
    pool = elig[elig["stratum"] == st]
    k = min(3 * n, len(pool))
    if k == 0:
        print(f"no comparator for stratum {st} (cell n={n})"); continue
    picks.append(pool.sample(n=k, random_state=int(rng.integers(1e9))).assign(cell_n=n))
m = pd.concat(picks)
why = m["why"].fillna("").astype(str)
m["has_reason"] = why.str.strip() != ""
m["names_financial_cause"] = why.str.contains(PAT_FINANCIAL, case=False, regex=True)
m["names_financial_or_business"] = why.str.contains(PAT_FIN_OR_BIZ, case=False, regex=True)
m["denies_safety_cause"] = why.str.contains(PAT_DENIES_SAFETY, case=False, regex=True)
m.to_csv(OUT / "comparator_matched.csv", index=False)
strings = sorted({s.strip() for s in why if s.strip()})
pd.DataFrame({"why": strings}).to_csv(OUT / "comparator_strings_to_code.csv", index=False)

pd.set_option("display.width", 250)
print(f"\npull: {len(pull)} records; precision-medicine matches excluded: {int(pull['precision_medicine_match'].sum())}; already in the halted set: {int(pull['in_study_halted_set'].sum())}; eligible: {len(elig)}")
print(f"matched sample: {len(m)} comparators for {len(cell)} cell trials across {m['stratum'].nunique()} strata; distinct reason strings: {len(strings)}")
print("\nstrata (cell n, comparators drawn):")
print(pd.concat([cell["stratum"].value_counts().rename("cell"), m["stratum"].value_counts().rename("comparators")], axis=1).fillna(0).astype(int).to_string())
print("\nkeyword flags, cell versus comparators (share of trials):")
for col in ["has_reason", "names_financial_or_business", "names_financial_cause", "denies_safety_cause"]:
    cv = cell["why"].fillna("").astype(str).str.strip().ne("").mean() if col == "has_reason" else cell[col].mean()
    print(f"  {col:32s} cell {cv:.3f}   comparators {m[col].mean():.3f}")
