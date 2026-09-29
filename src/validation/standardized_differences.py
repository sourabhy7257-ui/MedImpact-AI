"""
MedImpact AI
Standardized Mean Difference analysis.

IMPORTANT:
This module uses synthetic data for educational/research purposes.
"""

from pathlib import Path

import numpy as np
import pandas as pd


DATA_FILE = Path(
    "data/synthetic/diabetes_longitudinal_data.csv"
)


def load_data():
    """Load the synthetic dataset."""
    return pd.read_csv(DATA_FILE)


def calculate_smd(data, column):
    """
    Calculate standardized mean difference.

    SMD =
    (Mean_AI - Mean_Control) / Pooled Standard Deviation
    """

    ai = data[
        data["intervention"] == "AI_Assisted"
    ][column]

    control = data[
        data["intervention"] == "Control"
    ][column]

    ai_mean = ai.mean()
    control_mean = control.mean()

    ai_variance = ai.var()
    control_variance = control.var()

    ai_n = len(ai)
    control_n = len(control)

    pooled_sd = np.sqrt(
        (
            (ai_n - 1) * ai_variance
            + (control_n - 1) * control_variance
        )
        / (
            ai_n + control_n - 2
        )
    )

    smd = (
        (ai_mean - control_mean)
        / pooled_sd
    )

    return {
        "AI mean": ai_mean,
        "Control mean": control_mean,
        "SMD": smd,
        "Absolute SMD": abs(smd),
    }


def interpret_smd(abs_smd):
    """Provide a descriptive SMD interpretation."""

    if abs_smd < 0.10:
        return "Small difference"

    if abs_smd < 0.20:
        return "Possible moderate difference"

    return "Larger difference"


def main():

    print("=" * 70)
    print("MedImpact AI - Standardized Mean Difference Analysis")
    print("=" * 70)

    data = load_data()

    variables = [
        "age",
        "diabetes_duration_years",
        "bmi",
        "baseline_hba1c",
        "baseline_systolic_bp",
        "baseline_adherence_pct",
    ]

    results = []

    for variable in variables:

        result = calculate_smd(
            data,
            variable
        )

        result["Variable"] = variable

        result["Interpretation"] = interpret_smd(
            result["Absolute SMD"]
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    results_df = results_df[
        [
            "Variable",
            "AI mean",
            "Control mean",
            "SMD",
            "Absolute SMD",
            "Interpretation",
        ]
    ]

    print("\n--- Standardized Baseline Differences ---\n")

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    print("\n--- Interpretation Guide ---")

    print(
        "|SMD| < 0.10  : Small difference"
    )

    print(
        "0.10–0.20    : Possible moderate difference"
    )

    print(
        "|SMD| > 0.20  : Larger difference"
    )

    print(
        "\nThese thresholds are rules of thumb, "
        "not definitive clinical criteria."
    )

    print(
        "\nThe analysis describes synthetic data only "
        "and does not establish clinical equivalence."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()

