import pandas as pd
import numpy as np
from scipy import stats

veri = pd.read_csv("companion/spss/csv/b11.csv")
assert veri.shape == (395, 10)
assert not veri.isna().any().any()
assert veri.id.is_unique
assert veri.sex.isin([1, 2]).all()
assert veri.pass10.eq((veri.g3 >= 10).astype(int)).all()
grup_F = veri.loc[veri.sex == 1, "g3"]
grup_M = veri.loc[veri.sex == 2, "g3"]
fark = veri.g3-veri.g1
welch = stats.ttest_ind(grup_F, grup_M,
    equal_var=False, alternative="two-sided")
eslesmis = stats.ttest_rel(veri.g3, veri.g1,
                          alternative="two-sided")
print(welch); print(welch.confidence_interval(.95))
print(eslesmis); print(eslesmis.confidence_interval(.95))

def betimsel(degerler):
    return dict(n=len(degerler), ort=degerler.mean(),
        ss=degerler.std(ddof=1),
        sh=degerler.std(ddof=1)/np.sqrt(len(degerler)))

def test_ozeti(sonuc, ortalama_fark):
    aralik = sonuc.confidence_interval(.95)
    return dict(t=sonuc.statistic, df=sonuc.df,
        p_iki_yonlu=sonuc.pvalue, fark=ortalama_fark,
        alt=aralik.low, ust=aralik.high)

ozetler = {
    "F": betimsel(grup_F), "M": betimsel(grup_M),
    "Welch": test_ozeti(welch, grup_F.mean()-grup_M.mean()),
    "G3": betimsel(veri.g3), "G1": betimsel(veri.g1),
    "Eslesmis": test_ozeti(eslesmis, fark.mean()),
    "Fark": dict(betimsel(fark),
                 dz=fark.mean()/fark.std(ddof=1))}
for baslik, ozet in ozetler.items():
    print(baslik)
    for ad, deger in ozet.items():
        print(f"{ad}: {deger:.13f}")
print(int((veri.g3 == 0).sum()))

import matplotlib.pyplot as plt

sekil, eksenler = plt.subplots(1, 3, figsize=(12, 4))
eksenler[0].boxplot([grup_F, grup_M])
eksenler[0].set_xticks([1, 2], ["F", "M"])
eksenler[0].set_title("G3")
eksenler[1].boxplot(fark); eksenler[1].set_title("G3-G1")
eksenler[2].hist(fark, bins=15)
eksenler[2].set_title("G3-G1")
plt.tight_layout(); plt.show()