"""First-in-human date per cohort product from ClinicalTrials.gov v2 (topic 01 task 4).

For each product: query the registry for the asset's names and code names (query.intr, optionally
restricted by sponsor), keep interventional studies whose intervention names or titles match the
literal regex (the registry's concept expansion would otherwise pull in unrelated studies; see the
bundle README point 1), and take the earliest start date. Where the construct's first clinical use
was an academic trial under a different name, that trial is listed as origin_nct and fetched by id;
the first-in-human date is the earlier of the two. Every row records the NCT id so it can be checked.

Outputs: data/cohort/first_in_human.csv          one row per product with dates and durations
         data/cohort/raw/fih_candidates.csv      every matched interventional study, for audit

Run from research/findings:  python3 first_in_human_2026-09-04.py
"""
import re, time
from pathlib import Path
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
API = "https://clinicaltrials.gov/api/v2/studies"
FIELDS = "NCTId,BriefTitle,OfficialTitle,StartDate,Phase,StudyType,OverallStatus,LeadSponsorName,InterventionName"
FETCHED = "2026-09-04"

# product_key, search terms (OR), literal regex, sponsor filter, origin NCT ids (academic first use), note
P = [
    ("kymriah", ["tisagenlecleucel", "CTL019", "CART-19"], r"tisagenlecleucel|CTL-?019|CART-?19\b", None, ["NCT01029366"], "Penn CART-19 trial is the construct's first clinical use"),
    ("yescarta", ["axicabtagene ciloleucel", "KTE-C19"], r"axicabtagene|KTE-?C19|axi-cel", None, ["NCT00924326"], "NCI anti-CD19 CAR (FMC63-CD28) trial licensed to Kite is the construct's first clinical use"),
    ("tecartus", ["brexucabtagene autoleucel", "KTE-X19"], r"brexucabtagene|KTE-?X19", None, [], "same CAR as Yescarta with a different manufacturing process; dated from its own first trial"),
    ("breyanzi", ["lisocabtagene maraleucel", "JCAR017"], r"lisocabtagene|JCAR-?017|liso-cel", None, ["NCT02631044"], ""),
    ("abecma", ["idecabtagene vicleucel", "bb2121"], r"idecabtagene|bb2121|ide-cel", None, ["NCT02658929"], ""),
    ("carvykti", ["ciltacabtagene autoleucel", "LCAR-B38M", "JNJ-68284528"], r"ciltacabtagene|LCAR-?B38M|JNJ-?68284528|cilta-cel|JNJ-?4528", None, ["NCT03090659"], "LEGEND-2 in China is the construct's first clinical use"),
    ("aucatzyl", ["obecabtagene autoleucel", "AUTO1"], r"obecabtagene|AUTO1\b|obe-cel|CAT-?19", "Autolus", ["NCT02443831"], "CARPALL (UCL, paediatric) used the CAT CAR before ALLCAR19"),
    ("luxturna", ["voretigene neparvovec", "AAV2-hRPE65v2", "SPK-RPE65"], r"voretigene|hRPE65v2|SPK-?RPE65|rAAV2-?hRPE65", None, ["NCT00516477"], "CHOP phase 1 (2007) is the construct's first clinical use"),
    ("zolgensma", ["onasemnogene abeparvovec", "AVXS-101"], r"onasemnogene|AVXS-?101|scAAV9\.CB\.SMN", None, ["NCT02122952"], "Nationwide Children's phase 1 (2014)"),
    ("itvisma", ["OAV101", "AVXS-101 intrathecal", "onasemnogene abeparvovec intrathecal"], r"OAV-?101|intrathecal", "Novartis", ["NCT03381729"], "STRONG (intrathecal AVXS-101) 2017"),
    ("hemgenix", ["etranacogene dezaparvovec", "AMT-061"], r"etranacogene|AMT-?061", None, [], "dated from AMT-061 (Padua variant); the predecessor AMT-060 (wild-type FIX, NCT02396342, 2015-06) is a different construct"),
    ("beqvez", ["fidanacogene elaparvovec", "SPK-9001", "PF-06838435"], r"fidanacogene|SPK-?9001|PF-?06838435", None, [], ""),
    ("roctavian", ["valoctocogene roxaparvovec", "BMN 270"], r"valoctocogene|BMN\s?270", None, [], ""),
    ("casgevy", ["exagamglogene autotemcel", "CTX001"], r"exagamglogene|CTX-?001|exa-cel", None, [], ""),
    ("lyfgenia", ["lovotibeglogene autotemcel", "bb1111", "LentiGlobin"], r"lovotibeglogene|bb1111|lovo-cel|LentiGlobin", None, ["NCT02140554"], "HGB-206 (LentiGlobin BB305 in sickle cell disease) is the product's first trial"),
    ("zynteglo", ["betibeglogene autotemcel", "LentiGlobin BB305"], r"betibeglogene|beti-cel|BB305|LentiGlobin", None, ["NCT01745120"], "HGB-204 (2013); the 2007 French LG001 trial used an earlier vector and is not registered"),
    ("skysona", ["elivaldogene autotemcel", "Lenti-D"], r"elivaldogene|eli-cel|Lenti-?D", None, ["NCT01896102"], "ALD-102 (2013)"),
    ("lenmeldy", ["atidarsagene autotemcel", "OTL-200", "GSK2696274"], r"atidarsagene|OTL-?200|GSK-?2696274|arsa-cel", None, ["NCT01560182"], "TIGET phase 1/2 (2010)"),
    ("kebilidi", ["eladocagene exuparvovec", "AAV2-hAADC", "AGIL-AADC"], r"eladocagene|hAADC|AGIL-?AADC|PTC-?AADC", None, ["NCT01395641"], "registry start 2014-10 for the Taiwan phase 1/2; the first four patients were treated in 2010 under compassionate use (Hwu et al., Sci Transl Med 2012), so the true first-in-human is about four years earlier"),
    ("elevidys", ["delandistrogene moxeparvovec", "SRP-9001"], r"delandistrogene|SRP-?9001|rAAVrh74\.MHCK7", None, ["NCT03375164"], ""),
    ("vyjuvek", ["beremagene geperpavec", "B-VEC", "KB103"], r"beremagene|B-?VEC|KB-?103", None, [], ""),
    ("zevaskyn", ["prademagene zamikeracel", "EB-101"], r"prademagene|EB-?101|COL7A1", "Abeona", ["NCT01263379"], "Stanford phase 1 of LZRSE-COL7A1 keratinocyte sheets (2010)"),
    ("papzimeos", ["zopapogene imadenovec", "PRGN-2012"], r"zopapogene|PRGN-?2012", None, [], ""),
    ("adstiladrin", ["nadofaragene firadenovec", "rAd-IFN/Syn3", "Instiladrin", "SCH 721015"], r"nadofaragene|rAd-?IFN|Instiladrin|Adstiladrin|SCH\s?721015|Ad-IFN", None, ["NCT01162785"], "SCH 721015 (Ad-IFNa) phase 1b at MD Anderson (2011); the first phase 1 (2004 to 2006) is unregistered"),
    ("imlygic", ["talimogene laherparepvec", "OncoVEX", "T-VEC"], r"talimogene|OncoVEX|T-?VEC\b", None, [], ""),
    ("tudriqev", ["vusolimogene oderparepvec", "RP1"], r"vusolimogene|\bRP-?1\b", "Replimune", [], ""),
    ("tecelra", ["afamitresgene autoleucel", "ADP-A2M4"], r"afamitresgene|ADP-?A2M4|afami-cel|MAGE-A4\S*T\b", "Adaptimmune|USWM", ["NCT03132922"], "ADP-A2M4 phase 1 basket (2017) is registered under the MAGE-A4 TCR name and a successor sponsor"),
    ("amtagvi", ["lifileucel", "LN-144"], r"lifileucel|LN-?144", None, [], ""),
    ("provenge", ["sipuleucel-T", "APC8015", "Provenge"], r"sipuleucel|APC-?8015|Provenge", None, [], "registry began in 2000; the 1996 to 1998 phase 1 and 2 trials are unregistered"),
    ("ryoncil", ["remestemcel-L", "Prochymal"], r"remestemcel|Prochymal", None, [], ""),
    ("omisirge", ["omidubicel", "NiCord"], r"omidubicel|NiCord", None, [], ""),
    ("lantidra", ["donislecel", "Lantidra"], r"donislecel|Lantidra|islet", "CellTrans", ["NCT00566813"], "University of Illinois islet transplant trial (2004) is the product's origin"),
    ("tregzi", ["Orca-T"], r"Orca-?T\b", None, [], ""),
    ("waskyra", ["etuvetidigene autotemcel", "OTL-103", "GSK2696275"], r"etuvetidigene|OTL-?103|GSK-?2696275|Wiskott", "Telethon", ["NCT01515462"], "TIGET phase 1/2 (2010)"),
    ("kresladi", ["marnetegragene autotemcel", "RP-L201"], r"marnetegragene|RP-?L201", None, [], ""),
    ("otarmeni", ["DB-OTO"], r"DB-?OTO", None, [], ""),
    ("genglycos", ["DTX401"], r"DTX-?401", None, [], ""),
    ("encelto", ["revakinagene taroretcel", "NT-501"], r"revakinagene|NT-?501", None, [], "NT-501 was first tested in retinitis pigmentosa (2007) before macular telangiectasia"),
    ("strimvelis", ["GSK2696273", "Strimvelis"], r"GSK-?2696273|Strimvelis|ADA-?SCID", "Telethon", ["NCT00598481"], "TIGET ADA-SCID trial (2000)"),
    ("glybera", ["alipogene tiparvovec", "AMT-011"], r"alipogene|AMT-?011|Glybera", None, [], ""),
    ("zalmoxis", ["Zalmoxis", "HSV-TK"], r"Zalmoxis|HSV-?TK", "AGC Biologics", ["NCT00423124"], "MolMed became AGC Biologics; TK007 (2002) is the origin"),
    ("alofisel", ["darvadstrocel", "Cx601"], r"darvadstrocel|Cx-?601|Alofisel", None, [], ""),
    ("ebvallo", ["tabelecleucel", "ATA129"], r"tabelecleucel|ATA-?129|EBV-?specific", None, ["NCT00002663"], "MSK EBV-specific T-cell trials of the 1990s are the origin; unregistered before 1999"),
]


def get(params):
    r = None
    for attempt in range(4):
        r = requests.get(API, params=params, timeout=60, headers={"User-Agent": "phm5001-research"})
        if r.status_code == 200:
            return r.json()
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"API failed: {r.status_code} {r.text[:200]}")


def flatten(st):
    ps = st.get("protocolSection", {})
    ident, status, design = ps.get("identificationModule", {}), ps.get("statusModule", {}), ps.get("designModule", {})
    ivs = ps.get("armsInterventionsModule", {}).get("interventions", []) or []
    return {"nct": ident.get("nctId", ""), "brief_title": ident.get("briefTitle", ""), "official_title": ident.get("officialTitle", ""),
            "start_date": status.get("startDateStruct", {}).get("date", ""), "status": status.get("overallStatus", ""),
            "study_type": design.get("studyType", ""), "phases": "|".join(design.get("phases", []) or []),
            "sponsor": ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", ""),
            "interventions": "|".join(i.get("name", "") for i in ivs)}


def to_date(s):
    if not s:
        return pd.NaT
    return pd.to_datetime(s if len(s) > 7 else s + "-01", errors="coerce")


cohort = pd.read_csv(ROOT / "data/cohort/product_cohort.csv", dtype=str).fillna("")
cohort["key"] = cohort["product"].str.split(r"[\s/(]").str[0].str.lower()
cohort = cohort.drop_duplicates("key").set_index("key")

cands, rows = [], []
for key, terms, rx, spons, origins, note in P:
    q = {"query.intr": " OR ".join(f'"{t}"' if " " in t else t for t in terms), "fields": FIELDS, "pageSize": 1000, "countTotal": "true"}
    if spons:
        q["query.spons"] = spons
    studies, token = [], None
    while True:
        if token:
            q["pageToken"] = token
        j = get(q)
        studies += [flatten(s) for s in j.get("studies", [])]
        token = j.get("nextPageToken")
        if not token:
            break
    pat = re.compile(rx, re.I)
    matched = [s for s in studies if s["study_type"] == "INTERVENTIONAL" and (pat.search(s["interventions"]) or pat.search(s["brief_title"]) or pat.search(s["official_title"]))]
    for s in matched:
        cands.append({"product_key": key, **s, "matched_by": "search"})
    with_date = [(to_date(s["start_date"]), s) for s in matched if pd.notna(to_date(s["start_date"]))]
    auto = min(with_date, key=lambda x: x[0]) if with_date else (pd.NaT, {})
    orig = (pd.NaT, {})
    for o in origins:
        j = get({"query.id": o, "fields": FIELDS})
        st = [flatten(s) for s in j.get("studies", [])]
        if st:
            s = st[0]
            cands.append({"product_key": key, **s, "matched_by": "origin_nct"})
            d = to_date(s["start_date"])
            if pd.notna(d) and (pd.isna(orig[0]) or d < orig[0]):
                orig = (d, s)
    fih = min([d for d in [auto[0], orig[0]] if pd.notna(d)], default=pd.NaT)
    src = auto[1] if pd.notna(auto[0]) and (pd.isna(orig[0]) or auto[0] <= orig[0]) else orig[1]
    c = cohort.loc[key] if key in cohort.index else None
    fda = to_date(c["fda_approval_date"]) if c is not None else pd.NaT
    eu = to_date(c["eu_authorisation_date"]) if c is not None else pd.NaT
    first_appr = min([d for d in [fda, eu] if pd.notna(d)], default=pd.NaT)
    flags = []
    if src and src.get("phases", "") and not re.search(r"PHASE1|EARLY_PHASE1", src.get("phases", "")):
        flags.append(f"earliest matched trial is {src.get('phases')}: an earlier unregistered phase 1 is possible")
    if not matched:
        flags.append("no registry match for the search terms")
    rows.append({"product_key": key, "cohort_product": c["product"] if c is not None else "", "platform_class": c["platform_class"] if c is not None else "",
                 "search_terms": " OR ".join(terms), "regex": rx, "sponsor_filter": spons or "", "n_matched_interventional": len(matched),
                 "auto_earliest_nct": auto[1].get("nct", ""), "auto_earliest_start": auto[0].date() if pd.notna(auto[0]) else "",
                 "auto_earliest_phase": auto[1].get("phases", ""), "auto_earliest_sponsor": auto[1].get("sponsor", ""), "auto_earliest_title": auto[1].get("brief_title", ""),
                 "origin_nct": orig[1].get("nct", ""), "origin_start": orig[0].date() if pd.notna(orig[0]) else "", "origin_sponsor": orig[1].get("sponsor", ""), "origin_title": orig[1].get("brief_title", ""),
                 "first_in_human_date": fih.date() if pd.notna(fih) else "", "first_in_human_nct": src.get("nct", "") if src else "",
                 "fda_approval_date": fda.date() if pd.notna(fda) else "", "eu_authorisation_date": eu.date() if pd.notna(eu) else "",
                 "first_approval_date": first_appr.date() if pd.notna(first_appr) else "",
                 "years_fih_to_first_approval": round((first_appr - fih).days / 365.25, 2) if pd.notna(fih) and pd.notna(first_appr) else "",
                 "years_fih_to_fda": round((fda - fih).days / 365.25, 2) if pd.notna(fih) and pd.notna(fda) else "",
                 "status": "verified-from-data" if pd.notna(fih) else "not-found", "fetched": FETCHED, "flags": "; ".join(flags), "notes": note})
    print(f"{key:12s} matched {len(matched):3d}  auto {auto[1].get('nct',''):11s} {str(auto[0].date()) if pd.notna(auto[0]) else '':10s}  origin {orig[1].get('nct',''):11s} {str(orig[0].date()) if pd.notna(orig[0]) else '':10s}  FIH {str(fih.date()) if pd.notna(fih) else 'NA':10s}  first approval {str(first_appr.date()) if pd.notna(first_appr) else 'NA'}", flush=True)
    time.sleep(0.3)

out = pd.DataFrame(rows)
out.to_csv(ROOT / "data/cohort/first_in_human.csv", index=False)
pd.DataFrame(cands).to_csv(ROOT / "data/cohort/raw/fih_candidates.csv", index=False)
ok = out[out["years_fih_to_first_approval"] != ""].copy()
ok["y"] = ok["years_fih_to_first_approval"].astype(float)
print(f"\nproducts dated: {len(ok)} of {len(out)}; median years first-in-human to first approval {ok['y'].median():.1f} (IQR {ok['y'].quantile(.25):.1f} to {ok['y'].quantile(.75):.1f})")
print(ok.groupby("platform_class")["y"].agg(["count", "median", "min", "max"]).round(1).to_string())
