# 04 · Investment and sponsor commitment

## Scope
Sponsor commitment intervals, retreat and exit events after approval, sector financing by year,
acquisitions and licensing deals coded by manufacturing model, and the years of capital each
stage duration implies for each technology class.

## Questions
- How long do sponsors stay on a platform, and does that track the launch record?
- Which approved products were shelved, sold or exited, and when relative to their uptake curve?
- Did capital rotate from ex vivo autologous toward in vivo platforms as the 2022 to 2025 launch record arrived?
- How many years of capital does each class need from first-in-human to first revenue and to half penetration?

## What we know
- Six retreat cases are documented in `data/derived/commercial_retreat_cases.csv`; four are haemophilia (F011).
- Sponsor exit rates per platform exist in `data/derived/sponsor_exit_rates.csv` but disagree with the stated-reason measure; the interval-based measure in OPEN_ITEMS item 4 is the replacement.
- The stated-reason field never names a payer or a price, so investment signals must come from disclosures, not the registry (README, instrument limits).

## Sources
Company disclosures and trade press; S26 for financing totals; deal announcements; `trial_records.csv` for commitment intervals.

## Method
Sponsor survival on first-to-last trial interval; event table by year and manufacturing model; transparent time-to-revenue calculation per class per scenario. No valuation model. See `research/methods/projection_model.md` for the capital-horizon output.

## Tasks
1. Month 1: extend the retreat-case file to a systematic `data/investment/events.csv` covering every cohort product and every named exit since 2017; verify each against a primary disclosure.
2. Month 2: deal table for approved and late-stage products coded by manufacturing model; verify each.
3. Month 2: sector financing by year from S26.
4. Month 3: sponsor survival from `trial_records.csv`.

## Open questions
- How to date an exit when a program is quietly deprioritised rather than announced. Proposal: date of last trial start plus the sponsor's own disclosure where one exists.
