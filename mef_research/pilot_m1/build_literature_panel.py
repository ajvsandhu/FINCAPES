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
        "region": "MRO (US Midwest)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 834,
        "dominant_marginal_fuel": "Coal (~79%)",
        "aef_vs_mef_note": "2007 AEF within ~2% of MEF",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "RFC (US Mid-Atlantic)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 731,
        "dominant_marginal_fuel": "Coal (~70%)",
        "aef_vs_mef_note": "2007 AEF ~11% below MEF",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "SPP (US Southwest)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 596,
        "dominant_marginal_fuel": "Gas (~65%)",
        "aef_vs_mef_note": "2007 AEF 35% above MEF for CO2",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "TRE (Texas)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 527,
        "dominant_marginal_fuel": "Gas (~84%)",
        "aef_vs_mef_note": "2007 AEF 12% above MEF for CO2",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "WECC (US West)",
        "method": "Historical regression",
        "period": "2006–2011",
        "mef_kg_per_mwh": 486,
        "dominant_marginal_fuel": "Gas (~86%)",
        "aef_vs_mef_note": "2007 AEF ≈ MEF for CO2; large AEF–MEF gaps for SO2/NOx",
        "source": "Siler-Evans (2012), Tables 2.1–2.2",
    },
    {
        "region": "NPCC (US Northeast)",
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
    ax.text(
        0.02,
        0.02,
        "Published evidence only — not Jamali estimates. Midwest MEF ≈ 70% higher than West.",
        transform=ax.transAxes,
        fontsize=8,
        color="#444",
    )
    fig.tight_layout()
    fig_path = OUT / "literature_region_mefs.png"
    fig.savefig(fig_path, dpi=160)
    plt.close(fig)
    print(f"Wrote {csv_path}")
    print(f"Wrote {fig_path}")


if __name__ == "__main__":
    main()
