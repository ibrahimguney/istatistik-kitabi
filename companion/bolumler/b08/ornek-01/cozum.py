import argparse
import math
from numbers import Real
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


def hazirla(veri):
    if list(veri.columns) != ["n", "ortalama", "s"] or len(veri) != 1:
        raise ValueError("Tek satirda n, ortalama, s ozeti gerekli; bu dosya ham veri degildir.")
    if veri.isna().any().any():
        raise ValueError("Eksik ozet degeri kabul edilmez.")
    for sutun in veri.columns:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal ozet degerleri gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Sonlu ozet degerleri gerekli.")
    temiz = veri.reset_index(drop=True).copy(deep=True)
    hacim = float(temiz.loc[0, "n"])
    if hacim < 2 or not hacim.is_integer():
        raise ValueError("n en az 2 olan tam sayi olmali.")
    if temiz.loc[0, "s"] <= 0:
        raise ValueError("Bu pilot pozitif orneklem standart sapmasi gerektirir.")
    return temiz


def aralik_hesapla(veri, duzey):
    temiz = hazirla(veri)
    if not isinstance(duzey, Real) or isinstance(duzey, (bool, np.bool_)) or not math.isfinite(duzey) or not 0 < duzey < 1:
        raise ValueError("Guven duzeyi 0 ile 1 arasinda olmali; 95 yerine 0.95 kullanin.")
    hacim = int(temiz.loc[0, "n"])
    merkez = float(temiz.loc[0, "ortalama"])
    standart_hata = float(temiz.loc[0, "s"]) / math.sqrt(hacim)
    kritik = float(stats.t.ppf((1 + duzey) / 2, df=hacim - 1))
    hata_payi = kritik * standart_hata
    sonuc = {"guven_duzeyi": duzey, "alpha": 1 - duzey, "kritik_t": kritik,
             "hata_payi": hata_payi, "alt_sinir": merkez - hata_payi,
             "ust_sinir": merkez + hata_payi, "genislik": 2 * hata_payi}
    if not all(math.isfinite(deger) for deger in sonuc.values()):
        raise ValueError("Aralik sayisal olarak hesaplanamadi.")
    return sonuc


def hesapla(veri):
    temiz = hazirla(veri)
    hacim = int(temiz.loc[0, "n"])
    satirlar = [("ozet", "hacim", hacim), ("ozet", "ortalama", temiz.loc[0, "ortalama"]),
                ("ozet", "orneklem_sd", temiz.loc[0, "s"]),
                ("ozet", "standart_hata", temiz.loc[0, "s"] / math.sqrt(hacim)),
                ("ozet", "serbestlik", hacim - 1)]
    for etiket, duzey in [("GA95", 0.95), ("GA99", 0.99)]:
        satirlar.extend((etiket, olcu, deger) for olcu, deger in aralik_hesapla(temiz, duzey).items())
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
    merkez = float(temiz.loc[0, "ortalama"])
    fig, eksen = plt.subplots(figsize=(9, 3.5))
    for konum, duzey, renk in [(1, 0.95, "#1F4E79"), (0, 0.99, "#087F5B")]:
        ozet = aralik_hesapla(temiz, duzey)
        eksen.errorbar(merkez, konum, xerr=ozet["hata_payi"], fmt="o", capsize=7,
                       color=renk, linewidth=2, markersize=7)
        eksen.annotate(f'{ozet["alt_sinir"]:.4f}', (ozet["alt_sinir"], konum),
                      xytext=(0, 12), textcoords="offset points", ha="center")
        eksen.annotate(f'{ozet["ust_sinir"]:.4f}', (ozet["ust_sinir"], konum),
                      xytext=(0, 12), textcoords="offset points", ha="center")
    eksen.axvline(merkez, color="#AAAAAA", linestyle=":")
    eksen.set(yticks=[0, 1], yticklabels=["%99 guven", "%95 guven"], ylim=(-0.5, 1.6),
              xlabel="Evren ortalamasi icin aralik (puan)",
              title=f'n={int(temiz.loc[0, "n"])}; ortalama={merkez:g}; s={temiz.loc[0, "s"]:g}')
    eksen.margins(x=0.15)
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "guven-araliklari.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/guven-araliklari.png")


def main():
    parser = argparse.ArgumentParser(description="B08: ozet istatistiklerden t guven araligi")
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