import argparse
import math
import platform
from pathlib import Path

import numpy as np
import pandas as pd


def hazirla(veri):
    if list(veri.columns) != ["saat"]:
        raise ValueError("CSV yalniz saat sutununu icermeli.")
    if len(veri) < 2:
        raise ValueError("Orneklem varyansi icin en az iki gozlem gerekli.")
    if veri.isna().any().any():
        raise ValueError("Eksik deger kabul edilmez.")
    if pd.api.types.is_bool_dtype(veri["saat"]):
        raise ValueError("Mantiksal deger sure olamaz.")
    temiz = veri.copy(deep=True)
    temiz["saat"] = pd.to_numeric(temiz["saat"], errors="raise").astype(float)
    if not np.isfinite(temiz["saat"]).all() or (temiz["saat"] < 0).any():
        raise ValueError("Sureler sonlu ve negatif olmayan sayilar olmali.")
    return temiz


def histogram(saat):
    ust = max(15, 3 * math.ceil(float(np.max(saat)) / 3))
    sinirlar = np.arange(0, ust + 1, 3, dtype=float)
    sayilar, _ = np.histogram(saat, bins=sinirlar)
    etiketler = [
        f"[{alt:g};{ust:g}{']' if index == len(sayilar) - 1 else ')'}"
        for index, (alt, ust) in enumerate(zip(sinirlar[:-1], sinirlar[1:]))
    ]
    return sinirlar, sayilar, etiketler


def kutu_ozeti(saat):
    q1, medyan, q3 = np.quantile(saat, [0.25, 0.5, 0.75], method="linear")
    iqr = q3 - q1
    alt_sinir, ust_sinir = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    aykiri = (saat < alt_sinir) | (saat > ust_sinir)
    return {
        "q1": q1, "med": medyan, "q3": q3,
        "whislo": np.min(saat[~aykiri]), "whishi": np.max(saat[~aykiri]),
        "fliers": saat[aykiri], "label": "Saat",
    }, alt_sinir, ust_sinir


def hesapla(veri):
    saat = hazirla(veri)["saat"].to_numpy()
    kutu, alt_sinir, ust_sinir = kutu_ozeti(saat)
    duyarlilik = saat[saat != 13]
    satirlar = [
        ("veri", "satir_sayisi", len(saat)),
        ("veri", "degisken_sayisi", 1),
        ("saat", "gecerli", len(saat)),
        ("saat", "eksik", 0),
        ("saat", "toplam", np.sum(saat)),
        ("saat", "ortalama", np.mean(saat)),
        ("saat", "medyan", np.median(saat)),
        ("saat", "en_kucuk", np.min(saat)),
        ("saat", "en_buyuk", np.max(saat)),
        ("saat", "aciklik", np.ptp(saat)),
        ("saat", "orneklem_varyansi", np.var(saat, ddof=1)),
        ("saat", "orneklem_std", np.std(saat, ddof=1)),
        ("saat", "q1", kutu["q1"]),
        ("saat", "q3", kutu["q3"]),
        ("saat", "iqr", kutu["q3"] - kutu["q1"]),
        ("saat", "alt_sinir", alt_sinir),
        ("saat", "ust_sinir", ust_sinir),
        ("saat", "aykiri_sayisi", len(kutu["fliers"])),
        ("duyarlilik_13_haric", "hacim", len(duyarlilik)),
        ("duyarlilik_13_haric", "ortalama", np.mean(duyarlilik) if len(duyarlilik) else np.nan),
        ("duyarlilik_13_haric", "medyan", np.median(duyarlilik) if len(duyarlilik) else np.nan),
    ]
    _, sayilar, etiketler = histogram(saat)
    satirlar.extend(("histogram", etiket, sayi) for etiket, sayi in zip(etiketler, sayilar))
    return pd.DataFrame(satirlar, columns=["degisken", "olcu", "deger"])


def kontrol_et(sonuc, beklenen):
    if list(beklenen.columns) != ["degisken", "olcu", "deger"]:
        raise ValueError("Kontrol CSV sutunlari uyusmuyor.")
    anahtarlar = ["degisken", "olcu"]
    if not sonuc[anahtarlar].equals(beklenen[anahtarlar]):
        raise ValueError("Kontrol etiketleri veya sirasi uyusmuyor.")
    for gercek, hedef in zip(sonuc["deger"], beklenen["deger"]):
        if not math.isclose(gercek, float(hedef), rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(f"Kontrol degeri uyusmuyor: {gercek} != {hedef}")
    print(f"DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.")


def grafik_kaydet(veri, klasor):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    saat = hazirla(veri)["saat"].to_numpy()
    sinirlar, _, _ = histogram(saat)
    kutu, _, _ = kutu_ozeti(saat)
    fig, eksenler = plt.subplots(1, 2, figsize=(10, 4))
    eksenler[0].hist(saat, bins=sinirlar, color="#8FB8D8", edgecolor="white")
    eksenler[0].set(xlabel="Haftalik calisma suresi (saat)", ylabel="Frekans",
                   title="Histogram", xticks=sinirlar)
    eksenler[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    eksenler[1].bxp([kutu], orientation="horizontal", showfliers=True)
    eksenler[1].set(xlabel="Haftalik calisma suresi (saat)", title="Kutu grafigi (type 7)")
    fig.tight_layout()
    klasor = Path(klasor)
    klasor.mkdir(parents=True, exist_ok=True)
    hedef = klasor / "betimsel-grafikler.png"
    fig.savefig(hedef, dpi=150)
    plt.close(fig)
    print(f"Grafik: {hedef}")


def main():
    parser = argparse.ArgumentParser(description="B03: betimsel istatistik uygulamasi")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri = pd.read_csv("veri.csv")
    sonuc = hesapla(veri)
    print(sonuc.to_string(index=False))
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(veri, "ciktilar/python")
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}")


if __name__ == "__main__":
    main()