# Uptake layer tables

Built 4 to 5 September 2026 by the scripts in `research/findings/` from the raw agent tables in `raw/`.

| File | Content | Finding |
|---|---|---|
| `raw/<product>_revenue.csv`, `raw/<product>_disclosures.csv` | Every revenue row and every price, patient and centre statement retrieved per product, with URL and status | F023, F035 |
| `raw/eligible_E1a.csv` to `raw/eligible_E4.csv` | Eligible-population estimates per product, indication, geography and source | F034 |
| `raw/cms_asp_payment_limits.csv`, `raw/cms_asp_codes.csv` | Medicare ASP payment limits per HCPCS code per quarterly file; code confirmations | F030 |
| `raw/cart_registry_counts.csv` | CAR-T patients by registry, country and year | F036 |
| `raw/verification_hemgenix_tecartus.csv` | Primary-source checks for the Hemgenix stockout and the Tecartus price | F028, F029 |
| `pilot_revenue.csv`, `pilot_disclosures.csv`, `pilot_calibration.csv` | The six-product calibration pilot | F023 to F025 |
| `patients_quarterly.csv` | Patients per quarter at list price and at the class factor, by product and region (Total, US, Europe), with cumulative counts and coverage flags | F035 |
| `uptake_summary.csv` | One row per product: approvals, first-revenue quarter, lags, cumulative revenue and patients, price used, latest disclosed count | F035 |
| `net_price_asp.csv` | Implied ASP against list price by quarter | F030 |
| `eligible_population_rows.csv`, `eligible_population.csv`, `eligible_overrides.csv` | Normalised estimates; ranges per product, geography and family; the documented exclusions and reclassifications | F034 |
| `milestones.csv` | Clinical stage, first-revenue lag, eligible pool, penetration ranges, time to a quarter and half of the pool, H1 reading per product | F037 |
| `eligible_population_by_indication.csv` | Range per product, geography, family and indication key over verified and derived rows; input to the label-dated pools | F034, D012 |
| `label_events.csv` | Curated label events (initial indication, extensions, restrictions) per product and geography with the FDA or EC date and source; built from `raw/label_events.csv` | D012, F039 |
| `pool_quarterly.csv` | For label-dated products: indications in force, prevalent stock, day-weighted inflow and cumulative pool per quarter | D012, F039 |
| `raw/label_events.csv` | Agent table of label events with verbatim indication text and per-row URL and status | F039 |
| `cart_by_country.csv` | CAR-T patients by country, year and registry with patients per million (World Bank population) and per 100 eligible (range) | F041 |
| `raw/cart_country_supplement.csv`, `raw/country_population.csv` | EBMT 2024 country tables and 2018 to 2024 rates, DESCAR-T and national centre counts; World Bank populations 2017 to 2025 | F041 |
| `patients_quarterly_variant.csv`, `net_price_variant_summary.csv`, `net_price_variant_checks.csv` | Product-level net-price variant for the five CAR-Ts with an ASP series, and its check against disclosed counts | F040 |
| `raw/eligible_E5_label_expansions.csv` | Eligible-population rows for the populations added by label extensions | F034, F039 |

Conventions: every penetration is a range (low = lower-bound patients over upper-bound pool; high = central
patients over lower-bound pool); worldwide revenue divided by a US or US-plus-EU denominator is flagged in
the `flags` column; chronic therapies (Vyjuvek) are patient-years, course therapies (Provenge, Ryoncil) are
courses.

| `ex_us_price_series.csv`, `ex_us_price_summary.csv`, `patients_quarterly_exus_variant.csv` | Dated ex-US prices (Germany, France, England, Italy) at ECB annual rates with ratios to the US launch list; Europe CAR-T patients at the German price in force; built by `ex_us_price_variant_2026-09-07.py` | F051 |
| `raw/ecb_fx_annual.csv` | ECB annual average USD and GBP per EUR, 2010 to 2025 (fetched 2026-09-07) | F051 |
