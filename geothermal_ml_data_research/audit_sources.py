from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import argparse
import gzip
import json
import re
import zipfile

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
DATA = ROOT / "data"
OUTPUT = ROOT / "output"
NZ_BASE = "https://www.emi.ea.govt.nz/Wholesale/Datasets/Generation/Generation_MD"
EIA_URL = "https://www.eia.gov/electricity/data/eia923/archive/xls/f923_2024.zip"


def download(url, filename, compressed=False):
    destination = RAW / filename
    if destination.exists():
        content = gzip.decompress(destination.read_bytes()) if compressed else destination.read_bytes()
    else:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        content = response.content
        if content.lstrip().lower().startswith((b"<html", b"<!doctype html")):
            raise ValueError(f"Expected data, received HTML: {url}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(gzip.compress(content, mtime=0) if compressed else content)
    return content, {
        "url": url,
        "local_file": str(destination.relative_to(ROOT)),
        "uncompressed_bytes": len(content),
        "uncompressed_sha256": sha256(content).hexdigest(),
        "retrieved_on": "2026-10-29",
    }


def audit_nz(start, end):
    months = pd.period_range(f"{start}-01", f"{end}-12", freq="M")

    def read_month(month):
        filename = f"{month.strftime('%Y%m')}_Generation_MD.csv"
        content, metadata = download(f"{NZ_BASE}/{filename}", f"nz/{filename}.gz", compressed=True)
        source = pd.read_csv(BytesIO(content))
        source = source.rename(columns={"Trading_date": "Trading_Date"})
        source["Trading_Date"] = pd.to_datetime(source["Trading_Date"], errors="raise")
        if source["Trading_Date"].isna().any() or not source["Trading_Date"].dt.to_period("M").eq(month).all():
            raise ValueError(f"Unexpected dates in {filename}")
        geothermal = source.loc[source["Fuel_Code"].eq("Geo")].copy()
        geothermal["source_file"] = filename
        metadata["all_rows"] = len(source)
        metadata["geothermal_rows"] = len(geothermal)
        return geothermal, metadata

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(read_month, months))
    data = pd.concat([result[0] for result in results], ignore_index=True)
    periods = [f"TP{number}" for number in range(1, 51)]
    data["intervals_present"] = data[periods].notna().sum(axis=1)
    data["daily_kwh"] = data[periods].sum(axis=1, min_count=1)
    data["Trading_Date"] = pd.to_datetime(data["Trading_Date"])
    data.to_csv(DATA / "nz_geothermal_meter_days.csv.gz", index=False, compression="gzip")
    monthly = data.assign(month=data["Trading_Date"].dt.to_period("M").astype(str)).groupby(
        ["Gen_Code", "month"], as_index=False
    ).agg(meter_rows=("daily_kwh", "size"), dates=("Trading_Date", "nunique"), generation_kwh=("daily_kwh", "sum"))
    monthly.to_csv(DATA / "nz_geothermal_generator_months.csv", index=False)
    coverage = data.groupby("Gen_Code", as_index=False).agg(
        first_date=("Trading_Date", "min"), last_date=("Trading_Date", "max"),
        meter_rows=("Trading_Date", "size"), unique_dates=("Trading_Date", "nunique"),
        sites=("Site_Code", "nunique"), points_of_connection=("POC_Code", "nunique"),
    )
    coverage.to_csv(OUTPUT / "nz_generator_coverage.csv", index=False)
    multiple_meter_days = data.groupby(["Gen_Code", "Trading_Date"]).size()
    multiple_meter_days = multiple_meter_days.loc[multiple_meter_days.gt(1)]
    unexpected_month_lengths = monthly["dates"].ne(pd.to_datetime(monthly["month"]).dt.days_in_month)
    key = ["Site_Code", "POC_Code", "Nwk_Code", "Gen_Code", "Fuel_Code", "Tech_Code", "Trading_Date"]
    summary = {
        "first_date": str(data["Trading_Date"].min().date()),
        "last_date": str(data["Trading_Date"].max().date()),
        "files": len(results), "geothermal_meter_day_rows": len(data),
        "generators": int(data["Gen_Code"].nunique()),
        "generator_months": len(monthly),
        "distinct_casefold_generator_codes": int(data["Gen_Code"].str.casefold().nunique()),
        "casefold_aliases": data.groupby(data["Gen_Code"].str.casefold())["Gen_Code"].unique().apply(list).to_dict(),
        "nonmissing_halfhour_cells": int(data["intervals_present"].sum()),
        "duplicate_full_meter_date_keys": int(data.duplicated(key).sum()),
        "intervals_present_histogram": data["intervals_present"].value_counts().sort_index().to_dict(),
        "negative_interval_cells": int(data[periods].lt(0).sum().sum()),
        "zero_daily_rows": int(data["daily_kwh"].eq(0).sum()),
        "generator_days_with_multiple_meter_rows": len(multiple_meter_days),
        "generators_with_multiple_meter_rows": sorted(multiple_meter_days.index.get_level_values(0).unique().tolist()),
        "generator_months_with_missing_dates": int(unexpected_month_lengths.sum()),
        "warning": "Meter-day rows and halfhour cells are not independent plants or samples. Check EA definitions, DST, meter mapping and capacity histories before modeling.",
    }
    (OUTPUT / "nz_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUTPUT / "nz_download_manifest.json").write_text(json.dumps([result[1] for result in results], indent=2) + "\n")
    print("NZ", json.dumps(summary), flush=True)


def audit_eia():
    content, metadata = download(EIA_URL, "eia/f923_2024.zip")
    archive = zipfile.ZipFile(BytesIO(content))
    filename = next(name for name in archive.namelist() if "Schedules_2_3_4_5" in name)
    workbook = pd.ExcelFile(BytesIO(archive.read(filename)))
    sheet = "Page 1 Generation and Fuel Data"
    preview = pd.read_excel(workbook, sheet_name=sheet, header=None, nrows=15)
    header = next(index for index, row in preview.iterrows() if "Plant Id" in row.astype(str).tolist())
    data = pd.read_excel(workbook, sheet_name=sheet, header=header)
    data.columns = [re.sub(r"\s+", " ", str(column)).strip() for column in data.columns]
    fuel_column = next(column for column in data.columns if column == "Reported Fuel Type Code")
    geothermal = data.loc[data[fuel_column].eq("GEO")].copy()
    geothermal.to_csv(DATA / "us_geothermal_eia923_2024_rows.csv", index=False)
    net_columns = [column for column in data.columns if column.startswith("Netgen ")]
    summary = {
        "year": 2024, "worksheet": sheet, "header_row_one_based": header + 1,
        "all_rows": len(data), "geothermal_rows": len(geothermal),
        "plants": int(geothermal["Plant Id"].nunique()),
        "monthly_net_generation_columns": net_columns,
        "respondent_frequency_rows": geothermal["Respondent Frequency"].value_counts().to_dict(),
        "prime_mover_rows": geothermal["Reported Prime Mover"].value_counts().to_dict(),
        "nonmissing_monthly_net_generation_cells": int(geothermal[net_columns].apply(pd.to_numeric, errors="coerce").notna().sum().sum()),
        "states": sorted(geothermal["Plant State"].dropna().unique().tolist()),
        "workbook_sheets": workbook.sheet_names,
        "warning": "Rows are plant/prime-mover/fuel combinations, not necessarily individual generators. Join historical EIA-860 capacity and technology; verify M/AM reporting and estimated versus measured monthly values before modeling.",
    }
    (OUTPUT / "eia_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUTPUT / "eia_download_manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("EIA", json.dumps(summary), flush=True)


def audit_bps():
    urls = {
        "lampung_monthly_sales": "https://lampung.bps.go.id/id/statistics-table/2/Mzk4IzI=/listrik-terjual--bulanan-.html",
        "bandar_lampung_monthly_usage": "https://bandarlampungkota.bps.go.id/id/statistics-table/2/MjMwIzI=/besar-pemakaian-listrik-menurut-bulan.html",
    }
    summaries = []
    for name, url in urls.items():
        response = requests.get(url, timeout=45)
        response.raise_for_status()
        html = response.text
        (RAW / "indonesia").mkdir(exist_ok=True)
        (RAW / "indonesia" / f"{name}.html").write_text(html)
        payloads = re.findall(r"self\.__next_f\.push\((\[.*?\])\)</script>", html)
        for payload in payloads:
            item = json.loads(payload)
            if len(item) < 2 or not isinstance(item[1], str) or '"datacontent"' not in item[1]:
                continue
            text = item[1]
            position = text.index('"data":{"status"') + len('"data":')
            data = json.JSONDecoder().raw_decode(text[position:])[0]
            position = text.index('"listTahun":') + len('"listTahun":')
            listed_years = json.JSONDecoder().raw_decode(text[position:])[0]
            (RAW / "indonesia" / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n")
            rows = []
            for year in data["tahun"]:
                for category in data["vervar"]:
                    for variant in data["turvar"]:
                        for period in data["turtahun"]:
                            key = f"{category['val']}{data['var'][0]['val']}{variant['val']}{year['val']}{period['val']}"
                            if key in data["datacontent"]:
                                rows.append({
                                    "year": year["label"], "category": category["label"],
                                    "variant": variant["label"], "period": period["label"],
                                    "value": data["datacontent"][key], "unit": data["var"][0]["unit"],
                                    "source_url": url,
                                })
            if len(rows) != len(data["datacontent"]):
                raise ValueError(f"Unparsed BPS cells for {name}")
            pd.DataFrame(rows).to_csv(DATA / f"{name}.csv", index=False)
            summaries.append({
                "table": name, "url": url, "parsed_cells": len(rows),
                "retrieved_years": data["tahun"], "years_advertised_in_selector": listed_years,
                "note": "Advertised years are not confirmed complete series. Annual-total rows, if present, are not extra months. Province, city and PLN service areas are not interchangeable.",
            })
            break
        else:
            raise ValueError(f"No embedded BPS table in {url}")
    (OUTPUT / "bps_audit.json").write_text(json.dumps(summaries, indent=2) + "\n")
    print("BPS", json.dumps(summaries), flush=True)


def audit_wayang():
    path = DATA / "wayang_windu_monthly_main_meter_2018_2021.csv"
    data = pd.read_csv(path)
    expected = pd.period_range("2018-01", "2021-06", freq="M").astype(str).tolist()
    if data["month"].tolist() != expected:
        raise ValueError("Wayang Windu transcription has unexpected or missing months")
    values = data[["unit_1_reported_mwh", "unit_2_reported_mwh"]]
    if values.isna().any().any() or values.lt(0).any().any():
        raise ValueError("Invalid Wayang Windu monthly transcription")
    summary = {
        "source_url": "https://cdm.unfccc.int/UserManagement/FileStorage/FSK5I6HGV4BJ39YARNEOXZ18Q7MWUP",
        "registry_project": 3193, "source": "Revised v04 monitoring report, Annex 5, printed pages 90-94 of 99",
        "method": "Manual transcription of factual numerical tables retrieved using web PDF extraction; no local PDF binary obtained",
        "months": len(data), "units": 2, "unit_month_values": int(values.size),
        "first_month": data["month"].min(), "last_month": data["month"].max(),
        "source_tables": "Tables labelled Main Meter; reproduce published values including stated meter-error adjustments, not claimed to be raw SCADA",
        "excluded": "December 2017 omitted because monitoring begins December 2; earlier report has a December placeholder zero, not a full month of physical zero output",
        "qa": "Temporal continuity and numeric fields checked. Full reconciliation to daily readings and independent second-person transcription check are not complete. Revised report differs from earlier 93-page report; do not mix versions.",
    }
    (OUTPUT / "wayang_windu_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("Wayang Windu", json.dumps(summary), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["nz", "eia", "bps", "wayang", "all"], default="all")
    parser.add_argument("--start", type=int, default=2024)
    parser.add_argument("--end", type=int, default=2024)
    args = parser.parse_args()
    for directory in [RAW, DATA, OUTPUT]:
        directory.mkdir(parents=True, exist_ok=True)
    if args.source in ["nz", "all"]:
        audit_nz(args.start, args.end)
    if args.source in ["eia", "all"]:
        audit_eia()
    if args.source in ["bps", "all"]:
        audit_bps()
    if args.source in ["wayang", "all"]:
        audit_wayang()


if __name__ == "__main__":
    main()
