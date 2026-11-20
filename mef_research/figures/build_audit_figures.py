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


def _save(fig: plt.Figure, name: str, *, rect: tuple[float, float, float, float] | None = None) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    if rect is None:
        fig.tight_layout()
    else:
        fig.tight_layout(rect=rect)
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
    fig.text(
        0.5,
        0.02,
        "Not a complete unit census. Isolated systems excluded from interconnected Jamali unless connected.",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#444",
    )
    return _save(fig, "01_register_counts.png", rect=(0, 0.08, 1, 1))


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
    """Status table — not a progress/completeness bar chart."""
    rows = [
        ("M1 Historical regression", "First pilot — blocked on interval data", "#c4a35a"),
        ("M2 Reduced-order dispatch", "Some fleet inputs; same data gate", "#c4a35a"),
        ("M5 AVERT-style historical", "Not ready this stage", "#a35d4a"),
        ("M3 Network-resolved", "Not ready this stage", "#a35d4a"),
        ("M4 ML forecasting", "Not ready this stage", "#a35d4a"),
        ("Long-run capacity expansion", "Separate programme — not this stage", "#a35d4a"),
        ("CM accounting benchmark", "Published factors available — not an observed MEF", "#6b8f71"),
    ]
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    ax.set_axis_off()
    ax.set_title("What’s ready vs what’s not (status, not % complete)", pad=14, fontsize=13)
    table = ax.table(
        cellText=[[route, status] for route, status, _ in rows],
        colLabels=["Route", "Status for Jamali right now"],
        cellLoc="left",
        colLoc="left",
        loc="center",
        bbox=[0.02, 0.12, 0.96, 0.78],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width([0, 1])
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#d0d0d0")
        cell.set_linewidth(0.6)
        cell.PAD = 0.04
        if row == 0:
            cell.set_facecolor("#2f5d8a")
            cell.set_text_props(color="white", weight="bold")
            cell.set_height(0.09)
        else:
            route, status, color = rows[row - 1]
            cell.set_height(0.095)
            if col == 0:
                cell.set_facecolor("#f7f7f7" if row % 2 else "white")
                cell.set_text_props(weight="bold", color="#1f3a56")
            else:
                cell.set_facecolor(color)
                cell.set_text_props(color="white" if color != "#c4a35a" else "#1f1f1f")
    fig.text(
        0.5,
        0.04,
        "Gold = pathway defined but blocked without time-aligned UIP2B interval data.  "
        "Green = accounting benchmark only — not a Jamali MEF.",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#444",
    )
    return _save(fig, "08_method_readiness.png", rect=(0, 0.08, 1, 1))


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
