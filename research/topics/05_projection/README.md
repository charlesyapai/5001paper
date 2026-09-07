# 05 · Projection

## Scope
Expected year of first approval, first reimbursement and half penetration for the frontier
platforms, with ranges, under current and reformed architectures; the backcast against AAV and
CAR-T; and the comparison of the field's earlier forecasts with the realized record.

## Questions
- When do base editing, prime editing, epigenome editing and in vivo LNP programs reach patients at scale under measured stage durations?
- How many years does compressing the access stage or the uptake stage save?
- By how much did the 2021 demand projections overshoot, and which stage explains the gap?

## What we know
- Prior projections exist for the US (2021) and France (2024) and were built on demand and pipeline, not on measured access-stage durations (F015, provisional).
- Frontier pipeline counts are in hand (topic 01).

- Projected series extracted: NEWDIGS 2020 cumulative US approvals (62.4 by 2030), S17 France launches and newly treated patients 2023 to 2030, Tufts 2023 US patients treated per year to 2036; S16 abstract only (63.5 approvals by 2030, 93,000 patients in 2030). The approvals forecast tracks the record (13.0 vs 13 in 2022; 31.9 vs 28 to 33 in 2025); the patients forecast runs ahead of it (F033).

- Landscape projection to 2036 (F044, D013): 54 (46 to 63) genetic-product approvals 2027 to 2036, front-loaded 2028 to 2030 then falling to 2 to 3 a year as the phase-2 stock clears; the calibrated backcast reproduces the 2020 to 2025 record after halving the registry-implied rate for CAR-T and AAV. Patients treated rise from about 17,000 a year worldwide to 25,000 (17,000 to 42,000) in 2031 and 37,000 (22,000 to 66,000) in 2036, four fifths of them CAR-T; compressing access lags adds 3 percent; centre capacity keeps pace only if centre growth continues at 12 percent a year.

- Projection version 2 (D014; F048 to F050). Pipeline at construct level with four units backcast: only one lead programme per sponsor and class among constructs with a US or European site reproduces the 2020 to 2025 record without calibration (18, 13 to 23, against 16). Bass diffusion with per-product parameters and leave-one-out checks: a class curve predicts a held-out one-time therapy within a factor of two to three only. Forecast: 63 (54 to 73) genetic approvals 2027 to 2036; patients treated 31,800 (20,800 to 50,000) in 2031 and 48,900 (28,900 to 79,800) in 2036 worldwide, CAR-T seven eighths; the eligible flow of newly opened CAR-T diseases is the assumption that moves the answer most; US centre capacity binds at the US accreditation trend. Tables and sensitivity under `data/projection/`; figures P1 to P4.

## Sources
S16, S17, S20; layers 01 to 04.

## Method
`research/methods/projection_model.md`.

## Tasks
1. Month 1: extract the projected series from S16 and S17. **Done 2026-09-04 (F033); S16 full text still paywalled.**
2. Month 4: build the Monte Carlo; run the backcast; run scenarios; produce figures 6 and 7. **Class-level version done 2026-09-06 (F044) and rebuilt 2026-09-07 with a validated pipeline unit, measured durations, cumulative-incidence funding, Bass diffusion and sensitivity (F050; Figures P1 to P4); the per-platform frontier milestone table with donor mapping remains.**

## Open questions
- Which mature class is the right donor of stage durations for each frontier platform. Proposal in the method file; to be argued in the paper.
