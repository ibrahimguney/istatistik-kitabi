import argparse
import math
from pathlib import Path
import platform

import numpy as np
import pandas as pd


def sayisal_kontrol(veri, sutunlar, en_az):
    if list(veri.columns) != sutunlar or len(veri) < en_az:
        raise ValueError("Sutun duzeni veya satir sayisi gecersiz.")
    if veri.isna().any().any():
        raise ValueError("Eksik deger kabul edilmez.")
    for sutun in sutunlar:
        if not pd.api.types.is_numeric_dtype(veri[sutun]) or pd.api.types.is_bool_dtype(veri[sutun]):
            raise ValueError("Sayisal degerler gerekli.")
    if not np.isfinite(veri.to_numpy(dtype=float)).all():
        raise ValueError("Sonlu degerler gerekli.")


def hazirla(veri, benzetim):
    sayisal_kontrol(veri, ["yanit"], 1)
    if not veri["yanit"].isin([0, 1]).all():
        raise ValueError("Yanitlar yalniz 0/1 olmali.")
    sayisal_kontrol(benzetim, ["tekrar", "basari"], 2)
    temiz = benzetim.sort_values("tekrar").reset_index(drop=True).copy(deep=True)
    if not np.array_equal(temiz["tekrar"], np.arange(1, len(temiz) + 1)):
        raise ValueError("Tekrar kimlikleri 1..B arasinda benzersiz olmali.")
    basari = temiz["basari"].to_numpy(dtype=float)
    if not ((basari >= 0) & (basari <= 50) & (basari == np.floor(basari))).all():
        raise ValueError("Basari sayilari 0..50 arasinda tam sayi olmali.")
    return veri.copy(deep=True), temiz


def hesapla(veri, benzetim):
    gozlem, tekrarlar = hazirla(veri, benzetim)
    hacim = len(gozlem)
    oran = gozlem["yanit"].mean()
    tahminler = tekrarlar["basari"].to_numpy(dtype=float) / 50
    merkez = tahminler.mean()
    yanlilik = merkez - 0.40
    varyans = np.var(tahminler, ddof=0)
    satirlar = [
        ("gozlem", "hacim", hacim),
        ("gozlem", "olumlu", gozlem["yanit"].sum()),
        ("gozlem", "olumsuz", hacim - gozlem["yanit"].sum()),
        ("gozlem", "oran", oran),
        ("gozlem", "yaklasik_se", math.sqrt(oran * (1 - oran) / hacim)),
        ("gozlem", "yaklasik_varyans", oran * (1 - oran) / hacim),
        ("p_hat_060", "se_25", math.sqrt(0.60 * 0.40 / 25)),
        ("p_hat_060", "se_400", math.sqrt(0.60 * 0.40 / 400)),
        ("benzetim", "tekrar_sayisi", len(tekrarlar)),
        ("benzetim", "orneklem_hacmi", 50),
        ("benzetim", "gercek_oran", 0.40),
        ("benzetim", "merkez", merkez),
        ("benzetim", "yanlilik", yanlilik),
        ("benzetim", "varyans_B", varyans),
        ("benzetim", "varyans_Beksi1", np.var(tahminler, ddof=1)),
        ("benzetim", "ampirik_se", np.std(tahminler, ddof=1)),
        ("benzetim", "mse", np.mean((tahminler - 0.40) ** 2)),
        ("benzetim", "mse_ayrisimi", varyans + yanlilik ** 2),
        ("benzetim", "kuramsal_yanlilik", 0),
        ("benzetim", "kuramsal_se", math.sqrt(0.40 * 0.60 / 50)),
        ("benzetim", "kuramsal_mse", 0.40 * 0.60 / 50),
    ]
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


def grafik_kaydet(veri, benzetim):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    gozlem, tekrarlar = hazirla(veri, benzetim)
    frekans = gozlem["yanit"].value_counts().reindex([0, 1], fill_value=0)
    adetler = tekrarlar["basari"].value_counts().reindex(range(51), fill_value=0)
    fig, eksenler = plt.subplots(1, 2, figsize=(10, 4))
    eksenler[0].bar([0, 1], frekans / len(gozlem), color="#8FB8D8", width=0.6)
    eksenler[0].set(xticks=[0, 1], xlabel="Ikili yanit", ylabel="Gozlenen oran", ylim=(0, 1),
                   title=f"Gozlenen ornek: n={len(gozlem)}")
    eksenler[1].bar(np.arange(51) / 50, adetler / len(tekrarlar), width=0.016, color="#1F4E79")
    eksenler[1].axvline(0.40, color="#087F5B", linestyle="--", label="Gercek p=0.40")
    eksenler[1].set(xlim=(0, 1), xlabel="Oran tahmini", ylabel="Benzetim goreli frekansi",
                   title=f"n=50; {len(tekrarlar)} tekrar")
    eksenler[1].legend(fontsize="small")
    fig.tight_layout()
    hedef = Path("ciktilar/python")
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / "oran-tahmini.png", dpi=150)
    plt.close(fig)
    print("Grafik: ciktilar/python/oran-tahmini.png")


def main():
    parser = argparse.ArgumentParser(description="B07: oran, yanlilik ve MSE")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--grafik", action="store_true")
    secenek = parser.parse_args()
    veri = pd.read_csv("veri.csv")
    benzetim = pd.read_csv("benzetim.csv")
    sonuc = hesapla(veri, benzetim)
    print(sonuc.to_string(index=False))
    if secenek.check:
        kontrol_et(sonuc, pd.read_csv("beklenen-sonuclar.csv"))
    if secenek.grafik:
        grafik_kaydet(veri, benzetim)
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}")


if __name__ == "__main__":
    main()