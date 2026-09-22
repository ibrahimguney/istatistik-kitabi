"""Kitap bölümlerinde kullanılabilecek ortak sayısal çıktıları üretir."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
SEED = 2026


def descriptive_table(star: pd.DataFrame) -> None:
    columns = ["above_median_rate", "low_income_pct", "pupil_teacher_ratio"]
    summary = star[columns].describe().T
    summary["median"] = star[columns].median()
    summary["iqr"] = star[columns].quantile(0.75) - star[columns].quantile(0.25)
    summary.to_csv(TABLES / "chapter03_descriptive_summary.csv")


def sampling_distribution(star: pd.DataFrame) -> None:
    rng = np.random.default_rng(SEED)
    population = star["above_median_rate"].to_numpy()
    rows = []
    for n in (10, 30, 100):
        means = np.array(
            [rng.choice(population, size=n, replace=True).mean() for _ in range(5000)]
        )
        rows.append(
            {
                "sample_size": n,
                "simulation_repetitions": len(means),
                "mean_of_means": means.mean(),
                "empirical_se": means.std(ddof=1),
                "theoretical_se": population.std(ddof=0) / np.sqrt(n),
            }
        )
    pd.DataFrame(rows).to_csv(
        TABLES / "chapter04_sampling_distribution.csv", index=False
    )


def confidence_interval(star: pd.DataFrame) -> None:
    values = star["above_median_rate"].to_numpy()
    n = len(values)
    mean = values.mean()
    se = values.std(ddof=1) / np.sqrt(n)
    critical = stats.t.ppf(0.975, df=n - 1)
    result = pd.DataFrame(
        [
            {
                "n": n,
                "mean": mean,
                "standard_error": se,
                "ci_low": mean - critical * se,
                "ci_high": mean + critical * se,
            }
        ]
    )
    result.to_csv(TABLES / "chapter08_mean_ci.csv", index=False)


def welch_and_crosstab(spector: pd.DataFrame) -> None:
    program = spector.loc[
        spector["program_participation"] == 1, "pre_program_test"
    ]
    comparison = spector.loc[
        spector["program_participation"] == 0, "pre_program_test"
    ]
    welch = stats.ttest_ind(program, comparison, equal_var=False)
    pd.DataFrame(
        [
            {
                "program_n": len(program),
                "program_mean": program.mean(),
                "comparison_n": len(comparison),
                "comparison_mean": comparison.mean(),
                "welch_t": welch.statistic,
                "p_value": welch.pvalue,
            }
        ]
    ).to_csv(TABLES / "chapter11_welch.csv", index=False)

    observed = pd.crosstab(
        spector["program_group"], spector["improvement_label"]
    )
    observed.to_csv(TABLES / "chapter12_observed_counts.csv")
    odds_ratio, fisher_p = stats.fisher_exact(observed.to_numpy())
    pd.DataFrame(
        [{"odds_ratio": odds_ratio, "fisher_two_sided_p": fisher_p}]
    ).to_csv(TABLES / "chapter12_fisher.csv", index=False)


def correlation_regression(star: pd.DataFrame) -> None:
    x = star["low_income_pct"].to_numpy()
    y = star["above_median_rate"].to_numpy()
    correlation = stats.pearsonr(x, y)
    fit = stats.linregress(x, y)
    pd.DataFrame(
        [
            {
                "n": len(star),
                "pearson_r": correlation.statistic,
                "correlation_p": correlation.pvalue,
                "intercept": fit.intercept,
                "slope": fit.slope,
                "slope_se": fit.stderr,
                "r_squared": fit.rvalue**2,
            }
        ]
    ).to_csv(TABLES / "chapter13_regression.csv", index=False)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    star = pd.read_csv(CLEAN / "star98_districts.csv")
    spector = pd.read_csv(CLEAN / "spector_program.csv")
    descriptive_table(star)
    sampling_distribution(star)
    confidence_interval(star)
    welch_and_crosstab(spector)
    correlation_regression(star)
    print("Üretildi: bölüm örnekleri için sayısal çıktı tabloları.")


if __name__ == "__main__":
    main()