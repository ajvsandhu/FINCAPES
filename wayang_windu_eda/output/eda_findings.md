# Wayang Windu monthly generation: EDA findings

Analysis date: 2026-10-30. No forecasting model was trained or evaluated.

## 1. Aim and scope

Explore the consistency, coverage, output variation and lag relationships of published Indonesian geothermal electricity records before modelling. This is **monthly plant-output EDA**, not electricity-demand forecasting, daily-output EDA, reservoir modelling or an emissions/credit calculation.

The complete daily 2013-November 2017 dataset is not yet locally extracted. Its five example rows are excluded. This EDA instead uses the existing **42-month transcription, January 2018-June 2021, for Units 1 and 2 at Wayang Windu**: 84 unit-month values at one field, not 84 independent dates or two independent plants.

## 2. Source and checks

Source: UNFCCC CDM project 3193, revised-v04 monitoring report completed 28 April 2022, Annex 5, printed pages 90-94 of 99. Tables are labelled Main Meter. Preserve this definition rather than calling the values raw SCADA, gross generation, or the exact electricity used to calculate CERs without further reconciliation.

- All 84 transcription values were re-compared with online PDF table text on 30 October 2026, and all five source table page images inspected. No numerical mismatch was found. This was a same-analyst second pass, not independent-person QA or daily reconciliation.
- No duplicate months, gaps within the 42-month interval, missing numeric generation, negative generation or zero-generation months.
- No zero monthly totals does not establish that there were no shutdown days: monthly aggregation can hide them.
- December 2017 is excluded because monitoring starts December 2. July-December 2021 is outside coverage, not missing zero-output months.
- Retain the published values and flag August/September 2018, which have a stated 0.2% meter-error adjustment. Do not apply that adjustment twice.
- Local PDF and supporting XLSX download attempts returned HTML challenge pages. No complete downloaded daily file or local source PDF is claimed.

Official source: https://cdm.unfccc.int/UserManagement/FileStorage/FSK5I6HGV4BJ39YARNEOXZ18Q7MWUP

Registry and supporting documents: https://cdm.unfccc.int/Projects/DB/TUEV-SUED1260194062.48/CP/3MD0A9GB28W7MMR77ZOJJ4GVK8D0V4/iProcess/RWTUV1633521981.91/view

## 3. What the variables mean

Monthly MWh measures electricity over the month. It is affected by both output and the number of days. Monthly average MW = monthly MWh / (days in month x 24). This makes different-length months more comparable, but is not instantaneous power or a capacity factor. MWh/day is a monthly daily average, **not actual daily readings**. No capacity factor is calculated because matching historical capacity and meter boundaries have not been established.

## 4. Main findings

- Over the covered period, time-weighted average output is **105.61 MW for Unit 1** and **108.88 MW for Unit 2**. Time weighting divides total MWh by total calendar hours, rather than giving February and January equal weight.
- Unit 1's lowest monthly average is **75.77 MW in 2019-06**; Unit 2's lowest is **105.89 MW in 2019-06**. The Unit 1 dip is an observation, not a diagnosed cause. Keep the low-output values in the analysis.
- A descriptive threshold below 90% of each unit's full-sample median flags **1 unit-month observation(s)**. The threshold is exploratory, not an engineering operating limit, outage classification, prediction rule or reason to delete data.
- Combined reported generation changes **-1.90% in 2019** relative to 2018 and **+1.44% in 2020** relative to 2019. Only 2018-2020 are complete years. Compare January-June across all four years for a like-for-like view of 2021; do not annualize it or compare its six-month sum to full-year totals.
- Lag-1 correlations of raw monthly MWh are **-0.012** for Unit 1 and **-0.477** for Unit 2. After month-length adjustment they are **0.262** and **0.537**. Their difference shows why the calendar matters. These are in-sample descriptive associations, not prediction accuracy, causal effects or evidence that ML will beat persistence.
- With only 3-4 observations for each calendar month and a short, interrupted operating history, do not claim a robust seasonal cycle from the heatmap or annual lag correlations.

## 5. Implications for ML and validation

This dataset supports a preliminary historical monthly-output case study, but cannot support daily forecasts. With three lags, there are only 39 target dates per unit before train/validation/test separation; a 12-month lag leaves only 30. Units share a field, so keep both units together when splitting dates. Do not randomly split unit-month rows.

The full 42-month period has now informed EDA and earlier source inspection. **None of it should be described as an untouched final holdout.** Any subsequent past-only rolling evaluation within this period must be labelled exploratory, with tuning confined to earlier windows. A confirmatory claim needs additional, genuinely held-back Indonesian observations. Avoid spending this tiny sample on many feature/model choices.

If a monthly pilot proceeds, compare previous-month average power and a trailing mean against a small regularized model. Predict monthly average power and multiply by the target month's known calendar hours for MWh; also compare against a raw-MWh persistence baseline on the same dates. Use MAE/RMSE in MWh/month or MW, clearly specifying the target. Daily-model baselines belong to a separately extracted daily dataset.

If New Zealand training is later added, aggregate compatible electricity measurements to the same monthly target, establish comparable meter/plant definitions, and use foreign history available before each Indonesian forecast origin. Compare domestic-only and foreign-assisted models on identical Indonesian dates. Historical experiment results would not establish 2026 operational accuracy or generalization to other Indonesian fields.

## 6. Report-ready conclusion

The exploratory analysis found a continuous monthly generation series for two units at Wayang Windu from January 2018 to June 2021, with no missing or negative generation values in the transcribed interval. Adjusting energy totals for month length revealed a pronounced Unit 1 reduction in June 2019 and reduced calendar-related distortion in lag relationships. The records provide a useful preliminary Indonesian plant-output case study, but represent only 42 dates at one field. The analysis does not establish a reliable seasonal pattern, forecast accuracy, transfer-learning benefit, avoided emissions or carbon-credit issuance. A daily forecasting study still requires full extraction and validation of the daily source tables.
