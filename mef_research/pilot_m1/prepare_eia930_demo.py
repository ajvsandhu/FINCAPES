#!/usr/bin/env python3
"""Map EIA-930 balance rows for selected BAs into the M1 pilot schema.

PUBLIC NON-JAMALI DEMONSTRATION ONLY.
CO2 is constructed from fuel-specific generation using constant intensities.
This is a method dry-run, not an official EIA MEF product and not a Jamali estimate.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "public_demo" / "raw" / "EIA930_BALANCE_2024_Jan_Jun.csv"
OUT = HERE / "public_demo"
BAS = ("CISO", "ERCO", "MISO", "PJM")  # CAISO area, ERCOT, plus coal-heavier systems

# Approximate average intensities (tCO2 / MWh) for construction only.
FACTORS = {
    "coal": 1.00,
    "gas": 0.40,
    "oil": 0.70,
    "geo": 0.00,
    "other": 0.05,
}


def _num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def map_ba(df: pd.DataFrame, ba: str) -> pd.DataFrame:
    part = df[df["Balancing Authority"] == ba].copy()
    if part.empty:
        raise ValueError(f"No rows for balancing authority {ba}")

    # Use local BA clock time so hour-of-day profiles are interpretable.
    part["timestamp"] = pd.to_datetime(
        part["Local Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p"
    )
    part = part.sort_values("timestamp")

    demand_mw = _num(part["Demand (MW) (Adjusted)"].where(
        part["Demand (MW) (Adjusted)"].notna(), part["Demand (MW)"]
    ))
    coal = _num(part["Net Generation (MW) from Coal (Adjusted)"].where(
        part["Net Generation (MW) from Coal (Adjusted)"].notna(),
        part["Net Generation (MW) from Coal"],
    ))
    gas = _num(part["Net Generation (MW) from Natural Gas (Adjusted)"].where(
        part["Net Generation (MW) from Natural Gas (Adjusted)"].notna(),
        part["Net Generation (MW) from Natural Gas"],
    ))
    oil = _num(part["Net Generation (MW) from All Petroleum Products (Adjusted)"].where(
        part["Net Generation (MW) from All Petroleum Products (Adjusted)"].notna(),
        part["Net Generation (MW) from All Petroleum Products"],
    ))
    other = (
        _num(part["Net Generation (MW) from Other Fuel Sources (Adjusted)"].where(
            part["Net Generation (MW) from Other Fuel Sources (Adjusted)"].notna(),
            part["Net Generation (MW) from Other Fuel Sources"],
        ))
        + _num(part["Net Generation (MW) from Unknown Fuel Sources (Adjusted)"].where(
            part["Net Generation (MW) from Unknown Fuel Sources (Adjusted)"].notna(),
            part["Net Generation (MW) from Unknown Fuel Sources"],
        ))
    )
    interchange = _num(part["Total Interchange (MW) (Adjusted)"].where(
        part["Total Interchange (MW) (Adjusted)"].notna(), part["Total Interchange (MW)"]
    ))

    # Hourly integrated MW ≈ MWh for the hour.
    out = pd.DataFrame(
        {
            "timestamp": part["timestamp"],
            "demand_mwh": demand_mw,
            "gen_coal_mwh": coal,
            "gen_gas_mwh": gas,
            "gen_oil_mwh": oil,
            "gen_geo_mwh": 0.0,
            "gen_other_mwh": other,
            "interchange_mwh": interchange,
        }
    )
    out["co2_tonnes"] = (
        out["gen_coal_mwh"] * FACTORS["coal"]
        + out["gen_gas_mwh"] * FACTORS["gas"]
        + out["gen_oil_mwh"] * FACTORS["oil"]
        + out["gen_other_mwh"] * FACTORS["other"]
    )
    out = out.dropna(subset=["timestamp", "demand_mwh"]).drop_duplicates("timestamp")
    out = out[out["demand_mwh"] > 0].reset_index(drop=True)
    return out


def main() -> None:
    if not RAW.exists():
        raise SystemExit(f"Missing {RAW}. Download EIA-930 balance file first.")

    OUT.mkdir(parents=True, exist_ok=True)
    usecols = [
        "Balancing Authority",
        "Local Time at End of Hour",
        "Demand (MW)",
        "Demand (MW) (Adjusted)",
        "Total Interchange (MW)",
        "Total Interchange (MW) (Adjusted)",
        "Net Generation (MW) from Coal",
        "Net Generation (MW) from Coal (Adjusted)",
        "Net Generation (MW) from Natural Gas",
        "Net Generation (MW) from Natural Gas (Adjusted)",
        "Net Generation (MW) from All Petroleum Products",
        "Net Generation (MW) from All Petroleum Products (Adjusted)",
        "Net Generation (MW) from Other Fuel Sources",
        "Net Generation (MW) from Other Fuel Sources (Adjusted)",
        "Net Generation (MW) from Unknown Fuel Sources",
        "Net Generation (MW) from Unknown Fuel Sources (Adjusted)",
    ]
    df = pd.read_csv(RAW, usecols=usecols)
    factors = pd.DataFrame({"fuel": list(FACTORS), "tco2_per_mwh": list(FACTORS.values())})
    factors.to_csv(OUT / "demo_emission_factors.csv", index=False)

    for ba in BAS:
        mapped = map_ba(df, ba)
        path = OUT / f"{ba.lower()}_2024H1_interval_operations.csv"
        mapped.to_csv(path, index=False)
        print(f"{ba}: wrote {path} ({len(mapped)} hours)")

    (OUT / "PUBLIC_DEMO_README.txt").write_text(
        "PUBLIC NON-JAMALI DEMONSTRATION\n"
        "Source: U.S. EIA Form EIA-930 six-month balance file, Jan–Jun 2024.\n"
        "BAs: CISO (CAISO area), ERCO (ERCOT), MISO and PJM.\n"
        "CO2 constructed from fuel generation × constant intensities; not EIA published MEFs.\n"
        "Do not report these outputs as Jamali MEFs or as official US policy factors.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
