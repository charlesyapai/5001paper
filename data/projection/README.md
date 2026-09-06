# Projection layer tables

| File | Content | Finding |
|---|---|---|
| `forecast_vs_record.csv` | Prior projections (NEWDIGS 2020, Tufts 2023, France 2023) against the realised approvals and patients | F033 |
| `pipeline_programmes.csv` | Industry programmes per platform at their highest active phase, today and as the pipeline stood at the end of 2019 | F044 |
| `projection_parameters.csv` | Every fitted or assumed parameter of the model with its source | F044, D013 |
| `approvals_projection.csv` | Backcast 2020 to 2025 (uncalibrated and calibrated) against the record; forecast 2027 to 2036 per class, per year and cumulative, 10th, 50th and 90th percentiles | F044 |
| `access_projection.csv` | Products with funded access per system and year, baseline and compressed-access scenarios | F044 |
| `diffusion_fits.csv` | Class diffusion curves fitted to the observed penetration paths, with bootstrap spread | F044 |
| `patients_projection.csv` | Patients treated per year by class, region and scenario | F044 |
| `capacity_projection.csv` | CAR-T demand against qualified centres at trend and observed throughput | F044 |

Regenerate with `research/findings/project_landscape_2026-09-06.py [n_runs]` (production run 4,000) and the figures with
`figures_projection_2026-09-06.py`. Method and decision: `research/methods/projection_model.md`, D013.
