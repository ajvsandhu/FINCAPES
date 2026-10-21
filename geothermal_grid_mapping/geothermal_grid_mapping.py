import sys
from pathlib import Path

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SITES_FILE = ROOT / "genesis_geothermal_eda" / "output" / "genesis_geothermal_sites.csv"
UNITS_FILE = ROOT / "genesis_geothermal_eda" / "output" / "genesis_planned_unit_additions.csv"
GRIDS_FILE = ROOT / "esdm_grid_factors_eda" / "data" / "esdm_grid_emission_factors_2019.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"

STUDY_GRIDS = ["Jamali", "Sumatera"]
JAMALI_PROVINCES = {"BANTEN", "DKI JAKARTA", "JAWA BARAT", "JAWA TENGAH", "DI YOGYAKARTA", "JAWA TIMUR", "BALI"}
SUMATERA_PROVINCES = {
    "ACEH", "BENGKULU", "JAMBI", "LAMPUNG", "RIAU",
    "SUMATERA BARAT", "SUMATERA SELATAN", "SUMATERA UTARA",
}

# Site-level exceptions to the province rule, with the source that settles each one.
SITE_OVERRIDES = {
    "Jaboi": (
        "Sabang (isolated)", "high",
        "On Weh island (Kota Sabang); RUPTL 2025-2034 Aceh annex lists PLTP Jaboi under the isolated 20 kV "
        "Sistem Sabang. The 2019 decree has no Sabang row",
    ),
    "Bedugul": (
        "Jamali", "high",
        "RUPTL 2025-2034 plans Bali within Sistem Jawa-Bali, and the JCM grid note (Table 2) lists Bali under Jamali; "
        "the 2019 decree's province list omits Bali",
    ),
    "Samosir": (
        "Sumatera", "high",
        "RUPTL 2025-2034 North Sumatra annex: existing 150 kV substation at Pangururan on Samosir island",
    ),
    "Sungai Penuh": (
        "Sumatera", "high",
        "RUPTL 2025-2034 Jambi annex: existing 150/20 kV substation at Sungai Penuh (Kerinci)",
    ),
    "Graho Nyabu": (
        "Sumatera", "high",
        "Kerinci/Merangin; RUPTL 2025-2034 Jambi annex: existing 150/20 kV substations at Sungai Penuh and Bangko",
    ),
    "Koto Sani Tanjung Bingkung": (
        "Sumatera", "medium",
        "Province (Sumatera Barat) used because the GENESIS longitude (0.59) is wrong",
    ),
}


def province_grid(province):
    if province in JAMALI_PROVINCES:
        return "Jamali"
    if province in SUMATERA_PROVINCES:
        return "Sumatera"
    return "Other"


def load():
    for path in (SITES_FILE, UNITS_FILE, GRIDS_FILE):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the GENESIS and ESDM EDA scripts first.")
    return pd.read_csv(SITES_FILE), pd.read_csv(UNITS_FILE), pd.read_csv(GRIDS_FILE)


def map_sites(sites):
    mapped = sites[["id", "nama_pltp", "status", "provinsi_nama", "kota_nama", "latitude", "longitude",
                    "kapasitas_terpasang", "rencana_pengembangan"]].copy()
    mapped["grid_by_province"] = mapped["provinsi_nama"].map(province_grid)
    mapped["grid_checked"] = mapped["grid_by_province"]
    mapped["confidence"] = mapped["grid_by_province"].map(lambda g: "high" if g in STUDY_GRIDS else "not checked")
    mapped["reason"] = mapped["grid_by_province"].map(
        lambda g: f"Mainland site in a province served by the {g} grid" if g in STUDY_GRIDS
        else "Outside Jamali and Sumatera; served by a smaller regional or island grid"
    )
    for name, (grid, confidence, reason) in SITE_OVERRIDES.items():
        row = mapped["nama_pltp"] == name
        if not row.any():
            print(f"Warning: override for '{name}' matches no GENESIS site")
        mapped.loc[row, ["grid_checked", "confidence", "reason"]] = [grid, confidence, reason]
    return mapped


def coverage(mapped, grid_column):
    totals = mapped[["kapasitas_terpasang", "rencana_pengembangan"]].sum()
    rows = []
    for grid in STUDY_GRIDS + ["Both study grids"]:
        grids = STUDY_GRIDS if grid == "Both study grids" else [grid]
        part = mapped[mapped[grid_column].isin(grids)]
        rows.append({
            "grid": grid,
            "sites": len(part),
            "installed_mw": round(part["kapasitas_terpasang"].sum(), 1),
            "installed_share_pct": round(100 * part["kapasitas_terpasang"].sum() / totals["kapasitas_terpasang"], 1),
            "planned_mw": round(part["rencana_pengembangan"].sum(), 1),
            "planned_share_pct": round(100 * part["rencana_pengembangan"].sum() / totals["rencana_pengembangan"], 1),
        })
    return pd.DataFrame(rows)


def planned_by_year(mapped, units):
    units = units.merge(mapped[["id", "grid_checked"]], left_on="pltp_id", right_on="id", how="left")
    if units["grid_checked"].isna().any():
        print(f"Warning: {units['grid_checked'].isna().sum()} planned units do not match a site")
    table = units.pivot_table(index="tahun", columns="grid_checked", values="kapasitas_tambahan_mw",
                              aggfunc="sum", fill_value=0)
    table["Total"] = table.sum(axis=1)
    return table.round(1)


def print_section(title):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    sites, units, grids = load()
    mapped = map_sites(sites)

    print_section("ESDM 2019 factors for the study grids (tCO2/MWh)")
    print(grids[grids["grid"].isin(STUDY_GRIDS)][
        ["grid", "province", "num_plants", "om_tco2_per_mwh", "bm_tco2_per_mwh", "cm_expost_50_50", "cm_exante_50_50"]
    ].to_string(index=False))

    print_section("Sites checked individually")
    flagged = mapped["nama_pltp"].isin(SITE_OVERRIDES)
    print(mapped.loc[flagged, ["nama_pltp", "provinsi_nama", "kapasitas_terpasang", "rencana_pengembangan",
                               "grid_by_province", "grid_checked", "confidence", "reason"]].to_string(index=False))

    print_section("Coverage, province rule")
    by_province = coverage(mapped, "grid_by_province")
    print(by_province.to_string(index=False))
    print_section("Coverage, site-checked mapping")
    checked = coverage(mapped, "grid_checked")
    print(checked.to_string(index=False))
    high_only = mapped.assign(grid_high=mapped["grid_checked"].where(mapped["confidence"] == "high", "Unconfirmed"))
    print_section("Coverage, high-confidence sites only (lower bound)")
    lower = coverage(high_only, "grid_high")
    print(lower.to_string(index=False))

    print_section("Planned additions by year and grid (MW, site-checked mapping)")
    by_year = planned_by_year(mapped, units)
    print(by_year.to_string())

    print_section("Geothermal outside the study grids")
    other = mapped[~mapped["grid_checked"].isin(STUDY_GRIDS)]
    print(other.groupby("provinsi_nama")[["kapasitas_terpasang", "rencana_pengembangan"]].sum()
          .sort_values("rencana_pengembangan", ascending=False).to_string())

    mapped.to_csv(OUTPUT_DIR / "site_grid_mapping.csv", index=False)
    pd.concat([
        by_province.assign(mapping="province rule"),
        checked.assign(mapping="site-checked"),
        lower.assign(mapping="high-confidence only"),
    ]).to_csv(OUTPUT_DIR / "coverage_summary.csv", index=False)
    by_year.to_csv(OUTPUT_DIR / "planned_additions_by_grid_year.csv")
    print(f"\nSaved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
