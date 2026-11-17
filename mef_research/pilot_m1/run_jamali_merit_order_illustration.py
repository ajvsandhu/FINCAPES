#!/usr/bin/env python3
"""Stylised Jamali night/peak merit-order illustration (option 4a).

ILLUSTRATIVE SCENARIO ONLY — NOT A JAMALI MEF.
Uses audited NP annual heat rates plus simplified fuel-cost assumptions to
sketch which plant class is likely on the margin at night vs peak.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "outputs_jamali_illustration"
HEAT = ROOT / "output" / "jamali_inventory" / "annual_operating_characteristics.csv"

# Illustrative fuel prices and carbon contents for ranking only.
# These are scenario assumptions, not verified PLN contract prices.
ASSUMPTIONS = {
    "coal_usd_per_mmbtu": 2.5,   # DMO-like cheap coal cartoon
    "gas_usd_per_mmbtu": 8.0,    # higher delivered gas cartoon
    "kcal_per_mmbtu": 252.0,     # approx
    "coal_tco2_per_mwh_proxy": 1.00,
    "gas_tco2_per_mwh_proxy": 0.42,
}


def build_fleet() -> pd.DataFrame:
    heat = pd.read_csv(HEAT)
    rows = []
    for _, r in heat.iterrows():
        name = r["name"]
        nphr = float(r["nphr_kcal_per_net_kwh"])
        # Muara Karang is the gas/CCGT-like unit in this NP sample; others are coal UPs.
        fuel = "gas" if "Muara Karang" in name else "coal"
        mmbtu_per_mwh = nphr / ASSUMPTIONS["kcal_per_mmbtu"]
        fuel_price = ASSUMPTIONS["coal_usd_per_mmbtu"] if fuel == "coal" else ASSUMPTIONS["gas_usd_per_mmbtu"]
        var_cost = mmbtu_per_mwh * fuel_price
        intensity = (
            ASSUMPTIONS["coal_tco2_per_mwh_proxy"] if fuel == "coal" else ASSUMPTIONS["gas_tco2_per_mwh_proxy"]
        )
        # Cartoon capacities for stacking (not official dependable MW).
        cap_mw = 500.0 if fuel == "coal" else 800.0
        rows.append(
            {
                "name": name,
                "fuel": fuel,
                "nphr_kcal_per_net_kwh": nphr,
                "illustrative_var_cost_usd_per_mwh": var_cost,
                "illustrative_tco2_per_mwh": intensity,
                "cartoon_capacity_mw": cap_mw,
            }
        )
    # Add a must-run geothermal block for the night/peak story.
    rows.append(
        {
            "name": "Geothermal (must-run cartoon)",
            "fuel": "geo",
            "nphr_kcal_per_net_kwh": 0.0,
            "illustrative_var_cost_usd_per_mwh": 0.0,
            "illustrative_tco2_per_mwh": 0.0,
            "cartoon_capacity_mw": 700.0,
        }
    )
    fleet = pd.DataFrame(rows).sort_values("illustrative_var_cost_usd_per_mwh").reset_index(drop=True)
    fleet["stack_mw_end"] = fleet["cartoon_capacity_mw"].cumsum()
    fleet["stack_mw_start"] = fleet["stack_mw_end"] - fleet["cartoon_capacity_mw"]
    return fleet


def marginal_at(fleet: pd.DataFrame, demand_mw: float) -> dict:
    for _, r in fleet.iterrows():
        if r["stack_mw_start"] < demand_mw <= r["stack_mw_end"]:
            return {
                "demand_mw": demand_mw,
                "marginal_plant": r["name"],
                "marginal_fuel": r["fuel"],
                "illustrative_mef_tco2_per_mwh": r["illustrative_tco2_per_mwh"],
                "illustrative_var_cost_usd_per_mwh": r["illustrative_var_cost_usd_per_mwh"],
            }
    last = fleet.iloc[-1]
    return {
        "demand_mw": demand_mw,
        "marginal_plant": last["name"],
        "marginal_fuel": last["fuel"],
        "illustrative_mef_tco2_per_mwh": last["illustrative_tco2_per_mwh"],
        "illustrative_var_cost_usd_per_mwh": last["illustrative_var_cost_usd_per_mwh"],
        "note": "demand above cartoon stack; last unit treated as marginal",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fleet = build_fleet()
    night_demand = 2200.0
    peak_demand = 4200.0
    night = marginal_at(fleet, night_demand)
    peak = marginal_at(fleet, peak_demand)

    fleet.to_csv(OUT / "illustrative_merit_order_stack.csv", index=False)
    pd.DataFrame([night, peak]).assign(snapshot=["night", "peak"]).to_csv(
        OUT / "night_peak_marginal_units.csv", index=False
    )
    meta = {
        "disclaimer": "ILLUSTRATIVE JAMALI MERIT-ORDER CARTOON — NOT A MEF",
        "assumptions": ASSUMPTIONS,
        "night": night,
        "peak": peak,
        "source_heat_rates": str(HEAT),
    }
    (OUT / "illustration_summary.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = {"geo": "#6b8f71", "coal": "#4a4a4a", "gas": "#2f5d8a"}
    for _, r in fleet.iterrows():
        ax.barh(
            0,
            r["cartoon_capacity_mw"],
            left=r["stack_mw_start"],
            color=colors[r["fuel"]],
            edgecolor="white",
            height=0.45,
        )
        if r["cartoon_capacity_mw"] >= 400:
            ax.text(
                r["stack_mw_start"] + r["cartoon_capacity_mw"] / 2,
                0,
                r["name"].replace("UP ", ""),
                ha="center",
                va="center",
                fontsize=7,
                color="white",
            )
    ax.axvline(night_demand, color="#c4a35a", ls="--", label=f"Night demand {night_demand:.0f} MW")
    ax.axvline(peak_demand, color="#a35d4a", ls="--", label=f"Peak demand {peak_demand:.0f} MW")
    ax.set_yticks([])
    ax.set_xlabel("Cartoon cumulative capacity (MW)")
    ax.set_title("Stylised Jamali merit-order illustration (night vs peak)")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(
        0.02,
        0.02,
        "ILLUSTRATIVE ONLY — uses NP heat rates + assumed fuel prices; not a Jamali MEF or calibrated dispatch model.",
        transform=ax.transAxes,
        fontsize=8,
        color="#a35d4a",
    )
    fig.tight_layout()
    fig.savefig(OUT / "jamali_merit_order_night_peak.png", dpi=160)
    plt.close(fig)

    (OUT / "NOT_JAMALI_MEF.txt").write_text(
        "STYLISED ILLUSTRATION ONLY\nNot a numerical Jamali MEF.\n",
        encoding="utf-8",
    )
    print("Night:", night)
    print("Peak:", peak)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
