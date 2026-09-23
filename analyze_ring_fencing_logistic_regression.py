from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_FILE = Path("synthetic_ring_fencing_projects.csv")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find {DATA_FILE}. Run generate_ring_fencing_data.py first."
        )

    data = pd.read_csv(DATA_FILE)

    features = [
        "project_cost_idr_bn",
        "baseline_technical_loss_pct",
        "planning_capacity_score",
        "rab_readiness_score",
        "tariff_method_ready",
        "metering_data_quality_score",
        "technical_nontechnical_loss_separated",
        "protected_funding_share",
        "approval_delay_months",
        "construction_duration_months",
    ]
    target = "completed_on_time"

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Scale the inputs, then fit a simple and interpretable logistic-regression model.
    model = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("logistic_regression", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    model.fit(X_train, y_train)

    predicted_class = model.predict(X_test)
    predicted_probability = model.predict_proba(X_test)[:, 1]

    print("\n--- Model performance on the synthetic test set ---")
    print("Accuracy:", round(accuracy_score(y_test, predicted_class), 3))
    print("ROC-AUC:", round(roc_auc_score(y_test, predicted_probability), 3))
    print("\nConfusion matrix: rows = actual, columns = predicted")
    print(confusion_matrix(y_test, predicted_class))
    print("\nClassification report")
    print(classification_report(y_test, predicted_class, digits=3))

    coefficients = model.named_steps["logistic_regression"].coef_[0]
    interpretation = pd.DataFrame(
        {
            "feature": features,
            "coefficient": coefficients,
            "direction": [
                "raises simulated on-time probability" if c > 0 else "lowers simulated on-time probability"
                for c in coefficients
            ],
        }
    ).sort_values("coefficient", key=lambda s: s.abs(), ascending=False)

    print("\n--- Logistic-regression coefficients ---")
    print(interpretation.to_string(index=False, float_format="{:.3f}".format))

    examples = X_test.copy()
    examples["actual_completed_on_time"] = y_test
    examples["predicted_probability"] = predicted_probability.round(3)
    examples["predicted_class"] = predicted_class

    print("\n--- Five example predictions ---")
    print(
        examples[
            [
                "rab_readiness_score",
                "tariff_method_ready",
                "metering_data_quality_score",
                "protected_funding_share",
                "approval_delay_months",
                "actual_completed_on_time",
                "predicted_probability",
                "predicted_class",
            ]
        ]
        .head()
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
