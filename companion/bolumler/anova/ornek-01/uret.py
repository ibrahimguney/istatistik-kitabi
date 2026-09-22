import argparse
from pathlib import Path

import pandas as pd


def tablolar():
    return {
        "veri.csv": pd.DataFrame([["A", 10, 70, 6], ["B", 10, 75, 7], ["C", 10, 82, 5]],
                                   columns=["grup", "n", "ortalama", "standart_sapma"]),
        "welch.csv": pd.DataFrame([["A", 12, 70, 3], ["B", 20, 76, 10], ["C", 8, 84, 5]],
                                  columns=["grup", "n", "ortalama", "standart_sapma"]),
        "ciftler.csv": pd.DataFrame([[1, 1, 2], [2, 1, 3], [3, 2, 3]], columns=["cift", "ilk", "ikinci"]),
    }


def main():
    parser = argparse.ArgumentParser(description="Kitabin ANOVA ozetlerini tekrar kaydet; ham veri uretmez")
    parser.add_argument("--cikti", default="yeniden-ozetler")
    secenek = parser.parse_args()
    hedef = Path(secenek.cikti)
    if hedef.is_absolute() or ".." in hedef.parts:
        raise ValueError("Goreli alt klasor gerekli.")
    hedef.mkdir(exist_ok=False)
    for ad, tablo in tablolar().items():
        tablo.to_csv(hedef / ad, index=False, lineterminator="\n")
    print(f"Ozetler kaydedildi: {hedef}; bireysel gozlem uretilmedi.")


if __name__ == "__main__":
    main()