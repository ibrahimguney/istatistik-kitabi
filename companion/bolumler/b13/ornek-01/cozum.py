import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


ALFA = 0.05
YENI_SAAT = 6.0


def hazirla(veri):
    if list(veri.columns) != ["saat", "puan"] or len(veri) < 3:
        raise ValueError("En az uc eslesmis satir ve saat, puan sutunlari gerekli.")
    if veri.isna().any().any():
        raise ValueError("Eksik olcum kabul edilmez; sessiz satir silinmez.")
    for sutun in veri.columns:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal olcumler gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all() or (veri.saat < 0).any():
        raise ValueError("Sonlu olcum ve negatif olmayan saat gerekli.")
    if veri.saat.nunique() < 2 or veri.puan.nunique() < 2:
        raise ValueError("Sabit saat veya puan ile bu korelasyon/egim paketi kullanilamaz.")
    return veri.reset_index(drop=True).copy(deep=True)


def model_hesapla(veri, yeni_saat=YENI_SAAT):
    temiz = hazirla(veri)
    if isinstance(yeni_saat, bool) or not math.isfinite(float(yeni_saat)) or yeni_saat < 0:
        raise ValueError("Yeni saat sonlu ve negatif olmayan sayi olmali.")
    hacim = len(temiz)
    saat, puan = temiz.saat.to_numpy(dtype=float), temiz.puan.to_numpy(dtype=float)
    saat_ort, puan_ort = float(saat.mean()), float(puan.mean())
    saat_merkez, puan_merkez = saat - saat_ort, puan - puan_ort
    sxx = float(saat_merkez @ saat_merkez)
    syy = float(puan_merkez @ puan_merkez)
    sxy = float(saat_merkez @ puan_merkez)
    egim = sxy / sxx
    sabit = puan_ort - egim * saat_ort
    uydurulan = sabit + egim * saat
    artik = puan - uydurulan
    sse = float(artik @ artik)
    if sse <= np.finfo(float).eps * syy:
        raise ValueError("Tam veya sayisal olarak tama yakin uyumda bu cikarim paketi durur.")
    serbestlik = hacim - 2
    mse = sse / serbestlik
    korelasyon = sxy / math.sqrt(sxx * syy)
    se_egim = math.sqrt(mse / sxx)
    se_sabit = math.sqrt(mse * (1 / hacim + saat_ort ** 2 / sxx))
    t_egim = egim / se_egim
    p_egim = float(2 * stats.t.sf(abs(t_egim), df=serbestlik))
    kritik = float(stats.t.ppf(1 - ALFA / 2, df=serbestlik))
    ongoru = sabit + egim * yeni_saat
    se_ortalama = math.sqrt(mse * (1 / hacim + (yeni_saat - saat_ort) ** 2 / sxx))
    se_birey = math.sqrt(mse + se_ortalama ** 2)
    ozet = dict(hacim=hacim, saat_ort=saat_ort, puan_ort=puan_ort, sxx=sxx, syy=syy, sxy=sxy,
                sse=sse, mse=mse, serbestlik=serbestlik, korelasyon=korelasyon, r_kare=1 - sse / syy,
                egim=egim, sabit=sabit, se_egim=se_egim, se_sabit=se_sabit, t_egim=t_egim,
                p_egim=p_egim, kritik_t=kritik, egim_alt=egim - kritik * se_egim,
                egim_ust=egim + kritik * se_egim, sabit_alt=sabit - kritik * se_sabit,
                sabit_ust=sabit + kritik * se_sabit, yeni_saat=yeni_saat, ongoru=ongoru,
                se_ortalama=se_ortalama, se_birey=se_birey,
                ortalama_alt=ongoru - kritik * se_ortalama, ortalama_ust=ongoru + kritik * se_ortalama,
                birey_alt=ongoru - kritik * se_birey, birey_ust=ongoru + kritik * se_birey)
    if not all(math.isfinite(value) for value in ozet.values()):
        raise ValueError("Sonlu model sonucu hesaplanamadi.")
    return ozet, uydurulan, artik


def hesapla(veri, yeni_saat=YENI_SAAT):
    ozet, uydurulan, artik = model_hesapla(veri, yeni_saat)
    rows = [("ozet", key, value) for key, value in ozet.items()]
    for ad, values in [("uydurulan", uydurulan), ("artik", artik)]:
        rows += [(ad, f"satir_{indis:02d}", float(value)) for indis, value in enumerate(values, start=1)]
    return pd.DataFrame(rows, columns=["degisken", "olcu", "deger"])


def kontrol_et(sonuc, beklenen):
    if list(beklenen.columns) != ["degisken", "olcu", "deger"]:
        raise ValueError("Kontrol sutunlari uyusmuyor.")
    if not sonuc[["degisken", "olcu"]].equals(beklenen[["degisken", "olcu"]]):
        raise ValueError("Kontrol etiketleri veya sirasi uyusmuyor.")
    hedefler = pd.to_numeric(beklenen.deger, errors="raise")
    if not np.isfinite(hedefler).all() or not np.isfinite(sonuc.deger).all():
        raise ValueError("Sonlu kontrol degerleri gerekli.")
    for olcu, actual, expected in zip(sonuc.olcu, sonuc.deger, hedefler):
        atol, rtol = (0, 1e-8) if olcu == "p_egim" else (1e-9, 1e-9)
        if not math.isclose(actual, expected, abs_tol=atol, rel_tol=rtol):
            raise ValueError(f"Kontrol uyusmazligi: {olcu}")
    print(f"DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.")


def grafik_kaydet(veri):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    temiz = hazirla(veri)
    ozet, uydurulan, artik = model_hesapla(temiz)
    fig, paneller = plt.subplots(2, 2, figsize=(10, 8))
    saatlar = np.linspace(temiz.saat.min(), temiz.saat.max(), 100)
    paneller[0, 0].scatter(temiz.saat, temiz.puan, color="#1F4E79")
    paneller[0, 0].plot(saatlar, ozet["sabit"] + ozet["egim"] * saatlar, color="#087F5B")
    paneller[0, 0].set(xlabel="Calisma saati", ylabel="Son test puani", title="Sacilim ve regresyon dogrusu")
    paneller[0, 1].scatter(uydurulan, artik, color="#1F4E79")
    paneller[0, 1].axhline(0, linestyle="--", color="#555555")
    paneller[0, 1].set(xlabel="Uydurulan deger", ylabel="Ham artik", title="Artik - uydurulan deger")
    hacim = len(artik)
    duzeltme = .375 if hacim <= 10 else .5
    teorik = stats.norm.ppf((np.arange(1, hacim + 1) - duzeltme) / (hacim + 1 - 2 * duzeltme))
    sirali = np.sort(artik)
    nicelikler = np.quantile(artik, [.25, .75])
    normal_nicelikler = stats.norm.ppf([.25, .75])
    qq_egim = np.diff(nicelikler)[0] / np.diff(normal_nicelikler)[0]
    qq_sabit = nicelikler[0] - qq_egim * normal_nicelikler[0]
    paneller[1, 0].scatter(teorik, sirali, color="#1F4E79")
    paneller[1, 0].plot(teorik, qq_sabit + qq_egim * teorik, color="#555555", linestyle="--")
    paneller[1, 0].set(xlabel="Teorik normal nicelik", ylabel="Sirali ham artik", title="Normal Q-Q grafigi")
    for konum, etiket, alt, ust in [(1, "Ortalama yanit", ozet["ortalama_alt"], ozet["ortalama_ust"]),
                                   (0, "Yeni birey", ozet["birey_alt"], ozet["birey_ust"])]:
        paneller[1, 1].errorbar(ozet["ongoru"], konum, xerr=(ust - alt) / 2, fmt="o", capsize=6)
        paneller[1, 1].text(alt, konum + .15, f"{alt:.3f}", ha="center", fontsize=8)
        paneller[1, 1].text(ust, konum + .15, f"{ust:.3f}", ha="center", fontsize=8)
    paneller[1, 1].set(yticks=[0, 1], yticklabels=["Yeni birey", "Ortalama yanit"], ylim=(-.5, 1.6),
                      xlabel="Puan", xlim=(ozet["birey_alt"] - .8, ozet["birey_ust"] + .8), title="6 saat: %95 araliklar")
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "regresyon-tani.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/regresyon-tani.png")


def main():
    parser = argparse.ArgumentParser(description="B13: korelasyon, regresyon ve iki farkli ongoru araligi")
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