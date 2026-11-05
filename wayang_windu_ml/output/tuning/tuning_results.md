# Exploratory Ridge Hyperparameter Tuning

This follow-up tested whether selecting Ridge's regularisation strength from earlier observations improved Wayang Windu monthly average power forecasts. The original experiment and its output files were preserved.

## Methods

The source remains 42 months per unit, January 2018-June 2021, at one field. Monthly average MW equals published Main Meter MWh divided by calendar hours. No new observations, operational variables or New Zealand data were added.

At each outer forecast month, alpha was selected separately for each unit from 0.01, 0.1, 1, 10, 100 and 1000. Within the available history, training began with January-December 2018; an inner one-month-ahead forecast was made for January 2019, then the actual observation was added and the process repeated through the last observed month. Each candidate's inner MAE was calculated over these dates. The lowest inner MAE selected alpha; exact ties preferred larger alpha. Each inner fit used its own training-only scaler and previous-three-month inputs. The selected model was then refitted on all history preceding the outer date.

For the January 2020 outer forecast, selection used only the 12 inner forecasts from January-December 2019. For February 2020, January 2020 could join the inner validation history because it was now observed. Across the experiment there were 12-29 inner forecast dates per choice, not independent new data. The original January 2020-June 2021 outer dates were retained: 18 expanding one-month-ahead forecasts per unit. The first inner model had nine three-lag supervised examples; the first outer model had 21. Selection optimised MAE only, not RMSE. Grid, objective and windows were written in tuning_protocol.json before calculating tuned scores.

## Results

| Unit | Method | MAE (MW) | RMSE (MW) |
|---|---|---:|---:|
| Unit 1 | Previous month | 2.089 | 3.442 |
| Unit 1 | Three-month mean | 1.834 | 2.683 |
| Unit 1 | Ridge: fixed alpha=10 | 2.287 | 2.625 |
| Unit 2 | Previous month | 0.459 | 0.759 |
| Unit 2 | Three-month mean | 0.531 | 0.703 |
| Unit 2 | Ridge: fixed alpha=10 | 0.472 | 0.644 |
| Unit 1 | Ridge: tuned for MAE | 2.280 | 2.502 |
| Unit 2 | Ridge: tuned for MAE | 0.523 | 0.708 |

## Comparison with fixed alpha=10

- Unit 1: tuning changed MAE by -0.29% and RMSE by -4.68% relative to fixed Ridge (negative means improvement). Selected alpha counts: 1000: 18 months.
  Lowest MAE among all four methods: Three-month mean; lowest RMSE: Ridge: tuned for MAE.
- Unit 2: tuning changed MAE by +10.89% and RMSE by +9.90% relative to fixed Ridge (negative means improvement). Selected alpha counts: 1: 11 months, 1000: 7 months.
  Lowest MAE among all four methods: Previous month; lowest RMSE: Ridge: fixed alpha=10.

## Interpretation and limits

Tuning selects the alpha that worked best in earlier inner validation months; it does not guarantee that alpha will forecast the next month best. Selecting for MAE also does not guarantee improved RMSE. Different temporal windows, objectives or grids would be additional experiments, not reasons to silently replace this protocol after viewing results.

This follow-up was motivated by the original results, and the full period had already informed EDA. Although all inner selection is past-only in observation time, these are reused exploratory outer dates, not a new untouched confirmatory test. The revised monitoring data do not reconstruct real-time reporting availability. Only 18 outer dates and two units at one field were evaluated; no statistical significance or future/general superiority is claimed. Results do not validate transfer learning, long-horizon generation, avoided grid emissions or issued credits.

## Files

tuning_comparison.png contains all four methods. alpha_choices.csv records each decision; inner_candidate_scores.csv and inner_fold_predictions.csv expose every selection fold. rolling_predictions.csv and forecast_metrics.csv retain all four methods. validation_checks.json records chronology, scaler, manual NumPy, metric and future-perturbation checks.
