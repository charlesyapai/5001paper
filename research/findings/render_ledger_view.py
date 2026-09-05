"""Render findings_ledger.csv as a markdown table (research/findings/ledger.md) for reading on GitHub Pages.
The CSV stays the source of record; rerun this after every ledger change:
    python3 render_ledger_view.py
"""
import csv
from pathlib import Path

here = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(here / "findings_ledger.csv", newline="")))
esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
out = ["# Findings ledger (rendered view)", "", f"Rendered from `findings_ledger.csv` ({len(rows)} findings). The CSV is the source of record.", "",
       "| id | date | topic | status | statement | evidence | source | confidence | used in | notes |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    out.append("| " + " | ".join(esc(r[c]) for c in ["id", "date", "topic", "status", "statement", "evidence", "source", "confidence", "used_in", "notes"]) + " |")
(here / "ledger.md").write_text("\n".join(out) + "\n")
print(f"ledger.md: {len(rows)} rows")
