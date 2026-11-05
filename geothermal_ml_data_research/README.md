# Better data for geothermal ML: source audit and research scope

Research date: **29 October 2026**. This work does not change the existing demand experiments or geothermal avoided-emissions calculations. **No new forecasting model has been fitted or shown to improve accuracy.**

## Main finding

There is a more directly relevant Indonesian source than national annual demand: **UNFCCC CDM monitoring reports for Wayang Windu** contain daily electricity-generation tables for two units. The inspected reports cover 2013–2014 and 2015–November 2017; a later report contains monthly unit output through June 2021. This makes an Indonesian historical plant-output case study a credible research direction, rather than assuming foreign demand forecasts can predict Indonesian geothermal production.

New Zealand also offers a much larger downloadable geothermal generation panel. All 132 monthly files for 2015–2025 have been downloaded and audited here. These are useful for a foreign benchmark and a deliberately tested transfer experiment, not evidence of Indonesian forecast accuracy.

The Indonesian daily tables have been inspected online, including their headers, beginning/end records, zero-output periods and meter-comparison annexes. **They have not been fully extracted or reconciled into a training dataset.** Five factual example rows and a separate 42-month, two-unit transcription are saved here. Automated local CDM PDF downloads returned HTML challenge pages rather than PDFs; no such response is being represented as a downloaded PDF.

## 1. Keep the three questions separate

| Question | Required target | What this project can claim |
|---|---|---|
| Electricity-demand forecasting | Customer sales, consumption or system load for a defined geography and interval | Planning context; not geothermal production or displaced emissions |
| Geothermal-output forecasting | Measured plant/unit electricity delivered, preferably with operating history | Historical operational forecast skill for evaluated plants and horizons |
| Displaced-emissions estimation | Additional delivered electricity and an appropriate counterfactual grid factor or dispatch model | Conditional avoided-emissions scenarios, not automatic credit issuance |

The existing WDI and Ember experiments address the first question. The newly located plant records address the second. The original fixed-factor emissions model addresses a conditional version of the third. Their targets, sample sizes, units and evaluation errors must not be treated as interchangeable.

## 2. What was actually inspected

### Indonesia: Wayang Windu, UNFCCC project 3193

**2013–2014 monitoring report:** Annex 5, printed pages 54–69 of 74, contains daily columns for total electricity, Unit 2 electricity, existing Unit 1 electricity, steam and reported steam-related project emissions. The first electricity record checked is 1 January 2013; the last checked is 31 December 2014. Annex 6 contains main-meter/check-meter monthly comparisons.

**2015–2017 monitoring report:** Annex 5, printed pages 72–101 of 107, contains daily electricity, steam and project-emissions columns. Checked electricity records extend from 1 January 2015 to 30 November 2017. The report's monitoring-period heading extends to 1 December 2017, but the inspected daily annex ends on 30 November: do not manufacture a December 1 record from the heading. The June–August 2015 generation tables include genuine reported zeros; missing values and operational zeros must remain distinguishable. Full continuity, unique-date counts and report-total reconciliation remain to be audited.

**Later revised v04 report:** Annex 5, printed pages 90–94 of 99, contains monthly tables labelled Main Meter for each unit. `data/wayang_windu_monthly_main_meter_2018_2021.csv` transcribes **January 2018–June 2021: 42 months, 84 unit-month values**. It excludes December 2017 because that monitoring period starts on December 2. Earlier-report December placeholders must not be interpreted as a full month of zero physical output.

Important measurement issues:

- Daily DCS/check-meter data, monthly main-meter readings and conservative values used for credit calculations are separate series. Do not silently splice them together.
- The older report's monthly comparisons contain material meter differences in some 2017 months. The later report also notes 0.2% meter-error adjustments for August/September 2018.
- The earlier 93-page and revised 99-page later reports differ in some values, including December 2020 and January 2021. The saved monthly transcription consistently uses the revised v04 report, not a mixture.
- Two units sharing one field do not provide two independent sites. Historic site data cannot establish generalization to Sumatera or future GENESIS greenfield projects.
- The monthly transcription has temporal/numeric checks, but a complete daily-to-monthly reconciliation and independent second transcription check are not finished. It is a research starting extract, not deployment-ready data.

**Usability decision:** strongest Indonesian plant-output lead; daily extraction and measurement harmonization are a bounded data-preparation task on identified documents, not an unspecified future search. There is enough evidence to pursue a historical ML case study. There is not yet a fully audited Indonesian daily training panel.

### Indonesia: BPS monthly electricity tables

Two public page payloads were downloaded and parsed without an API key:

- Lampung province **Listrik Terjual (bulanan)**: 2014 only in the retrieved table and year selector. Twelve months and an annual-total row, for three branches plus their total: 52 cells. That is **12 dates**, not 52 independent monthly observations. Units are MWh.
- Bandar Lampung **Besar Pemakaian Listrik Menurut Bulan**: the retrieved 2023 table has 12 months for postpaid and prepaid consumption: 24 cells. Its year selector advertises 2019–2023, but the other four years were not retrieved and validated. A simple `?year=...` request still returned 2023 and therefore did not establish a five-year series. Units are kWh.

These are useful evidence that monthly Indonesian demand-related data exist, but neither retrieved extract is a long regional load series. They measure customer sales/usage, not geothermal generation, and a PLN service area is not automatically the entire Jamali or Sumatera grid. Do not concatenate provincial and city records as if they had identical boundaries.

### Indonesia: PGE and PLN disclosures

PGE's investor-update index exposes selected October 2024 and January 2025 operational releases, not a confirmed continuous monthly archive. The January release reports consolidated **steam and electricity** in GWh-equivalent terms and working-area outputs. The October release includes ten-month cumulative figures and full-year outlooks. These cannot all be treated as monthly net electricity delivered. The operating narratives identify steam shortages and maintenance, useful for designing predictors, but realized outages and same-month steam are not automatically known at forecast time.

The PLN Statistics 2024 publication was located on PLN's official site. It is annual reporting, not evidence of an accessible long monthly/hourly Jamali/Sumatera load feed. Its PDF could not be downloaded locally in this run. No claim that public higher-frequency Indonesian data do not exist follows from these access limits.

### New Zealand: Electricity Authority EMI Generation_MD

Downloaded **2015-01 through 2025-12**, all 132 monthly CSV files. Extracted only rows with `Fuel_Code == Geo`. Official dataset documentation describes half-hour energy in **kWh**, based on metered data as a proxy for generation; `Gen_Code` is the plant-series aggregation key. It is not reservoir or well telemetry.

Audit results:

- **49,438 geothermal meter-day rows**, **2,373,024 nonmissing half-hour values**.
- **15 literal generator codes**, or **14 after case folding**. These are code counts, not an independently verified physical-plant count.
- **1,622 generator-month groups** using the original codes; every group contains all calendar dates for its month.
- No duplicate full meter/date keys, no negative interval values, and 1,638 zero-output meter-day rows.
- 46/48/50 interval rows match the expected need to handle daylight-saving clock changes; absent TP49/TP50 on ordinary days are structural, not missing ordinary half-hours.
- `Te_Mihi` changes to `te_mihi` at 2020; both have site `THI`, connection `THI2201`, and non-overlapping dates. Preserve original codes and document any alias harmonization.
- `norskeskog` has **64 dates with multiple network rows**. A spot check on 9 May 2023 found positive values in both rows in five trading periods. The meaning of those overlaps is unresolved; exclude that series from an initial benchmark rather than assuming every row is additive.
- `Tauhara` appears from November 2023 in these files; presence in a metering file does not establish commercial operation throughout the period. Commissioning, capacity changes, site aliases and technology require fleet metadata.

**Usability decision:** a successfully downloaded and auditable high-frequency candidate panel. Use daily aggregation initially, preserve zeros, resolve aliases, and exclude ambiguous meter combinations. Millions of interval values are not millions of independent operating situations.

### United States: EIA-923

Downloaded the **2024 final ZIP** and inspected `Page 1 Generation and Fuel Data` in the schedules 2–5 workbook. The geothermal filter (`Reported Fuel Type Code == GEO`) produces:

- **63 plant IDs**, represented by **72 plant/prime-mover/fuel rows**.
- Twelve monthly net-generation columns and **864 numeric monthly cells**.
- Prime movers: 41 `BT` rows and 31 `ST` rows. This is not a single homogeneous geothermal technology.
- Respondent-frequency flags: 57 `AM`, 15 `M`; these flags and measured/estimated monthly reporting need interpretation before training. Numeric cells alone are not proof of independent measured monthly observations.

EIA's official archive provides additional years, and the page now lists 2025 final data; this audit deliberately inspected 2024, not all available years or the latest full archive. Join historical EIA-860 capacities and technology, inspect revisions and reporting flags, and preserve the plant/prime-mover level. The U.S. is a plausible second-country extension, not the simplest first transfer source given the already downloaded New Zealand panel.

## 3. Recommended research question

> **Can lagged generation improve one-day-ahead electricity-output forecasts for the historical Wayang Windu units relative to persistence, and does adding New Zealand geothermal operating histories improve those Indonesian forecasts?**

This is a concrete, Indonesia-centred historical pilot with two stages:

1. **Domestic model first:** use the identified 2013–November 2017 daily annexes after extraction and reconciliation. Compare persistence and trailing means with regularized regression and one small tree-based model. Use lagged generation, past-only rolling summaries and calendar features. Add lagged steam only if its timing and measurement are consistent. Keep same-day steam, total generation containing the target, same-day other-unit output and post-event outage narratives out of the predictor set.
2. **Transfer as an experiment:** aggregate the cleaned New Zealand interval data to daily energy and compare (a) Indonesia-only training, (b) foreign-only prediction, and (c) pooled/shared training with Indonesian calibration. A small shared regression or tree model is sufficient; a neural-network pretraining exercise is not justified merely because many half-hour rows exist.

The monthly Indonesian extract is immediately available for inspection and a small exploratory benchmark, but 42 dates from one site are not enough to make strong transfer claims. Do not expand monthly readings into artificial daily labels. The historic daily case study is not a model validated for operating Indonesian plants in 2026.

## 4. Validation design, fixed before fitting

- **Domestic chronology:** develop on 2013–2015, select features/settings with past-only rolling folds in 2016, and reserve January–November 2017 for a locked historical evaluation. Source inspection has occurred; call this a pre-specified evaluation, not a claim of untouched data. If model comparisons later influence changes, disclose that reuse.
- **Foreign chronology:** for every Indonesian forecast origin, use only foreign dates before that origin. The downloaded 2018–2025 New Zealand observations must not train a model evaluated as a 2017 Indonesian forecast. Initially use pre-2016 foreign data for development and allow later foreign records only as time advances. Later years can support a separate modern New Zealand benchmark, not retrospective leakage into Indonesia.
- **Horizon:** forecast the next day, not the next ten years. State whether the full previous-day generation is assumed available at the origin. These are revised historical records, so this is not proof that the original publications were available in real time.
- **Same cases:** evaluate all competing methods on the same Indonesian dates/units and feature-availability conditions. Fit scalers, imputers and normalization on training data only. If capacity is not consistent, use a documented past-only scale rather than an invented capacity factor.
- **Metrics:** MAE and RMSE in MWh/day, MASE where its training denominator is nonzero, and errors for outage versus normal-operation days. Do not make MAPE the main metric when observed generation can be zero. Compare against previous-day generation, a trailing seven-day mean and a constant-capacity-factor baseline only if consistent capacity is available.
- **Dependence:** resample paired errors in date blocks, keeping both units together, for uncertainty intervals. Do not randomly split neighboring days or place one unit's same-day outcome in another unit's features. Report the number of sites and actual dates, not just row counts.
- **Transfer acceptance:** claim an improvement only if the transferred/pooled method beats both the best simple baseline and the Indonesia-only method on the same reserved Indonesian cases, with uncertainty and regime-specific errors reported. Worse results are evidence of negative transfer, not a reason to hide the foreign-only result.
- **Scope of generalization:** two units at one field cannot establish transfer to another Indonesian field, Sumatera or unbuilt GENESIS projects. Those claims require other Indonesian sites and new chronological evaluations. A leave-one-site-out experiment within New Zealand can test foreign cross-site behavior, but cannot replace the Indonesian test.

## 5. Link to the avoided-emissions study without changing the target

Observed and forecast plant output can support an operational-energy component, and measured annual generation/capacity can eventually inform empirical operating scenarios. The emissions step remains separate: conditional gross avoided emissions equal additional delivered MWh times an appropriate grid emission factor. Subtracting project emissions and applying any crediting requirements are further steps.

A next-day output model does **not** identify the marginal displaced generator, forecast official OM/BM/CM factors through 2034, or justify replacing every planned plant's 80% capacity factor with a foreign prediction. Do not import New Zealand or U.S. grid factors into Indonesian calculations. For now, retain the original GENESIS capacity-factor sensitivity as a transparent scenario model and present the new ML work as a linked operational case study, not a validated ten-year emissions forecast.

## Files and reproducibility

- `data/wayang_windu_monthly_main_meter_2018_2021.csv`: 42-month numerical transcription; source/version/QA in `output/wayang_windu_audit.json`.
- `data/wayang_windu_daily_examples.csv`: five source-check examples, **not a daily training dataset**. PDF document IDs identify sources in `sources.csv`.
- `data/nz_geothermal_meter_days.csv.gz`: extracted half-hour geothermal rows, raw codes retained.
- `data/nz_geothermal_generator_months.csv`: provisional sums, **not yet a final modelling table**; ambiguous network rows retained for auditing.
- `data/us_geothermal_eia923_2024_rows.csv`: geothermal worksheet subset, original reporting flags retained.
- `data/lampung_monthly_sales.csv`, `data/bandar_lampung_monthly_usage.csv`: parsed BPS extracts, with totals/categories explicitly retained.
- `raw/`: compressed original NZ CSVs, U.S. ZIP, BPS HTML/JSON snapshots and NZ dataset documentation. No local CDM/PGE/PLN PDF is claimed.
- `output/`: machine-readable audit summaries, coverage and SHA-256 download manifests.
- `sources.csv`: official source/download addresses and inspection status.

Run with Python 3, pandas, requests and openpyxl:

```bash
python3 audit_sources.py --source nz --start 2015 --end 2025
python3 audit_sources.py --source eia
python3 audit_sources.py --source bps
python3 audit_sources.py --source wayang
```

The NZ and U.S. downloads are cached. BPS refreshes its public pages. The Wayang command validates the saved transcription; it does not re-download or independently re-extract the PDF. Keep the dated snapshots when reproducing a result because official sources may be revised.

## Report-ready conclusion

The data search identified a more relevant alternative to annual national electricity-demand forecasting: historical plant-output modelling using Indonesian geothermal monitoring records. UNFCCC reports for Wayang Windu contain daily unit-generation tables, while later reports provide monthly output. A larger New Zealand geothermal dataset has also been downloaded and audited and could support pooled-training or transfer experiments. These findings establish feasible data sources, not improved predictive accuracy. The recommended study first tests simple and machine-learning forecasts on Indonesian plant records, then evaluates whether foreign operating histories add value on the same chronological Indonesian cases. Operational output forecasting remains distinct from estimating displaced grid emissions or carbon-credit issuance.
