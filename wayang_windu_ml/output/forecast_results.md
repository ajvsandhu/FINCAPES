# Wayang Windu: exploratory monthly-output forecasting results

## Aim and frozen evaluation design

Test whether three-lag Ridge improves historical one-month-ahead monthly average power forecasts over previous-month and three-month-average baselines. This is a domestic-only pilot, not transfer learning or emissions modelling.

Initial history: January 2018-December 2019 (24 observed months, 21 supervised Ridge examples per unit). Evaluation: January 2020-June 2021, 18 forecasts per unit and method. Each next forecast incorporates the previous month's observed value; it is not a fixed-origin 18-month forecast. Models are fitted separately by unit and both units use identical chronological evaluation months.

Ridge uses lag 1, lag 2 and lag 3 of monthly average MW. Standardization is refitted only on supervised training features at each origin. The intercept is included, alpha=10 is fixed, and there is no hyperparameter search, calendar feature, other-unit input, forecast clipping or full-sample normalization. Penalty 10 follows the earlier project's Ridge default; it is not claimed optimal. Dates and design were fixed before this run's errors were inspected, but the entire period was already used for EDA: the evaluation is exploratory, not an untouched holdout.

## Scores

| Unit | Method | Months | MAE (MW) | RMSE (MW) |
|---|---|---:|---:|---:|
| Unit 1 | Previous month | 18 | 2.089 | 3.442 |
| Unit 1 | Three-month mean | 18 | 1.834 | 2.683 |
| Unit 1 | Ridge regression | 18 | 2.287 | 2.625 |
| Unit 2 | Previous month | 18 | 0.459 | 0.759 |
| Unit 2 | Three-month mean | 18 | 0.531 | 0.703 |
| Unit 2 | Ridge regression | 18 | 0.472 | 0.644 |

MAE is the average absolute error in monthly average MW. RMSE gives more weight to larger errors. Neither is a percentage or a capacity factor. Secondary MWh/month scores are saved separately by converting each forecast using the target month's known calendar hours. Do not compare these scores with annual WDI or Ember MAPE: the targets, units and periods differ.

## What the comparison shows

- **Unit 1:** lowest MAE: Three-month mean (1.834 MW); lowest RMSE: Ridge regression (2.625 MW).
  - Ridge MAE is 9.5% higher than Previous month; Ridge has lower absolute error in 7 of 18 months. Paired MAE difference (Ridge minus baseline): 0.198 MW; exploratory 95% block-bootstrap interval [-0.895, 1.189] MW.
  - Ridge MAE is 24.7% higher than Three-month mean; Ridge has lower absolute error in 8 of 18 months. Paired MAE difference (Ridge minus baseline): 0.453 MW; exploratory 95% block-bootstrap interval [-0.074, 0.999] MW.
- **Unit 2:** lowest MAE: Previous month (0.459 MW); lowest RMSE: Ridge regression (0.644 MW).
  - Ridge MAE is 2.9% higher than Previous month; Ridge has lower absolute error in 7 of 18 months. Paired MAE difference (Ridge minus baseline): 0.013 MW; exploratory 95% block-bootstrap interval [-0.113, 0.132] MW.
  - Ridge MAE is 11.2% lower than Three-month mean; Ridge has lower absolute error in 8 of 18 months. Paired MAE difference (Ridge minus baseline): -0.060 MW; exploratory 95% block-bootstrap interval [-0.165, 0.029] MW.

Bootstrap resamples paired three-month circular date blocks, using the same date selections for both units. All four paired MAE-difference intervals include zero in this run. With only 18 dates and prior EDA, these intervals are descriptive sensitivity checks, not reliable proof of general superiority or independence of units.

## Report-ready conclusion

The exploratory monthly forecasting results were mixed. Ridge regression achieved the lowest RMSE for both units, but did not achieve the lowest MAE for either unit. The three-month trailing average had the lowest MAE for Unit 1, while the previous-month baseline had the lowest MAE for Unit 2. This means Ridge performed better under a measure that gives extra weight to large errors, but did not consistently reduce average absolute errors compared with the best simple baseline. No single method dominated both measures. The result is limited to 18 evaluated months per unit at one field, with previously explored data and a fixed, untuned Ridge configuration; it does not establish future superiority or benefits from foreign data.

## Larger errors and coverage

- Unit 1, Previous month: largest absolute error in 2021-02, 7.688 MW (observed 100.813, forecast 108.501 MW).
- Unit 1, Three-month mean: largest absolute error in 2020-03, 7.375 MW (observed 100.305, forecast 107.680 MW).
- Unit 1, Ridge regression: largest absolute error in 2021-02, 5.287 MW (observed 100.813, forecast 106.100 MW).
- Unit 2, Previous month: largest absolute error in 2021-01, 2.373 MW (observed 109.874, forecast 107.501 MW).
- Unit 2, Three-month mean: largest absolute error in 2021-01, 1.673 MW (observed 109.874, forecast 108.201 MW).
- Unit 2, Ridge regression: largest absolute error in 2021-01, 1.697 MW (observed 109.874, forecast 108.177 MW).

The pronounced June 2019 Unit 1 dip lies in initial training, not evaluation. These results therefore do not test advance prediction of that event. No outage periods or difficult evaluation dates were removed. Error diagnostics describe failures, not verified operational causes. The year-specific table has 12 forecasts in 2020 and six in 2021, not equally sized annual tests.

## Validation and limitations

All methods share the same dates. Training ends before every forecast month, scaler training-row counts are checked, metrics are independently recomputed, and the baseline formulas and MWh conversions are verified. At every forecast origin, changing the current and all future target values leaves that origin's predictions unchanged. Altering the other unit also leaves each unit's own predictions unchanged. Constant-series predictions remain constant.

These checks establish past-only implementation in observation time; they do not establish real-time data availability. The source is a revised monitoring report, not a historical publication-vintage dataset. There are only 18 evaluation dates at one geothermal field, shared by two units. No additional sites, New Zealand training, recent Indonesian operational data or long-horizon forecasts were tested. Do not translate MW forecast errors into claims about marginal grid displacement, 2034 avoided emissions or issued carbon credits.

No alpha, evaluation start or features were changed after seeing these scores. Any subsequent search using these errors should be documented as further exploration and requires new held-back data for confirmation.
