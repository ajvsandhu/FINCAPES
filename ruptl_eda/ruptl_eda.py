import re
import sys
import webbrowser
from pathlib import Path

import fitz
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


SOURCE = "RUPTL PT PLN 2025-2034 (Kepmen ESDM No. 188.K/TL.03/MEM.L/2025, 26 May 2025)"
SOURCE_URL = (
    "https://gatrik.esdm.go.id/gatrik/gatrik-api/storage/migrasi/download_index/files/"
    "b967d-ruptl-pln-2025-2034-pub-.pdf"
)
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
PDF_FILE = ROOT / "grid_data_sources" / "raw" / "ruptl_2025_2034.pdf"
EMBER_FILE = ROOT / "ember_indonesia_eda" / "output" / "ember_indonesia_generation_by_fuel_wide.csv"
ESDM_FILE = ROOT / "grid_data_sources" / "output" / "esdm_factors_2017_2019_study_grids.csv"
GENESIS_PLANNED_FILE = ROOT / "geothermal_grid_mapping" / "output" / "planned_additions_by_grid_year.csv"
GENESIS_SITES_FILE = ROOT / "geothermal_grid_mapping" / "output" / "site_grid_mapping.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"

# (page, table index) of each table, pages numbered as in a PDF viewer. Tables that run over a page
# break are listed as several pieces in order.
HISTORICAL_SALES = {"Sumatera": [(194, 0), (194, 1)], "Jamali": [(195, 0), (195, 1)]}
HISTORICAL_GENERATION = {
    "Sumatera + Kalimantan": [(222, 1), (222, 2), (223, 0), (223, 1)],
    "Jamali": [(223, 2), (224, 0), (224, 1), (224, 2)],
}
PROJECTED_SALES = {"Sumatera": (323, 1), "Jamali": (324, 0)}
PROJECTED_GENERATION = {
    ("Sumatera", "RE Base"): [(475, 1), (476, 0)],
    ("Sumatera", "ARED"): [(476, 1)],
    ("Jamali", "RE Base"): [(483, 1), (484, 0)],
    ("Jamali", "ARED"): [(484, 1), (485, 0)],
}
PROJECTED_EMISSIONS = {
    ("Sumatera", "RE Base"): (512, 0),
    ("Sumatera", "ARED"): (512, 1),
    ("Jamali", "RE Base"): (513, 0),
    ("Jamali", "ARED"): (513, 1),
}
CAPACITY_ADDITIONS = {
    ("Sumatera", "RE Base"): [(344, 0), (345, 0)],
    ("Sumatera", "ARED"): [(345, 1), (346, 0)],
    ("Jamali", "RE Base"): [(360, 0), (361, 0)],
    ("Jamali", "ARED"): [(361, 1), (362, 0)],
}
TABLE_NUMBERS = {
    "historical_sales": "Tabel 4.2 (Sumatera), 4.3 (Jamali)",
    "historical_generation": "Tabel 4.32 (Sumatera + Kalimantan), 4.33 (Jamali)",
    "projected_sales": "Tabel 5.68 (Sumatera), 5.69 (Jamali)",
    "projected_generation": "Tabel 5.135/5.136 (Sumatera), 5.143/5.144 (Jamali)",
    "projected_emissions": "Tabel 5.177/5.178 (Sumatera), 5.179/5.180 (Jamali)",
    "capacity_additions": "Tabel 5.84/5.85 (Sumatera), 5.88/5.89 (Jamali)",
}

PARTIAL_YEAR = 2024
GRIDS = ["Jamali", "Sumatera"]
SCENARIOS = ["RE Base", "ARED"]
TOLERANCE_GWH = 3
TOLERANCE_MT = 0.15

HISTORICAL_FUELS = {
    "Air": "Hydro", "Panas Bumi": "Geothermal", "BBN (Biofuel)": "Bioenergy", "Biomassa": "Bioenergy",
    "Surya": "Solar", "Bayu": "Wind", "EBT Lain": "Other renewables", "Gas": "Gas",
    "HSD": "Oil", "MFO": "Oil", "IDO": "Oil", "HFO": "Oil", "BIO HSD": "Oil",
    "Batubara": "Coal", "Impor": "Imports",
}
PROJECTED_FUELS = {
    "Air": "Hydro", "Panas Bumi": "Geothermal", "Biomassa": "Bioenergy", "Sampah": "Bioenergy",
    "Surya": "Solar", "Bayu": "Wind", "Nuklir": "Nuclear", "Lainnya": "Other renewables",
    "Gas": "Gas", "BBM": "Oil", "Batubara": "Coal", "Impor": "Imports",
}
FOSSIL = ["Coal", "Gas", "Oil"]
TECHNOLOGIES = {
    "PLTU": "Coal", "PLTU MT": "Coal (mine-mouth)", "PLTGU": "Gas", "PLTG": "Gas", "PLTMG": "Gas",
    "PLTD": "Diesel", "PLTP": "Geothermal", "PLTA": "Hydro", "PLTM": "Hydro", "PLTA PS": "Pumped storage",
    "PLTS": "Solar", "PLTS+BESS": "Solar", "PLTB": "Wind", "PLTSa": "Bioenergy", "PLTBg": "Bioenergy",
    "PLTBm": "Bioenergy", "BESS": "Battery", "PLTN": "Nuclear",
}
FUEL_COLOURS = {
    "Coal": "#4d4d4d", "Gas": "#e08214", "Oil": "#8c510a", "Hydro": "#2166ac", "Geothermal": "#d6604d",
    "Bioenergy": "#5aae61", "Solar": "#fdd835", "Wind": "#80cdc1", "Nuclear": "#762a83",
    "Other renewables": "#b2abd2", "Imports": "#bababa", "Coal (mine-mouth)": "#252525",
    "Diesel": "#8c510a", "Pumped storage": "#4393c3", "Battery": "#c51b7d",
}

DATA_DICTIONARY = pd.DataFrame(
    [
        ("all", "grid", "text", "", "Jamali (Java-Madura-Bali), Sumatera, or 'Sumatera + Kalimantan' where the RUPTL only reports the two together"),
        ("all", "year", "number", "year", "Calendar year"),
        ("historical_sales / projected_sales", "customer_group", "text", "", "Household, Business, Public, Industry, or Total"),
        ("historical_sales / projected_sales", "sales_gwh", "number", "GWh", "Electricity sold by PLN to customers"),
        ("historical_generation", "fuel_ruptl", "text", "", "Fuel row as labelled in the RUPTL (Indonesian)"),
        ("historical_generation / projected_generation", "fuel", "text", "", "Fuel group used in this analysis"),
        ("historical_generation / projected_generation", "generation_gwh", "number", "GWh", "Electricity produced (PLN-owned, rented and IPP plants; excludes captive power)"),
        ("historical_generation", "partial_year", "true/false", "", "True for 2024: unaudited data to October only"),
        ("projected_*", "scenario", "text", "", "RE Base (base case) or ARED (accelerated renewables)"),
        ("projected_emissions", "emissions_mtco2", "number", "MtCO2", "Projected CO2 from fuel combustion"),
        ("projected_intensity", "average_tco2_per_mwh", "number", "tCO2/MWh", "Total emissions / total generation"),
        ("projected_intensity", "fossil_tco2_per_mwh", "number", "tCO2/MWh", "Total emissions / coal + gas + oil generation; a descriptive fossil-only intensity, not an official operating margin"),
        ("capacity_additions", "owner", "text", "", "PLN, SH-PLN (PLN subsidiaries), IPP, Kerjasama (cooperation), or Total"),
        ("capacity_additions", "technology_ruptl / technology", "text", "", "Plant type code from the RUPTL (e.g. PLTP = geothermal) and its English group"),
        ("capacity_additions", "capacity_mw", "number", "MW", "Capacity added in the year"),
    ],
    columns=["table", "field", "type", "unit", "meaning"],
)
FILTER_NOTES = pd.DataFrame(
    [
        ("Extraction", "Tables were read from the RUPTL PDF with PyMuPDF. Stray spaces inside numbers (e.g. '3 7.601') were removed; '.' is the thousands separator and ',' the decimal point, except where a value has a single digit after '.' (e.g. '202.8' MtCO2), which is read as a decimal."),
        ("Regions", "RUPTL historical generation for Sumatera is only published together with Kalimantan (Sumkal). Kalimantan has no geothermal plants, so the geothermal row is Sumatera's. Other fuels cannot be split."),
        ("Regions", "RUPTL 'Sumatera' projections cover the whole Sumatera region, including island systems and Bangka (planned to join the grid); slightly wider than the ESDM decree's Sumatera grid."),
        ("Interconnection", "From the 2030s, Jamali's projected hydro and geothermal include energy imported from Sumatera over the Sumatera-Java interconnection (ISJ), per the table footnote. Jamali solar includes rooftop PV."),
        ("Partial year", f"{PARTIAL_YEAR} historical generation is unaudited and runs to October only; it is kept but flagged and excluded from trend charts. {PARTIAL_YEAR} sales are a forecast (prognosa)."),
        ("Fuel groups", "BIO HSD (diesel blended with biodiesel) is grouped with oil. 'EBT' and 'BBM' subtotal rows are not stored, to avoid double counting; they are rebuilt from their components and checked."),
        ("Coverage", "RUPTL covers PLN's system (own plants, rented plants and IPPs). Captive industrial plants are excluded, so totals are lower than Ember's national figures."),
    ],
    columns=["topic", "note"],
)


def print_section(title):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def number(cell, blank=np.nan):
    if cell is None:
        return blank
    text = str(cell).replace(" ", "").replace("*", "").replace("%", "").strip()
    if text == "":
        return blank
    if text in ("-", "–"):
        return 0.0
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", text):
        text = text.replace(".", "")
    try:
        return float(text)
    except ValueError:
        return np.nan


def clean_label(cell):
    label = re.sub(r"\s+", " ", str(cell or "").replace("*", "").replace(":", "")).strip()
    return label.rstrip(")").strip() if "(" not in label else label


def year_of(cell):
    match = re.match(r"^\s*(20\d\d)", str(cell or ""))
    return int(match.group(1)) if match else None


class Pdf:
    def __init__(self, path):
        self.document = fitz.open(path)
        self.cache = {}

    def table(self, page, index):
        if page not in self.cache:
            self.cache[page] = [t.extract() for t in self.document[page - 1].find_tables().tables]
        tables = self.cache[page]
        if index >= len(tables):
            sys.exit(f"Expected a table {index} on page {page}; the PDF layout may have changed.")
        return tables[index]


def year_columns(rows):
    for row_number, row in enumerate(rows[:3]):
        columns = {i: year_of(cell) for i, cell in enumerate(row) if year_of(cell)}
        if len(columns) >= 2 or (len(columns) == 1 and len(row) <= 6):
            return row_number, columns
    return None, {}


def historical_sales(pdf):
    groups = {"Rumah Tangga": "Household", "Industri": "Industry", "Bisnis": "Business", "Publik": "Public", "Jumlah": "Total"}
    rows = []
    for grid, pieces in HISTORICAL_SALES.items():
        for page, index in pieces:
            table = pdf.table(page, index)
            header, years = year_columns(table)
            for row in table[header + 1:]:
                label = clean_label(row[0])
                if label in groups:
                    for column, year in years.items():
                        rows.append({"grid": grid, "year": year, "customer_group": groups[label], "sales_gwh": number(row[column])})
    return pd.DataFrame(rows)


def historical_generation(pdf):
    rows = []
    for grid, pieces in HISTORICAL_GENERATION.items():
        for page, index in pieces:
            table = pdf.table(page, index)
            header, years = year_columns(table)
            for row in table[header + 1:]:
                labels = [clean_label(x) for x in str(row[0] or "").split("\n")]
                for column, year in years.items():
                    subtotal_column = column + 3
                    if subtotal_column >= len(row):
                        continue
                    values = str(row[subtotal_column] or "").split("\n")
                    if len(values) != len(labels):
                        continue
                    for label, value in zip(labels, values):
                        if label in HISTORICAL_FUELS or label == "Subtotal":
                            rows.append({"grid": grid, "year": year, "fuel_ruptl": label, "generation_gwh": number(value)})
    data = pd.DataFrame(rows).drop_duplicates(["grid", "year", "fuel_ruptl"])
    totals = data[data["fuel_ruptl"] == "Subtotal"].set_index(["grid", "year"])["generation_gwh"]
    data = data[data["fuel_ruptl"] != "Subtotal"].copy()
    data["fuel"] = data["fuel_ruptl"].map(HISTORICAL_FUELS)
    data["partial_year"] = data["year"] == PARTIAL_YEAR
    return data.sort_values(["grid", "year", "fuel"]).reset_index(drop=True), totals


def projected_sales(pdf):
    groups = ["Household", "Business", "Public", "Industry", "Total"]
    labels = {"Rumah Tangga": "Household", "Bisnis": "Business", "Publik": "Public", "Industri": "Industry", "Total": "Total"}
    rows = []
    for grid, (page, index) in PROJECTED_SALES.items():
        table = pdf.table(page, index)
        if len(table) == 1:
            # The whole table is one merged row: each cell holds the year then the values in order.
            for cell in table[0][1:]:
                parts = str(cell or "").split("\n")
                year = year_of(parts[0])
                for group, value in zip(groups, parts[1:6]):
                    rows.append({"grid": grid, "year": year, "customer_group": group, "sales_gwh": number(value)})
            continue
        header, years = year_columns(table)
        for row in table[header + 1:]:
            label = clean_label(row[0])
            if label in labels:
                for column, year in years.items():
                    rows.append({"grid": grid, "year": year, "customer_group": labels[label], "sales_gwh": number(row[column])})
    return pd.DataFrame(rows)


def projected_generation(pdf):
    rows, totals = [], {}
    for (grid, scenario), pieces in PROJECTED_GENERATION.items():
        group = None
        for page, index in pieces:
            table = pdf.table(page, index)
            header, years = year_columns(table)
            for row in table[header + 1:]:
                number_cell = clean_label(row[0])
                label = clean_label(row[1]) or number_cell
                if number_cell.isdigit():
                    group = number_cell
                if label == "Total":
                    for column, year in years.items():
                        totals[(grid, scenario, year)] = number(row[column])
                    continue
                keep = (group == "1" and not number_cell.isdigit()) or (group != "1" and number_cell.isdigit())
                if keep and label in PROJECTED_FUELS:
                    for column, year in years.items():
                        rows.append({"grid": grid, "scenario": scenario, "year": year, "fuel_ruptl": label,
                                     "fuel": PROJECTED_FUELS[label], "generation_gwh": number(row[column])})
    totals = pd.Series(totals, name="total_gwh")
    totals.index.names = ["grid", "scenario", "year"]
    return pd.DataFrame(rows), totals


def projected_emissions(pdf):
    labels = {"Gas": "Gas", "BBM": "Oil", "Batubara": "Coal", "Total": "Total", "Jumlah": "Total"}
    rows = []
    for (grid, scenario), (page, index) in PROJECTED_EMISSIONS.items():
        table = pdf.table(page, index)
        header, years = year_columns(table)
        for row in table[header + 1:]:
            label = clean_label(row[1]) or clean_label(row[0])
            if label in labels:
                for column, year in years.items():
                    rows.append({"grid": grid, "scenario": scenario, "year": year, "fuel": labels[label],
                                 "emissions_mtco2": number(row[column])})
    return pd.DataFrame(rows)


def capacity_additions(pdf):
    owners = {"PLN": "PLN", "SH-PLN": "SH-PLN", "IPP": "IPP", "Total": "Total"}
    rows, missing = [], []
    for (grid, scenario), pieces in CAPACITY_ADDITIONS.items():
        owner = None
        for page, index in pieces:
            table = pdf.table(page, index)
            header, years = year_columns(table)
            for row in table[header + 1:]:
                label = clean_label(row[0])
                values = {year: number(row[column]) for column, year in years.items()}
                empty = all(np.isnan(v) for v in values.values())
                if label.startswith("Kerjasama"):
                    owner = "Kerjasama"
                elif label in owners and empty:
                    owner = owners[label]
                elif label in TECHNOLOGIES and owner:
                    if empty:
                        missing.append(f"{grid} {scenario} {owner} {label}")
                    for year, value in values.items():
                        rows.append({"grid": grid, "scenario": scenario, "owner": owner, "technology_ruptl": label,
                                     "technology": TECHNOLOGIES[label], "year": year, "capacity_mw": value})
    return pd.DataFrame(rows), missing


def check(hist_gen, hist_totals, proj_gen, proj_totals, emissions, capacity, missing, hist_sales, proj_sales):
    print_section("Check: historical fuel rows add up to the RUPTL subtotal (GWh)")
    sums = hist_gen.groupby(["grid", "year"])["generation_gwh"].sum()
    compare = pd.DataFrame({"sum_of_fuels": sums, "ruptl_subtotal": hist_totals}).dropna()
    compare["difference"] = (compare["sum_of_fuels"] - compare["ruptl_subtotal"]).round(1)
    print(compare.to_string())
    bad_hist = compare[compare["difference"].abs() > TOLERANCE_GWH]
    print(f"Years outside ±{TOLERANCE_GWH} GWh: {len(bad_hist)}")

    print_section("Check: projected fuel rows add up to the RUPTL total (GWh)")
    sums = proj_gen.groupby(["grid", "scenario", "year"])["generation_gwh"].sum()
    compare = pd.DataFrame({"sum_of_fuels": sums, "ruptl_total": proj_totals}).dropna()
    compare["difference"] = (compare["sum_of_fuels"] - compare["ruptl_total"]).round(1)
    bad_proj = compare[compare["difference"].abs() > TOLERANCE_GWH]
    print(f"{len(compare)} grid-scenario-years checked, {len(bad_proj)} outside ±{TOLERANCE_GWH} GWh")
    if not bad_proj.empty:
        print(bad_proj.to_string())

    print_section("Check: projected emissions by fuel add up to the total (MtCO2)")
    wide = emissions.pivot_table(index=["grid", "scenario", "year"], columns="fuel", values="emissions_mtco2")
    wide["difference"] = (wide[FOSSIL].sum(axis=1) - wide["Total"]).round(2)
    bad_emis = wide[wide["difference"].abs() > TOLERANCE_MT]
    print(f"{len(wide)} grid-scenario-years checked, {len(bad_emis)} outside ±{TOLERANCE_MT} Mt")
    if not bad_emis.empty:
        print(bad_emis.to_string())

    print_section("Check: sales by customer group add up to the total (GWh)")
    for name, sales in (("historical", hist_sales), ("projected", proj_sales)):
        wide = sales.pivot_table(index=["grid", "year"], columns="customer_group", values="sales_gwh")
        diff = (wide[["Household", "Business", "Public", "Industry"]].sum(axis=1) - wide["Total"]).abs()
        print(f"{name}: {len(wide)} grid-years checked, {(diff > TOLERANCE_GWH).sum()} outside ±{TOLERANCE_GWH} GWh")
    repeated = hist_sales[hist_sales["year"].isin([2023, 2024])].pivot_table(
        index=["grid", "customer_group"], columns="year", values="sales_gwh")
    repeated = repeated[repeated[2023] == repeated[2024]]
    if not repeated.empty:
        print("\nHistorical sales where 2024 repeats 2023 exactly (source-table anomaly; cause unconfirmed):")
        print(repeated.to_string())

    print_section("Comparison: RE Base and ARED in 2025 (differences are not automatically errors) (generation, GWh)")
    first = proj_gen[proj_gen["year"] == 2025].pivot_table(index=["grid", "fuel"], columns="scenario",
                                                           values="generation_gwh", aggfunc="sum")
    first["difference"] = first["ARED"] - first["RE Base"]
    print(first[first["difference"].abs() > 0].to_string() if (first["difference"].abs() > 0).any()
          else "Identical in 2025")

    print_section("Check: capacity additions by owner add up to the Total block (MW)")
    if missing:
        print("Rows blank in the source PDF (preserved as missing):")
        for item in missing:
            print(f"  {item}")
    parts = capacity[~capacity["owner"].isin(["Total", "Kerjasama"])].groupby(["grid", "scenario", "technology_ruptl"])["capacity_mw"].sum()
    total = capacity[capacity["owner"] == "Total"].groupby(["grid", "scenario", "technology_ruptl"])["capacity_mw"].sum()
    compare = pd.DataFrame({"sum_of_owners": parts, "total_block": total}).fillna(0)
    incomplete = capacity[capacity["capacity_mw"].isna()].set_index(["grid", "scenario", "technology_ruptl"]).index.unique()
    compare["ownership_incomplete"] = compare.index.isin(incomplete)
    compare.loc[compare["ownership_incomplete"], "sum_of_owners"] = np.nan
    compare["difference"] = compare["sum_of_owners"] - compare["total_block"]
    off = compare[compare["difference"].abs() > 1]
    print("Kerjasama Wilus excluded from this reconciliation per PDF p.345 footnote; missing ownership cells remain unresolved.")
    print(f"{len(compare)} grid-scenario-technologies checked, {len(off)} differ by more than 1 MW")
    if not off.empty:
        print(off.to_string())
    print(f"Incomplete ownership groups: {int(compare['ownership_incomplete'].sum())}; differences not computed.")
    bad_hist.to_csv(OUTPUT_DIR / "quality_historical_generation_exceptions.csv")
    bad_proj.to_csv(OUTPUT_DIR / "quality_projected_generation_exceptions.csv")
    bad_emis.to_csv(OUTPUT_DIR / "quality_emissions_exceptions.csv")
    compare.to_csv(OUTPUT_DIR / "quality_capacity_owner_reconciliation.csv")
    return bad_hist, bad_proj, bad_emis


def intensity(proj_gen, emissions):
    generation = proj_gen.groupby(["grid", "scenario", "year"])["generation_gwh"].sum()
    fossil = proj_gen[proj_gen["fuel"].isin(FOSSIL)].groupby(["grid", "scenario", "year"])["generation_gwh"].sum()
    total = emissions[emissions["fuel"] == "Total"].set_index(["grid", "scenario", "year"])["emissions_mtco2"]
    table = pd.DataFrame({
        "generation_gwh": generation,
        "fossil_generation_gwh": fossil,
        "emissions_mtco2": total,
    })
    table["average_tco2_per_mwh"] = (table["emissions_mtco2"] * 1000 / table["generation_gwh"]).round(3)
    table["fossil_tco2_per_mwh"] = (table["emissions_mtco2"] * 1000 / table["fossil_generation_gwh"]).round(3)
    table["fossil_share_pct"] = (100 * table["fossil_generation_gwh"] / table["generation_gwh"]).round(1)
    return table.reset_index()


def cross_checks(hist_gen, proj_gen, capacity, intensity_table):
    results = {}

    print_section("Cross-check: RUPTL geothermal capacity additions vs GENESIS (MW, 2025-2034)")
    ruptl = capacity[(capacity["owner"] == "Total") & (capacity["technology"] == "Geothermal")]
    ruptl = ruptl.groupby(["grid", "scenario"])["capacity_mw"].sum().unstack()
    if GENESIS_SITES_FILE.exists():
        sites = pd.read_csv(GENESIS_SITES_FILE)
        genesis = sites.groupby("grid_by_province")["rencana_pengembangan"].sum()
        ruptl["GENESIS (by province)"] = genesis.reindex(ruptl.index)
    print(ruptl.to_string())
    results["geothermal_capacity"] = ruptl

    print_section("Cross-check: RUPTL geothermal generation vs Ember 'Other renewables' (TWh)")
    geo = hist_gen[(hist_gen["fuel"] == "Geothermal") & ~hist_gen["partial_year"]]
    geo = geo.pivot_table(index="year", columns="grid", values="generation_gwh") / 1000
    geo["RUPTL Jamali + Sumatera"] = geo.sum(axis=1)
    if EMBER_FILE.exists():
        ember = pd.read_csv(EMBER_FILE).set_index("year")["Other renewables"]
        geo["Ember national (mostly geothermal)"] = ember.reindex(geo.index)
        geo["RUPTL share of Ember (%)"] = (100 * geo["RUPTL Jamali + Sumatera"] / geo["Ember national (mostly geothermal)"]).round(1)
    print(geo.round(2).to_string())
    results["geothermal_vs_ember"] = geo.round(2)

    print_section("Cross-check: RUPTL 2025 intensity vs ESDM 2019 factors (tCO2/MWh)")
    rows = []
    esdm = pd.read_csv(ESDM_FILE) if ESDM_FILE.exists() else None
    for grid in GRIDS:
        row = intensity_table[(intensity_table["grid"] == grid) & (intensity_table["year"] == 2025) & (intensity_table["scenario"] == "RE Base")].iloc[0]
        record = {"grid": grid, "RUPTL 2025 average": row["average_tco2_per_mwh"], "RUPTL 2025 fossil-only": row["fossil_tco2_per_mwh"]}
        if esdm is not None:
            factors = esdm[(esdm["grid"] == grid) & (esdm["data_year"] == 2019)].iloc[0]
            record.update({"ESDM 2019 OM": factors["om_tco2_per_mwh"], "ESDM 2019 BM": factors["bm_tco2_per_mwh"],
                           "ESDM 2019 CM 50/50": factors["cm_expost_50_50"]})
        rows.append(record)
    table = pd.DataFrame(rows)
    print(table.to_string(index=False))
    results["intensity_vs_esdm"] = table

    print_section("Diagnostic: geothermal generation / GENESIS start-of-year capacity (not an estimated capacity factor)")
    if GENESIS_PLANNED_FILE.exists() and GENESIS_SITES_FILE.exists():
        sites = pd.read_csv(GENESIS_SITES_FILE)
        installed = sites.groupby("grid_by_province")["kapasitas_terpasang"].sum()
        planned = pd.read_csv(GENESIS_PLANNED_FILE).set_index("tahun")
        rows = []
        for grid in GRIDS:
            capacity_mw = installed.get(grid, 0) + planned.get(grid, pd.Series(dtype=float)).reindex(range(2025, 2035), fill_value=0).cumsum()
            for scenario in SCENARIOS:
                gen = proj_gen[(proj_gen["grid"] == grid) & (proj_gen["scenario"] == scenario) & (proj_gen["fuel"] == "Geothermal")].set_index("year")["generation_gwh"]
                for year in range(2025, 2035):
                    # Capacity added during a year counts from the following year.
                    mw = installed.get(grid, 0) if year == 2025 else capacity_mw.loc[year - 1]
                    rows.append({"grid": grid, "scenario": scenario, "year": year, "capacity_mw_start_of_year": round(mw, 1),
                                 "generation_gwh": gen.get(year), "generation_to_start_capacity_pct": round(100 * gen.get(year) / (mw * 8.76), 1)})
        cf = pd.DataFrame(rows)
        print(cf.pivot_table(index="year", columns=["grid", "scenario"], values="generation_to_start_capacity_pct").to_string())
        print("Values above 100% flag incompatible timing or boundaries, not a measured plant capacity factor;"
              " for Jamali this includes Sumatera geothermal imported over the interconnection.")
        results["geothermal_capacity_factor"] = cf
    return results


def summarise(hist_gen, proj_gen, intensity_table, capacity):
    print_section("Historical generation by fuel, full years (TWh)")
    full = hist_gen[~hist_gen["partial_year"]]
    print((full.pivot_table(index="year", columns=["grid", "fuel"], values="generation_gwh", aggfunc="sum") / 1000).round(1).to_string())

    print_section("Projected generation mix, 2025 and 2034 (% of total)")
    mix = proj_gen[proj_gen["year"].isin([2025, 2034])].pivot_table(index=["grid", "scenario", "year"], columns="fuel",
                                                                    values="generation_gwh", aggfunc="sum")
    print((100 * mix.div(mix.sum(axis=1), axis=0)).round(1).to_string())

    print_section("Projected emission intensity (tCO2/MWh)")
    print(intensity_table.pivot_table(index="year", columns=["grid", "scenario"],
                                      values=["average_tco2_per_mwh", "fossil_tco2_per_mwh"]).to_string())

    print_section("Capacity additions 2025-2034 by technology (MW, Total block)")
    total = capacity[capacity["owner"] == "Total"].pivot_table(index="technology", columns=["grid", "scenario"],
                                                               values="capacity_mw", aggfunc="sum")
    print(total.round(0).to_string())


def plot_historical(hist_gen):
    full = hist_gen[~hist_gen["partial_year"]]
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=False)
    for ax, grid in zip(axes, HISTORICAL_GENERATION):
        wide = full[full["grid"] == grid].pivot_table(index="year", columns="fuel", values="generation_gwh", aggfunc="sum") / 1000
        wide = wide[[f for f in FUEL_COLOURS if f in wide.columns]]
        wide.plot(kind="bar", stacked=True, ax=ax, color=[FUEL_COLOURS[f] for f in wide.columns], width=0.8, legend=False)
        ax.set_title(grid)
        ax.set_xlabel("Year")
        ax.set_ylabel("Generation (TWh)")
        ax.grid(axis="y", alpha=0.3)
    handles, labels = axes[0].get_legend_handles_labels()
    extra_h, extra_l = axes[1].get_legend_handles_labels()
    legend = dict(zip(labels + extra_l, handles + extra_h))
    fig.legend(legend.values(), legend.keys(), loc="center right")
    fig.suptitle(f"Historical generation by fuel, PLN system ({min(full['year'])}-{max(full['year'])}; {PARTIAL_YEAR} excluded as partial)")
    fig.tight_layout(rect=(0, 0, 0.88, 0.95))
    fig.savefig(OUTPUT_DIR / "historical_generation_by_fuel.png", dpi=150)
    plt.close(fig)


def plot_projected(proj_gen):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharey="row")
    for row, grid in enumerate(GRIDS):
        for col, scenario in enumerate(SCENARIOS):
            ax = axes[row, col]
            data = proj_gen[(proj_gen["grid"] == grid) & (proj_gen["scenario"] == scenario)]
            wide = data.pivot_table(index="year", columns="fuel", values="generation_gwh", aggfunc="sum") / 1000
            wide = wide[[f for f in FUEL_COLOURS if f in wide.columns]]
            wide.plot(kind="bar", stacked=True, ax=ax, color=[FUEL_COLOURS[f] for f in wide.columns], width=0.8, legend=False)
            ax.set_title(f"{grid}, {scenario}")
            ax.set_xlabel("Year")
            ax.set_ylabel("Generation (TWh)")
            ax.grid(axis="y", alpha=0.3)
    legend = {}
    for ax in axes.flat:
        handles, labels = ax.get_legend_handles_labels()
        legend.update(dict(zip(labels, handles)))
    fig.legend(legend.values(), legend.keys(), loc="center right")
    fig.suptitle("Projected generation by fuel, RUPTL 2025-2034")
    fig.tight_layout(rect=(0, 0, 0.88, 0.96))
    fig.savefig(OUTPUT_DIR / "projected_generation_by_fuel.png", dpi=150)
    plt.close(fig)


def plot_intensity(intensity_table):
    esdm = pd.read_csv(ESDM_FILE) if ESDM_FILE.exists() else None
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
    measure_handles = [
        Line2D([0], [0], color="tab:brown", marker="o", label="Fossil-generation intensity"),
        Line2D([0], [0], color="tab:blue", marker="o", label="Average grid intensity"),
    ]
    scenario_handles = [
        Line2D([0], [0], color="black", linestyle="-", label="RE Base"),
        Line2D([0], [0], color="black", linestyle="--", label="ARED"),
    ]
    for ax, grid in zip(axes, GRIDS):
        reference_handles = []
        for scenario, style in zip(SCENARIOS, ["-", "--"]):
            data = intensity_table[(intensity_table["grid"] == grid) & (intensity_table["scenario"] == scenario)]
            ax.plot(data["year"], data["fossil_tco2_per_mwh"], style, color="tab:brown", marker="o")
            ax.plot(data["year"], data["average_tco2_per_mwh"], style, color="tab:blue", marker="o")
        if esdm is not None:
            factors = esdm[(esdm["grid"] == grid) & (esdm["data_year"] == 2019)].iloc[0]
            for column, colour, name in (("om_tco2_per_mwh", "tab:red", "ESDM 2019 OM"),
                                         ("bm_tco2_per_mwh", "tab:purple", "ESDM 2019 BM"),
                                         ("cm_expost_50_50", "black", "ESDM 2019 CM 50/50")):
                ax.axhline(factors[column], color=colour, linestyle=":")
                reference_handles.append(Line2D([0], [0], color=colour, linestyle=":", label=f"{name}: {factors[column]:.2f}"))
        ax.set_title(grid)
        ax.set_xlabel("Year")
        ax.set_ylabel("tCO2/MWh")
        ax.set_ylim(0, 1.3)
        ax.grid(alpha=0.3)
        measure_legend = ax.legend(handles=measure_handles, title="Measure", fontsize=8, title_fontsize=8, loc="upper left")
        ax.add_artist(measure_legend)
        scenario_legend = ax.legend(handles=scenario_handles, title="Scenario", fontsize=8, title_fontsize=8, loc="upper right")
        ax.add_artist(scenario_legend)
        ax.legend(handles=reference_handles, title="ESDM 2019 reference", fontsize=8, title_fontsize=8, loc="lower left")
    fig.suptitle("Projected emission intensity from RUPTL emissions and generation, with ESDM 2019 factors for reference")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUTPUT_DIR / "projected_intensity.png", dpi=150)
    plt.close(fig)


def plot_geothermal(hist_gen, proj_gen):
    fig, ax = plt.subplots(figsize=(13, 6))
    history = hist_gen[(hist_gen["fuel"] == "Geothermal") & ~hist_gen["partial_year"]]
    colours = {"Jamali": "tab:red", "Sumatera": "tab:blue", "Sumatera + Kalimantan": "tab:blue"}
    for grid, data in history.groupby("grid"):
        ax.plot(data["year"], data["generation_gwh"] / 1000, color=colours[grid], marker="o", label=f"{grid}, actual")
    for grid in GRIDS:
        for scenario, style in zip(SCENARIOS, ["--", ":"]):
            data = proj_gen[(proj_gen["grid"] == grid) & (proj_gen["scenario"] == scenario) & (proj_gen["fuel"] == "Geothermal")]
            ax.plot(data["year"], data["generation_gwh"] / 1000, style, color=colours[grid], marker=".", label=f"{grid}, {scenario}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Geothermal generation (TWh)")
    ax.set_title("Geothermal generation: actual (RUPTL Tabel 4.32/4.33) and projected (RUPTL Tabel 5.135-5.144)\n"
                 "Jamali projections include Sumatera geothermal imported over the Sumatera-Java interconnection")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "geothermal_generation.png", dpi=150)
    plt.close(fig)


def plot_capacity(capacity):
    total = capacity[(capacity["owner"] == "Total") & (capacity["scenario"] == "RE Base")]
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
    for ax, grid in zip(axes, GRIDS):
        wide = total[total["grid"] == grid].pivot_table(index="year", columns="technology", values="capacity_mw", aggfunc="sum") / 1000
        wide = wide.loc[:, wide.sum() > 0]
        wide = wide[[t for t in FUEL_COLOURS if t in wide.columns]]
        wide.plot(kind="bar", stacked=True, ax=ax, color=[FUEL_COLOURS[t] for t in wide.columns], width=0.8, legend=False)
        ax.set_title(f"{grid}, RE Base")
        ax.set_xlabel("Year")
        ax.set_ylabel("Capacity added (GW)")
        ax.grid(axis="y", alpha=0.3)
    legend = {}
    for ax in axes:
        handles, labels = ax.get_legend_handles_labels()
        legend.update(dict(zip(labels, handles)))
    fig.legend(legend.values(), legend.keys(), loc="center right")
    fig.suptitle("Planned capacity additions by technology, RUPTL 2025-2034 (RE Base)")
    fig.tight_layout(rect=(0, 0, 0.87, 0.95))
    fig.savefig(OUTPUT_DIR / "capacity_additions.png", dpi=150)
    plt.close(fig)


def html_table(data, index=False):
    return f'<div class="scroll">{data.to_html(index=index, na_rep="")}</div>'


def show_data(tables, cross):
    sections = ['<p><b>See <a href="eda_findings.md">EDA findings and limitations</a> before modelling. Fossil-only intensity is not an official OM, BM or CM.</b></p>', f"<p>Source: {SOURCE}. <a href=\"{SOURCE_URL}\">PDF</a>.</p>"]
    for title, (data, table_numbers) in tables.items():
        sections.append(f"<h2>{title} ({table_numbers}; {data.shape[0]} rows)</h2>{html_table(data)}")
    for title, data in cross.items():
        sections.append(f"<h2>Cross-check: {title.replace('_', ' ')}</h2>{html_table(data, index=not isinstance(data.index, pd.RangeIndex))}")
    sections.append(f"<h2>Data dictionary</h2>{html_table(DATA_DICTIONARY)}")
    sections.append(f"<h2>Filtering and extraction notes</h2>{html_table(FILTER_NOTES)}")
    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>RUPTL 2025-2034 tables</title>
<style>
  body {{ font-family: -apple-system, sans-serif; margin: 20px; }}
  .scroll {{ max-height: 60vh; overflow: auto; border: 1px solid #ccc; margin-bottom: 30px; }}
  table {{ border-collapse: collapse; font-size: 13px; }}
  th, td {{ padding: 4px 10px; border-bottom: 1px solid #eee; text-align: right; white-space: nowrap; }}
  th {{ position: sticky; top: 0; background: #f4f4f4; }}
  tr:hover td {{ background: #fafae0; }}
</style>
</head>
<body>
<h1>RUPTL 2025-2034: Jamali and Sumatera tables</h1>
{"".join(sections)}
</body>
</html>"""
    html_file = OUTPUT_DIR / "ruptl_data.html"
    html_file.write_text(page)
    if "--open" in sys.argv:
        webbrowser.open(html_file.as_uri())
    print(f"HTML report saved: {html_file}")


def main():
    if not PDF_FILE.exists():
        sys.exit(f"Missing {PDF_FILE}. Download it from {SOURCE_URL}")
    OUTPUT_DIR.mkdir(exist_ok=True)
    pdf = Pdf(PDF_FILE)

    hist_sales = historical_sales(pdf)
    hist_gen, hist_totals = historical_generation(pdf)
    proj_sales = projected_sales(pdf)
    proj_gen, proj_totals = projected_generation(pdf)
    emissions = projected_emissions(pdf)
    capacity, missing = capacity_additions(pdf)

    print_section("Shape of each extracted table")
    tables = {
        "Historical sales": (hist_sales, TABLE_NUMBERS["historical_sales"]),
        "Historical generation by fuel": (hist_gen, TABLE_NUMBERS["historical_generation"]),
        "Projected sales": (proj_sales, TABLE_NUMBERS["projected_sales"]),
        "Projected generation by fuel": (proj_gen, TABLE_NUMBERS["projected_generation"]),
        "Projected emissions by fuel": (emissions, TABLE_NUMBERS["projected_emissions"]),
        "Capacity additions": (capacity, TABLE_NUMBERS["capacity_additions"]),
    }
    for name, (data, numbers) in tables.items():
        print(f"{name}: {data.shape[0]} rows x {data.shape[1]} columns, years {data['year'].min()}-{data['year'].max()}, "
              f"missing values {int(data.isna().sum().sum())}  [{numbers}]")

    check(hist_gen, hist_totals, proj_gen, proj_totals, emissions, capacity, missing, hist_sales, proj_sales)
    for name, (data, _) in tables.items():
        keys = [c for c in data.columns if c not in {"sales_gwh", "generation_gwh", "capacity_mw", "emissions_mtco2", "fuel", "technology", "partial_year"}]
        if "fuel" in data and "fuel_ruptl" not in data:
            keys.append("fuel")
        if data.duplicated(keys).any():
            raise ValueError(f"Duplicate keys in {name}")
        value = next(c for c in data if c.endswith(("_gwh", "_mw", "_mtco2")))
        if (data[value].dropna() < 0).any():
            raise ValueError(f"Negative values in {name}")
    if len(hist_gen) != 300 or len(proj_totals) != 40:
        raise ValueError("Unexpected generation coverage")
    intensity_table = intensity(proj_gen, emissions)
    tables["Projected emission intensity"] = (intensity_table, "derived from the generation and emissions tables")
    summarise(hist_gen, proj_gen, intensity_table, capacity)
    cross = cross_checks(hist_gen, proj_gen, capacity, intensity_table)

    hist_sales.to_csv(OUTPUT_DIR / "ruptl_historical_sales.csv", index=False)
    hist_gen.to_csv(OUTPUT_DIR / "ruptl_historical_generation.csv", index=False)
    proj_sales.to_csv(OUTPUT_DIR / "ruptl_projected_sales.csv", index=False)
    proj_gen.to_csv(OUTPUT_DIR / "ruptl_projected_generation.csv", index=False)
    emissions.to_csv(OUTPUT_DIR / "ruptl_projected_emissions.csv", index=False)
    capacity.to_csv(OUTPUT_DIR / "ruptl_capacity_additions.csv", index=False)
    intensity_table.to_csv(OUTPUT_DIR / "ruptl_projected_intensity.csv", index=False)
    DATA_DICTIONARY.to_csv(OUTPUT_DIR / "data_dictionary.csv", index=False)
    FILTER_NOTES.to_csv(OUTPUT_DIR / "filter_notes.csv", index=False)
    for name, data in cross.items():
        data.to_csv(OUTPUT_DIR / f"crosscheck_{name}.csv", index=not isinstance(data.index, pd.RangeIndex))

    plot_historical(hist_gen)
    plot_projected(proj_gen)
    plot_intensity(intensity_table)
    plot_geothermal(hist_gen, proj_gen)
    plot_capacity(capacity)
    show_data(tables, cross)
    print(f"\nTables and plots saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
