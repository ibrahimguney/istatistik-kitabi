"""Bootstrap ve rastgeleleştirme bölümü için tablo ve grafikleri üretir."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"
SEED = 2026
BLUE = "#1F4E79"
ORANGE = "#B45F06"


def bootstrap_mean(star: pd.DataFrame, rng: np.random.Generator) -> np.ndarray:
    values = star["above_median_rate"].to_numpy()
    repetitions = 10000
    replicates = rng.choice(
        values, size=(repetitions, len(values)), replace=True
    ).mean(axis=1)
    low, high = np.quantile(replicates, [0.025, 0.975])
    pd.DataFrame(
        [
            {
                "sample_n": len(values),
                "repetitions": repetitions,
                "observed_mean": values.mean(),
                "bootstrap_se": replicates.std(ddof=1),
                "percentile_ci_low": low,
                "percentile_ci_high": high,
            }
        ]
    ).to_csv(TABLES / "chapter09_bootstrap_mean.csv", index=False)
    return replicates


def randomization_test(
    spector: pd.DataFrame, rng: np.random.Generator
) -> tuple[np.ndarray, float, float]:
    labels = spector["program_participation"].to_numpy()
    outcome = spector["grade_improved"].to_numpy()
    observed = outcome[labels == 1].mean() - outcome[labels == 0].mean()
    repetitions = 20000
    statistics = np.empty(repetitions)
    for index in range(repetitions):
        shuffled = rng.permutation(labels)
        statistics[index] = (
            outcome[shuffled == 1].mean() - outcome[shuffled == 0].mean()
        )
    extreme = int(np.sum(np.abs(statistics) >= abs(observed)))
    p_value = (extreme + 1) / (repetitions + 1)
    pd.DataFrame(
        [
            {
                "program_n": int(labels.sum()),
                "comparison_n": int(len(labels) - labels.sum()),
                "observed_proportion_difference": observed,
                "repetitions": repetitions,
                "extreme_repetitions": extreme,
                "two_sided_p_value": p_value,
            }
        ]
    ).to_csv(TABLES / "chapter09_randomization_test.csv", index=False)
    return statistics, observed, p_value


def make_figure(
    bootstrap_statistics: np.ndarray,
    randomization_statistics: np.ndarray,
    observed_difference: float,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    axes[0].hist(
        100 * bootstrap_statistics,
        bins=30,
        color="#8FB8D8",
        edgecolor="white",
    )
    axes[0].axvline(
        100 * bootstrap_statistics.mean(),
        color=ORANGE,
        linestyle="--",
        linewidth=2,
        label="Bootstrap merkezi",
    )
    axes[0].set(
        xlabel="Bootstrap ortalaması (%)",
        ylabel="Frekans",
        title="Bootstrap dağılımı",
    )
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].hist(
        randomization_statistics,
        bins=25,
        color="#B8C2CC",
        edgecolor="white",
    )
    axes[1].axvline(
        observed_difference,
        color=BLUE,
        linewidth=2,
        label="Gözlenen fark",
    )
    axes[1].axvline(-observed_difference, color=BLUE, linewidth=2)
    axes[1].set(
        xlabel="Karıştırılmış oran farkı",
        ylabel="Frekans",
        title="Sıfır hipotezi dağılımı",
    )
    axes[1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "chapter09_resampling.png", dpi=200)
    plt.close(fig)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    star = pd.read_csv(CLEAN / "star98_districts.csv")
    spector = pd.read_csv(CLEAN / "spector_program.csv")
    rng = np.random.default_rng(SEED)
    bootstrap_statistics = bootstrap_mean(star, rng)
    randomization_statistics, observed, p_value = randomization_test(
        spector, rng
    )
    make_figure(bootstrap_statistics, randomization_statistics, observed)
    print(f"Bootstrap ve rastgeleleştirme çıktıları üretildi; p={p_value:.4f}.")


if __name__ == "__main__":
    main()