"""Create a synthetic teaching dataset for Indonesian geothermal carbon-credit research.


from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
N_PROJECTS = 240
OUTPUT_FILE = Path("synthetic_geothermal_credit_projects.csv")


def sigmoid(x):
    """Convert any number into a probability between 0 and 1."""
    return 1 / (1 + np.exp(-x))


def main():
    rng = np.random.default_rng(RANDOM_SEED)

    # These ranges are assumptions 
    capacity_mw = rng.uniform(10, 230, N_PROJECTS).round(1)
    capacity_factor = rng.normal(0.88, 0.06, N_PROJECTS).clip(0.65, 0.97)
    grid_ef_tco2_per_mwh = rng.normal(0.68, 0.10, N_PROJECTS).clip(0.40, 0.90)
    ncg_gco2_per_kwh = rng.normal(63, 20, N_PROJECTS).clip(20, 140)

    # Administrative and MRV variables are scores, not legal conclusions.
    mrv_readiness_score = rng.integers(1, 6, N_PROJECTS)  # 1 = weak, 5 = strong
    additionality_evidence = rng.binomial(1, 0.55, N_PROJECTS)
    ownership_clarity = rng.binomial(1, 0.60, N_PROJECTS)
    registry_path_ready = rng.binomial(1, 0.50, N_PROJECTS)
    verification_delay_months = rng.normal(18, 7, N_PROJECTS).clip(3, 42)

    annual_generation_mwh = capacity_mw * 8760 * capacity_factor
    # Convert gCO2/kWh to tCO2/MWh. This is a direct-emissions adjustment only.
    direct_emissions_tco2 = annual_generation_mwh * (ncg_gco2_per_kwh / 1000)
    gross_avoided_tco2 = annual_generation_mwh * grid_ef_tco2_per_mwh
    estimated_avoided_tco2 = np.maximum(gross_avoided_tco2 - direct_emissions_tco2, 0)

    # Hidden simulation rule: the target depends mainly on MRV and institutional gates.
    # Capacity and estimated emissions matter less than readiness. This is intentional.
    log_odds = (
        -5.0
        + 0.75 * mrv_readiness_score
        + 1.10 * additionality_evidence
        + 1.00 * ownership_clarity
        + 1.15 * registry_path_ready
        - 0.055 * verification_delay_months
        + 0.0000015 * estimated_avoided_tco2
        - 0.005 * (ncg_gco2_per_kwh - 63)
        + rng.normal(0, 0.65, N_PROJECTS)
    )
    issuance_probability = sigmoid(log_odds)
    verified_issuance = rng.binomial(1, issuance_probability)

    data = pd.DataFrame(
        {
            "project_id": [f"SIM-GEO-{i:03d}" for i in range(1, N_PROJECTS + 1)],
            "capacity_mw": capacity_mw,
            "capacity_factor": capacity_factor.round(3),
            "annual_generation_mwh": annual_generation_mwh.round(0),
            "grid_ef_tco2_per_mwh": grid_ef_tco2_per_mwh.round(3),
            "ncg_gco2_per_kwh": ncg_gco2_per_kwh.round(1),
            "estimated_avoided_tco2": estimated_avoided_tco2.round(0),
            "mrv_readiness_score": mrv_readiness_score,
            "additionality_evidence": additionality_evidence,
            "ownership_clarity": ownership_clarity,
            "registry_path_ready": registry_path_ready,
            "verification_delay_months": verification_delay_months.round(1),
            "verified_issuance": verified_issuance,
        }
    )

    data.to_csv(OUTPUT_FILE, index=False)

    print("Synthetic data created:", OUTPUT_FILE.resolve())
    print(f"Rows: {len(data)}")
    print("\nTarget distribution (0 = no simulated issuance, 1 = simulated issuance):")
    print(data["verified_issuance"].value_counts().sort_index())
    print("\nReminder: estimated avoided emissions are not verified or issued credits.")


if __name__ == "__main__":
    main()
