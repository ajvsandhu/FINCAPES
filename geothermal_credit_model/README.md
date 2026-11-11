# Planned geothermal: gross avoided-emissions model

This model compares the potential gross avoided grid emissions from GENESIS capacity planned for Jamali and Sumatera between 2025 and 2034. It is not a calculation of issued carbon credits or a forecast of how grid emission factors will change through 2034.

## Calculation

For every year and grid:

`estimated generation (MWh) = operating planned capacity (MW) x 8,760 x capacity factor`

`gross avoided emissions (tCO2) = estimated generation (MWh) x emission factor (tCO2/MWh)`

The model applies a one-year lag between the stated commissioning year and the first full generation year. Capacity planned for 2034 therefore does not contribute within the 2025-2034 analysis window. The capacity schedule is future-facing, but the emission factors are held fixed across all years. The cumulative values are consequently an illustrative sensitivity comparison, not a forecast of annual or cumulative crediting under changing grid conditions.

## Capacity-factor scenarios

The low, central, and high cases are 70%, 80%, and 90%. The central 80% case is supported by ESDM's *Indonesian Technology Catalogue 2024*, which reports Indonesian geothermal generation of about 16.6 TWh from 2,360 MW in 2022, equivalent to over 80%. The 90% upper case reflects PGE's published operating performance. The 70% lower case is deliberately conservative.

## Factor-method sensitivity

The model holds generation constant and changes only the emission factor. It compares ESDM's 2019 OM, BM, CM ex-post 50/50 and CM ex-ante 50/50 values with the separate JCM alternative. The OM, BM and ex-post CM values describe historical grid conditions based on 2019 data. The ex-ante CM is ESDM's forward-looking factor for its stated 2022-2030 period. The JCM factors refer to 2016-2018 and use a distinct methodology. Applying any one of these factors unchanged over the full 2025-2034 capacity schedule does not mean that it is valid for every future year. In this chart, these factors are included to isolate the effect of factor choice, not to assert a 2025-2034 forecast.

For a future pathway, an official ex-ante factor can only support years within its published coverage. A separate, clearly labelled approach is needed for 2031-2034. RUPTL emissions divided by generation can describe projected average system intensity under RE Base and ARED, but this is not an official OM, BM or CM and should not be presented as one.

## Main result

With the central 80% capacity-factor assumption, the model estimates cumulative gross avoided emissions of **30.7-46.6 MtCO2 for Jamali** and **21.7-53.2 MtCO2 for Sumatera** across the 2025-2034 analysis years. In both grids, BM gives the highest estimate and the JCM alternative gives the lowest. The spread is especially large in Sumatera: the BM estimate is more than twice the JCM estimate. These figures are in `output/planned_geothermal_credit_potential_summary.csv`; the corresponding comparison is shown in `output/factor_method_sensitivity.png`.

The high and low estimates result from applying different published factors to the same planned-capacity schedule and assumed generation. They show that the factor choice materially changes this model's gross estimate; they do not establish which method a particular project is eligible or required to use.

## Limitations

Results are **gross avoided-emissions potential**, not issued carbon credits. They do not subtract project operational emissions, determine whether a project is additional, establish carbon-market eligibility, or account for monitoring, verification, registry rules, curtailment, transmission losses, or actual commissioning dates. The model uses an assumed capacity factor and a one-year commissioning lag; actual output and timing may differ. It applies historical published factors unchanged across the analysis years to isolate factor-method sensitivity. It therefore does not forecast how grid factors change through 2034.

## Additional commissioning-delay sensitivity

Run `python3 -B geothermal_credit_model/commissioning_delay_sensitivity.py` from the repository root. This separate script reuses the original cohort and factor functions without changing the base model or its outputs. It compares 0, 1 and 2 additional commissioning-delay years, always retaining the existing one-year start lag, 80% capacity factor, 8,760 hours/year, the original grid membership and the 2025–2034 window. It does not combine this timing comparison with the RUPTL replacement-generation scenarios.

Outputs are confined to `output/commissioning_delay/`: retained cohorts, unique annual generation, annual and cumulative factor-specific emissions and reductions, two report-ready PNGs, validation checks, and hashed input snapshots. One additional year reduces cumulative generation and gross emissions by 35.4% in Jamali and 29.6% in Sumatera; two years reduce them by 56.0% and 51.8%. These are scenario assumptions, not predicted delays or lifetime project losses. See [commissioning_delay_notes.md](commissioning_delay_notes.md) for complete results, definitions and reproduction details.

## Sources

* GENESIS planned unit data and grid mapping in this repository.
* ESDM 2019 grid factors extracted from Kepmen ESDM 163.K/HK.02/MEM.S/2021.
* ESDM, *Indonesian Technology Catalogue 2024*, geothermal section.
* Pertamina Geothermal Energy published operating metrics.
* PLN, *RUPTL 2025–2034*, planned capacity additions, processed in `ruptl_eda/output/ruptl_capacity_additions.csv`.
