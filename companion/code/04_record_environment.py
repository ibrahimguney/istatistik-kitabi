"""Çalışma ortamını ve üretilen dosyaların SHA-256 özetlerini kaydeder."""

from pathlib import Path
import hashlib
import platform

import matplotlib
import numpy
import pandas
import scipy
import statsmodels


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_environment() -> None:
    lines = [
        f"python={platform.python_version()}",
        f"numpy={numpy.__version__}",
        f"pandas={pandas.__version__}",
        f"scipy={scipy.__version__}",
        f"matplotlib={matplotlib.__version__}",
        f"statsmodels={statsmodels.__version__}",
    ]
    (ROOT / "environment.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest() -> None:
    targets = [
        path
        for folder in (ROOT / "data", ROOT / "outputs")
        for path in folder.rglob("*")
        if path.is_file()
    ]
    lines = ["relative_path,sha256,size_bytes"]
    for path in sorted(targets):
        lines.append(f"{path.relative_to(ROOT)},{sha256(path)},{path.stat().st_size}")
    (ROOT / "manifest_sha256.csv").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    write_environment()
    write_manifest()
    print("Kaydedildi: yazılım ortamı ve dosya bütünlük özeti.")


if __name__ == "__main__":
    main()