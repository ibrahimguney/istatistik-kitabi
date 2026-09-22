import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


ALFA = 0.05


def sayisal_kontrol(veri, sutunlar, en_az):
    if list(veri.columns) != sutunlar or len(veri) < en_az:
        raise ValueError("Sutun duzeni veya satir sayisi gecersiz.")
    for sutun in sutunlar:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal sutunlar gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Eksik veya sonsuz deger kabul edilmez; satirlar sessizce silinmez.")
    if (veri.saat < 0).any() or (veri.devamsizlik < 0).any():
        raise ValueError("Saat ve devamsizlik negatif olamaz.")
    if not np.equal(veri.devamsizlik, np.floor(veri.devamsizlik)).all():
        raise ValueError("Devamsizlik tam gun sayisi olmali.")


def hazirla(veri, yeni):
    sayisal_kontrol(veri, ["saat", "devamsizlik", "puan"], 4)
    sayisal_kontrol(yeni, ["saat", "devamsizlik"], 1)
    if len(yeni) != 1:
        raise ValueError("Tek bir yeni tasarim noktasi gerekli.")
    tasarim = np.column_stack([np.ones(len(veri)), veri.saat, veri.devamsizlik]).astype(float)
    if np.linalg.matrix_rank(tasarim) != 3 or np.linalg.cond(tasarim) > 1e12:
        raise ValueError("Tasarim tam rankli ve sayisal olarak iyi kosullu olmali.")
    if veri.puan.nunique() < 2:
        raise ValueError("Sabit puanla bu cikarim paketi kullanilamaz.")
    return veri.reset_index(drop=True).copy(deep=True), yeni.reset_index(drop=True).copy(deep=True), tasarim


def model_hesapla(veri, yeni):
    temiz, nokta, tasarim = hazirla(veri, yeni)
    puan = temiz.puan.to_numpy(dtype=float)
    ortogonal, ust_ucgen = np.linalg.qr(tasarim, mode="reduced")
    katsayi = np.linalg.solve(ust_ucgen, ortogonal.T @ puan)
    ters_ucgen = np.linalg.solve(ust_ucgen, np.eye(3))
    kov_taban = ters_ucgen @ ters_ucgen.T
    uydurulan = tasarim @ katsayi
    artik = puan - uydurulan
    sse = float(artik @ artik)
    merkez = puan - puan.mean()
    sst = float(merkez @ merkez)
    if not math.isfinite(sse + sst) or sse <= np.finfo(float).eps * sst:
        raise ValueError("Tam veya sayisal olarak tama yakin uyumda cikarim hesaplanmaz.")
    hacim = len(temiz)
    serbestlik = hacim - 3
    mse = sse / serbestlik
    se = np.sqrt(mse * np.diag(kov_taban))
    t_degerleri = katsayi / se
    p_degerleri = 2 * stats.t.sf(np.abs(t_degerleri), serbestlik)
    kritik = float(stats.t.ppf(1 - ALFA / 2, serbestlik))
    r_kare = 1 - sse / sst
    f_degeri = max(0.0, (sst - sse) / 2 / mse)
    aciklayicilar = temiz[["saat", "devamsizlik"]].to_numpy(dtype=float)
    rho = float(np.corrcoef(aciklayicilar, rowvar=False)[0, 1])
    vif = 1 / (1 - rho ** 2)
    yeni_tasarim = np.array([1, nokta.saat.iloc[0], nokta.devamsizlik.iloc[0]], dtype=float)
    ongoru = float(yeni_tasarim @ katsayi)
    h_yeni = float(yeni_tasarim @ kov_taban @ yeni_tasarim)
    se_ortalama = math.sqrt(mse * h_yeni)
    se_birey = math.sqrt(mse * (1 + h_yeni))
    satirlar = [("model", isim, deger) for isim, deger in {
        "n": hacim, "serbestlik": serbestlik, "sse": sse, "sst": sst,
        "mse": mse, "artik_sd": math.sqrt(mse), "r_kare": r_kare,
        "duzeltilmis_r_kare": 1 - (1 - r_kare) * (hacim - 1) / serbestlik,
        "f": f_degeri, "p_f": float(stats.f.sf(f_degeri, 2, serbestlik)),
        "alfa": ALFA, "kritik_t": kritik}.items()]
    for indis, ad in enumerate(["sabit", "saat", "devamsizlik"]):
        olculer = {"katsayi": katsayi[indis], "se": se[indis], "t": t_degerleri[indis],
                   "p": p_degerleri[indis], "alt": katsayi[indis] - kritik * se[indis],
                   "ust": katsayi[indis] + kritik * se[indis]}
        satirlar.extend((ad, isim, deger) for isim, deger in olculer.items())
    satirlar.extend([("vif", "saat", vif), ("vif", "devamsizlik", vif)])
    olculer = {"saat": float(nokta.saat.iloc[0]), "devamsizlik": float(nokta.devamsizlik.iloc[0]),
               "ongoru": ongoru, "h_yeni": h_yeni, "se_ortalama": se_ortalama,
               "se_birey": se_birey, "ortalama_alt": ongoru - kritik * se_ortalama,
               "ortalama_ust": ongoru + kritik * se_ortalama,
               "birey_alt": ongoru - kritik * se_birey, "birey_ust": ongoru + kritik * se_birey}
    satirlar.extend(("yeni", isim, deger) for isim, deger in olculer.items())
    for indis, (uyum, hata) in enumerate(zip(uydurulan, artik), start=1):
        satirlar.extend([(f"satir_{indis:02}", "uydurulan", uyum), (f"satir_{indis:02}", "artik", hata)])
    sonuc = pd.DataFrame(satirlar, columns=["degisken", "olcu", "deger"])
    if not np.isfinite(sonuc.deger).all():
        raise ValueError("Sonlu model sonuclari hesaplanamadi.")
    return sonuc, uydurulan, artik


def hesapla(veri, yeni):
    return model_hesapla(veri, yeni)[0]


def kontrol_et(sonuc, beklenen):
    if list(beklenen.columns) != ["degisken", "olcu", "deger"]:
        raise ValueError("Kontrol sutunlari uyusmuyor.")
    if not sonuc[["degisken", "olcu"]].equals(beklenen[["degisken", "olcu"]]):
        raise ValueError("Kontrol etiketleri veya sirasi uyusmuyor.")
    hedefler = pd.to_numeric(beklenen.deger, errors="raise")
    if not np.isfinite(hedefler).all():
        raise ValueError("Sonlu referanslar gerekli.")
    for olcu, gercek, hedef in zip(sonuc.olcu, sonuc.deger, hedefler):
        p_kontrol = olcu in {"p", "p_f"}
        if not math.isclose(gercek, hedef, rel_tol=1e-8 if p_kontrol else 1e-9,
                            abs_tol=0 if p_kontrol else 1e-9):
            raise ValueError(f"Kontrol uyusmazligi: {olcu}: {gercek} != {hedef}")
    print(f"DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.")


def grafik_kaydet(veri, yeni):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sonuc, uydurulan, artik = model_hesapla(veri, yeni)
    fig, eksenler = plt.subplots(1, 2, figsize=(10, 4))
    eksenler[0].scatter(uydurulan, artik, color="#1F4E79")
    eksenler[0].axhline(0, color="#555555", linestyle="--")
    eksenler[0].set(xlabel="Uydurulan puan", ylabel="Artik", title="Artik - uydurulan")
    stats.probplot(artik, dist="norm", plot=eksenler[1])
    eksenler[1].set(title="Normal Q-Q", xlabel="Kuramsal normal kantil", ylabel="Sirali artik")
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "coklu-regresyon-tani.png", dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Kapsamli bolum 15: coklu dogrusal regresyon")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri, yeni = pd.read_csv("veri.csv"), pd.read_csv("yeni.csv")
    sonuc = hesapla(veri, yeni)
    print(sonuc.to_string(index=False))
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(veri, yeni)
    for sutun in ["saat", "devamsizlik"]:
        if not veri[sutun].min() <= yeni[sutun].iloc[0] <= veri[sutun].max():
            print(f"UYARI: yeni {sutun} gozlenen araligin disinda; ekstrapolasyon.")
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}")


if __name__ == "__main__":
    main()