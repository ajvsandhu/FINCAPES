import sys
import webbrowser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


SOURCE = "Kepmen ESDM No. 163.K/HK.02/MEM.S/2021 (signed 30 August 2021), 2019 data"
SOURCE_PDF = (
    "https://gatrik.esdm.go.id/assets/uploads/download_index/files/"
    "96d7c-nilai-fe-grk-sistem-ketenagalistrikan-tahun-2019.pdf"
)
DATA_YEAR = 2019
COAL_ASSUMPTION_G_PER_KWH = 917
HEADLINE_GRID = "Jamali"
HEADLINE_COLUMN = "cm_expost_50_50"
NEAR_ZERO = 0.1
ROUNDING_TOLERANCE = 0.015
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "data" / "esdm_grid_emission_factors_2019.csv"
EMBER_INTENSITY_FILE = SCRIPT_DIR.parent / "ember_indonesia_eda" / "output" / "ember_indonesia_carbon_intensity_yearly.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"

FACTOR_COLUMNS = [
    "om_tco2_per_mwh",
    "bm_tco2_per_mwh",
    "cm_expost_50_50",
    "cm_expost_75_25",
    "cm_exante_50_50",
    "cm_exante_75_25",
]
COMBINED_MARGINS = {
    "cm_expost_50_50": 0.5,
    "cm_expost_75_25": 0.75,
}
UN_METHOD = "The UN's standard method for grid emission factors"
SENSITIVITY_GRIDS = ["Jamali", "Sumatera"]
WEIGHTINGS = [
    ("operating margin only", 1.0, "Lower bound (calculated)"),
    ("75/25", 0.75, "Solar and wind (published)"),
    ("50/50", 0.5, f"{UN_METHOD}: geothermal, first crediting period (published)"),
    ("25/75", 0.25, "Geothermal, second and third crediting periods (calculated)"),
    ("build margin only", 0.0, "Upper bound (calculated)"),
]
DATA_DICTIONARY = pd.DataFrame(
    [
        ("no", "number", "", "Row number in the decree's table"),
        ("grid", "text", "", "Name of the power system (an interconnected grid or an isolated island system)"),
        ("province", "text", "", "Province(s) the grid serves, separated by ';'"),
        ("num_plants", "number", "", "Number of power plants on the grid"),
        ("om_tco2_per_mwh", "number", "tCO2/MWh", "Operating margin: emissions per MWh of the plants that would run less if clean power were added"),
        ("bm_tco2_per_mwh", "number", "tCO2/MWh", "Build margin: emissions per MWh of the most recently built plants"),
        ("cm_expost_50_50", "number", "tCO2/MWh", "Combined margin from actual 2019 data, 0.5 x OM + 0.5 x BM; general default"),
        ("cm_expost_75_25", "number", "tCO2/MWh", "Combined margin from actual 2019 data, 0.75 x OM + 0.25 x BM; used for solar and wind"),
        ("cm_exante_50_50", "number", "tCO2/MWh", "Combined margin projected for 2022-2030, 50/50 weighting"),
        ("cm_exante_75_25", "number", "tCO2/MWh", "Combined margin projected for 2022-2030, 75/25 weighting"),
        ("source_note", "text", "", "Corrections made when transcribing the table, if any"),
    ],
    columns=["field", "type", "unit", "meaning"],
)
FILTER_NOTES = pd.DataFrame(
    [
        ("Transcription", "Values come from the decree's table as reprinted in the Ministry of Forestry carbon footprint manual (March 2025); the ESDM PDF does not download from a script. Spot-check against the PDF."),
        ("Transcription", "Two values printed with 'm' instead of a decimal point (Saumlaki, Sulutgo) were read as decimals; see source_note."),
        ("Missing values", "N/A in the decree means ESDM did not calculate that factor, usually because the grid is too small or has no recent plants."),
        ("Headline factor", f"{HEADLINE_GRID} {HEADLINE_COLUMN}: Jamali (Java-Madura-Bali) supplies about 70% of Indonesia's electricity, and geothermal runs around the clock, so it takes the 50/50 weighting; 75/25 is for solar and wind."),
        ("Comparison with Ember", "Ember's intensity is a national average over all generation, in lifecycle CO2-equivalent. ESDM factors are per grid, margin-based, and in tCO2; they are not expected to match."),
    ],
    columns=["topic", "note"],
)


def print_section(title):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def load():
    if not DATA_FILE.exists():
        sys.exit(f"Missing {DATA_FILE}. It holds the grid table from {SOURCE}.")
    return pd.read_csv(DATA_FILE, dtype={"num_plants": "Int64"})


def coverage(data):
    has = data[FACTOR_COLUMNS].notna()
    full = has.all(axis=1)
    no_exante = has[FACTOR_COLUMNS[:4]].all(axis=1) & ~has[FACTOR_COLUMNS[4:]].any(axis=1)
    om_only = has["om_tco2_per_mwh"] & ~has[FACTOR_COLUMNS[1:]].any(axis=1)
    none = ~has.any(axis=1)
    return pd.Series(
        {
            "All six factors": int(full.sum()),
            "OM, BM and ex-post CM, no ex-ante": int(no_exante.sum()),
            "Operating margin only": int(om_only.sum()),
            "No values": int(none.sum()),
            "Other pattern": int(len(data) - full.sum() - no_exante.sum() - om_only.sum() - none.sum()),
        }
    )


def describe(data):
    print_section("Shape")
    print(f"Rows (grids): {data.shape[0]}, columns: {data.shape[1]}")
    print(f"Source: {SOURCE}")

    print_section("Missing values per column")
    print(data.isna().sum().to_string())

    print_section("Which factors each grid has")
    print(coverage(data).to_string())

    print_section("Units and value ranges (tCO2/MWh)")
    print(data[FACTOR_COLUMNS].describe().round(3).to_string())
    print(f"\nPlants per grid: median {data['num_plants'].median():.0f}, max {data['num_plants'].max()}, "
          f"total {data['num_plants'].sum()}")


def check(data):
    print_section("Duplicates")
    print(f"Duplicate grid names: {data['grid'].duplicated().sum()}")

    print_section("Combined margin = weighted operating and build margins")
    for column, om_weight in COMBINED_MARGINS.items():
        rows = data.dropna(subset=["om_tco2_per_mwh", "bm_tco2_per_mwh", column])
        expected = om_weight * rows["om_tco2_per_mwh"] + (1 - om_weight) * rows["bm_tco2_per_mwh"]
        off = rows[(rows[column] - expected).abs() > ROUNDING_TOLERANCE]
        print(f"{column}: {len(rows)} grids checked, {len(off)} differ by more than {ROUNDING_TOLERANCE}")
        if not off.empty:
            print(off[["grid", "om_tco2_per_mwh", "bm_tco2_per_mwh", column]].assign(expected=expected.round(3)).to_string(index=False))

    print_section("Data quality flags")
    near_zero = data[data["om_tco2_per_mwh"] < NEAR_ZERO]
    print(f"Grids with operating margin below {NEAR_ZERO} tCO2/MWh (almost no fossil generation, or an error): {len(near_zero)}")
    if not near_zero.empty:
        print(near_zero[["grid", "province", "num_plants", "om_tco2_per_mwh"]].to_string(index=False))
    high = data[data[FACTOR_COLUMNS].max(axis=1) > 1.5]
    print(f"\nGrids with any factor above 1.5 tCO2/MWh: {len(high)}")
    if not high.empty:
        print(high[["grid", "province", "num_plants"] + FACTOR_COLUMNS].to_string(index=False))
    noted = data[data["source_note"].notna()]
    print(f"\nRows corrected or flagged during transcription: {len(noted)}")
    if not noted.empty:
        print(noted[["grid", "source_note"]].to_string(index=False))

    print_section("Build margin above operating margin (recent plants dirtier than the margin)")
    both = data.dropna(subset=["om_tco2_per_mwh", "bm_tco2_per_mwh"])
    dirtier = both[both["bm_tco2_per_mwh"] > both["om_tco2_per_mwh"]].sort_values("num_plants", ascending=False)
    print(f"{len(dirtier)} of {len(both)} grids with both margins")
    print(dirtier[["grid", "num_plants", "om_tco2_per_mwh", "bm_tco2_per_mwh"]].head(15).to_string(index=False))


def summarise(data):
    print_section("Largest grids by number of plants")
    largest = data.sort_values("num_plants", ascending=False).head(15)
    print(largest[["grid", "province", "num_plants"] + FACTOR_COLUMNS].to_string(index=False))

    print_section("By province (operating margin, tCO2/MWh; grids serving several provinces count in each)")
    exploded = data.assign(province=data["province"].str.split("; ")).explode("province")
    by_province = (
        exploded.groupby("province")
        .agg(
            grids=("grid", "size"),
            plants_on_its_grids=("num_plants", "sum"),
            om_min=("om_tco2_per_mwh", "min"),
            om_median=("om_tco2_per_mwh", "median"),
            om_max=("om_tco2_per_mwh", "max"),
        )
        .sort_values("plants_on_its_grids", ascending=False)
    )
    print(by_province.round(2).to_string())
    return largest, by_province


def ember_intensity():
    if not EMBER_INTENSITY_FILE.exists():
        return None
    ember = pd.read_csv(EMBER_INTENSITY_FILE)
    year = ember[ember["date"].astype(str).str[:4] == str(DATA_YEAR)]
    return None if year.empty else float(year["emissions_intensity_gco2_per_kwh"].iloc[0])


def weighted_factor(grid, om_weight):
    for column, weight in COMBINED_MARGINS.items():
        if weight == om_weight and pd.notna(grid[column]):
            return grid[column]
    return om_weight * grid["om_tco2_per_mwh"] + (1 - om_weight) * grid["bm_tco2_per_mwh"]


def sensitivity(data):
    print_section("Ex-post factor at each operating/build margin weighting (tCO2/MWh)")
    grids = data.set_index("grid")
    table = pd.DataFrame(
        [
            {"weighting": label, **{name: round(weighted_factor(grids.loc[name], om_weight), 3) for name in SENSITIVITY_GRIDS}, "use": use}
            for label, om_weight, use in WEIGHTINGS
        ]
    )
    print(table.to_string(index=False))
    return table


def compare(data):
    print_section(f"Comparison for {DATA_YEAR} (gCO2/kWh)")
    headline = data.set_index("grid").loc[HEADLINE_GRID]
    rows = [
        (
            f"ESDM {HEADLINE_GRID} {label}" + (f" ({UN_METHOD})" if om_weight == 0.5 else ""),
            weighted_factor(headline, om_weight) * 1000,
            use,
        )
        for label, om_weight, use in WEIGHTINGS
    ]
    rows.append(("Coal assumption", COAL_ASSUMPTION_G_PER_KWH, "Coal plants only"))
    ember = ember_intensity()
    if ember is None:
        print(f"Ember intensity not found at {EMBER_INTENSITY_FILE}; run ember_indonesia_eda.py first to include it.")
    else:
        rows.insert(0, ("Ember national average", ember, "All generation, lifecycle CO2e"))
    comparison = pd.DataFrame(rows, columns=["measure", "g_per_kwh", "basis"]).round(1)
    print(comparison.to_string(index=False))
    return comparison


def plot_distribution(data):
    om = data["om_tco2_per_mwh"].dropna()
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.hist(om, bins=30, color="tab:brown", edgecolor="white")
    headline = data.set_index("grid").loc[HEADLINE_GRID, "om_tco2_per_mwh"]
    ax.axvline(headline, color="tab:red", linestyle="--", label=f"{HEADLINE_GRID}: {headline:.2f}")
    ax.axvline(om.median(), color="black", linestyle=":", label=f"Median of all grids: {om.median():.2f}")
    ax.set_xlabel("Operating margin (tCO2/MWh)")
    ax.set_ylabel("Number of grids")
    ax.set_title(f"Operating margin across {len(om)} Indonesian grids (ESDM, {DATA_YEAR} data)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "operating_margin_distribution.png", dpi=150)
    plt.close(fig)


def plot_combined_margin(largest):
    data = largest.dropna(subset=[HEADLINE_COLUMN]).sort_values(HEADLINE_COLUMN)
    colours = ["tab:red" if grid == HEADLINE_GRID else "tab:brown" for grid in data["grid"]]
    fig, ax = plt.subplots(figsize=(11, 0.45 * len(data) + 1.5))
    bars = ax.barh(data["grid"], data[HEADLINE_COLUMN], color=colours)
    ax.bar_label(bars, labels=[f"{v:.2f}" for v in data[HEADLINE_COLUMN]], padding=3, fontsize=8)
    ax.set_xlabel("Combined margin, ex-post, 50% OM / 50% BM (tCO2/MWh)")
    ax.set_ylabel("Grid")
    ax.set_xlim(0, data[HEADLINE_COLUMN].max() * 1.15)
    ax.set_title(f"Grid emission factor of the {len(data)} largest grids by number of plants (ESDM, {DATA_YEAR} data)")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "combined_margin_largest_grids.png", dpi=150)
    plt.close(fig)


def plot_om_vs_bm(data):
    both = data.dropna(subset=["om_tco2_per_mwh", "bm_tco2_per_mwh"])
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.scatter(both["om_tco2_per_mwh"], both["bm_tco2_per_mwh"], s=10 + both["num_plants"].astype(float),
               alpha=0.6, color="tab:brown", edgecolor="black", linewidth=0.5)
    limit = max(both["om_tco2_per_mwh"].max(), both["bm_tco2_per_mwh"].max()) * 1.1
    ax.plot([0, limit], [0, limit], color="gray", linestyle="--", label="Build margin = operating margin")
    labelled = both[(both["num_plants"] >= 70) | (both[["om_tco2_per_mwh", "bm_tco2_per_mwh"]].max(axis=1) > 1.5)]
    for _, grid in labelled.iterrows():
        ax.annotate(grid["grid"], (grid["om_tco2_per_mwh"], grid["bm_tco2_per_mwh"]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_xlabel("Operating margin (tCO2/MWh)")
    ax.set_ylabel("Build margin (tCO2/MWh)")
    ax.set_title(f"Operating vs build margin, {len(both)} grids (ESDM, {DATA_YEAR} data)\n"
                 "size = number of plants; above the line = new plants dirtier than the margin",
                 fontsize=11)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "operating_vs_build_margin.png", dpi=150)
    plt.close(fig)


def plot_comparison(comparison):
    fig, ax = plt.subplots(figsize=(12, 7))
    colours = ["tab:red" if UN_METHOD in measure else "tab:brown" for measure in comparison["measure"]]
    labels = comparison["measure"].str.replace(f" ({UN_METHOD})", f"\n({UN_METHOD})", regex=False)
    bars = ax.barh(labels, comparison["g_per_kwh"], color=colours)
    ax.bar_label(bars, labels=[f"{v:.0f}" for v in comparison["g_per_kwh"]], padding=3, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("gCO2 per kWh")
    ax.set_xlim(0, comparison["g_per_kwh"].max() * 1.15)
    ax.set_title(f"Emissions per kWh, {DATA_YEAR}: Ember vs ESDM {HEADLINE_GRID} at each weighting vs coal\n"
                 "(weighting = operating margin / build margin)")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "intensity_comparison.png", dpi=150)
    plt.close(fig)


def html_table(data, index=False):
    return f'<div class="scroll">{data.to_html(index=index, na_rep="")}</div>'


def show_data(data, largest, by_province, weightings, comparison):
    sections = [
        f"<p>Source: {SOURCE}. <a href=\"{SOURCE_PDF}\">ESDM PDF</a> (opens in a browser only).</p>",
        f"<h2>Which factors each grid has</h2>{html_table(coverage(data).rename('grids').to_frame(), index=True)}",
        f"<h2>Ex-post factor at each weighting (tCO2/MWh)</h2>{html_table(weightings)}",
        f"<h2>Comparison for {DATA_YEAR} (gCO2/kWh)</h2>{html_table(comparison)}",
        f"<h2>Largest grids by number of plants</h2>{html_table(largest)}",
        f"<h2>By province</h2>{html_table(by_province.round(2), index=True)}",
        f"<h2>All grids ({data.shape[0]} rows x {data.shape[1]} columns)</h2>{html_table(data)}",
        f"<h2>Data dictionary</h2>{html_table(DATA_DICTIONARY)}",
        f"<h2>Filtering and transcription notes</h2>{html_table(FILTER_NOTES)}",
    ]
    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ESDM grid emission factors</title>
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
<h1>Grid emission factors (Indonesia, Ministry of Energy and Mineral Resources, ESDM)</h1>
{"".join(sections)}
</body>
</html>"""
    html_file = OUTPUT_DIR / "esdm_grid_factors_data.html"
    html_file.write_text(page)
    webbrowser.open(html_file.as_uri())
    print(f"Opened in your browser: {html_file}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load()
    DATA_DICTIONARY.to_csv(OUTPUT_DIR / "data_dictionary.csv", index=False)
    FILTER_NOTES.to_csv(OUTPUT_DIR / "filter_notes.csv", index=False)

    describe(data)
    check(data)
    largest, by_province = summarise(data)
    weightings = sensitivity(data)
    comparison = compare(data)
    largest.to_csv(OUTPUT_DIR / "esdm_largest_grids.csv", index=False)
    by_province.to_csv(OUTPUT_DIR / "esdm_factors_by_province.csv")
    weightings.to_csv(OUTPUT_DIR / "weighting_sensitivity.csv", index=False)
    comparison.to_csv(OUTPUT_DIR / "intensity_comparison.csv", index=False)
    show_data(data, largest, by_province, weightings, comparison)

    plot_distribution(data)
    plot_combined_margin(largest)
    plot_om_vs_bm(data)
    plot_comparison(comparison)
    print(f"\nPlots saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
