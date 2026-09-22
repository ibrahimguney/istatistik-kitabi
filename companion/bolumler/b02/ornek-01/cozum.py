import argparse
import math
import platform

import pandas as pd


def hazirla(veri):
    if list(veri.columns) != ["okul_turu", "sinif", "puan"]:
        raise ValueError("CSV sutunlari ve sirasi veri sozluguyle uyusmuyor.")
    if veri.empty or veri.isna().any().any():
        raise ValueError("Bu pilot bos veri veya eksik hucre kabul etmiyor.")
    if not veri["okul_turu"].isin(["Devlet", "Ozel"]).all():
        raise ValueError("Okul turu Devlet veya Ozel olmali.")
    veri = veri.copy()
    for alan in ["sinif", "puan"]:
        veri[alan] = pd.to_numeric(veri[alan], errors="raise")
        if not veri[alan].map(math.isfinite).all():
            raise ValueError("Sayisal girdiler sonlu olmali.")
    if not veri["sinif"].isin([1, 2, 3]).all():
        raise ValueError("Sinif kodlari 1, 2 veya 3 olmali.")
    veri["okul_turu"] = pd.Categorical(
        veri["okul_turu"], categories=["Devlet", "Ozel"], ordered=False
    )
    veri["sinif"] = pd.Categorical(
        veri["sinif"], categories=[1, 2, 3], ordered=True
    )
    return veri


def hesapla(veri):
    veri = hazirla(veri)
    satirlar = [
        ("veri", "satir_sayisi", len(veri)),
        ("veri", "degisken_sayisi", len(veri.columns)),
    ]
    for alan in ["okul_turu", "sinif", "puan"]:
        satirlar.extend([
            (alan, "gecerli", veri[alan].count()),
            (alan, "eksik", veri[alan].isna().sum()),
        ])
    for alan in ["okul_turu", "sinif"]:
        for kategori in veri[alan].cat.categories:
            frekans = (veri[alan] == kategori).sum()
            satirlar.extend([
                (alan, str(kategori) + "_frekans", frekans),
                (alan, str(kategori) + "_oran", frekans / len(veri)),
            ])
    satirlar.extend([
        ("puan", "ortalama", veri["puan"].mean()),
        ("puan", "en_kucuk", veri["puan"].min()),
        ("puan", "en_buyuk", veri["puan"].max()),
    ])
    for okul in ["Devlet", "Ozel"]:
        grup = veri.loc[veri["okul_turu"] == okul, "puan"]
        satirlar.append(("puan", okul + "_ortalama", grup.mean()))
    return pd.DataFrame(satirlar, columns=["degisken", "olcu", "deger"])


def main():
    parser = argparse.ArgumentParser(description="B02 okul, sinif ve puan cozumu")
    parser.add_argument("--check", action="store_true",
                        help="Ozgun veri icin beklenen sonuclari denetle")
    args = parser.parse_args()
    veri = pd.read_csv("veri.csv", dtype={"okul_turu": "string"})
    sonuc = hesapla(veri)
    print(f"Python {platform.python_version()} | pandas {pd.__version__}")
    print(sonuc.to_string(index=False))
    if args.check:
        beklenen = pd.read_csv("beklenen-sonuclar.csv")
        anahtarlar = ["degisken", "olcu"]
        if not sonuc[anahtarlar].equals(beklenen[anahtarlar]):
            raise ValueError("Beklenen sonuc satirlari veya sirasi farkli.")
        for hesaplanan, hedef in zip(sonuc["deger"], beklenen["deger"]):
            if not math.isclose(hesaplanan, hedef, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError(f"Sonuc uyusmazligi: {hesaplanan} != {hedef}")
        print(f"DOGRULANDI: {len(beklenen)} kontrol degeri eslesiyor.")


if __name__ == "__main__":
    main()