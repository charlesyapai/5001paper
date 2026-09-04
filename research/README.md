# Research base

The working knowledge base for the flagship translation-timeline paper and the companion
methods paper. Started 4 September 2026. Everything here is an established fact with its
evidence, a method with its specification, or a decision with its rationale. Manuscript prose
is written from this base, not the other way round.

## Layout

| Path | What it holds |
|---|---|
| `LOG.md` | Chronological log of what was done, found and decided. Append only. |
| `DECISIONS.md` | Decision record. One entry per decision, with rationale and consequences. |
| `topics/` | One folder per topic area. Each README states scope, the questions the layer answers, what is known, sources, tasks and open questions. Numbered in stage order because the stages are a sequence. |
| `methods/` | One file per method or data pipeline: what is measured, how, with what caveats, and the shape of the output table. |
| `findings/` | `findings_ledger.csv`, the single list of established facts with evidence and status, plus the scripts that regenerate the numbers in it. Every number that reaches a manuscript has a row here first. |
| `sources/` | `bibliography.csv`: every source consulted, what it gives, and whether it was read in full or only seen as a search snippet. |
| `../data/cohort/` | Seed tables for the new layers, as CSVs with verification columns. |

## Status vocabulary

| Status | Meaning |
|---|---|
| `verified-from-data` | Recomputed from a table in this bundle by a named script or command. |
| `verified-from-source` | Read from the primary document, fetched on the stated date. |
| `derived` | Arithmetic on verified rows, with the assumption stated in the row. |
| `provisional-from-snippet` | Seen only in a search summary. Usable for orientation, never for a figure. |
| `seeded-from-memory` | Written down without a source. Must be replaced before use. |
| `refuted` | Kept for the record, with the id of the row that refuted it. |

## Rules

1. A finding enters the ledger before it enters any prose.
2. Every number in the ledger names the file and the script or command that regenerates it.
3. `seeded-from-memory` and `provisional-from-snippet` rows never enter a figure or an abstract.
4. Penetration and eligible-population figures always carry a range.
5. Analysis bases are never mixed between a figure and its text.
6. Check every superlative against the full table before writing it.
7. Report a null as a failure to detect, with its power limit.
8. Commit messages carry the finding or decision id.

## How to add a finding

1. Append a row to `findings/findings_ledger.csv` with the next id.
2. Add the source to `sources/bibliography.csv` if it is new.
3. Add a line under "What we know" in the relevant topic README, citing the finding id.
4. Log it in `LOG.md`.
5. Commit with the message `F0xx: one-line statement`.
