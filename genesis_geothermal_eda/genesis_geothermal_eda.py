import sys
import time
import webbrowser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests


BASE_URL = "https://genesis.ebtke.esdm.go.id/api/api"
# GENESIS shows this date on its home page but does not include it in the data feed; update it if the site changes.
CAPACITY_AS_OF = "1 September 2025"
UNIT_YEARS = range(2000, 2051)
INDONESIA_LAT = (-11.5, 6.5)
INDONESIA_LON = (94.5, 141.5)
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"

STATUS_ENGLISH = {
    "Produksi": "Production",
    "Eksploitasi": "Exploitation (development)",
    "Eksplorasi": "Exploration",
    "PSPE": "Preliminary survey and exploration assignment",
    "Wilayah Terbuka": "Open area (not yet awarded)",
}
STATUS_COLOURS = {
    "Produksi": "tab:red",
    "Eksploitasi": "tab:orange",
    "Eksplorasi": "tab:blue",
    "PSPE": "tab:green",
    "Wilayah Terbuka": "tab:gray",
}

DATA_DICTIONARY = pd.DataFrame(
    [
        ("sites", "id", "number", "", "GENESIS site ID"),
        ("sites", "nama_pltp", "text", "", "Geothermal power plant (PLTP) or site name"),
        ("sites", "nama_badan_usaha", "text", "", "Developer / operating company; often blank"),
        ("sites", "kapasitas_terpasang", "number", "MW", "Installed capacity today"),
        ("sites", "rencana_pengembangan", "number", "MW", "Planned additional capacity in PLN's 2025-2034 electricity plan (RUPTL)"),
        ("sites", "latitude", "number", "degrees", "Site latitude"),
        ("sites", "longitude", "number", "degrees", "Site longitude"),
        ("sites", "status", "text", "", "Development stage: " + "; ".join(f"{k} = {v}" for k, v in STATUS_ENGLISH.items())),
        ("sites", "icon_placemark", "text", "", "Path of the map icon image on the GENESIS server"),
        ("sites", "dokumen_pendukung", "text", "", "Path of a supporting PDF on the GENESIS server, if any"),
        ("sites", "jarak", "number", "", "Distance value the GENESIS map uses to order sites; reference point not documented"),
        ("sites", "encrypt_id", "text", "", "Encrypted site ID used internally by GENESIS"),
        ("sites", "provinsi_kode", "text", "", "Province code (flattened from the nested provinsi field)"),
        ("sites", "provinsi_nama", "text", "", "Province name"),
        ("sites", "kota_kode", "text", "", "Regency/city codes the site spans, separated by ';'"),
        ("sites", "kota_nama", "text", "", "Regency/city names the site spans, separated by ';'"),
        ("planned units", "id", "number", "", "GENESIS ID of the planned unit"),
        ("planned units", "pltp_id", "number", "", "Site ID the unit belongs to (matches sites.id)"),
        ("planned units", "nama_unit", "text", "", "Unit name, e.g. Unit 1"),
        ("planned units", "tahun", "number", "year", "Year the unit is planned to come online"),
        ("planned units", "kapasitas_tambahan_mw", "number", "MW", "Capacity the unit adds"),
        ("planned units", "keterangan", "text", "", "Notes; mostly blank or the text 'null'"),
        ("planned units", "created_at / updated_at", "text", "", "When the record was created / last updated in GENESIS"),
        ("planned units", "nama_pltp / nama_badan_usaha", "text", "", "Site name and developer, joined from the sites table by GENESIS"),
        ("planned units", "encrypted_id / DT_RowIndex", "text", "", "Internal ID and table row number used by the GENESIS website"),
        ("capacity outlook", "tahun", "number", "year", "Year"),
        ("capacity outlook", "kapasitas_tambahan_mw", "number", "MW", "Capacity added in the year"),
        ("capacity outlook", "kapasitas_terpasang_mw", "number", "MW", "Cumulative installed capacity at the end of the year"),
        ("planned by region", "region / label / provinsi", "text", "", "Region key, display name and provinces it covers"),
        ("planned by region", "mw", "number", "MW", "Planned additional capacity in the region"),
        ("planned by region", "proyek", "number", "", "Number of planned projects in the region"),
        ("planned by period", "periode", "text", "", "Planning period"),
        ("planned by period", "total_mw", "number", "MW", "Planned additional capacity in the period"),
    ],
    columns=["table", "field", "type", "unit", "meaning"],
)


def post(endpoint, payload, attempts=3):
    for attempt in range(1, attempts + 1):
        try:
            response = requests.post(f"{BASE_URL}/{endpoint}", json=payload, timeout=60)
            break
        except requests.RequestException as error:
            if attempt == attempts:
                raise RuntimeError(f"GENESIS request to {endpoint} failed: {error}") from None
            time.sleep(2 * attempt)
    if response.status_code != 200:
        raise RuntimeError(f"GENESIS returned {response.status_code} for {endpoint}: {response.text[:300]}")
    return response.json()


def fetch_landing():
    response = post("landing-data/spasial-pltp", {})["response"]

    sites = pd.DataFrame(response["pltp"])
    location = sites.pop("provinsi").map(lambda provinces: provinces[0] if provinces else {})
    sites["provinsi_kode"] = location.map(lambda p: p.get("kode_provinsi"))
    sites["provinsi_nama"] = location.map(lambda p: p.get("nama_provinsi"))
    sites["kota_kode"] = location.map(lambda p: "; ".join(k["kode_kota"] for k in p.get("kota", [])))
    sites["kota_nama"] = location.map(lambda p: "; ".join(k["nama_kota"] for k in p.get("kota", [])))
    numeric = ["kapasitas_terpasang", "rencana_pengembangan", "latitude", "longitude", "jarak"]
    sites[numeric] = sites[numeric].apply(pd.to_numeric)

    chart = response["chart"]
    outlook = pd.DataFrame({"tahun": pd.to_numeric(chart["categories"])})
    for series in chart["series"]:
        column = "kapasitas_tambahan_mw" if "Tambahan" in series["name"] else "kapasitas_terpasang_mw"
        outlook[column] = pd.to_numeric(series["data"])

    regions = pd.DataFrame(response["summary"])
    regions.insert(0, "region", regions.pop("key").fillna(regions.pop("name")))
    regions["provinsi"] = regions["provinsi"].map("; ".join)
    regions = regions.drop(columns=["center", "zoom"])
    periods = pd.DataFrame(response["kapasitas_summary"])
    return sites, outlook, regions, periods


def fetch_units():
    def year_units(year):
        payload = {"start": 0, "length": 10000, "search": "", "tahun": year}
        return post("landing-data/kapasitas-pltp/get-unit-by-year", payload)["data"]

    rows = [row for year in UNIT_YEARS for row in year_units(year)]
    units = pd.DataFrame(rows)
    units["kapasitas_tambahan_mw"] = pd.to_numeric(units["kapasitas_tambahan_mw"])
    return units.sort_values(["tahun", "nama_pltp", "nama_unit"]).reset_index(drop=True)


def print_section(title):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def describe(tables):
    for name, data in tables.items():
        print_section(f"{name}: shape and missing values")
        print(f"Rows: {data.shape[0]}, columns: {data.shape[1]}")
        print(data.isna().sum().to_string())


def check(sites, units, outlook, regions, periods):
    print_section("Duplicates")
    print(f"Duplicate site IDs: {sites['id'].duplicated().sum()}, duplicate site names: {sites['nama_pltp'].duplicated().sum()}")
    print(f"Duplicate planned unit IDs: {units['id'].duplicated().sum()}")

    print_section("Consistency checks (MW)")
    installed = sites["kapasitas_terpasang"].sum()
    planned_sites = sites["rencana_pengembangan"].sum()
    planned_units = units["kapasitas_tambahan_mw"].sum()
    outlook_base = outlook["kapasitas_terpasang_mw"].iloc[0] - outlook["kapasitas_tambahan_mw"].iloc[0]
    region_total = regions.loc[regions["region"] == "total", "mw"].sum()
    print(f"Installed capacity, sum of sites:              {installed:,.2f}")
    print(f"Installed capacity before 2025, from outlook:  {outlook_base:,.2f}")
    print(f"Planned capacity, sum of sites:                {planned_sites:,.2f}")
    print(f"Planned capacity, sum of planned units:        {planned_units:,.2f}")
    print(f"Planned capacity, sum of outlook additions:    {outlook['kapasitas_tambahan_mw'].sum():,.2f}")
    print(f"Planned capacity, regional summary total:      {region_total:,.2f}")
    print(f"Planned capacity, regional summary by region:  {regions.loc[regions['region'] != 'total', 'mw'].sum():,.2f}")
    print(f"Planned capacity, sum of periods:              {periods['total_mw'].sum():,.2f}")
    running = outlook_base + outlook["kapasitas_tambahan_mw"].cumsum()
    print(f"Outlook years where installed != previous + added: {int(((running - outlook['kapasitas_terpasang_mw']).abs() > 0.01).sum())}")

    per_site = units.groupby("pltp_id")["kapasitas_tambahan_mw"].sum()
    compare = sites.set_index("id")[["nama_pltp", "rencana_pengembangan"]].join(per_site.rename("sum_of_units"))
    compare["sum_of_units"] = compare["sum_of_units"].fillna(0)
    mismatched = compare[(compare["rencana_pengembangan"] - compare["sum_of_units"]).abs() > 0.01]
    print(f"Sites whose planned MW differs from the sum of their planned units: {len(mismatched)}")
    if not mismatched.empty:
        print(mismatched.to_string())
    orphans = units[~units["pltp_id"].isin(sites["id"])]
    print(f"Planned units that point to a site not in the sites table: {len(orphans)}")

    print_section("Data quality flags")
    bad_coordinates = sites[
        ~sites["latitude"].between(*INDONESIA_LAT) | ~sites["longitude"].between(*INDONESIA_LON)
    ]
    print(f"Sites with coordinates outside Indonesia: {len(bad_coordinates)}")
    if not bad_coordinates.empty:
        print(bad_coordinates[["nama_pltp", "provinsi_nama", "latitude", "longitude"]].to_string(index=False))
    print(f"Sites with no developer name: {sites['nama_badan_usaha'].isna().sum()} of {len(sites)}")
    not_producing = sites[(sites["kapasitas_terpasang"] > 0) & (sites["status"] != "Produksi")]
    print(f"Sites with installed capacity but status other than Produksi: {len(not_producing)}")
    if not not_producing.empty:
        print(not_producing[["nama_pltp", "status", "kapasitas_terpasang"]].to_string(index=False))
    null_text = (units["keterangan"] == "null").sum()
    print(f"Planned unit notes containing the text 'null' instead of being blank: {null_text}")


def summarise(sites, units):
    print_section("Sites and capacity by status")
    by_status = (
        sites.groupby("status")
        .agg(sites=("id", "size"), installed_mw=("kapasitas_terpasang", "sum"), planned_mw=("rencana_pengembangan", "sum"))
        .sort_values("installed_mw", ascending=False)
    )
    by_status.insert(0, "status_english", by_status.index.map(STATUS_ENGLISH))
    print(by_status.round(2).to_string())

    print_section("Capacity by province (MW)")
    by_province = (
        sites.groupby("provinsi_nama")
        .agg(sites=("id", "size"), installed_mw=("kapasitas_terpasang", "sum"), planned_mw=("rencana_pengembangan", "sum"))
        .sort_values(["installed_mw", "planned_mw"], ascending=False)
    )
    print(by_province.round(2).to_string())

    print_section("Producing sites by installed capacity (MW)")
    producing = sites[sites["kapasitas_terpasang"] > 0].sort_values("kapasitas_terpasang", ascending=False)
    print(producing[["nama_pltp", "provinsi_nama", "status", "kapasitas_terpasang", "rencana_pengembangan"]].to_string(index=False))

    print_section("Planned additions by year (MW)")
    print(units.groupby("tahun").agg(units=("id", "size"), added_mw=("kapasitas_tambahan_mw", "sum")).to_string())
    return by_status, by_province


def plot_installed_by_site(sites):
    producing = sites[sites["kapasitas_terpasang"] > 0].sort_values("kapasitas_terpasang")
    fig, ax = plt.subplots(figsize=(11, 0.45 * len(producing) + 1.5))
    bars = ax.barh(producing["nama_pltp"], producing["kapasitas_terpasang"], color="tab:red")
    ax.bar_label(bars, labels=[f"{v:,.1f}" for v in producing["kapasitas_terpasang"]], padding=3, fontsize=8)
    ax.set_xlabel("Installed capacity (MW)")
    ax.set_ylabel("Geothermal site")
    ax.set_xlim(0, producing["kapasitas_terpasang"].max() * 1.15)
    ax.set_title(
        f"Installed geothermal capacity by site (GENESIS), total {sites['kapasitas_terpasang'].sum():,.2f} MW\n"
        f"as of {CAPACITY_AS_OF} (GENESIS last update)"
    )
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "installed_capacity_by_site.png", dpi=150)
    plt.close(fig)


def plot_outlook(outlook):
    last_addition = outlook.loc[outlook["kapasitas_tambahan_mw"] > 0, "tahun"].max()
    outlook = outlook[outlook["tahun"] <= last_addition]
    first_year = outlook["tahun"].min()
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(outlook["tahun"], outlook["kapasitas_tambahan_mw"], color="tab:orange", label="Capacity added in year")
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in outlook["kapasitas_tambahan_mw"]], padding=2, fontsize=8)
    ax.plot(outlook["tahun"], outlook["kapasitas_terpasang_mw"], marker="o", color="tab:red", label="Cumulative installed capacity")
    for year, value in zip(outlook["tahun"], outlook["kapasitas_terpasang_mw"]):
        ax.annotate(f"{value:,.0f}", (year, value), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Capacity (MW)")
    ax.set_xticks(outlook["tahun"])
    ax.set_ylim(0, outlook["kapasitas_terpasang_mw"].max() * 1.15)
    ax.set_title(f"Planned geothermal capacity {first_year}-{last_addition}, PLN electricity plan (RUPTL) (GENESIS)")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f"capacity_outlook_{first_year}_{last_addition}.png", dpi=150)
    plt.close(fig)


def plot_by_province(by_province, units):
    plan_years = f"{units['tahun'].min()}-{units['tahun'].max()}"
    data = by_province.sort_values("installed_mw")
    positions = range(len(data))
    fig, ax = plt.subplots(figsize=(12, 0.5 * len(data) + 1.5))
    installed = ax.barh([p + 0.2 for p in positions], data["installed_mw"], height=0.4, color="tab:red",
                        label=f"Installed (in operation as of {CAPACITY_AS_OF})")
    planned = ax.barh([p - 0.2 for p in positions], data["planned_mw"], height=0.4, color="tab:orange",
                      label=f"Planned additions {plan_years}")
    ax.bar_label(installed, labels=[f"{v:,.0f}" for v in data["installed_mw"]], padding=3, fontsize=8)
    ax.bar_label(planned, labels=[f"{v:,.0f}" for v in data["planned_mw"]], padding=3, fontsize=8)
    ax.set_yticks(list(positions), data.index.str.title())
    ax.set_xlabel("Capacity (MW)")
    ax.set_ylabel("Province")
    ax.set_xlim(0, max(data["installed_mw"].max(), data["planned_mw"].max()) * 1.15)
    ax.set_title(
        "Installed and planned geothermal capacity by province (GENESIS)\n"
        f"installed as of {CAPACITY_AS_OF} (GENESIS last update)"
    )
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "capacity_by_province.png", dpi=150)
    plt.close(fig)


def plot_map(sites):
    located = sites[sites["latitude"].between(*INDONESIA_LAT) & sites["longitude"].between(*INDONESIA_LON)]
    fig, ax = plt.subplots(figsize=(14, 6.5))
    for status, group in located.groupby("status"):
        size = 20 + (group["kapasitas_terpasang"] + group["rencana_pengembangan"]) * 0.8
        ax.scatter(group["longitude"], group["latitude"], s=size, alpha=0.7, color=STATUS_COLOURS.get(status),
                   edgecolor="black", linewidth=0.5, label=f"{status} ({STATUS_ENGLISH.get(status, status)})")
    labelled = located[located["kapasitas_terpasang"] >= 100].sort_values("longitude")
    offsets = [(8, 10), (8, -16), (-10, 26), (-10, -32), (20, 40), (20, -46)]
    for i, (_, site) in enumerate(labelled.iterrows()):
        ax.annotate(site["nama_pltp"], (site["longitude"], site["latitude"]), textcoords="offset points",
                    xytext=offsets[i % len(offsets)], fontsize=8,
                    arrowprops={"arrowstyle": "-", "color": "gray", "linewidth": 0.5})
    ax.set_xlabel("Longitude (degrees east)")
    ax.set_ylabel("Latitude (degrees)")
    ax.set_xlim(*INDONESIA_LON)
    ax.set_ylim(*INDONESIA_LAT)
    ax.set_title(
        "Geothermal sites in GENESIS (marker size = installed + planned MW; labels = sites with 100 MW or more installed)\n"
        f"installed as of {CAPACITY_AS_OF} (GENESIS last update)"
    )
    ax.legend(loc="lower left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "sites_map.png", dpi=150)
    plt.close(fig)


def html_table(data, index=False):
    return f'<div class="scroll">{data.to_html(index=index, na_rep="")}</div>'


def show_data(tables, by_status, by_province):
    sections = [f"<h2>{name} ({data.shape[0]} rows x {data.shape[1]} columns)</h2>{html_table(data)}" for name, data in tables.items()]
    sections.append(f"<h2>Sites and capacity by status</h2>{html_table(by_status.round(2), index=True)}")
    sections.append(f"<h2>Capacity by province</h2>{html_table(by_province.round(2), index=True)}")
    sections.append(f"<h2>Data dictionary</h2>{html_table(DATA_DICTIONARY)}")
    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>GENESIS geothermal capacity data</title>
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
<h1>GENESIS geothermal capacity data (Indonesia, Directorate of Geothermal, EBTKE, ESDM)</h1>
{"".join(sections)}
</body>
</html>"""
    html_file = OUTPUT_DIR / "genesis_geothermal_data.html"
    html_file.write_text(page)
    webbrowser.open(html_file.as_uri())
    print(f"Opened in your browser: {html_file}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    try:
        sites, outlook, regions, periods = fetch_landing()
        units = fetch_units()
    except RuntimeError as error:
        sys.exit(str(error))

    tables = {
        "Geothermal sites": sites,
        "Planned unit additions": units,
        "Capacity outlook 2025-2034": outlook,
        "Planned capacity by region": regions,
        "Planned capacity by period": periods,
    }
    sites.to_csv(OUTPUT_DIR / "genesis_geothermal_sites.csv", index=False)
    units.to_csv(OUTPUT_DIR / "genesis_planned_unit_additions.csv", index=False)
    outlook.to_csv(OUTPUT_DIR / "genesis_capacity_outlook.csv", index=False)
    regions.to_csv(OUTPUT_DIR / "genesis_planned_capacity_by_region.csv", index=False)
    periods.to_csv(OUTPUT_DIR / "genesis_planned_capacity_by_period.csv", index=False)
    DATA_DICTIONARY.to_csv(OUTPUT_DIR / "data_dictionary.csv", index=False)
    print(f"Saved GENESIS data to {OUTPUT_DIR}/")

    describe(tables)
    check(sites, units, outlook, regions, periods)
    by_status, by_province = summarise(sites, units)
    show_data(tables, by_status, by_province)

    plot_installed_by_site(sites)
    plot_outlook(outlook)
    plot_by_province(by_province, units)
    plot_map(sites)
    print(f"\nPlots saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
