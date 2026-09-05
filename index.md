# PHM5001 final project

Two papers share this repository. The flagship is the **translation timeline for gene and cell therapies**: how long each
product took from first-in-human trial to approval, from approval to reimbursement in six health systems, and from
reimbursement to patients treated, with the frontier platforms projected from those measured stages. The companion is a
**registry methods paper** on what the ClinicalTrials.gov stated-reason field can and cannot show about why trials halt.

## Reading order

1. [Translation timeline plan](manuscript/translation_timeline_plan.md), the flagship's design (decision D001).
2. [Research log](research/LOG.md), what was done and found, newest at the bottom.
3. [Findings ledger](research/findings/ledger.md), every established fact with its evidence and status (rendered from `findings_ledger.csv`).
4. [Decision record](research/DECISIONS.md), D001 to D012.
5. Topic notes, one per stage: [clinical](research/topics/01_clinical_stage/README.md), [access](research/topics/02_access_stage/README.md),
   [uptake](research/topics/03_uptake_stage/README.md), [investment](research/topics/04_investment/README.md),
   [projection](research/topics/05_projection/README.md), [diagnostics](research/topics/06_diagnostics/README.md),
   [companion methods paper](research/topics/07_companion_methods_paper/README.md).
6. [Companion manuscript, draft v7](manuscript/manuscript.md) and its [referee pitch](review/referee_pitch.md).
7. [Open items](OPEN_ITEMS.md) and the [research base conventions](research/README.md).

## Tables

| Layer | Guide | Main tables |
|---|---|---|
| Cohort | [data/cohort](data/cohort/README.md) | `product_cohort.csv`, `first_in_human.csv` |
| Access | [data/access](data/access/README.md) | `decisions.csv`, `access_summary.csv` |
| Uptake | [data/uptake](data/uptake/README.md) | `patients_quarterly.csv`, `eligible_population.csv`, `milestones.csv`, `cart_by_country.csv` |
| Investment | [data/investment](data/investment/README.md) | `events.csv`, `events_summary.csv` |
| Projection | [data/projection](data/projection/README.md) | `forecast_vs_record.csv` |

Methods are specified under [research/methods](research/methods/README.md); the scripts that regenerate every number are
listed in [research/findings](research/findings/README.md). The original migration guide for the registry study is the
repository [README](README.md).
