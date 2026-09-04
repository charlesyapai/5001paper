# Referee report — "The binding constraint in molecular precision medicine is payment, not biology"

**Reading as:** a working scientist deciding what to pursue next in genetic medicine / proteomics.
**Recommendation:** major revision.

I want this paper to exist. The instrument is clever, Section 3 is more honest than most papers
manage, and the diagnostic half of the thesis holds up under everything I threw at it. But the
half that gives the paper its title does not survive stratification by sponsor class, and the
category that carries it contains no sponsor statement that names a payer. That is fixable —
mostly by reframing to what the data actually shows, which is a sharper claim than the one
currently made — but it cannot be fixed in copy-editing.

All re-analysis below is computed from the supplied tables; numbers are in
`referee_reanalysis_stratified.csv` and `referee_boundary_sensitivity.csv`.

---

## 1. Does the argument hold?

### 1.1 The therapeutic/diagnostic split is an artefact of who sponsors what (blocking)

Section 2.1 concedes in passing that "the axis which really matters is whether a commercial
sponsor is carrying the program; modality is a good but imperfect proxy for that." It is not an
imperfect proxy. Once you condition on sponsor class, modality carries **no** independent
information about business-cited halting:

| stratum | therapeutic | diagnostic | OR | p |
|---|---|---|---|---|
| all halts (as published) | 41.1% | 23.0% | 2.33 | 2.6e-08 |
| **industry sponsors only** (n=229) | 66.0% | 26.8% | 5.29 | 9.6e-09 |
| **non-industry sponsors only** (n=588) | 22.9% | 22.2% | **1.04** | **0.47** |
| non-industry, CAR-T excluded (n=436) | 20.4% | 22.2% | 0.90 | 0.67 |

And the rival exposure is far stronger than the published one. *Within therapeutics*, sponsor
class gives OR **6.54** (industry 97/147 = 66.0% vs non-industry 46/201 = 22.9%, p = 4.3e-16) —
nearly three times the headline effect size. Within diagnostics, sponsor class does nothing
(OR 1.28, p = 0.22).

So the finding is an interaction, not a main effect: **industry-sponsored therapeutics** are
halted for stated business reasons; academic therapeutics fail exactly like academic
diagnostics. The CAR-T sensitivity analysis in Section 2.1 does not address this — CAR-T
exclusion and industry stratification are different cuts, and in the non-industry stratum the
effect is absent with or without CAR-T.

This matters beyond bookkeeping, because Section 4.1's "two failure modes require two remedies"
is built on the modality reading. On the sponsor reading, the remedy structure changes: the
therapeutic remedies (annuity payment, platform qualification) are remedies for *commercial*
programs, and the paper's own N-of-1 case (4.8% industry) shows a therapeutic modality that
needs the *diagnostic* remedy — evidence and a funding mechanism — not an annuity.

**Fix.** Reframe on the interaction. State it as: the payment constraint is observable only
where a commercial sponsor exists to make a portfolio decision, and modality predicts nothing
once sponsorship is held constant. Then the honest generalisation to the frontier editors in
Section 3.3 becomes conditional on their being commercially sponsored — which is a testable
prediction rather than an assumed one. Add the 2×2 (modality × sponsor class) as Figure 1c or
replace 1a with it.

### 1.2 Can sponsor-stated reasons bear this weight? Not as currently used (blocking)

The paper's central interpretive move is that business-cited halts mean *no payer would buy*
(Section 4.1: "it fails because no payer would buy"; Section 1: value in a shape "neither
health-system budgets nor capital markets are built to price"). I searched all 817 verbatim
strings for `reimburs|payer|payor|price|pricing|cost of goods|market size|commercial viab|
payment|coverage|HTA`:

> **Zero of 817 halt reasons name a price, a payer, a reimbursement decision or a market size.**

Only 76 of the 251 business-cited strings (30%) name *any* financial cause at all. Decomposing
the category by language, it is two different phenomena that map onto the modality split:

| | diagnostic | therapeutic |
|---|---|---|
| grant / funding exhausted | **57** | 17 |
| portfolio / strategic | 23 | **83** |
| bare ("sponsor decision", no cause) | 28 | 39 |
| both | 0 | 4 |

"My grant ran out" (the diagnostic mode) and "we reprioritised the pipeline" (the therapeutic
mode) are pooled, and the pooled category is then read as one mechanism — a payment
architecture. Neither sub-phenomenon is a payer refusing to buy. Academic grant exhaustion is
a research-funding fact, not a health-system pricing fact; portfolio reprioritisation is a
capital-allocation fact whose *cause* is unstated and may well be scientific.

The paper's Limitation 2 treats this as a bounding problem ("business share is an upper bound").
That is the wrong shape of caveat. The problem is not that the share is too high; it is that the
category does not identify the mechanism the paper attributes to it. An upper bound on a
mislabelled quantity is still mislabelled.

**Fix.** (a) Publish the decomposition above — it is a genuine finding and it strengthens the
diagnostic half. (b) Retitle the category "sponsor-attributed discontinuation" throughout and
reserve "payment" for the post-approval cases (Section 2.6), where price and reimbursement
*are* documented. (c) Rewrite Section 4.1's "no payer would buy" as an inference from Figure 6,
not from Section 2.1.

### 1.3 The instrument is blind to how scientific failure normally presents (blocking)

An efficacy failure in a Phase 2/3 trial usually manifests as a trial that **completes** and
misses its endpoint — not as a halt with a stated reason. The reason field therefore cannot see
the dominant mode of scientific failure, and the 5.8:1 ratio is computed on the subset where it
is structurally least likely to appear:

- 2,273 interventional Phase 2+ trials; 769 concluded.
- **534 completed vs 235 halted** → the reason field observes only **30.6%** of concluded
  Phase 2+ trials.
- Among the 534 completed, only 247 (46%) posted results — so for over half, an efficacy
  failure is not readable from the registry at all.
- For therapeutics specifically: 175 completed vs 124 halted.

This is selection, not attribution, and Limitation 2 does not cover it. The abstract's claim
that business decisions "terminate 5.8 times as many programs as safety and efficacy failures
combined" is true of *halted* trials and not of programs, which is the noun the abstract uses.

The paper's own flagship case shows the mechanism concretely. Of AAV's 18 business-cited halts:
four name finance; one names "lack of drug supply" (manufacturing, not business); one is
*"Sponsor decision to terminate; sufficient sample size for statistical analysis has been
achieved"* — a trial that met its target, counted as a business halt; and one is *"Sponsor has
suspended clinical development of MYDICAR for heart failure"*, which is a well-documented
Phase 2b efficacy failure recorded as a strategic decision. The remainder are bare sponsor
decisions. Section 2.3's "This is not a technology that failed to work" is asserted over a
set of 18 strings that includes at least one technology that demonstrably did not work.

**Fix.** State the censoring explicitly as Limitation 2b with the 534/235 numbers; add the
misclassified rollover-equivalents (the "sufficient sample size" row) to the administrative
exclusions; and soften Section 2.3 to what the strings support — that AAV's *stated* halt
reasons are overwhelmingly non-scientific.

### 1.4 The 5.8:1 headline is a category-boundary artefact (major)

| boundary choice | ratio |
|---|---|
| as published (business vs safety+efficacy) | 5.8:1 |
| manufacturing counted as technical | 4.0:1 |
| + regulatory/ethics hold | 2.5:1 |
| + protocol redesign | 2.0:1 |
| business restricted to texts naming a financial cause | 1.8:1 |

Counting manufacturing as a business rather than a technical failure is hard to defend in a
paper whose Section 4.5 recommendation #2 is that *"delivery and manufacturing are the
underpriced problems"* and whose Section 4.1 names "cost of goods" as a technical bottleneck.
The two headline categories jointly cover only 36.0% of the 817 halts. And recruitment (234) is
nearly as large as the business category (251) overall, is the largest single cause in three of
the four families, and is the modal cause among diagnostic halts (172/469) — yet the abstract
cites it only inside the diagnostic contrast, never as a quantity comparable to the one the
headline ratio is built on.

**Fix.** Report the ratio as a range across boundary choices, or drop the single-number
framing and lead with the modality/sponsor contrast, which is where the paper's actual
contribution is.

### 1.5 Two smaller argument gaps

**No external baseline (major).** The paper never establishes that a 5.8:1 ratio, or a 30%
business-cited share, is unusual. Published ClinicalTrials.gov termination analyses across all
therapeutic areas find recruitment dominant and business/funding substantial; without a
non-precision-medicine comparator the reader cannot tell whether this is a fact about molecular
precision medicine or a fact about ClinicalTrials.gov. Since Section 1 frames the paper against
imaging AI, the cleanest comparator is already in hand: the 5,601 AI/ML trials, 46% of which are
imaging/pathology. Run the same halt-reason classification on the imaging subset and report the
contrast. That single addition would convert the thesis from an observation into a comparison.

**Unfalsifiability in Section 2.1 (major).** Both therapeutic platforms that sit on the
"wrong" side of Figure 1b are explained by absence of a commercial sponsor. Since absence of a
commercial sponsor is itself framed as part of the payment problem, no therapeutic platform's
position can disconfirm the thesis. Add an explicit falsification statement: what pattern in
these data would have refuted the claim?

**Section 3.1 applies an inconsistent power standard (minor).** ρ = 0.00, p = 1.00 on n = 10
platforms is given as having "removed the easy recommendation" and established that "the payment
architecture is defective across the pipeline." Section 3.2 correctly caveats n = 8 as
underpowered. Apply the same caveat to 3.1; a null at n = 10 removes nothing.

---

## 2. Is it useful? Section 4.5 is not yet actionable

The paper is genuinely useful in one respect already: Section 2.5's separation of activity
volume from readiness (ρ = −0.08) is the kind of thing that would stop me over-reading a
crowded field, and Section 2.7's reporting numbers changed how I would read a platform's trial
count. Keep both.

Section 4.5 does not survive the same test. Item 1 ("identify which constraint binds your
technology before optimising against the other") restates the finding as an instruction without
supplying the procedure — I cannot tell from it which cell my own platform is in. Item 2
("delivery and manufacturing are the underpriced problems") is the most useful sentence in the
paper and is the one claim in the section supported by no measurement: there are 20
manufacturing-cited halts in the dataset and they are counted on the business side of the
headline ratio. Item 3 is close to actionable but stops at exhortation.

**What would make it actionable — all from data in hand:**

1. **A per-subfamily lookup table.** For each of the 21 subfamilies: dominant blocker, sponsor
   mix, assay-as-intervention trial count, Phase 3+ count, stage, results-posting rate. A
   scientist finds their own row and reads their binding constraint off it. This is a
   restructuring of tables you already have, and it is the artefact a reader would actually use.
2. **Quantify the liquid-biopsy template.** Section 4.1 already has the shape: liquid biopsy
   reached reimbursable status with 278 assay-as-intervention trials, 23 at Phase 3+, over ~a
   decade; affinity proteomics has 1 and 0. Turn that into a stated benchmark — the approximate
   assay-as-intervention volume associated with crossing into pivotal evidence — and then name
   every platform below it. That converts "generate decision-change evidence" into a number.
3. **Name the delivery-reuse claim as a testable one.** Section 4.1 calls platform qualification
   "the highest-leverage item" without measuring leverage. You can at least bound it: CRISPR
   reached Phase 3 in two years by inheriting AAV/lentiviral delivery, while base/prime/epigenome
   editing have not. Report that transit-time contrast explicitly as the evidence for reuse value.
4. **Indication-level orphaning.** Which conditions have the most halted programs and no
   surviving one? That is the most direct answer to "what should I work on," and the conditions
   field is in `trial_records.csv`.

---

## 3. Do the figures earn their place?

**Nine figures is two or three too many.** My triage:

- **Figure 1 — load-bearing but currently the wrong figure.** Panel (a) presents the stated-reason
  categories at face value, which is exactly the contested step (§1.2 above); panel (b) is the
  better half and should lead. Two specific problems. First, the two modality arms are not
  comparable in composition: the diagnostic arm is 74% "AI/ML referenced in protocol" (144),
  mass-spec proteomics (97) and pharmacogenomics (115) — and "AI/ML referenced in protocol" is a
  keyword flag on the parent trial, not a diagnostic technology that must change a clinical
  decision. The mechanism sentence in Section 2.1 does not describe most of the arm it is
  computed on. Second, the figure the paper needs — modality × sponsor class — is in neither the
  deck nor the text. Make that Figure 1. As a check, the "every diagnostic platform sits at or
  above the diagonal" claim does verify (Clinical WGS/WES sits exactly on it at 0.300/0.300), but
  it verifies for five platforms, one of which is a keyword flag.
- **Figure 2 — merge into Figure 3.** It sits at family level between Figure 1a (modality) and
  Figure 3 (platform) and adds one fact those two do not carry: recruitment leads in three of
  four families. That is a sentence. An 11-category × 4-family dot matrix is a lot of ink for it.
- **Figure 3 — load-bearing.** The AAV panel is the paper's strongest single image. Relabel so the
  denominators match Figure 1b (Figure 3 shows AAV 18/25 and CRISPR 10/21; readers will compare
  against 2.1's counts and stumble).
- **Figure 4 — load-bearing.** The "delivery matured a decade before precision" observation is the
  paper's best structural insight and this is where it lives. Keep.
- **Figure 5 — keep, shrink.** A full-page ranked bar chart carrying a null correlation. The
  content is useful for the target reader; it can be a two-panel figure with Figure 4.
- **Figure 6 — keep, demote.** Six curated cases, and rhetorically the most persuasive thing in the
  paper. It is also, per §1.2, the *only* place where price and reimbursement are actually
  documented — so it is more load-bearing than the paper credits. Keep it, retain the honesty
  flag, but stop calling it "weaker" evidence in Section 2.6 while relying on the registry
  section for the payment claim; the epistemic ordering is backwards.
- **Figure 7 — load-bearing.** Four-panel evidence-quality figure; the single-arm and
  results-posting panels are the ones that would change my behaviour.
- **Figure 8 — move to supplementary.** The access/equity material is a different paper's thesis.
  It does not bear on payment-vs-biology, and Section 2.8's own caveat concedes the left panel
  measures where research happens rather than access. In a contrarian paper, every claim that
  isn't load-bearing is an extra surface to be attacked on.
- **Figure S1 — correctly placed.**

**Net: eight figures become five or six** (1 reframed, 2+3 merged, 4+5 merged, 6, 7; 8 to
supplementary), which leaves room for the sponsor-exit figure below.

---

## 4. Structure, length, and what is missing

**Cut.** Section 4.3 (ethics) claims four issues follow "from the measurements rather than from
general principle," but three of the four are general principle with a dataset number attached.
Compress to one paragraph and keep only the withdrawal-after-approval point, which does follow
from Section 2.6. Section 4.2's regulatory-capacity material (staffing reductions) should go;
Section 4.2's LDT-versus-PMA route-selection point should stay and be expanded, because it is
genuinely the binding regulatory variable for the diagnostic half of the thesis. Section 4.4's
policy paragraphs are the weakest-sourced prose in the paper and are attached to a registry
analysis that does not need them.

**Missing, and available in the supplied data.**

1. **Sponsor-level exit analysis — this is the paper's missing keystone, and Section 8 already
   admits the fields are in hand.** It is not future work: `trial_records.csv` yields 1,035
   sponsors with ≥3 trials, median first-to-last span 7 years, and 100 such sponsors whose last
   trial started in 2021 or earlier. A sponsor that stops registering trials entirely is a
   *behavioural* measure of commercial withdrawal that does not depend on the self-reported
   labels §1.2 shows cannot carry the interpretation. If sponsor exits cluster in therapeutic
   platforms and track the business-cited halts, the thesis is corroborated by an independent
   instrument. Run this before resubmission; it addresses the paper's central vulnerability
   more effectively than anything else available.
2. **A time trend, which I ran and which supports you.** The business-cited share of halts rises
   monotonically with trial start era — 20.7% (2005–10), 24.4% (2011–15), 27.3% (2016–20), 37.5%
   (2021–24); ρ = 0.151, p = 7e-05, n = 690. In the industry-therapeutic cell it goes 56.4%
   (2016–20) to 70.5% (2021–24). This is a direct test of Section 6's prospective claim that
   the payment architecture has not changed, and it currently appears nowhere. It needs the
   obvious alternative reading stated — that registry reporting practice and field composition
   also changed over the period — but it belongs in Section 2.
3. **Halt rates, not just halt mixes.** Section 2.1 notes in an aside that AAV halts 8% of its
   trials and CRISPR 18%, then never returns to it. A payment constraint should show up in
   rates, and the mix-versus-rate distinction is the first thing a hostile reader will press.
4. **A falsification statement** in Section 3.

**Wrong section.** The disclosure-incentive caution is the paper's principal vulnerability and
currently appears as two sentences in Section 2.1 and one line in Limitation 2. With the
decomposition in §1.2 above it deserves its own subsection in Results (2.2), before the
family-level analysis rather than after it.

---

## 5. Tone

The analysis is more careful than the prose, and the prose will be what gets attacked. Specific
places where the writing is doing work the evidence isn't:

- **Title.** "is payment, not biology" asserts flatly what Section 3.3 concedes is uneven and
  partly a prediction, and what §1.2 shows the evidence cannot name. Something closer to
  *"Program halts in molecular precision medicine are dominated by sponsor-attributed business
  decisions, not scientific failure"* costs you nothing rhetorically and is defensible.
- **Abstract:** "Molecular precision medicine is usually described as a field waiting on biology.
  We show it is not." You show that halted trials rarely cite science. Those are different
  statements, and the second is the one you can defend.
- **§2.1:** "Two therapeutic platforms are exceptions and are informative rather than awkward."
  This tells the reader how to feel about disconfirming data. Delete the editorial clause and
  let the analysis stand — and see §1.5 on the unfalsifiability the passage creates.
- **§2.3:** "This is not a technology that failed to work." Not supportable over a string set
  containing MYDICAR. Rewrite as a statement about stated reasons.
- **§4.1:** "the highest-leverage item" — asserted leverage, unmeasured. Either bound it (see
  §2 item 3) or mark it as a hypothesis.
- **§4.4:** "Two independent methods converging matters here." Trade commentary on deal flow and
  sponsor-stated halt reasons are not independent methods; they are partly the same events
  reported through different channels. Overstated in exactly the place a skeptical reader is
  looking.
- **§4.4:** "This is the counter-example that prevents the analysis from being merely
  pessimistic" — editorialising about the paper's own mood; the LNP finding is interesting on
  its own.
- **§6:** "Neither failure is a biology failure" — untenable given manufacturing, regulatory
  holds, and the censoring in §1.3.
- **§1:** "The answer reframes what the field's central problem is, and therefore what work is
  worth doing." Let Section 4.5 earn this rather than promising it in the introduction.

One structural note on tone: the paper is at its most persuasive where it is most restrained —
Section 3, the Figure 1b cautions, Limitations 6 and 7. A contrarian thesis defended in that
register is very hard to dismiss. The advocacy passages above are the handholds a hostile
reader will use, and none of them is load-bearing.

---

## Summary

**Strongest element.** Section 3, and the decision to build the paper on an instrument (the
stated-reason field) that converts a case-study question into a countable one. Reporting four
failed extensions of your own thesis, including two that would have made the paper more
quotable, is what makes the rest credible. Section 2.5 and Section 2.7 are the parts that would
change my behaviour tomorrow.

**Weakest element.** The chain from "251 halts labelled business/strategic" to "health systems
and capital markets cannot price this value shape." Three independent links fail: the effect is
carried entirely by industry sponsorship rather than modality; no sponsor statement in the
dataset names a payer, price or reimbursement decision; and the instrument cannot see the
completed-but-failed trials where scientific failure normally lands. The diagnostic half of the
thesis — that platforms which must change a clinical decision fail on evidence generation —
survives every check I ran, including sponsor stratification, and is the claim the paper should
lead with.
