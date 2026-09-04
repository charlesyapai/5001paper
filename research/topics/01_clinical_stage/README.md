# 01 · Clinical stage: first-in-human to approval

## Scope
Durations and attrition from first registered trial to first regulatory approval, by platform
subfamily, plus the pipeline counts the projection layer consumes.

## Questions
- How long did each mature platform take from first-in-human to first Phase 3 and to first approval?
- What are the phase transition probabilities for durable cell and gene therapies, from the published literature?
- How large is the frontier pipeline (base editing, prime editing, epigenome editing, in vivo LNP) and at what phase?

## What we know
- Per-subfamily first trial year, first interventional year and first Phase 3 year are in `data/derived/technology_maturity_matrix.csv` (`first_year`, `first_int_year`, `first_ph3_year`), with maturity stage and phase counts. AAV first trial 1999, first Phase 3 2003 (manuscript section 2.3).
- Frontier pipeline counts: base editing 28 trials, prime editing 2, epigenome editing 2, in vivo LNP 68 (`trial_records.csv` subfamily counts).
- A published success-rate analysis for durable CGT exists and has not yet been extracted (F017).
- Halt dates and intervention names are not retained in `trial_records.csv`; start year is the only timing field on halted trials (F003 note).

## Sources
S06 (clinical success rates), S27 (EMA approval timelines), FDA CBER product pages for approval dates, EMA EPARs.

## Method
Descriptive stage durations per subfamily. Approval year joins from `data/cohort/product_cohort.csv` once dates are verified. See `research/methods/time_to_milestone.md` for the shared milestone definitions.

## Tasks
1. Week 1: read S06; extract phase transition probabilities and median phase durations into a table under `data/cohort/`.
2. Week 1: verify approval dates for every row of `product_cohort.csv` from FDA and EMA product pages.
3. Month 1: extend `code/01_retrieve.py` to retain `lastUpdatePostDate`, `statusVerifiedDate`, `whyStopped` and intervention names, so halts can be dated and clustered by asset.
4. Month 1: compute first-in-human to first approval per platform from the joined tables.

## Open questions
- Which trial counts as first-in-human for platforms whose early trials were academic and outside the US registry?
- Should approval be the first approval anywhere or the first FDA or EMA approval? Proposal: record both.
