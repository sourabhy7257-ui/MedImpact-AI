import pandas as pd
import numpy as np
from scipy import stats


DATA_PATH = "data/synthetic/diabetes_longitudinal_data.csv"


def compare_subgroups(df, column, label):
    print(f"\n--- {label} ---")

    results = []

    for subgroup in df[column].dropna().unique():

        subset = df[df[column] == subgroup]

        ai = subset.loc[
            subset["intervention"] == "AI_Assisted",
            "hba1c_change"
        ].dropna()

        control = subset.loc[
            subset["intervention"] == "Control",
            "hba1c_change"
        ].dropna()

        if len(ai) < 20 or len(control) < 20:
            continue

        ai_mean = ai.mean()
        control_mean = control.mean()
        difference = ai_mean - control_mean

        ai_var = ai.var(ddof=1)
        control_var = control.var(ddof=1)

        se = np.sqrt(
            ai_var / len(ai) +
            control_var / len(control)
        )

        numerator = (
            ai_var / len(ai) +
            control_var / len(control)
        ) ** 2

        denominator = (
            (ai_var / len(ai)) ** 2 / (len(ai) - 1)
            + (control_var / len(control)) ** 2 / (len(control) - 1)
        )

        df_welch = numerator / denominator

        t_stat = difference / se

        p_value = 2 * stats.t.sf(
            abs(t_stat),
            df=df_welch
        )

        critical_value = stats.t.ppf(
            0.975,
            df_welch
        )

        ci_lower = difference - critical_value * se
        ci_upper = difference + critical_value * se

        results.append({
            "Subgroup": subgroup,
            "AI n": len(ai),
            "Control n": len(control),
            "AI Mean": ai_mean,
            "Control Mean": control_mean,
            "Difference": difference,
            "CI Lower": ci_lower,
            "CI Upper": ci_upper,
            "p-value": p_value
        })

    results_df = pd.DataFrame(results)

    if not results_df.empty:
        print(
            results_df.to_string(
                index=False,
                formatters={
                    "AI Mean": "{:.3f}".format,
                    "Control Mean": "{:.3f}".format,
                    "Difference": "{:.3f}".format,
                    "CI Lower": "{:.3f}".format,
                    "CI Upper": "{:.3f}".format,
                    "p-value": lambda x: f"{x:.3e}"
                }
            )
        )

    return results_df


def main():

    print("=" * 70)
    print("MedImpact AI - Subgroup Analysis")
    print("=" * 70)

    df = pd.read_csv(DATA_PATH)

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
        labels=["<7", "7-7.9", "8-8.9", "9-9.9", "10+"],
        right=False
    )

    df["baseline_adherence_group"] = pd.cut(
        df["baseline_adherence_pct"],
        bins=[0, 50, 70, 85, 101],
        labels=["<50%", "50-69%", "70-84%", "85%+"],
        right=False
    )

    compare_subgroups(
        df,
        "age_group",
        "Observed HbA1c Change by Age Group"
    )

    compare_subgroups(
        df,
        "bmi_group",
        "Observed HbA1c Change by BMI Group"
    )

    compare_subgroups(
        df,
        "baseline_hba1c_group",
        "Observed HbA1c Change by Baseline HbA1c"
    )

    compare_subgroups(
        df,
        "baseline_adherence_group",
        "Observed HbA1c Change by Baseline Adherence"
    )

    compare_subgroups(
        df,
        "sex",
        "Observed HbA1c Change by Sex"
    )

    print("\n" + "=" * 70)
    print("Interpretation")
    print("=" * 70)

    print(
        "Differences represent AI-Assisted minus Control observed changes."
    )

    print(
        "Negative values indicate greater observed HbA1c reduction "
        "in the AI-Assisted group."
    )

    print(
        "Confidence intervals and p-values describe uncertainty under "
        "the assumptions of the Welch comparison."
    )

    print(
        "These subgroup comparisons do not establish causal effects "
        "or clinical efficacy in real patients."
    )

    print(
        "Formal interaction modeling is required before concluding "
        "that intervention effects differ between subgroups."
    )

    print(
        "The dataset is synthetic and intended for research and "
        "educational demonstration only."
    )


if __name__ == "__main__":
    main()

