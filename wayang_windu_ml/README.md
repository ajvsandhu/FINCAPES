# Wayang Windu: exploratory monthly-output forecasts

Compare previous-month average power, a three-month trailing average and three-lag Ridge regression separately for two units at one Indonesian geothermal field. No foreign data is used.

## Frozen protocol

- Input: existing revised-v04 Main Meter monthly transcription, January 2018-June 2021. Its SHA-256 is locked in the script. The source file and completed EDA are not modified.
- Initial training: January 2018-December 2019, 24 observations and 21 three-lag supervised examples per unit.
- Evaluation: January 2020-June 2021, 18 expanding-window one-month-ahead forecasts per unit. Both units and all three methods use the same dates. Actual observations are added as time advances, not forecasts recursively substituted for them.
- Target: monthly average power in MW, equal to published MWh divided by calendar hours. Secondary energy errors are in MWh/month, not daily MWh.
- Ridge: previous three values only; training-only StandardScaler, intercept, fixed alpha=10, deterministic SVD solver. No test-month tuning or clipping. Alpha follows the earlier project default and is not claimed optimal.
- The evaluation dates and settings were chosen before this experiment's scores were calculated, but all dates had already informed EDA. Results are exploratory, not an untouched final test. Observation-time lagging is not proof of real-time publication availability.

## Run

From the repository root:

```bash
python3 -B wayang_windu_ml/forecast_monthly_output.py
```

Dependencies: numpy, pandas, matplotlib, scikit-learn (existing environment; no network or API key required). Software versions and the input hash are recorded in `output/evaluation_protocol.json`.

## Outputs

- `report_results_section.md`: integrated report-ready narrative covering the original experiment and the later tuning follow-up, with all three PNG references and an updated conclusion.
- `output/forecast_results.html`: standalone report with embedded charts, scores and explanations.
- `output/forecast_results.md`: report-ready design, results, larger-error months and limitations.
- `output/forecast_metrics.csv`: unit-specific MAE/RMSE in MW and MWh/month, plus mean signed error (forecast minus actual).
- `output/rolling_predictions.csv`: all 108 forecast rows: 18 dates x 2 units x 3 methods, with history bounds, targets and errors.
- `output/training_fit_audit.csv`: training counts, target dates and training-only scaler statistics at all 36 unit/origins.
- `output/ridge_vs_baselines.csv`: paired comparisons and exploratory three-month-block bootstrap intervals; identical date resamples across units, seed 42, 2000 draws.
- `output/metrics_by_evaluation_year.csv`: 12 forecasts in 2020 vs six in 2021; not equal-length annual tests.
- `output/largest_errors.csv`: three largest errors for each unit/method, without excluding them from metrics.
- `output/validation_checks.json`: chronology, arithmetic, equal-date coverage, constant-series checks, and current/future-value and other-unit perturbation invariance.
- `output/monthly_input_with_derived_power.csv`: source snapshot plus explicitly derived monthly average power and calendar hours.
- Two PNG figures: actual/forecast paths and MAE/RMSE comparisons.

## Interpretation

Unit 1's June 2019 dip is in training, not evaluation. This run cannot establish the ability to anticipate that event. The score table does not validate daily forecasting, 2026 operations, foreign-to-Indonesian transfer, generalization to other geothermal fields, 2034 generation, grid emission factors or issued credits. A lower error on these 18 exploratory dates is an observed sample result, not proof of future superiority. Future model choices informed by these scores require new held-back data for confirmation.

Implementation references: scikit-learn's official Common pitfalls/data leakage and Ridge documentation. Primary energy-source provenance remains in the existing EDA audit and the locked input; no new source extraction is claimed.

## Exploratory alpha-tuning follow-up

Run `python3 -B wayang_windu_ml/tune_monthly_output.py` from the repository root.
The original script and results above remain unchanged. New results go to
`output/tuning/`, including a report, PNG comparison, all four methods' scores,
per-origin alpha choices, every inner validation prediction and validation checks.

The prespecified `tuning_protocol.json` uses alpha values 0.01, 0.1, 1, 10, 100
and 1000. At every outer date, select alpha by expanding one-month-ahead inner
MAE using only earlier observations. Inner forecasts begin in January 2019 after
12 months of history; each fold refits its own scaler. Refit the chosen alpha on
all available history before forecasting the outer month. Keep the original
January 2020-June 2021 outer dates and both baselines plus fixed-alpha Ridge.
Do not select on outer errors or change the grid after viewing tuned results.
This is follow-up exploration on reused dates, not a new untouched test or a
guarantee of improved accuracy. No foreign data were used.
