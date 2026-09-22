import argparse
import math
import platform

import pandas as pd


def hesapla(veri):
    if list(veri.columns) != ["devam_saati", "basari", "program"]:
        raise ValueError("CSV sutunlari ve sirasi veri sozluguyle uyusmuyor.")
    if veri.empty or veri.isna().any().any():
        raise ValueError("Bu ornek bos veri veya eksik hucre kabul etmiyor.")
    if not veri["program"].isin(["A", "B"]).all():
        raise ValueError("Program etiketleri A veya B olmali.")
    veri = veri.copy()
    for alan in ["devam_saati", "basari"]:
        veri[alan] = pd.to_numeric(veri[alan], errors="raise")
        if not veri[alan].map(math.isfinite).all():
            raise ValueError("Sayisal degerler sonlu olmali.")
    if (veri["devam_saati"] < 0).any():
        raise ValueError("Devam suresi negatif olamaz.")
    veri["program"] = pd.Categorical(veri["program"], categories=["A", "B"])
    satirlar = [
        ("veri", "satir_sayisi", len(veri)),
        ("veri", "degisken_sayisi", len(veri.columns)),
    ]
    for alan in ["devam_saati", "basari"]:
        degerler = veri[alan]
        satirlar.extend([
            (alan, "gecerli", degerler.count()),
            (alan, "eksik", degerler.isna().sum()),
            (alan, "ortalama", degerler.mean()),
            (alan, "en_kucuk", degerler.min()),
            (alan, "en_buyuk", degerler.max()),
        ])
    satirlar.extend([
        ("program", "gecerli", veri["program"].count()),
        ("program", "eksik", veri["program"].isna().sum()),
    ])
    for program in ["A", "B"]:
        frekans = (veri["program"] == program).sum()
        satirlar.extend([
            ("program", program + "_frekans", frekans),
            ("program", program + "_oran", frekans / len(veri)),
        ])
    return pd.DataFrame(satirlar, columns=["degisken", "olcu", "deger"])


def main():
    parser = argparse.ArgumentParser(description="B01 ortak CSV cozumu")
    parser.add_argument("--check", action="store_true",
                        help="Sonuclari beklenen degerlerle karsilastir")
    args = parser.parse_args()
    veri = pd.read_csv("veri.csv", dtype={"program": "string"})
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