# Diffusion fits

**Measures.** Speed and ceiling of uptake per product.

**Models.** Logistic curve for cumulative patients; Bass model where the series is long enough to
separate innovation and imitation parameters. Both fitted to cumulative central estimates with
the range propagated.

**Procedure.**
1. Fit only where at least eight quarters of data exist; otherwise report the raw series.
2. Report the fitted ceiling against the eligible-population range; a ceiling far below eligibility is a finding, not a fitting failure.
3. Report time to a quarter and half of the fitted ceiling and of the eligible range.
4. Compare parameters across classes and across systems for the same product.

**Caveats.** Short series make ceiling and speed trade off; report the confidence region, not a
point. Ultra-rare products can saturate their eligible pool within a few quarters, which is a
success and should be labelled as such.

**Output.** `data/uptake/fits.csv`: product, region, model, ceiling, ceiling_ci, speed,
speed_ci, t25, t50, quarters_used.

**Implementation, 7 September 2026 (F049).** `research/findings/fit_diffusion_2026-09-07.py` fits y = c F(t; p, q) with F the
Bass cumulative curve to penetration of the label-dated pool (cumulative over the prevalent pool for one-time therapies;
trailing four quarters over the annual flow for CAR-T), residuals on the log scale. Stage 1 pools each family; stage 2 fits
each product with a penalty toward the pooled p and q (0.5 log units) and c on (0.02, 1], an empirical-Bayes form of partial
pooling; the shrunk per-product tuples are the family's parameter distribution for the projection. Leave-one-product-out
checks predict each product from the other products' pooled curve and its own pool and report the log error at years 1 to 3
and coverage by the other products' spread. CAR-T as a class is fitted to the CIBMTR and EBMT annual totals with the ceiling
in patients and a residual bootstrap. Outputs `data/projection/diffusion_bass_fits.csv`, `diffusion_loo.csv`,
`diffusion_paths.csv`. The class curve predicts a held-out one-time therapy only within a factor of two to three; the
projection therefore draws per-product tuples rather than the pooled curve.
