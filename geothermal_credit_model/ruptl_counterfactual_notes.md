# RUPTL-consistent geothermal removal scenarios

This is an annual energy-balance sensitivity analysis, not a dispatch or
capacity-expansion model. RUPTL's RE Base and ARED scenarios both include
geothermal; neither is an official case without the planned projects.

## Inputs and schedule reconciliation

- Planned electricity uses the existing model's GENESIS capacity schedule,
  one-year commissioning lag, and 80% capacity factor.
- GENESIS planned capacity totals 2,503 MW for Jamali and 2,007 MW for the main
  Sumatera grid. The separate Sabang grid has 10 MW. RUPTL's geothermal
  additions total 2,503 MW in Jamali and 2,017 MW in its wider Sumatera region.
- Annual schedules differ modestly: 30 MW shifts between 2026 and 2027 in
  Jamali; 60 MW shifts between 2031 and 2033 in Sumatera, plus the two 5 MW
  Sabang additions in 2028 and 2033.
- RUPTL's fuel-specific generation and emissions supply annual coal and gas
  average intensities. These are not marginal plant emission rates.

## Counterfactual construction

For each grid, RUPTL scenario, and year:

1. Start with RUPTL's projected geothermal, coal, and gas generation.
2. Take the modelled GENESIS planned-project electricity at an 80% capacity
   factor. Bound the amount removed to the positive growth in RUPTL geothermal
   generation above its 2025 level. This retains at least the 2025 geothermal
   total in the illustrative without-project case.
3. Add exactly the removed electricity to coal, gas, or a coal-gas mix using
   the projected annual coal/gas generation proportions. Electricity supply is
   therefore unchanged in each case.
4. Multiply added coal and gas generation by the corresponding RUPTL annual
   fuel emissions divided by fuel generation. The difference is *gross* avoided
   emissions under that replacement rule.

The 2025 geothermal level is an accounting reference, not a measurement of
pre-project output. Some 2025 planned projects may already contribute to it.
The bound does not identify which actual projects operate. Jamali's projected
geothermal generation also includes electricity imported from Sumatera in the
2030s; RUPTL's Sumatera region includes island systems outside the main grid.

## Results

| Region | RUPTL scenario | Gas replacement | Proportional coal-gas | Coal replacement |
| --- | --- | ---: | ---: | ---: |
| Jamali | RE Base | 23.38 | 45.56 | 54.30 |
| Jamali | ARED | 24.68 | 46.99 | 54.27 |
| Sumatera | RE Base | 19.72 | 32.14 | 35.30 |
| Sumatera | ARED | 19.72 | 32.03 | 35.24 |

Figures are cumulative MtCO2 for 2025-2034. The bound leaves Jamali's modelled
49.59 TWh unchanged. It reduces Sumatera's removable planned electricity from
47.47 TWh to 32.70 TWh, binding in 2026, 2027, and 2032-2034. This is why
the earlier unbounded substitution figures cannot be used as a central
RUPTL-consistent counterfactual.

RUPTL also plans 2,000 MW of coal and 5,453 MW of gas additions in Jamali, and
3,300 MW of *mine-mouth coal* and 701 MW of gas additions in Sumatera. Their
presence makes both operating and build effects possible. The plan does not
say which plant would generate more or which build would be added without
geothermal, so none of the three replacement cases can be called the most
accurate. A dispatch and capacity-expansion run with and without the same
geothermal projects is needed for that claim.

## Reproduce

Run `python3 geothermal_credit_model/ruptl_counterfactual.py` from the
repository root. The script writes `output/ruptl_counterfactual_by_year.csv`
and `output/ruptl_counterfactual_summary.csv` beside itself.
