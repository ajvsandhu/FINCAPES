"""Illustrative annual energy-balance counterfactual for planned geothermal.

RUPTL does not publish a case without the planned geothermal projects. This
script holds projected electricity supply fixed, removes a bounded amount of
planned geothermal generation, and replaces it with coal and/or gas generation.
It does not simulate hourly dispatch or changes to the capacity build plan.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "geothermal_credit_model/output/planned_geothermal_credit_potential_by_year.csv"
GENERATION = ROOT / "ruptl_eda/output/ruptl_projected_generation.csv"
EMISSIONS = ROOT / "ruptl_eda/output/ruptl_projected_emissions.csv"
OUTPUT = Path(__file__).resolve().parent / "output"


def planned_generation():
    model = pd.read_csv(MODEL)
    chosen = model[
        model["capacity_factor_case"].eq("Central (80%)")
        & model["factor_method"].eq("OM")
    ].copy()
    chosen["planned_unadjusted_gwh"] = chosen["estimated_generation_mwh"] / 1_000
    return chosen[["grid", "analysis_year", "planned_unadjusted_gwh"]].rename(
        columns={"analysis_year": "year"}
    )


def build_counterfactual():
    generation = pd.read_csv(GENERATION)
    emissions = pd.read_csv(EMISSIONS)
    generation = generation.groupby(
        ["grid", "scenario", "year", "fuel"], as_index=False
    )["generation_gwh"].sum()
    generation = generation[generation["fuel"].isin(["Geothermal", "Coal", "Gas"])]
    emissions = emissions[emissions["fuel"].isin(["Coal", "Gas"])]

    years = generation.pivot(
        index=["grid", "scenario", "year"], columns="fuel", values="generation_gwh"
    ).rename(columns={
        "Geothermal": "geothermal_with_gwh",
        "Coal": "coal_with_gwh",
        "Gas": "gas_with_gwh",
    }).reset_index()
    fuel_emissions = emissions.pivot(
        index=["grid", "scenario", "year"], columns="fuel", values="emissions_mtco2"
    ).rename(columns={"Coal": "coal_with_mtco2", "Gas": "gas_with_mtco2"}).reset_index()
    years = years.merge(fuel_emissions, on=["grid", "scenario", "year"], validate="one_to_one")
    years = years.merge(planned_generation(), on=["grid", "year"], validate="many_to_one")

    # Explicit bound: retain at least the projected 2025 geothermal total in
    # every later year and attribute at most the growth above it to planned
    # projects. The 2025 total may include some newly commissioned projects;
    # this is a compatibility rule, not measured project output or dispatch.
    reference = years[years["year"].eq(2025)][["grid", "scenario", "geothermal_with_gwh"]]
    reference = reference.rename(columns={"geothermal_with_gwh": "reference_2025_gwh"})
    years = years.merge(reference, on=["grid", "scenario"], validate="many_to_one")
    available_growth = (years["geothermal_with_gwh"] - years["reference_2025_gwh"]).clip(lower=0)
    years["planned_bounded_gwh"] = years["planned_unadjusted_gwh"].clip(lower=0).combine(
        available_growth, min
    )
    years["bound_applied"] = years["planned_bounded_gwh"] < years["planned_unadjusted_gwh"] - 1e-9
    years["geothermal_without_gwh"] = years["geothermal_with_gwh"] - years["planned_bounded_gwh"]
    years["coal_tco2_per_mwh"] = years["coal_with_mtco2"] * 1_000 / years["coal_with_gwh"]
    years["gas_tco2_per_mwh"] = years["gas_with_mtco2"] * 1_000 / years["gas_with_gwh"]
    years["coal_share_of_coal_gas"] = years["coal_with_gwh"] / (
        years["coal_with_gwh"] + years["gas_with_gwh"]
    )

    cases = {
        "Gas replacement": 0.0,
        "Coal replacement": 1.0,
        "Proportional coal-gas replacement": None,
    }
    rows = []
    for label, coal_share in cases.items():
        case = years.copy()
        case["replacement_case"] = label
        case["replacement_coal_share"] = (
            case["coal_share_of_coal_gas"] if coal_share is None else coal_share
        )
        case["coal_without_gwh"] = (
            case["coal_with_gwh"]
            + case["planned_bounded_gwh"] * case["replacement_coal_share"]
        )
        case["gas_without_gwh"] = (
            case["gas_with_gwh"]
            + case["planned_bounded_gwh"] * (1 - case["replacement_coal_share"])
        )
        case["avoided_mtco2"] = case["planned_bounded_gwh"] * (
            case["replacement_coal_share"] * case["coal_tco2_per_mwh"]
            + (1 - case["replacement_coal_share"]) * case["gas_tco2_per_mwh"]
        ) / 1_000
        rows.append(case)
    annual = pd.concat(rows, ignore_index=True).sort_values(
        ["grid", "scenario", "replacement_case", "year"]
    )

    assert (annual["geothermal_without_gwh"] >= -1e-9).all()
    assert (annual["planned_bounded_gwh"] <= annual["planned_unadjusted_gwh"] + 1e-9).all()
    assert (
        (annual["coal_without_gwh"] + annual["gas_without_gwh"] + annual["geothermal_without_gwh"])
        - (annual["coal_with_gwh"] + annual["gas_with_gwh"] + annual["geothermal_with_gwh"])
    ).abs().max() < 1e-6

    summary = annual.groupby(["grid", "scenario", "replacement_case"], as_index=False).agg(
        planned_unadjusted_gwh=("planned_unadjusted_gwh", "sum"),
        planned_bounded_gwh=("planned_bounded_gwh", "sum"),
        years_bound=("bound_applied", "sum"),
        gross_avoided_mtco2=("avoided_mtco2", "sum"),
    )
    return annual, summary


def main():
    OUTPUT.mkdir(exist_ok=True)
    annual, summary = build_counterfactual()
    annual.to_csv(OUTPUT / "ruptl_counterfactual_by_year.csv", index=False)
    summary.to_csv(OUTPUT / "ruptl_counterfactual_summary.csv", index=False)
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.2f}"))


if __name__ == "__main__":
    main()
