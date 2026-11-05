"""Compare simple and machine-learning forecasts of Indonesian electricity use.

Target: World Bank annual electric power consumption, kWh per person.
Evaluation: rolling one-year-ahead forecasts for 2008-2024.

Run from this directory with:
    python3 forecast_electricity_consumption.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "world_bank_indonesia_electricity_consumption_per_capita_1990_2024.csv"
FEATURE_FILE = ROOT / "data" / "world_bank_predictor_features_indonesia_1990_2024.csv"
OUTPUT_DIR = ROOT / "output"
FIRST_TEST_YEAR = 2008
LAG_COUNT = 3
MACRO_FEATURES = [
    "gdp_per_capita_ppp_2021_usd",
    "industry_value_added_pct_gdp",
    "access_to_electricity_pct",
]


def load_data():
    data = pd.read_csv(DATA_FILE).sort_values("year").reset_index(drop=True)
    features = pd.read_csv(FEATURE_FILE).sort_values("year").reset_index(drop=True)
    data = data.merge(features, on="year", how="left", validate="one_to_one")
    expected_years = list(range(1990, 2025))
    if data["year"].tolist() != expected_years:
        raise ValueError("Expected one complete annual observation for every year from 1990 to 2024.")
    if data["electricity_consumption_kwh_per_capita"].isna().any():
        raise ValueError("The target series contains missing values.")
    return data


def make_lagged_training_data(history, include_macro_features=False):
    """Create examples with year and the previous three observed values as inputs."""
    years = history["year"].to_numpy(dtype=float)
    values = history["electricity_consumption_kwh_per_capita"].to_numpy(dtype=float)
    features, targets = [], []
    for i in range(LAG_COUNT, len(values)):
        row = [years[i], *values[i - LAG_COUNT : i][::-1]]
        if include_macro_features:
            row.extend(history.iloc[i - 1][MACRO_FEATURES].to_numpy(dtype=float))
        features.append(row)
        targets.append(values[i])
    return np.asarray(features, dtype=float), np.asarray(targets, dtype=float)


def forecast_one_year(history, target_year):
    years = history["year"].to_numpy(dtype=float)
    values = history["electricity_consumption_kwh_per_capita"].to_numpy(dtype=float)

    forecasts = {"previous_year": float(values[-1])}

    slope, intercept = np.polyfit(years, values, deg=1)
    forecasts["linear_trend"] = float(slope * target_year + intercept)

    x_train, y_train = make_lagged_training_data(history)
    recent_values = list(values[-LAG_COUNT:][::-1])
    x_next = np.asarray([[target_year, *recent_values]], dtype=float)

    # Alpha is fixed for this exploratory comparison; no test-year tuning is done.
    ridge = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    ridge.fit(x_train, y_train)
    forecasts["ridge_regression"] = float(ridge.predict(x_next)[0])

    # A deliberately constrained forest reduces the chance of fitting tiny samples.
    forest = RandomForestRegressor(
        n_estimators=400,
        max_depth=2,
        min_samples_leaf=3,
        max_features=1.0,
        random_state=42,
    )
    forest.fit(x_train, y_train)
    forecasts["random_forest"] = float(forest.predict(x_next)[0])

    # Macro features are lagged one year, so every predictor is known by the forecast origin.
    x_macro_train, y_macro_train = make_lagged_training_data(history, include_macro_features=True)
    x_macro_next = np.asarray(
        [[target_year, *recent_values, *history.iloc[-1][MACRO_FEATURES].to_numpy(dtype=float)]],
        dtype=float,
    )
    ridge_macro = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    ridge_macro.fit(x_macro_train, y_macro_train)
    forecasts["ridge_plus_macro_features"] = float(ridge_macro.predict(x_macro_next)[0])

    forest_macro = RandomForestRegressor(
        n_estimators=400,
        max_depth=2,
        min_samples_leaf=3,
        max_features=1.0,
        random_state=42,
    )
    forest_macro.fit(x_macro_train, y_macro_train)
    forecasts["random_forest_plus_macro_features"] = float(forest_macro.predict(x_macro_next)[0])
    return forecasts


def rolling_evaluation(data):
    rows = []
    for target_year in range(FIRST_TEST_YEAR, int(data["year"].max()) + 1):
        history = data[data["year"] < target_year]
        actual = float(
            data.loc[data["year"].eq(target_year), "electricity_consumption_kwh_per_capita"].iloc[0]
        )
        forecasts = forecast_one_year(history, target_year)
        for method, prediction in forecasts.items():
            rows.append({
                "forecast_year": target_year,
                "training_start_year": int(history["year"].min()),
                "training_end_year": int(history["year"].max()),
                "training_observations": len(history),
                "actual_kwh_per_capita": actual,
                "method": method,
                "forecast_kwh_per_capita": prediction,
                "error_kwh_per_capita": prediction - actual,
                "absolute_error_kwh_per_capita": abs(prediction - actual),
                "absolute_percentage_error": abs(prediction - actual) / actual * 100,
            })
    return pd.DataFrame(rows)


def summarize(predictions):
    summary = (
        predictions.groupby("method", as_index=False)
        .agg(
            forecast_years=("forecast_year", "count"),
            mae_kwh_per_capita=("absolute_error_kwh_per_capita", "mean"),
            rmse_kwh_per_capita=("error_kwh_per_capita", lambda x: np.sqrt(np.mean(np.square(x)))),
            mape_pct=("absolute_percentage_error", "mean"),
        )
        .sort_values("mape_pct")
    )
    return summary


def save_plot(data, predictions):
    actual = data[data["year"] >= FIRST_TEST_YEAR]
    wide = predictions.pivot(index="forecast_year", columns="method", values="forecast_kwh_per_capita")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(actual["year"], actual["electricity_consumption_kwh_per_capita"], color="#222222",
            marker="o", linewidth=2.5, label="Observed")
    styles = {
        "previous_year": ("#287d8e", "Previous year"),
        "linear_trend": ("#e58b37", "Linear trend"),
        "ridge_regression": ("#7b61a8", "Ridge regression"),
        "random_forest": ("#4f8a5b", "Random Forest"),
        "ridge_plus_macro_features": ("#b54a6a", "Ridge + macro features"),
        "random_forest_plus_macro_features": ("#6797bd", "Random Forest + macro features"),
    }
    for method, (color, label) in styles.items():
        ax.plot(wide.index, wide[method], marker=".", linewidth=1.5, color=color, label=label)
    ax.set_title("Rolling one-year-ahead forecasts of electricity consumption per person")
    ax.set_xlabel("Year")
    ax.set_ylabel("kWh per person")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "forecast_comparison.png", dpi=180)
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load_data()
    predictions = rolling_evaluation(data)
    summary = summarize(predictions)
    predictions.to_csv(OUTPUT_DIR / "rolling_forecast_predictions.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "forecast_metrics.csv", index=False)
    save_plot(data, predictions)
    print(f"Target data: {data.year.min()}-{data.year.max()} ({len(data)} annual observations)")
    print(f"Evaluation: {FIRST_TEST_YEAR}-{data.year.max()} ({predictions.forecast_year.nunique()} forecast years)")
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.2f}"))


if __name__ == "__main__":
    main()
