"""Figures for the landscape projection (data/projection/*.csv from project_landscape_2026-09-06.py).
Figure_P1: genetic-product approvals per year, backcast 2020 to 2025 against the record and forecast 2027 to 2036 with the 10th
to 90th percentile band. Figure_P2: patients treated per year by class, worldwide, baseline (median, stacked) with the
all-class band, and the US and Europe medians. Palette: dataviz reference categorical slots, fixed order.
Run from research/findings:  python3 figures_projection_2026-09-06.py
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "data/projection"
FIG = ROOT / "figures"
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]   # slots 1 to 5, fixed order
TXT, TXT2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": TXT2, "xtick.color": TXT2, "ytick.color": TXT2,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True})

ap = pd.read_csv(P / "approvals_projection.csv")
bc = ap[(ap["block"] == "backcast calibrated") & (ap["class"] == "five projected classes") & (ap["year"].astype(str).str.isdigit())].copy()
bc["year"] = bc["year"].astype(int)
fc = ap[(ap["block"] == "forecast") & (ap["class"] == "all genetic")].copy()
fc["year"] = fc["year"].astype(int)
fig, ax = plt.subplots(figsize=(8, 4), dpi=200)
ax.fill_between(bc["year"], bc["p10"], bc["p90"], color=C[0], alpha=0.15, linewidth=0)
ax.plot(bc["year"], bc["p50"], color=C[0], linewidth=2, label="model median (backcast from the 2019 pipeline)")
ax.plot(bc["year"], bc["realised"], color=TXT, linewidth=0, marker="o", markersize=5, label="realised first approvals, five classes")
ax.fill_between(fc["year"], fc["p10"], fc["p90"], color=C[1], alpha=0.15, linewidth=0, label="10th to 90th percentile")
ax.plot(fc["year"], fc["p50"], color=C[1], linewidth=2, label="forecast median, all genetic products")
ax.axvline(2026, color=GRID, linewidth=1)
ax.text(2026.1, ax.get_ylim()[1] * 0.95, "today", color=TXT2, fontsize=8)
ax.set_ylabel("first approvals per year (FDA or EMA)")
ax.set_title("Genetic therapy approvals: backcast against the record, then forward", loc="left", color=TXT, fontsize=11)
ax.legend(frameon=False, fontsize=8, loc="upper right")
ax.set_xticks(list(range(2020, 2037, 2)))
fig.tight_layout(); fig.savefig(FIG / "Figure_P1_approvals_projection.png"); plt.close(fig)

pt = pd.read_csv(P / "patients_projection.csv")
base = pt[pt["scenario"] == "baseline"]
classes = ["CAR-T", "AAV", "lentiviral ex vivo", "CRISPR ex vivo", "in vivo editing and LNP"]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=200, gridspec_kw={"width_ratios": [1.3, 1]})
ax = axes[0]
w = base[base["region"] == "worldwide"]
years = sorted(w["year"].unique())
bottom = pd.Series(0.0, index=years)
for k, c in enumerate(classes):
    v = w[w["class"] == c].set_index("year")["patients_p50"].reindex(years).fillna(0)
    ax.bar(years, v, bottom=bottom, color=C[k], width=0.8, label=c, linewidth=0)
    bottom = bottom + v
allc = w[w["class"] == "all classes"].set_index("year").reindex(years)
ax.errorbar(years, allc["patients_p50"], yerr=[allc["patients_p50"] - allc["patients_p10"], allc["patients_p90"] - allc["patients_p50"]], fmt="none", ecolor=TXT2, elinewidth=1, capsize=2, label="all classes, 10th to 90th")
ax.set_title("Patients treated per year, worldwide, baseline median by class", loc="left", color=TXT, fontsize=11)
ax.set_ylabel("patients per year (revenue-derived basis)")
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax = axes[1]
for k, region in enumerate(["US", "Europe", "rest of world"]):
    r = base[(base["region"] == region) & (base["class"] == "all classes")].set_index("year").reindex(years)
    ax.plot(years, r["patients_p50"], color=C[k], linewidth=2, label=region)
    ax.fill_between(years, r["patients_p10"], r["patients_p90"], color=C[k], alpha=0.12, linewidth=0)
ax.set_title("By region, all classes (median and band)", loc="left", color=TXT, fontsize=11)
ax.legend(frameon=False, fontsize=8, loc="upper left")
for a in axes:
    a.set_xticks(list(range(2027, 2037, 3)))
fig.tight_layout(); fig.savefig(FIG / "Figure_P2_patients_projection.png"); plt.close(fig)
print("figures written")
