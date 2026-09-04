# Claim-by-claim review: what the paper asserts, and whether it holds
**An adversarial read by a fresh-context expert reader, with every checkable number recomputed
against the 16 supplementary tables. 39 consolidated claims in reading order.**
Reviewed against manuscript version `6097c53f-7f40-4688-a484-43d15b0435dd`. Review date: 3 September 2026.
---

## The verdict in one line
> A genuinely careful registry study whose central measurement holds up under adversarial recomputation, wrapped in a title, abstract and conclusion that assert a field-wide main effect the body spends three sections retracting - and whose one unreproducible number is the one bounding its headline ratio.
**Would a serious reader finish it?** yes with reservations
**Where it lands as-is.** As-is: preprint, or a strong policy/industry report - the artefact set alone (verbatim reasons + labels + per-row queries + a per-platform lookup) makes it worth citing. It is not submittable to a peer-reviewed journal today, for two reasons that are discipline rather than data: there is no reference list at all, while Sections 4.2 and 4.4 make dated quantitative claims about FDA/CDC/NIH staffing and NIH appropriations and Limitation 3c invokes a registry-wide termination literature - all uncited; and the central measure is a single-coder machine classification with no validation. To move up a tier: (1) add references; (2) fix the title, abstract and conclusion to state the interaction rather than a main effect; (3) make the 159 reproducible or drop it; (4) report the sponsor-exit result at the paper's own threshold and call it a disagreement; (5) hand-code 150-200 reason strings and report kappa; (6) split Figure 6 into withdrawals and constrained launches. Every one of those except (1) and (5) is a rewrite, not new data collection. With (7) - the matched non-molecular comparator the author already names as the first thing they would add - this becomes a serious health-policy or translational-medicine paper, because the comparator converts every bare rate into a reference-classed one.
---

## 1. What the paper actually stands on
Five claims in a chain. Each line says what happens to the rest if that link fails.
1. 1. Among 784 deduplicated halted trials, sponsor-stated funding/business/strategic causes (242) outnumber stated safety/efficacy failures (40). VERIFIED exactly, but the ratio spans 1.6-6.1 across defensible category boundaries and its floor rests on a count I could not reproduce. If this falls, the title and conclusion fall; claim 2 survives untouched because it is a within-halted contrast.
2. 2. That excess is confined to one cell of the modality-by-sponsor table: industry therapeutics 66% (95/144) vs 22-26% elsewhere; the pooled modality effect is a composition artefact. VERIFIED exactly, and it survives excluding CAR-T (OR 4.60/6.12) and survives collapsing to one row per sponsor (OR 6.10 vs 1.72). This is the paper's spine and it holds. If it fell, everything would fall.
3. 3. Therefore the binding constraint is the commercial sponsor's portfolio decision, not therapeutic biology. This is an inference from a self-reported label to a behaviour, and the paper's own independent behavioural instrument disagrees - significantly so (p = 0.036) once the paper's own platform-inclusion threshold is applied. If this falls, the paper is a description of registry disclosure language, not of what stops programs.
4. 4. The portfolio decision is a payment decision, evidenced by post-approval withdrawals over reimbursement. Rests on 3 dated withdrawals (not 6 - two rows are constrained launches, one is a returned-rights event) from trade press, plus one claim misattributed to the paper's own case table. If this falls, the payment mechanism goes and the paper becomes descriptive.
5. 5. Therefore the frontier editors (base, prime, epigenome) will inherit an unchanged payment architecture at smaller population scale. This is an extrapolation the paper labels a prediction; it stands or falls entirely with 3 and 4.

**The weakest link.** The inference in step 3-4, from a self-reported registry label to a payment mechanism. Two things break it and both are the author's own evidence. First, the sponsor-exit instrument: reproduced at rho = -0.50, p = 0.14 only because Section 3.3 silently includes in vivo LNP, whose business share rests on 4 halted trials - below the 8-halt threshold used in Figure 1b and the 5-halt threshold in Section 4.5. Apply the paper's own rule and it is rho = -0.70, p = 0.036: not a failure to detect but a detected disagreement. Second, the payment mechanism rests on 3 usable trade-press rows, one of which ('rollout slower than expected', sourced to a stock newsletter) is not a retreat, and the manuscript points the reader to a bluebird bio row in its case table that does not exist. Section 3.3's own sentence - 'Section 2.1 should be read as a finding about how sponsors describe stopping' - is the correct verdict, and it is buried on page 12 while the title says the opposite.
---

## 2. The eleven things a reader will not forgive
In descending order of damage. Items 1–8 are corrections, not new analyses.
1. The title. Business decisions are 30.9% of halts against recruitment's 28.7% - a 2.2 pp gap, one-sided binomial p = 0.23 - and the paper's own Section 2.2 says recruitment leads in three of four families. 'Dominated by' is false as a statement about halts and is true only in the narrow pairwise comparison against safety and efficacy. A reader who checks this in ninety seconds discounts everything after it.
2. The title-page-versus-Limitation-3b contradiction, repeated in the Conclusion. '784 halted programs' and 'programs stop for money roughly six times as often' are both forbidden by the paper's own Limitation 3b ('Every ratio in this paper describes halted trials, not programs') and by Section 2.1's refusal to collapse the 1.6-6.1 range. Being contradicted by your own limitations section is worse than having the limitation.
3. The '242 to 159' restriction, which I could not reproduce from any transparent term list. A strict money-word read gives 75-79; adding business/strategic/portfolio gives 139; a wide list including 'sponsor' gives 194. Under the strict read the paper's stated floor of 1.6 becomes 0.8 - i.e. scientific causes would outnumber named-financial ones. This is the only headline number that fails the paper's own promise that every number traces to a published column, and it is the number bounding the central claim.
4. Pointing the reader at a supplementary row that does not exist. Section 2.6 says the bluebird bio private-equity sale 'is listed in the case table with its source'; commercial_retreat_cases.csv has six rows and none of them is that event. One broken pointer costs more than the sentence is worth in a paper whose credibility strategy is auditability.
5. Understating the paper's own disconfirmation. Section 3.3's null is threshold-dependent: at the paper's own >=8-halt inclusion rule the sponsor-exit correlation is rho = -0.70, p = 0.036 in the wrong direction. A referee who reconstructs it from the two published tables will conclude the softening was convenient, which is far more damaging than the disagreement itself.
6. Asserting the opposite of your own data. Section 2.7's 'null and terminated trials are the least likely to be written up' is contradicted by the author's own due-trial table: halted trials post at 23.5% versus 17.4% for non-halted. It is an uncited import from the reporting-bias literature dropped into the one section about evidence visibility.
7. The falsification test in 3.4 failing on the paper's own numbers. It predicts elevation 'among industry-sponsored programs of any modality'; industry diagnostics sit at 25.9%, indistinguishable from the non-industry cells. The section written to pre-empt unfalsifiability states a criterion the data refute and then reports it as passed.
8. Zero citations. A paper that states ~20,000 federal staff reductions, a $27.5bn NIH figure, 'industry commentary in early 2026' and a 'registry-wide termination' literature without a single source cannot be reviewed, let alone believed, on those points - and they are the points a policy reader will test first because they are the ones they already know.
9. Small superlatives that fail a ten-second table check: 'largest increase among gene-transfer platforms, though not the largest in the dataset (AI probe 12.5-fold)' omits spatial omics at 9.0-fold and base editing's 0-to-21; the abstract's '23-26%' floor is 22.1%; '2.4 to 1' is 2.49. Individually trivial, collectively they tell a reader the numbers were not checked against the full table.
10. Two Phase 3+ definitions for one platform. Pharmacogenomics is 232 in Section 2.5 and Figure S3 and 107 in the Section 4.5 table, unexplained, because the lookup's Ph3+ column silently mixes raw counts for therapeutics with assay-guided counts for diagnostics - and the 4.5 caption defines every column except that one. It undermines the paper's most reusable artefact.
11. The CAR-T/LNP staging inversion sitting unremarked in the actionable table: the most-registered therapeutic platform in the dataset (2,579 trials, 54 Phase 3+) is scored stage 4 while a platform with 68 trials is stage 5, because CAR-T's industry share is 29.4% against a 30% threshold. Limitation 6 covers the principle; the reader needs the footnote at the table.

---

## 3. What is genuinely new here — and what is not
**1.** The interaction itself, as a measurement. That business-attributed halting is confined to industry-sponsored therapeutics (66% vs 22-26%, OR 5.5-6.4) rather than being a property of therapeutic modality is not something a well-read person already believes, because nobody has stratified this field's halt reasons two ways at n = 784. It survives every check I ran: excluding CAR-T (OR 4.60/6.12), and collapsing to one row per sponsor (OR 6.10 among industry vs 1.72 among non-industry). This is the paper's real contribution and it is currently the third thing the abstract says.
**2.** Establishing, by exhaustive search of 784 verbatim strings, that the registry's stated-reason field cannot see payment at all - zero mentions of payer, price, reimbursement, coverage, formulary or HTA under a term list broader than the paper's. That is a durable negative methodological result about a widely used field, useful to anyone who was about to build an economic argument on it, and I have not seen it published.
**3.** The published disagreement between a self-reported measure and a behavioural instrument built to test it. Constructing an instrument that could refute your own headline, finding that it does, and reporting it in the abstract is rare enough that it is itself a contribution to how registry work gets done - and it is stronger evidence than the author thinks (p = 0.036 under their own inclusion rule, not p = 0.14).
**4.** A countable operationalisation of diagnostic reimbursement-readiness: trials in which the assay is named as the intervention, at Phase 3+. Liquid biopsy at 278/23 against affinity proteomics at 1/0, with affinity proteomics' literature growing 35% a year, converts 'generate decision-change evidence' from advice into a number a group can put on a slide and aim at. This is the single most actionable thing in the paper.
**5.** The reusable artefact set. 673 verbatim reason strings next to their labels, per-row registry and PubMed queries, a published per-trial due flag, and a per-platform lookup. It is what let me audit the business category independently and reconstruct the exit correlation, and it will outlive the paper's argument. Arguably the most valuable output here.
**6.** Honestly: the thesis is not novel. That companies abandon gene-therapy programs for portfolio rather than scientific reasons is the field's consensus position in 2026 after Pfizer, bluebird and BioMarin; that durable one-time therapies for small populations are mispriced by annual-budget payers has been argued in the health-economics literature since roughly 2019 (installment and annuity models, outcomes-based agreements); that delivery matured before precision, that activity volume is not readiness, and that polygenic scores are built in unrepresentative cohorts are all things this readership already believes. The author should assume a skeptical reader arrives already agreeing with the conclusion and unimpressed by it. What is new is the stratified measurement, the negative results, and the artefacts - so the paper should lead with the interaction and the instrument disagreement, not with the six-to-one ratio, which is both the least novel and the least robust thing in it.

---

## 4. What the existing data could still supply
Eleven additions, none requiring a new data source except #10.
1. The CAR-T-excluded test of the headline interaction. Limitation 3 names it as 'the appropriate check' but thesis_tests.csv contains it only for the superseded pooled comparison. I ran it: modality among industry sponsors OR 4.60 (p = 7e-5), sponsor class within therapeutics OR 6.12 (p = 5e-5), modality among non-industry OR 0.93 (p = 0.64). It is a clean strengthening result the paper claims to have and does not report.
2. The sponsor-collapsed (cluster-robust) analysis, also named in Limitation 3 and never run. Collapsing to one row per sponsor per cell: industry OR 6.10 (p = 1.1e-7), non-industry OR 1.72 (p = 0.029). Report it - it costs you the 'no modality effect at all' phrasing but it is the unit of analysis your own mechanism implies, and the interaction survives. Also report the sponsor concentration, which is in your favour: 88 distinct sponsors across the 144-trial cell, top sponsor 6.2%, top five 17.4%, so clustering is a milder threat than the limitation implies.
3. The sponsor-exit correlation restricted to platforms with >=8 halted trials - the paper's own Figure 1b threshold: rho = -0.70, p = 0.036, n = 9. And a sponsor-weighted version, since the unweighted Spearman lets AI/ML with 355 industry sponsors count the same as in vivo LNP with 13.
4. The strict Phase 2+ censoring figure. 'Phase 2+' currently includes PHASE1|PHASE2 records on the non-deduplicated basis; strict and deduplicated it is 418 completed vs 138 halted, so the field observes 24.8%, not 30.6%. Report both - the correction makes your own limitation stronger.
5. The binomial test behind the AAV recruitment claim, which the paper asserts and does not compute: 0 recruitment-cited halts of 24 against a 17.7% therapeutic base rate is p = 0.009. This turns 'contradicted' from rhetoric into a result, and it is a genuinely counterintuitive fact about the ultra-rare modality par excellence.
6. A names_financial_cause boolean column in halted_trials_blockers.csv, with the term list published, so the 159 and the 4.0/1.6 ratio endpoints become reproducible. As it stands they are the only headline numbers that fail the paper's own traceability promise.
7. Sponsor-level survival analysis, which Section 8 already identifies and which needs no new data: first-to-last trial interval per sponsor, from the published trial table. It is a strictly better commitment signal than the binary 2022 cutoff, and it directly addresses the leading candidate explanation the paper offers for its own null - one-trial sponsors who never returned. Restricting the exit measure to sponsors with two or more trials would test that in one cell.
8. A hand audit of the two subfamilies whose counts look contaminated. N-of-1 individualized genetic therapy is credited with 31 raw Phase 3+ trials and a same-year clinic-to-Phase-3 transit, which is not credible for that modality and both inflates the 4.5 table and threatens the 'fastest transit' superlative in Section 2.4. The 5,601 AI/ML count deserves the same treatment.
9. A denominator for Figure 6. All FDA- and EMA-approved cell and gene therapies is a list of a few dozen products; adding launch date, list price and withdrawal status converts six anecdotes into a rate, and the paper already names this as strengthening step 2. Until then the abstract should say three dated withdrawals, not six cases.
10. The matched non-molecular comparator (Limitation 3c). Classifying a few hundred reason strings from a phase- and year-matched sample of non-molecular trials would convert every bare rate in the paper from unanchored to reference-classed. It is the highest-value single addition available and the author has already identified it.
11. A count of how many of the 242 business-category strings explicitly deny a safety cause. The paper's upper-bound caveat is correct and currently rhetorical; the number is one regex away and would make Limitation 2 quantitative.

---

## 5. The claim ledger, in reading order
`solid` = defensible as written · `caveat` = defensible if the stated caveat travels with it ·
`reword` = the evidence supports a narrower claim · `new evidence` = needs an analysis not yet run ·
`NOT DEFENSIBLE` = contradicted by the paper's own data or unreproducible.

### Title
**C1 — reword** · *this is why they are reading*
> Program halts in molecular precision medicine are dominated by sponsor-attributed business decisions, not scientific failure.
- **Rests on:** I recomputed the category distribution over halted_trials_dedup.csv: business 242/784 = 30.9%, recruitment 225/784 = 28.7%. The gap is 2.2 pp (one-sided binomial p = 0.23 for business > recruitment). Business 'dominates' only in the narrow pairwise comparison against safety+efficacy (40), which the subtitle clause does state. The evidence cannot bear 'dominated' as a reader will parse it.
- **A reader objects:** Two objections, both fatal on a first read. (1) Business decisions are the largest of eleven categories by two percentage points over recruitment, and the paper's own Section 2.2 concedes recruitment leads in three of four families - so 'dominated' is false as a statement about halts. (2) The paper's actual result is an interaction confined to 144 of 784 trials (18.4% of the halted set); a title asserting a field-wide main effect is precisely the backslide Section 2.1 warns against.
- **Fix:** Retitle to the interaction: 'Business-attributed discontinuation in molecular precision medicine concentrates in industry-sponsored therapeutic programs: a registry analysis of 784 halted trials'. Drop 'dominated'. If you keep a contrastive title, it must be 'more often than scientific failure', not 'dominated by'.

### Subtitle
**C2 — reword** · *useful*
> The analysis covers 14,061 clinical trials and 784 halted programs.
- **Rests on:** Verified: 14,061 rows across 13,486 unique registrations in trial_records.csv; 784 rows in halted_trials_dedup.csv. But the 784 are trial registrations, not programs - and Limitation 3b says so in the paper's own words ('Every ratio in this paper describes halted trials, not programs').
- **A reader objects:** The title page contradicts Limitation 3b. A referee who notices this on page 1 will read the rest looking for more of it.
- **Fix:** Change 'halted programs' to 'halted trial registrations'. Do the same in the Conclusion ('programs stop for money'), which has the identical error.

### Abstract
**C3 — solid** · *this is why they are reading*
> Funding, business and strategic decisions are cited in 242 of 784 halted trials against 40 citing safety or efficacy failure.
- **Rests on:** Exact. I reproduced 242 business and 15 safety + 25 efficacy = 40 from halted_trials_dedup.csv. The 784 set, the 34 rollover exclusions and the 33 deduplications all reconcile (851 - 34 = 817 - 33 = 784).
- **A reader objects:** Only that a count of halted trials is not a count of programs, which the paper concedes elsewhere.
**C4 — caveat** · *this is why they are reading*
> Business discontinuation concentrates almost entirely in one cell - industry-sponsored therapeutics at 66% (95/144) - against 23-26% in the other three cells.
- **Rests on:** Reproduced exactly: 95/144 = 66.0%, 43/184 = 23.4%, 21/81 = 25.9%, 83/375 = 22.1%. The four Fisher tests reproduce to three significant figures (OR 5.54 p = 5.7e-9; 6.36 p = 5.2e-15; 1.07 p = 0.41; 1.23 p = 0.27). This is the paper's strongest number and it holds. The 'three cells within four percentage points' statement also verifies (spread 3.8 pp), and Figure 1a renders the table correctly and legibly.
- **A reader objects:** The stated floor is wrong: the lowest cell is 22.1%, not 23%. Trivial, but it is the abstract of a paper that promises every number traces to a column. Second, 'almost entirely' overstates - the cell holds 95 of 242 business halts (39%), not almost all of them.
- **Fix:** Write '22-26%'. Replace 'almost entirely in one cell' with 'is confined to one cell': the concentration claim is about the rate, not about where the business halts live. Add the sentence '39% of all business-cited halts occur in this cell, which holds 18% of the halted set.'
**C5 — new evidence** · *this is why they are reading*
> Neither modality nor sponsor class alone predicts business discontinuation; the effect exists only where both are present.
- **Rests on:** The two null cells are real at trial level. But I collapsed the data to one row per sponsor per cell (the unit the paper's own portfolio-decision mechanism implies) and the non-industry modality effect appears: OR 1.72, p = 0.029 (33/82 therapeutic vs 66/235 diagnostic). The interaction survives strongly (industry OR 6.10 vs non-industry OR 1.72) but the strict null does not.
- **A reader objects:** The claim 'no modality effect at all' is an artefact of counting trials rather than sponsors. A referee running the obvious cluster fix - which Limitation 3(ii) admits was never run - finds a significant modality effect among non-industry sponsors. The paper's cleanest rhetorical move is the one most sensitive to unit of analysis.
- **Fix:** Run the sponsor-collapsed analysis and report both bases in Section 2.1. Reframe from 'absent among non-industry sponsors' to 'three to six times larger among industry sponsors'. The interaction is what you need and it holds on both bases; the absolute null is not worth defending and you will lose it in review.
**C6 — reword** · *useful*
> AAV gene transfer, the earliest therapeutic modality to reach pivotal trials, has 18 of 25 halted trials citing business and 2 citing science, with 32 Phase 3 or later programs since 2003.
- **Rests on:** 18/25 and 2 verify on the 817 pre-deduplication basis. On the 784 basis used for the abstract's own headline table the same platform is 18/24 with 1 science halt. The '32 Phase 3 or later' is n_ph3plus from the master table - raw trial count, not programs; the assay-flagged equivalent is 14, and there are 24 distinct Phase 3+ sponsors.
- **A reader objects:** The abstract mixes two analysis bases in adjacent sentences without flagging it - a reader checking AAV in halted_trials_dedup.csv finds 24 and 1, not 25 and 2. And '32 programs' is 32 trials, which Limitation 6 concedes.
- **Fix:** Use the 784 basis throughout the abstract (18/24, 1 science) and say '32 Phase 3 or later trials'. Keep 25/2 in Section 2.3 where the 817 basis is declared.

### Abstract / 1. Introduction
**C7 — solid** · *useful*
> Only 9 of 5,601 AI/ML trials (0.2%) address molecular or drug discovery, against 46% for imaging and pathology.
- **Rests on:** Exact from ai_trials_by_application.csv: 2,581/5,601 = 46.1% imaging/pathology; 9 = 0.2% molecular/drug discovery.
- **A reader objects:** That 5,601 is a keyword-reference count, not a count of AI-driven trials, so the denominator mixes trials where AI is the intervention with trials that mention it in passing. The ratio is probably robust to that, and the figure is labelled as an attention measure.
- **Fix:** Say 'trials referencing AI/ML in the protocol' rather than 'AI trials' at first mention, as Figure S1 already does.

### 1. Introduction
**C8 — caveat** · *this is why they are reading*
> The binding constraint in molecular precision medicine is no longer whether the biology works, but that these technologies create value in a shape that neither health-system budgets nor capital markets are built to price.
- **Rests on:** This is the paper's thesis. Nothing in the registry measures budgets or capital markets: zero of 784 verbatim reasons name a payer, price, reimbursement, coverage, formulary or HTA term - I re-ran the search with a wider term list than the paper's and confirmed zero. The pricing half rests entirely on six curated trade-press rows (Section 2.6).
- **A reader objects:** A hostile reader objects that the thesis names a mechanism (pricing) the data cannot see, and that 'capital markets are not built to price it' is an economic claim made without a single financing observation - which the paper itself concedes two paragraphs later.
- **Fix:** Split the thesis into the two claims you actually have: (a) among halted trials, commercial sponsors' portfolio decisions dominate stated causes in therapeutics - measured; (b) the mechanism is a payment mismatch - argued from six post-approval cases. You already do this in Section 4.1; do it in the Introduction too, where the reader forms their prior.

### 2.1
**C9 — solid** · *useful*
> The pooled therapeutic-versus-diagnostic comparison (42.1% vs 22.8%, OR 2.46) is a composition artefact of the interaction and should not be read as a modality mechanism.
- **Rests on:** Reproduced exactly (138/328 vs 104/456, OR 2.458, p = 7.4e-9). Explicitly demoting your own previously headline result is the right call and rare.
**C10 — solid** · *this is why they are reading*
> Not one of the 784 verbatim reason strings mentions a payer, price, reimbursement decision, coverage, formulary or health technology assessment.
- **Rests on:** I re-ran this independently with a broader pattern (adding copay, CMS, NICE, tariff, cost-effectiveness, willingness-to-pay) and confirmed zero hits. The paper is right, and stating it in the results rather than the limitations is the single most credible thing in the manuscript.
**C11 — **NOT DEFENSIBLE**** · *this is why they are reading*
> Restricting the business category to strings that name any financial cause reduces it from 242 to 159, giving a ratio of 4.0 to 1 (and 1.6 to 1 with the manufacturing adjustment).
- **Rests on:** I could not reproduce 159 from any transparent term list. A strict money-word list (fund, financ, budget, cost, capital, invest, econom, resourc) gives 75-79 of 242. Adding business/commercial/strategic/portfolio/prioritisation gives 139. A wide list including 'sponsor' gives 194. 159 sits between two lists neither of which is 'names a financial cause'. Under the strict reading the restricted ratio is 1.9, and with the manufacturing/regulatory adjustment it is 0.8 - i.e. scientific causes would outnumber named-financial ones.
- **A reader objects:** This is the one number I could not verify, and it bounds the paper's central quantitative claim. A referee who tries the obvious reconstruction gets a lower bound of ~0.8-2.0 rather than 1.6, which crosses the point where the headline direction survives. The paper promises on its title page that every number traces to a published column; this one does not.
- **Fix:** Publish the term list as a column in halted_trials_blockers.csv (a boolean names_financial_cause), or drop the 159 and report the range as computed from published columns only. If the strict figure really is 75-79, say so - the honest range becomes 0.8 to 6.1, and the correct conclusion is that the ratio is not the result; the interaction is. Also fix 242/97 = 2.49, printed as '2.4'.

### 2.1 / 5 (3b)
**C12 — reword** · *this is why they are reading*
> The reason field observes only 30.6% of concluded Phase 2+ trials (534 completed vs 235 halted), structurally excluding completed-but-failed trials.
- **Rests on:** The arithmetic reproduces only if 'Phase 2+' includes PHASE1|PHASE2 records and is computed on the non-deduplicated 14,061-row basis. On a strict Phase 2+ definition (PHASE2, PHASE2|PHASE3, PHASE3, PHASE4) the counts are 418 completed and 138 halted - the field observes 24.8%, not 30.6%. On the deduplicated unique-registration basis it is 24.7%.
- **A reader objects:** The number is mislabelled twice - Phase 1/2 trials counted as 'Phase 2+', and the row basis used where the rest of Section 2.1 uses the deduplicated basis. It happens to cut against the paper: the true censoring is worse than stated.
- **Fix:** Report 24.8% on a strict, deduplicated Phase 2+ basis, and keep 30.6% only as a sensitivity ('30.6% if Phase 1/2 combined designs are included'). This strengthens the limitation, so there is no cost to fixing it.

### 2.1
**C13 — caveat** · *this is why they are reading*
> The business:science ratio ranges from 1.6 to 6.1 across defensible category boundaries; the direction is robust, the magnitude is not.
- **Rests on:** The 6.1 endpoint reproduces (242/40 = 6.05) and the manufacturing-adjusted 2.49 nearly does. The 1.6 floor depends on the unreproducible 159. Reporting a range instead of a point estimate is the correct instinct, and the paper's admission that the manufacturing assignment contradicts Section 4.5 is the kind of self-audit that buys credibility. The accompanying caveat - that sponsors have a disclosure incentive to call a stop strategic, so business is an upper bound and science a lower bound - is supported by the verbatim strings, several of which volunteer 'not due to safety concerns'.
- **A reader objects:** The floor is unverifiable (see C12), and the Conclusion then quotes the ceiling as if it were the estimate.
- **Fix:** Keep the range; make the floor reproducible; and enforce the range in the Conclusion and abstract - the paper cannot report a range in Section 2.1 and 'roughly six times' in Section 6. Also count how many of the 242 strings explicitly deny a safety cause; that turns the upper-bound caveat from rhetoric into a number.

### 2.2
**C14 — solid** · *this is why they are reading*
> Funding and business decisions outnumber safety and efficacy failures in all four registry-derived families, but recruitment is the single largest blocker in three of the four.
- **Rests on:** Both halves verified exactly on the 817 basis: business > science in all four (141/27, 41/6, 32/6, 37/4) and recruitment leads in proteomics 77/182, precision medicine 51/156, clinical AI 48/139. The basis switch to 817 is declared in the text. The adjacent claim that AAV's zero recruitment-cited halts contradict the small-market intuition also checks out and is stronger than stated: 0 of 24 against a 17.7% therapeutic base rate is binomial p = 0.009, a test the paper asserts but does not run.
- **A reader objects:** The second half of this sentence contradicts the paper's title, and the paper does not acknowledge the tension. That is a self-inflicted wound: the honest reading is in the body and the overreach is on the cover.
- **Fix:** Keep the sentence exactly as it is and fix the title (C1) to match it. And add the binomial to the AAV recruitment sentence ('zero of 24, against 4.2 expected, p = 0.009') so 'contradicted' is earned rather than asserted.

### 2.3
**C15 — solid** · *this is why they are reading*
> AAV gene transfer is the earliest therapeutic modality in scope to reach the clinic and pivotal trials, and 18 of its 25 halted trials cite business against 2 citing science.
- **Rests on:** All components verified against the master table: 316 trials, first trial 1999, first Phase 3 2003, 67.4% industry, and the 18/25/2 split on the declared 817 basis. The parenthetical conceding that 'most mature' cannot be uniquely assigned (four platforms tie at stage 5) is exactly the right correction and is honestly made.
- **A reader objects:** The section heading still says 'The most mature modality is the most commercially fragile' while the body retracts 'most mature'. A reader scanning headings gets the retracted claim.
- **Fix:** Retitle the section 'The earliest modality to reach pivotal trials is the most commercially fragile' so the heading and the body agree.
**C16 — solid** · *useful*
> CAR-T reproduces the pattern at scale (104 business vs 20 scientific across 251 halts) and CRISPR nuclease editing sits at 10 versus 1.
- **Rests on:** Exact on the 817 basis (CAR-T 251 halts, 104/20; CRISPR 21 halts, 10/1). Mass-spec and pharmacogenomics both at 17.9% also verify.
- **A reader objects:** CAR-T alone is 30% of the halted set, and Limitation 3 says the CAR-T-excluded sensitivity analysis is 'the appropriate check' - but the only such test in thesis_tests.csv is on the pooled comparison the paper has since superseded. I ran it on the interaction: it survives (modality among industry OR 4.60, p = 7e-5; sponsor class within therapeutics OR 6.12, p = 5e-5; non-industry modality OR 0.93, p = 0.64).
- **Fix:** Report the CAR-T-excluded interaction. It is a clean strengthening result the paper currently claims to have and does not.

### 2.4
**C17 — caveat** · *useful*
> Delivery matured roughly a decade before precision: AAV entered the clinic in 1999 and Phase 3 in 2003, while CRISPR entered in 2016 and reached Phase 3 in 2018 - a two-year transit, the fastest among the gene-transfer modalities and tied with in vivo LNP.
- **Rests on:** All milestone years verified from the master table. The two-year transit and the LNP tie (2011 to 2013) are correct among AAV (4), lentiviral (4) and CAR-T (6). But N-of-1 individualized genetic therapy shows first interventional 2000 and first Phase 3 2000 - a zero-year transit - and is a therapeutic gene-directed modality.
- **A reader objects:** The 'fastest' superlative depends on excluding N-of-1, which the sentence does not do explicitly. Separately, N-of-1 being credited with 31 raw Phase 3+ trials and a same-year Phase 3 is itself a signal of query contamination that a referee will read as a taxonomy problem, not a finding.
- **Fix:** Say 'fastest among the vector-based gene-transfer modalities (AAV, lentiviral, CAR-T, LNP, CRISPR)' and name the exclusion. Separately, audit the N-of-1 Phase 3+ trials by hand - 31 is not credible for that modality and it also inflates the 4.5 table.

### 2.4 / 3.5
**C18 — solid** · *this is why they are reading*
> For base, prime and epigenome editing the binding constraint is still biology, and no payer has yet been asked to buy anything.
- **Rests on:** Verified: base editing 28 trials and no Phase 3, prime editing 2 trials from 2024, epigenome editing 2 with first interventional 2025. The scope limit is correctly drawn and is the paper's most defensible piece of self-restraint.
- **A reader objects:** Minor: the master table gives epigenome editing first_year 2020 and first interventional 2025; 'first registered in 2025' should specify interventional.
- **Fix:** Add 'first interventional trial registered in 2025'.

### 2.5
**C19 — solid** · *useful*
> Newness of activity carries no information about clinical maturity: rho = -0.08 (p = 0.74) across 21 subfamilies.
- **Rests on:** Reproduced exactly (-0.077, p = 0.740). Excluding the AI-originated-candidate probe row - which is a curated 33-molecule probe, not a registry query, yet is staged on the same five-step ladder - gives rho = -0.19, p = 0.43. The conclusion is robust to that choice.
- **A reader objects:** A referee will ask why a hand-curated probe is included in a correlation over registry-derived subfamilies. The answer is that it does not matter, but the paper should say so.
- **Fix:** Add 'excluding the AI-candidate probe, rho = -0.19, p = 0.43' in a parenthesis.

### 2.5 / 4.5
**C20 — reword** · *useful*
> Pharmacogenomics has 232 Phase 3 or later trials and the lowest momentum in the dataset (16.8% since 2021).
- **Rests on:** 16.8% verified. But 232 is the raw n_ph3plus, while the Section 4.5 lookup table gives pharmacogenomics Ph3+ = 107, and Figure S3's caption repeats 232. The Ph3+ column in platform_lookup.csv mixes definitions: raw counts for therapeutic platforms (AAV 32, CAR-T 54, N-of-1 31) and assay-guided counts for diagnostics (pharmacogenomics 107, liquid biopsy 23, mass-spec 11).
- **A reader objects:** The same platform carries two different Phase 3+ counts in three places with no explanation, and the 4.5 caption defines every column except that one. A reader cross-checking the table against the text finds a 232-versus-107 contradiction and stops trusting the lookup - which is the paper's most useful artefact.
- **Fix:** Define Ph3+ in the 4.5 caption ('assay-guided Phase 3+ for diagnostic platforms, all Phase 3+ trials for therapeutic platforms'), and use 107 in Section 2.5 and Figure S3 with the raw count in parentheses. Better: publish both columns and label them.

### 2.6
**C21 — caveat** · *this is why they are reading*
> Post-approval, gene therapies have been withdrawn from markets over reimbursement rather than safety - the only direct evidence of the payment mechanism in this study.
- **Rests on:** Six rows in commercial_retreat_cases.csv. Three are dated market withdrawals (Zynteglo, Skysona, Beqvez), one is a returned-rights event with no approval (giroctocogene), and two are neither: Roctavian ('access limited to 3 reimbursed markets', sourced to an analyst comment) and Hemgenix ('rollout slower than expected', sourced to a stock newsletter). The evidence that actually carries the mechanism is n = 3, possibly 4.
- **A reader objects:** Figure 6 is titled 'Commercial retreats' and its subtitle asserts the therapies 'have left markets', but Hemgenix has not left any market and Roctavian is restricted, not withdrawn. Two of six rows are not the phenomenon, and they are the two with the weakest sources. A journal referee will reject an analyst comment and a stock newsletter as the evidentiary base for the paper's central mechanism. Separately, the Figure 6 subtitle asserts as fact ('treated no commercial patient in 10 months') what the text hedges as reporting, on the paper's most quotable data point.
- **Fix:** Split Figure 6 into 'market withdrawals' (n = 3, dated, with intervals) and 'constrained launches' (n = 2-3) with different markers and a caption that says the mechanism claim rests on the first group. Retitle to 'Post-approval commercial withdrawal and constrained launch'. Then say n = 3 in the abstract, not six. And make the figure annotations match the text's hedging on Beqvez ('no commercial patients reported') and on Skysona's '3 months in the EU', which compresses approval-to-announced-exit into a duration claim.
**C22 — **NOT DEFENSIBLE**** · *useful*
> bluebird bio, holder of three FDA-approved gene therapies, was sold to private equity for a fraction of its depressed market value; it is listed in the case table with its source but not plotted in Figure 6.
- **Rests on:** False as to the table. commercial_retreat_cases.csv contains exactly six rows - Zynteglo, Skysona, Beqvez, giroctocogene, Roctavian, Hemgenix - and no bluebird corporate event. The claim has no source anywhere in the published materials.
- **A reader objects:** The paper tells the reader where to verify a claim and the claim is not there. For a reader who has been promised that every number traces to a published column, one failed pointer is worth more damage than the claim is worth.
- **Fix:** Either add the row to the case table with its source and retrieval date, or delete the sentence. Then re-audit every other 'it is in the supplementary table' pointer in the manuscript - this one was wrong.

### 2.7
**C23 — solid** · *useful*
> Two forms of attrition are invisible in a trial count: 2,821 records (20.1%) are status-unknown and only 18.2% of 2,517 due interventional trials have posted results; with 71.2% of gene-therapy trials single-arm at median enrollment 20, the evidence base is far thinner than the activity implies.
- **Rests on:** All verified: 2,821/14,061 = 20.1% with family range 18.05-21.80%; (2,821 + 817)/14,061 = 25.9% with the sets disjoint by status; 2,517 due trials with 458 posted = 18.2%, and all four family rates to one decimal (infrastructure 31.5, gene editing 15.3, proteomics 11.1, clinical AI 10.6); single-arm 0.7118 vs 0.2855 for clinical AI, median enrollment 20. Publishing the per-trial `due` flag so the denominator is checkable is the right call and I used it.
- **A reader objects:** One internal inconsistency: the text says infrastructure is 'best at 31.5%' (unique-registration basis) while evidence_quality_by_family.csv, the source for Figure 7, gives 30.95% (row basis) - so Figure 7 and the text disagree. And a hostile reader notes single-arm design is the regulatory norm for ultra-rare indications, so calling it a 'weak foundation' is a value judgment presented as a finding.
- **Fix:** Recompute Figure 7's table on the unique basis so it matches the text, or quote 31.0%. Add one clause naming the counter-position on design: single-arm trials are accepted by regulators for ultra-rare indications, but they leave HTA bodies without a comparator - which is the decision Section 2.6 shows is binding.
**C24 — **NOT DEFENSIBLE**** · *useful*
> The missing fraction is not random: null and terminated trials are the least likely to be written up.
- **Rests on:** Contradicted by the paper's own data. Among the 2,517 due trials, those that halted post results at 23.5% (78/332) versus 17.4% for those that did not. Terminated trials in this dataset are more likely to have posted, not less.
- **A reader objects:** This is an uncited generalisation from the reporting-bias literature that is false in the author's own table, in a section whose whole point is that the visible evidence base is thinner than it looks. A referee who checks it - and this one is easy to check - has found the paper asserting the opposite of its data.
- **Fix:** Cut the sentence, or replace it with what the data show: 'Posting is not lower among halted trials (23.5% vs 17.4%), so the shortfall is general rather than concentrated in failures.' The 'null' half is untestable here and should not be asserted.

### 2.8
**C25 — solid** · *useful*
> The technologies most likely to be deployed as population-level predictive tools are developed in the least representative populations; CAR-T includes a non-high-income-country site in 59.2% of trials, driven by Chinese activity, while affinity proteomics (10.8%), N-of-1 (11.0%) and polygenic risk scores (11.1%) are almost entirely high-income research.
- **Rests on:** Every number verified against access_equity_by_subfamily.csv, including AAV 63.4% US, CAR-T 55.9% China and AAV 31.4% non-high-income. The caveat that a middle-income trial site does not imply affordability there is correct and well placed.
- **A reader objects:** The ancestry argument for polygenic risk scores is stated without citation, and 'high-income-country-only' is inferred from trial site geography, not from discovery-cohort ancestry - two different things. The conclusion is right; the evidence in this dataset is one step removed from it.
- **Fix:** Say 'trial-site geography is a proxy for, not a measure of, discovery-cohort ancestry' and cite the portability literature.

### 3.1
**C26 — solid** · *useful*
> Maturity stage does not predict business-attributed halt share (rho = 0.00, p = 1.00), and this test has almost no power because the ten measurable platforms take only two stage values.
- **Rests on:** Reproduced exactly (rho = 0.000, p = 1.000; six at stage 5, four at stage 4). Refusing to read the null as a result ('that would be reading a null as a result') is the correct handling.

### 3.2
**C27 — caveat** · *useful*
> Precision is not measurably narrowing the addressable population: neither trials-per-indication (rho = -0.38, p = 0.35) nor median enrollment (rho = -0.04, p = 0.93) trends with generation; enrollment is uniformly small (medians 10-40).
- **Rests on:** The enrollment correlation reproduces exactly (-0.036, p = 0.933) and the 10-40 median range holds across all eight subfamilies. Trials-per-indication is not a published column, so that one I could not check.
- **A reader objects:** The reframing - 'the payment mismatch was structural from the first trial' - is a stronger claim derived from a null at n = 8. It is more defensible than the failed original, but it is still an interpretation of a non-result.
- **Fix:** Publish the trials-per-indication column. And mark the reframed claim as interpretation: 'consistent with, rather than demonstrated by, these data.'

### 3.3
**C28 — new evidence** · *this is why they are reading*
> An independent behavioural instrument - sponsor exit - does not corroborate the stated-reason finding (rho = -0.50, p = 0.14, n = 10), if anything in the wrong direction.
- **Rests on:** The n = 10 figure reproduces exactly (-0.503, p = 0.138), but only because it includes in vivo LNP, whose business-cited share rests on 4 halted trials - below the 8-halt threshold the paper applies in Figure 1b and the 5-halt threshold in Section 4.5. Applying the paper's own inclusion rule gives n = 9, rho = -0.700, p = 0.036. Under its own threshold the instrument does not fail to corroborate; it significantly disagrees.
- **A reader objects:** The paper's most important negative result is softer than the data support, and the softening comes from silently relaxing an inclusion threshold used everywhere else. A referee who reconstructs the correlation from constraint_map_data.csv and sponsor_exit_rates.csv - the two published tables - gets p = 0.036 in the wrong direction, and will conclude the paper understated a disconfirmation.
- **Fix:** Report both: 'rho = -0.50 (p = 0.14) across the 10 platforms with 8 or more industry sponsors; restricting to platforms with 8 or more halted trials as elsewhere in this paper, rho = -0.70 (p = 0.036).' Then change the language from 'does not corroborate' to 'disagrees'. Also note the correlation is unweighted, so AI/ML with 355 sponsors counts the same as LNP with 13 - a sponsor-weighted version is the obvious robustness check.
**C29 — solid** · *this is why they are reading*
> Until the disagreement is resolved, Section 2.1 should be read as a finding about how sponsors describe stopping, which is weaker than a finding about whether sponsors leave.
- **Rests on:** This is the paper's most important sentence and it is correct. The three candidate readings offered (one-trial academic-adjacent sponsors, a too-recent 2022 cutoff, or a genuine failure of the main measure) are the right three, and the paper does not pretend to distinguish them.
- **A reader objects:** A hostile reader will ask why, if this is true, the title and abstract assert a claim about what stops programs rather than about what sponsors say. The paper's own retraction in 3.3 is stronger than the framing it retracts.
- **Fix:** Promote this sentence to the abstract. It is the difference between a paper a skeptic respects and one they dismiss - and right now it is buried in Section 3.

### 3.4
**C30 — **NOT DEFENSIBLE**** · *this is why they are reading*
> The claim is falsifiable: it predicts elevated business-attributed halting among industry-sponsored programs of any modality, and would have been refuted had industry-sponsored diagnostics shown the elevated rate.
- **Rests on:** The stated prediction is not what the data show. Industry diagnostics sit at 25.9%, indistinguishable from the non-industry cells - so on the paper's own falsification criterion ('industry-sponsored programs of any modality') the claim is refuted, not confirmed. What the data support is a joint condition: industry sponsorship AND therapeutic modality.
- **A reader objects:** This is a logical slip in the section specifically written to pre-empt the charge of unfalsifiability. As written, the falsification test is failed by the paper's own numbers and then reported as passed in the next clause.
- **Fix:** Rewrite the prediction to match the result: 'the finding predicts elevated business-attributed halting where industry sponsorship and therapeutic modality coincide, and predicts no elevation where either is absent. It would have been refuted had industry-sponsored therapeutics matched the other cells, or had either single factor produced the elevation on its own.' Then add the two out-of-sample tests that would actually discriminate it - a matched non-molecular comparator (Limitation 3c) and the sponsor-collapsed analysis (C5).

### 4.1
**C31 — solid** · *this is why they are reading*
> For diagnostics the remedy is evidentiary, and liquid biopsy is the template: 278 trials naming the assay as the intervention and 23 at Phase 3+, against affinity proteomics with 41 records, one such trial and none at Phase 3.
- **Rests on:** All four numbers verified against platform_lookup.csv and the master table, including the 35% annual publication growth for affinity proteomics (pub_cagr 0.349). This is the most useful comparison in the paper: it converts 'generate better evidence' into a countable target.
- **A reader objects:** 'and is reimbursed' is asserted without a source - no coverage or reimbursement data appears anywhere in this study, which is the paper's own stated gap. The comparison works without it.
- **Fix:** Either cite the coverage decisions or drop 'and is reimbursed' and let the trial counts carry the argument. Also state that liquid biopsy's 278 includes trials across many assays and sponsors, so it is a field-level target, not a single product's path.

### 4.2 / 4.4
**C32 — new evidence** · *useful*
> Regulatory capacity has become a variable: roughly 20,000 staff reductions across FDA, CDC and NIH, and the One Big Beautiful Bill Act mandates NIH funding of about $27.5 billion for 2026, roughly an $18 billion cut.
- **Rests on:** Nothing in this study bears on either claim, and the manuscript contains no reference list - these specific quantitative assertions about federal staffing and appropriations are uncited, as is 'industry commentary in early 2026' and the 'registry-wide termination analyses' invoked in Limitation 3c.
- **A reader objects:** A peer-reviewed journal will not accept a paper with zero citations, and least of all one whose policy section makes dated, specific, contested claims about appropriations and agency staffing without a single source. A policy reader will also note that congressional appropriations, not the reconciliation bill, set the final NIH figure - which the paper half-acknowledges and then quotes the mandated number anyway.
- **Fix:** Add a reference list. Every external claim in 4.2, 4.4 and Limitation 3c needs a source with a retrieval date, in the same style as commercial_retreat_cases.csv. Where the figure is contested (NIH 2026), give the range and the status rather than the point estimate.

### 4.4
**C33 — reword** · *useful*
> In vivo LNP genetic medicine grew 5.8-fold from 6 to 35 trials - the largest increase among gene-transfer platforms, though not the largest in the dataset (the AI-candidate probe grew 12.5-fold).
- **Rests on:** 5.83-fold verified. But the parenthetical implies the AI probe is the only larger growth: spatial omics grew 9.0-fold (4 to 36) and base editing went from 0 to 21 (undefined fold, larger in absolute terms). The superlative was checked against gene-transfer platforms but the 'not the largest in the dataset' clause was not checked against the full table.
- **A reader objects:** Exactly the class of error a reader checks first, because the master table makes it a ten-second test.
- **Fix:** Write 'the largest fold increase among the vector-based gene-transfer platforms; spatial omics (9.0-fold) and the AI-candidate probe (12.5-fold) are larger in the dataset, and base editing went from zero to 21.'
**C34 — reword** · *useful*
> Two independent methods converge: industry commentary reaching its conclusion from deal flow, and this dataset reaching it from sponsor-stated halt reasons.
- **Rests on:** The convergence argument is asserted against an uncited trade source, and it sits three pages after Section 3.3 reported that the study's own independent instrument does not converge. The paper claims corroboration from a source it does not cite while reporting disconfirmation from one it does.
- **A reader objects:** A referee will read this as selecting the agreeing instrument. It also is not independent: trade commentary and registry halt reasons both derive from company disclosure, so they share the disclosure incentive the paper flags in Limitation 2.
- **Fix:** Cite the source, drop 'independent' (both are sponsor disclosure), and cross-reference 3.3 in the same paragraph: 'a behavioural instrument constructed here does not converge (Section 3.3).' Reporting both makes the paragraph credible; reporting one makes it advocacy.

### 4.5
**C35 — caveat** · *this is why they are reading*
> The per-platform lookup table is the actionable form of the paper: read your row, and the binding constraint differs across rows.
- **Rests on:** The table reproduces platform_lookup.csv exactly, row for row, and the suppression rules (dominant blocker below 5 halts, results posting below 10 due trials) are applied consistently. Recommendation 1 (read your row, not the headline) and recommendation 2 (the liquid-biopsy-to-affinity-proteomics gap as a countable target) are genuinely actionable and specific to this dataset. Recommendation 3 is flagged by the author as argued not measured, and correctly notes it cuts against their own category assignment. Recommendation 4 is a restatement of Section 2.7.
- **A reader objects:** Two of the four are actionable and two are close to generic: 'delivery and manufacturing are underpriced' is the field's consensus position and is admitted to be unmeasured here, and 'treat evidence visibility as part of the work' is advice any reader already accepts. Also, CAR-T is staged 4 while in vivo LNP is staged 5 because CAR-T's industry share is 29.4% against a 30% threshold - the most-registered therapeutic platform in the dataset scores less mature than one with 68 trials, and a reader will see that as the ladder failing rather than as a finding.
- **Fix:** Keep 1 and 2 as the recommendations. Fold 4 into Section 2.7 and reduce 3 to one sentence in 4.1, since you concede it is unmeasured. Add a footnote to the Stage column naming the CAR-T/LNP inversion and its cause - Limitation 6 covers the principle but the reader needs it at the table.

### 5. Limitations
**C36 — caveat** · *this is why they are reading*
> Trials are not independent: CAR-T contributes 233 of 784 halts, and multiple trials from one sponsor are not independent observations, so p-values are anticonservative.
- **Rests on:** Honest and correctly signed, but understated in one direction and overstated in the other. Sponsor concentration in the key cell is low - 88 distinct sponsors across its 144 trials, top sponsor 6.2%, top five 17.4% - so clustering is a milder threat than implied. Conversely the CAR-T check the limitation names as 'appropriate' was never run on the current headline, and the sponsor-collapsed analysis flips one of the two null cells (C5).
- **A reader objects:** A referee will ask why a limitation names the right two checks and runs neither, when both take minutes with the published tables.
- **Fix:** Run both and move them out of Limitations into Section 2.1. Report the sponsor concentration figures - they are in your favour.

### 5. Limitations / 3c
**C37 — caveat** · *this is why they are reading*
> No external baseline is established, so part of what is measured may be a registry-wide property rather than a property of molecular medicine.
- **Rests on:** This is the correct first-order objection to the whole paper and the author raises it themselves. It is also the one limitation that cannot be answered by rewriting: without a matched non-molecular comparator, the reader cannot know whether 30.9% business-cited halts is high, average or low for ClinicalTrials.gov.
- **A reader objects:** A hostile reader will say the paper should not have been written without the comparator, since every headline is a bare rate with no reference class. The counter is that the interaction is a within-dataset contrast and needs no external baseline - but the title and abstract lead with the bare rate, not the interaction.
- **Fix:** Run the comparator. The same classification on a matched sample of non-molecular trials (same phase and year distribution) is a few hundred reason strings and would convert the paper's weakest structural gap into its strongest claim. Until then, lead with the interaction, which is baseline-free.

### 6. Conclusion
**C38 — **NOT DEFENSIBLE**** · *this is why they are reading*
> Across 14,061 registered trials, programs stop for money roughly six times as often as they stop for science.
- **Rests on:** Contradicted by three of the paper's own statements: Section 2.1 reports a range of 1.6-6.1 and says the magnitude is not robust; Limitation 3b says every ratio describes halted trials, not programs; and the reason field observes only a quarter to a third of concluded Phase 2+ programs.
- **A reader objects:** The Conclusion states as a point estimate the top of a range the Results explicitly refuse to collapse, and uses the unit the Limitations explicitly forbid. A referee reading the paper front to back arrives at this sentence having been told twice that it cannot be said.
- **Fix:** Rewrite: 'Among halted trials, sponsor-attributed business decisions outnumber stated scientific failures by between 1.6 and 6.1 to one depending on category boundaries, and that excess is concentrated in industry-sponsored therapeutic programs. Because the reason field observes only about a quarter of concluded Phase 2+ trials, this describes halted trials, not programs.'

### 7. Methods
**C39 — caveat** · *useful*
> Registry concept expansion badly contaminates phrase queries - a lentiviral query returned 7,296 studies of which 279 concerned lentiviral vectors - so all 25,600 returned records were re-filtered by literal regex to 14,061 retained records across 13,486 unique registrations. Reason strings were classified by a language model under a fixed schema with no human validation.
- **Rests on:** The 14,061 and 13,486 verify exactly. The 25,600 and 7,296 intermediates are not published, so the retention rate cannot be audited. This methodological finding is real and useful - most registry analyses do not do it - and the per-row query strings are published, which is the part that matters. The classification is correctly disclosed in Limitation 7 and mitigated by publishing all 673 verbatim strings next to their labels - which is exactly what let me audit the business category independently; the 'prefer a scientific cause when the text states one' instruction is the right conservative choice.
- **A reader objects:** The regex per subfamily is described but not published as a column, so the filter cannot be reproduced. And Section 2.4's N-of-1 numbers (31 Phase 3+ trials, same-year clinic-to-Phase-3) suggest the filter did not fully solve the problem for at least one subfamily. And a journal will require human validation with agreement statistics before accepting a single-coder machine classification as a paper's central measure; a preprint or policy report will accept the published-strings mitigation.
- **Fix:** Publish the literal regex per subfamily alongside ctgov_query, and the pre-filter and post-filter counts per row. Then hand-audit the two subfamilies whose counts look contaminated (N-of-1, and the AI/ML 5,601). Hand-code a stratified sample of 150-200 strings, report Cohen's kappa, and re-report the headline 2x2 on the human-coded subset - the cheapest single change that moves this paper up a venue tier.

---

## 6. Scope of this review
The reviewer declared these limits, which travel with its numbers:
- Read the figure deck as images for pages 1, 6 and 12 only (Figures 1, 6, S4 - the three figures carrying the pressure points named in the brief); the other 10 pages were adjudicated from their captions in the manuscript plus their underlying source tables, which I read in full.
- Did not read trial_records.csv row by row (14,061 rows); all claims against it were checked by aggregation, as the brief directed.
- Two manuscript numbers could not be checked because their inputs are not published: the trials-per-indication correlation in Section 3.2 (no such column) and the 25,600 / 7,296 pre-filter retrieval counts in Methods. Both are flagged as unverifiable in the relevant claim rows rather than assessed.
- My reconstruction of the '159 financial-cause' subset is provisional: I could not recover the author's term list, so the 75-79 / 139 / 194 alternatives I report are my own candidate readings, not a correction of a known value.

I independently recomputed the review's consequential new numbers before relaying them: the
threshold-dependent sponsor-exit correlation (ρ = −0.503, p = 0.138 as published; ρ = −0.700,
p = 0.036 at the paper's own ≥8-halt rule), the sponsor-collapsed interaction (industry OR 6.10,
p = 1.1×10⁻⁷; non-industry OR 1.72, p = 0.029), the CAR-T-excluded interaction (industry OR 4.60,
p = 7×10⁻⁵; non-industry OR 0.93, p = 0.64; sponsor-within-therapeutics OR 6.12, p = 4.9×10⁻⁵),
sponsor concentration in the focal cell (88 sponsors over 144 trials, top 6.2%, top five 17.4%),
the AAV recruitment binomial (0/24 against a 17.7% base rate, p = 0.0094), the reporting-rate
contradiction (halted trials post at 23.5% vs 17.4%), and the strict deduplicated censoring figure
(414 completed vs 136 halted, 24.7% observed). All reconcile. The '159' financial-cause subset does
not: a strict money-term list gives 79, adding business/strategy terms gives 141, a wide list
including 'sponsor' gives 193.
