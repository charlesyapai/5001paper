# Translation timeline plan

**Fourth framing document. Supersedes `thesis_architecture.md` as the flagship direction.
The earlier three documents remain valid for the clinical-stage layer and for the companion
methods paper. Assembled 4 September 2026 after the referee pitch, a recomputation of the
784-trial halted set, and a same-day literature scan.**

---

## 0. The decision in one paragraph

Keep the original question. Retire the registry stated-reason field as the flagship
instrument. Measure the trial-to-real-life transition directly, at the stage where it happens
and where prices, payers and patients are observable: after approval. The paper becomes an
end-to-end translation timeline for precision medicine. It measures how long each stage takes
and how many programs and patients each stage loses, identifies which levers move those
numbers, and projects when the frontier editing platforms reach patients at scale under
current and reformed architectures. The existing dataset supplies the pre-approval half. New
public-source data supplies the post-approval half. The halt-reason work is spun off as a
short companion methods paper.

## 1. Why the direction changed

The referee pitch established that the thesis was consensus and that the instrument could not
see payment. A recomputation of the halted set on 4 September 2026 added six findings that
together make the old framing unrecoverable as a research contribution.

1. **The interaction is real but probably generic.** It survives restriction to interventional
   trials (industry therapeutics 65.7% business-cited against 22.0%, 20.9% and 23.4% in the
   other cells). But a 2026 JNCI analysis of 1,740 phase 1 solid-tumour trials found sponsor or
   strategic decisions were the leading termination reason at 51.1% across all sponsors, with
   industry funding 71.2% of terminated trials. If academic terminations cite strategic reasons
   at about a quarter, the implied industry-only rate is about 60%. The headline cell here is
   three-quarters Phase 1 or Phase 1/2 and mostly oncology. The phase-matched comparator will
   very likely come back generic.
2. **The headline cell is two stories with opposite time trends.** CAR-T is 97 of the 144
   industry-therapeutic halts. Its business-cited share by trial start year is 35%, 55% and
   86% for starts up to 2018, 2019 to 2021, and 2022 onward. Gene therapy and editing run 75%,
   59% and 50% on small numbers. Industry diagnostics rose 16%, 24%, 41% over the same
   windows. Forty-four of the cell's 95 business halts are CAR-T trials started in 2022 or
   later: a capital-cycle and crowding story in a field where reimbursement exists. The thesis
   story about durable one-time small-population therapies fits AAV, not the data that carries
   the number.
3. **The proposed cheap comparator cannot work.** Modality is assigned per subfamily and the
   imaging-AI subfamily is diagnostic. It already forms 39 of the 81 industry-diagnostic
   halts. It can never populate the therapeutic row.
4. **The category is boilerplate.** Nine of the 95 industry-therapeutic business halts name a
   financial cause. The rest read "Sponsor decision" or "Business reasons"; one is MYDICAR,
   a documented efficacy failure. The sponsor-exit instrument's negative correlation is what
   asset-level failures dressed as strategy would produce.
5. **The payment evidence is six cases, four of them haemophilia**, where competition from
   prophylaxis and durability hesitancy is a well-documented rival explanation.
6. **The forward claim ignores architecture changes since 2024**: the CMS Cell and Gene
   Therapy Access Model, EU joint clinical assessments for advanced therapies from January
   2025, FDA platform designation and bespoke-therapy proposals, and the shift of in vivo
   editing toward large populations.

None of this makes the question wrong. It makes the instrument wrong for the question.

## 2. The question, restated so data can answer it

**Q1.** How long does each stage of translation take, by technology class: first-in-human to
approval, approval to reimbursement, reimbursement to patients treated at scale?
**Q2.** Where are programs and patients lost: attrition per stage, withdrawal and restriction
after approval, and the gap between eligible and treated populations?
**Q3.** What shortens the stages: payment arrangement, delivery setting, manufacturing model,
evidence type at approval, price relative to budget impact, treatment-centre capacity,
competition?
**Q4.** When do the frontier platforms reach patients under current and reformed
architectures, and how long must capital be patient in each case?

Five hypotheses, to be tested rather than assumed:

- **H1. Post-approval is now the longer stage.** For advanced therapies approved since 2017,
  median time from approval to half the eligible population treated exceeds median time from
  first-in-human to approval.
- **H2. Architecture beats technology.** Cross-country variation in uptake of the same
  product exceeds cross-product variation within one country.
- **H3. Two bottlenecks.** Diagnostics stall before coverage and diffuse fast once covered.
  Therapies stall after coverage because delivery capacity and payment structure bind.
- **H4. The effect gap is small; the access gap is large.** Real-world effectiveness of CAR-T
  tracks trial efficacy in registry studies; the transition fails on access, not on the
  science surviving contact with practice.
- **H5. The frontier inherits the timeline, and capital is rotating toward the shorter one.**
  Base editing and in vivo LNP programs now in Phase 1 or 2 reach half their eligible
  populations well into the 2030s under measured stage durations. Deal flow since 2024
  concentrates in in vivo platforms whose modelled translation timeline is shorter.

## 3. Crosswalk: what the old thesis covered, and where it now lives

| Old concern | Old instrument | Where it lives now |
|---|---|---|
| Blockers before approval | Sponsor-stated halt reasons | Kept as the clinical-stage attrition layer and as a supplementary panel. The stated-reason analysis itself becomes the companion methods paper. |
| Blockers at market access | Not observed | Health technology assessment documents: decision, timing, and stated reasons classified with the existing pipeline. Gatekeepers state reasons about evidence, durability and price; sponsors do not. |
| Blockers during uptake | Not observed | Determinants of diffusion speed: centre capacity, referral, manufacturing slots, delivery setting, payment arrangement. Measured as covariates of time-to-milestone. |
| Investment and capital markets | Six trade-press cases; sponsor-exit proxy | An explicit layer: sponsor commitment intervals, program retreat and exit events, sector financing by year, deal flow by delivery model, and the time-to-revenue implied by each stage duration. |
| Health-system economics | Asserted from the six cases | Reimbursement lag by country, managed-entry and outcomes-based arrangements, price against budget impact, and the same product diffusing through different systems. |
| Demand and competition | Section 4.4 narrative | Tested against the full approved-product denominator, with haemophilia as the case where competition dominates. |
| Diagnostics need evidence, not price | Assay-as-intervention count | Kept as the predictor of coverage timing, joined to Medicare uptake after coverage. |

## 4. Study design: five layers

### 4.1 Clinical stage. Have it.
- **Unit.** Platform subfamily; trial.
- **Measures.** First-in-human year, first Phase 3 year, first approval year; attrition and
  halt shares; pipeline counts for the projection layer.
- **Sources.** `data/primary/trial_records.csv`, `data/derived/technology_maturity_matrix.csv`,
  FDA CBER and EMA approval dates.
- **Method.** Descriptive stage durations by class; the published clinical success-rate
  literature for durable cell and gene therapies as the external benchmark.

### 4.2 Access stage. New.
- **Unit.** Product by country.
- **Measures.** Regulatory approval date; first health technology assessment decision date and
  outcome; managed-entry arrangement type; price at decision where public; stated reasons for
  restriction or rejection, classified.
- **Sources.** NICE, G-BA and IQWiG, HAS, AIFA, CDA-AMC, PBAC and MSAC appraisal documents;
  EFPIA availability indicator; existing European reimbursement-lag studies for validation.
- **Method.** Time from approval to decision; decision outcome by class and country; reason
  classification with `02_classify_halts.py` adapted to a new schema.

### 4.3 Uptake stage. New.
- **Unit.** Product by quarter; product by country by year.
- **Measures.** Patients treated per quarter; eligible population; penetration; time to a
  quarter and to half of eligible; plateau; withdrawal, restriction or discontinuation events.
- **Sources.** Quarterly product revenue from 10-K, 10-Q, annual reports and earnings
  releases, divided by list price, calibrated against disclosed patient counts. CIBMTR and
  EBMT activity surveys for CAR-T infusions by country; JSTCT for Japan; ABMTRR for
  Australia. Medicare Part B volumes by proprietary test code for diagnostics. Company and
  registry disclosures of treatment centres activated.
- **Method.** Logistic or Bass diffusion fits per product; Kaplan-Meier time-to-milestone by
  class with withdrawal as a competing risk; Cox models with class and covariates.

### 4.4 Investment and sponsor commitment. New, partly from existing data.
- **Unit.** Sponsor by platform; product; sector by year.
- **Measures.** First-to-last trial interval per sponsor per platform; program retreat and
  exit events after approval; sector financing totals by year; acquisitions and licensing
  deals for approved and late-stage products, coded by manufacturing model; implied years of
  capital from first-in-human to first revenue and to half penetration, by class.
- **Sources.** `trial_records.csv` for commitment intervals; company disclosures and trade
  press for retreat events, extending `commercial_retreat_cases.csv` to a systematic list;
  Alliance for Regenerative Medicine sector reports for financing totals; deal announcements.
- **Method.** Sponsor survival analysis; event counts by year and model; a transparent
  time-to-revenue calculation per class under each architecture scenario. No full valuation
  model. The point is the horizon, not the NPV.

### 4.5 Projection. New.
- **Unit.** Frontier platform.
- **Measures.** Expected year of first approval, first reimbursement, and half penetration,
  with ranges, under scenarios.
- **Method.** Monte Carlo over stage durations sampled from the empirical distributions of the
  nearest mature class, applied to the frontier pipeline counts. Scenarios: current
  architecture; access stage compressed to the best observed country; uptake stage compressed
  to outpatient or in vivo delivery benchmarks; both. Backcast check: the model run from 2003
  must reproduce the observed AAV and CAR-T histories within its own bands.
- **Comparison.** The field's own 2021 projections of US approvals and patients treated, and
  the 2024 France projections, against realized counts through 2025. A forecast that modelled
  demand and skipped the access stage overshoots; measuring by how much is a result.

## 5. Identification

In order of credibility.

1. **Same product, different systems.** CAR-T per-eligible uptake across the United States,
   Germany, France, the United Kingdom, Italy, Spain and Japan, against each country's
   reimbursement lag, centre density and payment model. Product and year fixed effects.
2. **Event studies around policy changes.** Interrupted time series, with synthetic controls
   where a comparator product exists. Candidate events are listed in 7.3.
3. **Cross-product determinants.** Diffusion speed regressed on payment arrangement, delivery
   setting, manufacturing model, evidence type at approval, price relative to budget impact,
   and competition. Reported as association.

## 6. Prior work check, 4 September 2026

Pieces of every layer exist. The integration does not, and the comparison of forecast to
realized uptake does not.

| Exists | Where | What this paper adds |
|---|---|---|
| Clinical success rates for durable cell and gene therapies | Nature Reviews Drug Discovery, 2025 | The post-approval stages, joined to the clinical stage on one timeline |
| Time to national reimbursement for advanced therapies in Europe, 9 to 17 months median | Value in Health, 2023; follow-up availability studies 2025 | Updated through 2026, linked to uptake rather than stopping at the decision |
| CAR-T utilisation across European countries against macro factors | EBMT activity-survey reports, 2024 and 2025 | Per-eligible normalisation, reimbursement lag and policy events as explanatory variables, and the contrast with gene therapy |
| Demand projections of patients treated | Drug Discovery Today, 2021 for the US; a 2024 France study | The realized record against those projections, and stage-based rather than demand-based projection |
| Product-level uptake notes: fewer than 20 Hemgenix patients by August 2024, tens of Lyfgenia and Zynteglo patients, Luxturna treating most of its eligible population | Consultancy reviews, 2024 and 2025 | Systematic, open, normalised, and modelled |
| Access barrier landscapes for paediatric CD19 CAR-T in Europe | medRxiv, 2025 | Quantified uptake consequences of the barriers |

Positioning sentence for the introduction: the pre-approval half of this timeline has been
measured; the post-approval half has been described product by product and forecast in
aggregate, but never measured as a stage with a duration, a loss rate and a set of levers.

## 7. Seed tables

**Every row below was seeded from memory on 4 September 2026. Verify every date, count and
classification against the primary source before it is used in any table or figure. The
month 1 task is to replace these with sourced rows.**

### 7.1 Product cohort: gene therapies and gene-modified cell therapies approved by FDA

| Product | Sponsor | Indication | Platform | FDA | EU | Public sales | Post-approval event |
|---|---|---|---|---|---|---|---|
| Imlygic | Amgen | melanoma | oncolytic HSV | 2015 | 2015 | yes, small | |
| Kymriah | Novartis | B-ALL, LBCL, FL | autologous CAR-T | 2017 | 2018 | yes | |
| Yescarta | Gilead / Kite | LBCL, FL | autologous CAR-T | 2017 | 2018 | yes | |
| Luxturna | Spark / Roche; Novartis ex-US | RPE65 retinal dystrophy | AAV subretinal | 2017 | 2018 | yes | near-complete uptake of small pool |
| Zolgensma | Novartis | SMA | AAV systemic | 2019 | 2020 | yes | |
| Tecartus | Gilead / Kite | MCL, B-ALL | autologous CAR-T | 2020 | 2020 | yes | |
| Breyanzi | BMS | LBCL, CLL, FL, MCL | autologous CAR-T | 2021 | 2022 | yes | |
| Abecma | BMS / 2seventy | multiple myeloma | autologous CAR-T | 2021 | 2021 | yes | 2seventy acquired by BMS 2025 |
| Carvykti | J&J / Legend | multiple myeloma | autologous CAR-T | 2022 | 2022 | yes | |
| Zynteglo | bluebird | transfusion-dependent thalassaemia | lentiviral ex vivo | 2022 | 2019, withdrawn 2021 | to 2025 | EU withdrawal; US outcomes-based agreement |
| Skysona | bluebird | cerebral ALD | lentiviral ex vivo | 2022 | 2021, withdrawn 2021 | to 2025 | haematologic malignancy warnings |
| Hemgenix | CSL Behring / uniQure | haemophilia B | AAV systemic | 2022 | 2023 | yes, annual | slow uptake |
| Adstiladrin | Ferring | NMIBC | adenoviral intravesical | 2022 | no | private | |
| Vyjuvek | Krystal | dystrophic EB | HSV topical | 2023 | 2025 | yes | |
| Elevidys | Sarepta | DMD | AAV systemic | 2023 | CHMP negative 2025 | yes | 2025 safety restriction |
| Roctavian | BioMarin | haemophilia A | AAV systemic | 2023 | 2022 | yes | minimal uptake; divestment explored 2025 |
| Casgevy | Vertex / CRISPR Tx | SCD, TDT | CRISPR ex vivo | 2023 | 2024 | yes | |
| Lyfgenia | bluebird | SCD | lentiviral ex vivo | 2023 | no | to 2025 | |
| Lenmeldy / Libmeldy | Orchard / Kyowa Kirin | MLD | lentiviral ex vivo | 2024 | 2020 | limited | |
| Beqvez / Durveqtix | Pfizer | haemophilia B | AAV systemic | 2024 | 2024 | yes | discontinued 2025 |
| Tecelra | Adaptimmune | synovial sarcoma | TCR-T | 2024 | no | yes | |
| Aucatzyl | Autolus | B-ALL | autologous CAR-T | 2024 | 2025 | yes | |
| Kebilidi / Upstaza | PTC | AADC deficiency | AAV intraputaminal | 2024 | 2022 | yes | |
| Zevaskyn | Abeona | recessive dystrophic EB | gene-modified keratinocyte sheets | 2025 | no | yes | |
| Papzimeos | Precigen | recurrent respiratory papillomatosis | adenoviral immunotherapy | 2025 | no | yes | |
| Encelto | Neurotech | macular telangiectasia | encapsulated cell | 2025 | no | private | |

Non-genetic cell therapies to include as a flagged comparator class: Amtagvi (Iovance, TIL,
2024), Ryoncil (Mesoblast, MSC, 2024), Omisirge (Gamida, 2023, company wound down 2024),
Lantidra (CellTrans, 2023, private). EU-only history for the withdrawal rate: Glybera (2012,
withdrawn 2017), Strimvelis (2016), Zalmoxis (2016, withdrawn 2019), Alofisel (2018, withdrawn
2024), Ebvallo (2022). Check FDA approvals from mid-2025 to date; candidates include an
intrathecal onasemnogene product and further CAR-T approvals.

### 7.2 Countries, gatekeepers and registries

| Country | Reimbursement gatekeeper | CAR-T count source | Role |
|---|---|---|---|
| United States | Medicare NCDs, Medicaid, commercial payers | CIBMTR | Uptake and diagnostics core |
| England | NICE and NHS England | EBMT | Access core |
| Germany | G-BA with IQWiG, AMNOG pricing | EBMT | Access core |
| France | HAS and CEPS | EBMT | Access core |
| Italy | AIFA | EBMT | Access core |
| Spain | AEMPS and CIPM | EBMT | Cross-country CAR-T |
| Canada | CDA-AMC and pCPA | CBMTG or provincial | Access core, English documents |
| Australia | PBAC and MSAC | ABMTRR | Access core, English documents |
| Japan | MHLW and Chuikyo | JSTCT | Optional seventh system |

### 7.3 Policy and market events for event studies

| Date | Event | Layer |
|---|---|---|
| 2018-03 | Medicare national coverage for next-generation sequencing in advanced cancer; germline expansion 2020-01 | Diagnostics coverage |
| 2019-08 | Medicare national coverage determination for CAR-T | Uptake |
| 2020-10 | Dedicated inpatient payment group for CAR-T in US hospitals | Uptake |
| 2021-03 | NHS England agreement for Zolgensma | Access |
| 2021-04 | Zynteglo withdrawn from Germany after price talks; bluebird exits Europe 2021-08 | Access, investment |
| 2022-07 | US rule permitting multiple best prices for value-based arrangements | Access |
| 2022-08 | Zynteglo US approval with outcomes-based agreement | Access |
| 2023-06 | Elevidys accelerated approval; label expansion 2024-06; safety restriction 2025 | Uptake |
| 2024-08 | NICE recommendation for Casgevy in thalassaemia; sickle cell 2025-01 | Access |
| 2025-01 | CMS Cell and Gene Therapy Access Model launches; most states join during 2025 | Access, uptake |
| 2025-01 | EU joint clinical assessments begin for advanced therapies and oncology | Access |
| 2025-02 | Pfizer discontinues Beqvez and exits gene therapy | Investment |
| 2025-06 | FDA removes REMS requirements for autologous CAR-T | Uptake |
| 2025 | bluebird acquired by private equity; 2seventy acquired by BMS | Investment |

### 7.4 Diagnostics: codes and coverage events

| Test or family | Codes to pull | Coverage event |
|---|---|---|
| Comprehensive genomic profiling, tissue | 0037U | NCD 90.2, 2018-03 |
| Liquid biopsy, comprehensive | 0239U, 0242U | MolDX coverage 2018 to 2020; NCD 90.2 |
| Molecular residual disease | 0340U | MolDX coverage 2021 onward |
| Pharmacogenomics, single gene | 81225 to 81231 | MolDX pharmacogenomics coverage 2020 |
| Pharmacogenomics, panel | 81418 | as above |
| Exome and genome | 81415, 81416, 81425, 81426 | state Medicaid and MolDX decisions |
| Breast cancer recurrence score | 81519 | long-covered comparator |

Source: Medicare Physician and Other Practitioners public use files and the Part B national
summary, annual volumes by code. Verify each code assignment.

### 7.5 Investment events to code by manufacturing model

Acquisitions of AveXis (2018), Spark (2019), Audentes (2019), Orchard (2023); the 2seventy,
bluebird and Verve transactions of 2025; the 2025 in vivo CAR-T acquisitions by AstraZeneca,
AbbVie and Gilead; Pfizer's 2025 exit; Roche's restructuring of Spark; sector financing
totals by year from Alliance for Regenerative Medicine reports. The hypothesis to test is that
capital rotated from ex vivo autologous toward in vivo platforms as the launch record of
2022 to 2025 arrived.

## 8. Figure plan

1. **The translation timeline.** Stacked stage durations per platform, first-in-human to
   approval to reimbursement to half uptake, with attrition at each boundary. The money figure.
2. **Every approved product's uptake curve**, normalised to eligible population, coloured by
   class, with time-to-quarter and time-to-half distributions.
3. **Same product, different systems.** CAR-T per-eligible uptake by country against
   reimbursement lag and centre density.
4. **What gatekeepers say.** Classified assessment reasons by class and country; time from
   approval to decision.
5. **Diagnostics.** Coverage to uptake in Medicare; assay-as-intervention evidence against
   coverage timing.
6. **Forecast against record.** The 2021 projections of patients treated against realized
   counts through 2025.
7. **Projections for the frontier** under scenarios, with ranges, and the implied years of
   capital per class.

Supplementary: real-world versus trial effectiveness for CAR-T; event studies; sensitivity to
price and eligible-population assumptions; data audit tables.

## 9. Reuse map

| Existing asset | New use |
|---|---|
| `data/primary/trial_records.csv` | Clinical-stage durations, pipeline counts, sponsor commitment intervals |
| `data/derived/technology_maturity_matrix.csv`, `technology_timeline_map.md` | Stage ladder and first-year columns for layer 4.1 |
| `data/derived/commercial_retreat_cases.csv` | Seed of the systematic retreat-event table |
| `data/derived/access_equity_by_subfamily.csv`, `editing_trial_geography.csv` | Trial geography against post-approval access geography |
| `data/derived/platform_lookup.csv` | Assay-as-intervention counts for the diagnostics layer |
| `code/01_retrieve.py` | Refresh pipeline counts; add halt dates and intervention names |
| `code/02_classify_halts.py` | Re-schema for health technology assessment reasons |
| `code/03_analyse.py` | Pattern for the new verification harness |
| Halt-reason analysis and referee record | Companion methods paper, per `OPEN_ITEMS.md` items 1 to 3 |

## 10. Timeline, gates and the first week

| Month | Work | Gate |
|---|---|---|
| 1 | Sourced product cohort with approvals, prices, eligible populations; pilot uptake curves on five products; confirm no integrated prior analysis | Sales-derived patient counts calibrate within about thirty percent of disclosed counts, else registry counts and reimbursement timing become the quantitative core |
| 2 | All uptake curves; assessment decisions and dates for six systems; reason classification; retreat-event table | H1 computable |
| 3 | CAR-T country counts; Medicare volumes; diffusion fits; time-to-milestone models; sponsor survival | H2 stable across per-capita and per-eligible denominators |
| 4 | Projection model and backcast; event studies; forecast-against-record; main figures | Backcast reproduces AAV and CAR-T within bands |
| 5 | Draft; adversarial claim review; preprint | Every number regenerated from a table in the cell that writes it |
| 6 | Submit; companion methods paper finished in parallel | |

First week:

- Pull the FDA CBER approved-products list and the EMA advanced-therapy list; replace 7.1.
- Pilot the revenue-to-patients method on Zolgensma, Yescarta, Hemgenix, Casgevy and Luxturna,
  where disclosed patient counts exist for calibration.
- Download the last three EBMT activity-survey reports and the latest CIBMTR summary; confirm
  CAR-T counts by country are extractable.
- Pull one year of Medicare Part B volumes for the codes in 7.4; confirm the series exists.
- Read the 2025 Nature Reviews Drug Discovery success-rate analysis and the 2021 Drug
  Discovery Today projection paper; extract their numbers for figures 1 and 6.
- Fix the two v7 defects and start the companion paper's comparator and audit.

## 11. Risks

- **Prior integrated analysis.** Mitigated by the scan in section 6; re-check at month 1.
- **Soft denominators.** Eligible populations and net prices are estimates. Every penetration
  figure carries a range; calibrate on products with disclosed counts.
- **Recent approvals are censored.** Survival methods handle it; weight projections toward
  classes with long follow-up.
- **Weak causal claims in the determinants layer.** Lead with the same-product cross-country
  design and event studies; keep the regression as supporting evidence.
- **Registry access.** EBMT and CIBMTR publish aggregate counts; patient-level data is not
  needed and should not be requested.
- **Scope creep into AI diagnostics.** Out of scope for the flagship except as a comparator
  row in the clinical-stage layer.

## 12. Venue, title and north star

Realistic top targets: Nature Medicine or Nature Biotechnology analysis; Nature Reviews Drug
Discovery analysis and Health Affairs as fallbacks. The entry ticket is the open dataset plus
one decision-relevant number. H1, if it holds, is that number.

Working title: **How long precision medicine takes to reach patients: a stage-by-stage
timeline and projection for gene, cell and molecular diagnostic technologies.**

Abstract north star, to be rewritten from results: Across every gene, cell and molecular
diagnostic technology approved since 2017, we measure how long each stage of translation took
and how many patients it reached, using public sales, registry and coverage data normalised to
eligible populations. The post-approval stage now takes longer and loses more programs than
clinical development. The same product diffuses several times faster in some systems than in
others, and the difference is explained by reimbursement lag, delivery setting and payment
arrangement rather than by the technology. Applying the measured stage durations to the
frontier pipeline, we project when base editing and in vivo platforms reach patients under
current and reformed architectures, and how many years of capital each requires.
