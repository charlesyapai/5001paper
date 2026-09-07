# Revenue to patients

**Measures.** Patients treated per quarter for each approved product with public sales.

**Unit.** Product by quarter, by region where sales are reported by region.

**Inputs.** Quarterly product revenue from filings and earnings releases; list price per treatment
by region and date; disclosed patient counts wherever a company states them; gross-to-net
assumptions where public.

**Procedure.**
1. Record revenue as reported, in reporting currency, with the document and page.
2. Record list price per treatment course at the date, with source. For multi-dose products, price per full course.
3. Patients = revenue / net price, where net price = list price × (1 − gross-to-net). Default gross-to-net: 0 for a lower bound on patients, and a stated assumption for the central estimate.
4. Calibrate on products with disclosed cumulative patient counts. Choose the gross-to-net that reconciles the cumulative revenue-derived count with the disclosed count; report it; apply class-level defaults to products without disclosures.
5. Report each quarter's estimate as a range: lower bound at list price, central at calibrated net price.
6. Aggregate to cumulative patients; join to the eligible-population range to give penetration as a range.

**Calibration protocol.** Pilot products: Zolgensma, Yescarta, Hemgenix, Casgevy, Luxturna.
Gate: cumulative revenue-derived count within about thirty percent of the disclosed count. If
the gate fails for the pilots, the uptake layer falls back to registry counts for CAR-T and
reimbursement timing for the rest, with revenue-derived counts kept as supplementary.

**Calibration result, 4 September 2026 (F024).** On 17 dated disclosure points across the five pilot
products, cumulative revenue at US list price recovers 63 to 86 percent of the disclosed count
(per-product medians: Casgevy 0.83, Luxturna 0.85, Yescarta plus Tecartus 0.80, Hemgenix 0.72,
Zolgensma 0.67). A single class factor of 0.76 brings every point within the 30 percent gate and 15
of 17 within 15 percent. **Gate passed.** Default for products without disclosures: net price = 0.76
of US list, with the list-price count as the lower bound. Script:
`research/findings/calibrate_revenue_to_patients_2026-09-04.py`; tables under `data/uptake/`.

**Caveats.** Revenue recognition timing can lag infusion; ex-US pricing is often confidential;
outcomes-based rebates reduce net price after the fact; single-quarter counts for ultra-rare
products are noisy and should be shown cumulatively.

**Known series limits (F023).** Novartis, Vertex and CSL give no US versus ex-US split. CSL breaks Hemgenix out only from FY2025. Roche did not break Luxturna out for 2020 to 2022. Kite patient milestones pool Yescarta and Tecartus. Novartis Zolgensma counts include trial and managed-access doses.

**US net price is list price for CAR-T (F030, 5 September 2026).** Medicare Part B ASP payment limits
divided by 1.06 equal the wholesale acquisition cost in force two quarters earlier for Yescarta and
Tecartus (median ratio 1.00, range 0.92 to 1.06 over 14 quarterly files each). The shortfall in the
calibration (F024) therefore comes from list-price increases after launch and lower ex-US prices, not
from US rebates. Eighteen coded gene therapies have never had a CMS payment limit and are paid by
invoice or WAC, so no public net price exists for them. Series: `data/uptake/net_price_asp.csv`,
script `research/findings/net_price_asp_2026-09-05.py`.

**Series builder (5 September 2026).** `research/findings/build_uptake_series_2026-09-04.py` reads every
`data/uptake/raw/<product>_revenue.csv`, keeps the finest non-overlapping set of reported periods per
region group (Total, US, Europe), derives the remainder of an annual or half-year figure after
subtracting the finer periods it overlaps, allocates longer periods evenly across their quarters
(flagged), and prices each quarter at the US launch list price per course (lower bound) and at 0.76 of
it (central). Per-unit prices are multiplied by the units per course (Luxturna 2 eyes, Ryoncil 8
infusions, Provenge 3 infusions). Chronic therapies (Vyjuvek, Adstiladrin) yield patient-years at the
annual cost, not patients; course-based therapies (Provenge, Ryoncil, Imlygic) yield courses. Products
without a sourced or fallback US price carry revenue only.

**Output.** `data/uptake/patients_quarterly.csv`: product, region (Total, US, Europe), quarter, regimen,
revenue_usd_m, period_as_reported, revenue_status, allocated, list_price_usd, class_factor,
patients_low, patients_central, cumulative_low, cumulative_central, coverage, source_doc, source_url.
`data/uptake/uptake_summary.csv`: one row per product with approval dates, first-revenue quarter,
months from approval to first revenue, quarters observed, cumulative revenue and patients, the US
and Europe cumulative counts where a split exists, and the latest disclosed patient count.


**Net-price variant, 5 September 2026 (F040).** `research/findings/net_price_variant_2026-09-05.py` prices US
revenue of the five CAR-Ts with a CMS ASP series at the price in force each quarter (implied ASP, else the
year's WAC from the disclosure tables, else launch list) with no factor, and ex-US revenue at launch list
times 0.76. It writes `data/uptake/patients_quarterly_variant.csv`, `net_price_variant_summary.csv` and
`net_price_variant_checks.csv`. The variant recovers 81 to 90 percent of Kite's disclosed cumulative
floors where the class-factor series recovers 103 to 110 percent, so the class factor remains the primary
series (D011). The variant is kept as a sensitivity bound.

**Ex-US price series, 7 September 2026 (F051).** `research/findings/ex_us_price_variant_2026-09-07.py` assembles the
public ex-US prices in the access tables (G-BA annual therapy cost, CEPS tarif, NICE and AIFA list prices) into
`data/uptake/ex_us_price_series.csv` at ECB annual reference rates and reprices the Europe revenue of the five CAR-Ts
with a Europe split at the German price in force (`patients_quarterly_exus_variant.csv`). The German negotiated price
settles at 0.55 to 0.82 of the US launch list for CAR-T, and the repriced Europe counts sit within 12 percent of the
class-factor counts, which supports keeping the 0.76 factor (D011) while giving every product with a German or French
price a product-level ex-US alternative.
