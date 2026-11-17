#!/usr/bin/env python3
"""Historical-regression short-run MEF pilot (M1).

Default input is the synthetic toy dataset. Pass a real mapped UIP2B CSV later
with --input. Toy outputs are illustrative only and are not Jamali MEFs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "toy_data" / "toy_interval_operations.csv"
DEFAULT_FACTORS = HERE / "toy_data" / "toy_emission_factors.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--factors", type=Path, default=DEFAULT_FACTORS)
    parser.add_argument("--outdir", type=Path, default=None)
    parser.add_argument("--train-fraction", type=float, default=0.75)
    parser.add_argument(
        "--label",
        default="ILLUSTRATIVE SYNTHETIC EXAMPLE — NOT A JAMALI MEF",
        help="Banner written on figures and summary JSON",
    )
    return parser.parse_args()


def load_interval(path: Path, factors_path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    required = [
        "timestamp",
        "demand_mwh",
        "gen_coal_mwh",
        "gen_gas_mwh",
        "gen_oil_mwh",
        "gen_geo_mwh",
        "gen_other_mwh",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Input missing required columns: {missing}")

    if "co2_tonnes" not in df.columns or df["co2_tonnes"].isna().all():
        factors = pd.read_csv(factors_path).set_index("fuel")["tco2_per_mwh"]
        df["co2_tonnes"] = (
            df["gen_coal_mwh"] * float(factors.get("coal", 1.0))
            + df["gen_gas_mwh"] * float(factors.get("gas", 0.42))
            + df["gen_oil_mwh"] * float(factors.get("oil", 0.75))
            + df["gen_geo_mwh"] * float(factors.get("geo", 0.0))
            + df["gen_other_mwh"] * float(factors.get("other", 0.05))
        )
        construction = "constructed_from_fuel_factors"
    else:
        construction = "provided_co2_tonnes"

    df["delta_demand_mwh"] = df["demand_mwh"].diff()
    df["delta_co2_tonnes"] = df["co2_tonnes"].diff()
    df["hour"] = df["timestamp"].dt.hour
    df.attrs["emissions_construction"] = construction
    return df.dropna(subset=["delta_demand_mwh", "delta_co2_tonnes"]).copy()


def fit_beta(x: np.ndarray, y: np.ndarray) -> dict:
    if len(x) < 3:
        raise ValueError("Need at least 3 observations to fit MEF")
    # OLS through demeaned series with intercept suppressed after demeaning
    # is equivalent to with-intercept slope.
    x_mean = x.mean()
    y_mean = y.mean()
    xd = x - x_mean
    yd = y - y_mean
    ss_xx = float(np.dot(xd, xd))
    if ss_xx == 0:
        raise ValueError("Demand changes have zero variance")
    beta = float(np.dot(xd, yd) / ss_xx)
    alpha = float(y_mean - beta * x_mean)
    resid = y - (alpha + beta * x)
    dof = max(len(x) - 2, 1)
    sigma2 = float(np.dot(resid, resid) / dof)
    se_beta = float(np.sqrt(sigma2 / ss_xx))
    y_hat = alpha + beta * x
    ss_tot = float(np.dot(yd, yd))
    r2 = float(1.0 - np.dot(resid, resid) / ss_tot) if ss_tot > 0 else float("nan")
    return {
        "alpha": alpha,
        "beta_tco2_per_mwh": beta,
        "se_beta": se_beta,
        "r2": r2,
        "n": int(len(x)),
        "resid_sd": float(np.sqrt(sigma2)),
    }


def hour_of_day_profile(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for hour, part in df.groupby("hour"):
        fit = fit_beta(part["delta_demand_mwh"].to_numpy(), part["delta_co2_tonnes"].to_numpy())
        rows.append(
            {
                "hour": int(hour),
                "beta_tco2_per_mwh": fit["beta_tco2_per_mwh"],
                "se_beta": fit["se_beta"],
                "r2": fit["r2"],
                "n": fit["n"],
            }
        )
    return pd.DataFrame(rows).sort_values("hour")


def plot_scatter(train: pd.DataFrame, fit: dict, outdir: Path, label: str) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.scatter(
        train["delta_demand_mwh"],
        train["delta_co2_tonnes"],
        s=6,
        alpha=0.25,
        color="#2f5d8a",
        label="Training Δ intervals",
    )
    x_line = np.linspace(train["delta_demand_mwh"].min(), train["delta_demand_mwh"].max(), 100)
    ax.plot(
        x_line,
        fit["alpha"] + fit["beta_tco2_per_mwh"] * x_line,
        color="#a35d4a",
        lw=2,
        label=f"Fit β = {fit['beta_tco2_per_mwh']:.3f} tCO₂/MWh",
    )
    ax.set_xlabel("Δ demand (MWh)")
    ax.set_ylabel("Δ CO₂ (tonnes)")
    ax.set_title("M1 historical regression (training period)")
    ax.legend(loc="best", fontsize=8)
    ax.text(0.02, 0.02, label, transform=ax.transAxes, fontsize=8, color="#a35d4a")
    fig.tight_layout()
    fig.savefig(outdir / "scatter_delta_demand_vs_delta_co2.png", dpi=160)
    plt.close(fig)


def plot_hour_profile(profile: pd.DataFrame, outdir: Path, label: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.errorbar(
        profile["hour"],
        profile["beta_tco2_per_mwh"],
        yerr=1.96 * profile["se_beta"],
        fmt="-o",
        color="#2f5d8a",
        ecolor="#888",
        capsize=3,
    )
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("MEF β (tCO₂ / MWh)")
    ax.set_title("Hour-of-day MEF profile (training period)")
    ax.set_xticks(range(0, 24, 2))
    ax.text(0.02, 0.02, label, transform=ax.transAxes, fontsize=8, color="#a35d4a")
    fig.tight_layout()
    fig.savefig(outdir / "hour_of_day_mef.png", dpi=160)
    plt.close(fig)


def plot_train_test(train: pd.DataFrame, test: pd.DataFrame, fit: dict, outdir: Path, label: str) -> None:
    def predict(df: pd.DataFrame) -> np.ndarray:
        return fit["alpha"] + fit["beta_tco2_per_mwh"] * df["delta_demand_mwh"].to_numpy()

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    for ax, part, name in (
        (axes[0], train, "Train"),
        (axes[1], test, "Test"),
    ):
        pred = predict(part)
        ax.scatter(part["delta_co2_tonnes"], pred, s=6, alpha=0.25, color="#2f5d8a")
        lims = [
            min(part["delta_co2_tonnes"].min(), pred.min()),
            max(part["delta_co2_tonnes"].max(), pred.max()),
        ]
        ax.plot(lims, lims, color="#a35d4a", lw=1.5)
        ax.set_title(name)
        ax.set_xlabel("Observed Δ CO₂")
        if ax is axes[0]:
            ax.set_ylabel("Predicted Δ CO₂")
    fig.suptitle("Chronological train/test check")
    fig.text(0.02, 0.01, label, fontsize=8, color="#a35d4a")
    fig.tight_layout()
    fig.savefig(outdir / "train_test_predicted_vs_observed.png", dpi=160)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    is_toy = "toy_data" in str(args.input)
    outdir = args.outdir or (HERE / ("outputs_toy" if is_toy else "outputs_run"))
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_interval(args.input, args.factors)
    n = len(df)
    split = int(n * args.train_fraction)
    train = df.iloc[:split].copy()
    test = df.iloc[split:].copy()

    fit_train = fit_beta(train["delta_demand_mwh"].to_numpy(), train["delta_co2_tonnes"].to_numpy())
    fit_test = fit_beta(test["delta_demand_mwh"].to_numpy(), test["delta_co2_tonnes"].to_numpy())
    profile = hour_of_day_profile(train)

    # Test-period fit quality using training β
    test_pred = fit_train["alpha"] + fit_train["beta_tco2_per_mwh"] * test["delta_demand_mwh"]
    test_resid = test["delta_co2_tonnes"] - test_pred
    ss_tot = float(((test["delta_co2_tonnes"] - test["delta_co2_tonnes"].mean()) ** 2).sum())
    test_r2_using_train_beta = float(1.0 - (test_resid**2).sum() / ss_tot) if ss_tot else float("nan")

    summary = {
        "disclaimer": args.label,
        "input": str(args.input),
        "emissions_construction": df.attrs.get("emissions_construction"),
        "n_intervals_after_diff": n,
        "train_fraction": args.train_fraction,
        "train_fit": fit_train,
        "test_refit": fit_test,
        "test_r2_using_train_beta": test_r2_using_train_beta,
        "jamali_mef_claim_allowed": False if is_toy else "only_after_review_of_real_uip2b_inputs",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    profile.to_csv(outdir / "hour_of_day_mef.csv", index=False)

    plot_scatter(train, fit_train, outdir, args.label)
    plot_hour_profile(profile, outdir, args.label)
    plot_train_test(train, test, fit_train, outdir, args.label)

    banner = outdir / "NOT_JAMALI_MEF.txt"
    banner.write_text(
        args.label + "\n"
        "This folder contains dry-run or provisional pilot outputs.\n"
        "Do not copy toy β values into the Jamali findings summary.\n",
        encoding="utf-8",
    )

    print(f"Output directory: {outdir}")
    print(f"Train β = {fit_train['beta_tco2_per_mwh']:.4f} tCO2/MWh "
          f"(SE {fit_train['se_beta']:.4f}, R2 {fit_train['r2']:.3f}, n={fit_train['n']})")
    print(f"Test R2 using train β = {test_r2_using_train_beta:.3f}")
    print(args.label)


if __name__ == "__main__":
    main()
