# Manuscript revision notes

Moved out of `manuscript/manuscript.md` on 6 September 2026 so the public reading copy carries the paper, not its
edit history. The notes are unchanged.

**Revision note (v3).** Draft v1 framed the central finding as a therapeutic-versus-diagnostic
contrast; referee review established it is an interaction with sponsor class, removed 33
double-counted registrations, and moved the payment claim off the registry counts. A third,
claim-by-claim review of v2 forced the following, all incorporated here. The title no longer says
"dominated by": business decisions are 30.9% of halts against recruitment's 28.7% (one-sided
binomial p = 0.23), so dominance holds only in the pairwise comparison against safety and
efficacy. "Halted programs" is now "halted trial registrations" throughout, and the conclusion no
longer quotes a point ratio. The financial-cause restriction is now a published boolean column:
the honest range is **0.8 to 6.1**, not 1.6 to 6.1, and it includes parity — so the aggregate
ratio is reported as uninformative about magnitude. The sponsor-exit instrument is reported at
this paper's own inclusion threshold, where it **significantly contradicts** the main measure
(ρ = −0.70, p = 0.036) rather than merely failing to corroborate it. Two sensitivity analyses the
limitations promised but never reported are now run and reported. A claim that terminated trials
are least likely to post results has been deleted: our own data show the opposite. The
falsification criterion in Section 3.4 has been narrowed to the joint condition the data actually
support. A pointer to a non-existent supplementary row has been corrected, the censoring figure
recomputed on a strict deduplicated basis (24.7%, not 30.6%), and a reference list added.

**Revision note (v7, 5 September 2026).** Two defects recorded in the referee pitch (section 6a) are
fixed. The heading of Section 2.3 and the Conclusion claimed the "most mature" modality is the
most fragile while the body of 2.3 withdrew that property; both now state the property the argument
uses, earliest genetic modality to reach pivotal trials, which AAV holds uniquely on
`technology_maturity_matrix.csv` (`first_ph3_year`). The References note pointed the untested
non-molecular comparator at Section 8 item 5, which is the human-validation item; the comparator is
now Section 8 item 6 and the note points there. The header version, which still read v3, is
corrected. No number in the paper changed.

## v8, 7 September 2026

The matched non-molecular comparator (Section 8 item 6 since v7) has been run (F052; `data/companion/`): 378
industry-sponsored halted drug trials outside molecular medicine, matched on phase and start year and classified under
the same instruction, cite business reasons at 60% against the cell's 64% (p = 0.34). Under the rule set before the
pull (within ten points ends the specificity claim), the industry-therapeutic elevation is generic to industry-sponsored
early-phase drug trials. Changes: one sentence in the abstract; new Section 3.5 with the result and its caveat (a later
version of the same model family labelled the comparator strings under the identical instruction; the keyword flags
agree); Limitation 3c now cites the comparator; Section 8 item 6 records the run; the References note points to
Section 3.5. The title and the headline stratified contrast are unchanged; the interpretation that the pattern is a
property of commercial sponsors rather than of molecular biology is now supported by the comparator rather than argued
from the stratification alone. The blank human-coding sheet (item 5) is `data/companion/halt_human_coding_sheet.csv`.
