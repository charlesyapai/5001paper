# Findings ledger

`findings_ledger.csv` is the single list of established facts. Columns:

| Column | Content |
|---|---|
| `id` | F001, F002, ... never reused |
| `date` | date established, ISO |
| `topic` | topic folder name |
| `statement` | the finding, with its numbers |
| `evidence` | file and script or command that regenerates it, or the document read |
| `source` | bibliography id or bundle path |
| `status` | one of the statuses in `research/README.md` |
| `confidence` | high, medium, low, with a reason if not high |
| `used_in` | where the finding is used |
| `notes` | anything a reader needs before reusing it |

`recompute_2026-09-04.py` regenerates F001 to F006 from the bundle's primary tables. Run it
from this folder:

```bash
python3 recompute_2026-09-04.py
```

`verify_cohort_dates_2026-09-04.py ../../data/cohort/raw` regenerates the dated cohort behind
F019 to F022. `calibrate_revenue_to_patients_2026-09-04.py ../../data/uptake/raw` regenerates
`data/uptake/pilot_*.csv` behind F023 to F025.

Later scripts (run from this folder with `../../.venv/bin/python`):

| Script | Regenerates |
|---|---|
| `build_uptake_series_2026-09-04.py ../../data/uptake/raw` | `data/uptake/patients_quarterly.csv`, `uptake_summary.csv` (F035) |
| `first_in_human_2026-09-04.py` | `data/cohort/first_in_human.csv`, `data/cohort/raw/fih_candidates.csv` (F032; live registry query) |
| `net_price_asp_2026-09-05.py` | `data/uptake/net_price_asp.csv` (F030) |
| `build_eligible_ranges_2026-09-05.py` | `data/uptake/eligible_population.csv`, `eligible_population_rows.csv` (F034) |
| `build_milestones_2026-09-05.py` | `data/uptake/milestones.csv` (F037); run after the three above |
| `forecast_vs_record_2026-09-05.py` | `data/projection/forecast_vs_record.csv` (F033) |
| `curate_label_events_2026-09-05.py` | `data/uptake/label_events.csv` from `raw/label_events.csv` (D012, F039); run before `build_milestones` |
| `build_milestones_2026-09-05.py [--label-events PATH]` | also `data/uptake/pool_quarterly.csv` for label-dated products (F039) |
| `net_price_variant_2026-09-05.py` | `data/uptake/patients_quarterly_variant.csv`, `net_price_variant_summary.csv`, `net_price_variant_checks.csv` (F040) |
| `build_cart_by_country_2026-09-05.py` | `data/uptake/cart_by_country.csv` (F041) |
| `build_investment_events_2026-09-05.py` | `data/investment/events.csv`, `events_summary.csv` (F042) |
| `build_access_decisions_2026-09-05.py` | `data/access/decisions.csv`, `access_summary.csv` (F043) |
| `project_landscape_2026-09-06.py [n_runs]` | `data/projection/approvals_projection.csv`, `access_projection.csv`, `patients_projection.csv`, `capacity_projection.csv`, `diffusion_fits.csv`, `pipeline_programmes.csv`, `projection_parameters.csv` (F044; D013) |
| `figures_projection_2026-09-06.py` | `figures/Figure_P1_approvals_projection.png`, `Figure_P2_patients_projection.png` (F044) |
| `build_governance_by_region_2026-09-06.py` | `data/access/governance_by_region.csv`, `stated_reasons.csv` (F045) |
| `access_time_to_event_2026-09-07.py` | `data/access/access_time_to_event.csv`, `access_survival_curves.csv`, `access_survival_summary.csv`, `access_indication_durations.csv` (F047); run after `build_access_decisions` |
| `fetch_trial_interventions_2026-09-07.py` | `data/projection/raw/trial_interventions.csv` (live registry query by NCT id: intervention names, site countries) |
| `render_ledger_view.py` | `ledger.md`, the Pages view of this ledger; run after every ledger change |

Order after a raw-table change: `build_uptake_series`, `build_eligible_ranges`, `curate_label_events`, `build_milestones`, then the
independent builders (`net_price_variant`, `build_cart_by_country`, `build_investment_events`, `build_access_decisions`).
