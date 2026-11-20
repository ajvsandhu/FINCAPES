#!/usr/bin/env python3
"""Write the cross-region published-findings panel used in the report draft."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUT = Path(__file__).resolve().parent / "public_demo"

# Sourced from Siler-Evans (2012) dissertation Table 2.1 (2006–2011) and Table 2.2 (2007).
# CO2 MEF units: kg/MWh. This is published evidence, not a new estimation.
ROWS = [
    {
        "region": "US Midwest (MRO)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 834,
        "dominant_marginal_fuel": "Coal (~79%)",
        "aef_vs_mef_note": "2007 AEF within ~2% of MEF",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "US Mid-Atlantic (RFC)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 731,
        "dominant_marginal_fuel": "Coal (~70%)",
        "aef_vs_mef_note": "2007 AEF ~11% below MEF",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "US Southwest (SPP)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 596,
        "dominant_marginal_fuel": "Gas (~65%)",
        "aef_vs_mef_note": "2007 AEF 35% above MEF for CO2",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "Texas (TRE)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 527,
        "dominant_marginal_fuel": "Gas (~84%)",
        "aef_vs_mef_note": "2007 AEF 12% above MEF for CO2",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "US West (WECC)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 486,
        "dominant_marginal_fuel": "Gas (~86%)",
        "aef_vs_mef_note": "2007 AEF ≈ MEF for CO2; large AEF–MEF gaps for SO2/NOx",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "US Northeast (NPCC)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 489,
        "dominant_marginal_fuel": "Gas (~81%)",
        "aef_vs_mef_note": "2007 AEF 25% below MEF for CO2",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(ROWS)
    csv_path = OUT / "literature_region_panel.csv"
    df.to_csv(csv_path, index=False)

    plot_df = df.sort_values("mef_kg_per_mwh")
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.barh(plot_df["region"], plot_df["mef_kg_per_mwh"], color="#2f5d8a")
    ax.set_xlabel("Published short-run CO₂ MEF (kg/MWh)")
    ax.set_title("Published US regional MEFs (Siler-Evans, 2006–2011)")
    fig.text(
        0.5,
        0.02,
        "Published evidence only — not Jamali estimates. Midwest MEF ≈ 70% higher than West.",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#444",
    )
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig_path = OUT / "literature_region_mefs.png"
    fig.savefig(fig_path, dpi=160)
    plt.close(fig)
    print(f"Wrote {csv_path}")
    print(f"Wrote {fig_path}")


if __name__ == "__main__":
    main()
