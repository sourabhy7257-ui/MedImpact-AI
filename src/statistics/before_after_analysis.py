"""
MedImpact AI
Before/After and Between-Group Statistical Analysis

IMPORTANT:
This module is designed for synthetic/educational data.
It does not provide medical advice or establish clinical efficacy.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


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
    """Load the synthetic longitudinal dataset."""
    return pd.read_csv(DATA_FILE)


# ---------------------------------------------------------
# Mean change
# ---------------------------------------------------------

def calculate_mean_change(
    data,
    baseline_column,
    followup_column
):
    """Calculate mean follow-up minus baseline."""

    changes = (
        data[followup_column]
        - data[baseline_column]
    )

    return {
        "mean_change": changes.mean(),
        "std_change": changes.std(),
        "n": len(changes)
    }


# ---------------------------------------------------------
# Confidence interval
# ---------------------------------------------------------

def calculate_mean_change_ci(
    data,
    baseline_column,
    followup_column,
    confidence=0.95
):
    """Calculate a confidence interval for mean change."""

    changes = (
        data[followup_column]
        - data[baseline_column]
    )

    n = len(changes)
    mean_change = changes.mean()
    standard_error = stats.sem(changes)

    interval = stats.t.interval(
        confidence,
        df=n - 1,
        loc=mean_change,
        scale=standard_error
    )

    return {
        "lower": interval[0],
        "upper": interval[1]
    }


# ---------------------------------------------------------
# Paired t-test
# ---------------------------------------------------------

def paired_t_test(
    data,
    baseline_column,
    followup_column
):
    """Perform a paired t-test."""

    baseline = data[baseline_column]
    followup = data[followup_column]

    result = stats.ttest_rel(
        baseline,
        followup
    )

    return {
        "t_statistic": result.statistic,
        "p_value": result.pvalue
    }


# ---------------------------------------------------------
# Wilcoxon signed-rank test
# ---------------------------------------------------------

def wilcoxon_test(
    data,
    baseline_column,
    followup_column
):
    """Perform a Wilcoxon signed-rank test."""

    baseline = data[baseline_column]
    followup = data[followup_column]

    result = stats.wilcoxon(
        baseline,
        followup
    )

    return {
        "statistic": result.statistic,
        "p_value": result.pvalue
    }


# ---------------------------------------------------------
# Paired Cohen's d
# ---------------------------------------------------------

def paired_cohens_d(
    data,
    baseline_column,
    followup_column
):
    """Calculate Cohen's d for paired observations."""

    changes = (
        data[followup_column]
        - data[baseline_column]
    )

    standard_deviation = changes.std()

    if standard_deviation == 0:
        return np.nan

    return changes.mean() / standard_deviation


# ---------------------------------------------------------
# Difference in mean changes
# ---------------------------------------------------------

def between_group_change_analysis(
    data,
    baseline_column,
    followup_column,
    group_column="intervention"
):
    """
    Compare changes between AI-Assisted and Control groups.
    """

    data = data.copy()

    data["change"] = (
        data[followup_column]
        - data[baseline_column]
    )

    ai_group = data[
        data[group_column] == "AI_Assisted"
    ]["change"]

    control_group = data[
        data[group_column] == "Control"
    ]["change"]

    difference = (
        ai_group.mean()
        - control_group.mean()
    )

    test = stats.ttest_ind(
        ai_group,
        control_group,
        equal_var=False
    )

    return {
        "ai_mean_change": ai_group.mean(),
        "control_mean_change": control_group.mean(),
        "difference_in_mean_change": difference,
        "t_statistic": test.statistic,
        "p_value": test.pvalue
    }


# ---------------------------------------------------------
# Difference-in-Differences
# ---------------------------------------------------------

def difference_in_differences(
    data,
    baseline_column,
    followup_column,
    group_column="intervention"
):
    """
    Calculate the simple Difference-in-Differences estimate.

    DID =
    AI group change - Control group change
    """

    data = data.copy()

    data["change"] = (
        data[followup_column]
        - data[baseline_column]
    )

    ai_change = data[
        data[group_column] == "AI_Assisted"
    ]["change"].mean()

    control_change = data[
        data[group_column] == "Control"
    ]["change"].mean()

    did_estimate = ai_change - control_change

    return {
        "ai_change": ai_change,
        "control_change": control_change,
        "did_estimate": did_estimate
    }


# ---------------------------------------------------------
# Main analysis
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("MedImpact AI - Statistical Impact Analysis")
    print("=" * 70)

    data = load_data()

    print(f"\nDataset: {DATA_FILE}")
    print(f"Total observations: {len(data)}")

    # ---------------------------------------------
    # Overall before/after analysis
    # ---------------------------------------------

    overall = calculate_mean_change(
        data,
        "baseline_hba1c",
        "followup_hba1c"
    )

    ci = calculate_mean_change_ci(
        data,
        "baseline_hba1c",
        "followup_hba1c"
    )

    paired_test = paired_t_test(
        data,
        "baseline_hba1c",
        "followup_hba1c"
    )

    wilcoxon = wilcoxon_test(
        data,
        "baseline_hba1c",
        "followup_hba1c"
    )

    effect_size = paired_cohens_d(
        data,
        "baseline_hba1c",
        "followup_hba1c"
    )

    print("\n--- Overall Before vs After ---")

    print(
        f"Mean HbA1c change: "
        f"{overall['mean_change']:.3f}"
    )

    print(
        f"95% CI: "
        f"[{ci['lower']:.3f}, "
        f"{ci['upper']:.3f}]"
    )

    print(
        f"Paired t-test p-value: "
        f"{paired_test['p_value']:.6f}"
    )

    print(
        f"Wilcoxon p-value: "
        f"{wilcoxon['p_value']:.6f}"
    )

    print(
        f"Paired Cohen's d: "
        f"{effect_size:.3f}"
    )

    # ---------------------------------------------
    # Between-group analysis
    # ---------------------------------------------

    group_analysis = between_group_change_analysis(
        data,
        "baseline_hba1c",
        "followup_hba1c"
    )

    print("\n--- Between-Group Change ---")

    print(
        f"AI-Assisted mean change: "
        f"{group_analysis['ai_mean_change']:.3f}"
    )

    print(
        f"Control mean change: "
        f"{group_analysis['control_mean_change']:.3f}"
    )

    print(
        f"Difference in mean change: "
        f"{group_analysis['difference_in_mean_change']:.3f}"
    )

    print(
        f"Between-group p-value: "
        f"{group_analysis['p_value']:.6f}"
    )

    # ---------------------------------------------
    # Difference-in-Differences
    # ---------------------------------------------

    did = difference_in_differences(
        data,
        "baseline_hba1c",
        "followup_hba1c"
    )

    print("\n--- Difference-in-Differences ---")

    print(
        f"AI-Assisted change: "
        f"{did['ai_change']:.3f}"
    )

    print(
        f"Control change: "
        f"{did['control_change']:.3f}"
    )

    print(
        f"DID estimate: "
        f"{did['did_estimate']:.3f}"
    )

    print("\n--- Interpretation ---")

    print(
        "The results describe changes observed in "
        "the synthetic dataset."
    )

    print(
        "They do NOT establish clinical efficacy "
        "or causality in real patients."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()

