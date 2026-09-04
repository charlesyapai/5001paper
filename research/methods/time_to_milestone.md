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
