

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_FILE = Path("synthetic_geothermal_credit_projects.csv")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find {DATA_FILE}. Run generate_geothermal_credit_data.py first."
        )

    data = pd.read_csv(DATA_FILE)

    # We use variables that describe data/MRV readiness and project conditions.
    # Do not use estimated_avoided_tco2 as a substitute for a registry decision.
    features = [
        "capacity_mw",
        "capacity_factor",
        "grid_ef_tco2_per_mwh",
        "ncg_gco2_per_kwh",
        "mrv_readiness_score",
        "additionality_evidence",
        "ownership_clarity",
        "registry_path_ready",
        "verification_delay_months",
    ]
    target = "verified_issuance"

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # StandardScaler puts continuous variables on comparable scales.
    # LogisticRegression then estimates the probability of class 1.
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

    # Coefficients are easier to compare because the inputs were standardized.
    coefficients = model.named_steps["logistic_regression"].coef_[0]
    interpretation = pd.DataFrame(
        {
            "feature": features,
            "coefficient": coefficients,
            "direction": ["raises simulated probability" if c > 0 else "lowers simulated probability" for c in coefficients],
        }
    ).sort_values("coefficient", key=lambda s: s.abs(), ascending=False)

    print("\n--- Logistic-regression coefficients ---")
    print(interpretation.to_string(index=False, float_format="{:.3f}".format))

    # Show a few examples 
    examples = X_test.copy()
    examples["actual_verified_issuance"] = y_test
    examples["predicted_probability"] = predicted_probability.round(3)
    examples["predicted_class"] = predicted_class

    print("\n--- Five example predictions ---")
    print(
        examples[
            [
                "mrv_readiness_score",
                "additionality_evidence",
                "ownership_clarity",
                "registry_path_ready",
                "verification_delay_months",
                "actual_verified_issuance",
                "predicted_probability",
                "predicted_class",
            ]
        ]
        .head()
        .to_string(index=False)
    )




if __name__ == "__main__":
    main()
