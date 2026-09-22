import argparse
from pathlib import Path

import pandas as pd


def uret():
    veri = pd.DataFrame([(saat, gun) for gun in [0, 1, 2] for saat in [2, 4, 6, 8]],
                        columns=["saat", "devamsizlik"])
    hata = [1, -1, -1, 1, -2, 2, 2, -2, 1, -1, -1, 1]
    veri["puan"] = 40 + 2 * veri.saat - 3 * veri.devamsizlik + hata
    return veri


def main():
    parser = argparse.ArgumentParser(description="Kitaptaki deterministik ogretim verisini uret")
    parser.add_argument("--cikti", default="yeniden-veri.csv")
    secenek = parser.parse_args()
    hedef = Path(secenek.cikti)
    if hedef.is_absolute() or ".." in hedef.parts:
        raise ValueError("Goreli bir cikti yolu gerekli.")
    with hedef.open("x", encoding="utf-8", newline="") as stream:
        uret().to_csv(stream, index=False, lineterminator="\n")
    print(f"Uretildi: {hedef}; deterministik hata dizisi, rassal cekim yok.")


if __name__ == "__main__":
    main()