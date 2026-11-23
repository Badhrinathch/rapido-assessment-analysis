# Rapido Data Science Assessment — Working

## Files
- `analysis.py` — end-to-end reproducible analysis from the seven raw CSVs.
- `funnel.csv` — onboarding funnel.
- `stage_impact.csv` — stage-drop recovery sizing.
- `segment_performance.csv` — segment approval rates.
- `airport_hourly_summary.csv` — airport hourly demand/supply summary.
- `airport_trip_return_summary.csv` — post-airport-trip outcomes.
- `memo.pdf` — executive memo (2 pages).
- `deck.pptx` — presentation deck (6 slides).

## Key framing choices
1. **Cohort:** January–May 2026 signups. June is excluded from conversion-rate conclusions because the extract ends June 30 and contains 1,297 `in_progress` signups; it is right-censored.
2. **A2O:** signup → approved, using signup as the denominator.
3. **Document order:** DL → RC → Aadhaar → Permit (Auto/Cab only) → Fitness → Insurance.
4. **Stage impact:** mature drops at a stage × downstream approval rate among captains reaching that stage, divided by five mature months.
5. **CAMP_WA_002:** observational analysis. The adjusted estimate controls for pre-treatment document progress plus signup attributes. It should **not** be described as causal without an experiment.
6. **Airport sizing:** extra concurrent peak online captains are estimated from observed fulfilled rides per captain-hour. This is a sizing assumption, not a causal capacity estimate.

## Headline numbers
- Mature A2O: **17.5%** (3532/20,207)
- Largest approval-leverage document leak: **Insurance**, with an estimated **418 approvals/month** if all mature Insurance-stage drops were recovered.
- CAMP_WA_002 adjusted association: **9.2%** approval uplift (approx. 95% CI **7.7%–10.6%**); causal confidence is low because assignment was not randomized.
- Airport fill rate: **59.8%** overall; **30.4%** from 21:00–02:00.
- Peak window needs roughly **59 additional concurrent online captains** if current productivity holds; 23:00 alone is about **71**.
- Suburban airport trips: **16.5%** return fare within 20 min and **21.0%** captain cancellation.

## Run
Place the raw seven CSVs beside `analysis.py`, then run:
```bash
python analysis.py
```
