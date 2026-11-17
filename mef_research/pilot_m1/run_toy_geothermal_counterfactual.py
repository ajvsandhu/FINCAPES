#!/usr/bin/env python3
"""Toy with/without geothermal counterfactual (option 5a).

ILLUSTRATIVE SYNTHETIC ONLY — NOT A JAMALI RESULT.
Adds must-run geothermal to the toy merit order and measures displaced fossil
generation and CO2 relative to the baseline toy world.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TOY = HERE / "toy_data" / "toy_interval_operations.csv"
OUT = HERE / "outputs_toy_geothermal"
FACTORS = {"coal": 1.00, "gas": 0.42, "oil": 0.75, "geo": 0.00, "other": 0.05}
# Extra geothermal capacity (MW) tested in the counterfactual.
EXTRA_GEO_MW = 500.0


def dispatch(demand_mw: np.ndarray, geo_extra_mw: float, rng: np.random.Generator) -> pd.DataFrame:
    geo_mw = 700.0 + geo_extra_mw
    other_mw = np.full(len(demand_mw), 800.0)
    coal_ceiling = 14_500.0
    residual = np.maximum(demand_mw - geo_mw - other_mw, 0.0)
    coal_mw = np.minimum(residual, coal_ceiling)
    after_coal = residual - coal_mw
    gas_cap = 6_000.0
    gas_mw = np.minimum(after_coal, gas_cap)
    oil_mw = after_coal - gas_mw

    out = pd.DataFrame(
        {
            "demand_mwh": demand_mw * 0.5,
            "gen_geo_mwh": geo_mw * 0.5,
            "gen_other_mwh": other_mw * 0.5,
            "gen_coal_mwh": coal_mw * 0.5,
            "gen_gas_mwh": gas_mw * 0.5,
            "gen_oil_mwh": oil_mw * 0.5,
        }
    )
    out["co2_tonnes"] = (
        out["gen_coal_mwh"] * FACTORS["coal"]
        + out["gen_gas_mwh"] * FACTORS["gas"]
        + out["gen_oil_mwh"] * FACTORS["oil"]
        + out["gen_other_mwh"] * FACTORS["other"]
        + rng.normal(0.0, 6.0, size=len(out))
    )
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    base = pd.read_csv(TOY, parse_dates=["timestamp"])
    # Recover approximate MW demand from MWh half-hours.
    demand_mw = (base["demand_mwh"] / 0.5).to_numpy()

    without = dispatch(demand_mw, 0.0, rng)
    with_geo = dispatch(demand_mw, EXTRA_GEO_MW, np.random.default_rng(8))

    delta = with_geo - without
    summary = {
        "disclaimer": "ILLUSTRATIVE TOY COUNTERFACTUAL — NOT JAMALI",
        "extra_geothermal_mw": EXTRA_GEO_MW,
        "extra_geothermal_mwh_total": float(delta["gen_geo_mwh"].sum()),
        "coal_displaced_mwh": float(-delta["gen_coal_mwh"].sum()),
        "gas_displaced_mwh": float(-delta["gen_gas_mwh"].sum()),
        "oil_displaced_mwh": float(-delta["gen_oil_mwh"].sum()),
        "co2_avoided_tonnes": float(-delta["co2_tonnes"].sum()),
        "implied_avoided_tco2_per_extra_geo_mwh": float(
            (-delta["co2_tonnes"].sum()) / delta["gen_geo_mwh"].sum()
        ),
    }

    # Average by local hour: which fuel was displaced?
    hours = base["timestamp"].dt.hour
    hour_disp = pd.DataFrame(
        {
            "hour": hours,
            "coal": -delta["gen_coal_mwh"],
            "gas": -delta["gen_gas_mwh"],
            "oil": -delta["gen_oil_mwh"],
            "co2": -delta["co2_tonnes"],
        }
    ).groupby("hour", as_index=False).mean()

    pd.DataFrame([summary]).to_csv(OUT / "geothermal_counterfactual_summary.csv", index=False)
    hour_disp.to_csv(OUT / "geothermal_displacement_by_hour.csv", index=False)
    (OUT / "geothermal_counterfactual_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].stackplot(
        hour_disp["hour"],
        hour_disp["coal"],
        hour_disp["gas"],
        hour_disp["oil"],
        labels=["Coal", "Gas", "Oil"],
        colors=["#4a4a4a", "#2f5d8a", "#a35d4a"],
    )
    axes[0].set_title("Mean displaced generation by hour")
    axes[0].set_xlabel("Hour")
    axes[0].set_ylabel("MWh displaced / interval")
    axes[0].legend(loc="upper right", fontsize=8)

    axes[1].plot(hour_disp["hour"], hour_disp["co2"], color="#6b8f71", lw=2)
    axes[1].set_title("Mean avoided CO₂ by hour")
    axes[1].set_xlabel("Hour")
    axes[1].set_ylabel("tCO₂ avoided / interval")

    fig.suptitle(f"Toy with/without +{EXTRA_GEO_MW:.0f} MW geothermal")
    fig.text(
        0.02,
        0.01,
        "ILLUSTRATIVE SYNTHETIC EXAMPLE — NOT A JAMALI GEOTHERMAL IMPACT ESTIMATE",
        fontsize=8,
        color="#a35d4a",
    )
    fig.tight_layout()
    fig.savefig(OUT / "toy_geothermal_displacement.png", dpi=160)
    plt.close(fig)

    (OUT / "NOT_JAMALI_MEF.txt").write_text(
        "TOY GEOTHERMAL COUNTERFACTUAL ONLY\nNot a Jamali project assessment.\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
