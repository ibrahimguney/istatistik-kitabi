import pandas as pd
import numpy as np
from scipy import stats

veri = pd.read_csv("companion/spss/csv/b14.csv")
assert veri.shape == (395, 10)
assert not veri.isna().any().any()
assert veri.id.is_unique
assert veri.sex.isin([1, 2]).all()
assert veri.pass10.isin([0, 1]).all()
assert veri.pass10.eq((veri.g3 >= 10).astype(int)).all()

def betimsel(degerler):
    return dict(n=len(degerler), ortalama=degerler.mean(),
        ss=degerler.std(ddof=1), minimum=degerler.min(),
        maksimum=degerler.max())

def yazdir(baslik, ozet):
    print("\n" + baslik)
    for ad, deger in ozet.items():
        print(f"{ad}: {deger:.15g}")

def tablo_yazdir(baslik, cerceve):
    print("\n" + baslik)
    print(cerceve.to_string(
        float_format=lambda deger: f"{deger:.15g}"))

yazdir("Veri kontrolu", dict(satir=len(veri),
    sutun=veri.shape[1], eksik=int(veri.isna().sum().sum()),
    sifir_not=int((veri.g3 == 0).sum())))
yazdir("G1 betimsel", betimsel(veri.g1))
yazdir("G3 betimsel", betimsel(veri.g3))
test = stats.ttest_1samp(veri.g3, 10,
                         alternative="two-sided")
aralik = test.confidence_interval(.95)
yazdir("Tek orneklem testi ve guven araliklari", dict(
    t=test.statistic, df=len(veri)-1,
    p_iki_yonlu=test.pvalue,
    ortalama_fark=veri.g3.mean()-10,
    ortalama_alt=aralik.low, ortalama_ust=aralik.high,
    fark_alt=aralik.low-10, fark_ust=aralik.high-10))

tablo = pd.crosstab(veri.sex, veri.pass10).reindex(
    index=[1, 2], columns=[0, 1], fill_value=0)
tablo.index = ["F", "M"]
tablo.columns = ["10_alti", "10_ve_uzeri"]
tablo_yazdir("Capraz tablo", tablo)
print("Satir toplamlari:", tablo.sum(axis=1).to_dict())
print("Sutun toplamlari:", tablo.sum(axis=0).to_dict())
print("Genel toplam:", int(tablo.to_numpy().sum()))
yuzdeler = 100*tablo.div(tablo.sum(axis=1), axis=0)
tablo_yazdir("Satir yuzdeleri", yuzdeler)
ki_kare, p_degeri, serbestlik, beklenen = (
    stats.chi2_contingency(tablo, correction=False))
tablo_yazdir("Beklenen sayimlar", pd.DataFrame(
    beklenen, index=tablo.index, columns=tablo.columns))
yazdir("Pearson ki-kare testi", dict(
    ki_kare=ki_kare, df=serbestlik, p=p_degeri,
    cramer_v=np.sqrt(ki_kare/tablo.to_numpy().sum()),
    min_beklenen=beklenen.min(),
    bes_alti_hucre=int((beklenen < 5).sum())))

korelasyon = stats.pearsonr(veri.g1, veri.g3)
yazdir("Pearson korelasyonu", dict(n=len(veri),
    r=korelasyon.statistic, p_iki_yonlu=korelasyon.pvalue))
pozitif = veri.loc[veri.g3 > 0].copy()
yazdir("Pozitif G3", betimsel(pozitif.g3))
yazdir("Tum G3", betimsel(veri.g3))
assert len(veri) == 395
assert len(pozitif) == 357

import matplotlib.pyplot as plt

plt.figure(figsize=(6, 5))
plt.boxplot(veri.g3)
plt.title("Tum kayitlarda yil sonu notu")
plt.ylabel("G3")
plt.xticks([1], ["Tum kayitlar"])
plt.tight_layout(); plt.show()