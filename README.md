# Precision-medicine registry study — migration bundle

Everything needed to continue this investigation in another environment: the manuscript,
all 13 figures, the primary and derived data, the reproduction code, and the review record.

Assembled 4 September 2026. Registry data retrieved 2 September 2026.

---

## Start here

```bash
pip install -r code/requirements.txt
cd code && python 03_analyse.py
```

`03_analyse.py` recomputes **24 published statistics** from the bundled tables and prints
each next to its expected value. It exits non-zero if any disagree. In the reference run
all 24 reproduce. **Run it before trusting anything else in this bundle** — it is the
fastest way to confirm the migration is intact.

---

## What is in here

| Path | Contents |
|---|---|
| `manuscript/` | `manuscript.md` is the current draft (v7). Also the three earlier framing documents: thesis architecture, implementation blockers, technology timeline map. **`translation_timeline_plan.md` is the fourth framing document and the current flagship direction (4 September 2026).** |
| `review/` | The adversarial review record: `referee_pitch.md` (pitch, methodology, findings, readership, extensions), `claim_review_walkthrough.md` and `claim_review.csv` (39-claim ledger with verdicts), `referee_report.md`, plus the three referee recomputation tables. |
| `figures/` | 13 figures at 300 dpi under submission names (`Figure_1`–`Figure_8`, `Figure_S1`–`Figure_S5`), `figure_deck.pdf` with all of them in narrative order, and `source_names/` holding the same files under the `figN_*.png` names the code refers to. |
| `data/primary/` | `trial_records.csv` — 14,061 retained trial records, one row per (subfamily, NCT). `halted_trials_blockers.csv` — every halted record with its verbatim reason next to its assigned label. `halted_trials_dedup.csv` — the 784-trial analysis set, one row per registration, with the audit flags. |
| `data/derived/` | 13 summary tables, all regenerable from primary. |
| `code/` | Three scripts, the query strings, and the literal regex filters. |

## The three scripts

1. **`01_retrieve.py`** — pulls ClinicalTrials.gov v2 for each subfamily using `queries.csv`
   and re-filters with `filter_regex.csv`. Writes a refreshed trial table plus a per-subfamily
   retention report.
2. **`02_classify_halts.py`** — assigns a cause category to each verbatim stop reason under a
   fixed 11-label schema. Also writes a blank human-coding sheet with `--sample N`.
3. **`03_analyse.py`** — the verification harness described above.

Scripts 1 and 2 regenerate the data; script 3 checks it. If you only want to extend the
analysis, you need script 3 and `data/`.

---

## Five things that will trip you up

**1. The registry's concept expansion silently ruins phrase queries.** `query.term` does not
restrict to a quoted phrase. `"lentiviral" OR "lentivirus"` returns ~7,300 studies of which
~280 concern lentiviral vectors — the rest are HIV trials matched through a lentivirus→HIV
concept link. Every retained record in this study passed a second, literal regex check over
its own title, summary, description, keywords and intervention names. `filter_regex.csv`
holds those patterns. **Do not remove this step**, and check the retention report if counts
look wrong.

**2. Subfamily queries overlap.** 33 registrations matched two subfamilies in the published
run, so the halted set is 817 rows over 784 unique registrations. **Deduplicate by NCT before
any counting or contingency test.** Every figure and number in the current manuscript is on
the 784 basis.

**3. The v2 API uses singular field names.** `Phase` and `Condition` work; `Phases` and
`Conditions` return HTTP 400.

**4. Trial phase belongs to the parent trial, not to a diagnostic assay.** A liquid-biopsy
sub-study inside a Phase 3 oncology trial is not a Phase 3 diagnostic. The `driver` column
flags records where the technology is named as the intervention or in the title; diagnostics
are staged only on that subset, with a separate maturity ladder from therapeutics.

**5. Administrative rollovers are not failures.** Reason text describing participants moving
into a long-term follow-up or extension study is an administrative transfer. It has its own
label and must be excluded from failure counts. Trials with no stated cause are kept as a
visible "No reason stated" category — never dropped, never attributed.

---

## Analysis conventions this project settled on

These were adopted after adversarial review overturned an earlier draft. They are worth
keeping.

- **Stratify halt-cause analyses by sponsor class before reporting any modality effect.** The
  pooled therapeutic-versus-diagnostic contrast (OR 2.46) is a composition artefact. The real
  structure is an interaction: the effect lives in industry-sponsored therapeutics (66%) and
  is absent among non-industry sponsors (OR 1.07, p = 0.41).
- **Report a null as a failure to detect, with its power limit** — never as evidence of
  absence. Four of this study's negative results rest on n = 8 to n = 21 platforms.
- **Check a superlative against the full table before writing it.** Several were caught only
  because a table said otherwise.
- **Regenerate derived claims about rankings, memberships and coordinates from the table in
  the same cell that writes the sentence.** Hand-edited prose drifted from the data more than
  once here.
- **A figure headline must not overgeneralise a stratum-specific result.**
- **Never mix analysis bases between figures and text.**
- **The aggregate business:science ratio is not quotable.** Across defensible category
  boundaries it spans 6.0, 2.5, 2.0 and 0.8 — it includes parity. Only the stratified
  contrast carries weight. All four endpoints are reproduced by `03_analyse.py` from the
  published boolean flags.

---

## The instrument's two structural limits

Both are established, both are in the manuscript, and neither is fixable with more registry
data.

**It cannot see payment.** Across all 784 halted trials, **zero** verbatim reasons name a
payer, price, reimbursement decision, coverage, formulary or HTA body. The field records
*that* a sponsor stopped, not *why the economics failed*. The paper's payment claim rests on
six hand-curated post-approval cases (`data/derived/commercial_retreat_cases.csv`), not on
the registry.

**It is censored with respect to scientific failure.** The reason field exists only for
terminated, withdrawn or suspended trials. Among concluded Phase 2+ interventional trials,
414 completed and 136 halted — so the field observes **24.7%** of concluded later-phase
trials, and completed-but-failed trials, where efficacy failure normally lands, are invisible
to it.

---

## Open items, in priority order

See `OPEN_ITEMS.md` for the full list with rationale. The first two should be done before
anyone outside the project reads the manuscript.

## Direction as of 4 September 2026

The flagship paper is now the **translation timeline** described in
`manuscript/translation_timeline_plan.md`: an end-to-end measurement of how long each stage of
translation takes by technology class, where programs and patients are lost, which levers
shorten the stages, and when the frontier platforms reach patients under current and reformed
architectures. The registry stated-reason analysis in `manuscript.md` continues as a companion
methods paper; `OPEN_ITEMS.md` items 1 to 3 still apply to it.
