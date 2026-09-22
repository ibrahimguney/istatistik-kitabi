import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy import stats


ARAMA_UST = 10000


def hazirla(veri, plan=False):
    sutunlar = (["hacim", "fark", "standart_sapma", "alfa", "hedef_guc"] if plan else
                ["hacim", "ortalama", "standart_sapma", "referans", "alfa"])
    if list(veri.columns) != sutunlar or len(veri) != 1:
        raise ValueError("Tek ozet satiri ve dogru sutun sirasi gerekli.")
    if veri.isna().any().any():
        raise ValueError("Eksik ozet kabul edilmez.")
    for sutun in sutunlar:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal ozet gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Sonlu ozet gerekli.")
    temiz = veri.reset_index(drop=True).copy(deep=True)
    hacim = float(temiz.loc[0, "hacim"])
    if hacim < 2 or not hacim.is_integer():
        raise ValueError("Hacim en az 2 olan tam sayi olmali.")
    if temiz.loc[0, "standart_sapma"] <= 0 or not 0 < temiz.loc[0, "alfa"] < 1:
        raise ValueError("Standart sapma pozitif, alfa 0 ile 1 arasinda olmali.")
    if plan and (temiz.loc[0, "fark"] == 0 or not temiz.loc[0, "alfa"] < temiz.loc[0, "hedef_guc"] < 1):
        raise ValueError("Hacim plani icin sifirdan farkli etki ve alfa < hedef guc < 1 gerekli.")
    return temiz


def guc_hesapla(hacim, etki, alfa):
    if not all(math.isfinite(float(value)) for value in [hacim, etki, alfa]):
        raise ValueError("Sonlu guc girdileri gerekli.")
    if hacim < 2 or not 0 < alfa < 1:
        raise ValueError("Guc icin hacim >= 2 ve 0 < alfa < 1 gerekli.")
    serbestlik = hacim - 1
    kritik = stats.t.ppf(1 - alfa / 2, df=serbestlik)
    merkezdisilik = abs(etki) * math.sqrt(hacim)
    guc = float(stats.nct.cdf(-kritik, df=serbestlik, nc=merkezdisilik) +
                stats.nct.sf(kritik, df=serbestlik, nc=merkezdisilik))
    if not math.isfinite(guc) or not 0 <= guc <= 1:
        raise ValueError("Guc sayisal olarak hesaplanamadi.")
    return guc


def en_kucuk_hacim(etki, alfa, hedef):
    if etki == 0 or not alfa < hedef < 1:
        raise ValueError("Sonlu hacim plani icin sifir olmayan etki ve alfa < hedef < 1 gerekli.")
    alt, ust = 2, 2
    while guc_hesapla(ust, etki, alfa) < hedef:
        if ust == ARAMA_UST:
            raise ValueError("Hedef guc 10000 gozleme kadar bulunamadi; bu paket arama siniri asildi.")
        ust = min(2 * ust, ARAMA_UST)
    while alt < ust:
        orta = (alt + ust) // 2
        if guc_hesapla(orta, etki, alfa) >= hedef:
            ust = orta
        else:
            alt = orta + 1
    return alt


def hesapla(veri, plan):
    veri, plan = hazirla(veri), hazirla(plan, plan=True)
    hacim, ortalama, sapma, referans, alfa = map(float, veri.iloc[0])
    plan_hacim, fark, plan_sapma, plan_alfa, hedef = map(float, plan.iloc[0])
    serbestlik = hacim - 1
    standart_hata = sapma / math.sqrt(hacim)
    t_degeri = (ortalama - referans) / standart_hata
    p_degeri = float(2 * stats.t.sf(abs(t_degeri), df=serbestlik))
    kritik = float(stats.t.ppf(1 - alfa / 2, df=serbestlik))
    hata_payi = kritik * standart_hata
    test = dict(serbestlik=serbestlik, standart_hata=standart_hata, t=t_degeri,
                p_cift=p_degeri, cohen_d=(ortalama - referans) / sapma, kritik_t=kritik,
                alt_sinir=ortalama - hata_payi, ust_sinir=ortalama + hata_payi,
                hata_payi=hata_payi, genislik=2 * hata_payi, reddet_cift=int(p_degeri < alfa))
    etki = fark / plan_sapma
    guc = guc_hesapla(plan_hacim, etki, plan_alfa)
    gereken = en_kucuk_hacim(etki, plan_alfa, hedef)
    guc_onceki = guc_hesapla(gereken - 1, etki, plan_alfa) if gereken > 2 else float("nan")
    tasarim = dict(plan_d=etki, plan_serbestlik=plan_hacim - 1,
                   plan_kritik_t=float(stats.t.ppf(1 - plan_alfa / 2, df=plan_hacim - 1)),
                   merkezdisilik=abs(etki) * math.sqrt(plan_hacim), guc=guc, beta=1 - guc,
                   gereken_hacim=gereken, onceki_guc=guc_onceki,
                   gereken_guc=guc_hesapla(gereken, etki, plan_alfa))
    rows = [("girdi", key, float(veri.loc[0, key])) for key in veri.columns]
    rows += [("plan_girdi", key, float(plan.loc[0, key])) for key in plan.columns]
    rows += [("test", key, value) for key, value in test.items()]
    rows += [("plan", key, value) for key, value in tasarim.items()]
    sonuc = pd.DataFrame(rows, columns=["degisken", "olcu", "deger"])
    degerler = sonuc.loc[sonuc.olcu != "onceki_guc", "deger"]
    if not np.isfinite(degerler).all():
        raise ValueError("Sonuc sayisal olarak hesaplanamadi.")
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


def grafik_kaydet(plan):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    temiz = hazirla(plan, plan=True)
    hacim, fark, sapma, alfa, hedef = map(float, temiz.iloc[0])
    etki = fark / sapma
    gereken = en_kucuk_hacim(etki, alfa, hedef)
    ust = min(ARAMA_UST, max(60, hacim + 10, gereken + 10))
    hacimler = np.unique(np.rint(np.linspace(2, ust, 120)).astype(int))
    fig, panel = plt.subplots(figsize=(8, 4.5))
    for carpan, stil in [(1, "-"), (.5, "--")]:
        gucler = [guc_hesapla(int(aday), etki * carpan, alfa) for aday in hacimler]
        panel.plot(hacimler, gucler, stil, label=f"Planlanan |d| = {abs(etki * carpan):g}")
    panel.axhline(hedef, color="#555555", linestyle=":", label=f"Hedef guc = {hedef:g}")
    panel.scatter([gereken], [guc_hesapla(gereken, etki, alfa)], color="#087F5B", zorder=3)
    panel.annotate(f"En kucuk n = {gereken}", (gereken, guc_hesapla(gereken, etki, alfa)),
                   xytext=(8, -22), textcoords="offset points")
    panel.set(xlabel="Bagimsiz gozlem sayisi n", ylabel="Iki tarafli test gucu", ylim=(0, 1),
              title=f"Ileriye donuk tek orneklem t testi plani (alfa={alfa:g})")
    panel.legend(loc="lower right")
    fig.tight_layout()
    hedef_dizin = Path("ciktilar/python")
    hedef_dizin.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef_dizin / "guc-egrisi.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/guc-egrisi.png")


def main():
    parser = argparse.ArgumentParser(description="B10: tek orneklem t testi ve ileriye donuk guc")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri, plan = pd.read_csv("veri.csv"), pd.read_csv("plan.csv")
    sonuc = hesapla(veri, plan)
    print(sonuc.to_string(index=False))
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(plan)
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}")


if __name__ == "__main__":
    main()