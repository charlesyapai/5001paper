#!/usr/bin/env python3
"""
02_classify_halts.py — assign a cause category to each free-text WhyStopped string.

METHOD AND ITS KNOWN WEAKNESS
-----------------------------
ClinicalTrials.gov requires a sponsor to record a reason when a trial is terminated,
withdrawn or suspended. Those strings are heterogeneous free text. A hand-tuned regex
pass was tried first and rejected: it left roughly a third unclassifiable and, worse,
mislabelled trials whose participants had simply rolled into a long-term follow-up
study as failures. The published run used a language model constrained to a fixed
label set via a tool schema.

THIS IS THE LARGEST METHODOLOGICAL GAP IN THE STUDY. The published classification is
SINGLE-CODER and MACHINE-ASSIGNED with no inter-rater statistic. Before relying on the
category counts, hand-code a stratified sample of 150-200 strings and report a kappa.
`--sample N` writes a blank coding sheet for exactly that purpose.

TWO SETTLED HANDLING RULES (keep them)
--------------------------------------
1. Text describing participants transferring into a long-term follow-up, extension or
   rollover study is an ADMINISTRATIVE TRANSFER, not a failure. It gets its own label
   and must be excluded from failure counts.
2. Trials with no stated cause are kept as a visible "No reason stated" category. They
   are never dropped and never attributed.

The prompt below deliberately biases toward scientific causes: it instructs the model to
prefer safety or efficacy whenever the text states one, so the business/funding bucket
reads as a LOWER bound and the scientific buckets as upper bounds.

Usage:
  python 02_classify_halts.py --in ../data/primary/trial_records_refreshed.csv
  python 02_classify_halts.py --in ... --sample 200   # blank sheet for human coding
"""
import argparse, json, os, sys
import pandas as pd

CATEGORIES = [
    "Safety or toxicity",
    "Efficacy failure or futility",
    "Recruitment or feasibility failure",
    "Funding, business or strategic decision",
    "Manufacturing or product supply",
    "Regulatory or ethics hold",
    "COVID-19 disruption",
    "Investigator, site or administrative",
    "Protocol redesign or replacement",
    "Administrative rollover or transfer (not a failure)",
    "Unclear",
]

SYSTEM = (
    "You classify why a clinical trial stopped, using ONLY the reason text given. "
    "Reply with exactly one category label from the provided list and nothing else. "
    "Rules: prefer a scientific cause (safety, efficacy) when the text states one. "
    "Sponsor or company decisions, portfolio or strategy changes, pipeline "
    "deprioritisation, funding shortfalls, and 'development plan change' are "
    "'Funding, business or strategic decision'. Text saying participants move to a "
    "long-term follow-up, extension or rollover study, or that the trial was replaced by "
    "a differently-sponsored trial, is 'Administrative rollover or transfer (not a "
    "failure)'. Use 'Unclear' only when the text carries no information about cause."
)

TOOL = {"name": "classify_stop",
        "input_schema": {"type": "object",
                         "properties": {"category": {"type": "string", "enum": CATEGORIES}},
                         "required": ["category"]}}

HALTED = ["TERMINATED", "WITHDRAWN", "SUSPENDED"]

# Boolean audit columns published alongside the labels so the ratio endpoints in the
# paper are reproducible. See manuscript Methods.
PAT_FINANCIAL = (r"fund|financ|budget|cost|capital|invest|econom|resourc|\bmoney\b|"
                 r"\bfee\b|revenue|profit")
PAT_FIN_OR_BIZ = PAT_FINANCIAL + r"|business|commercial|strateg|portfolio|prioriti"
PAT_DENIES_SAFETY = (r"not (due to|related to|because of|for)[^.]{0,40}(safety|toxicit|efficacy)|"
                     r"no safety (concern|signal|issue)|unrelated to safety|not a safety")


def classify_batch(strings, model=None, max_concurrency=16, chunk=400):
    """Label distinct reason strings. Requires a `host.llm`-style batch interface.

    In the Claude Science kernel `host` is pre-injected. Elsewhere, replace this
    function body with a call to whatever LLM client you have — the contract is
    {string -> one label from CATEGORIES}. Keep SYSTEM and TOOL unchanged so the
    labels stay comparable with the published run.
    """
    try:
        host  # noqa: F821  (injected in the Claude Science kernel)
    except NameError:
        raise RuntimeError(
            "No `host` in scope. Either run this inside Claude Science, or replace "
            "classify_batch() with your own LLM call using the SYSTEM prompt and TOOL "
            "schema defined above."
        )
    reqs = [{"prompt": f'Reason a clinical trial stopped:\n"""{s}"""\n\nClassify it.',
             "system": SYSTEM, "tools": [TOOL],
             "tool_choice": {"type": "tool", "name": "classify_stop"},
             "max_tokens": 200, "thinking": {"type": "disabled"},
             "model": model or host.reasoning_model()}  # noqa: F821
            for s in strings]
    res = []
    for i in range(0, len(reqs), chunk):          # batch cap: chunk the fan-out
        res += host.llm(reqs[i:i + chunk], max_concurrency=max_concurrency)  # noqa: F821
    out = {}
    for s, r in zip(strings, res):
        tu = r.get("tool_use") if isinstance(r, dict) else None
        cat = (tu or {}).get("input", {}).get("category")
        out[s] = cat if cat in CATEGORIES else "Unclear"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--sample", type=int, default=0,
                    help="write a blank human-coding sheet of N strings and exit")
    args = ap.parse_args()

    tr = pd.read_csv(args.inp, low_memory=False)
    halted = tr[tr.status.isin(HALTED)].copy()
    print(f"halted records: {len(halted)}  unique NCT: {halted.nct.nunique()}")
    with_reason = halted[halted.why.notna() & (halted.why.astype(str).str.strip() != "")]
    uniq = sorted({s.strip() for s in with_reason.why.astype(str)})
    print(f"with a stated reason: {len(with_reason)} ({len(with_reason)/len(halted):.0%})"
          f"  distinct strings: {len(uniq)}")

    if args.sample:
        import random
        random.seed(0)
        sheet = pd.DataFrame({"why": random.sample(uniq, min(args.sample, len(uniq)))})
        sheet["human_category"] = ""
        sheet["categories_allowed"] = " | ".join(CATEGORIES)
        p = os.path.join(os.path.dirname(os.path.abspath(args.inp)),
                         "human_coding_sheet.csv")
        sheet.to_csv(p, index=False)
        print(f"\nwrote {len(sheet)} strings for human coding -> {p}\n"
              f"Code them, then compute Cohen's kappa against the machine labels.")
        return

    lab = classify_batch(uniq)
    halted["blocker"] = [lab.get(str(w).strip(), "No reason stated")
                         if isinstance(w, str) and w.strip() else "No reason stated"
                         for w in halted.why]
    why = halted.why.fillna("")
    halted["names_financial_cause"] = why.str.contains(PAT_FINANCIAL, case=False, regex=True)
    halted["names_financial_or_business"] = why.str.contains(PAT_FIN_OR_BIZ, case=False, regex=True)
    halted["denies_safety_cause"] = why.str.contains(PAT_DENIES_SAFETY, case=False, regex=True)

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.inp)),
                                   "halted_trials_blockers_refreshed.csv")
    halted.to_csv(out, index=False)
    print("\n" + halted.blocker.value_counts().to_string())
    print(f"\nwrote {out}")
    print("REMINDER: exclude 'Administrative rollover or transfer' before any failure "
          "count, and deduplicate by NCT.")


if __name__ == "__main__":
    main()
