# Open items

Priority order. The first two block external circulation of the manuscript.

---

## 1. Two defects in the current draft (v7)

**A superlative the paper's own caveat retracts.** Section heading 2.3 reads *"The most
mature modality is the most commercially fragile"*, and the Conclusion repeats it. Two
sentences into §2.3 the paper states that four therapeutic platforms tie at the top maturity
stage — AI-originated candidates, AAV gene transfer, CRISPR nuclease editing and in vivo LNP
— *"so 'most mature' is not a property we can assign uniquely."* The heading asserts what the
body withdraws.

*Fix:* retitle §2.3 to "The earliest modality to reach pivotal trials is the most commercially
fragile" — the property the argument actually uses, and one AAV holds uniquely — and make the
same substitution in the Conclusion. Verify against
`data/derived/technology_maturity_matrix.csv` (`stage_n`, `modality`).

**A cross-reference that does not resolve.** The References section says the non-molecular
comparator *"has not been run (Section 8, item 5)"*. Section 8 item 5 is human validation of
the halt classification. The comparator is not in Section 8 at all — so the analysis both
prior referees called the biggest hole is missing from the paper's own list of what would
strengthen it.

*Fix:* add the comparator to Section 8 and repoint the reference.

---

## 2. The non-molecular comparator (the one extension that changes the paper's standing)

Every comparison in this study is within molecular precision medicine. A reader cannot
currently tell whether a 66%-versus-22% split is remarkable or simply what
ClinicalTrials.gov looks like when *any* therapeutic area is stratified by sponsor class.

Two candidate comparators, both cheap:

- The 5,601 imaging-AI trials already in `data/primary/trial_records.csv` (subfamily
  `AI/ML referenced in protocol`) — already retrieved and classified.
- A fresh pull of a mature small-molecule area, using `01_retrieve.py` with a new row in
  `queries.csv` and `filter_regex.csv`.

Run the same stratified contrast. **If the interaction is specific to molecular precision
medicine, this is a substantially stronger paper. If it is generic to industry-sponsored
therapeutics, the paper becomes a study of how commercial sponsors report stopping** — still
publishable and honest, but a different paper with a different title. Either way this is the
first thing a referee will ask for, and it is one query plus one classification run.

---

## 3. Human validation of the halt classification

The largest methodological gap. Every count rests on a single machine coder with no
inter-rater statistic. `02_classify_halts.py --sample 200` writes a blank coding sheet;
hand-code it and report a kappa. Cheapest high-value item on this list.

## 4. Sponsor-level survival analysis

First-to-last trial interval per sponsor is a better commitment signal than trial volume, and
would replace the sponsor-exit proxy that currently *disagrees* with the main measure
(ρ = −0.70, p = 0.036 at the paper's own inclusion threshold). The required fields are
already in `trial_records.csv` — this is a rewrite of one analysis, not new data. It also
addresses the leading explanation for the disagreement: that the exit measure is dominated by
one-trial academic-adjacent sponsors.

## 5. Model the interaction directly

Replace six stratified two-by-two tables with one logistic regression carrying a
modality×sponsor interaction term, sponsor-clustered standard errors, and subfamily as a
random effect. Three benefits: one interaction estimate instead of six tables, the clustering
objection absorbed formally, and **adjustment for start year — currently unadjusted and a
live confounder**, since business-attributed halting may simply be more common in recent
years.

## 6. Recover the censored arm

Completed-but-failed later-phase trials are invisible to the reason field. Linking to posted
results for the ~18% of due trials that reported would let you count endpoint failures
directly and bound how much scientific failure the instrument misses — turning Limitation 3b
from a caveat into a measurement.

## 7. A deal and financing layer

Keyed by sponsor, joining to the halted-trial table through the `sponsor` field. This is what
would convert "a business decision" into a dated and priced event, and is the only route to
making the payment claim rest on the registry rather than on six curated cases. Requires a
commercial data source this project never had.

## 8. Non-US registries

CTIS, ChiCTR, jRCT — would correct the geography claims and the halt-rate estimates. Lower
priority: it widens coverage but does not answer a standing objection.

---

## Narrative decision, resolved 4 September 2026

The flagship paper is no longer either Option A or Option B. It is the **translation timeline**
laid out in `manuscript/translation_timeline_plan.md`: the same question, measured after
approval where prices, payers and patients are observable, with the same product across
health systems as the control for biology.

What that means for the items above:

- **Items 1 to 3 still apply**, now to the companion methods paper built from the halt-reason
  analysis. Run the phase- and start-year-matched comparator, not the imaging-AI subset, which
  is already inside the industry-diagnostic control cell and can never populate the
  therapeutic row. Add an audit of the 95 industry-therapeutic business halts against press
  releases and filings alongside the kappa.
- **Item 4** moves into the flagship as part of the investment layer.
- **Item 5** is superseded by the flagship's time-to-milestone and cross-country models.
- **Item 6** is superseded: efficacy failure is observed post-approval through withdrawal and
  restriction events and through the real-world effectiveness comparison.
- **Item 7** becomes the flagship's investment layer, built from public disclosures rather than
  a commercial deal database.
- **Item 8** stays low priority for the companion paper; the flagship covers non-US systems
  directly through the access and uptake layers.
