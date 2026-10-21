# RUPTL 2025-2034: EDA findings for Jamali and Sumatera

## What was extracted

The analysis extracts historical sales and generation (2015-2024), projected sales, generation and emissions (2025-2034), and planned capacity additions (2025-2034) from PLN's RUPTL 2025-2034. The tidy CSV files in this folder are the analysis-ready outputs. `ruptl_data.html` provides a browsable version of every extracted table, data dictionary and filtering note.

## Data-quality checks

All 20 historical grid-year fuel totals agree with the RUPTL subtotal within 3 GWh. All 40 projected grid-scenario-year fuel totals agree within 3 GWh. This provides a strong internal check on the extraction.

Projected emissions are rounded in the source. Five Jamali ARED year totals differ from the sum of displayed coal, gas and oil emissions by 0.27-0.40 MtCO2. Use the source's displayed `Total` row for average-intensity calculations, and describe these small differences as rounding.

Sumatera historical sales for household, industry, business and total repeat exactly between 2023 and 2024, while public sales differs. Since the source labels 2024 as a forecast (`prognosa`), retain the figures but do not interpret the repeated categories as observed data.

One ownership row, Sumatera ARED IPP geothermal, is blank in the source table. The total geothermal addition is still present (2,017 MW), and it matches GENESIS. The blank must remain missing rather than being treated as zero.

## Scope and interpretation

Historical RUPTL generation combines Sumatera and Kalimantan. It is therefore suitable for observing the geothermal row (Kalimantan has no geothermal plants) but not for claiming a Sumatera-only historical fuel mix. Use a Sumatera-only source, such as Statistik PLN, if the research requires that mix.

The 2024 generation figures are unaudited and cover January-October only. They are retained as a flagged partial year and excluded from trend charts.

RUPTL covers PLN-owned, rented and IPP supply; it excludes captive generation. This explains why it should not be expected to equal Ember's national total. In 2015-2023, Jamali plus Sumatera/Kalimantan geothermal generation represents 90.6-95.6% of Ember's national `Other renewables` category, consistent with geothermal being the dominant component.

The derived projected average intensity is total RUPTL combustion emissions divided by total generation. The fossil-only intensity is total emissions divided by coal, gas and oil generation. Neither measure is an official OM, BM or CM and neither should replace the ESDM factors in credit calculations.

## Findings relevant to the research question

RUPTL and GENESIS agree exactly on planned geothermal additions: 2,503 MW in Jamali and 2,017 MW in Sumatera in both scenarios. This supports using the RUPTL to represent the rest of the generation system alongside the GENESIS geothermal project data.

For 2025, RUPTL's average projected grid intensity is 0.882 tCO2/MWh in Jamali and 0.695 tCO2/MWh in Sumatera. The corresponding ESDM 2019 CM factors are 0.87 and 0.94 tCO2/MWh. The Sumatera difference is material and reflects different definitions: RUPTL's average mix includes low-carbon generation, whereas CM is a project-crediting factor built from OM and BM.

Jamali's projected geothermal generation cannot be converted directly into a local capacity factor after 2030. The RUPTL table notes that Jamali's hydro and geothermal generation include imports through the Sumatera-Java interconnection. The diagnostic exceeds 100% from 2031 because it compares that wider energy supply with Jamali's local GENESIS capacity. Do not use it as a capacity-factor estimate.

## Recommended use in the report

Use the historical and projected RUPTL generation, emissions and additions as the grid-system evidence. Use ESDM OM/BM/CM factors as the official crediting-factor evidence. Keep the boundaries separate in the methods section, and state the Sumatera+Kalimantan and interconnection limitations explicitly.
