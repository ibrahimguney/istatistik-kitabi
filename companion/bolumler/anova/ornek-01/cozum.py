import argparse
from itertools import combinations
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


ALFA = 0.05


def hazirla(veri):
    if list(veri.columns) != ["grup", "n", "ortalama", "standart_sapma"] or len(veri) != 3:
        raise ValueError("Uc satirlik grup,n,ortalama,standart_sapma ozeti gerekli.")
    if veri.grup.tolist() != ["A", "B", "C"]:
        raise ValueError("Grup etiketleri A,B,C sirasinda olmali.")
    for sutun in ["n", "ortalama", "standart_sapma"]:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal ozet degerleri gerekli.")
    if not np.isfinite(veri.iloc[:, 1:].to_numpy(dtype=float)).all():
        raise ValueError("Eksik veya sonsuz ozet kabul edilmez.")
    if not ((veri.n >= 2) & (veri.n == np.floor(veri.n))).all():
        raise ValueError("Her grupta n en az 2 olan tam sayi olmali.")
    if not (veri.standart_sapma > 0).all():
        raise ValueError("Bu paket pozitif orneklem standart sapmalari gerektirir.")
    return veri.reset_index(drop=True).copy(deep=True)


def klasik_hesapla(veri):
    temiz = hazirla(veri)
    hacimler, ortalamalar, sapmalar = temiz.iloc[:, 1:].to_numpy(dtype=float).T
    grup_sayisi = len(temiz)
    toplam = float(hacimler.sum())
    genel = float(np.average(ortalamalar, weights=hacimler))
    ss_grup = float(np.sum(hacimler * (ortalamalar - genel) ** 2))
    ss_hata = float(np.sum((hacimler - 1) * sapmalar ** 2))
    sd_grup, sd_hata = grup_sayisi - 1, toplam - grup_sayisi
    ms_grup, mse = ss_grup / sd_grup, ss_hata / sd_hata
    f_degeri = ms_grup / mse
    kritik = float(stats.studentized_range.ppf(1 - ALFA, grup_sayisi, sd_hata))
    ozet = {"grup_sayisi": grup_sayisi, "toplam_n": toplam, "genel_ortalama": genel,
            "ss_grup": ss_grup, "ss_hata": ss_hata, "ss_toplam": ss_grup + ss_hata,
            "sd_grup": sd_grup, "sd_hata": sd_hata, "ms_grup": ms_grup, "mse": mse,
            "f": f_degeri, "p": float(stats.f.sf(f_degeri, sd_grup, sd_hata)),
            "eta2": ss_grup / (ss_grup + ss_hata),
            "omega2": (ss_grup - sd_grup * mse) / (ss_grup + ss_hata + mse),
            "alfa": ALFA, "q_kritik": kritik}
    ciftler = []
    for ilk, ikinci in combinations(range(grup_sayisi), 2):
        fark = float(ortalamalar[ilk] - ortalamalar[ikinci])
        se_q = math.sqrt(mse / 2 * (1 / hacimler[ilk] + 1 / hacimler[ikinci]))
        q_degeri = abs(fark) / se_q
        yari_genislik = kritik * se_q
        p_degeri = float(stats.studentized_range.sf(q_degeri, grup_sayisi, sd_hata))
        ciftler.append((f"{temiz.grup.iloc[ilk]}-{temiz.grup.iloc[ikinci]}", {
            "fark": fark, "se_q": se_q, "q": q_degeri, "yari_genislik": yari_genislik,
            "alt": fark - yari_genislik, "ust": fark + yari_genislik,
            "p_duzeltilmis": p_degeri, "reddet": int(p_degeri < ALFA)}))
    return ozet, ciftler


def welch_hesapla(veri):
    temiz = hazirla(veri)
    hacimler, ortalamalar, sapmalar = temiz.iloc[:, 1:].to_numpy(dtype=float).T
    grup_sayisi = len(temiz)
    agirliklar = hacimler / sapmalar ** 2
    paylar = agirliklar / agirliklar.sum()
    merkez = float(np.sum(paylar * ortalamalar))
    duzeltme = float(np.sum((1 - paylar) ** 2 / (hacimler - 1)))
    pay = float(np.sum(agirliklar * (ortalamalar - merkez) ** 2) / (grup_sayisi - 1))
    carpan = 1 + 2 * (grup_sayisi - 2) * duzeltme / (grup_sayisi ** 2 - 1)
    f_degeri = pay / carpan
    sd_payda = (grup_sayisi ** 2 - 1) / (3 * duzeltme)
    return {"grup_sayisi": grup_sayisi, "toplam_n": float(hacimler.sum()),
            "agirlik_toplami": float(agirliklar.sum()), "agirlikli_merkez": merkez,
            "duzeltme": duzeltme, "pay": pay, "duzeltme_carpani": carpan,
            "f": f_degeri, "sd_pay": grup_sayisi - 1, "sd_payda": sd_payda,
            "p": float(stats.f.sf(f_degeri, grup_sayisi - 1, sd_payda)), "alfa": ALFA}


def hesapla(veri, welch):
    klasik, ciftler = klasik_hesapla(veri)
    esitsiz = welch_hesapla(welch)
    satirlar = []
    for kod, tablo in [("girdi_klasik", hazirla(veri)), ("girdi_welch", hazirla(welch))]:
        for satir in tablo.itertuples(index=False):
            for isim in ["n", "ortalama", "standart_sapma"]:
                satirlar.append((f"{kod}_{satir.grup}", isim, float(getattr(satir, isim))))
    satirlar.extend(("klasik", isim, deger) for isim, deger in klasik.items())
    for cift, sonuc in ciftler:
        satirlar.extend((f"tukey_{cift}", isim, deger) for isim, deger in sonuc.items())
    satirlar.extend(("welch", isim, deger) for isim, deger in esitsiz.items())
    sonuc = pd.DataFrame(satirlar, columns=["degisken", "olcu", "deger"])
    if not np.isfinite(sonuc.deger).all():
        raise ValueError("Sonlu analiz sonucu hesaplanamadi.")
    return sonuc


def kontrol_et(sonuc, beklenen):
    if list(beklenen.columns) != ["degisken", "olcu", "deger"]:
        raise ValueError("Kontrol sutunlari uyusmuyor.")
    if not sonuc[["degisken", "olcu"]].equals(beklenen[["degisken", "olcu"]]):
        raise ValueError("Kontrol etiketleri veya sirasi uyusmuyor.")
    hedefler = pd.to_numeric(beklenen.deger, errors="raise")
    if not np.isfinite(hedefler).all():
        raise ValueError("Sonlu referanslar gerekli.")
    for olcu, deger, hedef in zip(sonuc.olcu, sonuc.deger, hedefler):
        p_kontrol = olcu in {"p", "p_duzeltilmis"}
        if not math.isclose(deger, hedef, rel_tol=1e-8 if p_kontrol else 1e-9,
                            abs_tol=0 if p_kontrol else 1e-9):
            raise ValueError(f"Kontrol uyusmazligi: {olcu}: {deger} != {hedef}")
    print(f"DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.")


def grafik_kaydet(veri):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    temiz = hazirla(veri)
    ozet, ciftler = klasik_hesapla(temiz)
    fig, eksenler = plt.subplots(1, 2, figsize=(11, 4))
    eksenler[0].errorbar(temiz.grup, temiz.ortalama, yerr=temiz.standart_sapma,
                         fmt="o", capsize=5, color="#1F4E79")
    eksenler[0].set(xlabel="Grup", ylabel="Puan", title="Ortalama +/- SD (GA degil)")
    eksenler[1].errorbar([sonuc["fark"] for ad, sonuc in ciftler], range(3),
                         xerr=[sonuc["yari_genislik"] for ad, sonuc in ciftler],
                         fmt="o", capsize=5, color="#087F5B")
    eksenler[1].axvline(0, color="#555555", linestyle="--")
    eksenler[1].set(yticks=range(3), yticklabels=[ad for ad, sonuc in ciftler],
                    xlabel="Ilk grup - ikinci grup", title="Tukey: %95 eszamanli araliklar")
    eksenler[1].invert_yaxis()
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "anova-tukey.png", dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Kapsamli bolum 16: ozetlerden ANOVA, Tukey ve Welch")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri, welch = pd.read_csv("veri.csv"), pd.read_csv("welch.csv")
    ciftler = pd.read_csv("ciftler.csv")
    if list(ciftler.columns) != ["cift", "ilk", "ikinci"] or not np.array_equal(
            ciftler.to_numpy(), [[1, 1, 2], [2, 1, 3], [3, 2, 3]]):
        raise ValueError("SPSS karsilastirma haritasi A-B, A-C, B-C sirasinda olmali.")
    sonuc = hesapla(veri, welch)
    print(sonuc.to_string(index=False))
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(veri)
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}")


if __name__ == "__main__":
    main()