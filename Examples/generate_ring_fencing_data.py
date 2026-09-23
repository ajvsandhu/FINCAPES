from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
N_PROJECTS = 240
OUTPUT_FILE = Path("synthetic_ring_fencing_projects.csv")


def sigmoid(x):
    """Convert a number into a probability between 0 and 1."""
    return 1 / (1 + np.exp(-x))


def main():
    rng = np.random.default_rng(RANDOM_SEED)

    project_cost_idr_bn = rng.uniform(100, 3_500, N_PROJECTS)
    baseline_technical_loss_pct = rng.normal(7.0, 1.5, N_PROJECTS).clip(3.0, 12.0)
    planning_capacity_score = rng.integers(1, 6, N_PROJECTS)  # 1 = weak, 5 = strong
    rab_readiness_score = rng.integers(1, 6, N_PROJECTS)  # regulated asset base readiness
    tariff_method_ready = rng.binomial(1, 0.50, N_PROJECTS)
    metering_data_quality_score = rng.integers(1, 6, N_PROJECTS)
    technical_nontechnical_loss_separated = rng.binomial(1, 0.55, N_PROJECTS)
    protected_funding_share = rng.uniform(0.30, 1.00, N_PROJECTS)
    approval_delay_months = rng.normal(16, 7, N_PROJECTS).clip(2, 42)
    construction_duration_months = rng.normal(30, 9, N_PROJECTS).clip(12, 60)

    # The expected loss reduction is only a planning proxy, not a power-flow result.
    expected_loss_reduction_pct = (
        0.25 * planning_capacity_score
        + 1.30 * protected_funding_share
        + rng.normal(0, 0.6, N_PROJECTS)
    ).clip(0, 5)


    log_odds = (
        -5.5
        + 0.70 * planning_capacity_score
        + 0.80 * rab_readiness_score
        + 1.10 * tariff_method_ready
        + 0.65 * metering_data_quality_score
        + 0.85 * technical_nontechnical_loss_separated
        + 1.10 * protected_funding_share
        - 0.070 * approval_delay_months
        - 0.035 * construction_duration_months
        - 0.00018 * project_cost_idr_bn
        + rng.normal(0, 0.65, N_PROJECTS)
    )
    completion_probability = sigmoid(log_odds)
    completed_on_time = rng.binomial(1, completion_probability)

    data = pd.DataFrame(
        {
            "project_id": [f"SIM-RF-{i:03d}" for i in range(1, N_PROJECTS + 1)],
            "project_cost_idr_bn": project_cost_idr_bn.round(1),
            "baseline_technical_loss_pct": baseline_technical_loss_pct.round(2),
            "expected_loss_reduction_pct": expected_loss_reduction_pct.round(2),
            "planning_capacity_score": planning_capacity_score,
            "rab_readiness_score": rab_readiness_score,
            "tariff_method_ready": tariff_method_ready,
            "metering_data_quality_score": metering_data_quality_score,
            "technical_nontechnical_loss_separated": technical_nontechnical_loss_separated,
            "protected_funding_share": protected_funding_share.round(2),
            "approval_delay_months": approval_delay_months.round(1),
            "construction_duration_months": construction_duration_months.round(1),
            "completed_on_time": completed_on_time,
        }
    )
    data.to_csv(OUTPUT_FILE, index=False)

    print("Synthetic dataset created:", OUTPUT_FILE.resolve())
    print(f"Rows: {len(data)}")
    print("\nTarget distribution (0 = not on time, 1 = completed on time):")
    print(data["completed_on_time"].value_counts().sort_index())



if __name__ == "__main__":
    main()
