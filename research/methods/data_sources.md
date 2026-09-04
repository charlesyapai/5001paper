# Data sources

Status: `confirmed` means the series was seen and is extractable; `to confirm` means it is
expected to exist and has not yet been checked.

| Layer | Source | Gives | Access | Cadence | Status |
|---|---|---|---|---|---|
| 01 | `data/primary/trial_records.csv` | 14,061 registry records, start year, phase, sponsor, status, results posted | bundle | static | confirmed |
| 01 | FDA CBER approved products page and product pages (S22) | cohort membership; approval dates on product pages | web | updated on approval | membership confirmed; dates to pull |
| 01 | EMA EPARs and the CAT list of authorised ATMPs | EU approval dates, conditional status, withdrawals | web | updated on approval | to confirm |
| 01 | S06 | phase transition probabilities for durable CGT | article | static | to read |
| 02 | NICE guidance pages | decision date, recommendation, managed access, committee reasons | web, English | per appraisal | to confirm |
| 02 | G-BA resolutions, IQWiG dossier assessments | added-benefit rating, date, reasons | web, German | per product | to confirm |
| 02 | HAS transparency committee opinions; CEPS published prices | ASMR and SMR ratings, date, reasons; price | web, French | per product | to confirm |
| 02 | AIFA determinations | reimbursement class and date | web, Italian | per product | to confirm |
| 02 | CDA-AMC reimbursement reviews; pCPA negotiation status | recommendation, date, reasons | web, English | per product | to confirm |
| 02 | PBAC public summary documents; MSAC outcomes | recommendation, date, reasons | web, English | per meeting | to confirm |
| 02 | EFPIA W.A.I.T. indicator (S23) | time to availability by country | report | annual | to locate |
| 03 | Company 10-K, 10-Q, annual reports, earnings releases | quarterly product revenue; disclosed patient counts | SEC EDGAR and company sites | quarterly | to confirm per company |
| 03 | EBMT activity survey papers (S11, S12) | CAR-T patients by country and year | articles | annual | to confirm country tables |
| 03 | CIBMTR summary slides (S24) | US CAR-T infusions by year | web | annual | to locate |
| 03 | JSTCT and ABMTRR reports | Japan and Australia CAR-T counts | web | annual | to locate |
| 03 | FDA and EMA safety communications, company announcements | restriction, withdrawal and discontinuation events | web | ad hoc | to confirm |
| 04 | Alliance for Regenerative Medicine sector reports (S26) | financing totals by year | report | annual | to locate |
| 04 | Deal announcements, trade press | acquisitions and licences | web | ad hoc | to confirm |
| 06 | Medicare Physician and Other Practitioners PUF; Part B national summary (S25) | annual volumes by HCPCS and PLA code | CMS data portal | annual | to confirm |
| 06 | CMS NCDs; MolDX LCDs | coverage dates and criteria | web | ad hoc | to confirm |

Eligible populations: label-defined indication, epidemiology from published incidence and
prevalence, and company-stated addressable populations, each recorded with its source and
combined into a range. Never a single number.
