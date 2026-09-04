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

**Caveats.** Revenue recognition timing can lag infusion; ex-US pricing is often confidential;
outcomes-based rebates reduce net price after the fact; single-quarter counts for ultra-rare
products are noisy and should be shown cumulatively.

**Output.** `data/uptake/patients_quarterly.csv`: product, region, quarter, revenue, currency,
list_price, gross_to_net, patients_low, patients_central, cumulative_low, cumulative_central,
source_doc, notes.
