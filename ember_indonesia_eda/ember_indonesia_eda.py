import os
import sys
import webbrowser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests


BASE_URL = "https://api.ember-energy.org/v1"
ENTITY_CODE = "IDN"
DATASETS = [
    "electricity-generation/yearly",
    "power-sector-emissions/yearly",
    "carbon-intensity/yearly",
    "electricity-demand/yearly",
    "electricity-generation/monthly",
    "power-sector-emissions/monthly",
    "carbon-intensity/monthly",
    "electricity-demand/monthly",
    "installed-capacity/monthly",
]
ROW_KEYS = ["entity", "entity_code", "is_aggregate_entity", "date", "series", "is_aggregate_series"]
DATA_DICTIONARY = pd.DataFrame(
    [
        ("entity", "all", "text", "", "Country or region name, e.g. Indonesia, ASEAN, World"),
        ("entity_code", "all", "text", "", "3-letter ISO country code; blank for regions"),
        ("is_aggregate_entity", "all", "true/false", "", "True if the entity is a region made of several countries"),
        ("date", "all", "text", "", "Year (YYYY) for yearly datasets, first day of the month for monthly datasets"),
        ("series", "generation, emissions, capacity", "text", "", "Fuel or group of fuels the row describes (see series table)"),
        ("is_aggregate_series", "generation, emissions, capacity", "true/false", "", "True if the series is a total Ember sums from several fuels"),
        ("generation_twh", "electricity-generation", "number", "TWh", "Electricity generated in the period, terawatt-hours"),
        ("share_of_generation_pct", "electricity-generation", "number", "%", "Series generation as a percent of total generation; Demand can exceed 100"),
        ("emissions_mtco2", "power-sector-emissions", "number", "MtCO2e", "Lifecycle greenhouse gas emissions from generating the electricity, million tonnes CO2-equivalent; Ember multiplies generation by fuel emission factors that include mining, methane leaks and manufacturing, so solar, wind and hydro are small but not zero"),
        ("share_of_emissions_pct", "power-sector-emissions", "number", "%", "Series emissions as a percent of total power-sector emissions"),
        ("emissions_intensity_gco2_per_kwh", "carbon-intensity", "number", "gCO2e/kWh", "Lifecycle grams of CO2-equivalent emitted per kilowatt-hour generated (total emissions / total generation)"),
        ("demand_twh", "electricity-demand", "number", "TWh", "Electricity demand: generation plus net imports, terawatt-hours"),
        ("capacity_gw", "installed-capacity", "number", "GW", "Installed generating capacity, gigawatts"),
        ("capacity_w_per_capita", "installed-capacity", "number", "W/person", "Installed capacity per person, watts"),
    ],
    columns=["field", "datasets", "type", "unit", "meaning"],
)
SERIES_DICTIONARY = pd.DataFrame(
    [
        ("Coal", False, "Coal-fired generation"),
        ("Gas", False, "Natural gas generation"),
        ("Other fossil", False, "Oil and other fossil fuels"),
        ("Nuclear", False, "Nuclear generation (not present for Indonesia)"),
        ("Hydro", False, "Hydropower"),
        ("Bioenergy", False, "Biomass and biogas"),
        ("Solar", False, "Solar PV and solar thermal"),
        ("Wind", False, "Onshore and offshore wind"),
        ("Other renewables", False, "Mainly geothermal, plus tidal and wave"),
        ("Net imports", False, "Imports minus exports; not generated in the country"),
        ("Fossil", True, "Coal + Gas + Other fossil"),
        ("Renewables", True, "Hydro + Bioenergy + Solar + Wind + Other renewables"),
        ("Clean", True, "Renewables + Nuclear"),
        ("Wind and solar", True, "Wind + Solar"),
        ("Hydro, bioenergy and other renewables", True, "Hydro + Bioenergy + Other renewables"),
        ("Total generation", True, "Sum of all generation fuels, excluding Net imports"),
        ("Demand", True, "Total generation + Net imports"),
    ],
    columns=["series", "is_aggregate_series", "meaning"],
)
PLOT_LABELS = {"Other renewables": "Other renewables (geothermal, tidal, wave)"}
SCRIPT_DIR = Path(__file__).resolve().parent
ENV_FILE = SCRIPT_DIR / ".env"
OUTPUT_DIR = SCRIPT_DIR / "output"


def load_api_key():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "EMBER_API_KEY" and value.strip():
                return value.strip().strip("\"'")
    return os.environ.get("EMBER_API_KEY")


def api_get(api_key, dataset, params):
    try:
        response = requests.get(f"{BASE_URL}/{dataset}", params={**params, "api_key": api_key}, timeout=300)
    except requests.RequestException as error:
        raise RuntimeError(str(error).replace(api_key, "***")) from None
    if response.status_code != 200:
        message = response.text[:300].replace(api_key, "***")
        raise RuntimeError(f"Ember API returned {response.status_code}: {message}")
    return pd.DataFrame(response.json()["data"])


def fetch_dataset(api_key, dataset):
    params = {"entity_code": ENTITY_CODE}
    if dataset.endswith("/yearly"):
        params["start_date"] = "1900"
    return api_get(api_key, dataset, params)


def fetch_all(api_key):
    datasets = {}
    status = []
    for dataset in DATASETS:
        try:
            data = fetch_dataset(api_key, dataset)
        except RuntimeError as error:
            status.append({"dataset": dataset, "rows": None, "columns": None, "note": str(error)})
            continue
        note = "" if not data.empty else "No Indonesia data in this dataset"
        status.append({"dataset": dataset, "rows": len(data), "columns": data.shape[1], "note": note})
        if not data.empty:
            datasets[dataset] = data
            csv_file = OUTPUT_DIR / f"ember_indonesia_{dataset.replace('-', '_').replace('/', '_')}.csv"
            data.to_csv(csv_file, index=False)
    return datasets, pd.DataFrame(status).astype({"rows": "Int64", "columns": "Int64"})


def combine(datasets):
    combined = None
    for dataset in ["electricity-generation/yearly", "power-sector-emissions/yearly"]:
        if dataset in datasets:
            data = datasets[dataset]
            combined = data if combined is None else combined.merge(data, on=ROW_KEYS, how="outer")
    if combined is not None and "carbon-intensity/yearly" in datasets:
        intensity = datasets["carbon-intensity/yearly"]
        keys = [key for key in ROW_KEYS if key in intensity.columns]
        combined = combined.merge(intensity, on=keys, how="left")
    return combined


def print_section(title):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def html_table(data):
    return f'<div class="scroll">{data.to_html(index=False, na_rep="")}</div>'


def dictionary_sections():
    return [
        f"<h2>Data dictionary: fields</h2>{html_table(DATA_DICTIONARY)}",
        f"<h2>Data dictionary: series</h2>{html_table(SERIES_DICTIONARY)}",
    ]


def write_html_page(title, sections, file_name):
    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; margin: 20px; }}
  .scroll {{ max-height: 80vh; overflow: auto; border: 1px solid #ccc; margin-bottom: 30px; }}
  table {{ border-collapse: collapse; font-size: 13px; }}
  th, td {{ padding: 4px 10px; border-bottom: 1px solid #eee; text-align: right; white-space: nowrap; }}
  th {{ position: sticky; top: 0; background: #f4f4f4; }}
  tr:hover td {{ background: #fafae0; }}
</style>
</head>
<body>
<h1>{title}</h1>
{"".join(sections)}
</body>
</html>"""
    html_file = OUTPUT_DIR / file_name
    html_file.write_text(page)
    webbrowser.open(html_file.as_uri())
    print(f"Opened in your browser: {html_file}")


def show_data(datasets, status, combined, summaries):
    sections = [f"<h2>What the Ember API has for Indonesia</h2>{html_table(status)}"]
    sections += [f"<h2>{name}</h2>{html_table(summary)}" for name, summary in summaries.items()]
    if combined is not None:
        sections.append(
            "<h2>All yearly data combined: generation, emissions and carbon intensity "
            f"({combined.shape[0]} rows x {combined.shape[1]} columns)</h2>{html_table(combined)}"
        )
    for dataset, data in datasets.items():
        sections.append(
            f"<h2>Raw API data: {dataset} ({data.shape[0]} rows x {data.shape[1]} columns)</h2>{html_table(data)}"
        )
    sections += dictionary_sections()
    write_html_page("Ember data for Indonesia", sections, "ember_indonesia_data.html")


def describe_all(datasets, status, combined):
    print_section("Datasets available for Indonesia")
    print(status.to_string(index=False))
    tables = dict(datasets)
    if combined is not None:
        tables["combined yearly table"] = combined
    for name, data in tables.items():
        print_section(f"{name}: shape and missing values")
        print(f"Rows: {data.shape[0]}, columns: {data.shape[1]}")
        print(data.isna().sum().to_string())


def describe(data):
    print_section("Electricity generation: shape")
    print(f"Rows: {data.shape[0]}, columns: {data.shape[1]}")
    print(f"Columns: {list(data.columns)}")
    print(f"Years: {data['year'].min()}-{data['year'].max()} ({data['year'].nunique()} years)")
    print(f"Entities: {data['entity'].unique().tolist()}")

    print_section("Series (fuel) catalogue")
    catalogue = (
        data.groupby(["series", "is_aggregate_series"])
        .agg(rows=("year", "size"), first_year=("year", "min"), last_year=("year", "max"))
        .reset_index()
        .sort_values(["is_aggregate_series", "series"])
    )
    print(catalogue.to_string(index=False))

    print_section("Missing values per column")
    print(data.isna().sum().to_string())

    print_section("Missing fuel-year combinations")
    full_grid = pd.MultiIndex.from_product(
        [data["series"].unique(), range(data["year"].min(), data["year"].max() + 1)],
        names=["series", "year"],
    )
    present = pd.MultiIndex.from_frame(data[["series", "year"]])
    missing = full_grid.difference(present)
    if len(missing) == 0:
        print("None: every series has a row for every year.")
    else:
        print(missing.to_frame(index=False).groupby("series")["year"].apply(list).to_string())

    print_section("Duplicate series-year rows")
    print(int(data.duplicated(["series", "year"]).sum()))

    print_section("Units and value ranges")
    print("generation_twh: terawatt-hours of electricity generated in the year")
    print("share_of_generation_pct: percent of total generation in the year")
    print(data[["generation_twh", "share_of_generation_pct"]].describe().round(3).to_string())
    negatives = data[(data["generation_twh"] < 0) | (data["share_of_generation_pct"] < 0)]
    print(f"Rows with negative values: {len(negatives)}")


def generation_fuels(data):
    return data[~data["is_aggregate_series"].astype(bool) & (data["series"] != "Net imports")]


def check_units(data):
    print_section("Unit consistency checks")
    wide = data.pivot(index="year", columns="series", values="generation_twh")
    fuel_totals = generation_fuels(data).groupby("year")[["generation_twh", "share_of_generation_pct"]].sum()

    comparison = pd.DataFrame(
        {
            "sum_of_fuels_twh": fuel_totals["generation_twh"],
            "total_generation_twh": wide["Total generation"],
            "net_imports_twh": wide["Net imports"],
            "demand_twh": wide["Demand"],
        }
    )
    comparison["fuels_minus_total"] = comparison["sum_of_fuels_twh"] - comparison["total_generation_twh"]
    comparison["demand_minus_gen_minus_imports"] = (
        comparison["demand_twh"] - comparison["total_generation_twh"] - comparison["net_imports_twh"]
    )
    print("Sum of generation fuels vs Total generation, and Demand = Total generation + Net imports (TWh):")
    print(comparison.round(2).to_string())

    off = fuel_totals[(fuel_totals["share_of_generation_pct"] - 100).abs() > 0.5]
    print(f"\nYears where generation fuel shares do not sum to 100% (+/-0.5): {len(off)}")
    if not off.empty:
        print(off.round(3).to_string())

    over_100 = data[data["share_of_generation_pct"] > 100]
    print(f"Rows with share above 100%: {sorted(over_100['series'].unique())} (shares are relative to Total generation)")

    print_section("Years with zero generation")
    zeros = (wide == 0).sum()
    print(zeros[zeros > 0].to_string())

    print_section("Runs of identical values (possible carried-forward estimates)")
    for fuel in generation_fuels(data)["series"].unique():
        series = wide[fuel]
        run_ids = (series != series.shift()).cumsum()
        runs = series.groupby(run_ids).agg(["first", "size"])
        runs["start"] = series.index.to_series().groupby(run_ids.values).min().values
        long_runs = runs[(runs["size"] >= 5) & (runs["first"] > 0)]
        for _, run in long_runs.iterrows():
            print(f"{fuel}: {run['first']} TWh for {int(run['size'])} years from {int(run['start'])}")


def plot_fuels(data):
    fuels = generation_fuels(data)
    wide = fuels.pivot(index="year", columns="series", values="generation_twh").sort_index()
    wide = wide[wide.max().sort_values(ascending=False).index]
    wide.to_csv(OUTPUT_DIR / "ember_indonesia_generation_by_fuel_wide.csv")
    wide = wide.rename(columns=PLOT_LABELS)

    n = len(wide.columns)
    ncols = 3
    nrows = -(-n // ncols)
    first_year, last_year = wide.index.min(), wide.index.max()
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 4.2 * nrows))
    axes = axes.flatten()
    for ax, fuel in zip(axes, wide.columns):
        values = wide[fuel]
        ax.plot(wide.index, values, marker="o", markersize=3)
        name, _, detail = fuel.partition(" (")
        title = f"{name} generation\n({detail}" if detail else f"{name} generation"
        ax.set_title(title, fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel("Generation (TWh)")
        ax.set_xlim(first_year - 1, last_year + 2)
        ax.set_xticks(range(first_year, last_year + 1, 5))
        ax.set_ylim(0, values.max() * 1.2 if values.max() > 0 else 1)
        ax.tick_params(labelbottom=True, labelleft=True)
        for year in (first_year, last_year):
            ax.annotate(
                f"{values[year]:.2f}",
                (year, values[year]),
                textcoords="offset points",
                xytext=(0, 7),
                ha="center",
                fontsize=8,
            )
        ax.grid(alpha=0.3)
    for ax in axes[n:]:
        ax.set_visible(False)
    fig.suptitle("Indonesia electricity generation by fuel (Ember, yearly)", fontsize=14)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fuel_small_multiples.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.stackplot(wide.index, wide.fillna(0).T.values, labels=wide.columns)
    ax.set_xlabel("Year")
    ax.set_ylabel("Generation (TWh)")
    ax.set_xticks(range(first_year, last_year + 1, 5))
    ax.set_title("Indonesia electricity generation mix (Ember, yearly)")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fuel_stacked.png", dpi=150)
    plt.close(fig)


def with_year(data):
    return data.assign(year=pd.to_numeric(data["date"].str[:4]))


def series_summary(data, value, share):
    wide = data.pivot(index="year", columns="series", values=value)
    shares = data.pivot(index="year", columns="series", values=share)
    first, last = wide.index.min(), wide.index.max()
    order = list(generation_fuels(data)["series"].unique()) + ["Fossil", "Renewables", "Total generation"]
    rows = []
    for series in order:
        values = wide[series]
        growth = ((values[last] / values[first]) ** (1 / (last - first)) - 1) * 100 if values[first] > 0 else None
        rows.append(
            {
                "series": series,
                f"{first}": values[first],
                f"{last}": values[last],
                "avg_yearly_growth_pct": growth,
                f"share_{first}_pct": shares.loc[first, series],
                f"share_{last}_pct": shares.loc[last, series],
                "peak_year": values.idxmax(),
                "peak_value": values.max(),
            }
        )
    return pd.DataFrame(rows).round(2)


def summarise_generation(data):
    print_section("Generation summary by fuel (TWh)")
    summary = series_summary(data, "generation_twh", "share_of_generation_pct")
    print(summary.to_string(index=False))

    shares = data.pivot(index="year", columns="series", values="share_of_generation_pct")
    total = data.pivot(index="year", columns="series", values="generation_twh")["Total generation"]
    print(f"\nRenewables share: highest {shares['Renewables'].max():.2f}% in {shares['Renewables'].idxmax()}, "
          f"lowest {shares['Renewables'].min():.2f}% in {shares['Renewables'].idxmin()}")
    print(f"Coal share: highest {shares['Coal'].max():.2f}% in {shares['Coal'].idxmax()}")
    falls = total.diff()[lambda change: change < 0]
    print("Years total generation fell: " + ", ".join(f"{year} ({change:.2f} TWh)" for year, change in falls.items()))
    return summary


def analyse_emissions(emissions, generation, intensity):
    print_section("Emissions: consistency checks")
    wide = emissions.pivot(index="year", columns="series", values="emissions_mtco2")
    fuel_totals = generation_fuels(emissions).groupby("year")[["emissions_mtco2", "share_of_emissions_pct"]].sum()
    gap = (fuel_totals["emissions_mtco2"] - wide["Total generation"]).abs().max()
    print(f"Largest gap between sum of fuel emissions and Total generation emissions: {gap:.2f} MtCO2e")
    print(f"Fuel emission shares sum to between {fuel_totals['share_of_emissions_pct'].min():.2f}% "
          f"and {fuel_totals['share_of_emissions_pct'].max():.2f}%")

    print_section("Emissions summary by fuel (MtCO2e)")
    summary = series_summary(emissions, "emissions_mtco2", "share_of_emissions_pct")
    print(summary.to_string(index=False))

    print_section("Emission factor implied for each fuel (gCO2e per kWh = MtCO2e / TWh x 1000)")
    generation_wide = generation.pivot(index="year", columns="series", values="generation_twh")
    fuels = list(generation_fuels(emissions)["series"].unique())
    factors = (wide[fuels] / generation_wide[fuels] * 1000).round(0)
    print(factors.loc[[factors.index.min(), factors.index.max()]].T.to_string())

    print_section("Carbon intensity (gCO2e/kWh)")
    ci = intensity.set_index("year")["emissions_intensity_gco2_per_kwh"]
    print(f"{ci.index.min()}: {ci.iloc[0]:.2f}, {ci.index.max()}: {ci.iloc[-1]:.2f}, "
          f"lowest {ci.min():.2f} in {ci.idxmin()}, highest {ci.max():.2f} in {ci.idxmax()}")
    implied = wide["Total generation"] / generation_wide["Total generation"] * 1000
    print(f"Largest gap between reported intensity and total emissions / total generation: {(implied - ci).abs().max():.2f} gCO2e/kWh")
    return summary


def plot_emissions(emissions):
    fuels = generation_fuels(emissions)
    wide = fuels.pivot(index="year", columns="series", values="emissions_mtco2").sort_index()
    wide = wide[wide.max().sort_values(ascending=False).index].rename(columns=PLOT_LABELS)
    total = wide.sum(axis=1)
    first_year, last_year = wide.index.min(), wide.index.max()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.stackplot(wide.index, wide.T.values, labels=wide.columns)
    for year in (first_year, 2010, 2020, last_year):
        ax.annotate(f"{total[year]:.1f}", (year, total[year]), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Emissions (MtCO2e)")
    ax.set_xticks(range(first_year, last_year + 1, 5))
    ax.set_ylim(0, total.max() * 1.15)
    ax.set_title("Indonesia power-sector emissions by fuel (Ember, lifecycle CO2-equivalent, yearly)")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "emissions_stacked.png", dpi=150)
    plt.close(fig)


def plot_intensity(intensity):
    ci = intensity.set_index("year")["emissions_intensity_gco2_per_kwh"]
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.plot(ci.index, ci.values, marker="o", markersize=4, color="tab:brown")
    labelled = {ci.index.min(), ci.index.max(), ci.idxmin(), ci.idxmax()}
    for year in sorted(labelled):
        ax.annotate(f"{ci[year]:.1f}", (year, ci[year]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
    ax.set_xlabel("Year")
    ax.set_ylabel("Carbon intensity (gCO2e per kWh)")
    ax.set_xticks(range(ci.index.min(), ci.index.max() + 1, 5))
    ax.set_ylim(0, ci.max() * 1.15)
    ax.set_title("Indonesia electricity carbon intensity (Ember, lifecycle CO2-equivalent, yearly)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "carbon_intensity.png", dpi=150)
    plt.close(fig)


def main():
    api_key = load_api_key()
    if not api_key:
        sys.exit(
            f"Put EMBER_API_KEY=<your key> in {ENV_FILE} or set it as an environment variable "
            "(register at https://ember-energy.org/data/api/)."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)
    datasets, status = fetch_all(api_key)
    if "electricity-generation/yearly" not in datasets:
        sys.exit("Ember API returned no electricity generation data for Indonesia.")
    combined = combine(datasets)
    if combined is not None:
        combined.to_csv(OUTPUT_DIR / "ember_indonesia_all_yearly_combined.csv", index=False)
    DATA_DICTIONARY.to_csv(OUTPUT_DIR / "data_dictionary_fields.csv", index=False)
    SERIES_DICTIONARY.to_csv(OUTPUT_DIR / "data_dictionary_series.csv", index=False)
    print(f"Saved raw API data for each dataset to {OUTPUT_DIR}/")

    describe_all(datasets, status, combined)

    data = with_year(datasets["electricity-generation/yearly"])
    describe(data)
    check_units(data)
    summaries = {"Generation summary by fuel (TWh)": summarise_generation(data)}
    plot_fuels(data)

    if "power-sector-emissions/yearly" in datasets and "carbon-intensity/yearly" in datasets:
        emissions = with_year(datasets["power-sector-emissions/yearly"])
        intensity = with_year(datasets["carbon-intensity/yearly"])
        summaries["Emissions summary by fuel (MtCO2e)"] = analyse_emissions(emissions, data, intensity)
        plot_emissions(emissions)
        plot_intensity(intensity)

    for name, summary in summaries.items():
        summary.to_csv(OUTPUT_DIR / f"ember_indonesia_{name.split(' (')[0].lower().replace(' ', '_')}.csv", index=False)
    show_data(datasets, status, combined, summaries)
    print(f"\nPlots saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
