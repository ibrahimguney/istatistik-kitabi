"""Temiz veri dosyalarının temel yapısal ve mantıksal kontrolleri."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"


def validate_star98() -> None:
    data = pd.read_csv(CLEAN / "star98_districts.csv")
    assert len(data) == 303, "STAR98 satır sayısı beklenenden farklı."
    assert data["district_id"].is_unique, "Okul bölgesi kimlikleri benzersiz değil."
    assert not data.isna().any().any(), "STAR98 temiz verisinde eksik değer var."
    assert (data["tested_count"] > 0).all(), "Sınava giren öğrenci sayısı pozitif olmalı."
    assert data["above_median_rate"].between(0, 1).all(), "Oran 0-1 dışında."
    for column in [
        "low_income_pct",
        "asian_students_pct",
        "black_students_pct",
        "hispanic_students_pct",
        "minority_teachers_pct",
        "college_prep_pct",
        "charter_schools_pct",
        "year_round_schools_pct",
    ]:
        assert data[column].between(0, 100).all(), f"{column} yüzde aralığı dışında."


def validate_spector() -> None:
    data = pd.read_csv(CLEAN / "spector_program.csv")
    assert len(data) == 32, "Spector satır sayısı beklenenden farklı."
    assert data["student_id"].is_unique, "Öğrenci kimlikleri benzersiz değil."
    assert not data.isna().any().any(), "Spector temiz verisinde eksik değer var."
    assert set(data["program_participation"]) <= {0, 1}
    assert set(data["grade_improved"]) <= {0, 1}
    assert data["gpa"].between(0, 4).all(), "GPA 0-4 aralığı dışında."


def main() -> None:
    validate_star98()
    validate_spector()
    print("Doğrulama başarılı: bütün veri kontrolleri geçti.")


if __name__ == "__main__":
    main()