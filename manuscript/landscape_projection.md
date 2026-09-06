# The landscape to 2036

*What the measured record implies for gene and cell therapy approvals, funded access, patients treated and hospital
capacity over the next ten years. Model and tables: `data/projection/`, decision D013, finding F044.*

## The question

Forecasts made in 2020 and 2021 got the number of approvals right and the number of patients wrong. They projected
demand from the pipeline and skipped the two stages that sit between approval and treatment: the funding decision in
each health system, and the slow diffusion of a one-time therapy through hospitals, referral networks and eligible
patients. This projection chains all three stages, each measured on the 43 products approved so far, and is run
backwards over 2020 to 2025 before it is run forwards.

## How the model works

1. **Approvals.** Every industry programme in the trial registry is placed at its highest active phase (CAR-T 60, 59
   and 14 programmes at phases 1, 2 and 3; AAV 13, 37 and 19; lentiviral 8, 10 and 4; CRISPR 5, 6 and 2; in vivo
   editing and LNP 6, 7 and 0). Each survives the remaining phases at the published rates for its class and, if it
   succeeds, reaches approval after a clinical stage drawn from the measured distribution for that class (median
   6.4 years for CAR-T, 6.9 for AAV, 10.5 for lentiviral). New programmes enter phase 1 at the 2021 to 2025 rate.
2. **Backcast and calibration.** Run from the pipeline as it stood at the end of 2019, the raw model predicts 30
   approvals in the five classes for 2020 to 2025; the record is 16. The registry counts programmes that never seek
   FDA or EMA approval, so a class factor (CAR-T 0.45, AAV 0.50, lentiviral 1.0) is applied and reported. With it,
   the backcast gives 16 (range 12 to 21) and every year falls inside the band.
3. **Funded access.** Each approval draws the lag to the first positive funding decision in each of seven systems
   from the measured lags, and clears it with that system's observed probability (Germany 0.91 of approvals,
   Italy 0.84, United States 0.82, Australia 0.70, France 0.67, Canada 0.64, England 0.57).
4. **Patients.** CAR-T is projected as a class: penetration of the eligible flow follows the curve fitted to seven
   products, anchored on the 2024 registry totals (5,266 in the United States, 6,082 in Europe); a quarter of new
   CAR-T approvals are assumed to open a new disease with its own eligible pool. One-time gene therapies are
   projected product by product: each new approval draws an eligible pool from the observed range and follows the
   class curve, whose early slope (6 percent of the pool per year) is identified while its ceiling is not.
5. **Capacity.** CAR-T demand is set against qualified centres growing at the observed 12 percent a year and the
   observed patients per centre (22 across Europe, 37 in Germany).

Every parameter, with its source, is in `data/projection/projection_parameters.csv`.

## What it says

![Figure P1](../figures/Figure_P1_approvals_projection.png)

**Approvals come in a bulge, then a trough.** The median path is 54 first approvals of genetic products between
2027 and 2036 (range 46 to 63): 17 CAR-T, 15 AAV, 8 lentiviral, 2 CRISPR, 2 in vivo, and about 10 from other vectors
at the historical rate. Ten a year arrive in 2028 and 2029 as today's large phase-2 stock clears, falling to two or
three a year by 2033 unless phase-1 entry rises. The frontier is small in this window: programmes entering phase 1
now reach approval, if they do, after 2033.

![Figure P2](../figures/Figure_P2_patients_projection.png)

**Patients treated roughly double by 2036, and CAR-T stays four fifths of the total.** Worldwide, about 17,000
patients a year today become 25,000 in 2031 (range 17,000 to 42,000) and 37,000 in 2036 (22,000 to 66,000). In the
United States the model reaches 11,000 a year across all classes by 2031, the figure that the 2023 Tufts projection
placed in 2024. CAR-T grows from 5,300 to 11,600 a year in the United States and from 6,100 to 14,800 in Europe.
One-time gene therapies together reach about 2,000 a year in the United States and 1,700 in Europe by 2036: AAV
1,400 and 700, lentiviral 1,100 and 540, CRISPR 500 and 250, in vivo editing 480 and 230.

**Funded access widens unevenly.** Products with a positive funding decision rise from 26 to about 60 in the United
States by 2036, 21 to 59 in Germany, 16 to 51 in Italy, 13 to 41 in France, 13 to 37 in England, 8 to 37 in
Australia and 7 to 33 in Canada. The gap between systems is set less by how long a decision takes than by how many
approvals ever get one.

**Faster decisions add little volume; capacity binds only if hospitals stop joining.** Compressing every system's
funding lag to the best observed adds 3 percent to patients treated by 2036. CAR-T demand of 11,600 a year in the
United States in 2036 needs 315 to 530 treatment centres at observed throughputs; the network of about 160 today
reaches 500 if it keeps growing at the European rate, but frozen at today's size it caps United States volume near
6,000 a year at German throughput and 3,500 at the European average. Europe's 278 reporting centres cover the
projected demand with room to spare at trend.

## Assumptions that move the answer

- The programme proxy (one per sponsor per platform) and the calibration that corrects it; a sharper pipeline
  count by construct would replace both.
- The share of CAR-T approvals that open a new disease (0.25) and the eligible flows of those diseases.
- The CAR-T ceiling (fitted at 92 percent of the eligible flow) and the one-time therapy ceiling (not identified).
- The Europe to United States population ratio (1.5) and the Europe share of ex-US patients (0.75).
- Prices and revenue: patient counts on the revenue basis carry the class net-to-list factor (F024, F040).

## What would change the picture

A rise in phase-1 entry from 2025 onward lifts the trough after 2033. In vivo delivery that removes the centre and
apheresis constraint would change the CAR-T curve, not the approval count, within this window. A system that funds
a larger share of approvals (Germany's 0.91 against England's 0.57) matters more for its patients than one that
decides faster.
