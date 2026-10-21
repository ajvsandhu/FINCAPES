import sys
from pathlib import Path

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
IGES_FILE = SCRIPT_DIR / "raw" / "IGES_GRID_EF_v11.7_20260309.xlsx"
OUTPUT_DIR = SCRIPT_DIR / "output"
SOURCE = "IGES List of Grid Emission Factors v11.7 (March 2026)"

STUDY_GRIDS = {"Jamali": "Jamali", "Jamali (Jawa-Madura-Bali)": "Jamali", "Sumatera": "Sumatera"}
FACTOR_COLUMNS = [
    "om_tco2_per_mwh", "om_exante_tco2_per_mwh", "bm_tco2_per_mwh",
    "cm_expost_50_50", "cm_expost_75_25", "cm_exante_50_50", "cm_exante_75_25",
]
# Column positions in the yearly ESDM sheets; the 2018 table has an extra ex-ante OM column.
YEARLY_SHEET_COLUMNS = {
    "Indonesia2017": {1: "grid", 3: "om_tco2_per_mwh", 4: "bm_tco2_per_mwh", 5: "cm_expost_50_50",
                      6: "cm_expost_75_25", 7: "cm_exante_50_50", 8: "cm_exante_75_25"},
    "Indonesia2018": {1: "grid", 3: "om_tco2_per_mwh", 4: "om_exante_tco2_per_mwh", 5: "bm_tco2_per_mwh",
                      6: "cm_expost_50_50", 7: "cm_expost_75_25", 8: "cm_exante_50_50", 9: "cm_exante_75_25"},
    "Indonesia2019": {1: "grid", 3: "om_tco2_per_mwh", 4: "bm_tco2_per_mwh", 5: "cm_expost_50_50",
                      6: "cm_expost_75_25", 7: "cm_exante_50_50", 8: "cm_exante_75_25"},
}
CDM_COLUMNS = {
    2: "cdm_reference", 3: "crediting_start", 4: "registration_date", 5: "om_vintage", 6: "om_method",
    7: "om_tco2_per_mwh", 8: "bm_vintage", 9: "bm_tco2_per_mwh", 10: "om_bm_weights", 11: "cm_tco2_per_mwh",
    12: "renewal_date", 13: "second_renewal_date",
}


def number(value):
    if pd.isna(value):
        return None
    text = str(value).strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def yearly_factors():
    rows = []
    for sheet, columns in YEARLY_SHEET_COLUMNS.items():
        table = pd.read_excel(IGES_FILE, sheet, header=None).rename(columns=columns)
        table = table[table["grid"].isin(STUDY_GRIDS)]
        for _, row in table.iterrows():
            record = {"data_year": int(sheet[-4:]), "grid": STUDY_GRIDS[row["grid"]]}
            record.update({column: number(row.get(column)) for column in FACTOR_COLUMNS})
            rows.append(record)
    return pd.DataFrame(rows).sort_values(["grid", "data_year"])


def official_series():
    table = pd.read_excel(IGES_FILE, "EFfromCountriesOrSB", header=None)
    years = table.iloc[3]
    year_columns = [i for i, year in years.items() if str(year).replace(".0", "").isdigit()]
    start = table.index[table[0].astype(str).str.strip() == "Indonesia"][0]
    rows, grid = [], None
    for index in range(start, len(table)):
        if index > start and pd.notna(table.iat[index, 0]):
            break
        if pd.notna(table.iat[index, 1]):
            grid = str(table.iat[index, 1]).strip()
        if grid not in STUDY_GRIDS:
            continue
        for column in year_columns:
            value = number(table.iat[index, column])
            if value is not None:
                rows.append({
                    "grid": STUDY_GRIDS[grid],
                    "vintage": str(table.iat[index, 3]).strip().lower(),
                    "data_year": int(float(years[column])),
                    "cm_tco2_per_mwh": value,
                })
    return pd.DataFrame(rows).sort_values(["grid", "vintage", "data_year"])


def cdm_projects():
    table = pd.read_excel(IGES_FILE, "EFfromCDMProjects", header=None, skiprows=3)
    table = table[table[1].astype(str).str.strip() == "Indonesia"].rename(columns=CDM_COLUMNS)
    table = table[list(CDM_COLUMNS.values())]
    for column in ["om_tco2_per_mwh", "bm_tco2_per_mwh", "cm_tco2_per_mwh"]:
        table[column] = table[column].map(number)
    for column in ["crediting_start", "registration_date", "renewal_date", "second_renewal_date"]:
        table[column] = pd.to_datetime(table[column], errors="coerce").dt.date
    return table.sort_values("registration_date").reset_index(drop=True)


def print_section(title):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def main():
    if not IGES_FILE.exists():
        sys.exit(f"Missing {IGES_FILE}. Download it from https://www.iges.or.jp/en/pub/list-grid-emission-factor/en")
    OUTPUT_DIR.mkdir(exist_ok=True)

    yearly = yearly_factors()
    print_section("ESDM factors by data year, Jamali and Sumatera (tCO2/MWh)")
    print(yearly.to_string(index=False))

    series = official_series()
    print_section("Official combined margin series (IGES country sheet; weighting not stated)")
    print(series.pivot_table(index="data_year", columns=["grid", "vintage"], values="cm_tco2_per_mwh").to_string())

    projects = cdm_projects()
    print_section(f"Indonesian CDM projects: {len(projects)} (grid and project type are not in this file)")
    print(projects[["om_tco2_per_mwh", "bm_tco2_per_mwh", "cm_tco2_per_mwh"]].describe().round(3).to_string())
    print("\nOM/BM weights used:")
    print(projects["om_bm_weights"].value_counts().to_string())

    yearly.to_csv(OUTPUT_DIR / "esdm_factors_2017_2019_study_grids.csv", index=False)
    series.to_csv(OUTPUT_DIR / "official_cm_series_study_grids.csv", index=False)
    projects.to_csv(OUTPUT_DIR / "indonesia_cdm_project_factors.csv", index=False)
    print(f"\nSource: {SOURCE}\nSaved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
