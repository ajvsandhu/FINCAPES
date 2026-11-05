"""Past-only alpha selection, preserving the original fixed-alpha experiment."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import forecast_monthly_output as original


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output/tuning"
PROTOCOL_FILE = ROOT / "tuning_protocol.json"
PROTOCOL = json.loads(PROTOCOL_FILE.read_text())
ALPHAS = tuple(PROTOCOL["alpha_candidates"])
MINIMUM_INNER_HISTORY = PROTOCOL["minimum_inner_history_months"]
LABELS = {
    "previous_month": "Previous month",
    "trailing_three_month_mean": "Three-month mean",
    "ridge": "Ridge: fixed alpha=10",
    "ridge_tuned": "Ridge: tuned for MAE",
}


def fit_predict(values, alpha):
    history = np.asarray(values, dtype=float)
    if len(history) <= 3 or not np.isfinite(history).all():
        raise ValueError("Need finite history and at least one supervised example")
    features = np.asarray([history[position - 3:position][::-1] for position in range(3, len(history))])
    model = make_pipeline(StandardScaler(), Ridge(alpha=alpha, solver="svd"))
    model.fit(features, history[3:])
    prediction = float(model.predict(history[-3:][::-1].reshape(1, -1))[0])
    return prediction, model


def select_alpha(values, months):
    if len(values) <= MINIMUM_INNER_HISTORY:
        raise ValueError("No inner validation dates")
    fold_rows, score_rows = [], []
    for alpha in ALPHAS:
        errors = []
        for position in range(MINIMUM_INNER_HISTORY, len(values)):
            forecast, model = fit_predict(values[:position], alpha)
            error = forecast - float(values[position])
            errors.append(abs(error))
            scaler = model.named_steps["standardscaler"]
            fold_rows.append({
                "alpha": alpha, "inner_forecast_month": months[position],
                "inner_training_end_month": months[position - 1],
                "inner_history_months": position, "scaler_fit_rows": int(scaler.n_samples_seen_),
                "actual_average_mw": float(values[position]), "forecast_average_mw": forecast,
                "absolute_error_mw": abs(error),
            })
        score_rows.append({"alpha": alpha, "inner_mae_mw": float(np.mean(errors)), "inner_forecasts": len(errors)})
    selected = min(score_rows, key=lambda row: (row["inner_mae_mw"], -row["alpha"]))
    return selected["alpha"], fold_rows, score_rows


def evaluate(frame, positions=None):
    if positions is None:
        positions = np.flatnonzero(frame["date"].ge(original.FIRST_FORECAST_MONTH))
    predictions, folds, scores, choices = [], [], [], []
    for position in positions:
        current = frame.iloc[position]
        history = frame.iloc[:position]
        for unit, label in original.UNITS.items():
            values = history[f"{unit}_average_mw"].to_numpy()
            months = history["month"].tolist()
            alpha, inner_folds, inner_scores = select_alpha(values, months)
            prediction, model = fit_predict(values, alpha)
            context = {"unit": label, "forecast_month": current["month"]}
            folds.extend([{**context, **row} for row in inner_folds])
            scores.extend([{**context, **row, "selected": row["alpha"] == alpha} for row in inner_scores])
            audit = {
                **context, "selected_alpha": alpha, "training_end_month": months[-1],
                "history_months": len(values), "scaler_fit_rows": int(model.named_steps["standardscaler"].n_samples_seen_),
                "inner_first_month": months[MINIMUM_INNER_HISTORY], "inner_last_month": months[-1],
                "inner_forecasts": len(values) - MINIMUM_INNER_HISTORY,
            }
            choices.append(audit)
            actual = float(current[f"{unit}_average_mw"])
            hours = int(current["hours_in_month"])
            error = prediction - actual
            predictions.append({
                **context, "method": "ridge_tuned", "training_end_month": months[-1],
                "selected_alpha": alpha, "actual_average_mw": actual, "forecast_average_mw": prediction,
                "error_mw": error, "absolute_error_mw": abs(error), "squared_error_mw": error ** 2,
                "hours_in_target_month": hours, "forecast_mwh": prediction * hours,
                "error_mwh": error * hours, "absolute_error_mwh": abs(error * hours),
            })
    return tuple(pd.DataFrame(rows) for rows in (predictions, folds, scores, choices))


def validate(frame, tuned, folds, scores, choices, combined, metrics):
    assert len(tuned) == 36 and len(choices) == 36 and len(combined) == 144
    assert (folds["inner_training_end_month"] < folds["inner_forecast_month"]).all()
    assert (folds["inner_forecast_month"] < folds["forecast_month"]).all()
    assert (folds["scaler_fit_rows"] == folds["inner_history_months"] - 3).all()
    assert (choices["scaler_fit_rows"] == choices["history_months"] - 3).all()
    assert choices["inner_forecasts"].min() == 12 and choices["inner_forecasts"].max() == 29
    expected_dates = list(pd.date_range("2020-01-01", "2021-06-01", freq="MS").strftime("%Y-%m"))
    for _, part in combined.groupby(["unit", "method"]):
        assert part["forecast_month"].tolist() == expected_dates
    recomputed = folds.groupby(["unit", "forecast_month", "alpha"])["absolute_error_mw"].mean()
    for _, row in scores.iterrows():
        assert np.isclose(row["inner_mae_mw"], recomputed.loc[(row["unit"], row["forecast_month"], row["alpha"])])
    for (unit, month), part in scores.groupby(["unit", "forecast_month"]):
        best = part.sort_values(["inner_mae_mw", "alpha"], ascending=[True, False]).iloc[0]
        choice = choices[choices["unit"].eq(unit) & choices["forecast_month"].eq(month)].iloc[0]
        assert choice["selected_alpha"] == best["alpha"]
    manual_maximum_difference = 0.0
    for _, row in tuned.iterrows():
        unit = next(key for key, label in original.UNITS.items() if label == row["unit"])
        values = frame.loc[frame["month"].lt(row["forecast_month"]), f"{unit}_average_mw"].to_numpy()
        features = np.asarray([values[position - 3:position][::-1] for position in range(3, len(values))])
        means, scales = features.mean(axis=0), features.std(axis=0)
        scales = np.where(scales == 0, 1.0, scales)
        standardized = (features - means) / scales
        targets = values[3:]
        coefficients = np.linalg.solve(standardized.T @ standardized + row["selected_alpha"] * np.eye(3), standardized.T @ (targets - targets.mean()))
        manual = float(targets.mean() + ((values[-3:][::-1] - means) / scales) @ coefficients)
        manual_maximum_difference = max(manual_maximum_difference, abs(manual - row["forecast_average_mw"]))
        assert np.isclose(manual, row["forecast_average_mw"], rtol=0, atol=1e-8)
    maximum_delta = 0.0
    for position in np.flatnonzero(frame["date"].ge(original.FIRST_FORECAST_MONTH)):
        altered = frame.copy()
        for unit in original.UNITS:
            altered.loc[position:, f"{unit}_average_mw"] += 10000
        changed, changed_folds, changed_scores, changed_choices = evaluate(altered, positions=[position])
        month = frame.iloc[position]["month"]
        expected = tuned[tuned["forecast_month"].eq(month)]
        delta = float(np.max(np.abs(changed["forecast_average_mw"].to_numpy() - expected["forecast_average_mw"].to_numpy())))
        maximum_delta = max(maximum_delta, delta)
        assert delta == 0
        assert changed_choices["selected_alpha"].tolist() == expected["selected_alpha"].tolist()
        pd.testing.assert_frame_equal(changed_scores.reset_index(drop=True), scores[scores["forecast_month"].eq(month)].reset_index(drop=True))
        pd.testing.assert_frame_equal(changed_folds.reset_index(drop=True), folds[folds["forecast_month"].eq(month)].reset_index(drop=True))
    for alpha in ALPHAS:
        constant, _ = fit_predict(np.full(24, 100.0), alpha)
        assert np.isclose(constant, 100)
    for _, row in metrics.iterrows():
        part = combined[combined["unit"].eq(row["unit"]) & combined["method"].eq(row["method"])]
        errors = part["forecast_average_mw"].to_numpy() - part["actual_average_mw"].to_numpy()
        assert np.isclose(row["mae_mw"], np.abs(errors).mean())
        assert np.isclose(row["rmse_mw"], np.sqrt((errors ** 2).mean()))
    return {
        "status": "passed", "all_methods_same_18_dates": True,
        "inner_training_and_validation_strictly_before_outer_date": True,
        "inner_and_outer_training_only_scaler_counts": True,
        "inner_scores_and_alpha_choices_recomputed": True,
        "all_18_origins_current_future_perturbation_preserves_predictions_choices_and_inner_scores": True,
        "maximum_perturbation_difference_mw": maximum_delta,
        "manual_numpy_check_all_36_tuned_forecasts_maximum_difference_mw": manual_maximum_difference,
        "constant_series_all_alphas_checked": True, "metrics_recomputed": True,
        "source_sha256": original.SOURCE_SHA256,
    }


def save_chart(metrics):
    colors = ["#26728e", "#bc681b", "#7752a1", "#16816b"]
    figure, axes = plt.subplots(2, 2, figsize=(12, 7), constrained_layout=True)
    for row_index, unit in enumerate(original.UNITS.values()):
        part = metrics[metrics["unit"].eq(unit)].set_index("method").loc[list(LABELS)]
        for column_index, (metric, label) in enumerate([("mae_mw", "MAE"), ("rmse_mw", "RMSE")]):
            axis = axes[row_index, column_index]
            values = part[metric].to_numpy()
            axis.barh(list(LABELS.values()), values, color=colors)
            axis.invert_yaxis()
            axis.set(title=f"{unit}: {label}", xlabel="Forecast error (MW); lower is better", xlim=(0, values.max() * 1.26))
            for position, value in enumerate(values):
                axis.text(value + values.max() * 0.025, position, f"{value:.3f}", va="center", fontsize=10)
            axis.spines[["top", "right"]].set_visible(False)
    figure.suptitle("Wayang Windu: past-only Ridge tuning\n18 one-month forecasts per unit, January 2020-June 2021", fontsize=14)
    figure.savefig(OUTPUT_DIR / "tuning_comparison.png", dpi=180)
    plt.close(figure)


def write_report(metrics, choices):
    lines = [
        "# Exploratory Ridge Hyperparameter Tuning", "",
        "This follow-up tested whether selecting Ridge's regularisation strength from earlier observations improved Wayang Windu monthly average power forecasts. The original experiment and its output files were preserved.", "",
        "## Methods", "",
        "The source remains 42 months per unit, January 2018-June 2021, at one field. Monthly average MW equals published Main Meter MWh divided by calendar hours. No new observations, operational variables or New Zealand data were added.", "",
        "At each outer forecast month, alpha was selected separately for each unit from 0.01, 0.1, 1, 10, 100 and 1000. Within the available history, training began with January-December 2018; an inner one-month-ahead forecast was made for January 2019, then the actual observation was added and the process repeated through the last observed month. Each candidate's inner MAE was calculated over these dates. The lowest inner MAE selected alpha; exact ties preferred larger alpha. Each inner fit used its own training-only scaler and previous-three-month inputs. The selected model was then refitted on all history preceding the outer date.", "",
        "For the January 2020 outer forecast, selection used only the 12 inner forecasts from January-December 2019. For February 2020, January 2020 could join the inner validation history because it was now observed. Across the experiment there were 12-29 inner forecast dates per choice, not independent new data. The original January 2020-June 2021 outer dates were retained: 18 expanding one-month-ahead forecasts per unit. The first inner model had nine three-lag supervised examples; the first outer model had 21. Selection optimised MAE only, not RMSE. Grid, objective and windows were written in tuning_protocol.json before calculating tuned scores.", "",
        "## Results", "", "| Unit | Method | MAE (MW) | RMSE (MW) |", "|---|---|---:|---:|",
    ]
    for _, row in metrics.iterrows():
        lines.append(f"| {row['unit']} | {LABELS[row['method']]} | {row['mae_mw']:.3f} | {row['rmse_mw']:.3f} |")
    lines += ["", "## Comparison with fixed alpha=10", ""]
    for unit in original.UNITS.values():
        part = metrics[metrics["unit"].eq(unit)].set_index("method")
        fixed, tuned = part.loc["ridge"], part.loc["ridge_tuned"]
        mae_change = (tuned["mae_mw"] / fixed["mae_mw"] - 1) * 100
        rmse_change = (tuned["rmse_mw"] / fixed["rmse_mw"] - 1) * 100
        counts = choices[choices["unit"].eq(unit)]["selected_alpha"].value_counts().sort_index()
        lines.append(f"- {unit}: tuning changed MAE by {mae_change:+.2f}% and RMSE by {rmse_change:+.2f}% relative to fixed Ridge (negative means improvement). Selected alpha counts: " + ", ".join(f"{alpha:g}: {count} months" for alpha, count in counts.items()) + ".")
        best_mae = part["mae_mw"].idxmin()
        best_rmse = part["rmse_mw"].idxmin()
        lines.append(f"  Lowest MAE among all four methods: {LABELS[best_mae]}; lowest RMSE: {LABELS[best_rmse]}.")
    lines += [
        "", "## Interpretation and limits", "",
        "Tuning selects the alpha that worked best in earlier inner validation months; it does not guarantee that alpha will forecast the next month best. Selecting for MAE also does not guarantee improved RMSE. Different temporal windows, objectives or grids would be additional experiments, not reasons to silently replace this protocol after viewing results.", "",
        "This follow-up was motivated by the original results, and the full period had already informed EDA. Although all inner selection is past-only in observation time, these are reused exploratory outer dates, not a new untouched confirmatory test. The revised monitoring data do not reconstruct real-time reporting availability. Only 18 outer dates and two units at one field were evaluated; no statistical significance or future/general superiority is claimed. Results do not validate transfer learning, long-horizon generation, avoided grid emissions or issued credits.", "",
        "## Files", "",
        "tuning_comparison.png contains all four methods. alpha_choices.csv records each decision; inner_candidate_scores.csv and inner_fold_predictions.csv expose every selection fold. rolling_predictions.csv and forecast_metrics.csv retain all four methods. validation_checks.json records chronology, scaler, manual NumPy, metric and future-perturbation checks.",
    ]
    (OUTPUT_DIR / "tuning_results.md").write_text("\n".join(lines) + "\n")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    frame = original.load_data()
    baseline, _ = original.evaluate(frame)
    saved = pd.read_csv(ROOT / "output/rolling_predictions.csv")
    pd.testing.assert_frame_equal(baseline, saved, check_dtype=False, atol=1e-8, rtol=0)
    tuned, folds, scores, choices = evaluate(frame)
    combined = pd.concat([baseline, tuned], ignore_index=True)
    metrics = original.metrics_table(combined)
    validation = validate(frame, tuned, folds, scores, choices, combined, metrics)
    for name, result in [
        ("rolling_predictions", combined), ("forecast_metrics", metrics),
        ("inner_fold_predictions", folds), ("inner_candidate_scores", scores), ("alpha_choices", choices),
    ]:
        result.to_csv(OUTPUT_DIR / f"{name}.csv", index=False, float_format="%.10f")
    (OUTPUT_DIR / "validation_checks.json").write_text(json.dumps(validation, indent=2) + "\n")
    (OUTPUT_DIR / "evaluation_protocol.json").write_text(json.dumps({
        **PROTOCOL, "protocol_sha256": hashlib.sha256(PROTOCOL_FILE.read_bytes()).hexdigest(),
        "source_sha256": original.SOURCE_SHA256, "original_prediction_comparison": "matched saved original run",
    }, indent=2) + "\n")
    save_chart(metrics)
    write_report(metrics, choices)
    print(metrics[["unit", "method", "mae_mw", "rmse_mw"]].to_string(index=False))
    print("Validation:", validation["status"])


if __name__ == "__main__":
    main()
