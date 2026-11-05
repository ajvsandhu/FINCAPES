"""Explore one-year-ahead forecasts of Indonesia's annual electricity demand.

Target: Ember annual electricity demand (generation plus net imports), TWh.
Evaluation: rolling forecasts for 2010-2024. Ember's 2025 estimate is excluded.

Run from this directory with:
    python3 forecast_ember_demand.py
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
DATA_FILE = ROOT / "data" / "ember_indonesia_annual_demand_2000_2025.csv"
OUTPUT_DIR = ROOT / "output" / "ember_demand"
FIRST_TEST_YEAR = 2010
LAST_ACTUAL_YEAR = 2024
LAG_COUNT = 3


def load_data():
    data = pd.read_csv(DATA_FILE).sort_values("year").reset_index(drop=True)
    data = data[data["year"].between(2000, LAST_ACTUAL_YEAR)].reset_index(drop=True)
    expected = list(range(2000, LAST_ACTUAL_YEAR + 1))
    if data["year"].tolist() != expected:
        raise ValueError("Expected one annual Ember demand observation for every year from 2000 to 2024.")
    if data["electricity_demand_twh"].isna().any():
        raise ValueError("The Ember demand series contains missing values.")
    return data


def forecast_one_year(history, target_year):
    years = history["year"].to_numpy(dtype=float)
    values = history["electricity_demand_twh"].to_numpy(dtype=float)
    forecasts = {"previous_year": float(values[-1])}

    slope, intercept = np.polyfit(years, values, deg=1)
    forecasts["linear_trend"] = float(slope * target_year + intercept)

    x_train, y_train = [], []
    for i in range(LAG_COUNT, len(values)):
        x_train.append([years[i], *values[i - LAG_COUNT : i][::-1]])
        y_train.append(values[i])
    x_next = np.asarray([[target_year, *values[-LAG_COUNT:][::-1]],], dtype=float)

    ridge = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    ridge.fit(np.asarray(x_train), np.asarray(y_train))
    forecasts["ridge_regression"] = float(ridge.predict(x_next)[0])

    forest = RandomForestRegressor(
        n_estimators=400,
        max_depth=2,
        min_samples_leaf=3,
        max_features=1.0,
        random_state=42,
    )
    forest.fit(np.asarray(x_train), np.asarray(y_train))
    forecasts["random_forest"] = float(forest.predict(x_next)[0])
    return forecasts


def rolling_evaluation(data):
    rows = []
    for target_year in range(FIRST_TEST_YEAR, LAST_ACTUAL_YEAR + 1):
        history = data[data["year"] < target_year]
        actual = float(data.loc[data["year"].eq(target_year), "electricity_demand_twh"].iloc[0])
        for method, prediction in forecast_one_year(history, target_year).items():
            rows.append({
                "forecast_year": target_year,
                "training_start_year": int(history["year"].min()),
                "training_end_year": int(history["year"].max()),
                "training_observations": len(history),
                "actual_demand_twh": actual,
                "method": method,
                "forecast_demand_twh": prediction,
                "error_twh": prediction - actual,
                "absolute_error_twh": abs(prediction - actual),
                "absolute_percentage_error": abs(prediction - actual) / actual * 100,
            })
    return pd.DataFrame(rows)


def summarize(predictions):
    return (
        predictions.groupby("method", as_index=False)
        .agg(
            forecast_years=("forecast_year", "count"),
            mae_twh=("absolute_error_twh", "mean"),
            rmse_twh=("error_twh", lambda x: np.sqrt(np.mean(np.square(x)))),
            mape_pct=("absolute_percentage_error", "mean"),
        )
        .sort_values("mape_pct")
    )


def save_plot(data, predictions):
    observed = data[data["year"].ge(FIRST_TEST_YEAR)]
    wide = predictions.pivot(index="forecast_year", columns="method", values="forecast_demand_twh")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(observed["year"], observed["electricity_demand_twh"], color="#222222", marker="o",
            linewidth=2.5, label="Observed demand")
    styles = {
        "previous_year": ("#287d8e", "Previous year"),
        "linear_trend": ("#e58b37", "Linear trend"),
        "ridge_regression": ("#7b61a8", "Ridge regression"),
        "random_forest": ("#4f8a5b", "Random Forest"),
    }
    for method, (color, label) in styles.items():
        ax.plot(wide.index, wide[method], marker=".", linewidth=1.5, color=color, label=label)
    ax.set_title("Rolling one-year-ahead forecasts of Indonesia's annual electricity demand")
    ax.set_xlabel("Year")
    ax.set_ylabel("TWh")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "forecast_comparison.png", dpi=180)
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    predictions = rolling_evaluation(data)
    summary = summarize(predictions)
    predictions.to_csv(OUTPUT_DIR / "rolling_forecast_predictions.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "forecast_metrics.csv", index=False)
    save_plot(data, predictions)
    print(f"Target data: 2000-{LAST_ACTUAL_YEAR} ({len(data)} annual observations; 2025 estimate excluded)")
    print(f"Evaluation: {FIRST_TEST_YEAR}-{LAST_ACTUAL_YEAR} ({predictions.forecast_year.nunique()} forecast years)")
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.2f}"))


if __name__ == "__main__":
    main()
