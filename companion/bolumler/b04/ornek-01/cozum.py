import argparse
from itertools import product
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd


def sayisal_veri(veri, sutunlar):
    if list(veri.columns) != sutunlar or veri.empty:
        raise ValueError("Bos veri veya yanlis sutun duzeni.")
    if veri.isna().any().any():
        raise ValueError("Eksik deger kabul edilmez.")
    temiz = veri.copy(deep=True)
    for sutun in sutunlar:
        if not pd.api.types.is_numeric_dtype(temiz[sutun]) or pd.api.types.is_bool_dtype(temiz[sutun]):
            raise ValueError("Girdiler sayisal olmali.")
        temiz[sutun] = temiz[sutun].astype(float)
    if not np.isfinite(temiz.to_numpy()).all():
        raise ValueError("Girdiler sonlu olmali.")
    return temiz


def ciftleri_uret(evren):
    degerler = sayisal_veri(evren, ["deger"])["deger"]
    if len(degerler) < 2 or degerler.duplicated().any():
        raise ValueError("En az iki farkli, esit olasilikli evren degeri gerekli.")
    return pd.DataFrame(product(degerler, repeat=2), columns=["ilk", "ikinci"])


def hazirla(evren, veri):
    beklenen = ciftleri_uret(evren)
    ciftler = sayisal_veri(veri, ["ilk", "ikinci"])
    sirali = ciftler.sort_values(["ilk", "ikinci"]).reset_index(drop=True)
    hedef = beklenen.sort_values(["ilk", "ikinci"]).reset_index(drop=True)
    if not sirali.equals(hedef):
        raise ValueError("veri.csv evrenin tum sirali ciftlerini birer kez icermeli.")
    return ciftler


def dagilim_hesapla(evren, veri):
    ciftler = hazirla(evren, veri)
    ortalamalar = ciftler.mean(axis=1)
    dagilim = ortalamalar.value_counts().sort_index().rename_axis("ortalama").reset_index(name="frekans")
    dagilim["olasilik"] = dagilim["frekans"] / len(ciftler)
    return ortalamalar, dagilim


def hesapla(evren, veri):
    ortalamalar, dagilim = dagilim_hesapla(evren, veri)
    degerler = evren["deger"].to_numpy(dtype=float)
    mu = degerler.mean()
    evren_varyansi = np.mean((degerler - mu) ** 2)
    merkez = ortalamalar.mean()
    varyans = np.mean((ortalamalar - merkez) ** 2)
    satirlar = [
        ("evren", "hacim", len(degerler)),
        ("evren", "ortalama", mu),
        ("evren", "varyans", evren_varyansi),
        ("evren", "standart_sapma", math.sqrt(evren_varyansi)),
        ("tasarim", "orneklem_hacmi", 2),
        ("tasarim", "sirali_sonuc_sayisi", len(ortalamalar)),
        ("tasarim", "olasilik_toplami", dagilim["olasilik"].sum()),
        ("orneklem_ortalamasi", "beklenen_deger", merkez),
        ("orneklem_ortalamasi", "varyans", varyans),
        ("orneklem_ortalamasi", "standart_hata", math.sqrt(varyans)),
        ("orneklem_ortalamasi", "kuramsal_standart_hata", math.sqrt(evren_varyansi / 2)),
        ("orneklem_ortalamasi", "yanlilik", merkez - mu),
        ("orneklem_ortalamasi", "p_en_az_7", np.mean(ortalamalar >= 7)),
        ("orneklem_ortalamasi", "p_esit_5", np.mean(ortalamalar == 5)),
    ]
    for satir in dagilim.itertuples(index=False):
        etiket = f"ortalama_{satir.ortalama:.15g}"
        satirlar.extend([(etiket, "frekans", satir.frekans), (etiket, "olasilik", satir.olasilik)])
    return pd.DataFrame(satirlar, columns=["degisken", "olcu", "deger"])


def kontrol_et(sonuc, beklenen):
    if list(beklenen.columns) != ["degisken", "olcu", "deger"]:
        raise ValueError("Kontrol sutunlari uyusmuyor.")
    if not sonuc[["degisken", "olcu"]].equals(beklenen[["degisken", "olcu"]]):
        raise ValueError("Kontrol etiketleri veya sirasi uyusmuyor.")
    hedefler = pd.to_numeric(beklenen["deger"], errors="raise")
    if not np.isfinite(hedefler).all() or not np.isfinite(sonuc["deger"]).all():
        raise ValueError("Kontrol degerleri sonlu olmali.")
    for gercek, hedef in zip(sonuc["deger"], hedefler):
        if not math.isclose(gercek, hedef, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(f"Kontrol uyusmazligi: {gercek} != {hedef}")
    print(f"DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.")


def grafik_kaydet(evren, veri):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _, dagilim = dagilim_hesapla(evren, veri)
    degerler = np.sort(evren["deger"].to_numpy(dtype=float))
    fig, eksenler = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)
    eksenler[0].bar(degerler, np.repeat(1 / len(degerler), len(degerler)), width=0.6, color="#8FB8D8")
    eksenler[1].bar(dagilim["ortalama"], dagilim["olasilik"], width=0.6, color="#1F4E79")
    eksenler[0].set(title="Tek cekim X", xlabel="Deger", ylabel="Olasilik")
    eksenler[1].set(title="Iki cekimin ortalamasi", xlabel="Orneklem ortalamasi")
    for eksen in eksenler:
        eksen.axvline(degerler.mean(), color="#087F5B", linestyle="--", label="Evren ortalamasi")
        eksen.set_xticks(sorted(set(degerler) | set(dagilim["ortalama"])))
    eksenler[1].legend(fontsize="small")
    fig.tight_layout()
    klasor = Path("ciktilar/python")
    klasor.mkdir(parents=True, exist_ok=True)
    fig.savefig(klasor / "ornekleme-dagilimi.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/ornekleme-dagilimi.png")


def main():
    parser = argparse.ArgumentParser(description="B04: tam sayimla ornekleme dagilimi")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    evren = pd.read_csv("evren.csv")
    veri = pd.read_csv("veri.csv")
    sonuc = hesapla(evren, veri)
    print(sonuc.to_string(index=False))
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(evren, veri)
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}")


if __name__ == "__main__":
    main()