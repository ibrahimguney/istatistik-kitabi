"""Veri hazırlama, doğrulama, analiz ve grafik üretimini sırayla çalıştırır."""

from pathlib import Path
import runpy


HERE = Path(__file__).resolve().parent


def main() -> None:
    for script in (
        "00_prepare_data.py",
        "01_validate_data.py",
        "02_chapter_examples.py",
        "03_make_figures.py",
        "05_resampling_examples.py",
        "06_multiple_regression.py",
        "04_record_environment.py",
    ):
        print(f"\n--- {script} ---")
        runpy.run_path(HERE / script, run_name="__main__")


if __name__ == "__main__":
    main()