# Wayang Windu monthly generation EDA

This follows the earlier project EDA format: a reproducible Python script, tidy CSVs, a data dictionary, quality checks, PNG charts, a browsable HTML report, and report-ready findings.

## Scope

**Monthly output, not the unfinished daily dataset.** The input is the 42-month transcription of the UNFCCC revised-v04 Main Meter tables for January 2018-June 2021, for two units at one Indonesian geothermal field. Five illustrative daily rows are not used. Direct downloads of the daily PDFs and a supporting workbook returned HTML challenge pages during this run; the full daily dataset is not claimed to be extracted.

All 84 monthly values were compared again against the revised report's online table text on 30 October 2026; all five table page images were inspected. This same-analyst check found no numeric mismatches, but is not independent-person transcription QA or reconciliation to daily readings. Original published values and source-page references are preserved. The existing research folder is not modified.

## Run

```bash
python3 -m pip install pandas numpy matplotlib
python3 wayang_windu_eda/wayang_windu_eda.py
```

Run the second command from the repository root, or use the script's absolute path from any directory. No API key, network connection or browser server is required. Dependencies used: Python 3.9, pandas 2.3.3, numpy 2.0.2, matplotlib 3.9.4. The analysis date records the source check, not an automatically refreshed download date.

## Start here

- `output/wayang_windu_data.html`: self-contained charts, findings, data tables and audit, with embedded images; opens directly in a browser.
- `output/eda_findings.md`: report-ready interpretation, limitations and next modelling steps.
- `output/wayang_windu_monthly_tidy.csv`: one unit-month per row, derived quantities and provenance.
- `output/data_quality_audit.json`: coverage, source version, input SHA-256 and QA status.
- `output/data_dictionary.csv`: definitions and units.
- `output/summary_statistics.csv`, `output/annual_generation_and_coverage.csv`, `output/comparable_january_june_generation.csv`, `output/lag_correlations.csv`, `output/low_output_months.csv`: descriptive outputs.
- Five PNG figures: time series, distribution, annual/half-year totals, calendar heatmap and lag relationships.

## Interpretation safeguards

- Monthly average MW = monthly MWh / calendar hours. MWh/day is only a monthly average, not measured daily values. No capacity factor is inferred.
- July-December 2021 is outside coverage, not zero. Full-year charts use 2018-2020 only; January-June comparisons retain equal coverage across 2018-2021.
- All 42 months inform this descriptive EDA. They are not an untouched final test set. No forecast accuracy or ML improvement is claimed.
- Low-output flags use an exploratory full-sample median threshold and are not diagnoses, reasons to delete records or forecasting inputs.
- The two units share a field; retain date-grouped chronological evaluation if a pilot model is built. Monthly data do not validate daily forecasts, 2026 operations, cross-field transfer, displaced emissions or issued credits.

Official report: https://cdm.unfccc.int/UserManagement/FileStorage/FSK5I6HGV4BJ39YARNEOXZ18Q7MWUP

Supporting-document registry: https://cdm.unfccc.int/Projects/DB/TUEV-SUED1260194062.48/CP/3MD0A9GB28W7MMR77ZOJJ4GVK8D0V4/iProcess/RWTUV1633521981.91/view
