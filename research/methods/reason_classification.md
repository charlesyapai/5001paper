# Reason classification

Two uses: the stated reasons in health technology assessment documents (topic 02), and the
disclosure audit for the companion paper (topic 07). Both reuse the fixed-schema approach of
`code/02_classify_halts.py`.

## Assessment-reason schema, draft
| Label | Meaning |
|---|---|
| evidence_comparator | uncertainty from single-arm or indirect comparison |
| evidence_durability | uncertainty about persistence of effect |
| evidence_population | trial population narrower or different from the label |
| cost_effectiveness | incremental cost per outcome above threshold |
| budget_impact | affordability at population level |
| price_negotiation | decision contingent on a price outcome |
| implementation | centre, infrastructure or delivery constraints |
| managed_entry_required | recommended only under data collection or outcomes-based terms |
| positive_unrestricted | recommended without restriction |
| other | anything else, with the verbatim text kept |

Procedure: extract the committee's reasoning section verbatim; classify with the model under
the fixed schema allowing multiple labels; human-code a stratified sample of 60 documents
across bodies and languages; report kappa by label. Classify from the original language and
validate on a translated sample.

## Disclosure audit protocol, companion paper
For each of the 95 industry-therapeutic business halts:
1. Identify the sponsor and the asset from the registry record.
2. Search press releases, 8-K and 10-K filings and earnings transcripts from six months before to twelve months after the last registry status change.
3. Record the first document that discusses the program's discontinuation and quote the stated cause.
4. Code the disclosed cause under the existing 11-label schema; add `competitive_landscape` and `financing_runway` as sub-labels of the business category.
5. Report: share with any external disclosure; share with a disclosed scientific cause; share with a disclosed competitive or financing cause; share with no disclosure. Two coders on a 30-halt subsample; kappa.

Output: `data/audit/industry_therapeutic_business_halts.csv`: nct, sponsor, asset, halt_status,
registry_reason, disclosure_doc, disclosure_date, disclosed_cause_verbatim, disclosed_label,
coder, notes.
