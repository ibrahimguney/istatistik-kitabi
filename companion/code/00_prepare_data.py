"""Gerçek eğitim verilerini ham ve temiz CSV dosyalarına dönüştürür."""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
DICTIONARIES = ROOT / "data" / "dictionaries"


def ensure_directories() -> None:
    for directory in (RAW, CLEAN, DICTIONARIES):
        directory.mkdir(parents=True, exist_ok=True)


def prepare_star98() -> None:
    module = sm.datasets.star98
    original = module.load_pandas().data.copy()
    original.insert(0, "DISTRICT_ID", np.arange(1, len(original) + 1))
    original.to_csv(RAW / "star98_statsmodels.csv", index=False)

    clean = original[
        [
            "DISTRICT_ID",
            "NABOVE",
            "NBELOW",
            "LOWINC",
            "PERASIAN",
            "PERBLACK",
            "PERHISP",
            "PERMINTE",
            "AVYRSEXP",
            "AVSALK",
            "PERSPENK",
            "PTRATIO",
            "PCTAF",
            "PCTCHRT",
            "PCTYRRND",
        ]
    ].rename(
        columns={
            "DISTRICT_ID": "district_id",
            "NABOVE": "above_median_count",
            "NBELOW": "below_median_count",
            "LOWINC": "low_income_pct",
            "PERASIAN": "asian_students_pct",
            "PERBLACK": "black_students_pct",
            "PERHISP": "hispanic_students_pct",
            "PERMINTE": "minority_teachers_pct",
            "AVYRSEXP": "teacher_experience_years",
            "AVSALK": "teacher_salary_thousands",
            "PERSPENK": "spending_per_pupil_thousands",
            "PTRATIO": "pupil_teacher_ratio",
            "PCTAF": "college_prep_pct",
            "PCTCHRT": "charter_schools_pct",
            "PCTYRRND": "year_round_schools_pct",
        }
    )
    clean["tested_count"] = (
        clean["above_median_count"] + clean["below_median_count"]
    ).astype(int)
    clean["above_median_rate"] = (
        clean["above_median_count"] / clean["tested_count"]
    )
    clean["low_income_group"] = pd.qcut(
        clean["low_income_pct"],
        q=3,
        labels=["low", "middle", "high"],
        duplicates="drop",
    )
    clean["charter_group"] = np.where(
        clean["charter_schools_pct"] > 0, "has_charter", "no_charter"
    )
    clean.to_csv(CLEAN / "star98_districts.csv", index=False)

    dictionary = pd.DataFrame(
        [
            ("district_id", "Okul bölgesi sıra kimliği", "identifier", "none"),
            ("above_median_count", "Matematikte ulusal medyanın üzerindeki öğrenci sayısı", "count", "student"),
            ("below_median_count", "Matematikte ulusal medyanın altındaki öğrenci sayısı", "count", "student"),
            ("tested_count", "İki sonuç sayısının toplamı", "count", "student"),
            ("above_median_rate", "Ulusal medyanın üzerindeki öğrencilerin oranı", "proportion", "0-1"),
            ("low_income_pct", "Düşük gelirli öğrencilerin yüzdesi", "continuous", "percent"),
            ("asian_students_pct", "Asyalı öğrencilerin yüzdesi", "continuous", "percent"),
            ("black_students_pct", "Siyah öğrencilerin yüzdesi", "continuous", "percent"),
            ("hispanic_students_pct", "Hispanik öğrencilerin yüzdesi", "continuous", "percent"),
            ("minority_teachers_pct", "Azınlık grubundaki öğretmenlerin yüzdesi", "continuous", "percent"),
            ("teacher_experience_years", "Öğretmenlerin ortalama hizmet yılı", "continuous", "year"),
            ("teacher_salary_thousands", "Öğretmen başına maaş ve yan hak bütçesi", "continuous", "thousand_currency_units"),
            ("spending_per_pupil_thousands", "Öğrenci başına harcama", "continuous", "thousand_currency_units"),
            ("pupil_teacher_ratio", "Öğrenci-öğretmen oranı", "continuous", "students_per_teacher"),
            ("college_prep_pct", "Üniversite hazırlık dersi alanların yüzdesi", "continuous", "percent"),
            ("charter_schools_pct", "Charter okullarının yüzdesi", "continuous", "percent"),
            ("year_round_schools_pct", "Yıl boyu eğitim veren okulların yüzdesi", "continuous", "percent"),
            ("low_income_group", "Düşük gelir yüzdesinin üçte birlik grubu", "ordinal", "low/middle/high"),
            ("charter_group", "Bölgede charter okul bulunma durumu", "nominal", "has_charter/no_charter"),
        ],
        columns=["variable", "description_tr", "measurement_type", "unit_or_levels"],
    )
    dictionary.to_csv(DICTIONARIES / "star98_dictionary.csv", index=False)


def prepare_spector() -> None:
    module = sm.datasets.spector
    original = module.load_pandas().data.copy()
    original.insert(0, "STUDENT_ID", np.arange(1, len(original) + 1))
    original.to_csv(RAW / "spector_statsmodels.csv", index=False)

    clean = original.rename(
        columns={
            "STUDENT_ID": "student_id",
            "GPA": "gpa",
            "TUCE": "pre_program_test",
            "PSI": "program_participation",
            "GRADE": "grade_improved",
        }
    )
    clean["program_participation"] = clean["program_participation"].astype(int)
    clean["grade_improved"] = clean["grade_improved"].astype(int)
    clean["program_group"] = clean["program_participation"].map(
        {0: "comparison", 1: "program"}
    )
    clean["improvement_label"] = clean["grade_improved"].map(
        {0: "not_improved", 1: "improved"}
    )
    clean.to_csv(CLEAN / "spector_program.csv", index=False)

    dictionary = pd.DataFrame(
        [
            ("student_id", "Öğrenci sıra kimliği", "identifier", "none"),
            ("gpa", "Not ortalaması", "continuous", "original scale"),
            ("pre_program_test", "Programa ilişkin ekonomi testi puanı", "continuous", "score"),
            ("program_participation", "Programa katılım göstergesi", "binary", "0/1"),
            ("grade_improved", "Notun iyileşme göstergesi", "binary", "0/1"),
            ("program_group", "Programa katılım etiketi", "nominal", "comparison/program"),
            ("improvement_label", "Not iyileşmesi etiketi", "nominal", "not_improved/improved"),
        ],
        columns=["variable", "description_tr", "measurement_type", "unit_or_levels"],
    )
    dictionary.to_csv(DICTIONARIES / "spector_dictionary.csv", index=False)


def write_provenance() -> None:
    blocks = []
    for name, module in (
        ("STAR98", sm.datasets.star98),
        ("SPECTOR", sm.datasets.spector),
    ):
        blocks.append(
            "\n".join(
                [
                    f"[{name}]",
                    f"title: {module.TITLE.strip()}",
                    f"source: {module.SOURCE.strip()}",
                    f"copyright: {module.COPYRIGHT.strip()}",
                ]
            )
        )
    (DICTIONARIES / "provenance.txt").write_text(
        "\n\n".join(blocks) + "\n", encoding="utf-8"
    )


def main() -> None:
    ensure_directories()
    prepare_star98()
    prepare_spector()
    write_provenance()
    print("Hazırlandı: STAR98 ve Spector ham/temiz veri dosyaları.")


if __name__ == "__main__":
    main()