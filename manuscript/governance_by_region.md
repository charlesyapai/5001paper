# Governance and blockers by region

*How each health system decides whether to pay for a gene or cell therapy, how long it takes, and what it says when
it says no. Tables: `data/access/governance_by_region.csv`, `stated_reasons.csv`, `decisions.csv`; findings F043 and
F045. The regional sections for the United States, Singapore and China are being assembled from their own source
tables and appear below as they are verified.*

## The pattern in one table

| System | Bodies | Months from authorisation to a funding decision (median) | Share of approvals ever funded | What the refusals and conditions say |
|---|---|---|---|---|
| Germany | G-BA benefit assessment, negotiated reimbursement amount | 9.8 | 0.91 | Added benefit "not quantifiable" for almost every first resolution; evidence and comparator language in three quarters of rows; price in half; the only system that states an eligible count almost every time |
| United States | Medicare coverage rules, Medicaid, commercial payers; no single decision | 4.7 to first revenue | 0.82 | Payment settled product by product; coverage restrictions rather than refusals (regional section below) |
| Italy | AIFA determination in the Gazzetta Ufficiale | 17.4 | 0.84 | Price in four fifths of rows; managed-entry agreements (payment at or by result, capping, registries) in 87 percent; innovativeness often conditional |
| France | HAS opinion, early access, JO listing, CEPS price | 5.2 with early access, 23.4 without | 0.67 | Population restriction and comparator or evidence in two thirds of rows; no cost-effectiveness language in the opinion; early access gives patients the product before the price exists |
| England | NICE appraisal, Cancer Drugs Fund, managed access | 9.4 | 0.57 | Cost-effectiveness in two thirds of rows; a third of first appraisals terminated because the company did not submit; managed access for CAR-T |
| Australia | MSAC or PBAC advice, then funding | 3.7 to committee support | 0.70 | Price, cost-effectiveness and restriction in equal measure; nine deferrals before support; committee runs alongside registration |
| Canada | CADTH or CDA-AMC recommendation, then pCPA negotiation | 21.0 to a negotiated letter | 0.64 | Reimburse with conditions in ten of eleven first recommendations; price reductions of 10 to 99 percent demanded; two negotiations closed without agreement |

Read across the columns and three different kinds of system appear.

**Systems that fund nearly everything and argue about evidence and price afterwards.** Germany funds from launch and
lets the benefit assessment set the price; the friction shows up as "not quantifiable" ratings, data-collection
requirements and negotiated prices that fall at re-assessment (Kymriah from 320,000 to 239,000 euros). Italy funds most
products but wraps them in outcomes-based contracts and registries, and takes a year and a half to do it.

**Systems that gate on value and let a third of products fall out.** England's appraisal decides whether the product
enters at all; the products that never reach NICE (Abecma, Carvykti, the bluebird therapies) are the blocker, not the
appraisal time. Canada's committee is fast but the negotiation that follows takes two years and fails outright for some
products (Carvykti, Beqvez).

**Systems with an early door.** France's early-access route and Australia's parallel committee review put patients on
therapy within months, with the price argument deferred. France's ordinary route, without early access, is the slowest
of the six.

## What the stated reasons show

Keyword coding of the committees' own words (294 rows, four languages; the schema is in the script header and a human
validation sample is still to be coded):

| Category | England | Germany | France | Italy | Canada | Australia |
|---|---|---|---|---|---|---|
| Uncertainty about durability or immature data | 19 | 27 | 18 | 2 | 14 | 16 |
| Cost-effectiveness | 26 | 0 | 0 | 0 | 14 | 18 |
| Comparator or evidence quality | 2 | 49 | 54 | 2 | 3 | 3 |
| Price | 20 | 32 | 11 | 24 | 19 | 19 |
| Population or restriction | 22 | 4 | 55 | 5 | 6 | 18 |
| Budget impact | 1 | 0 | 0 | 1 | 9 | 3 |
| Capacity or delivery | 0 | 0 | 4 | 0 | 2 | 1 |
| No reason stated | 8 | 9 | 22 | 4 | 12 | 13 |

Durability uncertainty is universal. Beyond it, each system argues in the vocabulary its law gives it: cost per
quality-adjusted life year in England, Canada and Australia; added benefit against a named comparator in Germany and
France; price in Italy. Capacity is almost never named in a funding document, even where it binds (see the landscape
projection).

## Regional sections

### United States
*In retrieval: Medicare coverage determination and payment rules, the Medicaid Cell and Gene Therapy Access Model,
commercial coverage statements, treatment-centre counts and turnaround times.*

### Singapore
*In retrieval: HSA registrations, ACE guidance and MOH subsidy listings, MediShield Life coverage, delivering
hospitals and patient numbers, policy statements.*

### China
*In retrieval: NMPA approvals of imported and domestic CAR-T and gene therapies, launch prices and cuts, National
Reimbursement Drug List outcomes, city insurance coverage, centres and treated patients.*
