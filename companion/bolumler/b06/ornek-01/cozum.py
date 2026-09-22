import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd


def hazirla(veri):
    if list(veri.columns) != ["id", "sinif", "basit", "tabakali"] or len(veri) != 12:
        raise ValueError("Bu pilot dort sutunlu, 12 kisilik cerceveyi bekler.")
    if veri.isna().any().any():
        raise ValueError("Eksik deger kabul edilmez.")
    for sutun in veri.columns:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal sutunlar gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Sonlu degerler gerekli.")
    temiz = veri.sort_values("id").reset_index(drop=True).copy(deep=True)
    if not np.array_equal(temiz["id"], np.arange(1, 13)):
        raise ValueError("Kimlikler 1..12 arasinda benzersiz olmali.")
    if not np.array_equal(temiz["sinif"], np.repeat([1, 2, 3], 4)):
        raise ValueError("Kimlik-sinif eslesmesi kitap cercevesiyle uyusmuyor.")
    if not temiz[["basit", "tabakali"]].isin([0, 1]).all().all():
        raise ValueError("Secim gostergeleri 0 veya 1 olmali.")
    if temiz["basit"].sum() != 6:
        raise ValueError("Basit secimde alti farkli birim gerekli.")
    adetler = temiz.groupby("sinif")["tabakali"].sum()
    if not (adetler == 2).all():
        raise ValueError("Tabakali secimde her siniftan iki birim gerekli.")
    temiz = temiz.astype(int)
    temiz["sinif"] = pd.Categorical(temiz["sinif"], categories=[1, 2, 3], ordered=True)
    return temiz


def hesapla(veri):
    temiz = hazirla(veri)
    satirlar = [("cerceve", "hacim", len(temiz)),
                ("cerceve", "benzersiz_id", temiz["id"].nunique()),
                ("cerceve", "sinif_sayisi", temiz["sinif"].nunique())]
    for tasarim in ["basit", "tabakali"]:
        secilen = temiz[temiz[tasarim] == 1]
        olasilik = len(secilen) / len(temiz) if tasarim == "basit" else 2 / 4
        agirlik = 1 / olasilik
        satirlar.extend([(tasarim, "orneklem_hacmi", len(secilen)),
                         (tasarim, "dahil_edilme_olasiligi", olasilik),
                         (tasarim, "tasarim_agirligi", agirlik),
                         (tasarim, "agirlik_toplami", len(secilen) * agirlik)])
        for sinif in [1, 2, 3]:
            satirlar.append((tasarim, f"sinif_{sinif}_frekans", (secilen["sinif"] == sinif).sum()))
        satirlar.extend((tasarim, f"secilen_id_{sira}", kimlik)
                        for sira, kimlik in enumerate(secilen["id"], start=1))
    return pd.DataFrame(satirlar, columns=["degisken", "olcu", "deger"])


def kontrol_et(sonuc, beklenen):
    if list(beklenen.columns) != ["degisken", "olcu", "deger"]:
        raise ValueError("Kontrol sutunlari uyusmuyor.")
    if not sonuc[["degisken", "olcu"]].equals(beklenen[["degisken", "olcu"]]):
        raise ValueError("Kontrol etiketleri veya sirasi uyusmuyor.")
    hedefler = pd.to_numeric(beklenen["deger"], errors="raise")
    if not np.isfinite(hedefler).all() or not np.isfinite(sonuc["deger"]).all():
        raise ValueError("Sonlu kontrol degerleri gerekli.")
    for gercek, hedef in zip(sonuc["deger"], hedefler):
        if not math.isclose(gercek, hedef, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(f"Kontrol uyusmazligi: {gercek} != {hedef}")
    print(f"DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.")


def grafik_kaydet(veri):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    temiz = hazirla(veri)
    fig, eksen = plt.subplots(figsize=(10, 3.5))
    for konum, tasarim, renk in [(2, None, "#555555"), (1, "basit", "#1F4E79"), (0, "tabakali", "#087F5B")]:
        eksen.scatter(temiz["id"], [konum] * 12, s=120, facecolors="white", edgecolors="#AAAAAA")
        secilen = temiz if tasarim is None else temiz[temiz[tasarim] == 1]
        eksen.scatter(secilen["id"], [konum] * len(secilen), s=120, color=renk)
    for sinir in [4.5, 8.5]:
        eksen.axvline(sinir, color="#BBBBBB", linestyle=":")
    for merkez, sinif in [(2.5, 1), (6.5, 2), (10.5, 3)]:
        eksen.text(merkez, 2.4, f"Sinif {sinif}", ha="center")
    eksen.set(xlim=(0.5, 12.5), ylim=(-0.5, 2.8), xticks=range(1, 13),
              yticks=[0, 1, 2], yticklabels=["Tabakali", "Basit rastgele", "Cerceve"],
              xlabel="Yapay ogrenci kimligi", title="Kayitli secimler: dolu nokta secilen birimi gosterir")
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "secim-haritasi.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/secim-haritasi.png")


def main():
    parser = argparse.ArgumentParser(description="B06: kayitli basit ve tabakali secimleri cozumle")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri = pd.read_csv("veri.csv")
    sonuc = hesapla(veri)
    print(sonuc.to_string(index=False))
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(veri)
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}")


if __name__ == "__main__":
    main()