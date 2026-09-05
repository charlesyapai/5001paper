# Time to milestone

**Measures.** Time from an origin event to a milestone, with censoring and competing risks.

**Origins.** First-in-human trial start; regulatory approval; first reimbursement decision.

**Milestones.** First approval; first reimbursement; first commercial patient; a quarter of the
eligible-population range; half of it; withdrawal, restriction or discontinuation.

**Procedure.**
1. One row per product per origin-milestone pair, with dates and a censoring flag at the data cutoff.
2. Kaplan-Meier curves by technology class; median and interquartile times where reached.
3. Withdrawal, restriction and discontinuation as competing risks for uptake milestones, using cumulative incidence rather than treating them as censored.
4. Cox models with class and the determinants in `cross_country_design.md`, reported as association.
5. Recent approvals are censored, not excluded; report the number at risk at each year.

**Eligible population.** A range from label, epidemiology and company guidance. Milestone times
are computed at both ends of the range and reported as a range.

**Output.** `data/uptake/milestones.csv`: product, class, origin, milestone, origin_date,
milestone_date, censored, eligible_low, eligible_high, source_notes.

**Implementation, 5 September 2026.** `research/findings/build_milestones_2026-09-05.py` joins
`data/cohort/first_in_human.csv` (clinical stage), `data/cohort/product_cohort.csv` (approvals),
`data/uptake/patients_quarterly.csv` and `data/uptake/eligible_population.csv`, and writes
`data/uptake/milestones.csv`. Origins: first-in-human (earliest registered interventional trial of the
construct, including its academic origin) and first approval anywhere. Milestones: first quarter with
revenue; a quarter and half of the eligible pool, at both ends of the range (conservative: lower-bound
patients against the upper-bound pool; optimistic: central patients against the lower-bound pool),
censored at 30 June 2026 where not reached. Eligible pool for one-time therapies: prevalent range at
launch plus the annual incident range times years since first revenue; for oncology cell therapies:
annual eligible times years since first revenue, with run-rate penetration (last four quarters over the
annual range) as the primary measure. Denominator geography follows the revenue series: US when the
series is US-only or a US split covers most quarters, otherwise US plus EU where both ranges exist,
otherwise US with a flag that worldwide revenue is being divided by a US denominator. H1 is read per
product: decided where half of the pool is reached at both ends of the range, or where follow-up
already exceeds the clinical stage without reaching half; otherwise not yet decidable.

**Label-dated pools, 5 September 2026 (D012).** For products with verified label events in
`data/uptake/label_events.csv` (columns `product_key, geography, event_date, action, indication_key,
replaces, source_url, status`), the pool is rebuilt quarter by quarter from
`data/uptake/eligible_population_by_indication.csv`: only indications on the label on a given day count;
an extension that widens an existing population names the narrower key in `replaces` and supersedes it;
an added disease adds its own range; a restriction removes its key; the annual inflow is day-weighted in
the quarter of a change. `indication_key` may list aliases separated by semicolons where two source
vocabularies name the same population in different families (an annual inflow key and a prevalent stock
key); aliases within one family must not overlap, or the pool double counts. When the product has no
eligible row for an indication in force, the range of another product with the same indication and
geography is borrowed and flagged; when none exists the pool omits that indication and the flag says so.
The per-quarter pools are written to `data/uptake/pool_quarterly.csv`; `milestones.csv` carries a
`pool_basis` column. Products without label events keep the static pool and their rows are unchanged.
