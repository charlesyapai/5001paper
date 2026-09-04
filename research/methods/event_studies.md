# Event studies

**Purpose.** Estimate the effect of named architecture changes on access timing and uptake.

**Events.** `data/cohort/policy_events.csv`, each verified before use.

**Design.** Interrupted time series on the affected product or class, with at least four
pre-event and four post-event quarters. Where a comparator product exists in the same system
and was not affected, a difference-in-differences. Where several unaffected products exist, a
synthetic control built from them.

**Placebo checks.** Shift the event date by two quarters in each direction; run the same design on
an unaffected product.

**Reporting.** Effect on level and on slope, with confidence intervals; the number of quarters
used; and the placebo results next to the main result.

**Candidates most likely to be estimable.** Removal of REMS requirements for autologous CAR-T
(2025); the CMS Cell and Gene Therapy Access Model (2025); NICE recommendations for Casgevy
(2024, 2025); Zynteglo's Germany withdrawal and US relaunch (2021, 2022).
