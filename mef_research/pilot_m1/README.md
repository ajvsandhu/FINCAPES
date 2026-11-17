# M1 historical-regression pilot scaffold

Ready-to-run short-run MEF pilot recommended in the readiness assessment.

## Important

- Default inputs under `toy_data/` are **synthetic**.
- Outputs under `outputs_toy/` are **illustrative only**.
- **Do not report toy β values as a Jamali MEF.**
- When UIP2B data arrive, map them to [schema.md](schema.md) and re-run with `--input`.

## Quick start

```bash
# from repository root
python3 -B mef_research/pilot_m1/generate_toy_data.py
python3 -B mef_research/pilot_m1/run_pilot.py
```

## What the pilot does

1. Loads half-hourly demand, generation by fuel and CO₂ (measured or constructed).
2. Computes interval changes \(\Delta Demand\) and \(\Delta CO_2\).
3. Fits \(\Delta CO_2 = \alpha + \beta \Delta Demand\) on a chronological training window.
4. Checks the training \(\beta\) on a later test window.
5. Also estimates an hour-of-day MEF profile on the training window.

## Public non-Jamali demonstration (EIA-930)

Uses U.S. EIA Form EIA-930 hourly balance data for CISO, ERCO, MISO and PJM (Jan–Jun 2024).
CO₂ is constructed from fuel generation × constant intensities.

```bash
# assumes EIA930_BALANCE_2024_Jan_Jun.csv already in public_demo/raw/
python3 -B mef_research/pilot_m1/prepare_eia930_demo.py
python3 -B mef_research/pilot_m1/build_literature_panel.py
python3 -B mef_research/pilot_m1/run_public_comparisons.py
```

`run_public_comparisons.py` produces:
- AEF vs demand MEF
- demand MEF vs fossil-generation MEF
- multi-BA hour-of-day profiles

Do not report these β values as Jamali MEFs or as official U.S. policy factors.

## Further illustrations (12 / 5a / 4a)

```bash
python3 -B mef_research/pilot_m1/run_data_gap_simulation.py
python3 -B mef_research/pilot_m1/run_toy_geothermal_counterfactual.py
python3 -B mef_research/pilot_m1/run_jamali_merit_order_illustration.py
```

- **Data-gap:** hourly → daily → monthly → annual collapse on EIA demos  
- **Toy geothermal:** with/without +500 MW geothermal counterfactual  
- **Jamali cartoon:** night/peak merit-order illustration from NP heat rates  

All three are labelled non-Jamali-MEF (or illustrative only).

## Later: real UIP2B data

```bash
python3 -B mef_research/pilot_m1/run_pilot.py \
  --input path/to/mapped_uip2b.csv \
  --factors path/to/emission_factors.csv \
  --outdir mef_research/pilot_m1/outputs_jamali \
  --label "PROVISIONAL JAMALI PILOT — REVIEW BEFORE PUBLICATION"
```
