# Audit figures (real Jamali evidence)

Figures in `audit/` are built from already-reviewed files under `mef_research/output/`.

They summarise register coverage, annual samples and method readiness. **They do not estimate a Jamali MEF.**

## Rebuild

```bash
python3 -B mef_research/figures/build_audit_figures.py
```

Run from the repository root (`FINCAPES/`).

## Outputs

| File | Content |
|---|---|
| `01_register_counts.png` | Existing / planning / isolated counts |
| `02_planned_technology_counts.png` | Top RUPTL planning technologies |
| `03_annual_heat_rates.png` | Selected NP 2024 heat rates |
| `04_annual_availability.png` | Selected NP 2024 availability |
| `05_jamali_annual_sales.png` | Annual sales by customer group |
| `06_wayang_windu_monthly.png` | Wayang Windu monthly sample |
| `07_ip_roster_top_capacity.png` | Largest IP plant/group totals |
| `08_method_readiness.png` | Qualitative readiness snapshot |
