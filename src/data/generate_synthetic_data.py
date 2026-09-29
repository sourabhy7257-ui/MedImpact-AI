"""
MedImpact AI
Synthetic longitudinal medical dataset generator.

IMPORTANT:
This dataset is completely synthetic and contains no real patient information.
It is created only for research, education, and software development.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

RANDOM_SEED = 42
N_PATIENTS = 1000

OUTPUT_DIR = Path("data/synthetic")
OUTPUT_FILE = OUTPUT_DIR / "diabetes_longitudinal_data.csv"


# ---------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------

rng = np.random.default_rng(RANDOM_SEED)


# ---------------------------------------------------------
# Generate patient characteristics
# ---------------------------------------------------------

patient_ids = [
    f"P{number:04d}"
    for number in range(1, N_PATIENTS + 1)
]

age = rng.integers(
    low=30,
    high=76,
    size=N_PATIENTS
)

sex = rng.choice(
    ["Male", "Female"],
    size=N_PATIENTS,
    p=[0.55, 0.45]
)

diabetes_duration_years = np.round(
    rng.uniform(1, 15, N_PATIENTS),
    1
)

bmi = np.round(
    np.clip(
        rng.normal(28.5, 4.5, N_PATIENTS),
        19,
        45
    ),
    1
)


# ---------------------------------------------------------
# Baseline clinical measurements
# ---------------------------------------------------------

baseline_hba1c = np.round(
    np.clip(
        rng.normal(8.2, 1.2, N_PATIENTS),
        6.5,
        12.5
    ),
    2
)

baseline_systolic_bp = np.round(
    np.clip(
        rng.normal(140, 15, N_PATIENTS),
        100,
        190
    ),
    0
)

baseline_adherence_pct = np.round(
    np.clip(
        rng.normal(65, 15, N_PATIENTS),
        25,
        100
    ),
    1
)


# ---------------------------------------------------------
# Assign intervention groups
# ---------------------------------------------------------

intervention = rng.choice(
    ["Control", "AI_Assisted"],
    size=N_PATIENTS,
    p=[0.5, 0.5]
)


# ---------------------------------------------------------
# Follow-up period
# ---------------------------------------------------------

followup_days = rng.integers(
    low=84,
    high=181,
    size=N_PATIENTS
)


# ---------------------------------------------------------
# Simulate follow-up adherence
# ---------------------------------------------------------

adherence_improvement = np.where(
    intervention == "AI_Assisted",
    rng.normal(10, 5, N_PATIENTS),
    rng.normal(3, 5, N_PATIENTS)
)

followup_adherence_pct = np.round(
    np.clip(
        baseline_adherence_pct + adherence_improvement,
        20,
        100
    ),
    1
)


# ---------------------------------------------------------
# Simulate follow-up HbA1c
# ---------------------------------------------------------

# Natural variation affecting both groups
natural_hba1c_change = rng.normal(
    -0.20,
    0.35,
    N_PATIENTS
)

# Additional simulated intervention effect
# This is deliberately synthetic and NOT a medical claim.
ai_effect = np.where(
    intervention == "AI_Assisted",
    rng.normal(-0.45, 0.20, N_PATIENTS),
    0
)

followup_hba1c = np.round(
    np.clip(
        baseline_hba1c
        + natural_hba1c_change
        + ai_effect,
        5.0,
        13.0
    ),
    2
)


# ---------------------------------------------------------
# Simulate follow-up systolic blood pressure
# ---------------------------------------------------------

natural_bp_change = rng.normal(
    -2,
    7,
    N_PATIENTS
)

ai_bp_effect = np.where(
    intervention == "AI_Assisted",
    rng.normal(-5, 3, N_PATIENTS),
    0
)

followup_systolic_bp = np.round(
    np.clip(
        baseline_systolic_bp
        + natural_bp_change
        + ai_bp_effect,
        90,
        200
    ),
    0
)


# ---------------------------------------------------------
# Build DataFrame
# ---------------------------------------------------------

df = pd.DataFrame(
    {
        "patient_id": patient_ids,
        "age": age,
        "sex": sex,
        "diabetes_duration_years": diabetes_duration_years,
        "bmi": bmi,
        "baseline_hba1c": baseline_hba1c,
        "baseline_systolic_bp": baseline_systolic_bp,
        "baseline_adherence_pct": baseline_adherence_pct,
        "intervention": intervention,
        "followup_hba1c": followup_hba1c,
        "followup_systolic_bp": followup_systolic_bp,
        "followup_adherence_pct": followup_adherence_pct,
        "followup_days": followup_days,
    }
)


# ---------------------------------------------------------
# Calculate simple patient-level changes
# ---------------------------------------------------------

df["hba1c_change"] = np.round(
    df["followup_hba1c"] - df["baseline_hba1c"],
    2
)

df["systolic_bp_change"] = np.round(
    df["followup_systolic_bp"]
    - df["baseline_systolic_bp"],
    2
)

df["adherence_change"] = np.round(
    df["followup_adherence_pct"]
    - df["baseline_adherence_pct"],
    2
)


# ---------------------------------------------------------
# Save dataset
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Display summary
# ---------------------------------------------------------

print("=" * 60)
print("MedImpact AI - Synthetic Dataset Generator")
print("=" * 60)

print(f"Patients generated: {len(df)}")
print(f"Output file: {OUTPUT_FILE}")

print("\nIntervention distribution:")
print(df["intervention"].value_counts())

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset generation completed successfully.")
print("=" * 60)

