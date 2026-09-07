# Projection layer tables

| File | Content | Finding |
|---|---|---|
| `forecast_vs_record.csv` | Prior projections (NEWDIGS 2020, Tufts 2023, France 2023) against the realised approvals and patients | F033 |
| `raw/trial_interventions.csv` | Intervention names, site countries and sponsor for 2,982 interventional trials in the genetic subfamilies (registry fetch 2026-09-07) | F048 |
| `pipeline_constructs.csv` | Industry constructs per sponsor and class: trials, first start, phase-3 start, highest active phase today and by end-2019, US or EU site, approved product | F048 |
| `phase_durations.csv` | The cohort's own durations from the earliest phase-2 and phase-3 trial start to first approval | F048 |
| `diffusion_bass_fits.csv` | Bass fits: pooled and per-product (shrunk) for CAR-T and one-time therapies; class fits on the registry totals per region with bootstrap tuples | F049 |
| `diffusion_loo.csv` | Leave-one-product-out predictive checks of the Bass curves | F049 |
| `diffusion_paths.csv` | Observed and fitted penetration per product and quarter | F049 |
| `projection_parameters.csv` | Every fitted or assumed parameter with its source; the `assumption` block carries the low and high values used in the sensitivity analyses | F050, D014 |
| `approvals_projection.csv` | Backcast 2020 to 2025 for four pipeline units against the record; forecast 2027 to 2036 per class, per year and cumulative, 10th, 50th and 90th percentiles | F050 |
| `access_projection.csv` | Products with funded access per system and year, baseline and compressed-access scenarios | F050 |
| `patients_projection.csv` | Patients treated per year by class, region and scenario | F050 |
| `capacity_projection.csv` | CAR-T demand against qualified centres at the US and European growth trends and observed throughput | F050 |
| `sensitivity_oneway.csv` | Tornado: each assumption at its low and high value, headline outputs | F050 |
| `sensitivity_structural.csv` | Pipeline units, calibration on and off, pooled diffusion curve | F050 |
| `validation.csv` | Face, internal, cross, external, predictive and uncertainty validity in ISPOR-SMDM terms | F050 |

Regenerate in this order from `research/findings/`: `fetch_trial_interventions_2026-09-07.py` (live registry query; skip to keep the
2026-09-07 fetch), `build_pipeline_constructs_2026-09-07.py`, `fit_diffusion_2026-09-07.py`, `project_landscape_2026-09-07.py [n_runs]`
(production run 4,000; about three minutes), `figures_projection_2026-09-07.py`. The access curves come from
`access_time_to_event_2026-09-07.py`. Method and decisions: `research/methods/projection_model.md`, `diffusion_fits.md`, D013 and D014.
The 6 September scripts remain in the repository as the record of D013; their outputs are no longer kept.
