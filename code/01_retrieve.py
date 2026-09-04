#!/usr/bin/env python3
"""
01_retrieve.py — pull ClinicalTrials.gov v2 records for each technology subfamily
and re-filter them with a literal regex.

WHY THE REGEX STEP EXISTS (do not remove it)
--------------------------------------------
ClinicalTrials.gov's `query.term` applies concept expansion. A quoted phrase does
NOT restrict to that phrase. The clearest case: '"lentiviral" OR "lentivirus"'
returns ~7,300 studies of which only ~280 concern lentiviral vectors — the rest are
HIV trials matched through a lentivirus->HIV concept link. Every record returned must
therefore be re-checked against a literal, case-insensitive pattern over the trial's
own free text before it is retained. Retention varies enormously by subfamily and is
the single most important quality figure in this pipeline; it is printed per subfamily.

FIELD NAMES
-----------
The v2 API uses SINGULAR field names. `Phase` and `Condition` are valid;
`Phases` and `Conditions` return HTTP 400.

Usage:  python 01_retrieve.py [--out ../data/primary/trial_records_refreshed.csv]
"""
import argparse, json, os, re, sys, time
import pandas as pd
import requests

API = "https://clinicaltrials.gov/api/v2/studies"
FIELDS = ("NCTId|BriefTitle|OverallStatus|Phase|StudyType|StartDate|PrimaryCompletionDate|"
          "LeadSponsorName|LeadSponsorClass|Condition|InterventionName|EnrollmentCount|"
          "BriefSummary|DetailedDescription|Keyword|InterventionOtherName|WhyStopped|"
          "StdAge|DesignAllocation|HasResults|DesignInterventionModel|LocationCountry")
HERE = os.path.dirname(os.path.abspath(__file__))


def load_spec():
    q = pd.read_csv(os.path.join(HERE, "queries.csv"))
    rx = pd.read_csv(os.path.join(HERE, "filter_regex.csv"))
    rx = dict(zip(rx.subfamily, rx.retained_if_regex_matches))
    # the AI-originated-candidate row is a named-molecule probe, not a term query
    q = q[q.ctgov_query.str.startswith('"')]
    return q, rx


def pull(term, page_size=1000, cap=20000, pause=0.2):
    out, token = [], None
    while True:
        params = {"query.term": term, "pageSize": page_size, "fields": FIELDS}
        if token:
            params["pageToken"] = token
        r = requests.get(API, params=params, timeout=180)
        r.raise_for_status()
        j = r.json()
        out += j.get("studies", [])
        token = j.get("nextPageToken")
        if not token or len(out) >= cap:
            break
        time.sleep(pause)
    return out


def flatten(study, subfamily, family, modality):
    ps = study["protocolSection"]
    idm, sm = ps["identificationModule"], ps.get("statusModule", {})
    dm, eg = ps.get("designModule", {}), ps.get("eligibilityModule", {})
    sp = ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
    ivs, other = [], []
    for iv in (ps.get("armsInterventionsModule", {}).get("interventions", []) or []):
        ivs.append(iv.get("name", ""))
        other += (iv.get("otherNames", []) or [])
    countries = sorted({l.get("country") for l in
                        (ps.get("contactsLocationsModule", {}).get("locations", []) or [])
                        if l.get("country")})
    blob = " ".join([idm.get("briefTitle", ""),
                     ps.get("descriptionModule", {}).get("briefSummary", "") or "",
                     ps.get("descriptionModule", {}).get("detailedDescription", "") or "",
                     " ".join(ps.get("conditionsModule", {}).get("keywords", []) or []),
                     " ".join(ivs), " ".join(other)])
    return dict(
        nct=idm["nctId"], family=family, subfamily=subfamily, modality=modality,
        title=idm.get("briefTitle"), status=sm.get("overallStatus"),
        start=sm.get("startDateStruct", {}).get("date"),
        prim_compl=sm.get("primaryCompletionDateStruct", {}).get("date"),
        study_type=dm.get("studyType"),
        phase="|".join(dm.get("phases", []) or []),
        enrollment=(dm.get("enrollmentInfo", {}) or {}).get("count"),
        sponsor=sp.get("name"), sponsor_class=sp.get("class"),
        conditions="; ".join(ps.get("conditionsModule", {}).get("conditions", []) or []),
        std_age="|".join(eg.get("stdAges", []) or []),
        alloc=(dm.get("designInfo", {}) or {}).get("allocation"),
        model=(dm.get("designInfo", {}) or {}).get("interventionModel"),
        has_results=bool(study.get("hasResults")),
        why=sm.get("whyStopped"),
        countries="|".join(countries),
        _blob=blob, _iv_text=" ".join(ivs + other),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "..", "data", "primary",
                                                  "trial_records_refreshed.csv"))
    args = ap.parse_args()

    spec, rx = load_spec()
    rows, report = [], []
    for _, s in spec.iterrows():
        pat = rx.get(s.subfamily)
        if not pat:
            print(f"!! no regex for {s.subfamily}; skipped", file=sys.stderr)
            continue
        studies = pull(s.ctgov_query)
        kept = 0
        for st in studies:
            f = flatten(st, s.subfamily, s.family, s.modality)
            if re.search(pat, f["_blob"], re.I):
                # intervention-role flag: is the technology the intervention, or context?
                f["driver"] = bool(re.search(pat, f["_iv_text"] + " " + (f["title"] or ""), re.I))
                rows.append(f)
                kept += 1
        report.append(dict(subfamily=s.subfamily, returned=len(studies), retained=kept,
                           retention=round(kept / max(len(studies), 1), 3)))
        print(f"{s.subfamily:42s} returned {len(studies):6d}  retained {kept:6d} "
              f"({kept/max(len(studies),1):.0%})", flush=True)

    df = pd.DataFrame(rows).drop(columns=["_blob", "_iv_text"])
    df["start_year"] = pd.to_datetime(df.start, errors="coerce", format="mixed").dt.year
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    df.to_csv(args.out, index=False)
    pd.DataFrame(report).to_csv(os.path.abspath(args.out).replace(".csv", "_retention.csv"),
                                index=False)
    print(f"\nwrote {len(df)} rows ({df.nct.nunique()} unique NCT) -> {args.out}")
    print("NOTE: subfamily queries overlap. Deduplicate by NCT before counting; "
          "in the published run 33 registrations matched two subfamilies.")


if __name__ == "__main__":
    main()
