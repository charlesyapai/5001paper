# Projection model

**Purpose.** Expected year of first approval, first reimbursement and half penetration for each
frontier platform, with ranges, under named scenarios; and the years of capital each class
requires.

**Inputs.** Empirical stage-duration distributions per mature class from layers 01 to 03;
frontier pipeline counts and current phases from layer 01; success probabilities from S06.

**Donor mapping, to be argued in the paper.**

| Frontier platform | Donor class for stage durations |
|---|---|
| Base editing, ex vivo | CRISPR nuclease ex vivo, then lentiviral ex vivo |
| Base editing, in vivo LNP | AAV systemic for access and uptake; in vivo LNP for clinical |
| Prime editing | CRISPR nuclease ex vivo |
| Epigenome editing | AAV systemic |
| In vivo CAR-T | AAV systemic for access; autologous CAR-T for indication and centres |

**Procedure.**
1. For each frontier program at its current phase, sample remaining clinical-stage duration and success from the donor distributions.
2. Sample access-stage duration from the donor class in each system.
3. Sample uptake-stage time to half penetration from the donor class.
4. Repeat 10,000 times; report the 10th, 50th and 90th percentile year for each milestone.
5. Scenarios: current; access stage compressed to the best observed system; uptake stage compressed to the outpatient or in vivo benchmark; both.
6. Capital horizon: years from first-in-human to first revenue and to half penetration, per class per scenario.

**Backcast.** Run the model from 2003 for AAV and from 2012 for CAR-T with only information
available at the time; the observed histories must fall inside the 10th to 90th bands. If they
do not, report where and why before using the model forward.

**Forecast against record.** Extract the projected annual patients-treated series from S16 and
S17; plot against realized counts from layer 03; attribute the gap to the stage the projection
skipped.

**Output.** `data/projection/frontier_milestones.csv`: platform, scenario, milestone, p10, p50,
p90, donor_class, n_programs.

**Implementation, 6 September 2026 (D013).** `research/findings/project_landscape_2026-09-06.py` implements a
staged Monte Carlo for the whole class rather than per frontier programme: pipeline survival (S06 rates, measured
clinical-stage distributions, phase-remaining shares 0.70 to 1.00, 0.40 to 0.70, 0.15 to 0.40; programme entry at
the 2021 to 2025 rate), access lags and funding probabilities per system (F043, F035), class diffusion curves
S(1 - exp(-t/tau)) fitted to the observed penetration paths (CAR-T: run-rate over the label-dated flow, S 0.92, tau
8.6 years; one-time therapies: cumulative over the prevalent pool, initial rate 0.06 of the pool per year, saturation
not identified), CAR-T as a class anchored on the 2024 registry totals with new-disease approvals adding their own
pools, and a capacity check against qualified centres and observed throughput. Backcast: the pipeline at end-2019
predicted 30 (24 to 35) approvals in the five classes for 2020 to 2025 against 16 realised; calibration factors
CAR-T 0.45, AAV 0.50, lentiviral 1.0, CRISPR 0.50, in vivo 0.58 bring the backcast to 16 (12 to 21) with every year
inside the band. Outputs under `data/projection/`; figures `Figure_P1_approvals_projection.png` and
`Figure_P2_patients_projection.png` from `figures_projection_2026-09-06.py`. The donor-mapped frontier milestone
table above is still to be produced.

**Implementation, version 2, 7 September 2026 (D014).** `research/findings/project_landscape_2026-09-07.py` replaces the
6 September script. Stage A: constructs from `pipeline_constructs.csv` (F048); the primary unit is one lead programme per
sponsor and class among constructs with a US or European site, chosen because its uncalibrated backcast (18, 13 to 23)
covers the 16 approvals of 2020 to 2025 while the construct-level and all-site units overpredict (26 to 38); each
programme survives its remaining S06 transitions and its time to approval is drawn from the class lognormal (F032)
conditional on the time already elapsed since its first trial (left truncation), or for phase-3 programmes from the
cohort's phase-3-start-to-approval lognormal (3.6 years median, sigma 0.55, n 18) conditional on the time since the
phase-3 start. Stage B: funding times per system are inverse draws from the Aalen-Johansen cumulative incidence (F047),
scaled within its bootstrap band in the probabilistic run. Stage C: Bass curves (F049); CAR-T as a class follows the
registry-total fits per region with a bootstrap tuple per run, new-disease approvals add their own pools with a
per-product tuple; one-time therapies continue their own shrunk fits and new approvals draw a tuple and a pool; rest
of world is a share of US plus Europe. Uncertainty: fourteen assumptions with ranges and sources
(`projection_parameters.csv`, block "assumption") are drawn per block of runs in the headline run; `sensitivity_oneway.csv`
holds the tornado, `sensitivity_structural.csv` the pipeline units, calibration on and off and the pooled diffusion
curve; `validation.csv` records face, internal, cross, external and predictive validity in ISPOR-SMDM terms. Figures
P1 to P4 from `figures_projection_2026-09-07.py`. The per-platform frontier milestone table above is still to be
produced.
