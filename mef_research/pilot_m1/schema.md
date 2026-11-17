# M1 pilot input schema

Expected columns for the historical-regression short-run MEF pilot.
Real PLN UIP2B files should be mapped into this schema before running `run_pilot.py`.

## Required interval table (`interval_operations.csv`)

| Column | Type | Definition |
|---|---|---|
| `timestamp` | datetime | Interval start, timezone-aware or documented as WIB |
| `demand_mwh` | float | System demand for the interval (MWh). Prefer net of auxiliaries if that matches generation. |
| `gen_coal_mwh` | float | Coal generation in the interval (MWh) |
| `gen_gas_mwh` | float | Gas generation in the interval (MWh) |
| `gen_oil_mwh` | float | Oil / diesel generation (MWh); use 0 if unused |
| `gen_geo_mwh` | float | Geothermal generation (MWh) |
| `gen_other_mwh` | float | Other generation (hydro, solar, wind, imports allocated to system, etc.) |
| `interchange_mwh` | float | Net imports into the study boundary (+ = import). Optional but recommended. |

Interval length must be constant (30 minutes preferred; hourly acceptable). Missing intervals should be flagged rather than silently interpolated.

## Optional emissions table

If measured CO₂ is available, add:

| Column | Type | Definition |
|---|---|---|
| `co2_tonnes` | float | Measured or official interval CO₂ for the same boundary |

Otherwise the pilot constructs emissions from generation × emission factors.

## Plant / fuel factors (`emission_factors.csv`)

| Column | Type | Definition |
|---|---|---|
| `fuel` | string | One of: coal, gas, oil, geo, other |
| `tco2_per_mwh` | float | Average CO₂ intensity used when measured emissions are absent |

These are placeholders for annual heat-rate × fuel-carbon constructions. Replace with unit-specific factors when UIP2B / APPLE-GATRIK data arrive.

## Estimand implemented by `run_pilot.py`

\[
\Delta CO2_t = \beta \cdot \Delta Demand_t + \varepsilon_t
\]

- Chronological split (default: first 75% train, last 25% test)
- Overall \(\beta\) plus hour-of-day profile on the training set
- Toy outputs are illustrative only and must not be reported as Jamali MEFs
