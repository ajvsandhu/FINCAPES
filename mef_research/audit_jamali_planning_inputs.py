"""Reconcile published Jamali planning quantities without changing earlier outputs."""

import csv
import hashlib
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

import fitz
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REVIEW_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = REVIEW_ROOT.parent
OUTPUT_ROOT = REVIEW_ROOT / "output" / "jamali_input_audit"
YEARS = list(range(2025, 2035))
SCENARIOS = {"RE Base": 351, "ARED": 355}
SYSTEM_FIELDS = {
    "sales_gwh": "a. Penjualan",
    "production_gwh": "c. Produksi",
    "load_factor_pct": "d. Faktor Beban",
    "gross_peak_mw": "e. Beban Puncak Bruto",
    "net_peak_mw": "f. Beban Puncak Neto",
    "existing_installed_mw": "a. Total Kapasitas Terpasang",
    "existing_net_dependable_mw": "b. Total Daya Mampu Netto (DMN):",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verified_bytes(path, metadata):
    content = path.read_bytes()
    require(len(content) == metadata["size_bytes"], f"Size mismatch: {path.name}")
    require(hashlib.sha256(content).hexdigest() == metadata["sha256"], f"Hash mismatch: {path.name}")
    return content


def source_number(cell):
    text = "".join(str(cell).split()).replace("%", "")
    require(text not in {"", "None", "-", "–"}, f"Missing numeric cell: {cell!r}")
    require(all(character in "0123456789.,-" for character in text), f"Unexpected numeric cell: {cell!r}")
    return Decimal(text.replace(".", "").replace(",", "."))


def unique_row(table, label):
    matches = [row for row in table if row[0] is not None and " ".join(row[0].split()) == label]
    require(len(matches) == 1, f"Expected exactly one source row: {label}")
    require(len(matches[0][2:]) == len(YEARS), f"Unexpected year count: {label}")
    return matches[0]


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def extract_regional_table(document):
    page = document[323]
    require("Tabel 5.69" in page.get_text(), "Regional sales table moved")
    table = page.find_tables().tables[0].extract()
    require(len(table) == 1 and len(table[0]) == 11, "Unexpected merged regional table layout")
    require("Total" in table[0][0], "Regional total label missing")
    records = []
    for expected_year, cell in zip(YEARS, table[0][1:]):
        values = cell.splitlines()
        require(len(values) == 9 and int(values[0]) == expected_year, "Unexpected regional year layout")
        records.append({
            "year": expected_year,
            "sales_gwh": float(source_number(values[5])),
            "reported_noncoincident_peak_mw": float(source_number(values[8])),
            "sector_sum_minus_total_gwh": float(sum(source_number(value) for value in values[1:5]) - source_number(values[5])),
            "source": "RUPTL Table 5.69, PDF p.324 (V-88)",
        })
    return records, table


def extract_system_tables(document):
    records = []
    source_tables = {}
    for scenario, page_number in SCENARIOS.items():
        page = document[page_number - 1]
        table_number = "5.86" if scenario == "RE Base" else "5.87"
        require(f"Tabel {table_number}" in page.get_text(), "System power-balance table moved")
        table = page.find_tables().tables[0].extract()
        require([int(value) for value in table[0][2:]] == YEARS, "Unexpected system year headings")
        field_rows = {field: unique_row(table, label) for field, label in SYSTEM_FIELDS.items()}
        retired = unique_row(table, "6) Retired")[2:]
        mothballed = unique_row(table, "7) Mothballed")[2:]
        for column, year in enumerate(YEARS):
            record = {
                "scenario": scenario,
                "year": year,
                "source": f"RUPTL Table {table_number}, PDF p.{page_number}",
            }
            record.update({field: float(source_number(row[column + 2])) for field, row in field_rows.items()})
            record["retired_raw"] = retired[column]
            record["mothballed_raw"] = mothballed[column]
            records.append(record)
        source_tables[f"system_{scenario}"] = table
    return records, source_tables


def regional_production_totals(document):
    result = {}
    raw_tables = {}
    for scenario, page_number in [("RE Base", 484), ("ARED", 485)]:
        table = document[page_number - 1].find_tables().tables[0].extract()
        values = unique_row(table, "Total")[2:]
        result[scenario] = [float(source_number(value)) for value in values]
        raw_tables[f"regional_production_{scenario}"] = table
    return result, raw_tables


def legacy_crosschecks(regional, production_totals, manifest):
    input_paths = {source["source_id"]: REPOSITORY_ROOT / source["repository_path"] for source in manifest["repository_inputs"]}
    with input_paths["J3a"].open() as source:
        sales_rows = [row for row in csv.DictReader(source) if row["grid"] == "Jamali" and row["customer_group"] == "Total"]
    require(len(sales_rows) == 10 and len({row["year"] for row in sales_rows}) == 10, "Duplicate or missing legacy sales years")
    require({int(row["year"]): float(row["sales_gwh"]) for row in sales_rows} == {row["year"]: row["sales_gwh"] for row in regional}, "Legacy regional sales disagree with primary table")
    generation = defaultdict(float)
    seen = set()
    with input_paths["J3b"].open() as source:
        for row in csv.DictReader(source):
            if row["grid"] != "Jamali":
                continue
            key = (row["scenario"], int(row["year"]), row["fuel_ruptl"])
            require(key not in seen, f"Duplicate legacy generation component: {key}")
            seen.add(key)
            generation[key[:2]] += float(row["generation_gwh"])
    require(set(generation) == {(scenario, year) for scenario in SCENARIOS for year in YEARS}, "Unexpected legacy scenario/year coverage")
    residuals = []
    for scenario in SCENARIOS:
        for position, year in enumerate(YEARS):
            residual = generation[(scenario, year)] - production_totals[scenario][position]
            require(abs(residual) <= 3, "Component residual exceeds earlier extraction's 3 GWh tolerance")
            residuals.append({"scenario": scenario, "year": year, "component_sum_minus_published_total_gwh": residual})
    return residuals


def draw_boundary_gaps(records):
    figure, axis = plt.subplots(figsize=(10, 5.8))
    axis.plot(YEARS, [row["regional_minus_system_sales_gwh"] for row in records], marker="o", label="Sales: regional table minus system table", color="#2274a5")
    axis.plot(YEARS, [row["regional_minus_system_production_gwh"] for row in records], marker="s", label="Generation: regional table minus system table", color="#c76e21")
    for field, offset in [("regional_minus_system_sales_gwh", -18), ("regional_minus_system_production_gwh", 10)]:
        axis.annotate(f"{records[-1][field]:,.0f} GWh", (YEARS[-1], records[-1][field]), xytext=(-6, offset), textcoords="offset points", ha="right", fontsize=11)
    axis.set_ylim(bottom=0, top=max(row["regional_minus_system_production_gwh"] for row in records) * 1.17)
    axis.set_xticks(YEARS)
    axis.set_xlabel("Planning year", fontsize=11)
    axis.set_ylabel("Difference between published totals (GWh/year)", fontsize=11)
    axis.tick_params(labelsize=10)
    axis.grid(axis="y", alpha=0.25)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(loc="upper left", fontsize=10, frameon=False)
    figure.suptitle("Jamali planning tables do not have identical totals", fontsize=15, y=0.97)
    axis.set_title("RUPTL 2025–2034: annual projections, not operating observations", fontsize=11, pad=16)
    figure.text(0.12, 0.02, "Differences are not attributed to losses or isolated systems without a reconciliation.\nSources: Tables 5.69, 5.86 and 5.143. This is not an emissions or MEF result.", fontsize=9)
    figure.subplots_adjust(bottom=0.21, top=0.82, right=0.97, left=0.12)
    figure.savefig(OUTPUT_ROOT / "demand_boundary_comparison.png", dpi=200)
    plt.close(figure)


def main():
    manifest = json.loads((REVIEW_ROOT / "planning_input_audit_manifest.json").read_text())
    long_run = json.loads((REVIEW_ROOT / "long_run_review_manifest.json").read_text())
    ruptl_source = next(source for source in long_run["repository_inputs"] if source["source_id"] == "L6")
    ruptl_path = REPOSITORY_ROOT / ruptl_source["repository_path"]
    verified_bytes(ruptl_path, ruptl_source)
    for source in manifest["repository_inputs"]:
        verified_bytes(REPOSITORY_ROOT / source["repository_path"], source)
    statistics_source = manifest["snapshots"][0]
    statistics_path = REVIEW_ROOT / statistics_source["local_path"]
    verified_bytes(statistics_path, statistics_source)
    with fitz.open(statistics_path) as statistics:
        require(len(statistics) == 106, "Unexpected statistics page count")
        require("1 Januari 2024" in statistics[10].get_text(), "Statistics calendar-year definition missing")
        require("Harga Satuan" in statistics[14].get_text(), "Fuel-price contents entry missing")
        require("Tabel/Table 25" in statistics[66].get_text(), "Annual fuel-price table missing")
    with fitz.open(ruptl_path) as document:
        require(len(document) == ruptl_source["pdf_pages"], "Unexpected RUPTL page count")
        regional, raw_regional = extract_regional_table(document)
        system, raw_system = extract_system_tables(document)
        production_totals, raw_production = regional_production_totals(document)
        text = " ".join(document[359].get_text().split())
        require("PLTS Sistem Isolated Jawa" in text, "Isolated-solar boundary note missing")
        require("25 subsistem isolated" in " ".join(document[917].get_text().split()), "East Java isolated-system note missing")
    comparisons = []
    source_differences = []
    for position, year in enumerate(YEARS):
        current = {row["scenario"]: row for row in system if row["year"] == year}
        for field in SYSTEM_FIELDS:
            difference = current["ARED"][field] - current["RE Base"][field]
            if difference:
                source_differences.append({"year": year, "field": field, "ared_minus_re_base": difference})
        for field in ["sales_gwh", "production_gwh", "net_peak_mw"]:
            require(current["RE Base"][field] == current["ARED"][field], f"Scenario demand difference: {field}")
        require(production_totals["RE Base"][position] == production_totals["ARED"][position], "Published regional production totals differ")
        base = current["RE Base"]
        comparisons.append({
            "year": year,
            "regional_sales_gwh": regional[position]["sales_gwh"],
            "system_sales_gwh": base["sales_gwh"],
            "regional_minus_system_sales_gwh": regional[position]["sales_gwh"] - base["sales_gwh"],
            "regional_production_gwh": production_totals["RE Base"][position],
            "system_production_gwh": base["production_gwh"],
            "regional_minus_system_production_gwh": production_totals["RE Base"][position] - base["production_gwh"],
            "system_production_minus_sales_gwh": base["production_gwh"] - base["sales_gwh"],
            "regional_sales_difference_pct_of_regional": 100 * (regional[position]["sales_gwh"] - base["sales_gwh"]) / regional[position]["sales_gwh"],
        })
    require(all(row["regional_minus_system_sales_gwh"] > 0 and row["regional_minus_system_production_gwh"] > 0 for row in comparisons), "Unexpected direction of source differences")
    require(comparisons[0]["regional_sales_gwh"] == 226327 and comparisons[0]["system_sales_gwh"] == 226107, "2025 source cross-check failed")
    residuals = legacy_crosschecks(regional, production_totals, manifest)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_ROOT / "demand_reconciliation.json", {
        "review_date": manifest["review_date"],
        "status": "Published projections; boundary bridge unresolved; not an MEF dataset",
        "annual_comparisons": comparisons,
        "regional_records": regional,
        "system_records": system,
        "published_scenario_field_differences": source_differences,
        "legacy_component_rounding_residuals": residuals,
    })
    write_json(OUTPUT_ROOT / "source_table_cells.json", {"regional_sales": raw_regional, **raw_system, **raw_production})
    write_json(OUTPUT_ROOT / "validation_results.json", {
        "status": "PASS",
        "years_checked": len(YEARS),
        "system_scenario_years_checked": len(system),
        "legacy_sales_agreement": "exact",
        "legacy_generation_max_absolute_component_residual_gwh": max(abs(row["component_sum_minus_published_total_gwh"]) for row in residuals),
        "source_field_differences_preserved": source_differences,
        "pdf_extractor_version": fitz.VersionBind,
        "matplotlib_version": matplotlib.__version__,
        "limits": "Integrity and reconciliation checks, not model validation or emissions accuracy",
    })
    draw_boundary_gaps(comparisons)
    print(f"PASS: {len(YEARS)} planning years, {len(system)} system scenario-years; legacy sales exact; component residuals retained.")
    print("Source differences preserved:", source_differences)
    print(f"Outputs: {OUTPUT_ROOT}")
    print("No interval operating dataset or numerical MEF was created.")


if __name__ == "__main__":
    main()
