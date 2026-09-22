import argparse
from pathlib import Path
import platform

import numpy as np
import pandas as pd


def uret():
    cerceve = pd.DataFrame({"id": range(1, 13), "sinif": [1] * 4 + [2] * 4 + [3] * 4})
    basit = cerceve.sample(n=6, replace=False, random_state=2026)
    tabakali = cerceve.groupby("sinif", group_keys=False).sample(n=2, replace=False, random_state=2026)
    return cerceve.assign(basit=cerceve["id"].isin(basit["id"]).astype(int),
                         tabakali=cerceve["id"].isin(tabakali["id"]).astype(int))


def main():
    parser = argparse.ArgumentParser(description="B06: kayitli secimleri yeniden uret")
    parser.add_argument("--cikti", default="yeniden-uretilen.csv")
    secenek = parser.parse_args()
    hedef = Path(secenek.cikti)
    if hedef.is_absolute() or ".." in hedef.parts:
        raise ValueError("Ornek klasoru icinde goreli bir cikti yolu gerekli.")
    with hedef.open("x", encoding="utf-8", newline="") as stream:
        uret().to_csv(stream, index=False, lineterminator="\n")
    print(f"Uretildi: {hedef}; her pandas secim cagrisinda random_state=2026")
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}")


if __name__ == "__main__":
    main()