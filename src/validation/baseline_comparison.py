"""
MedImpact AI
Baseline comparability analysis.

IMPORTANT:
This analysis uses synthetic data for educational/research purposes.
It does not establish clinical efficacy.
"""

from pathlib import Path

import pandas as pd
from scipy import stats


DATA_FILE = Path(
    "data/synthetic/diabetes_longitudinal_data.csv"
)


def load_data():
    """Load synthetic longitudinal data."""
    return pd.read_csv(DATA_FILE)


def compare_continuous_variable(data, column):
    """Compare a continuous baseline variable between groups."""

    ai = data[
        data["intervention"] == "AI_Assisted"
    ][column]

    control = data[
        data["intervention"] == "Control"
    ][column]

    result = stats.ttest_ind(
        ai,
        control,
        equal_var=False
    )

    return {
        "AI mean": ai.mean(),
        "Control mean": control.mean(),
        "Mean difference": ai.mean() - control.mean(),
        "p-value": result.pvalue,
    }


def main():

    print("=" * 70)
    print("MedImpact AI - Baseline Comparability Analysis")
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

        result = compare_continuous_variable(
            data,
            variable
        )

        result["Variable"] = variable

        results.append(result)

    results_df = pd.DataFrame(results)

    results_df = results_df[
        [
            "Variable",
            "AI mean",
            "Control mean",
            "Mean difference",
            "p-value",
        ]
    ]

    print("\n--- Baseline Characteristics ---\n")

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    print("\n--- Interpretation ---")

    print(
        "These tests describe baseline differences "
        "in the synthetic groups."
    )

    print(
        "A large baseline difference can indicate "
        "that simple outcome comparisons may be misleading."
    )

    print(
        "Statistical significance alone does not determine "
        "whether a baseline difference is clinically important."
    )

    print("\nIMPORTANT:")
    print(
        "This is synthetic data and does not represent "
        "real patients or clinical evidence."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()

