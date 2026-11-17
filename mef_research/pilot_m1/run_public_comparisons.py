#!/usr/bin/env python3
"""Public-demo modelling extensions (NOT Jamali):

1. AEF vs demand-based MEF
2. Demand MEF vs fossil-generation MEF
3. Multi-BA comparison including coal-heavier systems (MISO, PJM)

Uses mapped EIA-930 interval files from prepare_eia930_demo.py.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEMO = HERE / "public_demo"
OUT = HERE / "outputs_public_compare"
BAS = ("CISO", "ERCO", "MISO", "PJM")
TRAIN_FRACTION = 0.75


def fit_beta(x: np.ndarray, y: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 3:
        raise ValueError("need >=3 points")
    x_mean, y_mean = x.mean(), y.mean()
    xd, yd = x - x_mean, y - y_mean
    ss_xx = float(np.dot(xd, xd))
    if ss_xx == 0:
        raise ValueError("zero variance in x")
    beta = float(np.dot(xd, yd) / ss_xx)
    alpha = float(y_mean - beta * x_mean)
    resid = y - (alpha + beta * x)
    dof = max(len(x) - 2, 1)
    sigma2 = float(np.dot(resid, resid) / dof)
    ss_tot = float(np.dot(yd, yd))
    r2 = float(1.0 - np.dot(resid, resid) / ss_tot) if ss_tot > 0 else float("nan")
    return {
        "alpha": alpha,
        "beta": beta,
        "se_beta": float(np.sqrt(sigma2 / ss_xx)),
        "r2": r2,
        "n": int(len(x)),
    }


def load_ba(ba: str) -> pd.DataFrame:
    path = DEMO / f"{ba.lower()}_2024H1_interval_operations.csv"
    df = pd.read_csv(path, parse_dates=["timestamp"]).sort_values("timestamp")
    df["fossil_mwh"] = df["gen_coal_mwh"] + df["gen_gas_mwh"] + df["gen_oil_mwh"]
    df["delta_demand"] = df["demand_mwh"].diff()
    df["delta_fossil"] = df["fossil_mwh"].diff()
    df["delta_co2"] = df["co2_tonnes"].diff()
    df["hour"] = df["timestamp"].dt.hour
    return df.dropna(subset=["delta_demand", "delta_fossil", "delta_co2"]).copy()


def analyse_ba(ba: str) -> dict:
    df = load_ba(ba)
    split = int(len(df) * TRAIN_FRACTION)
    train, test = df.iloc[:split], df.iloc[split:]

    demand_fit = fit_beta(train["delta_demand"].to_numpy(), train["delta_co2"].to_numpy())
    fossil_fit = fit_beta(train["delta_fossil"].to_numpy(), train["delta_co2"].to_numpy())

    # AEF over full sample: total constructed CO2 / total demand
    aef = float(df["co2_tonnes"].sum() / df["demand_mwh"].sum())
    # Also report generation-weighted AEF using fossil+other constructed emissions already in co2
    aef_vs_demand_mef_pct = (aef - demand_fit["beta"]) / demand_fit["beta"] * 100.0

    # Test R2 using training demand beta
    test_pred = demand_fit["alpha"] + demand_fit["beta"] * test["delta_demand"]
    ss_tot = float(((test["delta_co2"] - test["delta_co2"].mean()) ** 2).sum())
    test_r2 = float(1.0 - ((test["delta_co2"] - test_pred) ** 2).sum() / ss_tot) if ss_tot else float("nan")

    # Coal share of fossil energy (context, not a MEF)
    fossil_total = float(df["fossil_mwh"].sum())
    coal_share = float(df["gen_coal_mwh"].sum() / fossil_total) if fossil_total else float("nan")

    hour_rows = []
    for hour, part in train.groupby("hour"):
        if len(part) < 20:
            continue
        dfit = fit_beta(part["delta_demand"].to_numpy(), part["delta_co2"].to_numpy())
        ffit = fit_beta(part["delta_fossil"].to_numpy(), part["delta_co2"].to_numpy())
        hour_rows.append(
            {
                "ba": ba,
                "hour": int(hour),
                "demand_mef": dfit["beta"],
                "fossil_mef": ffit["beta"],
                "n": dfit["n"],
            }
        )

    return {
        "ba": ba,
        "n_hours": int(len(df) + 1),  # approximate; after diff lost 1
        "n_train": demand_fit["n"],
        "aef_tco2_per_mwh": aef,
        "demand_mef_tco2_per_mwh": demand_fit["beta"],
        "demand_mef_se": demand_fit["se_beta"],
        "demand_mef_r2": demand_fit["r2"],
        "demand_mef_test_r2": test_r2,
        "fossil_mef_tco2_per_mwh": fossil_fit["beta"],
        "fossil_mef_se": fossil_fit["se_beta"],
        "fossil_mef_r2": fossil_fit["r2"],
        "aef_minus_demand_mef_pct": aef_vs_demand_mef_pct,
        "coal_share_of_fossil": coal_share,
        "hour_profile": hour_rows,
    }


def plot_aef_vs_mef(summary: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    x = np.arange(len(summary))
    width = 0.35
    ax.bar(x - width / 2, summary["aef_tco2_per_mwh"], width, label="AEF (avg intensity)", color="#6b8f71")
    ax.bar(x + width / 2, summary["demand_mef_tco2_per_mwh"], width, label="Demand MEF (β)", color="#2f5d8a")
    ax.set_xticks(x)
    ax.set_xticklabels(summary["ba"])
    ax.set_ylabel("tCO₂ / MWh")
    ax.set_title("Public demo: AEF vs demand-based MEF")
    ax.legend()
    ax.text(
        0.02,
        0.02,
        "PUBLIC EIA-930 DEMO — NOT JAMALI. Constructed CO₂; Jan–Jun 2024.",
        transform=ax.transAxes,
        fontsize=8,
        color="#a35d4a",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_demand_vs_fossil(summary: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    x = np.arange(len(summary))
    width = 0.35
    ax.bar(x - width / 2, summary["demand_mef_tco2_per_mwh"], width, label="ΔCO₂ ~ Δdemand", color="#2f5d8a")
    ax.bar(x + width / 2, summary["fossil_mef_tco2_per_mwh"], width, label="ΔCO₂ ~ Δfossil gen", color="#a35d4a")
    ax.set_xticks(x)
    ax.set_xticklabels(summary["ba"])
    ax.set_ylabel("MEF β (tCO₂ / MWh)")
    ax.set_title("Public demo: demand MEF vs fossil-generation MEF")
    ax.legend()
    ax.text(
        0.02,
        0.02,
        "PUBLIC EIA-930 DEMO — NOT JAMALI. Same constructed CO₂; estimand differs.",
        transform=ax.transAxes,
        fontsize=8,
        color="#a35d4a",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_multi_ba_hour(profiles: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    for ba, part in profiles.groupby("ba"):
        part = part.sort_values("hour")
        ax.plot(part["hour"], part["demand_mef"], "-o", label=ba, markersize=3)
    ax.set_xlabel("Local hour of day")
    ax.set_ylabel("Demand MEF β (tCO₂ / MWh)")
    ax.set_title("Public demo: hour-of-day demand MEFs across balancing authorities")
    ax.set_xticks(range(0, 24, 2))
    ax.legend()
    ax.text(
        0.02,
        0.02,
        "PUBLIC EIA-930 DEMO — NOT JAMALI. Training-period hour profiles.",
        transform=ax.transAxes,
        fontsize=8,
        color="#a35d4a",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    results = [analyse_ba(ba) for ba in BAS]
    hour_profiles = pd.DataFrame([row for r in results for row in r["hour_profile"]])
    summary = pd.DataFrame([{k: v for k, v in r.items() if k != "hour_profile"} for r in results])

    summary_path = OUT / "comparison_summary.csv"
    hour_path = OUT / "hour_profiles_demand_mef.csv"
    summary.to_csv(summary_path, index=False)
    hour_profiles.to_csv(hour_path, index=False)

    plot_aef_vs_mef(summary, OUT / "aef_vs_demand_mef.png")
    plot_demand_vs_fossil(summary, OUT / "demand_vs_fossil_mef.png")
    plot_multi_ba_hour(hour_profiles, OUT / "multi_ba_hour_demand_mef.png")

    meta = {
        "disclaimer": "PUBLIC EIA-930 DEMO — NOT A JAMALI MEF",
        "period": "2024-01 to 2024-06",
        "bas": list(BAS),
        "co2": "constructed from fuel generation x constant intensities",
        "train_fraction": TRAIN_FRACTION,
        "summary": summary.to_dict(orient="records"),
    }
    (OUT / "comparison_summary.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (OUT / "NOT_JAMALI_MEF.txt").write_text(
        "PUBLIC DEMO OUTPUTS ONLY\nNot Jamali MEFs. Not official US policy factors.\n",
        encoding="utf-8",
    )

    print(summary[
        [
            "ba",
            "aef_tco2_per_mwh",
            "demand_mef_tco2_per_mwh",
            "fossil_mef_tco2_per_mwh",
            "aef_minus_demand_mef_pct",
            "coal_share_of_fossil",
            "demand_mef_r2",
            "fossil_mef_r2",
        ]
    ].to_string(index=False))
    print(f"Wrote outputs to {OUT}")


if __name__ == "__main__":
    main()
