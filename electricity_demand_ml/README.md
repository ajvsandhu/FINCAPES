# Exploratory electricity-consumption forecasting

This analysis compares simple and machine-learning methods for forecasting Indonesia's annual electricity consumption per person one year ahead. The target is the World Bank indicator **Electric power consumption (kWh per capita)**, indicator `EG.USE.ELEC.KH.PC`, for 1990-2024. The data snapshot is saved in `data/` so the analysis can be reproduced without an API connection.

## Methods

The evaluation is rolling one-year-ahead. For the 2008 forecast, models train using observations from 1990-2007. After the 2008 actual value is observed, it is included in the training history for the 2009 forecast. This continues through 2024, giving 17 test years. Every method is evaluated on the same years.

Methods compared:

* **Previous year:** forecast the next value as equal to the most recent actual value. This is the main simple baseline.
* **Linear trend:** fit a straight line to all available historical values and extend it one year.
* **Ridge regression:** use calendar year and the previous three observations as inputs; standardize the inputs and use a fixed regularization strength (`alpha=10`).
* **Random Forest:** use the same inputs, with 400 trees, maximum depth 2, minimum leaf size 3, and fixed random seed 42.
* **Ridge + macro features** and **Random Forest + macro features:** add last year's GDP per person, industry value added as a share of GDP, and access to electricity as predictors. These inputs are lagged by one year so the model does not use values from the forecast year.

For Ridge and Random Forest, supervised training examples begin in 1993 because each example requires three prior years. Model settings are fixed and are not tuned against the test years. This is an exploratory comparison, not a model-selection study.

## Results

Across the 17 rolling test forecasts (2008-2024), the previous-year baseline performed best. Its mean absolute percentage error (MAPE) was 6.23%, compared with 6.95% for Ridge with macro features, 8.09% for Ridge alone, 11.64% for the linear trend, 18.96% for Random Forest alone, and 19.33% for Random Forest with macro features. The table also reports mean absolute error (MAE) and root mean squared error (RMSE), both in kWh per person. Adding the macro features improved Ridge compared with Ridge alone, but did not outperform the baseline. It slightly worsened Random Forest compared with Random Forest alone.

This is a small, exploratory comparison. It does not show that ML cannot improve other forecasts, and the WDI consumption-per-person measure is not the same as regional system demand or RUPTL customer sales. The fixed 2008-2024 evaluation period has already informed these experiments, so results are exploratory rather than a fresh, untouched final test.

The project also contains a separate Ember-based experiment on total annual electricity demand (TWh) from 2000-2024. It uses 2000-2009 as the initial training history and tests forecasts from 2010-2024 (15 test years). The previous-year method again performed best: MAPE was 5.88%, compared with 6.19% for the linear trend, 6.44% for Ridge, and 16.42% for Random Forest. Ridge and Random Forest have only seven lagged training examples at the first test forecast, so their scores are especially uncertain. Ember's 2025 value is retained in the source snapshot but excluded because it is an estimate, not a completed historical observation. This target is closer to electricity demand than the World Bank per-capita indicator, but it has fewer years and is still national rather than regional.

The Ember demand snapshot was extracted from the existing project file `ember_indonesia_eda/output/ember_indonesia_all_yearly_combined.csv`, selecting rows where `series == "Demand"`. The `generation_twh` field on those rows records Ember's annual demand (generation plus net imports).

## Run

Requirements: Python 3, pandas, numpy, matplotlib, and scikit-learn.

```bash
python3 forecast_electricity_consumption.py
python3 forecast_ember_demand.py
```

The per-capita script writes `output/rolling_forecast_predictions.csv`, `output/forecast_metrics.csv`, and `output/forecast_comparison.png`. The direct-demand script writes the corresponding files under `output/ember_demand/`.

## Interpretation and limits

The target is annual national consumption per person. It is not monthly demand and does not distinguish Jamali from Sumatera. Thirty-five annual observations are a small sample for machine learning. This analysis can show whether these particular methods improved one-year-ahead forecasts on this series; it cannot establish that machine learning is generally better or worse.

The forecasts do not enter the geothermal avoided-emissions model. Connecting demand forecasts to geothermal emissions estimates would require regional demand and dispatch data, plus a power-system model that estimates which generators respond to demand changes. Do not use these forecasts as grid emission factors or as direct estimates of carbon credits.

## Source

World Bank, World Development Indicators, `EG.USE.ELEC.KH.PC`: [Electric power consumption (kWh per capita), Indonesia](https://data.worldbank.org/indicator/EG.USE.ELEC.KH.PC?locations=ID). Series methodology and definition are available in the [World Bank metadata](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/EG.USE.ELEC.KH.PC).

World Bank predictor series: [GDP per capita, PPP](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD?locations=ID), [industry value added (% GDP)](https://data.worldbank.org/indicator/NV.IND.TOTL.ZS?locations=ID), and [access to electricity (% population)](https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS?locations=ID). Ember source: [Yearly Electricity Data](https://ember-energy.org/data/yearly-electricity-data/).
