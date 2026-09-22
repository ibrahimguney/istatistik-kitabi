import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


GRUPLAR = ["Birinci", "Ikinci"]
SONUCLAR = ["Basarili", "Basarisiz"]
ALFA = 0.05


def hazirla(veri):
    if list(veri.columns) != ["grup", "sonuc", "frekans"] or len(veri) != 4:
        raise ValueError("Dort hucre ve grup, sonuc, frekans sutunlari gerekli.")
    if veri.isna().any().any() or veri.duplicated(["grup", "sonuc"]).any():
        raise ValueError("Eksik veya yinelenen hucre kabul edilmez.")
    hucreler = pd.MultiIndex.from_product([GRUPLAR, SONUCLAR], names=["grup", "sonuc"])
    if set(zip(veri.grup, veri.sonuc)) != set(hucreler):
        raise ValueError("Grup/sonuc etiketleri beklenen 2x2 tabloya uymuyor.")
    if not pd.api.types.is_numeric_dtype(veri.frekans) or pd.api.types.is_bool_dtype(veri.frekans):
        raise ValueError("Frekanslar sayisal tam sayi olmali.")
    sayilar = veri.frekans.to_numpy(dtype=float)
    if not np.isfinite(sayilar).all() or (sayilar < 0).any() or (sayilar != np.floor(sayilar)).any():
        raise ValueError("Frekanslar sonlu, negatif olmayan tam sayilar olmali.")
    temiz = veri.set_index(["grup", "sonuc"]).reindex(hucreler).reset_index().copy(deep=True)
    gozlenen = temiz.frekans.to_numpy(dtype=float).reshape(2, 2)
    if (gozlenen.sum(axis=0) <= 0).any() or (gozlenen.sum(axis=1) <= 0).any():
        raise ValueError("Bos satir veya sutunla bagimsizlik testi yapilamaz.")
    return temiz


def tablolar(veri):
    temiz = hazirla(veri)
    gozlenen = temiz.frekans.to_numpy(dtype=float).reshape(2, 2)
    beklenen = np.outer(gozlenen.sum(axis=1), gozlenen.sum(axis=0)) / gozlenen.sum()
    if (beklenen < 5).any():
        raise ValueError("Bu pilot tum beklenen frekanslari >=5 ister; seyrek tabloda uygun kesin yontemi degerlendirin.")
    ki_kare, p_degeri, serbestlik, beklenen = stats.chi2_contingency(gozlenen, correction=False)
    katki = (gozlenen - beklenen) ** 2 / beklenen
    artik = (gozlenen - beklenen) / np.sqrt(beklenen)
    oran = gozlenen / gozlenen.sum(axis=1, keepdims=True)
    return gozlenen, beklenen, katki, artik, oran, float(ki_kare), float(p_degeri), int(serbestlik)


def hesapla(veri):
    gozlenen, beklenen, katki, artik, oran, ki_kare, p_degeri, serbestlik = tablolar(veri)
    hucre_adlari = [f"{grup}_{sonuc}" for grup in GRUPLAR for sonuc in SONUCLAR]
    rows = []
    for ad, matris in [("gozlenen", gozlenen), ("beklenen", beklenen), ("katki", katki),
                        ("pearson_artik", artik), ("satir_orani", oran)]:
        rows.extend((ad, hucre, float(value)) for hucre, value in zip(hucre_adlari, matris.ravel()))
    toplamlar = dict(toplam=float(gozlenen.sum()), satir_Birinci=float(gozlenen[0].sum()),
                     satir_Ikinci=float(gozlenen[1].sum()), sutun_Basarili=float(gozlenen[:, 0].sum()),
                     sutun_Basarisiz=float(gozlenen[:, 1].sum()))
    test = dict(ki_kare=ki_kare, serbestlik=serbestlik, p=p_degeri,
                cramer_v=math.sqrt(ki_kare / gozlenen.sum()), min_beklenen=float(beklenen.min()),
                alfa=ALFA, reddet=int(p_degeri < ALFA))
    rows += [("toplamlar", key, value) for key, value in toplamlar.items()]
    rows += [("test", key, value) for key, value in test.items()]
    sonuc = pd.DataFrame(rows, columns=["degisken", "olcu", "deger"])
    if not np.isfinite(sonuc.deger).all():
        raise ValueError("Sonlu sonuc hesaplanamadi.")
    return sonuc


def kontrol_et(sonuc, beklenen):
    if list(beklenen.columns) != ["degisken", "olcu", "deger"]:
        raise ValueError("Kontrol sutunlari uyusmuyor.")
    if not sonuc[["degisken", "olcu"]].equals(beklenen[["degisken", "olcu"]]):
        raise ValueError("Kontrol etiketleri veya sirasi uyusmuyor.")
    hedefler = pd.to_numeric(beklenen.deger, errors="raise")
    if not np.isfinite(hedefler).all() or not np.isfinite(sonuc.deger).all():
        raise ValueError("Sonlu kontrol degerleri gerekli.")
    if not all(math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
               for actual, expected in zip(sonuc.deger, hedefler)):
        raise ValueError("Kontrol degerleri uyusmuyor.")
    print(f"DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.")


def grafik_kaydet(veri):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    gozlenen, beklenen, katki, artik, oran, ki_kare, p_degeri, serbestlik = tablolar(veri)
    fig, paneller = plt.subplots(1, 2, figsize=(10, 4))
    konum = np.arange(2)
    for sutun, (etiket, renk) in enumerate(zip(SONUCLAR, ["#087F5B", "#1F4E79"])):
        merkez = konum + (sutun - .5) * .35
        bars = paneller[0].bar(merkez, oran[:, sutun] * 100, width=.35, color=renk, label=etiket)
        paneller[0].bar_label(bars, fmt="%.1f%%", padding=3)
    paneller[0].set(xticks=konum, xticklabels=GRUPLAR, ylim=(0, 105), ylabel="Satir yuzdesi",
                    title="Grup icindeki sonuc oranlari")
    paneller[0].legend(loc="upper right", fontsize="small")
    sinir = max(1, float(np.max(np.abs(artik))))
    resim = paneller[1].imshow(artik, cmap="RdBu", vmin=-sinir, vmax=sinir)
    for satir in range(2):
        for sutun in range(2):
            paneller[1].text(sutun, satir, f"{artik[satir, sutun]:+.4f}", ha="center", va="center",
                             color="white" if abs(artik[satir, sutun]) > .6 * sinir else "black")
    paneller[1].set(xticks=konum, xticklabels=SONUCLAR, yticks=konum, yticklabels=GRUPLAR,
                    title="Pearson artiklari (O-E)/sqrt(E)")
    fig.colorbar(resim, ax=paneller[1], fraction=.046, pad=.04)
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "oranlar-artiklar.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/oranlar-artiklar.png")


def main():
    parser = argparse.ArgumentParser(description="B12: duzeltmesiz Pearson bagimsizlik testi")
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
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}")


if __name__ == "__main__":
    main()