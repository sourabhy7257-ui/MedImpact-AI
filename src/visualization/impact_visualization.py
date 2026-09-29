"""
MedImpact AI
Visualization module for medical intervention impact analysis.

IMPORTANT:
All current data is synthetic and intended for educational/research use.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DATA_FILE = Path(
    "data/synthetic/diabetes_longitudinal_data.csv"
)

OUTPUT_DIR = Path("data/synthetic/charts")


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

def load_data():
    """Load the synthetic longitudinal dataset."""
    return pd.read_csv(DATA_FILE)


# ---------------------------------------------------------
# Prepare output directory
# ---------------------------------------------------------

def prepare_output_directory():
    """Create chart output directory if needed."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ---------------------------------------------------------
# Chart 1: Before vs After HbA1c
# ---------------------------------------------------------

def plot_before_after(data):
    """Plot mean HbA1c before and after intervention."""

    summary = (
        data.groupby("intervention")[
            ["baseline_hba1c", "followup_hba1c"]
        ]
        .mean()
    )

    ax = summary.plot(
        kind="bar",
        figsize=(9, 6)
    )

    ax.set_title(
        "Mean HbA1c: Before vs After"
    )

    ax.set_xlabel("Group")
    ax.set_ylabel("HbA1c")

    ax.legend(
        ["Baseline", "Follow-up"]
    )

    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "before_after_hba1c.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ---------------------------------------------------------
# Chart 2: Change by intervention group
# ---------------------------------------------------------

def plot_group_change(data):
    """Plot average HbA1c change by group."""

    summary = (
        data.groupby("intervention")[
            "hba1c_change"
        ]
        .mean()
    )

    ax = summary.plot(
        kind="bar",
        figsize=(8, 6)
    )

    ax.set_title(
        "Mean HbA1c Change by Intervention Group"
    )

    ax.set_xlabel("Group")
    ax.set_ylabel("HbA1c Change")

    plt.axhline(
        y=0,
        linewidth=1
    )

    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "group_hba1c_change.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ---------------------------------------------------------
# Chart 3: Distribution of individual changes
# ---------------------------------------------------------

def plot_change_distribution(data):
    """Plot distribution of individual HbA1c changes."""

    plt.figure(figsize=(9, 6))

    for group in [
        "Control",
        "AI_Assisted"
    ]:

        group_data = data[
            data["intervention"] == group
        ]

        plt.hist(
            group_data["hba1c_change"],
            bins=30,
            alpha=0.5,
            label=group
        )

    plt.axvline(
        x=0,
        linewidth=1
    )

    plt.title(
        "Distribution of Individual HbA1c Changes"
    )

    plt.xlabel(
        "HbA1c Change (Follow-up - Baseline)"
    )

    plt.ylabel("Number of Patients")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "hba1c_change_distribution.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ---------------------------------------------------------
# Chart 4: Confidence intervals
# ---------------------------------------------------------

def plot_confidence_intervals(data):
    """Plot mean change with 95% confidence intervals."""

    from scipy import stats

    groups = [
        "Control",
        "AI_Assisted"
    ]

    means = []
    errors = []

    for group in groups:

        changes = data[
            data["intervention"] == group
        ]["hba1c_change"]

        mean = changes.mean()

        standard_error = stats.sem(
            changes
        )

        confidence_interval = (
            stats.t.ppf(
                0.975,
                len(changes) - 1
            )
            * standard_error
        )

        means.append(mean)
        errors.append(confidence_interval)

    plt.figure(figsize=(8, 6))

    plt.errorbar(
        groups,
        means,
        yerr=errors,
        fmt="o",
        capsize=6
    )

    plt.axhline(
        y=0,
        linewidth=1
    )

    plt.title(
        "Mean HbA1c Change with 95% Confidence Intervals"
    )

    plt.xlabel("Intervention Group")
    plt.ylabel("Mean HbA1c Change")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "hba1c_change_confidence_intervals.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("MedImpact AI - Impact Visualization")
    print("=" * 70)

    data = load_data()

    prepare_output_directory()

    plot_before_after(data)
    plot_group_change(data)
    plot_change_distribution(data)
    plot_confidence_intervals(data)

    print("\nCharts generated successfully.")

    print(
        f"\nSaved to: {OUTPUT_DIR}"
    )

    print("\nGenerated files:")

    for file in sorted(
        OUTPUT_DIR.glob("*.png")
    ):
        print(f" - {file.name}")

    print("=" * 70)


if __name__ == "__main__":
    main()

