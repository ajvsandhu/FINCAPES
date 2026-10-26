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

## RUPTL scenario comparison

The separate `ruptl_projected_geothermal_generation_by_scenario.csv` and `ruptl_projected_geothermal_generation_by_scenario.png` compare RUPTL's projected geothermal generation directly, in GWh, under RE Base and ARED for Jamali and Sumatera from 2025 to 2034. This comparison does not multiply generation by emissions intensity because its purpose is to compare the electricity projections themselves.

These RUPTL figures represent **total projected regional geothermal generation**, not generation from only the new GENESIS projects. Jamali's projected geothermal generation includes electricity imported from Sumatera over the Sumatera-Java interconnection. Sumatera's geothermal-generation projection is identical under RE Base and ARED throughout the period; Jamali's projections are close through 2029 and then diverge, with RE Base higher in 2034. The chart describes PLN's scenario projections; it does not estimate how much electricity only the new planned projects will generate or how many credits they could earn. This direct generation comparison is separate from the fixed-factor ESDM/JCM sensitivity analysis.

## Limitations

Results are gross avoided-emissions potential. They do not subtract project operational emissions, determine whether a project is additional, establish carbon-market eligibility, or account for monitoring, verification, registry rules, curtailment, transmission losses, or actual commissioning dates. They must not be reported as verified or issued credits. The fixed-factor sensitivity chart must not be described as a changing-grid forecast through 2034. RUPTL's projected average intensity is contextual evidence, not an official crediting factor or a marginal displacement estimate.

## Sources

* GENESIS planned unit data and grid mapping in this repository.
* ESDM 2019 grid factors extracted from Kepmen ESDM 163.K/HK.02/MEM.S/2021.
* ESDM, *Indonesian Technology Catalogue 2024*, geothermal section.
* Pertamina Geothermal Energy published operating metrics.
* PLN, *RUPTL 2025–2034*, projected generation and emissions under RE Base and ARED, processed in `ruptl_eda/output/ruptl_projected_generation.csv` and `ruptl_eda/output/ruptl_projected_intensity.csv`.
