#!/usr/bin/env python3
"""Build report figures from audited Jamali evidence only.

These charts summarise inventory and annual samples already in
mef_research/output/. They do not estimate a Jamali MEF.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "audit"
INV = ROOT / "output" / "jamali_inventory"
IP = ROOT / "output" / "ip_roster_audit"

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "font.size": 10,
    }
)


def _save(fig: plt.Figure, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def fig_register_counts() -> Path:
    existing = pd.read_csv(INV / "existing_resources.csv")
    planned = pd.read_csv(INV / "planned_resources.csv")
    isolated = pd.read_csv(INV / "isolated_systems.csv")
    counts = {
        "Existing named\nentries": len(existing),
        "Planning rows": len(planned),
        "Isolated East\nJava systems": len(isolated),
    }
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    bars = ax.bar(list(counts.keys()), list(counts.values()), color=["#2f5d8a", "#6b8f71", "#a35d4a"])
    ax.set_ylabel("Count")
    ax.set_title("Partial Jamali register coverage (audited evidence counts)")
    for bar, value in zip(bars, counts.values()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, str(value), ha="center")
    ax.text(
        0.02,
        0.98,
        "Not a complete unit census. Isolated systems excluded from interconnected Jamali unless connected.",
        transform=ax.transAxes,
        va="top",
        fontsize=8,
        color="#444",
    )
    return _save(fig, "01_register_counts.png")


def fig_planned_technology() -> Path:
    planned = pd.read_csv(INV / "planned_resources.csv")
    tech = planned["technology"].fillna("Unspecified").value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(tech.index, tech.values, color="#2f5d8a")
    ax.set_xlabel("Number of planning rows")
    ax.set_title("Top technologies in RUPTL planning rows (not all are new capacity)")
    ax.text(
        0.02,
        0.02,
        "Includes quotas, storage, replacements and efficiency rows; do not sum as installed MW.",
        transform=ax.transAxes,
        fontsize=8,
        color="#444",
    )
    return _save(fig, "02_planned_technology_counts.png")


def fig_heat_rates() -> Path:
    ann = pd.read_csv(INV / "annual_operating_characteristics.csv")
    ann = ann.sort_values("nphr_kcal_per_net_kwh")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(ann["name"], ann["nphr_kcal_per_net_kwh"], color="#6b8f71")
    ax.set_xlabel("Net plant heat rate (kcal / net kWh)")
    ax.set_title("Selected PLN Nusantara Power 2024 annual heat rates")
    ax.text(
        0.02,
        0.02,
        "Annual averages only — not incremental heat-rate curves for MEF construction.",
        transform=ax.transAxes,
        fontsize=8,
        color="#444",
    )
    return _save(fig, "03_annual_heat_rates.png")


def fig_availability() -> Path:
    ann = pd.read_csv(INV / "annual_operating_characteristics.csv")
    ann = ann.sort_values("eaf_percent")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(ann["name"], ann["eaf_percent"], color="#2f5d8a")
    ax.set_xlabel("Equivalent availability factor (%)")
    ax.set_title("Selected PLN Nusantara Power 2024 availability")
    ax.set_xlim(0, 100)
    return _save(fig, "04_annual_availability.png")


def fig_sales() -> Path:
    sales = pd.read_csv(INV / "sample_historical_sales.csv")
    groups = ["Household", "Industry", "Business", "Public"]
    pivot = sales[sales["customer_group"].isin(groups)].pivot(
        index="year", columns="customer_group", values="sales_gwh"
    )[groups]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    pivot.plot(kind="area", stacked=True, ax=ax, alpha=0.85)
    ax.set_ylabel("Sales (GWh)")
    ax.set_xlabel("Year")
    ax.set_title("Jamali annual electricity sales by customer group")
    ax.text(
        0.02,
        0.02,
        "Annual sales are not half-hourly system demand and cannot support an MEF pilot alone.",
        transform=ax.transAxes,
        fontsize=8,
        color="#444",
    )
    ax.legend(title="", loc="upper left")
    return _save(fig, "05_jamali_annual_sales.png")


def fig_wayang_windu() -> Path:
    ww = pd.read_csv(INV / "sample_wayang_windu_monthly.csv")
    ww["month"] = pd.to_datetime(ww["month"])
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(ww["month"], ww["unit_1_reported_mwh"] / 1000, label="Unit 1")
    ax.plot(ww["month"], ww["unit_2_reported_mwh"] / 1000, label="Unit 2")
    ax.set_ylabel("Reported output (GWh)")
    ax.set_title("Wayang Windu monthly output sample (two units)")
    ax.legend()
    ax.text(
        0.02,
        0.02,
        "One geothermal plant sample; does not reveal the grid's marginal response.",
        transform=ax.transAxes,
        fontsize=8,
        color="#444",
    )
    return _save(fig, "06_wayang_windu_monthly.png")


def fig_ip_capacity_top() -> Path:
    roster = pd.read_csv(IP / "plant_roster.csv")
    top = roster.nlargest(15, "installed_mw").sort_values("installed_mw")
    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.barh(top["plant_name"], top["installed_mw"], color="#2f5d8a")
    ax.set_xlabel("Installed MW (source plant totals)")
    ax.set_title("Largest PLN Indonesia Power plant/group totals in 2024 roster")
    ax.text(
        0.02,
        0.02,
        "Do not add parent totals to constituent rows. National roster ≠ Jamali unit census.",
        transform=ax.transAxes,
        fontsize=8,
        color="#444",
    )
    return _save(fig, "07_ip_roster_top_capacity.png")


def fig_readiness_gap() -> Path:
    routes = [
        "Historical\nregression",
        "AVERT-style\nhistorical",
        "Reduced-order\ndispatch",
        "Network-\nresolved",
        "ML\nforecasting",
        "Long-run\ncapacity",
        "CM accounting\nbenchmark",
    ]
    # 0 = missing, 1 = partial, 2 = available for that route's purpose
    status = [1, 0, 1, 0, 0, 0, 2]
    labels = {
        0: "Missing for pilot",
        1: "Partial / blocked by interval data",
        2: "Available (not an observed MEF)",
    }
    colors = {0: "#a35d4a", 1: "#c4a35a", 2: "#6b8f71"}
    fig, ax = plt.subplots(figsize=(9.5, 4.5))
    ax.bar(routes, status, color=[colors[s] for s in status])
    ax.set_ylim(0, 2.6)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["Missing", "Partial", "Available"])
    ax.set_title("Method readiness snapshot (qualitative)")
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=colors[k], label=labels[k]) for k in (0, 1, 2)
    ]
    ax.legend(handles=handles, loc="upper right", fontsize=8)
    ax.text(
        0.02,
        0.98,
        "All short-run numerical MEF routes remain blocked without time-aligned UIP2B data.",
        transform=ax.transAxes,
        va="top",
        fontsize=8,
        color="#444",
    )
    return _save(fig, "08_method_readiness.png")


def main() -> None:
    paths = [
        fig_register_counts(),
        fig_planned_technology(),
        fig_heat_rates(),
        fig_availability(),
        fig_sales(),
        fig_wayang_windu(),
        fig_ip_capacity_top(),
        fig_readiness_gap(),
    ]
    print(f"Wrote {len(paths)} figures to {OUT}")
    for path in paths:
        print(f"  {path.name}")


if __name__ == "__main__":
    main()
