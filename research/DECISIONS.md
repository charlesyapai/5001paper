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
