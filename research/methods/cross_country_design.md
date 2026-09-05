# Same product, different systems

**Purpose.** Hold the technology constant and let the architecture vary. The strongest
identification available to the flagship.

**Unit.** Product by country by year. Primary product class: CD19 and BCMA CAR-T, because
registries publish infusion counts by country. Secondary: gene therapies with country-level
reimbursement dates, where uptake is binary access rather than counts.

**Outcome.** CAR-T infusions per million population and per estimated eligible patients, by
country and year.

**Eligible denominator.** Annual incident cases of the covered indications from national cancer
registries or GLOBOCAN, times the share reaching the covered line of therapy from published
treatment-pattern studies, as a range.

**Covariates.** Reimbursement lag from approval; arrangement type; number of qualified centres per
million; inpatient or outpatient delivery; price where public; health spending per capita.

**Model.** Panel regression of log per-eligible uptake on covariates with product and year fixed
effects; country random effects as a sensitivity. Report per-capita and per-eligible results side
by side (convention 10).

**Countries.** United States, Germany, France, United Kingdom, Italy, Spain; Japan and Australia
if their registries publish counts.

**Caveats.** Registry completeness differs by country; use the registries' own coverage estimates
to bound it. Cross-border treatment is small for CAR-T but not zero.

**Output.** `data/uptake/cart_by_country.csv`: country, year, product_or_class, infusions,
population, eligible_low, eligible_high, reimbursement_date, centres, delivery_setting,
source.


**Implementation, 5 September 2026 (F041).** `research/findings/build_cart_by_country_2026-09-05.py` merges the
registry counts (`data/uptake/raw/cart_registry_counts.csv`, `cart_country_supplement.csv`), World Bank populations
(`raw/country_population.csv`) and the per-indication eligible ranges into `data/uptake/cart_by_country.csv`, one row per
country, year and registry, with patients per million and per 100 eligible (range). The country eligible flow sums the
diseases the approved CAR-Ts treat, each ranged across products and lines. Rows with an EBMT published rate but no count
carry the rate only. Reimbursement dates and centre counts join from `data/access/decisions.csv` and the centre rows of
the supplement in the next pass.
