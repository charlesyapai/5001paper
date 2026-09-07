# Governance and blockers by region

*How each health system decides whether to pay for a gene or cell therapy, how long it takes, and what it says when
it says no. Tables: `data/access/governance_by_region.csv`, `stated_reasons.csv`, `decisions.csv`; findings F043 and
F045. The regional sections for the United States, Singapore and China draw on their own source tables
(`data/access/raw/governance_{us,singapore,china}.csv`). The funded shares are cumulative incidence at five years from authorisation with every authorised product at risk and refusals and withdrawals as competing events (F047; Figure P4 in the landscape page).*

## The pattern in one table

| System | Bodies | Months from authorisation to funding, among funded products (median) | Share of authorised products funded within five years (routine listing only) | What the refusals and conditions say |
|---|---|---|---|---|
| Germany | G-BA benefit assessment, negotiated reimbursement amount | 9.9 | 0.83 | Added benefit "not quantifiable" for almost every first resolution; evidence and comparator language in three quarters of rows; price in half; the only system that states an eligible count almost every time |
| United States | Medicare coverage rules, Medicaid, commercial payers; no single decision | 4.4 to first revenue | 1.00 of products with public sales | Payment settled product by product; coverage restrictions rather than refusals (regional section below) |
| Italy | AIFA determination in the Gazzetta Ufficiale | 17.4 | 0.70 | Price in four fifths of rows; managed-entry agreements (payment at or by result, capping, registries) in 87 percent; innovativeness often conditional |
| France | HAS opinion, early access, JO listing, CEPS price | 5.2 with early access, 23.4 without | 0.48 (0.36) | Population restriction and comparator or evidence in two thirds of rows; no cost-effectiveness language in the opinion; early access gives patients the product before the price exists |
| England | NICE appraisal, Cancer Drugs Fund, managed access | 9.4 | 0.53 (0.40) | Cost-effectiveness in two thirds of rows; a third of first appraisals terminated because the company did not submit; managed access for CAR-T |
| Australia | MSAC or PBAC advice, then funding | 3.7 to committee support | 0.88 (eight products) | Price, cost-effectiveness and restriction in equal measure; nine deferrals before support; committee runs alongside registration |
| Canada | CADTH or CDA-AMC recommendation, then pCPA negotiation | 23.0 to a negotiated letter | 0.42 | Reimburse with conditions in ten of eleven first recommendations; price reductions of 10 to 99 percent demanded; two negotiations closed without agreement |

Read across the columns and three different kinds of system appear.

**Systems that fund nearly everything and argue about evidence and price afterwards.** Germany funds from launch and
lets the benefit assessment set the price; the friction shows up as "not quantifiable" ratings, data-collection
requirements and negotiated prices that fall at re-assessment (Kymriah from 320,000 to 239,000 euros). Italy funds most
products but wraps them in outcomes-based contracts and registries, and takes a year and a half to do it.

**Systems that gate on value and let half of products fall out.** Counting every authorised product, including the ones never submitted, England and France fund about half within five years and Canada two fifths. England's appraisal decides whether the product
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

The United States has no funding decision. Products are sold from approval (median 4.7 months to first revenue),
and the questions the other systems settle in one committee are settled payer by payer and hospital by hospital.
Three mechanisms carry the weight. Medicare covers CAR-T under a 2019 national coverage determination and pays
inpatient cases through a dedicated diagnosis-related group created in 2021, whose relative weight rose from 36.1 in
fiscal 2023 to 45.1 in fiscal 2027, topped up by new-technology add-on payments that are granted product by product
and expire (Kymriah and Yescarta 186,500 then 242,450 dollars in 2019 and 2020; Casgevy 1.65 million and Lyfgenia
2.33 million in fiscal 2025; Zevaskyn 2.05 million in fiscal 2027; Breyanzi refused once, Aucatzyl ruled not new).
Medicaid, the payer for most sickle cell patients, was given a federal outcomes-based purchasing model in 2024 that 33
states plus the District of Columbia and Puerto Rico had joined by July 2025, covering about 84 percent of Medicaid
sickle cell beneficiaries, after a 2022 rule allowed manufacturers to report several "best prices" for value-based
contracts. Commercial coverage is negotiated by sponsors: Krystal reports 97 percent of commercial lives covered for
Vyjuvek, Vertex about 90 percent of United States patients with reimbursed access to Casgevy by the end of 2025,
Autolus more than 90 percent of covered lives for Aucatzyl, and bluebird outcomes-based agreements covering about 200
million lives.

The friction shows up as time and travel rather than refusal. Published surveys find commercial prior authorisation
for CAR-T taking 62 days against 32 for Medicare, a quarter of patients requiring single-case agreements, state
Medicaid restriction rates of 54 to 68 percent, and a median 104 miles to a treatment centre for patients who go
untreated against 34 for those treated. Capacity is the visible constraint: Yescarta opened with 16 certified centres
in 2017 and had more than 150 by 2026, Kymriah 25 in 2018, Carvykti more than 140 with a stated 10,000-dose annual
capacity target for 2025 after slot rationing in 2023, Casgevy 12 United States centres at launch in 2024 against a
goal of about 50, bluebird's network growing from 27 to more than 70 qualified centres between December 2023 and
November 2024, and 171 FACT-accredited immune effector cell programmes in all. Vein-to-vein times fell from 17 to 14
days for Yescarta and stand at 70 to 105 days for bluebird's manufacturing.

The blocker pattern is therefore a distributed one: no gate refuses a product, but every product must build its own
network of certified hospitals, its own payer contracts and its own add-on payment, and the patients who fall out are
those far from a centre or behind a slow authorisation. Sources and per-row status:
`data/access/raw/governance_us.csv` (122 rows, 112 verified, mostly Federal Register texts and sponsor filings).

### Singapore

Singapore built a dedicated regulatory class and a dedicated funding list, and used both slowly and selectively.
The Health Sciences Authority's cell, tissue and gene therapy framework came into force on 1 March 2021; Kymriah was
approved eight days later as the first commercial CAR-T in Southeast Asia, Yescarta in March 2023, and five class-2
products (including Zolgensma and Luxturna) were registered by April 2024. Elevidys is supplied unregistered under
the Special Access Route. Funding followed a separate, later track: the Ministry of Health's CTGTP List opened on 1
August 2024 with Kymriah as its only product, 41 months after registration, with a means-tested subsidy of up to 75
percent capped at 150,000 Singapore dollars per course; MediShield Life and MediSave coverage (a claim limit of
141,000 dollars) began in October 2025. Yescarta was refused in July 2024 on an "unacceptable pricing proposal",
reversed in November 2024 after a revised price, and listed for second-line use from April 2025 and third-line from
August 2025. Zolgensma was refused for the list in September 2025 after a cost comparison with risdiplam, for about
three babies a year; families have crowdfunded the 2.4 million dollar price. The Rare Disease Fund can pay for
CTGTPs case by case and had supported eight patients by November 2023, none of them a cohort gene therapy.

Delivery is concentrated: Singapore General Hospital was the sole centre reporting CAR-T to the EBMT survey in 2024,
with 12 patients, about 2 per million residents against 17 in Germany. The National University Hospital has run an
in-house CD7 CAR-T programme since 2019 (17 patients) and KK Women's and Children's Hospital a point-of-care CD19
CAR-T trial since 2022; ACTRIS, the national manufacturing centre, was established in 2020 and launched in 2023.
The ministry's own estimate of 20 to 30 patients a year who could benefit from Yescarta sets the scale.

The blocker pattern is therefore not the regulator, which moved early, nor the hospitals, which manufacture their own
constructs, but the value gate: one committee (the Drug Advisory Committee, on Agency for Care Effectiveness
evaluations, with a Health Technology Advisory Council for high-cost cases) deciding product by product, with price
the stated reason both times a product was refused. Sources and per-row status: `data/access/raw/governance_singapore.csv`
(95 rows, 44 verified; HSA's product database is a web application whose listing dates could not be read directly).

### China

China approved quickly, built the widest hospital network, and left payment to insurers outside the state scheme.
The regulator treated cell therapies as drugs from the December 2017 guideline and has approved eight CAR-Ts since
June 2021: Fosun Kite's licensed axicabtagene ciloleucel (Yikaida, 22 June 2021), JW's relmacabtagene autoleucel
(September 2021), IASO's equecabtagene autoleucel and Juventas's inaticabtagene autoleucel (2023), CARsgen's
zevorcabtagene autoleucel (March 2024), Legend's ciltacabtagene autoleucel (August 2024, a Chinese-origin construct
approved in the United States two years earlier), and in June 2026 the first CAR-T for a solid tumour, CARsgen's
satricabtagene autoleucel for Claudin18.2-positive gastric cancer. China's first haemophilia B gene therapy (BBM-H901,
Belief BioMed with Takeda) followed in April 2025. Registered CAR-T trials in China outnumber those in the United States
for leukaemia and lymphoma.

Payment is the blocker, and it has taken an unusual form. Launch prices were 1.2 million yuan for Yikaida, 1.29
million for Carteyva and 1.17 million for Fucaso; domestic products launched later priced near 1 million. No CAR-T has
entered the basic National Reimbursement Drug List in any round from 2021 to 2025 (Yikaida applied in July 2023 and July
2024 and was not admitted). Instead, coverage came through city supplementary schemes (Huiminbao) and commercial
policies: Yikaida was in more than 110 city schemes and 80 commercial products by the end of 2024, and Shanghai's
Huhuibao names three CAR-Ts in its claims guide. In December 2025 the National Healthcare Security Administration
created a second list, the Commercial Health Insurance Innovative Drug List, and placed all five domestically marketed
CAR-Ts on it (Carvykti excluded), valid from January 2026 to December 2027. The state has thus formalised a two-tier
architecture: the basic list will not carry a million-yuan therapy, and a parallel list signals to private insurers what
they should.

Delivery scaled fastest of any system: more than 180 registered treatment centres across 28 provinces for Yikaida alone
by the end of 2024, against 160 in the whole United States, yet cumulative treated patients were about 800 for Yikaida
after three and a half years, so the network is broad and thin. Sources and per-row status:
`data/access/raw/governance_china.csv` (111 rows, 40 verified; nmpa.gov.cn and cde.org.cn block direct fetches, so
approval dates come from sponsor filings and the NHSA notices).
