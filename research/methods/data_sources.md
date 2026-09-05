# Data sources

Status: `confirmed` means the series was seen and is extractable; `to confirm` means it is
expected to exist and has not yet been checked.

| Layer | Source | Gives | Access | Cadence | Status |
|---|---|---|---|---|---|
| 01 | `data/primary/trial_records.csv` | 14,061 registry records, start year, phase, sponsor, status, results posted | bundle | static | confirmed |
| 01 | FDA CBER approved products page and product pages (S22) | cohort membership; approval dates on product pages | web | updated on approval | confirmed (F019) |
| 01 | EMA EPARs and the CAT list of authorised ATMPs | EU approval dates, conditional status, withdrawals | web | updated on approval | confirmed (F019, F020) |
| 01 | ClinicalTrials.gov API v2 (S40) | first registered interventional trial per product construct | API | live | confirmed (F032) |
| 01 | S06, S39 | phase transition probabilities for durable CGT | article and supplementary PDF | static | read (F027); no phase durations |
| 02 | NICE guidance pages | decision date, recommendation, managed access, committee reasons; eligible per year in resource impact reports | web, English (HTML and PDFs via curl with a browser user agent; replaced guidance via Wayback) | per appraisal | confirmed: 63 decision rows (F043) |
| 02 | G-BA resolutions, IQWiG dossier assessments | added-benefit rating, date, reasons; Anzahl der Patienten | web, German | per product | confirmed: 89 decision rows incl. re-assessments and AbD resolutions (F043) |
| 02 | HAS transparency committee opinions; CEPS published prices | ASMR and SMR ratings, date, reasons; price; population cible | web, French | per product | confirmed via the BDPM bulk extracts (CIS_HAS_SMR, CIS_HAS_ASMR), ANSM early-access tables and Legifrance; has-sante.fr itself 403 (F043) |
| 02 | AIFA determinations | reimbursement class and date | web, Italian (Gazzetta Ufficiale per-article fetch; TrovaNormeFarmaco API from 2025; AIFA innovativi ODS) | per product | confirmed: 57 rows; no eligible counts (F043) |
| 02 | CDA-AMC reimbursement reviews; pCPA negotiation status | recommendation, date, reasons | web, English (cda-amc.ca 403; NCBI Bookshelf and CJHT republications; pCPA export) | per product | confirmed: 71 rows (F043) |
| 02 | PBAC public summary documents; MSAC outcomes | recommendation, date, reasons | web, English | per meeting | confirmed: 92 rows, 47 verified, via pbs.gov.au and Wayback; msac.gov.au and tga.gov.au unreachable (F043) |
| 02 | EFPIA W.A.I.T. indicator (S23) | time to availability by country | report | annual | to locate |
| 03 | Company 10-K, 10-Q, annual reports, earnings releases (S29 to S33, S43) | quarterly product revenue; disclosed patient counts | SEC EDGAR and company sites | quarterly | confirmed for 22 products (F023, F035); Imlygic, Kebilidi and Beqvez not broken out |
| 03 | CMS Part B ASP pricing files (S35) | US net price (payment limit / 1.06) per HCPCS code per quarter | cms.gov zip files | quarterly | confirmed for 12 products; absent for 18 gene therapies (F030) |
| 03 | ICER reports and HTA gatekeeper documents (S41, S42) | eligible population per product, indication and country | web | per product | confirmed (F034); Japan, Italy and Spain sparse |
| 03 | EBMT activity survey papers (S11, S12, S44, S49) | CAR-T patients by country and year | articles | annual | confirmed: Europe totals 2018 to 2024; country counts for 2024 and rates per 10 million 2018 to 2024 in the 2024-data supplements (F041) |
| 03 | CIBMTR summary slides (S24) | US CAR-T infusions by year | web | annual | confirmed 2016 to 2024 (F036) |
| 03 | JSTCT and ABMTRR reports (S44) | Japan and Australia CAR-T counts | web | annual | confirmed: Japan 2019 to 2024, Australia and New Zealand 2024 (F036) |
| 03 | FDA and EMA safety communications, company announcements | restriction, withdrawal and discontinuation events | web | ad hoc | confirmed (F042; label events F039) |
| 04 | Alliance for Regenerative Medicine sector reports (S26) | financing totals by year | report | annual | to locate |
| 04 | Deal announcements, trade press | acquisitions and licences | web | ad hoc | confirmed from SEC filings and EMA pages: 102 events (F042) |
| 06 | Part B National Summary Data File (S25, S36); Physician and Other Practitioners PUF | annual volumes by HCPCS and PLA code | cms.gov zip files; data.cms.gov API (403 from this environment) | annual from 2000, 2023 not published | confirmed (F031) |
| 06 | CMS NCDs; MolDX LCDs | coverage dates and criteria | web | ad hoc | to confirm |

Eligible populations: label-defined indication, epidemiology from published incidence and
prevalence, and company-stated addressable populations, each recorded with its source and
combined into a range. Never a single number.
