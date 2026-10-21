"""Estimate gross avoided-emissions potential from planned Indonesian geothermal capacity.

This is a scenario model, not a carbon-credit issuance calculation.  It estimates
generation from GENESIS planned capacity, then multiplies it by alternative grid
emission factors.  It does not establish additionality, eligibility, verification,
project emissions, leakage, or the number of credits actually issuable.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
MAPPING_FILE = ROOT / "geothermal_grid_mapping" / "output" / "planned_additions_by_grid_year.csv"
ESDM_FILE = ROOT / "grid_data_sources" / "output" / "esdm_factors_2017_2019_study_grids.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

GRIDS = ["Jamali", "Sumatera"]
YEARS = range(2025, 2035)
COMMISSIONING_LAG_YEARS = 1
CAPACITY_FACTORS = {
    "Low (70%)": 0.70,
    "Central (80%)": 0.80,
    "High (90%)": 0.90,
}
JCM_FACTORS = {"Jamali": 0.619, "Sumatera": 0.458}


def factor_methods():
    """Return 2019 ESDM alternatives plus the separate JCM alternative."""
    esdm = pd.read_csv(ESDM_FILE)
    esdm = esdm[esdm["data_year"].eq(2019) & esdm["grid"].isin(GRIDS)]
    columns = {
        "OM": "om_tco2_per_mwh",
        "BM": "bm_tco2_per_mwh",
        "CM ex-post 50/50": "cm_expost_50_50",
        "CM ex-ante 50/50": "cm_exante_50_50",
    }
    rows = []
    for _, item in esdm.iterrows():
        for method, column in columns.items():
            rows.append({"grid": item["grid"], "factor_method": method,
                         "factor_tco2_per_mwh": item[column], "factor_source": "ESDM 2019"})
    rows.extend({"grid": grid, "factor_method": "JCM alternative",
                 "factor_tco2_per_mwh": factor, "factor_source": "JCM Indonesia grid note (2016-2018)"}
                for grid, factor in JCM_FACTORS.items())
    return pd.DataFrame(rows)


def planned_capacity():
    additions = pd.read_csv(MAPPING_FILE).rename(columns={"tahun": "commissioning_year"})
    data = additions.melt(id_vars="commissioning_year", value_vars=GRIDS,
                          var_name="grid", value_name="capacity_added_mw")
    data = data[data["commissioning_year"].isin(YEARS)].copy()
    data["generation_start_year"] = data["commissioning_year"] + COMMISSIONING_LAG_YEARS
    return data.sort_values(["grid", "commissioning_year"])


def build_model():
    capacity = planned_capacity()
    factors = factor_methods()
    rows = []
    for grid in GRIDS:
        cohorts = capacity[capacity["grid"].eq(grid)]
        for analysis_year in YEARS:
            operating_mw = cohorts.loc[
                cohorts["generation_start_year"].le(analysis_year), "capacity_added_mw"
            ].sum()
            for capacity_factor_name, capacity_factor in CAPACITY_FACTORS.items():
                generation_mwh = operating_mw * 8760 * capacity_factor
                for _, factor in factors[factors["grid"].eq(grid)].iterrows():
                    rows.append({
                        "grid": grid,
                        "analysis_year": analysis_year,
                        "capacity_factor_case": capacity_factor_name,
                        "capacity_factor": capacity_factor,
                        "operating_planned_capacity_mw": operating_mw,
                        "estimated_generation_mwh": generation_mwh,
                        "factor_method": factor["factor_method"],
                        "factor_tco2_per_mwh": factor["factor_tco2_per_mwh"],
                        "factor_source": factor["factor_source"],
                        "gross_avoided_emissions_tco2": generation_mwh * factor["factor_tco2_per_mwh"],
                    })
    return pd.DataFrame(rows)


def make_chart(summary):
    central = summary[summary["capacity_factor_case"].eq("Central (80%)")]
    methods = ["OM", "BM", "CM ex-post 50/50", "CM ex-ante 50/50", "JCM alternative"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, grid in zip(axes, GRIDS):
        data = central[central["grid"].eq(grid)].set_index("factor_method").reindex(methods)
        bars = ax.bar(data.index, data["gross_avoided_emissions_tco2"] / 1_000_000, color="#287d8e")
        ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=9)
        ax.set_title(grid)
        ax.set_ylabel("2025-2034 gross avoided emissions (MtCO2)")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(axis="y", alpha=0.3)
    fig.suptitle("Planned geothermal capacity: sensitivity to emission-factor method\nCentral capacity-factor case (80%); generation begins one year after planned commissioning")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUTPUT_DIR / "factor_method_sensitivity.png", dpi=180)
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    model = build_model()
    summary = (model.groupby(["grid", "capacity_factor_case", "factor_method", "factor_tco2_per_mwh"], as_index=False)
               .agg(operating_capacity_mw_2034=("operating_planned_capacity_mw", "last"),
                    estimated_generation_mwh=("estimated_generation_mwh", "sum"),
                    gross_avoided_emissions_tco2=("gross_avoided_emissions_tco2", "sum")))
    model.to_csv(OUTPUT_DIR / "planned_geothermal_credit_potential_by_year.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "planned_geothermal_credit_potential_summary.csv", index=False)
    factor_methods().to_csv(OUTPUT_DIR / "emission_factor_methods.csv", index=False)
    planned_capacity().to_csv(OUTPUT_DIR / "planned_geothermal_capacity_cohorts.csv", index=False)
    make_chart(summary)
    print(summary.to_string(index=False, float_format="{:.0f}".format))


if __name__ == "__main__":
    main()
