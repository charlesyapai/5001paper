# Gene and cell therapies: from trial to patient

How long does a gene or cell therapy take to reach the people it was made for, where does it slow down, and what will
the next ten years look like? This site holds the research base for that question: 43 approved products followed from
first-in-human trial to approval, from approval to a funding decision in eight health systems, and from funding to
patients treated, with a projection of approvals, access and patient numbers to 2036.

## Read in this order

1. [The landscape to 2036](manuscript/landscape_projection.md): what the model says about approvals, access by region, patients treated and hospital capacity, with the assumptions listed.
2. [Governance and blockers by region](manuscript/governance_by_region.md): how the United States, Germany, England, France, Italy, Canada, Australia, Singapore and China decide, how long they take, and what they say when they refuse.
3. [What the record shows so far](research/LOG.md): the dated log of every finding, newest at the bottom, with the [findings table](research/findings/ledger.md) behind it.
4. [The study design](manuscript/translation_timeline_plan.md) and the [decision record](research/DECISIONS.md).
5. The stage notes: [clinical](research/topics/01_clinical_stage/README.md), [access](research/topics/02_access_stage/README.md), [uptake](research/topics/03_uptake_stage/README.md), [investment](research/topics/04_investment/README.md), [projection](research/topics/05_projection/README.md), [diagnostics](research/topics/06_diagnostics/README.md).
6. The companion paper on what trial registries can and cannot show about why trials stop: [manuscript](manuscript/manuscript.md).

## The data

| Layer | Guide | Main tables |
|---|---|---|
| Cohort | [data/cohort](data/cohort/README.md) | `product_cohort.csv`, `first_in_human.csv` |
| Access | [data/access](data/access/README.md) | `decisions.csv`, `access_summary.csv`, `governance_by_region.csv` |
| Uptake | [data/uptake](data/uptake/README.md) | `patients_quarterly.csv`, `eligible_population.csv`, `milestones.csv`, `cart_by_country.csv` |
| Investment | [data/investment](data/investment/README.md) | `events.csv`, `events_summary.csv` |
| Projection | [data/projection](data/projection/README.md) | `approvals_projection.csv`, `patients_projection.csv`, `access_projection.csv`, `capacity_projection.csv` |

Every number on this site is in a table before it is in a sentence, and every table names the script that regenerates it
and the document it was read from. Methods are specified under [research/methods](research/methods/README.md).
