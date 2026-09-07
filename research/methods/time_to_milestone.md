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

**Access stage as time-to-event, 7 September 2026 (F047).** `research/findings/access_time_to_event_2026-09-07.py`
implements steps 1 to 3 and 5 for the access stage. Unit: product x system. Origin: the authorisation that puts the
product at risk in that system (EU authorisation for England, Germany, France and Italy; the Health Canada or TGA date
stated in the rows for Canada and Australia; FDA approval for the United States, where the at-risk set is limited to
products whose sponsor reports product revenue). Every authorised product is at risk, so never-submitted products are
censored at the data cutoff (5 September 2026) rather than dropped. Primary endpoint, defined once: the first decision that
makes the product available at public expense to part of its label population (NICE guidance including the Cancer Drugs
Fund and managed access; G-BA Beschluss; pCPA letter of intent; for France paid early access, JO inscription or a CEPS
price, whichever is first; AIFA determination; MSAC or PBAC support or a funding start; first revenue quarter in the
United States). Routine-listing sensitivity: France without early access; England without managed access. Competing
events: a refusal or a sponsor-terminated appraisal not followed by a positive step or a live resubmission; withdrawal of
the marketing authorisation. Estimators: Aalen-Johansen cumulative incidence (primary), Kaplan-Meier with competing
events censored (upper bound), bootstrap over products for the 60-month share. Outputs `data/access/access_time_to_event.csv`,
`access_survival_curves.csv`, `access_survival_summary.csv`. Extension indications are re-dated from the EMA procedural
steps in `label_events.csv` in `access_indication_durations.csv`; the product-level clock keeps the initial authorisation.
Known limits: no MHRA dates for products authorised after 2020 (England uses the EU date); Canada and Australia at-risk
sets depend on the rows stating a national authorisation; Australia has eight products.
