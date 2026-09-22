"""Ortak verilerden kitapta kullanılabilecek erişilebilir grafikler üretir."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
FIGURES = ROOT / "outputs" / "figures"
BLUE = "#1F4E79"
ORANGE = "#B45F06"
GRAY = "#555555"


def save_histogram(star: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(
        100 * star["above_median_rate"],
        bins=18,
        color="#8FB8D8",
        edgecolor="white",
    )
    ax.axvline(
        100 * star["above_median_rate"].median(),
        color=ORANGE,
        linestyle="--",
        label="Medyan",
    )
    ax.set(xlabel="Ulusal medyanın üzerindeki öğrenciler (%)", ylabel="Okul bölgesi sayısı")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "chapter03_star98_distribution.png", dpi=200)
    plt.close(fig)


def save_sampling_plot(star: pd.DataFrame) -> None:
    rng = np.random.default_rng(2026)
    population = star["above_median_rate"].to_numpy()
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, n in zip(axes, (10, 30, 100)):
        means = np.array(
            [rng.choice(population, size=n, replace=True).mean() for _ in range(5000)]
        )
        ax.hist(means, bins=25, color="#8FB8D8", edgecolor="white")
        ax.axvline(population.mean(), color=ORANGE, linestyle="--")
        ax.set_title(f"n = {n}")
        ax.set_xlabel("Örneklem ortalaması")
    axes[0].set_ylabel("Frekans")
    fig.tight_layout()
    fig.savefig(FIGURES / "chapter04_sampling_means.png", dpi=200)
    plt.close(fig)


def save_categorical_plot(spector: pd.DataFrame) -> None:
    table = pd.crosstab(
        spector["program_group"],
        spector["improvement_label"],
        normalize="index",
    )
    table = table[["not_improved", "improved"]]
    ax = table.plot(
        kind="bar",
        stacked=True,
        color=["#B8C2CC", BLUE],
        figsize=(6.5, 4),
    )
    ax.set(xlabel="Program grubu", ylabel="Grup içi oran", ylim=(0, 1))
    ax.legend(["İyileşmedi", "İyileşti"], frameon=False)
    ax.set_xticklabels(["Karşılaştırma", "Program"])
    ax.tick_params(axis="x", rotation=0)
    ax.figure.tight_layout()
    ax.figure.savefig(FIGURES / "chapter12_program_improvement.png", dpi=200)
    plt.close(ax.figure)


def save_regression_diagnostics(star: pd.DataFrame) -> None:
    x = star["low_income_pct"].to_numpy()
    y = 100 * star["above_median_rate"].to_numpy()
    fit = stats.linregress(x, y)
    fitted = fit.intercept + fit.slope * x
    residuals = y - fitted

    order = np.argsort(x)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    axes[0].scatter(x, y, color=BLUE, alpha=0.7, marker="o")
    axes[0].plot(x[order], fitted[order], color=ORANGE, linewidth=2)
    axes[0].set(
        xlabel="Düşük gelirli öğrenciler (%)",
        ylabel="Ulusal medyanın üzerindeki öğrenciler (%)",
    )
    axes[1].scatter(fitted, residuals, color=BLUE, alpha=0.7, marker="o")
    axes[1].axhline(0, color=ORANGE, linestyle="--")
    axes[1].set(xlabel="Uydurulan değer", ylabel="Artık")
    fig.tight_layout()
    fig.savefig(FIGURES / "chapter13_regression_diagnostics.png", dpi=200)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    star = pd.read_csv(CLEAN / "star98_districts.csv")
    spector = pd.read_csv(CLEAN / "spector_program.csv")
    save_histogram(star)
    save_sampling_plot(star)
    save_categorical_plot(spector)
    save_regression_diagnostics(star)
    print("Üretildi: dört ortak veri grafiği.")


if __name__ == "__main__":
    main()