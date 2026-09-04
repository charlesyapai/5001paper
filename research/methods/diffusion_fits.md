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
