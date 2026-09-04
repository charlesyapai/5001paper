# Research log

Append only. Newest at the bottom.

## 2026-09-02
- Registry data retrieved from ClinicalTrials.gov v2 and PubMed for 21 subfamilies with `code/01_retrieve.py`.

## 2026-09-03
- Manuscript revised after the claim-by-claim review; revision note at the top of `manuscript/manuscript.md`.

## 2026-09-04
- Referee pitch written from manuscript v7: `review/referee_pitch.md`.
- Recomputation of the 784-trial halted set. The interaction survives restriction to interventional trials (F001). The industry-therapeutic cell is two-thirds CAR-T and its business-cited share rises sharply for trials started in 2022 or later (F002, F003). The business category is mostly boilerplate (F004). The imaging-AI subfamily cannot serve as a comparator for the therapeutic row (F005). Chinese-named sponsors are not the driver (F006). Script: `findings/recompute_2026-09-04.py`.
- Literature baselines fetched: JNCI 2026 phase 1 solid-tumour terminations (F007, F008), Zhang 2023 Cancer Medicine (F009). Buergy 2021 seen as a snippet only (F010).
- Decision D001: the flagship becomes the translation timeline. D002: the halt-reason analysis becomes the companion methods paper. D003 to D005 on comparator design, disclosure audit and the investment layer. See `DECISIONS.md`.
- `manuscript/translation_timeline_plan.md` written. README, OPEN_ITEMS and MANIFEST updated. Plan published as a shareable page.
- Literature scan for prior integrated analyses (S06 to S21). Pieces exist for every layer; no integrated stage timeline found (F012 to F015, F017).
- Research base created. Seed tables converted to CSVs under `data/cohort/` with verification columns.
- FDA approved cellular and gene therapy products page fetched, page dated 18 August 2026: 53 entries. Seven products absent from the seed list added to the cohort (F016). Approval dates are not on the list page and remain to be verified product by product.
- Repository initialised under git.
