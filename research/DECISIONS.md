# Decision record

## D001 · 2026-09-04 · The flagship paper is the translation timeline
**Decision.** The flagship measures the trial-to-real-life transition after approval, stage by
stage, across gene, cell and molecular diagnostic technologies, and projects the frontier.
**Rationale.** The registry stated-reason field observes neither payment nor late-phase efficacy
failure. The headline interaction is probably a generic property of industry-sponsored early-phase
trials (F007, F008). The old thesis is the field's consensus. The question survives; the
instrument does not.
**Consequences.** Four new layers (access, uptake, investment, projection); seed tables under
`data/cohort/`; plan in `manuscript/translation_timeline_plan.md`.

## D002 · 2026-09-04 · The halt-reason analysis becomes a companion methods paper
**Decision.** The v7 manuscript is reframed around what the stated-reason field can and cannot
show, and finished separately.
**Rationale.** It is nearly done, its negative methodological results are a real contribution,
and it would clutter the flagship.
**Consequences.** `OPEN_ITEMS.md` items 1 to 3 apply to it; topic folder `07_companion_methods_paper`.

## D003 · 2026-09-04 · The imaging-AI subset is rejected as the comparator
**Decision.** The companion paper's comparator is a fresh pull of industry-sponsored non-precision
therapeutics matched on phase and start year.
**Rationale.** Modality is fixed per subfamily; the AI/ML subfamily is diagnostic and already forms
39 of the 81 industry-diagnostic halts (F005). It can never populate the therapeutic row.

## D004 · 2026-09-04 · A disclosure audit joins the classification kappa
**Decision.** The 95 industry-therapeutic business halts are audited against press releases and
regulatory filings for an externally disclosed scientific or competitive cause.
**Rationale.** Nine of the 95 name a financial cause (F004). A kappa validates the label; the audit
validates the statement.

## D005 · 2026-09-04 · Investment is an explicit layer
**Decision.** Sponsor commitment, retreat and exit events, sector financing, deal flow by
manufacturing model, and implied years of capital are measured as a layer of the flagship.
**Rationale.** The project's economics and business framing requires it, and the old thesis's
capital-market claim was otherwise unmeasured.

## D006 · 2026-09-04 · Seed tables must be verified before use
**Decision.** The status vocabulary in `research/README.md` is adopted. Rows marked
`seeded-from-memory` or `provisional-from-snippet` never enter a figure or an abstract.
**Rationale.** The seed cohort written on 4 September 2026 missed seven FDA-listed products (F016).

## D007 · 2026-09-04 · Where new material lives
**Decision.** Research notes under `research/`; cohort and seed tables under `data/cohort/`;
later extracted data under `data/access/`, `data/uptake/`, `data/investment/`; the registry
study's `data/primary/` and `data/derived/` are left untouched.

## D008 · 2026-09-04 · Version control
**Decision.** The bundle is a git repository from 4 September 2026. Commit messages carry the
finding or decision id they implement. No remote yet.

## D009 · 2026-09-05 · First-in-human is the earliest registered interventional trial of the construct
**Decision.** The clinical stage starts at the start date of the earliest registered interventional trial
of the construct that became the product, including academic trials under a different name (the Penn
CART-19 trial for Kymriah, the NCI anti-CD19 CAR trial for Yescarta, the CHOP trial for Luxturna), and
ends at the first approval by FDA or EMA, whichever came first. A predecessor construct is not counted
(AMT-060 for Hemgenix).
**Rationale.** Registry start dates are sourced and reproducible (F032); unregistered pre-2000 trials are
flagged per product rather than guessed.
**Consequences.** `data/cohort/first_in_human.csv` with the NCT id per product; sixteen products whose
earliest registered trial is phase 2 or 3 carry a flag that an earlier unregistered phase 1 is possible.

## D010 · 2026-09-05 · Eligible denominators are ranges built from documented rows
**Decision.** Every eligible population is a range over verified and derived source rows, per product,
geography and family (annual incident flow or prevalent pool), with indication-specific estimates summed
across distinct diseases and ranged within a disease. Rows that are not label populations (budget-impact
spreading, superset populations, Medicare-only samples) are excluded through
`data/uptake/eligible_overrides.csv`, which records the reason for each judgment.
**Rationale.** Agent-collected rows mix gatekeeper counts, company statements and epidemiology; the range
and the override file keep every judgment visible (conventions 4 and 7).
**Consequences.** `data/uptake/eligible_population.csv` and `eligible_population_rows.csv`; provisional
rows never enter the range used for a figure.

## D011 · 2026-09-05 · The class net-to-list factor stays until product-level net prices exist
**Decision.** Patient counts keep the calibrated class factor of 0.76 on US launch list price (F024) for
all products. The CMS ASP series (F030) shows US net equals list for CAR-T, so for CAR-T the factor
represents post-launch list-price increases and ex-US prices rather than rebates.
**Rationale.** Consistency with the calibration; the ASP series covers only 12 products and none of the
gene therapies.
**Consequences.** A product-level variant (US revenue at current WAC or ASP, ex-US at the calibrated
factor) is a month-2 refinement, not a change to the current tables.

## D012 · 2026-09-05 · Eligible pools are dated to the label in force
**Decision.** For products whose label changed after launch, the eligible pool is rebuilt quarter by quarter
from verified label events (`data/uptake/label_events.csv`): only indications on the label on a given day count;
an extension that widens an existing population replaces its narrower key (second-line myeloma replaces
fifth-line); an added disease adds its own range; a restriction removes its key; inflow is day-weighted in the
quarter of a change. Where the product has no eligible row for an indication in force, the range of another
product with the same indication and geography is borrowed and flagged; where none exists the gap is flagged
and the pool is understated rather than guessed. Products without label events keep the static pool.
**Rationale.** The static ranges mixed lines of therapy (Carvykti's US range ran from the fifth-line flow to the
second-line flow, F037), so penetration ranges were wide for the wrong reason: a definitional mixture, not
source disagreement. Dating the pool to the label separates the two.
**Consequences.** `build_milestones_2026-09-05.py` reads the events file and writes `data/uptake/pool_quarterly.csv`;
`build_eligible_ranges_2026-09-05.py` writes `eligible_population_by_indication.csv`. Only events with status
verified-from-source or derived are applied (rule 3). The launch-label reading in F037 is superseded for the
label-dated products by F039.

## D013 · 2026-09-06 · The projection is a staged Monte Carlo chained on the measured stages, backcast before use
**Decision.** Approvals, funded access and patients treated to 2036 are projected by chaining the three measured
stages: (A) industry programmes in the registry pipeline (one per sponsor per platform at its highest active phase)
survive phase transitions at the S06 rates (F027) and reach approval after a clinical stage drawn from the cohort's
measured distribution for the class (F032), scaled by the share remaining at the current phase; new programmes
enter phase 1 at the 2021 to 2025 rate; (B) each approval draws a lag to the first positive funding step from the
measured lags per system (F043) with the system's observed share of approvals ever funded; (C) patients follow class
diffusion curves fitted to the observed penetration paths against the label-dated pools (F039), CAR-T as a class
against its eligible flow anchored on the registry totals (F041), one-time therapies product by product with pools
drawn from the observed range. The model is run first as a backcast from the pipeline at the end of 2019 against the
2020 to 2025 record; where the record falls outside the band, a per-class calibration factor (realised over backcast
median, capped at 1) is applied and reported. Scenarios: baseline, compressed access, capacity-constrained. Every
output is a 10th, 50th and 90th percentile.
**Rationale.** Prior projections (S16, S17, S20) skipped the access and diffusion stages and overshot the patient
record while getting the approval count right (F033). A chained model with measured stage distributions is the
simplest structure that can be backcast, and the calibration step makes the registry's overcount of approvable
programmes explicit rather than hidden.
**Consequences.** `research/findings/project_landscape_2026-09-06.py` writes `data/projection/approvals_projection.csv`,
`access_projection.csv`, `patients_projection.csv`, `capacity_projection.csv`, `diffusion_fits.csv`,
`pipeline_programmes.csv` and `projection_parameters.csv` (every fitted or assumed value with its source). The
frontier-platform milestone table in `projection_model.md` remains a month-4 output. Assumptions to revisit: the
programme proxy, the share of CAR-T approvals opening a new disease (0.25), the Europe population ratio (1.5), the
Europe share of ex-US patients (0.75), and the rest-of-world share.

## D014 · 2026-09-07 · The projection is rebuilt on measured distributions, validated by unit, and carries its assumptions as ranges
**Decision.** `research/findings/project_landscape_2026-09-07.py` supersedes the D013 implementation. (A) The pipeline unit is
one lead programme per sponsor and class among registry constructs with a US or European trial site (F048); approved constructs
leave the pipeline at approval. Four units were backcast from the end-2019 pipeline and the one whose uncalibrated band covers the
2020 to 2025 record is used forward without calibration; the other three are reported as structural alternatives. If a future
rerun's primary backcast misses the record, the correction is estimated per class as a Gamma posterior of realised over predicted
and drawn per run, never fixed. Time to approval is drawn from the class distribution conditional on the time already elapsed since
the construct's first trial, and from the cohort's phase-3-start-to-approval distribution for phase-3 constructs; the remaining-share
ranges of D013 are dropped. (B) Each approval draws its funding time per system from the Aalen-Johansen cumulative incidence of
F047, which carries the never-funded mass. (C) Uptake follows Bass curves with per-product parameters drawn from the shrunk
per-product set (F049); CAR-T as a class follows the registry-total fits per region with bootstrap tuples; rest of world is an
explicit share. (D) Every fixed assumption is listed with a range and a source in `projection_parameters.csv`, drawn per run in the
headline probabilistic run, and varied one at a time in a tornado; structural alternatives and an ISPOR-SMDM validation table are
written with the outputs.
**Rationale.** The referee objections listed in the 7 September handover: the sponsor proxy and its fudge factor, the assumed
remaining shares, the naive funded share, the unidentified diffusion ceiling and the sampling-only bands. Choosing the pipeline unit
on the backcast is model selection on the validation data; it is stated as such and the alternatives are shown.
**Consequences.** F048, F049, F050 replace F044. `data/projection/pipeline_programmes.csv` and `diffusion_fits.csv` (D013 outputs)
are removed; `pipeline_constructs.csv`, `phase_durations.csv`, `diffusion_bass_fits.csv`, `diffusion_loo.csv`,
`sensitivity_oneway.csv`, `sensitivity_structural.csv` and `validation.csv` are added. Figures P3 (sensitivity) and P4 (funded
access as cumulative incidence) join P1 and P2.
