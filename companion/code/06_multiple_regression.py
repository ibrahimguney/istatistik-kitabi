"""Çoklu regresyon bölümü için gerçek veri analizi ve tanı grafiği."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"
BLUE = "#1F4E79"
ORANGE = "#B45F06"

PREDICTORS = [
    "low_income_pct",
    "pupil_teacher_ratio",
    "teacher_experience_years",
    "spending_per_pupil_thousands",
    "college_prep_pct",
]

DISPLAY_LABELS = {
    "low_income_pct": "Düşük gelir (%)",
    "pupil_teacher_ratio": "Öğrenci/öğretmen",
    "teacher_experience_years": "Öğretmen deneyimi",
    "spending_per_pupil_thousands": "Öğrenci başına harcama",
    "college_prep_pct": "Üniversite hazırlık (%)",
}


def fit_model(data: pd.DataFrame):
    y = 100 * data["above_median_rate"]
    x = sm.add_constant(data[PREDICTORS])
    return sm.OLS(y, x).fit(), x, y


def save_tables(model, x: pd.DataFrame) -> None:
    interval = model.conf_int()
    coefficients = pd.DataFrame(
        {
            "term": model.params.index,
            "estimate": model.params.values,
            "standard_error": model.bse.values,
            "t_value": model.tvalues.values,
            "p_value": model.pvalues.values,
            "ci_low": interval[0].values,
            "ci_high": interval[1].values,
        }
    )
    coefficients.to_csv(TABLES / "chapter15_multiple_coefficients.csv", index=False)

    summary = pd.DataFrame(
        [
            {
                "n": int(model.nobs),
                "predictor_count": int(model.df_model),
                "r_squared": model.rsquared,
                "adjusted_r_squared": model.rsquared_adj,
                "f_value": model.fvalue,
                "model_p_value": model.f_pvalue,
                "residual_standard_error": np.sqrt(model.mse_resid),
            }
        ]
    )
    summary.to_csv(TABLES / "chapter15_multiple_summary.csv", index=False)

    vif = pd.DataFrame(
        {
            "term": PREDICTORS,
            "vif": [
                variance_inflation_factor(x.to_numpy(), index)
                for index in range(1, len(PREDICTORS) + 1)
            ],
        }
    )
    vif.to_csv(TABLES / "chapter15_vif.csv", index=False)


def save_figure(model) -> None:
    terms = PREDICTORS
    estimates = model.params[terms].to_numpy()
    intervals = model.conf_int().loc[terms]
    lower = estimates - intervals[0].to_numpy()
    upper = intervals[1].to_numpy() - estimates
    positions = np.arange(len(terms))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    axes[0].errorbar(
        estimates,
        positions,
        xerr=np.vstack([lower, upper]),
        fmt="o",
        color=BLUE,
        ecolor=BLUE,
        capsize=3,
    )
    axes[0].axvline(0, color=ORANGE, linestyle="--")
    axes[0].set_yticks(positions)
    axes[0].set_yticklabels([DISPLAY_LABELS[term] for term in terms])
    axes[0].invert_yaxis()
    axes[0].set(xlabel="Katsayı ve yüzde 95 güven aralığı", title="Ayarlanmış katsayılar")

    axes[1].scatter(model.fittedvalues, model.resid, color=BLUE, alpha=0.7)
    axes[1].axhline(0, color=ORANGE, linestyle="--")
    axes[1].set(
        xlabel="Uydurulan başarı yüzdesi",
        ylabel="Artık",
        title="Artık--uydurulan değer grafiği",
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "chapter15_multiple_regression.png", dpi=200)
    plt.close(fig)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(CLEAN / "star98_districts.csv")
    model, x, _ = fit_model(data)
    save_tables(model, x)
    save_figure(model)
    print(
        "Çoklu regresyon çıktıları üretildi: "
        f"R2={model.rsquared:.3f}, düzeltilmiş R2={model.rsquared_adj:.3f}."
    )


if __name__ == "__main__":
    main()