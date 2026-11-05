import base64
import hashlib
import html
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_FILE = SCRIPT_DIR / "data/wayang_windu_monthly_main_meter_2018_2021.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"
SOURCE_URL = "https://cdm.unfccc.int/UserManagement/FileStorage/FSK5I6HGV4BJ39YARNEOXZ18Q7MWUP"
REGISTRY_URL = "https://cdm.unfccc.int/Projects/DB/TUEV-SUED1260194062.48/CP/3MD0A9GB28W7MMR77ZOJJ4GVK8D0V4/iProcess/RWTUV1633521981.91/view"
UNITS = {"unit_1": "Unit 1", "unit_2": "Unit 2"}
COLORS = {"unit_1": "#2266a5", "unit_2": "#b4551c"}
ANALYSIS_DATE = "2026-10-30"


def prepare_data():
    original = pd.read_csv(INPUT_FILE)
    required = ["month", "unit_1_reported_mwh", "unit_2_reported_mwh", "unit_1_pdf_page", "unit_2_pdf_page", "source_note"]
    if original.columns.tolist() != required:
        raise ValueError("Unexpected source schema")
    frame = original.copy()
    frame["date"] = pd.to_datetime(frame["month"], format="%Y-%m", errors="raise")
    if frame["date"].duplicated().any():
        raise ValueError("Duplicate months require reconciliation")
    frame = frame.sort_values("date").reset_index(drop=True)
    expected = pd.date_range("2018-01-01", "2021-06-01", freq="MS")
    missing = expected.difference(frame["date"])
    extra = pd.DatetimeIndex(frame["date"]).difference(expected)
    if len(missing) or len(extra):
        raise ValueError("Unexpected coverage; do not silently fill months")
    frame["year"] = frame["date"].dt.year
    frame["calendar_month"] = frame["date"].dt.month
    frame["days_in_month"] = frame["date"].dt.days_in_month
    frame["hours_in_month"] = frame["days_in_month"] * 24
    frame["published_meter_adjustment_note"] = frame["month"].isin(["2018-08", "2018-09"])
    tidy = []
    for unit, label in UNITS.items():
        values = pd.to_numeric(frame[f"{unit}_reported_mwh"], errors="raise")
        if values.isna().any() or not np.isfinite(values).all() or (values < 0).any():
            raise ValueError(f"Invalid generation values for {label}")
        frame[f"{unit}_average_mw"] = values / frame["hours_in_month"]
        frame[f"{unit}_mean_mwh_per_day"] = values / frame["days_in_month"]
        part = frame[["month", "date", "year", "calendar_month", "days_in_month", "hours_in_month", "published_meter_adjustment_note"]].copy()
        part["unit"] = label
        part["reported_generation_mwh"] = values
        part["monthly_average_mw"] = frame[f"{unit}_average_mw"]
        part["mean_mwh_per_day"] = frame[f"{unit}_mean_mwh_per_day"]
        part["previous_month_average_mw"] = part["monthly_average_mw"].shift(1)
        part["change_from_previous_month_mw"] = part["monthly_average_mw"].diff()
        median = part["monthly_average_mw"].median()
        part["below_90pct_sample_unit_median"] = part["monthly_average_mw"] < 0.9 * median
        part["source_pdf_printed_page"] = frame[f"{unit}_pdf_page"]
        part["source_url"] = SOURCE_URL
        part["source_version"] = "04, completed 2022-04-28"
        tidy.append(part)
    frame["combined_reported_mwh"] = frame[[f"{unit}_reported_mwh" for unit in UNITS]].sum(axis=1)
    return frame, pd.concat(tidy, ignore_index=True)


def save_chart(figure, filename):
    figure.savefig(OUTPUT_DIR / filename, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def charts(frame, tidy):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.2})
    figure, axes = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True, constrained_layout=True)
    for unit, label in UNITS.items():
        axes[0].plot(frame["date"], frame[f"{unit}_reported_mwh"] / 1000, marker=".", label=label, color=COLORS[unit])
        axes[1].plot(frame["date"], frame[f"{unit}_average_mw"], marker=".", label=label, color=COLORS[unit])
    axes[0].set(title="Wayang Windu: reported monthly electricity", ylabel="Monthly energy (GWh)")
    axes[1].set(title="Month-length-adjusted view: monthly average power", ylabel="Monthly average (MW)", xlabel="Month")
    axes[0].legend(ncol=2)
    axes[1].annotate("Unit 1: June 2019 dip\nCause not inferred from this plot", xy=(pd.Timestamp("2019-06-01"), frame.loc[frame["month"].eq("2019-06"), "unit_1_average_mw"].iloc[0]), xytext=(pd.Timestamp("2019-09-01"), 84), arrowprops={"arrowstyle": "->", "color": "#555555"})
    axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    save_chart(figure, "monthly_generation_and_average_power.png")

    figure, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for unit, label in UNITS.items():
        values = frame[f"{unit}_average_mw"]
        axes[0].hist(values, bins=np.linspace(72, 113, 18), alpha=0.6, label=label, color=COLORS[unit])
    axes[0].set(title="Distribution of monthly average power", xlabel="Monthly average (MW)", ylabel="Months")
    axes[0].legend()
    axes[1].boxplot([frame[f"{unit}_average_mw"] for unit in UNITS], tick_labels=list(UNITS.values()), showmeans=True)
    axes[1].set(title="Spread and unusual observations", ylabel="Monthly average (MW)")
    save_chart(figure, "generation_distribution.png")

    figure, axes = plt.subplots(1, 2, figsize=(11, 4.7), constrained_layout=True)
    for unit, label in UNITS.items():
        complete = frame[frame["year"].le(2020)].groupby("year")[f"{unit}_reported_mwh"].sum() / 1000
        offset = -0.18 if unit == "unit_1" else 0.18
        axes[0].bar(np.arange(len(complete)) + offset, complete.values, width=0.36, label=label, color=COLORS[unit])
        comparable = frame[frame["calendar_month"].le(6)].groupby("year")[f"{unit}_reported_mwh"].sum() / 1000
        axes[1].plot(comparable.index, comparable.values, marker="o", label=label, color=COLORS[unit])
    axes[0].set(xticks=np.arange(3), xticklabels=[2018, 2019, 2020], title="Complete calendar years only", ylabel="Reported energy (GWh)", xlabel="Year")
    axes[0].set_ylim(0, 1100)
    axes[0].legend()
    axes[1].set(xticks=[2018, 2019, 2020, 2021], title="Like-for-like January-June comparison", ylabel="January-June energy (GWh)", xlabel="Year")
    axes[1].legend()
    save_chart(figure, "annual_and_comparable_half_year_generation.png")

    figure, axes = plt.subplots(2, 1, figsize=(11, 5.8), constrained_layout=True)
    for axis, (unit, label) in zip(axes, UNITS.items()):
        pivot = frame.pivot(index="year", columns="calendar_month", values=f"{unit}_average_mw").reindex(columns=range(1, 13))
        image = axis.imshow(np.ma.masked_invalid(pivot.values), aspect="auto", cmap="viridis", vmin=75, vmax=112)
        for row in range(len(pivot)):
            for column in range(12):
                value = pivot.iloc[row, column]
                axis.text(column, row, "--" if pd.isna(value) else f"{value:.1f}", ha="center", va="center", color="black" if pd.isna(value) or value > 97 else "white", fontsize=8)
        axis.set(title=label, yticks=range(len(pivot)), yticklabels=pivot.index, xticks=range(12), xticklabels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        axis.grid(False)
    figure.colorbar(image, ax=axes, label="Monthly average power (MW)", shrink=0.85)
    figure.suptitle("Calendar view: missing July-December 2021 is outside coverage, not zero")
    save_chart(figure, "calendar_heatmap_average_power.png")

    figure, axes = plt.subplots(1, 2, figsize=(11, 4.7), constrained_layout=True)
    for unit, label in UNITS.items():
        part = tidy[tidy["unit"].eq(label)]
        axes[0].scatter(part["previous_month_average_mw"], part["monthly_average_mw"], color=COLORS[unit], label=label, alpha=0.8)
        values = [frame[f"{unit}_average_mw"].autocorr(lag) for lag in range(1, 13)]
        axes[1].plot(range(1, 13), values, marker=".", color=COLORS[unit], label=label)
    axes[0].plot([72, 113], [72, 113], color="#666666", linestyle="--", label="Unchanged output")
    axes[0].set(title="Previous vs current month", xlabel="Previous month's average (MW)", ylabel="Current month's average (MW)")
    axes[0].legend()
    axes[1].axhline(0, color="#666666", linewidth=1)
    axes[1].set(title="Descriptive autocorrelation, not forecast accuracy", xlabel="Lag (months)", ylabel="Pearson correlation", xticks=range(1, 13), ylim=(-1, 1))
    axes[1].legend()
    save_chart(figure, "lag_relationships.png")


def summarize(frame, tidy):
    summary = []
    for unit, label in UNITS.items():
        part = tidy[tidy["unit"].eq(label)]
        values = part["monthly_average_mw"]
        minimum = part.loc[values.idxmin()]
        maximum = part.loc[values.idxmax()]
        summary.append({"unit": label, "months": len(part), "mean_monthly_mwh": part["reported_generation_mwh"].mean(), "total_mwh_in_covered_period": part["reported_generation_mwh"].sum(), "time_weighted_average_mw": part["reported_generation_mwh"].sum() / part["hours_in_month"].sum(), "unweighted_mean_monthly_average_mw": values.mean(), "median_monthly_average_mw": values.median(), "sample_std_monthly_average_mw": values.std(), "min_month": minimum["month"], "min_monthly_average_mw": values.min(), "max_month": maximum["month"], "max_monthly_average_mw": values.max(), "zero_months": int(part["reported_generation_mwh"].eq(0).sum()), "lag1_monthly_average_mw_correlation": values.autocorr(), "lag1_raw_monthly_mwh_correlation": part["reported_generation_mwh"].autocorr(), "months_below_90pct_sample_median": int(part["below_90pct_sample_unit_median"].sum())})
    annual = tidy.groupby(["unit", "year"]).agg(months_present=("month", "size"), reported_generation_mwh=("reported_generation_mwh", "sum"), hours_covered=("hours_in_month", "sum")).reset_index()
    annual["complete_calendar_year"] = annual["months_present"].eq(12)
    annual["coverage_label"] = np.where(annual["complete_calendar_year"], "January-December", "January-June only; not annualized")
    annual["time_weighted_average_mw"] = annual["reported_generation_mwh"] / annual["hours_covered"]
    half_year = tidy[tidy["calendar_month"].le(6)].groupby(["unit", "year"]).agg(months_present=("month", "size"), january_june_mwh=("reported_generation_mwh", "sum")).reset_index()
    lags = []
    for unit, label in UNITS.items():
        for lag in range(1, 13):
            lags.append({"unit": label, "lag_months": lag, "paired_months": len(frame) - lag, "raw_monthly_mwh_correlation": frame[f"{unit}_reported_mwh"].autocorr(lag), "monthly_average_mw_correlation": frame[f"{unit}_average_mw"].autocorr(lag)})
    quality = {"analysis_date": ANALYSIS_DATE, "target": "Reported Main Meter monthly electricity, not daily observations", "source_version": "04, completed 2022-04-28", "source_url": SOURCE_URL, "registry_url": REGISTRY_URL, "source_sha256": hashlib.sha256(INPUT_FILE.read_bytes()).hexdigest(), "source_printed_pages": [90, 91, 92, 93, 94], "first_month": frame["month"].iloc[0], "last_month": frame["month"].iloc[-1], "distinct_months": len(frame), "unit_month_observations": len(tidy), "distinct_fields": 1, "duplicate_months": int(frame["month"].duplicated().sum()), "missing_months_within_expected_coverage": 0, "missing_generation_values": int(tidy["reported_generation_mwh"].isna().sum()), "negative_generation_values": int(tidy["reported_generation_mwh"].lt(0).sum()), "zero_generation_months": int(tidy["reported_generation_mwh"].eq(0).sum()), "published_meter_adjustment_months": ["2018-08", "2018-09"], "source_comparison": "All 84 values compared with online revised-v04 PDF text; all five table page images inspected on 2026-10-30; zero numeric mismatches. Same analyst second pass, not independent-person QA or daily reconciliation.", "daily_download_status": "Direct PDF and supporting XLSX downloads returned HTML challenge pages; no complete daily dataset was extracted.", "daily_example_rows_excluded": 5, "excluded_months": {"2017-12": "Monitoring begins December 2; not a full calendar month", "2021-07_through_2021-12": "Outside source coverage; never filled with zero"}, "evaluation_status": "Descriptive EDA across all 42 months. No model evaluated. This period is not an untouched final holdout."}
    return pd.DataFrame(summary), annual, half_year, pd.DataFrame(lags), quality


def data_dictionary():
    rows = [
        ("month", "YYYY-MM", "Calendar month; 42 dates, not 84 independent dates"),
        ("unit", "text", "Unit 1 or Unit 2 at one geothermal field"),
        ("reported_generation_mwh", "MWh/month", "Published Main Meter series; not automatically identical to energy used for credit calculations"),
        ("monthly_average_mw", "MW", "Monthly MWh divided by calendar hours; monthly average, not instantaneous or rated capacity"),
        ("mean_mwh_per_day", "MWh/day", "Monthly MWh divided by calendar days; NOT reconstructed daily observations"),
        ("days_in_month", "days", "Calendar days including February 2020 leap day"),
        ("hours_in_month", "hours", "24 times calendar days; no daylight saving in this Indonesian series"),
        ("previous_month_average_mw", "MW", "Previous chronological monthly average; first value missing by construction"),
        ("change_from_previous_month_mw", "MW", "Current minus previous monthly average; descriptive change, not forecast error"),
        ("below_90pct_sample_unit_median", "boolean", "Descriptive low-output screen using full-sample unit median; not an outage diagnosis or deployable forecast input"),
        ("published_meter_adjustment_note", "boolean", "Published 0.2% meter-error note applies August/September 2018; values retained without adjusting again"),
        ("source_pdf_printed_page", "page", "One-based printed page in 99-page revised-v04 report"),
        ("source_url", "URL", "Official UNFCCC source document"),
        ("source_version", "text", "Consistently revised v04; do not splice earlier report versions"),
        ("date", "YYYY-MM-DD", "First day of month, a period label rather than a daily measurement"),
        ("year", "year", "Calendar year; 2021 is partial"),
        ("calendar_month", "1-12", "Month number; only 3-4 repetitions per month")
    ]
    return pd.DataFrame(rows, columns=["field", "unit_or_format", "meaning"])


def write_report(frame, tidy, summary, annual, lags, quality):
    first, second = summary.iloc[0], summary.iloc[1]
    low = tidy[tidy["below_90pct_sample_unit_median"]]
    totals = annual.pivot(index="year", columns="unit", values="reported_generation_mwh")
    change_2019 = (totals.loc[2019].sum() / totals.loc[2018].sum() - 1) * 100
    change_2020 = (totals.loc[2020].sum() / totals.loc[2019].sum() - 1) * 100
    findings = f"""# Wayang Windu monthly generation: EDA findings

Analysis date: {ANALYSIS_DATE}. No forecasting model was trained or evaluated.

## 1. Aim and scope

Explore the consistency, coverage, output variation and lag relationships of published Indonesian geothermal electricity records before modelling. This is **monthly plant-output EDA**, not electricity-demand forecasting, daily-output EDA, reservoir modelling or an emissions/credit calculation.

The complete daily 2013-November 2017 dataset is not yet locally extracted. Its five example rows are excluded. This EDA instead uses the existing **42-month transcription, January 2018-June 2021, for Units 1 and 2 at Wayang Windu**: 84 unit-month values at one field, not 84 independent dates or two independent plants.

## 2. Source and checks

Source: UNFCCC CDM project 3193, revised-v04 monitoring report completed 28 April 2022, Annex 5, printed pages 90-94 of 99. Tables are labelled Main Meter. Preserve this definition rather than calling the values raw SCADA, gross generation, or the exact electricity used to calculate CERs without further reconciliation.

- All 84 transcription values were re-compared with online PDF table text on 30 October 2026, and all five source table page images inspected. No numerical mismatch was found. This was a same-analyst second pass, not independent-person QA or daily reconciliation.
- No duplicate months, gaps within the 42-month interval, missing numeric generation, negative generation or zero-generation months.
- No zero monthly totals does not establish that there were no shutdown days: monthly aggregation can hide them.
- December 2017 is excluded because monitoring starts December 2. July-December 2021 is outside coverage, not missing zero-output months.
- Retain the published values and flag August/September 2018, which have a stated 0.2% meter-error adjustment. Do not apply that adjustment twice.
- Local PDF and supporting XLSX download attempts returned HTML challenge pages. No complete downloaded daily file or local source PDF is claimed.

Official source: {SOURCE_URL}

Registry and supporting documents: {REGISTRY_URL}

## 3. What the variables mean

Monthly MWh measures electricity over the month. It is affected by both output and the number of days. Monthly average MW = monthly MWh / (days in month x 24). This makes different-length months more comparable, but is not instantaneous power or a capacity factor. MWh/day is a monthly daily average, **not actual daily readings**. No capacity factor is calculated because matching historical capacity and meter boundaries have not been established.

## 4. Main findings

- Over the covered period, time-weighted average output is **{first['time_weighted_average_mw']:.2f} MW for Unit 1** and **{second['time_weighted_average_mw']:.2f} MW for Unit 2**. Time weighting divides total MWh by total calendar hours, rather than giving February and January equal weight.
- Unit 1's lowest monthly average is **{first['min_monthly_average_mw']:.2f} MW in {first['min_month']}**; Unit 2's lowest is **{second['min_monthly_average_mw']:.2f} MW in {second['min_month']}**. The Unit 1 dip is an observation, not a diagnosed cause. Keep the low-output values in the analysis.
- A descriptive threshold below 90% of each unit's full-sample median flags **{len(low)} unit-month observation(s)**. The threshold is exploratory, not an engineering operating limit, outage classification, prediction rule or reason to delete data.
- Combined reported generation changes **{change_2019:+.2f}% in 2019** relative to 2018 and **{change_2020:+.2f}% in 2020** relative to 2019. Only 2018-2020 are complete years. Compare January-June across all four years for a like-for-like view of 2021; do not annualize it or compare its six-month sum to full-year totals.
- Lag-1 correlations of raw monthly MWh are **{first['lag1_raw_monthly_mwh_correlation']:.3f}** for Unit 1 and **{second['lag1_raw_monthly_mwh_correlation']:.3f}** for Unit 2. After month-length adjustment they are **{first['lag1_monthly_average_mw_correlation']:.3f}** and **{second['lag1_monthly_average_mw_correlation']:.3f}**. Their difference shows why the calendar matters. These are in-sample descriptive associations, not prediction accuracy, causal effects or evidence that ML will beat persistence.
- With only 3-4 observations for each calendar month and a short, interrupted operating history, do not claim a robust seasonal cycle from the heatmap or annual lag correlations.

## 5. Implications for ML and validation

This dataset supports a preliminary historical monthly-output case study, but cannot support daily forecasts. With three lags, there are only 39 target dates per unit before train/validation/test separation; a 12-month lag leaves only 30. Units share a field, so keep both units together when splitting dates. Do not randomly split unit-month rows.

The full 42-month period has now informed EDA and earlier source inspection. **None of it should be described as an untouched final holdout.** Any subsequent past-only rolling evaluation within this period must be labelled exploratory, with tuning confined to earlier windows. A confirmatory claim needs additional, genuinely held-back Indonesian observations. Avoid spending this tiny sample on many feature/model choices.

If a monthly pilot proceeds, compare previous-month average power and a trailing mean against a small regularized model. Predict monthly average power and multiply by the target month's known calendar hours for MWh; also compare against a raw-MWh persistence baseline on the same dates. Use MAE/RMSE in MWh/month or MW, clearly specifying the target. Daily-model baselines belong to a separately extracted daily dataset.

If New Zealand training is later added, aggregate compatible electricity measurements to the same monthly target, establish comparable meter/plant definitions, and use foreign history available before each Indonesian forecast origin. Compare domestic-only and foreign-assisted models on identical Indonesian dates. Historical experiment results would not establish 2026 operational accuracy or generalization to other Indonesian fields.

## 6. Report-ready conclusion

The exploratory analysis found a continuous monthly generation series for two units at Wayang Windu from January 2018 to June 2021, with no missing or negative generation values in the transcribed interval. Adjusting energy totals for month length revealed a pronounced Unit 1 reduction in June 2019 and reduced calendar-related distortion in lag relationships. The records provide a useful preliminary Indonesian plant-output case study, but represent only 42 dates at one field. The analysis does not establish a reliable seasonal pattern, forecast accuracy, transfer-learning benefit, avoided emissions or carbon-credit issuance. A daily forecasting study still requires full extraction and validation of the daily source tables.
"""
    (OUTPUT_DIR / "eda_findings.md").write_text(findings)
    titles = {
        "monthly_generation_and_average_power.png": "1. Monthly energy and month-length-adjusted output",
        "generation_distribution.png": "2. Output distribution",
        "annual_and_comparable_half_year_generation.png": "3. Complete-year and comparable half-year totals",
        "calendar_heatmap_average_power.png": "4. Calendar coverage and output",
        "lag_relationships.png": "5. Descriptive lag relationships (not forecast accuracy)"
    }
    figures = []
    for filename, title in titles.items():
        encoded = base64.b64encode((OUTPUT_DIR / filename).read_bytes()).decode()
        figures.append(f'<section><h2>{title}</h2><img src="data:image/png;base64,{encoded}" alt="{html.escape(title)}"></section>')
    tables = [("Summary statistics", summary), ("Yearly totals and coverage", annual), ("Data dictionary", data_dictionary()), ("All 84 monthly unit records", tidy.drop(columns="date")), ("Data-quality and provenance", pd.DataFrame([{"check": key, "result": str(value)} for key, value in quality.items()]))]
    rendered_tables = "".join(f'<section><h2>{title}</h2><div class="table-scroll">{table.to_html(index=False, float_format=lambda value: f"{value:,.3f}", escape=True)}</div></section>' for title, table in tables)
    report = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wayang Windu monthly EDA</title><style>body{max-width:1150px;margin:32px auto;padding:0 20px;font:16px/1.6 system-ui;color:#172b3a;background:#fafbfc}h1,h2{line-height:1.25}section{margin:36px 0}img{max-width:100%;height:auto}.notice{padding:16px;background:#fff1cc;border-left:4px solid #aa6c00}.table-scroll{overflow:auto}table{border-collapse:collapse;font-size:13px;width:100%}td,th{padding:8px;border-bottom:1px solid #ccd4db;text-align:left;vertical-align:top}th{background:#e9eff3}a{color:#165b92}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style></head><body>'
    report += '<h1>Wayang Windu: monthly generation EDA</h1><p>January 2018-June 2021 | 42 dates | 2 units | 1 field</p><p class="notice"><strong>Monthly, not daily.</strong> No model has been evaluated. All dates are exploratory; there is no untouched holdout. Monthly daily averages must not be treated as observed daily output.</p>'
    report += f'<p><a href="{SOURCE_URL}">Official revised-v04 source report</a> | <a href="eda_findings.md">Report-ready findings</a> | <a href="wayang_windu_monthly_tidy.csv">Tidy data</a></p>'
    report += "".join(figures) + '<section><h2>Findings and interpretation</h2><pre>' + html.escape(findings) + '</pre></section>' + rendered_tables + '</body></html>'
    (OUTPUT_DIR / "wayang_windu_data.html").write_text(report)


def write_inline_chart(frame):
    lines = []
    for unit, label in UNITS.items():
        coordinates = []
        for position, value in enumerate(frame[f"{unit}_average_mw"]):
            horizontal = 56 + position * 604 / 41
            vertical = 240 - (value - 70) * 190 / 45
            coordinates.append(f"{horizontal:.1f},{vertical:.1f}")
        color = "var(--chart-1)" if unit == "unit_1" else "var(--chart-2)"
        dashed = '' if unit == "unit_1" else ' stroke-dasharray="6 3"'
        lines.append(f'<polyline points="{" ".join(coordinates)}" fill="none" stroke="{color}" stroke-width="2.5"{dashed}><title>{label}: 42 monthly average power observations</title></polyline>')
    ticks = []
    for value in [70, 80, 90, 100, 110]:
        vertical = 240 - (value - 70) * 190 / 45
        ticks.append(f'<line x1="56" x2="660" y1="{vertical:.1f}" y2="{vertical:.1f}" stroke="var(--border)"/><text x="46" y="{vertical + 4:.1f}" text-anchor="end">{value}</text>')
    for position in [0, 12, 24, 41]:
        horizontal = 56 + position * 604 / 41
        anchor = "end" if position == 41 else "middle"
        ticks.append(f'<text x="{horizontal:.1f}" y="265" text-anchor="{anchor}">{frame.iloc[position]["date"].strftime("%b %Y")}</text>')
    document = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;color:var(--foreground);font-family:var(--font-sans)}.scroll{overflow-x:auto}svg{display:block;width:100%;min-width:680px;height:290px}svg text{fill:var(--foreground);font:12px var(--font-sans)}.legend{display:flex;gap:24px;flex-wrap:wrap}.swatch{display:inline-block;width:25px;border-top:3px solid var(--chart-1);vertical-align:middle;margin-right:6px}.second{border-color:var(--chart-2);border-top-style:dashed}p{margin:8px 0;color:var(--muted-foreground)}</style></head><body><div class="legend"><span><span class="swatch"></span>Unit 1</span><span><span class="swatch second"></span>Unit 2</span></div><div class="scroll"><svg viewBox="0 0 680 290" role="img" aria-label="Wayang Windu monthly average power from January 2018 to June 2021. Unit 1 has a pronounced June 2019 dip to 75.77 MW. Unit 2 is relatively stable."><text x="56" y="24">Monthly average output (MW)</text>'''
    document += "".join(ticks + lines)
    document += '<circle cx="306.4" cy="215.6" r="4" fill="var(--chart-1)"/><text x="328" y="206">Jun 2019: Unit 1, 75.77 MW</text><text x="660" y="287" text-anchor="end">Month</text></svg></div><p>Monthly MWh divided by calendar hours; not measured daily output or a capacity factor. Source: UNFCCC project 3193, revised-v04 Annex 5.</p></body></html>'
    (OUTPUT_DIR / "eda_summary_inline.html").write_text(document)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    frame, tidy = prepare_data()
    summary, annual, half_year, lags, quality = summarize(frame, tidy)
    outputs = {"wayang_windu_monthly_wide.csv": frame, "wayang_windu_monthly_tidy.csv": tidy, "summary_statistics.csv": summary, "annual_generation_and_coverage.csv": annual, "comparable_january_june_generation.csv": half_year, "lag_correlations.csv": lags, "low_output_months.csv": tidy[tidy["below_90pct_sample_unit_median"]], "data_dictionary.csv": data_dictionary()}
    for filename, table in outputs.items():
        table.to_csv(OUTPUT_DIR / filename, index=False, float_format="%.8f")
    (OUTPUT_DIR / "data_quality_audit.json").write_text(json.dumps(quality, indent=2) + "\n")
    charts(frame, tidy)
    write_report(frame, tidy, summary, annual, lags, quality)
    write_inline_chart(frame)
    assert len(frame) == 42 and len(tidy) == 84
    assert np.allclose(tidy["monthly_average_mw"] * tidy["hours_in_month"], tidy["reported_generation_mwh"])
    assert frame.loc[frame["month"].eq("2020-02"), "days_in_month"].iloc[0] == 29
    assert annual[annual["complete_calendar_year"]]["months_present"].eq(12).all()
    print(json.dumps({"status": "complete", "months": len(frame), "unit_month_values": len(tidy), "charts": 5, "models_evaluated": 0, "output_directory": str(OUTPUT_DIR)}, indent=2))


if __name__ == "__main__":
    main()
