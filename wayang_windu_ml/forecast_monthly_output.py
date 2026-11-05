"""Exploratory one-month-ahead Wayang Windu output forecasts."""

import base64
import hashlib
import html
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT.parent / "wayang_windu_eda/data/wayang_windu_monthly_main_meter_2018_2021.csv"
OUTPUT_DIR = ROOT / "output"
SOURCE_SHA256 = "50a471aed7890c91248db33c42f94ece29fb98bea741df7756921584bfe73e89"
FIRST_FORECAST_MONTH = pd.Timestamp("2020-01-01")
LAG_COUNT = 3
RIDGE_ALPHA = 10.0
METHODS = {
    "previous_month": "Previous month",
    "trailing_three_month_mean": "Three-month mean",
    "ridge": "Ridge regression",
}
METHOD_COLORS = {"previous_month": "#26728e", "trailing_three_month_mean": "#bc681b", "ridge": "#7752a1"}
UNITS = {"unit_1": "Unit 1", "unit_2": "Unit 2"}


def load_data():
    if hashlib.sha256(DATA_FILE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("Source snapshot changed: review provenance before changing the locked hash")
    frame = pd.read_csv(DATA_FILE)
    frame["date"] = pd.to_datetime(frame["month"], format="%Y-%m", errors="raise")
    frame = frame.sort_values("date").reset_index(drop=True)
    if frame["date"].tolist() != list(pd.date_range("2018-01-01", "2021-06-01", freq="MS")):
        raise ValueError("Expected exactly 42 unique consecutive monthly observations")
    frame["hours_in_month"] = frame["date"].dt.days_in_month * 24
    for unit in UNITS:
        values = pd.to_numeric(frame[f"{unit}_reported_mwh"], errors="raise")
        if not np.isfinite(values).all() or values.lt(0).any():
            raise ValueError(f"Invalid target values for {unit}")
        frame[f"{unit}_average_mw"] = values / frame["hours_in_month"]
    return frame


def forecast_from_history(history):
    values = np.asarray(history, dtype=float)
    if len(values) <= LAG_COUNT or not np.isfinite(values).all():
        raise ValueError("Need finite historical values and at least one supervised training example")
    features = np.asarray([values[position - LAG_COUNT:position][::-1] for position in range(LAG_COUNT, len(values))])
    targets = values[LAG_COUNT:]
    model = make_pipeline(StandardScaler(), Ridge(alpha=RIDGE_ALPHA, solver="svd"))
    model.fit(features, targets)
    next_features = values[-LAG_COUNT:][::-1].reshape(1, -1)
    forecasts = {
        "previous_month": float(values[-1]),
        "trailing_three_month_mean": float(values[-LAG_COUNT:].mean()),
        "ridge": float(model.predict(next_features)[0]),
    }
    return forecasts, model


def evaluate(frame):
    predictions, fit_audits = [], []
    for position in range(len(frame)):
        current = frame.iloc[position]
        if current["date"] < FIRST_FORECAST_MONTH:
            continue
        history = frame.iloc[:position]
        if history["date"].max() >= current["date"]:
            raise AssertionError("Forecast origin includes current or future data")
        for unit, unit_label in UNITS.items():
            values = history[f"{unit}_average_mw"].to_numpy()
            forecasts, model = forecast_from_history(values)
            scaler = model.named_steps["standardscaler"]
            audit = {
                "unit": unit_label, "forecast_month": current["month"],
                "history_start_month": history["month"].iloc[0], "history_end_month": history["month"].iloc[-1],
                "history_months": len(history), "supervised_training_examples": len(history) - LAG_COUNT,
                "first_training_target_month": history["month"].iloc[LAG_COUNT],
                "last_training_target_month": history["month"].iloc[-1],
                "ridge_alpha": RIDGE_ALPHA, "scaler_fit_rows": int(scaler.n_samples_seen_),
            }
            for lag_position in range(LAG_COUNT):
                audit[f"lag_{lag_position + 1}_scaler_mean"] = float(scaler.mean_[lag_position])
                audit[f"lag_{lag_position + 1}_scaler_scale"] = float(scaler.scale_[lag_position])
            fit_audits.append(audit)
            for method, prediction in forecasts.items():
                actual = float(current[f"{unit}_average_mw"])
                error = prediction - actual
                hours = int(current["hours_in_month"])
                predictions.append({
                    "unit": unit_label, "forecast_month": current["month"], "method": method,
                    "training_start_month": history["month"].iloc[0], "training_end_month": history["month"].iloc[-1],
                    "training_months": len(history), "ridge_training_examples": len(history) - LAG_COUNT,
                    "hours_in_target_month": hours, "actual_average_mw": actual, "forecast_average_mw": prediction,
                    "error_mw": error, "absolute_error_mw": abs(error), "squared_error_mw": error ** 2,
                    "actual_mwh": float(current[f"{unit}_reported_mwh"]), "forecast_mwh": prediction * hours,
                    "error_mwh": error * hours, "absolute_error_mwh": abs(error * hours),
                })
    return pd.DataFrame(predictions), pd.DataFrame(fit_audits)


def metrics_table(predictions):
    return predictions.groupby(["unit", "method"], sort=False).agg(
        forecast_months=("forecast_month", "size"), mae_mw=("absolute_error_mw", "mean"),
        rmse_mw=("error_mw", lambda values: np.sqrt(np.mean(np.square(values)))),
        mean_error_mw=("error_mw", "mean"), mae_mwh_per_month=("absolute_error_mwh", "mean"),
        rmse_mwh_per_month=("error_mwh", lambda values: np.sqrt(np.mean(np.square(values)))),
    ).reset_index()


def baseline_comparisons(predictions, metrics):
    rows = []
    random = np.random.default_rng(42)
    unique_months = sorted(predictions["forecast_month"].unique())
    count = len(unique_months)
    starts = random.integers(0, count, size=(2000, int(np.ceil(count / 3))))
    block_indices = ((starts[:, :, None] + np.arange(3)) % count).reshape(2000, -1)[:, :count]
    for unit in UNITS.values():
        monthly_errors = predictions[predictions["unit"].eq(unit)].pivot(index="forecast_month", columns="method", values="absolute_error_mw").reindex(unique_months)
        unit_metrics = metrics[metrics["unit"].eq(unit)].set_index("method")
        for baseline in ["previous_month", "trailing_three_month_mean"]:
            paired = (monthly_errors["ridge"] - monthly_errors[baseline]).to_numpy()
            bootstrap_means = paired[block_indices].mean(axis=1)
            lower, upper = np.quantile(bootstrap_means, [0.025, 0.975])
            baseline_mae = float(unit_metrics.loc[baseline, "mae_mw"])
            rows.append({
                "unit": unit, "baseline": baseline, "paired_forecast_months": count,
                "ridge_minus_baseline_mae_mw": float(paired.mean()),
                "ridge_mae_reduction_pct": (1 - float(unit_metrics.loc["ridge", "mae_mw"]) / baseline_mae) * 100 if baseline_mae else np.nan,
                "ridge_minus_baseline_rmse_mw": float(unit_metrics.loc["ridge", "rmse_mw"] - unit_metrics.loc[baseline, "rmse_mw"]),
                "ridge_lower_absolute_error_months": int((paired < 0).sum()),
                "ridge_higher_absolute_error_months": int((paired > 0).sum()),
                "paired_mae_difference_bootstrap_2_5pct_mw": float(lower),
                "paired_mae_difference_bootstrap_97_5pct_mw": float(upper),
                "bootstrap": "Exploratory paired circular moving blocks: 3 months, 2000 resamples, seed 42; negative difference favors Ridge",
            })
    return pd.DataFrame(rows)


def validate(frame, predictions, fits, metrics):
    expected_months = pd.date_range(FIRST_FORECAST_MONTH, "2021-06-01", freq="MS").strftime("%Y-%m").tolist()
    assert len(predictions) == 108 and len(fits) == 36 and len(metrics) == 6
    assert not predictions.duplicated(["unit", "forecast_month", "method"]).any()
    for _, group in predictions.groupby(["unit", "method"]):
        assert group["forecast_month"].tolist() == expected_months
    assert (pd.to_datetime(predictions["training_end_month"]) < pd.to_datetime(predictions["forecast_month"])).all()
    assert fits["history_months"].min() == 24 and fits["history_months"].max() == 41
    assert fits["supervised_training_examples"].min() == 21 and fits["supervised_training_examples"].max() == 38
    assert (fits["scaler_fit_rows"] == fits["supervised_training_examples"]).all()
    assert np.isfinite(predictions.select_dtypes(include="number")).all().all()
    assert np.allclose(predictions["forecast_mwh"], predictions["forecast_average_mw"] * predictions["hours_in_target_month"])
    maximum_delta = 0.0
    for forecast_month in expected_months:
        mutated = frame.copy()
        current_or_future = mutated["date"].ge(pd.Timestamp(forecast_month))
        for unit in UNITS:
            mutated.loc[current_or_future, f"{unit}_average_mw"] += 1000.0
        changed, _ = evaluate(mutated)
        original_forecasts = predictions.loc[predictions["forecast_month"].eq(forecast_month), "forecast_average_mw"].to_numpy()
        changed_forecasts = changed.loc[changed["forecast_month"].eq(forecast_month), "forecast_average_mw"].to_numpy()
        delta = float(np.max(np.abs(original_forecasts - changed_forecasts)))
        maximum_delta = max(maximum_delta, delta)
        assert np.allclose(original_forecasts, changed_forecasts, rtol=0, atol=1e-10)
    for unit, label in UNITS.items():
        values = frame[frame["date"].lt(FIRST_FORECAST_MONTH)][f"{unit}_average_mw"].to_numpy()
        first = predictions[predictions["unit"].eq(label) & predictions["forecast_month"].eq("2020-01")].set_index("method")
        assert np.isclose(first.loc["previous_month", "forecast_average_mw"], values[-1])
        assert np.isclose(first.loc["trailing_three_month_mean", "forecast_average_mw"], values[-3:].mean())
        own_forecasts, _ = forecast_from_history(values)
        altered = frame.copy()
        other_unit = "unit_2" if unit == "unit_1" else "unit_1"
        altered[f"{other_unit}_average_mw"] += 1000.0
        altered_predictions, _ = evaluate(altered)
        own_rows = predictions[predictions["unit"].eq(label)]["forecast_average_mw"].to_numpy()
        altered_rows = altered_predictions[altered_predictions["unit"].eq(label)]["forecast_average_mw"].to_numpy()
        assert np.array_equal(own_rows, altered_rows)
        constant_forecasts, _ = forecast_from_history(np.full(24, 100.0))
        assert all(np.isclose(value, 100.0) for value in constant_forecasts.values())
        assert np.isfinite(list(own_forecasts.values())).all()
    for _, metric in metrics.iterrows():
        part = predictions[predictions["unit"].eq(metric["unit"]) & predictions["method"].eq(metric["method"])]
        assert np.isclose(metric["mae_mw"], np.mean(np.abs(part["forecast_average_mw"] - part["actual_average_mw"])))
        assert np.isclose(metric["rmse_mw"], np.sqrt(np.mean((part["forecast_average_mw"] - part["actual_average_mw"]) ** 2)))
    maximum_manual_ridge_difference = 0.0
    for _, row in predictions.iterrows():
        unit = "unit_1" if row["unit"] == "Unit 1" else "unit_2"
        values = frame.loc[frame["date"].lt(pd.Timestamp(row["forecast_month"])), f"{unit}_average_mw"].to_numpy()
        if row["method"] == "previous_month":
            independent_prediction = float(values[-1])
        elif row["method"] == "trailing_three_month_mean":
            independent_prediction = float(values[-3:].sum() / 3)
        else:
            features = np.asarray([values[position - 3:position][::-1] for position in range(3, len(values))])
            targets = values[3:]
            means = features.mean(axis=0)
            scales = features.std(axis=0)
            scales = np.where(scales == 0, 1.0, scales)
            standardized = (features - means) / scales
            coefficients = np.linalg.solve(standardized.T @ standardized + RIDGE_ALPHA * np.eye(3), standardized.T @ (targets - targets.mean()))
            independent_prediction = float(targets.mean() + ((values[-3:][::-1] - means) / scales) @ coefficients)
            maximum_manual_ridge_difference = max(maximum_manual_ridge_difference, abs(independent_prediction - row["forecast_average_mw"]))
        assert np.isclose(independent_prediction, row["forecast_average_mw"], rtol=0, atol=1e-8)
    return {
        "status": "passed", "predictions": len(predictions), "fit_origins": len(fits),
        "same_18_months_for_all_methods_and_units": True, "strict_past_only_training_dates": True,
        "training_only_scaler_rows_checked": True,
        "current_and_future_target_perturbation_checked_at_all_18_origins": True,
        "maximum_forecast_change_under_current_future_perturbation_mw": maximum_delta,
        "other_unit_perturbation_invariance": True, "constant_series_predictions_checked": True,
        "first_month_baseline_arithmetic_checked": True, "metrics_independently_recomputed": True,
        "all_72_baseline_forecasts_independently_recomputed": True,
        "all_36_ridge_forecasts_match_independent_numpy_solution": True,
        "maximum_manual_ridge_forecast_difference_mw": maximum_manual_ridge_difference,
        "mwh_conversion_checked": True, "source_hash": SOURCE_SHA256,
    }


def save_plots(predictions, metrics):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, constrained_layout=True)
    for axis, unit in zip(axes, UNITS.values()):
        part = predictions[predictions["unit"].eq(unit)]
        actual = part.drop_duplicates("forecast_month")
        axis.plot(pd.to_datetime(actual["forecast_month"]), actual["actual_average_mw"], color="#222222", linewidth=2.4, marker="o", label="Observed")
        for method, label in METHODS.items():
            forecast = part[part["method"].eq(method)]
            axis.plot(pd.to_datetime(forecast["forecast_month"]), forecast["forecast_average_mw"], color=METHOD_COLORS[method], marker=".", linestyle="--", label=label)
        axis.set(title=unit, ylabel="Monthly average power (MW)")
        axis.grid(alpha=0.2)
    axes[0].legend(ncol=2, fontsize=9)
    axes[1].set_xlabel("Forecast month")
    axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    figure.suptitle("Exploratory rolling one-month-ahead forecasts: January 2020-June 2021")
    figure.savefig(OUTPUT_DIR / "forecast_comparison.png", dpi=160, bbox_inches="tight")
    plt.close(figure)
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for axis, metric, label in zip(axes, ["mae_mw", "rmse_mw"], ["MAE (MW)", "RMSE (MW)"]):
        for offset_position, (method, method_label) in enumerate(METHODS.items()):
            part = metrics[metrics["method"].eq(method)].set_index("unit").reindex(list(UNITS.values()))
            positions = np.arange(2) + (offset_position - 1) * 0.23
            bars = axis.bar(positions, part[metric], width=0.23, label=method_label, color=METHOD_COLORS[method])
            axis.bar_label(bars, fmt="%.2f", padding=3, fontsize=9)
        axis.set(xticks=[0, 1], xticklabels=list(UNITS.values()), ylabel=label, title=f"{label}: lower is better")
        axis.set_ylim(0, metrics[metric].max() * 1.35)
        axis.grid(axis="y", alpha=0.2)
    axes[0].legend(fontsize=9)
    figure.suptitle("Same 18 forecast months per method and unit; no test-month tuning")
    figure.savefig(OUTPUT_DIR / "forecast_errors.png", dpi=160, bbox_inches="tight")
    plt.close(figure)


def write_outputs(frame, predictions, fits, metrics, comparisons, validation):
    protocol = {
        "experiment": "Wayang Windu monthly output, domestic-only exploratory pilot", "run_date": "2026-11-03",
        "initial_training_months": ["2018-01", "2019-12"], "first_forecast_month": "2020-01",
        "last_forecast_month": "2021-06", "forecast_months_per_unit": 18, "units": list(UNITS.values()),
        "target": "Monthly average power in MW = published Main Meter MWh / calendar hours",
        "evaluation": "Expanding-window one-month-ahead, observed prior targets added after each forecast",
        "methods": METHODS, "ridge_features": ["lag_1_average_mw", "lag_2_average_mw", "lag_3_average_mw"],
        "ridge_alpha": RIDGE_ALPHA, "ridge_solver": "svd", "ridge_fit_intercept": True,
        "preprocessing": "StandardScaler fitted only on each unit's current supervised training feature rows",
        "initial_ridge_examples_per_unit": 21, "last_origin_ridge_examples_per_unit": 38,
        "hyperparameter_tuning": "None; alpha=10 fixed before examining forecast errors, matching earlier project Ridge default",
        "negative_forecast_clipping": "None", "foreign_data_used": False,
        "test_selection": "First evaluation month and methods fixed before this run; full period already inspected in EDA",
        "real_time_limit": "Retrospective revised data, not publication-vintage or reporting-delay reconstruction",
        "bootstrap": "Paired circular date blocks shared across units; length 3 months, 2000 resamples, seed 42. Exploratory intervals, not proof of significance.",
        "source_file": str(DATA_FILE.relative_to(ROOT.parent)), "source_sha256": SOURCE_SHA256,
        "source_url": "https://cdm.unfccc.int/UserManagement/FileStorage/FSK5I6HGV4BJ39YARNEOXZ18Q7MWUP",
        "software": {"numpy": np.__version__, "pandas": pd.__version__, "sklearn": sklearn.__version__, "matplotlib": matplotlib.__version__},
    }
    by_year = predictions.assign(forecast_year=predictions["forecast_month"].str[:4]).groupby(["unit", "method", "forecast_year"]).agg(
        months=("forecast_month", "size"), mae_mw=("absolute_error_mw", "mean"), rmse_mw=("error_mw", lambda values: np.sqrt(np.mean(np.square(values))))).reset_index()
    largest = predictions.sort_values("absolute_error_mw", ascending=False).groupby(["unit", "method"], sort=False).head(3)
    outputs = {"rolling_predictions.csv": predictions, "forecast_metrics.csv": metrics, "training_fit_audit.csv": fits,
               "ridge_vs_baselines.csv": comparisons, "metrics_by_evaluation_year.csv": by_year,
               "largest_errors.csv": largest, "monthly_input_with_derived_power.csv": frame}
    for filename, table in outputs.items():
        table.to_csv(OUTPUT_DIR / filename, index=False, float_format="%.10f")
    for filename, value in [("evaluation_protocol.json", protocol), ("validation_checks.json", validation)]:
        (OUTPUT_DIR / filename).write_text(json.dumps(value, indent=2) + "\n")
    report = ["# Wayang Windu: exploratory monthly-output forecasting results", "",
              "## Aim and frozen evaluation design", "",
              "Test whether three-lag Ridge improves historical one-month-ahead monthly average power forecasts over previous-month and three-month-average baselines. This is a domestic-only pilot, not transfer learning or emissions modelling.", "",
              "Initial history: January 2018-December 2019 (24 observed months, 21 supervised Ridge examples per unit). Evaluation: January 2020-June 2021, 18 forecasts per unit and method. Each next forecast incorporates the previous month's observed value; it is not a fixed-origin 18-month forecast. Models are fitted separately by unit and both units use identical chronological evaluation months.", "",
              "Ridge uses lag 1, lag 2 and lag 3 of monthly average MW. Standardization is refitted only on supervised training features at each origin. The intercept is included, alpha=10 is fixed, and there is no hyperparameter search, calendar feature, other-unit input, forecast clipping or full-sample normalization. Penalty 10 follows the earlier project's Ridge default; it is not claimed optimal. Dates and design were fixed before this run's errors were inspected, but the entire period was already used for EDA: the evaluation is exploratory, not an untouched holdout.", "",
              "## Scores", "", "| Unit | Method | Months | MAE (MW) | RMSE (MW) |", "|---|---|---:|---:|---:|"]
    for _, row in metrics.iterrows():
        report.append(f"| {row['unit']} | {METHODS[row['method']]} | {row['forecast_months']} | {row['mae_mw']:.3f} | {row['rmse_mw']:.3f} |")
    report += ["", "MAE is the average absolute error in monthly average MW. RMSE gives more weight to larger errors. Neither is a percentage or a capacity factor. Secondary MWh/month scores are saved separately by converting each forecast using the target month's known calendar hours. Do not compare these scores with annual WDI or Ember MAPE: the targets, units and periods differ.", "", "## What the comparison shows", ""]
    for unit in UNITS.values():
        scores = metrics[metrics["unit"].eq(unit)].set_index("method")
        best_mae = scores["mae_mw"].idxmin()
        best_rmse = scores["rmse_mw"].idxmin()
        report.append(f"- **{unit}:** lowest MAE: {METHODS[best_mae]} ({scores.loc[best_mae, 'mae_mw']:.3f} MW); lowest RMSE: {METHODS[best_rmse]} ({scores.loc[best_rmse, 'rmse_mw']:.3f} MW).")
        for _, row in comparisons[comparisons["unit"].eq(unit)].iterrows():
            direction = "lower" if row["ridge_mae_reduction_pct"] > 0 else "higher"
            report.append(f"  - Ridge MAE is {abs(row['ridge_mae_reduction_pct']):.1f}% {direction} than {METHODS[row['baseline']]}; Ridge has lower absolute error in {row['ridge_lower_absolute_error_months']} of 18 months. Paired MAE difference (Ridge minus baseline): {row['ridge_minus_baseline_mae_mw']:.3f} MW; exploratory 95% block-bootstrap interval [{row['paired_mae_difference_bootstrap_2_5pct_mw']:.3f}, {row['paired_mae_difference_bootstrap_97_5pct_mw']:.3f}] MW.")
    report += ["", "Bootstrap resamples paired three-month circular date blocks, using the same date selections for both units. All four paired MAE-difference intervals include zero in this run. With only 18 dates and prior EDA, these intervals are descriptive sensitivity checks, not reliable proof of general superiority or independence of units.", "", "## Report-ready conclusion", "",
               "The exploratory monthly forecasting results were mixed. Ridge regression achieved the lowest RMSE for both units, but did not achieve the lowest MAE for either unit. The three-month trailing average had the lowest MAE for Unit 1, while the previous-month baseline had the lowest MAE for Unit 2. This means Ridge performed better under a measure that gives extra weight to large errors, but did not consistently reduce average absolute errors compared with the best simple baseline. No single method dominated both measures. The result is limited to 18 evaluated months per unit at one field, with previously explored data and a fixed, untuned Ridge configuration; it does not establish future superiority or benefits from foreign data.", "", "## Larger errors and coverage", ""]
    for unit in UNITS.values():
        for method in METHODS:
            row = predictions[predictions["unit"].eq(unit) & predictions["method"].eq(method)].sort_values("absolute_error_mw", ascending=False).iloc[0]
            report.append(f"- {unit}, {METHODS[method]}: largest absolute error in {row['forecast_month']}, {row['absolute_error_mw']:.3f} MW (observed {row['actual_average_mw']:.3f}, forecast {row['forecast_average_mw']:.3f} MW).")
    report += ["", "The pronounced June 2019 Unit 1 dip lies in initial training, not evaluation. These results therefore do not test advance prediction of that event. No outage periods or difficult evaluation dates were removed. Error diagnostics describe failures, not verified operational causes. The year-specific table has 12 forecasts in 2020 and six in 2021, not equally sized annual tests.", "", "## Validation and limitations", "",
               "All methods share the same dates. Training ends before every forecast month, scaler training-row counts are checked, metrics are independently recomputed, and the baseline formulas and MWh conversions are verified. At every forecast origin, changing the current and all future target values leaves that origin's predictions unchanged. Altering the other unit also leaves each unit's own predictions unchanged. Constant-series predictions remain constant.", "",
               "These checks establish past-only implementation in observation time; they do not establish real-time data availability. The source is a revised monitoring report, not a historical publication-vintage dataset. There are only 18 evaluation dates at one geothermal field, shared by two units. No additional sites, New Zealand training, recent Indonesian operational data or long-horizon forecasts were tested. Do not translate MW forecast errors into claims about marginal grid displacement, 2034 avoided emissions or issued carbon credits.", "",
               "No alpha, evaluation start or features were changed after seeing these scores. Any subsequent search using these errors should be documented as further exploration and requires new held-back data for confirmation."]
    (OUTPUT_DIR / "forecast_results.md").write_text("\n".join(report) + "\n")
    figures = []
    for filename, title in [("forecast_comparison.png", "Observed and forecast monthly average power"), ("forecast_errors.png", "Errors on the same evaluation dates")]:
        encoded = base64.b64encode((OUTPUT_DIR / filename).read_bytes()).decode()
        figures.append(f'<h2>{title}</h2><img alt="{title}" src="data:image/png;base64,{encoded}">')
    document = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wayang Windu forecast results</title><style>body{font:16px/1.6 system-ui;color:#172b3a;max-width:1100px;margin:32px auto;padding:0 20px;background:#fafbfc}img{width:100%;height:auto}pre{font:inherit;white-space:pre-wrap;overflow-wrap:anywhere}.notice{padding:16px;background:#fff1cc}table{border-collapse:collapse}th,td{padding:9px;border-bottom:1px solid #ccd4db}.scroll{overflow:auto}</style></head><body><h1>Wayang Windu monthly output forecasts</h1><p class="notice">Exploratory, domestic-only: 18 chronological forecast months per unit. Not an untouched test or a demonstrated transfer-learning result.</p>'
    document += '<div class="scroll">' + metrics.to_html(index=False, float_format=lambda value: f"{value:.3f}") + '</div>' + ''.join(figures)
    document += '<h2>Report-ready findings and design</h2><pre>' + html.escape("\n".join(report)) + '</pre></body></html>'
    (OUTPUT_DIR / "forecast_results.html").write_text(document)


def write_inline_chart(metrics):
    template = (ROOT / "forecast_errors_template.html").read_text()
    maximum = float(np.ceil(metrics[["mae_mw", "rmse_mw"]].to_numpy().max()))
    template = template.replace("{{SCALE_MAX}}", f"{maximum:.0f}")
    template = template.replace("{{SCALE_MID}}", f"{maximum / 2:.0f}")
    for _, row in metrics.iterrows():
        unit_key = row["unit"].lower().replace(" ", "_")
        for metric in ["mae_mw", "rmse_mw"]:
            key = f"{unit_key}_{row['method']}_{metric}"
            value = float(row[metric])
            template = template.replace("{{" + key + "}}", f"{value:.3f}")
            template = template.replace("{{" + key + "_width}}", f"{100 * value / maximum:.4f}")
    if "{{" in template:
        raise ValueError("Unfilled chart template value")
    (OUTPUT_DIR / "forecast_errors_inline.html").write_text(template)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    frame = load_data()
    predictions, fits = evaluate(frame)
    metrics = metrics_table(predictions)
    comparisons = baseline_comparisons(predictions, metrics)
    validation = validate(frame, predictions, fits, metrics)
    save_plots(predictions, metrics)
    write_outputs(frame, predictions, fits, metrics, comparisons, validation)
    write_inline_chart(metrics)
    print(metrics[["unit", "method", "forecast_months", "mae_mw", "rmse_mw"]].to_string(index=False, float_format=lambda value: f"{value:.6f}"))
    print("Validation:", validation["status"])


if __name__ == "__main__":
    main()
