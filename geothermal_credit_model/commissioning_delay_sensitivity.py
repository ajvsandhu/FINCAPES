"""Isolate additional commissioning delays without altering the original model."""

import hashlib
import json
import platform
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

from geothermal_credit_model import (
    CAPACITY_FACTORS, COMMISSIONING_LAG_YEARS, ESDM_FILE, GRIDS,
    MAPPING_FILE, OUTPUT_DIR, ROOT, YEARS, build_model, factor_methods,
    planned_capacity,
)

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT = OUTPUT_DIR / "commissioning_delay"
CENTRAL_CF = CAPACITY_FACTORS["Central (80%)"]
HOURS = 8760
DELAYS = {0: "Current schedule", 1: "Additional 1-year delay", 2: "Additional 2-year delay"}
METHODS = ["OM", "BM", "CM ex-post 50/50", "CM ex-ante 50/50", "JCM alternative"]
KEYS = ["grid", "additional_delay_years", "factor_method"]
QUANTITIES = ["estimated_generation_mwh", "gross_avoided_emissions_tco2"]


def build_delay_scenarios():
    original = planned_capacity()
    cohorts = pd.concat([
        original.assign(
            additional_delay_years=delay,
            schedule_case=label,
            delayed_commissioning_year=original["commissioning_year"] + delay,
            generation_start_year=original["commissioning_year"] + delay + COMMISSIONING_LAG_YEARS,
        )
        for delay, label in DELAYS.items()
    ], ignore_index=True)
    cohorts["full_generation_years_in_window"] = (
        max(YEARS) - cohorts["generation_start_year"].clip(lower=min(YEARS)) + 1
    ).clip(lower=0)
    cohorts["starts_after_window"] = cohorts["generation_start_year"].gt(max(YEARS))
    cohorts["estimated_generation_mwh"] = (
        cohorts["capacity_added_mw"] * HOURS * CENTRAL_CF
        * cohorts["full_generation_years_in_window"]
    )
    rows = []
    for (grid, delay), group in cohorts.groupby(["grid", "additional_delay_years"]):
        for year in YEARS:
            operating = group.loc[group["generation_start_year"].le(year), "capacity_added_mw"].sum()
            rows.append({
                "grid": grid, "additional_delay_years": delay,
                "schedule_case": DELAYS[delay], "analysis_year": year,
                "capacity_factor": CENTRAL_CF, "hours_per_year": HOURS,
                "operating_planned_capacity_mw": operating,
                "estimated_generation_mwh": operating * HOURS * CENTRAL_CF,
            })
    generation = pd.DataFrame(rows).sort_values(["grid", "additional_delay_years", "analysis_year"])
    generation["cumulative_generation_mwh"] = generation.groupby(
        ["grid", "additional_delay_years"]
    )["estimated_generation_mwh"].cumsum()
    annual = generation.merge(factor_methods(), on="grid", validate="many_to_many")
    annual = annual.sort_values(KEYS + ["analysis_year"]).reset_index(drop=True)
    annual["gross_avoided_emissions_tco2"] = (
        annual["estimated_generation_mwh"] * annual["factor_tco2_per_mwh"]
    )
    annual["cumulative_gross_avoided_emissions_tco2"] = annual.groupby(KEYS)[
        "gross_avoided_emissions_tco2"
    ].cumsum()
    for quantity in QUANTITIES + ["cumulative_generation_mwh", "cumulative_gross_avoided_emissions_tco2"]:
        reference = annual.loc[annual["additional_delay_years"].eq(0),
                               ["grid", "analysis_year", "factor_method", quantity]]
        reference_name = f"current_schedule_{quantity}"
        annual = annual.merge(reference.rename(columns={quantity: reference_name}),
                              on=["grid", "analysis_year", "factor_method"], validate="many_to_one")
        annual[f"reduction_{quantity}"] = annual[reference_name] - annual[quantity]
        annual[f"reduction_pct_{quantity}"] = (
            100 * annual[f"reduction_{quantity}"] / annual[reference_name].replace(0, np.nan)
        )
    summary = annual.groupby(KEYS + ["schedule_case", "factor_tco2_per_mwh", "factor_source"],
                             as_index=False).agg(
        operating_capacity_mw_2034=("operating_planned_capacity_mw", "last"),
        estimated_generation_mwh=("estimated_generation_mwh", "sum"),
        gross_avoided_emissions_tco2=("gross_avoided_emissions_tco2", "sum"),
        current_schedule_estimated_generation_mwh=("current_schedule_estimated_generation_mwh", "sum"),
        current_schedule_gross_avoided_emissions_tco2=("current_schedule_gross_avoided_emissions_tco2", "sum"),
    )
    for quantity in QUANTITIES:
        summary[f"reduction_{quantity}"] = summary[f"current_schedule_{quantity}"] - summary[quantity]
        summary[f"reduction_pct_{quantity}"] = (
            100 * summary[f"reduction_{quantity}"] / summary[f"current_schedule_{quantity}"]
        )
    boundary = cohorts.assign(capacity_starting_after_window_mw=lambda data: data["capacity_added_mw"].where(
        data["starts_after_window"], 0
    )).groupby(["grid", "additional_delay_years"], as_index=False).agg(
        original_planned_capacity_mw=("capacity_added_mw", "sum"),
        capacity_starting_after_window_mw=("capacity_starting_after_window_mw", "sum"),
    )
    summary = summary.merge(boundary, on=["grid", "additional_delay_years"], validate="many_to_one")
    return cohorts, generation, annual, summary


def validate(cohorts, generation, annual, summary):
    checks = []

    def record(name, condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append({"check": name, "passed": True})

    def close(actual, expected):
        return np.allclose(actual, expected, rtol=0, atol=1e-7)

    original = planned_capacity()
    record("Unique original grid/year cohorts", not original.duplicated(["grid", "commissioning_year"]).any())
    record("Nonnegative finite original capacity", np.isfinite(original["capacity_added_mw"]).all()
           and original["capacity_added_mw"].ge(0).all())
    record("Complete unique cohort membership in every delay", len(cohorts) == len(original) * len(DELAYS)
           and not cohorts.duplicated(["grid", "commissioning_year", "additional_delay_years"]).any())
    for delay in DELAYS:
        retained = cohorts[cohorts["additional_delay_years"].eq(delay)]
        pd.testing.assert_frame_equal(retained[original.columns[:3]].reset_index(drop=True),
                                      original[original.columns[:3]].reset_index(drop=True))
    record("Original capacity totals retained, excluding Sabang", cohorts.groupby(
        ["grid", "additional_delay_years"])["capacity_added_mw"].sum().to_dict()
        == {(grid, delay): capacity for grid, capacity in [("Jamali", 2503), ("Sumatera", 2007)] for delay in DELAYS})
    record("Additional delay preserves one-year generation lag", cohorts["generation_start_year"].eq(
        cohorts["commissioning_year"] + cohorts["additional_delay_years"] + 1).all())
    record("Complete unique annual and summary keys", len(generation) == len(GRIDS) * len(DELAYS) * len(YEARS)
           and len(annual) == len(generation) * len(METHODS) and len(summary) == len(GRIDS) * len(DELAYS) * len(METHODS)
           and not annual.duplicated(KEYS + ["analysis_year"]).any() and not summary.duplicated(KEYS).any())
    zero = annual[annual["additional_delay_years"].eq(0)]
    original_model = build_model().query('capacity_factor_case == "Central (80%)"')
    comparison_keys = ["grid", "analysis_year", "factor_method"]
    shared = [column for column in original_model if column in zero]
    pd.testing.assert_frame_equal(
        zero[shared].sort_values(comparison_keys).reset_index(drop=True),
        original_model[shared].sort_values(comparison_keys).reset_index(drop=True), check_exact=True,
    )
    record("Zero delay exactly reproduces original in-memory central model", True)
    for name, current, keys in [
        ("by_year", zero, comparison_keys), ("summary", summary.query("additional_delay_years == 0"), ["grid", "factor_method"])
    ]:
        saved = pd.read_csv(OUTPUT_DIR / f"planned_geothermal_credit_potential_{name}.csv")
        saved = saved[saved["capacity_factor_case"].eq("Central (80%)")]
        joined = current.merge(saved, on=keys, suffixes=("_new", "_saved"), validate="one_to_one")
        record(f"Zero delay matches saved original {name} within 1e-7 absolute units", len(joined) == len(saved)
               and all(close(joined[f"{quantity}_new"], joined[f"{quantity}_saved"]) for quantity in QUANTITIES))
    for row in generation.itertuples():
        source = original[original["grid"].eq(row.grid)]
        expected_capacity = sum(
            cohort.capacity_added_mw for cohort in source.itertuples()
            if row.analysis_year > cohort.commissioning_year + row.additional_delay_years
        )
        record(f"Cohort timing {row.grid}/{row.additional_delay_years}/{row.analysis_year}",
               row.operating_planned_capacity_mw == expected_capacity
               and row.estimated_generation_mwh == expected_capacity * HOURS * CENTRAL_CF)
    expected_totals = []
    for row in summary.itertuples():
        expected_totals.append(sum(
            cohort.capacity_added_mw * HOURS * CENTRAL_CF
            * sum(year > cohort.commissioning_year + row.additional_delay_years for year in YEARS)
            for cohort in original[original["grid"].eq(row.grid)].itertuples()
        ))
    record("Independent cohort-year cumulative reconciliation", close(summary["estimated_generation_mwh"], expected_totals))
    record("Delayed capacity outside window retained and contributes zero", cohorts.loc[
        cohorts["starts_after_window"], "estimated_generation_mwh"].eq(0).all()
        and summary["operating_capacity_mw_2034"].add(summary["capacity_starting_after_window_mw"]).eq(
            summary["original_planned_capacity_mw"]).all())
    record("Nonnegative annual and cumulative generation", generation[["estimated_generation_mwh", "cumulative_generation_mwh"]].ge(0).all().all())
    record("Cumulative generation grows with analysis year", generation.groupby(
        ["grid", "additional_delay_years"])["cumulative_generation_mwh"].diff().dropna().ge(0).all())
    for quantity in ["estimated_generation_mwh", "cumulative_generation_mwh"]:
        wide = generation.pivot(index=["grid", "analysis_year"], columns="additional_delay_years", values=quantity)
        record(f"Uniform delay never increases {quantity}", wide[0].ge(wide[1]).all() and wide[1].ge(wide[2]).all())
    record("Generation identical across factor methods", annual.groupby(
        ["grid", "additional_delay_years", "analysis_year"])["estimated_generation_mwh"].nunique().eq(1).all())
    record("Fixed published factors unchanged", annual.groupby(["grid", "factor_method"])["factor_tco2_per_mwh"].nunique().eq(1).all())
    record("Annual emissions arithmetic", close(annual[QUANTITIES[1]], annual[QUANTITIES[0]] * annual["factor_tco2_per_mwh"]))
    for quantity, cumulative in zip(QUANTITIES, ["cumulative_generation_mwh", "cumulative_gross_avoided_emissions_tco2"]):
        last = annual.groupby(KEYS)[cumulative].last()
        record(f"Annual-to-cumulative {quantity}", close(last, summary.set_index(KEYS).loc[last.index, quantity]))
    for table_name, table in [("annual", annual), ("summary", summary)]:
        quantities = QUANTITIES if table_name == "summary" else QUANTITIES + [
            "cumulative_generation_mwh", "cumulative_gross_avoided_emissions_tco2"]
        for quantity in quantities:
            reference = table[f"current_schedule_{quantity}"]
            record(f"{table_name} absolute reduction {quantity}", close(
                table[f"reduction_{quantity}"], reference - table[quantity]))
            nonzero = reference.ne(0)
            record(f"{table_name} percentage reduction {quantity}", close(
                table.loc[nonzero, f"reduction_pct_{quantity}"],
                100 * (1 - table.loc[nonzero, quantity] / reference[nonzero]))
                   and table.loc[~nonzero, f"reduction_pct_{quantity}"].isna().all())
    record("Equal generation/emissions percentage reductions", close(
        summary[f"reduction_pct_{QUANTITIES[0]}"], summary[f"reduction_pct_{QUANTITIES[1]}"]))
    return checks


def make_charts(generation, summary):
    colors = ["#176b87", "#d97706", "#923a78"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), sharey=True)
    for axis, grid in zip(axes, GRIDS):
        for (delay, label), color, marker in zip(DELAYS.items(), colors, ["o", "s", "^"]):
            data = generation[(generation["grid"].eq(grid)) & (generation["additional_delay_years"].eq(delay))]
            axis.plot(data["analysis_year"], data["estimated_generation_mwh"] / 1e6,
                      label=label, color=color, marker=marker, linewidth=2)
        axis.set_title(grid, fontsize=13, fontweight="bold")
        axis.set_xlabel("Generation year")
        axis.set_xticks(list(YEARS)[::2] + [max(YEARS)])
        axis.grid(alpha=0.2)
        axis.set_ylim(bottom=0)
    axes[0].set_ylabel("Annual planned-project electricity (TWh)")
    fig.suptitle("Later commissioning shifts electricity beyond the study window", fontsize=15)
    fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", bbox_to_anchor=(0.5, 0.04), ncol=3, frameon=False)
    fig.text(0.5, 0.015, "Scenario assumptions: 80% capacity factor; 8,760 hours/year; existing one-year start lag retained in all cases.", ha="center", fontsize=10)
    fig.tight_layout(rect=(0, 0.13, 1, 0.93))
    fig.savefig(OUTPUT / "commissioning_delay_annual_generation.png", dpi=200)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.4), sharey=True)
    positions = np.arange(len(METHODS))
    for axis, grid in zip(axes, GRIDS):
        for (delay, label), color in zip(DELAYS.items(), colors):
            data = summary[(summary["grid"].eq(grid)) & (summary["additional_delay_years"].eq(delay))].set_index("factor_method").loc[METHODS]
            bars = axis.bar(positions + (delay - 1) * 0.26, data["gross_avoided_emissions_tco2"] / 1e6,
                            width=0.24, color=color, label=label)
            axis.bar_label(bars, fmt="%.1f", padding=3, fontsize=9)
        axis.set_title(grid, fontsize=13, fontweight="bold")
        axis.set_xticks(positions, ["OM", "BM", "CM ex-post\n50/50", "CM ex-ante\n50/50", "JCM\nalternative"], fontsize=10)
        axis.set_ylim(0, 62)
        axis.grid(axis="y", alpha=0.2)
        axis.set_axisbelow(True)
    axes[0].set_ylabel("2025–2034 cumulative gross avoided emissions (MtCO₂)")
    fig.suptitle("Commissioning delays reduce gross estimates under every fixed factor", fontsize=15)
    fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", bbox_to_anchor=(0.5, 0.055), ncol=3, frameon=False)
    fig.text(0.5, 0.025, "Same projects, grid boundaries and published factors; 80% capacity factor; one-year start lag + additional delay.", ha="center", fontsize=10)
    fig.text(0.5, 0.002, "Scenario sensitivity, not predicted delays, confidence intervals or issued credits. Bar labels rounded to 0.1 MtCO₂.", ha="center", fontsize=10)
    fig.tight_layout(rect=(0, 0.16, 1, 0.93))
    fig.savefig(OUTPUT / "commissioning_delay_factor_comparison.png", dpi=200)
    plt.close(fig)


def save_provenance():
    snapshots = OUTPUT / "input_snapshots"
    snapshots.mkdir(exist_ok=True)
    paths = [MAPPING_FILE, ESDM_FILE, Path(__file__).with_name("geothermal_credit_model.py"),
             OUTPUT_DIR / "planned_geothermal_credit_potential_by_year.csv",
             OUTPUT_DIR / "planned_geothermal_credit_potential_summary.csv"]
    records = []
    for path in paths:
        payload = path.read_bytes()
        (snapshots / path.name).write_bytes(payload)
        records.append({"source": str(path.relative_to(ROOT)), "snapshot": f"input_snapshots/{path.name}",
                        "sha256": hashlib.sha256(payload).hexdigest()})
    manifest = {
        "analysis_window": list(YEARS), "additional_delay_years": list(DELAYS),
        "existing_commissioning_lag_years": COMMISSIONING_LAG_YEARS,
        "capacity_factor": CENTRAL_CF, "hours_per_year": HOURS,
        "generation_start_rule": "original commissioning year + additional delay + existing one-year lag",
        "percentage_denominator": "Current schedule of the same grid/factor; zero denominators left blank",
        "versions": {"python": platform.python_version(), "pandas": pd.__version__,
                     "numpy": np.__version__, "matplotlib": matplotlib.__version__},
        "inputs": records,
    }
    (OUTPUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main():
    cohorts, generation, annual, summary = build_delay_scenarios()
    checks = validate(cohorts, generation, annual, summary)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, data in [("cohorts", cohorts), ("generation_by_year", generation),
                       ("by_year", annual), ("summary", summary)]:
        data.to_csv(OUTPUT / f"commissioning_delay_{name}.csv", index=False)
    factor_methods().to_csv(OUTPUT / "emission_factor_methods.csv", index=False)
    (OUTPUT / "validation_checks.json").write_text(json.dumps(checks, indent=2) + "\n")
    save_provenance()
    make_charts(generation, summary)
    print(summary[["grid", "additional_delay_years", "factor_method", *QUANTITIES,
                   "reduction_pct_estimated_generation_mwh", "capacity_starting_after_window_mw"]].to_string(index=False))
    print(f"Passed {len(checks)} checks; outputs: {OUTPUT}")


if __name__ == "__main__":
    main()
