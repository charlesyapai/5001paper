# Referee's pitch and assessment
**What this paper is, what it measured, what it found, who should read it, and what I would
change. Written from manuscript v7 with every quoted number recomputed from the supplementary
tables in the same session.**
Assessed 4 September 2026.

---
## 1. The pitch
### The pitch the paper currently makes
> Molecular precision medicine is described as a field waiting on biology. It is not what stops
> programs. Across 14,061 registered trials, sponsor-stated business decisions end far more
> programs than safety or efficacy failure, and the excess is concentrated almost entirely in
> industry-sponsored therapeutic programs. The binding constraint is the mismatch between how
> these technologies create value and how health systems and capital markets are built to pay
> for it.

### The pitch I would make instead
The thesis above is true, defensible in this dataset, and **not novel** — see §4. The novel
content is one cell of a two-by-two table and one exhaustive-search null:
> When a commercial sponsor carries a therapeutic program in molecular precision medicine, that
> program is abandoned for stated business reasons **66%** of the time it stops — against
> **26%**, **23%** and **22%** in the other three cells of the
> modality-by-sponsor table. Neither modality nor commercial sponsorship alone produces the
> effect; it requires both. And the registry that reveals this **cannot explain it**: across
> 784 halted trials, not one sponsor statement names a payer, a price, a
> reimbursement decision, a formulary or an HTA body.

That framing is stronger for three reasons. It leads with a measurement nobody has made rather
than a conclusion the field already holds. It is robust to every sensitivity the paper runs,
whereas the aggregate ratio is not (§3). And it makes the paper's most uncomfortable result — the
instrument's blindness to payment — into a contribution instead of a caveat.

---

## 2. The methodology
**The instrument.** ClinicalTrials.gov requires a sponsor to record a free-text reason when a
trial is terminated, withdrawn or suspended. The paper treats that field as a countable
instrument for a question normally answered by interview and case study. This is the paper's
real methodological contribution and it is genuinely underused in the literature.

**The pipeline, in five steps.**
1. **Scope.** 21 technology subfamilies across four families — gene editing and gene therapy,
   AI-driven drug discovery, proteomic and multi-omic diagnostics, precision-medicine
   infrastructure — with the exact registry and PubMed query for each row published as a column
   of the master table.
2. **Retrieval and de-contamination.** The registry's concept expansion badly contaminates
   phrase queries (a lentiviral query returns mostly HIV trials via a lentivirus→HIV concept
   link). Every returned record is re-filtered with a literal case-insensitive regex over title,
   summary, description, keywords and intervention names, reducing ~25,600 returned records to
   **14,061 retained**. This step is not optional and is the reason the counts differ from a
   naive query.
3. **Role flagging.** Trial phase belongs to the parent trial, not to a diagnostic assay, so an
   intervention-role flag marks records where the technology is named as the intervention or in
   the title. Diagnostics are staged only on that flagged subset, with separate maturity ladders
   for therapeutic and diagnostic modalities.
4. **Halt classification.** 673 distinct verbatim reason strings assigned to an 11-category
   schema by a language model under a fixed tool schema, instructed to prefer a scientific cause
   wherever the text states one, so the non-scientific buckets read as lower bounds.
   Administrative rollovers into follow-up studies are excluded as non-failures; 'no reason
   stated' is kept as a visible category. Deduplication to one row per registration gives the
   **784-trial analysis set**.
5. **Inference.** Two-by-two contingency comparisons by Fisher's exact test, stratified by
   modality and sponsor class, with two sensitivity analyses (exclusion of the dominant
   subfamily; collapse to one row per sponsor as a cluster-robust unit) and rank correlations for
   the platform-level tests.

**What the design cannot do, stated by the paper itself.** No financing data of any kind. The
reason field observes only 24.7% of concluded Phase 2+ trials, structurally excluding the
completed-but-failed trials where efficacy failure normally lands. The classification is
single-coder and machine-assigned with no inter-rater statistic. The post-approval evidence is
six hand-curated trade-press cases, not a registry query.

---

## 3. What it found
### The result that holds
Business-attributed discontinuation is not a field-wide property. It is an interaction:

| Share of halts citing a business decision | Industry-sponsored | Non-industry |
|---|---|---|
| **Therapeutic** | **66.0%** (95/144) | 23.4% (43/184) |
| **Diagnostic / analytic** | 25.9% (21/81) | 22.1% (83/375) |

Three cells sit within four percentage points of each other; the fourth is roughly two and a
half times higher. Modality among industry sponsors gives OR 5.54 (p = 6×10⁻⁹); among
non-industry sponsors OR 1.07 (p = 0.41). Sponsor class within therapeutics gives OR 6.36
(p = 5×10⁻¹⁵); within diagnostics 1.23 (p = 0.27). It survives dropping the dominant subfamily
(OR 4.60) and survives one-row-per-sponsor clustering (OR 6.10 versus 1.72).

![Figure 1](../figures/Figure_1_constraint_map.png)
*(bundle path: `figures/Figure_1_constraint_map.png`)*

**The mirror-image result.** Diagnostic programs fail on recruitment and feasibility rather
than on business decisions (OR 2.69, p < 0.001). So the two modalities fail in different ways:
a therapy must become a priced product and dies of the portfolio decision; a diagnostic must
change a clinical decision and dies of the evidence it never generated.

**The extreme case.** AAV gene transfer — the earliest therapeutic modality in scope to reach
pivotal trials, first trial 1999, first Phase 3 2003 — has 18 of 24 halted trials citing
business reasons and 1 citing safety or efficacy, the widest gap of any platform. It has **zero**
recruitment-cited halts against a 17.7% therapeutic base rate (exact binomial p = 0.009),
which is counterintuitive for the modality with the smallest addressable populations.

**Supporting structure.** Research momentum is uncorrelated with clinical maturity
(ρ = −0.08, p = 0.74): the newest-activity platforms are not the most deployable. Only
18.2% of 2,517 due interventional trials posted results and 20.2% of records
carry an unverified status, so the visible evidence base is far thinner than the trial counts
imply. Access is concentrated: several platforms are ~89% high-income-country-only.

### The four negative results, which are the best part of the paper
Each was tested because it would have strengthened the thesis. All four failed, and the paper
reports them:
1. **Maturity does not predict commercial failure** (ρ = 0.00, p = 1.00) — reported as a
   non-detection with its power limit stated, since the ten measurable platforms take only two
   distinct stage values.
2. **Precision is not measurably narrowing the addressable population** (trials-per-indication
   ρ = −0.38, p = 0.35; median enrollment ρ = −0.04, p = 0.93). Enrollment is uniformly small
   across every generation, medians 10–40. This *reframes* the thesis usefully: the small-market
   character is a constant property of the modality, not a worsening trajectory, which is why
   three decades of delivery maturation did not resolve it.
3. **An independent behavioural instrument contradicts the main measure.** Sponsor-exit rate
   against business-cited halt share: ρ = −0.50 (p = 0.14) across all ten platforms, and
   **ρ = −0.70 (p = 0.036)** under the paper's own ≥8-halted-trial inclusion rule. Therapeutic
   platforms cite business reasons more often but their sponsors leave *less* often.
4. **The aggregate ratio is uninformative about magnitude.** Across defensible category
   boundaries it spans **0.8 to 6.1** — 242:40 as categorised, 79:97 when the business
   category is restricted to strings explicitly naming a financial cause and manufacturing and
   regulatory holds are counted as technical. The range includes parity, so only the stratified
   contrast carries weight.

![Figure S4](../figures/Figure_S4_sponsor_exit.png)
*(bundle path: `figures/Figure_S4_sponsor_exit.png`)*

---

## 4. How relevant is this — and what is actually new
### The thesis is not novel
This is the most useful sentence I can give you. That commercial sponsors abandon gene-therapy
programs for portfolio rather than scientific reasons is the field's **consensus position** by
2026, after the sequence of withdrawals the paper itself catalogues. That durable one-time
therapies for small populations are mispriced by annual-budget payers has been in the
health-economics literature since roughly 2019. Assume your skeptical reader arrives already
agreeing with your conclusion and unimpressed by it. A paper whose contribution is the thesis
will be desk-rejected as a well-evidenced restatement.

### Five things that are new, in descending order of strength
1. **The two-way stratified measurement.** Nobody has cross-tabulated halt causes by modality
   and sponsor class at this n. The finding that the effect requires *both* — that commercial
   sponsorship alone does nothing to diagnostics, and therapeutic modality alone does little
   without a commercial sponsor — is a real result and changes what an intervention would have
   to target.
2. **A durable negative methodological result.** By exhaustive search of every verbatim string,
   the registry's stated-reason field **cannot see payment at all** — zero mentions of payer,
   price, reimbursement, coverage, formulary or HTA. Anyone planning to build an economic
   argument on that field needs to know this, and it generalises well beyond this therapeutic
   area.
3. **Publishing an instrument that disagrees with your own headline.** Constructing a
   behavioural test of your own self-reported measure, finding it significantly contradicts you,
   and reporting it at the threshold least favourable to yourself is rare enough to be a
   contribution to how registry work gets done.
4. **A countable operationalisation of diagnostic reimbursement-readiness.** Interventional
   trials in which the assay is named as the intervention — liquid biopsy at 278 (23 at Phase 3+)
   and reimbursed, against affinity proteomics at 1 and 0 with literature growing 35% a year. This is
   the single most actionable number in the paper and it is currently in §4.5, not the abstract.
5. **The artefact set.** 16 tables with every query string, every verbatim halt reason next to
   its assigned label, and 19 tests including seven negative ones. Reusable by others, which is
   itself a citable contribution.

### Where the relevance actually lands
**Prospectively, not retrospectively.** The retrospective claim (AAV died commercially) is
known. The forward claim is the one with teeth: prime editing, base editing and epigenome
editing have 2, 28 and 2 registered trials respectively and have never been asked to be paid
for. Nothing in the dataset suggests the architecture that ended the previous generation's
programs has changed. **Solving specificity while inheriting that architecture reproduces the
outcome at higher scientific cost.** That is the sentence a scientist choosing a direction
should read, and it is currently in the conclusion rather than the abstract.

---

## 5. Who would read this
### Primary — will read it and act on it
- **Translational scientists and platform leads in genetic medicine** deciding what to work on
  next. §4.5's per-platform lookup is built for exactly this reader; it is the part of the paper
  most likely to be screenshotted.
- **Diagnostics and biomarker groups.** The assay-as-intervention count reframes 'we need more
  cohort associations' into 'we need a trial in which our assay changes management' — a
  different and more expensive research programme.
- **Biotech investors and BD teams** in genetic medicine, for whom the interaction is directly
  operational: it says the portfolio decision, not the science, is the modal exit.

### Secondary — will cite it, may not act
- **Health-policy and HTA researchers** working on payment models for durable therapies. They
  will value the quantification and immediately note that the paper observes no payer decisions.
- **Meta-research and registry-methods researchers.** For this audience the negative
  methodological result is the paper, and the therapeutic area is the case study.
- **Funders and programme officers** allocating translational funding, for whom the
  evidence-visibility finding (a fifth of records unverified, a sixth of due trials reporting)
  is a governance problem in its own right.

### Who will push back hardest
- **Health economists**, on the grounds that a paper about payment observes no prices — which
  the paper concedes but the title still gestures at.
- **Clinical trialists**, on the grounds that a self-reported registry field is a weak
  instrument and the censoring is severe. §3.3 and §3.4 pre-empt this honestly; whether that
  rescues it is the reviewer's judgement call.
- **Anyone who has run a gene-therapy programme**, who will say they knew this already. §4 is
  your answer to them, and it needs to be in the abstract.

### Venue read
As framed, this is a **preprint plus a strong industry or policy analysis piece** — the natural
homes are a *Nature Biotechnology* analysis/feature, *Nature Reviews Drug Discovery*
commentary, or a health-policy outlet. Reframed around the instrument (§6, option B), it is
submittable to a meta-research or clinical-epidemiology journal, where the negative
methodological result and the disagreeing instrument are the contribution and the consensus
thesis becomes background. The second route is the shorter path to peer review.

---

## 6. Extensions and adjustments
### 6a. Two defects I found in v7 while writing this
Both are the class of error this project has agreed to treat as errors, and neither was in the
previous review.

**A superlative the paper's own caveat retracts.** Section heading 2.3 reads *"The most mature
modality is the most commercially fragile"*, and the Conclusion repeats it. Two sentences into
§2.3 the paper states the opposite: *"Four therapeutic platforms tie at the top stage of the
maturity ladder, so 'most mature' is not a property we can assign uniquely."* I verified it —
AI-originated candidates, AAV gene transfer, CRISPR nuclease editing and in vivo LNP all sit at
stage 5. The heading and conclusion assert what the body withdraws. **Fix:** retitle 2.3 to
*"The earliest modality to reach pivotal trials is the most commercially fragile"* — the property
the argument actually uses, and one AAV holds uniquely — and make the same substitution in the
Conclusion.

**A cross-reference that does not resolve.** The References section says the non-molecular
comparator *"has not been run (Section 8, item 5)"*. Section 8 item 5 is human validation of the
halt classification. **The comparator is not in Section 8 at all** — so the analysis both prior
referees called the single biggest hole is absent from the paper's own list of what would
strengthen it, and the one pointer to it lands on the wrong item. **Fix:** add it to Section 8
and repoint the reference.

### 6b. The one extension that changes the paper's standing
**Run the same halt-reason classification on a non-molecular comparator.** Everything in this
paper is a within-molecular-medicine comparison. A reader cannot currently tell whether a
66%-versus-22% split is remarkable or simply what ClinicalTrials.gov looks like when you
stratify any therapeutic area by sponsor class. Two candidate comparators are already partly in
hand: the 5,601 imaging-AI trials in this dataset, and a fresh pull of a mature small-molecule
area. If the interaction is specific to molecular precision medicine, that is a much stronger
paper. **If it is generic to industry-sponsored therapeutics, the paper becomes a study of how
commercial sponsors report stopping — still publishable, and honest, but a different paper.**
This is one registry query plus one classification run, and it is the first thing a referee will
ask for. It should be run before submission, not offered as future work.

### 6c. Methodology adjustments, ordered by cost-to-value
1. **Human-validate the classification** on a stratified sample of 150–200 strings with a
   reported kappa. This is the largest methodological gap and the cheapest to close. Every
   count in the paper currently rests on a single machine coder.
2. **Sponsor-level survival analysis.** First-to-last trial interval per sponsor is a better
   commitment signal than trial volume, and it would replace the sponsor-exit proxy that
   currently disagrees with the main measure. The required fields are already in the published
   trial table, so this is a rewrite of one analysis, not new data. It also addresses the leading
   explanation for the disagreement — that the exit measure is dominated by one-trial
   academic-adjacent sponsors.
3. **Model the interaction directly** rather than through stratified two-by-twos: a logistic
   regression with a modality×sponsor term, sponsor-clustered standard errors, and subfamily as
   a random effect. It would give one interaction estimate instead of six tables, absorb the
   clustering objection formally, and let you adjust for start year — which is currently
   unadjusted and is a live confounder, since business-attributed halting may simply be more
   common in recent years.
4. **Recover the censored arm.** Completed-but-failed later-phase trials are structurally
   invisible to the reason field. Linking to posted results for the ~18% that reported would let
   you count endpoint failures directly and put a bound on how much scientific failure the
   instrument misses — turning Limitation 3b from a caveat into a measurement.
5. **Non-US registries** (CTIS, ChiCTR, jRCT) to correct both the geography claims and the
   halt-rate estimates. Lower priority: it widens coverage but does not answer an objection.

### 6d. Narrative adjustments
**Option A — keep the thesis paper, fix its emphasis.** Four changes, all rewrites:
- Move the interaction table into the abstract's first two sentences and the aggregate ratio
  out of the abstract entirely. It spans parity; it cannot lead.
- Move the forward-looking claim — frontier editors inherit an unchanged payment architecture —
  from the Conclusion to the Introduction. It is the paper's reason to exist and currently
  appears on the last page.
- State in the Introduction that the thesis is the field's consensus and that the contribution
  is its measurement and stratification. Pre-empting 'we knew this' is stronger than being told.
- Promote the assay-as-intervention metric from §4.5 to a named result in §2. It is the most
  actionable output and it is buried in a table caption.

**Option B — reframe as a methods paper, which I think is the stronger route.** Title it
something like *"What clinical-trial registries can and cannot tell you about why programs
stop."* The contribution becomes: the stated-reason field is a usable instrument for
attributing discontinuation; it is structurally blind to payment (0 of 784); it is
censored with respect to scientific failure (observes 24.7% of concluded later-phase trials);
its category boundaries move a headline ratio from 0.8 to 6.1; and a behavioural instrument
built to validate it significantly disagrees. Molecular precision medicine is the case study,
and the interaction is the demonstration that the instrument can detect real structure.

Option B is more novel, fully defensible on the evidence in hand, has an obvious peer-reviewed
home, and needs no new data — only the comparator in §6b to be convincing. Its cost is that it
reaches the working scientist less directly than Option A. The two are not exclusive: B as the
paper, A as the accompanying commentary.

---

## 7. Overall
A careful study whose central measurement survives adversarial recomputation, whose negative
results are handled better than most published papers handle their positive ones, and whose
framing still claims more than its instrument can deliver. The gap between what it measured
(sponsors say they stopped for business reasons) and what it argues (payment architecture is the
binding constraint) is bridged by six trade-press cases and by the reader's prior agreement —
not by the registry. Say so in the Introduction and the paper gets stronger, not weaker.

**Two things to do before anyone else reads it:** the comparator run in §6b, and the two
defects in §6a.
