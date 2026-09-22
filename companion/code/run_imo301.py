"""IMO301 ders sürümünün temel veri, analiz ve grafik adımlarını çalıştırır."""

from pathlib import Path
import runpy


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
SCRIPTS = (
    "00_prepare_data.py",
    "01_validate_data.py",
    "02_chapter_examples.py",
    "03_make_figures.py",
    "04_record_environment.py",
)


def main() -> None:
    for script_name in SCRIPTS:
        print(f"Çalıştırılıyor: {script_name}")
        runpy.run_path(SCRIPT_DIRECTORY / script_name, run_name="__main__")


if __name__ == "__main__":
    main()