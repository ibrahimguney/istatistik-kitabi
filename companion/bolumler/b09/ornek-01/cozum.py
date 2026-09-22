import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


def hazirla(veri):
    if list(veri.columns) != ["fark", "standart_hata", "serbestlik", "null_degeri", "alfa"] or len(veri) != 1:
        raise ValueError("Tek satirda fark, standart_hata, serbestlik, null_degeri, alfa ozeti gerekli.")
    if veri.isna().any().any():
        raise ValueError("Eksik ozet kabul edilmez.")
    for sutun in veri.columns:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal ozet degerleri gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Sonlu ozet degerleri gerekli.")
    temiz = veri.reset_index(drop=True).copy(deep=True)
    if temiz.loc[0, "standart_hata"] <= 0 or temiz.loc[0, "serbestlik"] <= 0:
        raise ValueError("Standart hata ve serbestlik pozitif olmali.")
    if not 0 < temiz.loc[0, "alfa"] < 1:
        raise ValueError("Alfa 0 ile 1 arasinda olmali; 5 yerine 0.05 kullanin.")
    return temiz


def test_hesapla(veri):
    temiz = hazirla(veri)
    fark, standart_hata, serbestlik, null_degeri, alfa = map(float, temiz.iloc[0])
    t_degeri = (fark - null_degeri) / standart_hata
    p_cift = float(2 * stats.t.sf(abs(t_degeri), df=serbestlik))
    p_ust = float(stats.t.sf(t_degeri, df=serbestlik))
    p_alt = float(stats.t.cdf(t_degeri, df=serbestlik))
    kritik = float(stats.t.ppf(1 - alfa / 2, df=serbestlik))
    hata_payi = kritik * standart_hata
    alt_sinir, ust_sinir = fark - hata_payi, fark + hata_payi
    sonuc = {"t": t_degeri, "p_cift": p_cift, "p_ust": p_ust, "p_alt": p_alt,
             "reddet_cift": int(p_cift < alfa), "reddet_alfa001": int(p_cift < 0.01),
             "reddet_ust": int(p_ust < alfa), "reddet_alt": int(p_alt < alfa),
             "guven_duzeyi": 1 - alfa, "kritik_t": kritik, "hata_payi": hata_payi,
             "alt_sinir": alt_sinir, "ust_sinir": ust_sinir, "genislik": 2 * hata_payi,
             "null_aralikta": int(alt_sinir <= null_degeri <= ust_sinir)}
    if not all(math.isfinite(value) for value in sonuc.values()):
        raise ValueError("Test veya aralik sayisal olarak hesaplanamadi.")
    return sonuc


def hesapla(veri):
    temiz = hazirla(veri)
    sonuc = test_hesapla(temiz)
    satirlar = [("girdi", sutun, float(temiz.loc[0, sutun])) for sutun in temiz.columns]
    satirlar.extend(("test", anahtar, sonuc[anahtar]) for anahtar in
                    ["t", "p_cift", "p_ust", "p_alt", "reddet_cift", "reddet_alfa001", "reddet_ust", "reddet_alt"])
    satirlar.extend(("aralik", anahtar, sonuc[anahtar]) for anahtar in
                    ["guven_duzeyi", "kritik_t", "hata_payi", "alt_sinir", "ust_sinir", "genislik", "null_aralikta"])
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
    sonuc = test_hesapla(temiz)
    fark = float(temiz.loc[0, "fark"])
    null_degeri = float(temiz.loc[0, "null_degeri"])
    serbestlik = float(temiz.loc[0, "serbestlik"])
    sinir = max(5, abs(sonuc["t"]) + 1, sonuc["kritik_t"] + 1)
    eksen = np.linspace(-sinir, sinir, 2001)
    yogunluk = stats.t.pdf(eksen, df=serbestlik)
    fig, paneller = plt.subplots(1, 2, figsize=(11, 4))
    paneller[0].plot(eksen, yogunluk, color="#1F4E79")
    paneller[0].fill_between(eksen, yogunluk, where=np.abs(eksen) >= abs(sonuc["t"]), color="#8FB8D8")
    for konum in [-abs(sonuc["t"]), abs(sonuc["t"])]:
        paneller[0].axvline(konum, color="#1F4E79", linestyle=":")
    paneller[0].set(xlabel="H0 altinda t", ylabel="Yogunluk", title=f'Cift yonlu p = {sonuc["p_cift"]:.5f}')
    paneller[1].errorbar(fark, 0, xerr=sonuc["hata_payi"], fmt="o", capsize=7, color="#087F5B")
    paneller[1].axvline(null_degeri, color="#555555", linestyle="--", label=f"H0: delta={null_degeri:g}")
    for uc in [sonuc["alt_sinir"], sonuc["ust_sinir"]]:
        paneller[1].annotate(f"{uc:.4f}", (uc, 0), xytext=(0, 12), textcoords="offset points", ha="center")
    paneller[1].set(xlim=(min(null_degeri, sonuc["alt_sinir"]) - sonuc["hata_payi"] * .3,
                         max(null_degeri, sonuc["ust_sinir"]) + sonuc["hata_payi"] * .3),
                    yticks=[], ylim=(-.5, .7), xlabel="Evren farki delta (fark birimi)",
                    title=f'%{100 * sonuc["guven_duzeyi"]:g} iki tarafli guven araligi')
    paneller[1].legend(loc="lower right", fontsize="small")
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "test-ve-aralik.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/test-ve-aralik.png")


def main():
    parser = argparse.ArgumentParser(description="B09: ozetten hipotez testi ve guven araligi")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri = pd.read_csv("veri.csv")
    sonuc = hesapla(veri)
    print(sonuc.to_string(index=False))
    karar = test_hesapla(veri)["reddet_cift"]
    print("Ana cift yonlu karar:", "H0 reddedilir" if karar else "H0 reddedilemez")
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(veri)
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}")


if __name__ == "__main__":
    main()