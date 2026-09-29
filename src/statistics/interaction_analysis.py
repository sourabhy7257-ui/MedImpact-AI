import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multitest import multipletests


DATA_PATH = "data/synthetic/diabetes_longitudinal_data.csv"


def prepare_subgroups(df):

    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 40, 50, 60, 70, 100],
        labels=["<40", "40-49", "50-59", "60-69", "70+"],
        right=False
    )

    df["bmi_group"] = pd.cut(
        df["bmi"],
        bins=[0, 18.5, 25, 30, 35, 100],
        labels=[
            "Underweight",
            "Normal",
            "Overweight",
            "Obesity I",
            "Obesity II+"
        ],
        right=False
    )

    df["baseline_hba1c_group"] = pd.cut(
        df["baseline_hba1c"],
        bins=[0, 7, 8, 9, 10, 20],
        labels=[
            "<7",
            "7-7.9",
            "8-8.9",
            "9-9.9",
            "10+"
        ],
        right=False
    )

    df["baseline_adherence_group"] = pd.cut(
        df["baseline_adherence_pct"],
        bins=[0, 50, 70, 85, 101],
        labels=[
            "<50%",
            "50-69%",
            "70-84%",
            "85%+"
        ],
        right=False
    )

    # Remove unused categorical levels.
    for column in [
        "age_group",
        "bmi_group",
        "baseline_hba1c_group",
        "baseline_adherence_group"
    ]:
        df[column] = df[column].cat.remove_unused_categories()

    return df


def run_interaction_analysis(df, subgroup, label):

    print(f"\n--- {label} ---")

    reduced_formula = (
        f"hba1c_change ~ C(intervention) "
        f"+ C({subgroup}) "
        f"+ baseline_hba1c"
    )

    full_formula = (
        f"hba1c_change ~ C(intervention) "
        f"* C({subgroup}) "
        f"+ baseline_hba1c"
    )

    reduced_model = smf.ols(
        reduced_formula,
        data=df
    ).fit()

    full_model = smf.ols(
        full_formula,
        data=df
    ).fit()

    comparison = anova_lm(
        reduced_model,
        full_model
    )

    p_value = comparison["Pr(>F)"].iloc[1]
    f_stat = comparison["F"].iloc[1]
    df_diff = comparison["df_diff"].iloc[1]

    print(f"Omnibus F-statistic: {f_stat:.4f}")
    print(f"Interaction degrees of freedom: {int(df_diff)}")
    print(f"Raw p-value: {p_value:.3e}")
    print(f"Model R-squared: {full_model.rsquared:.4f}")

    return {
        "Subgroup": label,
        "F-statistic": f_stat,
        "df": df_diff,
        "Raw p-value": p_value,
        "R-squared": full_model.rsquared
    }


def main():

    print("=" * 70)
    print("MedImpact AI - Omnibus Interaction Analysis")
    print("=" * 70)

    df = pd.read_csv(DATA_PATH)

    df = prepare_subgroups(df)

    analyses = [
        ("age_group", "Treatment × Age Group"),
        ("bmi_group", "Treatment × BMI Group"),
        (
            "baseline_hba1c_group",
            "Treatment × Baseline HbA1c Group"
        ),
        (
            "baseline_adherence_group",
            "Treatment × Baseline Adherence Group"
        ),
        ("sex", "Treatment × Sex")
    ]

    results = []

    for subgroup, label in analyses:

        result = run_interaction_analysis(
            df,
            subgroup,
            label
        )

        results.append(result)

    # ---------------------------------------------------------
    # Holm correction across the five omnibus tests
    # ---------------------------------------------------------

    raw_p_values = [
        result["Raw p-value"]
        for result in results
    ]

    _, adjusted_p_values, _, _ = multipletests(
        raw_p_values,
        method="holm"
    )

    for result, adjusted_p in zip(
        results,
        adjusted_p_values
    ):
        result["Holm adjusted p-value"] = adjusted_p

    print("\n" + "=" * 70)
    print("Omnibus Interaction Tests")
    print("=" * 70)

    results_df = pd.DataFrame(results)

    print(
        results_df.to_string(
            index=False,
            formatters={
                "F-statistic": "{:.4f}".format,
                "df": "{:.0f}".format,
                "Raw p-value": lambda x: f"{x:.3e}",
                "R-squared": "{:.4f}".format,
                "Holm adjusted p-value":
                    lambda x: f"{x:.3e}"
            }
        )
    )

    print("\n" + "=" * 70)
    print("Interpretation")
    print("=" * 70)

    print(
        "The omnibus interaction test evaluates whether the "
        "AI-Assisted versus Control association differs across "
        "any level of the specified subgroup variable."
    )

    print(
        "Holm-adjusted p-values account for the five subgroup-level "
        "interaction tests."
    )

    print(
        "A significant interaction does not by itself establish "
        "a causal subgroup effect."
    )

    print(
        "These analyses are exploratory and are based on synthetic data."
    )

    print(
        "The results do not establish clinical efficacy or treatment "
        "effectiveness in real patients."
    )


if __name__ == "__main__":
    main()

