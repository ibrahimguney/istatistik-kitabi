import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


def hazirla(veri):
    if list(veri.columns) != ["cift_sayisi", "ortalama_fark", "fark_sapmasi", "alfa"] or len(veri) != 1:
        raise ValueError("Tek ozet satiri ve dogru sutun sirasi gerekli.")
    if veri.isna().any().any():
        raise ValueError("Eksik ozet kabul edilmez.")
    for sutun in veri.columns:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal ozet gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Sonlu ozet gerekli.")
    temiz = veri.reset_index(drop=True).copy(deep=True)
    hacim = float(temiz.loc[0, "cift_sayisi"])
    if hacim < 2 or not hacim.is_integer():
        raise ValueError("Tam cift sayisi en az 2 olan tam sayi olmali.")
    if temiz.loc[0, "fark_sapmasi"] <= 0:
        raise ValueError("Farklarin standart sapmasi pozitif olmali.")
    if not 0 < temiz.loc[0, "alfa"] < 1:
        raise ValueError("Alfa 0 ile 1 arasinda olmali.")
    return temiz


def test_hesapla(veri):
    temiz = hazirla(veri)
    hacim, fark, sapma, alfa = map(float, temiz.iloc[0])
    standart_hata = sapma / math.sqrt(hacim)
    serbestlik = hacim - 1
    t_degeri = fark / standart_hata
    p_degeri = float(2 * stats.t.sf(abs(t_degeri), df=serbestlik))
    kritik = float(stats.t.ppf(1 - alfa / 2, df=serbestlik))
    hata_payi = kritik * standart_hata
    alt, ust = fark - hata_payi, fark + hata_payi
    sonuc = dict(standart_hata=standart_hata, serbestlik=serbestlik, t=t_degeri, p_cift=p_degeri,
                  dz=fark / sapma, kritik_t=kritik, hata_payi=hata_payi, alt_sinir=alt,
                  ust_sinir=ust, genislik=2 * hata_payi, reddet=int(p_degeri < alfa),
                  sifir_aralikta=int(alt <= 0 <= ust), guven_duzeyi=1 - alfa)
    if not all(math.isfinite(value) for value in sonuc.values()):
        raise ValueError("Sonlu test sonucu hesaplanamadi.")
    return sonuc


def hesapla(veri):
    temiz = hazirla(veri)
    rows = [("girdi", key, float(temiz.loc[0, key])) for key in temiz.columns]
    rows += [("test", key, value) for key, value in test_hesapla(temiz).items()]
    return pd.DataFrame(rows, columns=["degisken", "olcu", "deger"])


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

    temiz = hazirla(veri)
    sonuc = test_hesapla(temiz)
    fark = float(temiz.loc[0, "ortalama_fark"])
    fig, panel = plt.subplots(figsize=(8, 3))
    panel.errorbar(fark, 0, xerr=sonuc["hata_payi"], fmt="o", capsize=8, color="#1F4E79")
    panel.axvline(0, color="#555555", linestyle="--", label="H0: ortalama fark = 0")
    for uc in [sonuc["alt_sinir"], sonuc["ust_sinir"]]:
        panel.annotate(f"{uc:.4f}", (uc, 0), xytext=(0, 15), textcoords="offset points", ha="center")
    pay = .35 * sonuc["hata_payi"]
    panel.set(xlim=(min(0, sonuc["alt_sinir"]) - pay, max(0, sonuc["ust_sinir"]) + pay),
              ylim=(-.5, .7), yticks=[], xlabel="Evren ortalama farki: son - on (puan)",
              title=f"Eslestirilmis test: %{100 * sonuc['guven_duzeyi']:g} fark araligi; p={sonuc['p_cift']:.5f}")
    panel.legend(loc="lower right", fontsize="small")
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "son-on-araligi.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/son-on-araligi.png")


def main():
    parser = argparse.ArgumentParser(description="B14: yontem secimi, eslestirilmis test ve sinav raporu")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri = pd.read_csv("veri.csv")
    sonuc = hesapla(veri)
    print(sonuc.to_string(index=False))
    print("H0 reddedilir" if test_hesapla(veri)["reddet"] else "H0 reddedilemez")
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(veri)
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}")


if __name__ == "__main__":
    main()