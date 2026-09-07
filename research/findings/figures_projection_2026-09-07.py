"""Figures for the landscape projection, version 2 (data/projection/*.csv from project_landscape_2026-09-07.py).
Figure_P1: backcast 2020 to 2025 for the four pipeline variants against the record, and the forecast 2027 to 2036 with the
10th to 90th percentile band. Figure_P2: patients treated per year by class (worldwide, baseline median, stacked) with the
all-class band, and the three regions. Figure_P3: one-way sensitivity (tornado) on worldwide patients in 2036 and the
structural alternatives. Figure_P4: cumulative incidence of funded access per system (F047).
Palette: dataviz reference categorical slots, fixed order. Run from research/findings:  python3 figures_projection_2026-09-07.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "data/projection"; FIG = ROOT / "figures"
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#8a6fd1", "#5b8c5a"]
TXT, TXT2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": TXT2, "xtick.color": TXT2, "ytick.color": TXT2,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True})

ap = pd.read_csv(P / "approvals_projection.csv")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=200, gridspec_kw={"width_ratios": [1, 1.4]})
ax = axes[0]
variants = [b.replace("backcast uncalibrated: ", "") for b in ap["block"].unique() if b.startswith("backcast uncalibrated")]
bc = ap[ap["block"].str.startswith("backcast uncalibrated") & (ap["year"] == "2020-2025 cumulative") & (ap["class"] == "five projected classes")]
for k, (_, r) in enumerate(bc.iterrows()):
    ax.plot([r["p10"], r["p90"]], [k, k], color=C[k], linewidth=6, alpha=0.35, solid_capstyle="butt")
    ax.plot(r["p50"], k, "o", color=C[k], markersize=7)
ax.axvline(bc["realised"].iloc[0], color=TXT, linewidth=1.2, linestyle="--")
ax.text(bc["realised"].iloc[0] + 0.5, len(bc) - 0.6, f"record: {int(bc['realised'].iloc[0])}", color=TXT, fontsize=8)
ax.set_yticks(range(len(bc))); ax.set_yticklabels([b.replace("backcast uncalibrated: ", "") for b in bc["block"]], fontsize=8)
ax.set_xlabel("approvals 2020 to 2025 in the five classes, uncalibrated backcast (median, 10th to 90th)")
ax.set_title("Backcast from the end-2019 pipeline, by pipeline unit", loc="left", color=TXT, fontsize=10.5)
ax.invert_yaxis()
ax = axes[1]
prim = ap[(ap["block"].str.startswith("backcast primary") | ap["block"].str.startswith("backcast calibrated")) & ap["year"].astype(str).str.isdigit()].copy()
prim["year"] = prim["year"].astype(int)
ax.fill_between(prim["year"], prim["p10"], prim["p90"], color=C[0], alpha=0.15, linewidth=0)
ax.plot(prim["year"], prim["p50"], color=C[0], linewidth=2, label="backcast median, primary variant")
ax.plot(prim["year"], prim["realised"], color=TXT, linewidth=0, marker="o", markersize=5, label="realised first approvals, five classes")
fc = ap[(ap["block"] == "forecast") & (ap["class"] == "all genetic")].copy(); fc["year"] = fc["year"].astype(int)
ax.fill_between(fc["year"], fc["p10"], fc["p90"], color=C[1], alpha=0.15, linewidth=0, label="10th to 90th percentile")
ax.plot(fc["year"], fc["p50"], color=C[1], linewidth=2, label="forecast median, all genetic products")
ax.axvline(2026, color=GRID, linewidth=1); ax.text(2026.1, ax.get_ylim()[1] * 0.95, "today", color=TXT2, fontsize=8)
ax.set_ylabel("first approvals per year (FDA or EMA)"); ax.set_xticks(list(range(2020, 2037, 2)))
ax.set_title("Approvals: backcast against the record, then forward", loc="left", color=TXT, fontsize=10.5)
ax.legend(frameon=False, fontsize=8, loc="upper right")
fig.tight_layout(); fig.savefig(FIG / "Figure_P1_approvals_projection.png"); plt.close(fig)

pt = pd.read_csv(P / "patients_projection.csv"); base = pt[pt["scenario"] == "baseline"]
classes = ["CAR-T", "AAV", "lentiviral ex vivo", "CRISPR ex vivo", "in vivo editing and LNP"]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=200, gridspec_kw={"width_ratios": [1.3, 1]})
ax = axes[0]; w = base[base["region"] == "worldwide"]; years = sorted(w["year"].unique()); bottom = pd.Series(0.0, index=years)
for k, c in enumerate(classes):
    v = w[w["class"] == c].set_index("year")["patients_p50"].reindex(years).fillna(0)
    ax.bar(years, v, bottom=bottom, color=C[k], width=0.8, label=c, linewidth=0); bottom = bottom + v
allc = w[w["class"] == "all classes"].set_index("year").reindex(years)
ax.errorbar(years, allc["patients_p50"], yerr=[allc["patients_p50"] - allc["patients_p10"], allc["patients_p90"] - allc["patients_p50"]], fmt="none", ecolor=TXT2, elinewidth=1, capsize=2, label="all classes, 10th to 90th")
ax.set_title("Patients treated per year, worldwide, baseline median by class", loc="left", color=TXT, fontsize=10.5); ax.set_ylabel("patients per year")
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax = axes[1]
for k, region in enumerate(["US", "Europe", "rest of world"]):
    r = base[(base["region"] == region) & (base["class"] == "all classes")].set_index("year").reindex(years)
    ax.plot(years, r["patients_p50"], color=C[k], linewidth=2, label=region); ax.fill_between(years, r["patients_p10"], r["patients_p90"], color=C[k], alpha=0.12, linewidth=0)
cap = pt[(pt["scenario"] == "capacity-constrained") & (pt["region"] == "US") & (pt["class"] == "all classes")].set_index("year").reindex(years)
ax.plot(years, cap["patients_p50"], color=C[0], linewidth=1.2, linestyle="--", label="US, capacity-constrained")
ax.set_title("By region, all classes (median and band)", loc="left", color=TXT, fontsize=10.5); ax.legend(frameon=False, fontsize=8, loc="upper left")
for a in axes:
    a.set_xticks(list(range(2027, 2037, 3)))
fig.tight_layout(); fig.savefig(FIG / "Figure_P2_patients_projection.png"); plt.close(fig)

one = pd.read_csv(P / "sensitivity_oneway.csv"); st = pd.read_csv(P / "sensitivity_structural.csv")
b0 = one["base_patients_worldwide_2036_p50"].iloc[0]
piv = one.pivot_table(index="assumption", columns="arm", values="patients_worldwide_2036_p50")
piv["span"] = (piv["high"] - piv["low"]).abs(); piv = piv[piv["span"] > 0].sort_values("span")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), dpi=200, gridspec_kw={"width_ratios": [1.2, 1]})
ax = axes[0]
for k, (name, r) in enumerate(piv.iterrows()):
    lo, hi = min(r["low"], r["high"]), max(r["low"], r["high"])
    ax.barh(k, hi - b0, left=b0, color=C[1], alpha=0.8, height=0.6); ax.barh(k, lo - b0, left=b0, color=C[0], alpha=0.8, height=0.6)
ax.axvline(b0, color=TXT, linewidth=1); ax.set_yticks(range(len(piv))); ax.set_yticklabels(piv.index, fontsize=8)
ax.set_xlabel("worldwide patients in 2036, median: one assumption at its low (blue) or high (orange) value")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k"))
ax.set_title("One-way sensitivity", loc="left", color=TXT, fontsize=10.5)
ax = axes[1]
st2 = st.copy(); st2["label"] = st2["alternative"].str.replace(" (calibrated where the backcast misses)", "", regex=False).str.replace("base (assumptions at base values, sampling uncertainty only)", "base", regex=False)
for k, (_, r) in enumerate(st2.iterrows()):
    ax.plot([r["patients_worldwide_2036_p10"], r["patients_worldwide_2036_p90"]], [k, k], color=C[2], linewidth=6, alpha=0.35, solid_capstyle="butt"); ax.plot(r["patients_worldwide_2036_p50"], k, "o", color=C[2], markersize=6)
    ax.text(r["patients_worldwide_2036_p90"] + 1000, k, f"{int(r['approvals_2027_2036_all_genetic_p50'])} approvals", va="center", fontsize=7.5, color=TXT2)
ax.set_yticks(range(len(st2))); ax.set_yticklabels(st2["label"], fontsize=7.5); ax.invert_yaxis()
ax.set_xlabel("worldwide patients in 2036 (median, 10th to 90th)"); ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k")); ax.set_title("Structural alternatives", loc="left", color=TXT, fontsize=10.5)
fig.tight_layout(); fig.savefig(FIG / "Figure_P3_sensitivity.png"); plt.close(fig)

cv = pd.read_csv(ROOT / "data/access/access_survival_curves.csv"); cv = cv[cv["endpoint"] == "primary"]
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=200)
for k, s in enumerate(["Germany", "Italy", "England", "France", "Canada", "Australia", "United States"]):
    g = cv[cv["system"] == s]; ax.step(g["months"], g["cif_funded"], where="post", color=C[k], linewidth=2, label=s)
ax.set_xlim(0, 84); ax.set_ylim(0, 1); ax.set_xlabel("months from authorisation in the system"); ax.set_ylabel("share of authorised products with funded access")
ax.set_title("Funded access as cumulative incidence, refusals and withdrawals competing (F047)", loc="left", color=TXT, fontsize=10.5)
ax.legend(frameon=False, fontsize=8, loc="lower right", ncol=2)
fig.tight_layout(); fig.savefig(FIG / "Figure_P4_access_incidence.png"); plt.close(fig)
print("figures written: P1, P2, P3, P4")
