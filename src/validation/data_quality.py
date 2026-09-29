"""
MedImpact AI
Synthetic medical dataset quality validation.

This module performs structural and range checks before
statistical analysis.

IMPORTANT:
The dataset is synthetic and contains no real patient data.
"""

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DATA_FILE = Path(
    "data/synthetic/diabetes_longitudinal_data.csv"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

def load_data():
    """Load the synthetic dataset."""
    return pd.read_csv(DATA_FILE)


# ---------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------

def check_missing_values(data):
    """Check for missing values."""

    missing = data.isnull().sum()

    return missing[missing > 0]


def check_duplicate_patients(data):
    """Check for duplicate patient IDs."""

    return data["patient_id"].duplicated().sum()


def check_age(data):
    """Check whether ages are within the expected range."""

    return (
        (data["age"] < 18)
        | (data["age"] > 100)
    ).sum()


def check_bmi(data):
    """Check whether BMI values are plausible."""

    return (
        (data["bmi"] < 10)
        | (data["bmi"] > 80)
    ).sum()


def check_hba1c(data):
    """Check HbA1c ranges."""

    columns = [
        "baseline_hba1c",
        "followup_hba1c"
    ]

    invalid = 0

    for column in columns:
        invalid += (
            (data[column] < 3)
            | (data[column] > 20)
        ).sum()

    return invalid


def check_blood_pressure(data):
    """Check systolic blood pressure ranges."""

    columns = [
        "baseline_systolic_bp",
        "followup_systolic_bp"
    ]

    invalid = 0

    for column in columns:
        invalid += (
            (data[column] < 60)
            | (data[column] > 250)
        ).sum()

    return invalid


def check_adherence(data):
    """Check adherence percentages."""

    columns = [
        "baseline_adherence_pct",
        "followup_adherence_pct"
    ]

    invalid = 0

    for column in columns:
        invalid += (
            (data[column] < 0)
            | (data[column] > 100)
        ).sum()

    return invalid


def check_intervention(data):
    """Check intervention labels."""

    valid_groups = {
        "Control",
        "AI_Assisted"
    }

    invalid = ~data[
        "intervention"
    ].isin(valid_groups)

    return invalid.sum()


def check_followup_days(data):
    """Check follow-up duration."""

    return (
        (data["followup_days"] <= 0)
        | (data["followup_days"] > 3650)
    ).sum()


# ---------------------------------------------------------
# Group balance
# ---------------------------------------------------------

def check_group_balance(data):
    """Return intervention group counts."""

    return data[
        "intervention"
    ].value_counts()


# ---------------------------------------------------------
# Main validation
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("MedImpact AI - Data Quality Validation")
    print("=" * 70)

    data = load_data()

    print(
        f"\nDataset: {DATA_FILE}"
    )

    print(
        f"Rows: {len(data)}"
    )

    print(
        f"Columns: {len(data.columns)}"
    )

    # -----------------------------------------------------
    # Run checks
    # -----------------------------------------------------

    missing = check_missing_values(data)
    duplicates = check_duplicate_patients(data)
    invalid_age = check_age(data)
    invalid_bmi = check_bmi(data)
    invalid_hba1c = check_hba1c(data)
    invalid_bp = check_blood_pressure(data)
    invalid_adherence = check_adherence(data)
    invalid_intervention = check_intervention(data)
    invalid_followup = check_followup_days(data)

    # -----------------------------------------------------
    # Report
    # -----------------------------------------------------

    print("\n--- Quality Checks ---")

    print(
        f"Missing values: "
        f"{missing.sum() if len(missing) else 0}"
    )

    print(
        f"Duplicate patient IDs: "
        f"{duplicates}"
    )

    print(
        f"Invalid ages: "
        f"{invalid_age}"
    )

    print(
        f"Invalid BMI values: "
        f"{invalid_bmi}"
    )

    print(
        f"Invalid HbA1c values: "
        f"{invalid_hba1c}"
    )

    print(
        f"Invalid blood pressure values: "
        f"{invalid_bp}"
    )

    print(
        f"Invalid adherence values: "
        f"{invalid_adherence}"
    )

    print(
        f"Invalid intervention labels: "
        f"{invalid_intervention}"
    )

    print(
        f"Invalid follow-up periods: "
        f"{invalid_followup}"
    )

    # -----------------------------------------------------
    # Group balance
    # -----------------------------------------------------

    print("\n--- Intervention Group Balance ---")

    print(
        check_group_balance(data)
    )

    # -----------------------------------------------------
    # Final status
    # -----------------------------------------------------

    total_errors = (
        missing.sum()
        + duplicates
        + invalid_age
        + invalid_bmi
        + invalid_hba1c
        + invalid_bp
        + invalid_adherence
        + invalid_intervention
        + invalid_followup
    )

    print("\n--- Validation Result ---")

    if total_errors == 0:

        print(
            "PASS: No data-quality violations detected."
        )

    else:

        print(
            f"FAIL: {total_errors} "
            "data-quality violations detected."
        )

    print("=" * 70)


if __name__ == "__main__":
    main()

