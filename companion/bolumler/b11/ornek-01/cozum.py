import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


SUTUNLAR = ["hacim_1", "ortalama_1", "standart_sapma_1", "hacim_2", "ortalama_2",
            "standart_sapma_2", "cift_sayisi", "ortalama_fark", "fark_sapmasi", "alfa"]


def hazirla(veri):
    if list(veri.columns) != SUTUNLAR or len(veri) != 1:
        raise ValueError("Tek ozet satiri ve dogru sutun sirasi gerekli.")
    if veri.isna().any().any():
        raise ValueError("Eksik ozet kabul edilmez.")
    for sutun in SUTUNLAR:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal ozet gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Sonlu ozet gerekli.")
    temiz = veri.reset_index(drop=True).copy(deep=True)
    for sutun in ["hacim_1", "hacim_2", "cift_sayisi"]:
        hacim = float(temiz.loc[0, sutun])
        if hacim < 2 or not hacim.is_integer():
            raise ValueError("Hacimler en az 2 olan tam sayilar olmali.")
    if any(temiz.loc[0, sutun] <= 0 for sutun in ["standart_sapma_1", "standart_sapma_2", "fark_sapmasi"]):
        raise ValueError("Bu paket pozitif standart sapmalar gerektirir.")
    if not 0 < temiz.loc[0, "alfa"] < 1:
        raise ValueError("Alfa 0 ile 1 arasinda olmali.")
    return temiz


def test_ozeti(fark, standart_hata, serbestlik, alfa):
    t_degeri = fark / standart_hata
    p_degeri = float(2 * stats.t.sf(abs(t_degeri), df=serbestlik))
    kritik = float(stats.t.ppf(1 - alfa / 2, df=serbestlik))
    hata_payi = kritik * standart_hata
    sonuc = dict(standart_hata=standart_hata, serbestlik=serbestlik, t=t_degeri,
                  p_cift=p_degeri, kritik_t=kritik, hata_payi=hata_payi,
                  alt_sinir=fark - hata_payi, ust_sinir=fark + hata_payi,
                  genislik=2 * hata_payi, reddet_cift=int(p_degeri < alfa))
    if not all(math.isfinite(value) for value in sonuc.values()):
        raise ValueError("Test sayisal olarak hesaplanamadi.")
    return sonuc


def hesapla(veri):
    temiz = hazirla(veri)
    deger = {key: float(temiz.loc[0, key]) for key in SUTUNLAR}
    katki_1 = deger["standart_sapma_1"] ** 2 / deger["hacim_1"]
    katki_2 = deger["standart_sapma_2"] ** 2 / deger["hacim_2"]
    toplam = katki_1 + katki_2
    serbestlik = toplam ** 2 / (katki_1 ** 2 / (deger["hacim_1"] - 1) +
                                katki_2 ** 2 / (deger["hacim_2"] - 1))
    fark = deger["ortalama_1"] - deger["ortalama_2"]
    welch = dict(katki_1=katki_1, katki_2=katki_2, fark=fark)
    welch.update(test_ozeti(fark, math.sqrt(toplam), serbestlik, deger["alfa"]))
    eslesmis = test_ozeti(deger["ortalama_fark"], deger["fark_sapmasi"] / math.sqrt(deger["cift_sayisi"]),
                          deger["cift_sayisi"] - 1, deger["alfa"])
    eslesmis["dz"] = deger["ortalama_fark"] / deger["fark_sapmasi"]
    rows = [("girdi", key, value) for key, value in deger.items()]
    rows += [("welch", key, value) for key, value in welch.items()]
    rows += [("eslesmis", key, value) for key, value in eslesmis.items()]
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

    temiz = hazirla(veri)
    sonuc = hesapla(temiz)
    fig, paneller = plt.subplots(1, 2, figsize=(10, 4))
    bilgiler = [("welch", "Welch: Grup 1 - Grup 2"), ("eslesmis", "Eslestirilmis: son - on")]
    for panel, (grup, baslik) in zip(paneller, bilgiler):
        ozet = sonuc.loc[sonuc.degisken == grup].set_index("olcu").deger
        merkez = (ozet["alt_sinir"] + ozet["ust_sinir"]) / 2
        panel.errorbar(merkez, 0, xerr=ozet["hata_payi"], fmt="o", capsize=7, color="#087F5B")
        panel.axvline(0, linestyle="--", color="#555555", label="H0: fark = 0")
        for uc in [ozet["alt_sinir"], ozet["ust_sinir"]]:
            panel.annotate(f"{uc:.4f}", (uc, 0), xytext=(0, 12), textcoords="offset points", ha="center")
        pay = .35 * ozet["hata_payi"]
        panel.set(xlim=(min(0, ozet["alt_sinir"]) - pay, max(0, ozet["ust_sinir"]) + pay),
                  ylim=(-.5, .6), yticks=[], xlabel="Evren ortalama farki (puan)",
                  title=f"{baslik}\np = {ozet['p_cift']:.6f}")
        panel.legend(loc="lower right", fontsize="small")
    fig.suptitle(f"Iki ayri ornek: %{100 * (1 - float(temiz.loc[0, 'alfa'])):g} fark araliklari")
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "fark-araliklari.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/fark-araliklari.png")


def main():
    parser = argparse.ArgumentParser(description="B11: ozetlerden Welch ve eslestirilmis t testi")
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