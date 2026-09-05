# Access layer tables

Built 5 September 2026 by `research/findings/build_access_decisions_2026-09-05.py` from the raw agent tables in `raw/`.

| File | Content | Finding |
|---|---|---|
| `raw/decisions_nice.csv` | England: NICE appraisals and HST guidance, Cancer Drugs Fund and managed access, committee reasons, list prices, eligible per year (63 rows) | F043 |
| `raw/decisions_gba.csv` | Germany: G-BA resolutions per patient group with Zusatznutzen, Anzahl der Patienten, Jahrestherapiekosten, AbD requirements (89 rows) | F043 |
| `raw/decisions_cda_amc.csv` | Canada: CADTH/CDA-AMC recommendations, conditions and price reductions, pCPA negotiation outcomes, NOC dates (71 rows) | F043 |
| `raw/decisions_aifa.csv` | Italy: AIFA determinations with classe, ex-factory price, managed-entry agreement and innovativeness (57 rows) | F043 |
| `raw/decisions_has.csv` | France: HAS avis (SMR, ASMR), ANSM early access, JO inscription, CEPS tariffs (132 rows) | F043 |
| `raw/decisions_australia.csv` | Australia: TGA registration, MSAC and PBAC advice and deferrals, funding start where published (92 rows, 37 provisional) | F043 |
| `decisions.csv` | Every row normalised: product key, parsed dates, months from regulatory approval (basis recorded) and from FDA approval, usable flag | F043 |
| `access_summary.csv` | One row per product and system: first usable decision, first positive funding step (NICE, G-BA, pCPA, JO/CEPS/ANSM, AIFA) and its lag, latest outcome, arrangement types | F043 |

Conventions: outcome vocabulary recommended, recommended-restricted, recommended-managed-access, not-recommended,
terminated-or-withdrawn, under-assessment, not-submitted, not-found; rows with status provisional-from-snippet or
not-found never enter a duration; HAS avis rows read from the official BDPM extract are graded verified in the merge and say so in notes.
