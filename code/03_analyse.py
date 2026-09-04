#!/usr/bin/env python3
"""
03_analyse.py — reproduce every headline statistic in the manuscript from the
published tables, and print each one next to its expected value.

Run this FIRST after migrating. If any line prints MISMATCH, the environment or the
data differs from the published run and nothing downstream should be trusted.

Usage:  python 03_analyse.py [--data ../data]
"""
import argparse, os, sys
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, spearmanr, binomtest

SCI = {"Safety or toxicity", "Efficacy failure or futility"}
BIZ = "Funding, business or strategic decision"
REC = "Recruitment or feasibility failure"
HALTED = ["TERMINATED", "WITHDRAWN", "SUSPENDED"]
PAY_TERMS = (r"reimburs|payer|payor|\bprice|pricing|market size|cost[- ]effect|\bHTA\b|"
             r"formulary|coverage|\bCMS\b|\bNICE\b|willingness to pay")

_fails = []


def chk(label, got, expect, tol=0.02):
    ok = abs(got - expect) <= tol * max(abs(expect), 1e-9) if isinstance(expect, float) \
        else got == expect
    print(f"  {'ok  ' if ok else 'MISMATCH'}  {label:58s} got {got}   expected {expect}")
    if not ok:
        _fails.append(label)


def two_by_two(df, row_col, pos, neg, outcome):
    t = pd.crosstab(df[row_col], df[outcome])
    a, b = int(t.loc[pos, True]), int(t.loc[pos, False])
    c, d = int(t.loc[neg, True]), int(t.loc[neg, False])
    o, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    return a, b, c, d, o, p


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--data", default=os.path.join(here, "..", "data"))
    args = ap.parse_args()
    P = lambda *x: os.path.join(args.data, *x)

    H = pd.read_csv(P("primary", "halted_trials_dedup.csv"))
    TR = pd.read_csv(P("primary", "trial_records.csv"), low_memory=False)
    M = pd.read_csv(P("derived", "technology_maturity_matrix.csv"))
    EX = pd.read_csv(P("derived", "sponsor_exit_rates.csv"))

    print("\n== 1. dataset shape ==")
    chk("retained trial records", len(TR), 14061)
    chk("deduplicated halted trials", len(H), 784)
    chk("technology subfamilies", len(M), 21)

    print("\n== 2. halt causes (deduplicated) ==")
    vc = H.blocker.value_counts()
    biz, rec = int(vc.get(BIZ, 0)), int(vc.get(REC, 0))
    sci = int(sum(vc.get(k, 0) for k in SCI))
    tech = int(vc.get("Manufacturing or product supply", 0) + vc.get("Regulatory or ethics hold", 0))
    chk("business-cited halts", biz, 242)
    chk("safety+efficacy halts", sci, 40)
    chk("recruitment-cited halts", rec, 225)
    print(f"\n  ratio range across defensible category boundaries "
          f"(the paper reports this range, NOT a point estimate):")
    fin = int((H.blocker.eq(BIZ) & H.get("names_financial_cause", pd.Series(False, index=H.index))).sum()) \
        if "names_financial_cause" in H.columns else None
    print(f"    as categorised                              {biz}:{sci} = {biz/sci:.1f}")
    print(f"    manufacturing+regulatory counted technical  {biz}:{sci+tech} = {biz/(sci+tech):.1f}")
    if fin:
        print(f"    business restricted to named financial      {fin}:{sci} = {fin/sci:.1f}")
        print(f"    both adjustments                            {fin}:{sci+tech} = {fin/(sci+tech):.1f}")
    print("    -> the range INCLUDES PARITY. Do not quote the aggregate ratio as a finding.")
    b = binomtest(biz, biz + rec, 0.5, alternative="greater")
    chk("business > recruitment, one-sided p", round(b.pvalue, 2), 0.23)

    print("\n== 3. THE MAIN RESULT: modality x sponsor class ==")
    for m in ["Therapeutic", "Diagnostic/analytic"]:
        for s, lab in [(True, "industry"), (False, "non-industry")]:
            g = H[(H.modality == m) & (H.ind == s)]
            print(f"  {m:20s} {lab:13s} {int(g.biz.sum()):3d}/{len(g):3d} = {g.biz.mean():.3f}")
    for s, lab, eo in [(True, "industry", 5.54), (False, "non-industry", 1.07)]:
        *_, o, p = two_by_two(H[H.ind == s], "modality", "Therapeutic", "Diagnostic/analytic", "biz")
        chk(f"modality OR among {lab} sponsors", round(o, 2), eo)
    th = H[H.modality == "Therapeutic"].assign(k=lambda d: np.where(d.ind, "I", "N"))
    *_, o, p = two_by_two(th, "k", "I", "N", "biz")
    chk("sponsor-class OR within therapeutics", round(o, 2), 6.36)
    dg = H[H.modality != "Therapeutic"].assign(k=lambda d: np.where(d.ind, "I", "N"))
    *_, o, p = two_by_two(dg, "k", "I", "N", "biz")
    chk("sponsor-class OR within diagnostics", round(o, 2), 1.23)

    print("\n== 4. sensitivity: the two analyses the Limitations promise ==")
    X = H[H.subfamily != "Engineered T-cell therapy (CAR-T)"]
    *_, o, p = two_by_two(X[X.ind], "modality", "Therapeutic", "Diagnostic/analytic", "biz")
    chk("modality OR among industry, CAR-T excluded", round(o, 2), 4.60)
    coll = (H.dropna(subset=["sponsor"])
              .groupby(["sponsor", "modality"])
              .agg(biz=("biz", "max"), ind=("ind", "first")).reset_index())
    *_, o, p = two_by_two(coll[coll.ind], "modality", "Therapeutic", "Diagnostic/analytic", "biz")
    chk("modality OR among industry, one row per sponsor", round(o, 2), 6.10)
    *_, o, p = two_by_two(coll[~coll.ind], "modality", "Therapeutic", "Diagnostic/analytic", "biz")
    chk("modality OR among non-industry, one row per sponsor", round(o, 2), 1.72)
    cell = H[(H.modality == "Therapeutic") & H.ind]
    chk("distinct sponsors in the focal cell", cell.sponsor.nunique(), 88)

    print("\n== 5. the diagnostic mirror image ==")
    *_, o, p = two_by_two(H, "modality", "Diagnostic/analytic", "Therapeutic", "rec")
    chk("recruitment OR, diagnostic vs therapeutic", round(o, 2), 2.69)

    print("\n== 6. AAV, the extreme case ==")
    aav = H[H.subfamily == "AAV gene transfer"]
    base = H[H.modality == "Therapeutic"].rec.mean()
    bt = binomtest(int(aav.rec.sum()), len(aav), base, alternative="less")
    chk("AAV business-cited halts", int(aav.biz.sum()), 18)
    chk("AAV halted trials", len(aav), 24)
    chk("AAV zero-recruitment binomial p", round(bt.pvalue, 3), 0.009)

    print("\n== 7. the instrument's blind spot (the key negative result) ==")
    n_pay = int(H.why.fillna("").str.contains(PAY_TERMS, case=False, regex=True).sum())
    chk("halt reasons naming a payer/price/HTA term", n_pay, 0)

    print("\n== 8. the disagreeing instrument (threshold-dependent) ==")
    bz = H.groupby("subfamily").agg(biz_share=("biz", "mean"), n_halted=("nct", "size"))
    J = EX.set_index("subfamily").join(bz).dropna(subset=["biz_share"])
    r_all, p_all = spearmanr(J.exit_rate, J.biz_share)
    J8 = J[J.n_halted >= 8]
    r_8, p_8 = spearmanr(J8.exit_rate, J8.biz_share)
    chk("sponsor-exit rho, all platforms", round(r_all, 2), -0.50)
    chk("sponsor-exit rho, >=8 halted trials (paper's own rule)", round(r_8, 2), -0.70)
    chk("sponsor-exit p, >=8 halted trials", round(p_8, 3), 0.036)
    print("    -> a DETECTED disagreement, not a failure to detect. Report both thresholds.")

    print("\n== 9. censoring and evidence visibility ==")
    pc = pd.to_datetime(TR.prim_compl, errors="coerce", format="mixed")
    due = TR[(TR.study_type == "INTERVENTIONAL") & pc.notna()
             & (pc <= pd.Timestamp("2023-12-31"))].drop_duplicates("nct")
    chk("share of due trials posting results", round(due.has_results.mean(), 3), 0.182)
    hl = due.status.isin(HALTED)
    print(f"    halted due trials post at {due[hl].has_results.mean():.3f} vs "
          f"{due[~hl].has_results.mean():.3f} for the rest — the shortfall is NOT "
          f"concentrated in failures")
    strict = TR[(TR.study_type == "INTERVENTIONAL")
                & TR.phase.fillna("").str.contains("PHASE2|PHASE3|PHASE4")
                & ~TR.phase.fillna("").eq("PHASE1|PHASE2")].drop_duplicates("nct")
    nc = int(strict.status.eq("COMPLETED").sum()); nh = int(strict.status.isin(HALTED).sum())
    chk("share of concluded Phase 2+ observed by the reason field", round(nh/(nc+nh), 3), 0.247)

    print("\n== 10. negative results (all four must stay in the paper) ==")
    chk("momentum vs maturity rho", round(spearmanr(M.share_trials_since_2021, M.stage_n)[0], 2), -0.08)

    print("\n" + "=" * 74)
    if _fails:
        print(f"FAILED to reproduce {len(_fails)} statistic(s):")
        for f in _fails:
            print("  -", f)
        sys.exit(1)
    print("All published statistics reproduced.")


if __name__ == "__main__":
    main()
