# Planned geothermal: gross avoided-emissions model

This model estimates the potential avoided grid emissions from capacity planned in GENESIS for Jamali and Sumatera between 2025 and 2034. It is not a calculation of issued carbon credits.

## Calculation

For every year and grid:

`estimated generation (MWh) = operating planned capacity (MW) x 8,760 x capacity factor`

`gross avoided emissions (tCO2) = estimated generation (MWh) x emission factor (tCO2/MWh)`

The model applies a one-year lag between the stated commissioning year and the first full generation year. This avoids assuming that a new unit produces a full year of electricity in its commissioning year. Capacity planned for 2034 therefore does not contribute within the 2025-2034 analysis window.

## Capacity-factor scenarios

The low, central, and high cases are 70%, 80%, and 90%. The central 80% case is supported by ESDM's *Indonesian Technology Catalogue 2024*, which reports Indonesian geothermal generation of about 16.6 TWh from 2,360 MW in 2022, equivalent to over 80%. The 90% upper case reflects PGE's published operating performance. The 70% lower case is deliberately conservative.

## Factor-method sensitivity

The model holds generation constant and changes only the emission factor. It compares ESDM 2019 OM, BM, CM ex-post 50/50 and CM ex-ante 50/50 with the separate JCM alternative. ESDM factors are official historical/projecting grid factors, while the JCM factors use a different methodology and period; the JCM values are included for sensitivity, not as an interchangeable official replacement.

## Limitations

Results are gross avoided-emissions potential. They do not subtract project operational emissions, determine whether a project is additional, establish carbon-market eligibility, or account for monitoring, verification, registry rules, curtailment, transmission losses, or actual commissioning dates. They must not be reported as verified or issued credits.

## Sources

* GENESIS planned unit data and grid mapping in this repository.
* ESDM 2019 grid factors extracted from Kepmen ESDM 163.K/HK.02/MEM.S/2021.
* ESDM, *Indonesian Technology Catalogue 2024*, geothermal section.
* Pertamina Geothermal Energy published operating metrics.
