"""Plot saved tuned forecasts without refitting models or changing results."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


OUTPUT = Path(__file__).resolve().parent / "output" / "tuning"
METHODS = {
    "previous_month": ("Previous month", "#237c98", "--"),
    "trailing_three_month_mean": ("Three-month mean", "#d26810", "--"),
    "ridge": ("Ridge: fixed alpha = 10", "#8054b1", "--"),
    "ridge_tuned": ("Ridge: tuned alpha", "#18864b", "-"),
}


def main():
    predictions = pd.read_csv(OUTPUT / "rolling_predictions.csv")
    predictions["forecast_month"] = pd.to_datetime(predictions["forecast_month"])
    expected_dates = pd.date_range("2020-01-01", "2021-06-01", freq="MS")
    assert not predictions.duplicated(["unit", "forecast_month", "method"]).any()
    assert set(predictions["method"]) == set(METHODS)
    figure, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    for axis, unit in zip(axes, ["Unit 1", "Unit 2"]):
        data = predictions[predictions["unit"].eq(unit)]
        assert data.groupby("forecast_month")["actual_average_mw"].nunique().eq(1).all()
        observed = data.drop_duplicates("forecast_month").sort_values("forecast_month")
        assert observed["forecast_month"].tolist() == expected_dates.tolist()
        axis.plot(observed["forecast_month"], observed["actual_average_mw"],
                  color="#252525", marker="o", linewidth=2.3, markersize=5.5,
                  label="Observed", zorder=5)
        for method, (label, color, style) in METHODS.items():
            part = data[data["method"].eq(method)].sort_values("forecast_month")
            assert part["forecast_month"].tolist() == expected_dates.tolist()
            assert part["training_end_month"].lt(part["forecast_month"].dt.strftime("%Y-%m")).all()
            axis.plot(part["forecast_month"], part["forecast_average_mw"],
                      label=label, color=color, linestyle=style,
                      marker="s" if method == "ridge_tuned" else "o",
                      linewidth=2 if method == "ridge_tuned" else 1.4,
                      markersize=3.5 if method == "ridge_tuned" else 2.5)
        axis.set_title(unit)
        axis.set_ylabel("Monthly average power (MW)")
        axis.grid(alpha=0.2)
        axis.spines[["top", "right"]].set_visible(False)
    axes[1].set_xlabel("Forecast month")
    axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    figure.suptitle("Wayang Windu: forecasts with past-only hyperparameter tuning\n"
                    "Exploratory rolling one-month-ahead forecasts: January 2020–June 2021", fontsize=13)
    figure.legend(*axes[0].get_legend_handles_labels(), loc="lower center",
                  bbox_to_anchor=(0.5, 0.055), ncol=3, fontsize=10, frameon=False)
    figure.text(0.5, 0.015,
                "Tuned alpha selected using earlier inner-validation MAE at each forecast date.\n"
                "Panels use different vertical scales; saved forecasts only, no new model fitting.",
                ha="center", fontsize=9)
    figure.tight_layout(rect=(0, 0.15, 1, 0.94))
    path = OUTPUT / "tuned_forecast_comparison.png"
    figure.savefig(path, dpi=240, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(path)


if __name__ == "__main__":
    main()
