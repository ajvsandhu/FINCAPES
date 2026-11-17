#!/usr/bin/env python3
"""Data-gap simulation (option 12): show why coarse data cannot replace interval MEFs.

PUBLIC DEMO — NOT A JAMALI MEF.
Takes hourly EIA-mapped series, estimates a demand MEF, then degrades the same
series to daily / monthly aggregates and shows the estimate collapsing or biasing.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEMO = HERE / "public_demo"
OUT = HERE / "outputs_data_gap"
BAS = ("MISO", "CISO")  # coal-heavier vs cleaner contrast


def fit_beta(x: np.ndarray, y: np.ndarray) -> dict:
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 3:
        return {"beta": np.nan, "r2": np.nan, "n": int(len(x)), "se": np.nan}
    xd, yd = x - x.mean(), y - y.mean()
    ss_xx = float(np.dot(xd, xd))
    if ss_xx == 0:
        return {"beta": np.nan, "r2": np.nan, "n": int(len(x)), "se": np.nan}
    beta = float(np.dot(xd, yd) / ss_xx)
    resid = y - (y.mean() - beta * x.mean() + beta * x)
    ss_tot = float(np.dot(yd, yd))
    r2 = float(1 - np.dot(resid, resid) / ss_tot) if ss_tot else np.nan
    se = float(np.sqrt((np.dot(resid, resid) / max(len(x) - 2, 1)) / ss_xx))
    return {"beta": beta, "r2": r2, "n": int(len(x)), "se": se}


def mef_from_levels(df: pd.DataFrame, demand_col: str, co2_col: str) -> dict:
    d = df[demand_col].diff()
    e = df[co2_col].diff()
    return fit_beta(d.to_numpy(), e.to_numpy())


def analyse(ba: str) -> dict:
    df = pd.read_csv(DEMO / f"{ba.lower()}_2024H1_interval_operations.csv", parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    hourly = mef_from_levels(df, "demand_mwh", "co2_tonnes")

    daily = (
        df.set_index("timestamp")
        .resample("D")
        .agg({"demand_mwh": "sum", "co2_tonnes": "sum"})
        .dropna()
        .reset_index()
    )
    daily_mef = mef_from_levels(daily, "demand_mwh", "co2_tonnes")

    monthly = (
        df.set_index("timestamp")
        .resample("MS")
        .agg({"demand_mwh": "sum", "co2_tonnes": "sum"})
        .dropna()
        .reset_index()
    )
    monthly_mef = mef_from_levels(monthly, "demand_mwh", "co2_tonnes")

    # Annual-like: only one period total => cannot form Δ regression at all.
    annual_like = {
        "beta": np.nan,
        "r2": np.nan,
        "n": 1,
        "se": np.nan,
        "note": "single aggregate period; regression of changes impossible",
    }

    return {
        "ba": ba,
        "hourly": hourly,
        "daily": daily_mef,
        "monthly": monthly_mef,
        "annual_like": annual_like,
        "n_hourly": len(df),
        "n_daily": len(daily),
        "n_monthly": len(monthly),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    results = []
    for ba in BAS:
        r = analyse(ba)
        results.append(r)
        for freq in ("hourly", "daily", "monthly", "annual_like"):
            fit = r[freq]
            rows.append(
                {
                    "ba": ba,
                    "frequency": freq,
                    "beta_tco2_per_mwh": fit.get("beta"),
                    "r2": fit.get("r2"),
                    "n_obs_after_diff": max(fit.get("n", 0) - 1, 0) if freq != "annual_like" else 0,
                    "n_periods": fit.get("n"),
                    "note": fit.get("note", ""),
                }
            )
    summary = pd.DataFrame(rows)
    summary.to_csv(OUT / "data_gap_summary.csv", index=False)

    # Bar chart of betas by frequency for each BA
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    order = ["hourly", "daily", "monthly"]
    for ax, ba in zip(axes, BAS):
        part = summary[(summary["ba"] == ba) & (summary["frequency"].isin(order))]
        vals = [part.loc[part["frequency"] == f, "beta_tco2_per_mwh"].iloc[0] for f in order]
        ax.bar(order, vals, color=["#2f5d8a", "#6b8f71", "#c4a35a"])
        ax.set_title(ba)
        ax.set_ylabel("Demand MEF β (tCO₂/MWh)")
        ax.axhline(0, color="#999", lw=0.8)
    fig.suptitle("Data-gap simulation: MEF estimate under coarser aggregation")
    fig.text(
        0.02,
        0.01,
        "PUBLIC DEMO — NOT JAMALI. Annual totals cannot support a change-on-change regression at all.",
        fontsize=8,
        color="#a35d4a",
    )
    fig.tight_layout()
    fig.savefig(OUT / "data_gap_mef_by_frequency.png", dpi=160)
    plt.close(fig)

    (OUT / "data_gap_summary.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    (OUT / "NOT_JAMALI_MEF.txt").write_text(
        "DATA-GAP SIMULATION ON PUBLIC EIA SERIES\nNot a Jamali MEF.\n",
        encoding="utf-8",
    )
    print(summary.to_string(index=False))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
