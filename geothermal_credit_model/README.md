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

For a future pathway, an official ex-ante factor can only support years within its published coverage. A separate, clearly labelled approach is needed for 2031-2034. RUPTL emissions divided by generation can describe projected average system intensity under RE Base and ARED, but this proxy is not an official OM, BM or CM and should not be presented as one.

## RUPTL scenario comparison

The separate `ruptl_scenario_intensity_proxy.csv` and `ruptl_scenario_intensity_proxy.png` combine each year's planned geothermal generation estimate with the RUPTL projected **average** grid intensity for the matching grid, year, and scenario (RE Base or ARED):

`intensity-weighted proxy (tCO2) = estimated geothermal generation (MWh) x RUPTL average intensity (tCO2/MWh)`

This gives a like-for-like illustration of how the RE Base and ARED system pathways change the intensity-weighted estimate through 2034. The chart shows annual values for the central 80% capacity-factor case; the CSV also includes 70% and 90% cases. It is a scenario comparison, not a forecast of credits or a method for calculating official avoided emissions. Average system intensity describes all generation in the RUPTL system; it does not identify which generators geothermal would displace. RUPTL projections may also already include the planned geothermal additions, so applying system-average intensity to those same additions can double count their effect if interpreted causally. Treat the output as an illustrative proxy only. It complements the fixed-factor sensitivity chart and does not replace official ESDM/JCM crediting methodologies.

## Limitations

Results are gross avoided-emissions potential. They do not subtract project operational emissions, determine whether a project is additional, establish carbon-market eligibility, or account for monitoring, verification, registry rules, curtailment, transmission losses, or actual commissioning dates. They must not be reported as verified or issued credits. The fixed-factor sensitivity chart must not be described as a changing-grid forecast through 2034.

## Sources

* GENESIS planned unit data and grid mapping in this repository.
* ESDM 2019 grid factors extracted from Kepmen ESDM 163.K/HK.02/MEM.S/2021.
* ESDM, *Indonesian Technology Catalogue 2024*, geothermal section.
* Pertamina Geothermal Energy published operating metrics.
* PLN, *RUPTL 2025–2034*, projected generation and emissions under RE Base and ARED, processed in `ruptl_eda/output/ruptl_projected_intensity.csv`.
