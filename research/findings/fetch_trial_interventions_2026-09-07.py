"""Fetch intervention names, other names, site countries and sponsor for every interventional trial in the eight genetic
subfamilies of data/primary/trial_records.csv, from the ClinicalTrials.gov v2 API by NCT id (the bundle's trial_records.csv
kept neither field). Used to rebuild the projection pipeline at construct level (handover item A1).

Output: data/projection/raw/trial_interventions.csv  one row per trial: nct, status, start_date, phases, sponsor, sponsor_class,
        intervention_names (|-separated), intervention_other_names, n_sites, countries (|-separated unique), has_us_or_eu_site,
        fetched_date
Run from research/findings:  python3 fetch_trial_interventions_2026-09-07.py
"""
import time, sys
from datetime import date
from pathlib import Path
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/projection/raw"
OUT.mkdir(parents=True, exist_ok=True)
API = "https://clinicaltrials.gov/api/v2/studies"
FIELDS = "NCTId|InterventionName|InterventionOtherName|LocationCountry|Phase|OverallStatus|StartDate|LeadSponsorName|LeadSponsorClass"
SUB = {"Engineered T-cell therapy (CAR-T)", "AAV gene transfer", "Lentiviral ex vivo gene therapy", "CRISPR nuclease editing",
       "In vivo LNP genetic medicine", "Base editing", "Prime editing", "Epigenome editing"}
EU = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
      "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
      "Spain", "Sweden", "United Kingdom", "Norway", "Iceland", "Switzerland"}

t = pd.read_csv(ROOT / "data/primary/trial_records.csv", low_memory=False)
ids = sorted(t[t["subfamily"].isin(SUB) & (t["study_type"] == "INTERVENTIONAL")]["nct"].dropna().unique())
print(f"{len(ids)} trials to fetch")
rows, today = [], date.today().isoformat()
for i in range(0, len(ids), 100):
    batch = ids[i:i + 100]
    for attempt in range(4):
        try:
            r = requests.get(API, params={"filter.ids": ",".join(batch), "fields": FIELDS, "pageSize": 100}, timeout=60)
            r.raise_for_status()
            break
        except Exception as e:
            print("retry", i, e, file=sys.stderr); time.sleep(5 * (attempt + 1))
    else:
        raise SystemExit(f"batch at {i} failed")
    for s in r.json().get("studies", []):
        p = s.get("protocolSection", {})
        ivs = (p.get("armsInterventionsModule", {}) or {}).get("interventions", []) or []
        locs = (p.get("contactsLocationsModule", {}) or {}).get("locations", []) or []
        countries = sorted({l.get("country", "") for l in locs if l.get("country")})
        rows.append({"nct": p.get("identificationModule", {}).get("nctId"), "status": p.get("statusModule", {}).get("overallStatus"),
                     "start_date": (p.get("statusModule", {}).get("startDateStruct", {}) or {}).get("date"),
                     "phases": "|".join(p.get("designModule", {}).get("phases", []) or []),
                     "sponsor": (p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}) or {}).get("name"),
                     "sponsor_class": (p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}) or {}).get("class"),
                     "intervention_names": "|".join(iv.get("name", "") for iv in ivs),
                     "intervention_other_names": "|".join(";".join(iv.get("otherNames", []) or []) for iv in ivs),
                     "n_sites": len(locs), "countries": "|".join(countries),
                     "has_us_or_eu_site": bool({"United States"} & set(countries)) or bool(EU & set(countries)),
                     "fetched_date": today})
    print(f"{i + len(batch)} / {len(ids)}", end="\r")
    time.sleep(0.5)
df = pd.DataFrame(rows)
df.to_csv(OUT / "trial_interventions.csv", index=False)
print(f"\nwrote {len(df)} rows; missing from the API: {len(set(ids) - set(df['nct']))}")
