import pandas as pd
import numpy as np
from scipy import stats

veri = pd.read_csv("companion/spss/csv/b13.csv")
assert veri.shape == (395, 10)
assert not veri.isna().any().any()
assert veri.id.is_unique
assert veri.pass10.eq((veri.g3 >= 10).astype(int)).all()
ilk_not = veri.g1.to_numpy()
son_not = veri.g3.to_numpy()
korelasyon = stats.pearsonr(ilk_not, son_not)
model = stats.linregress(ilk_not, son_not)
serbestlik = len(veri)-2
kritik = stats.t.ppf(.975, serbestlik)
egim_araligi = (model.slope
    + np.array([-1, 1])*kritik*model.stderr)
tahmin = model.intercept+model.slope*ilk_not
artik = son_not-tahmin
model_sh = np.sqrt(np.sum(artik**2)/serbestlik)
zresid = artik/model_sh
zpred = (tahmin-tahmin.mean())/tahmin.std(ddof=1)

print("Satir:", len(veri), "Sutun:", veri.shape[1])
print("Eksik:", int(veri.isna().sum().sum()))
print("Sifir not:", int((veri.g3 == 0).sum()))
ozet = {
    "Pearson r": korelasyon.statistic,
    "Korelasyon p": korelasyon.pvalue,
    "Sabit": model.intercept, "Egim": model.slope,
    "Egim standart hatasi": model.stderr,
    "Egim p": model.pvalue,
    "Egim GA alt": egim_araligi[0],
    "Egim GA ust": egim_araligi[1],
    "R2": model.rvalue**2,
    "Duzeltilmis R2": 1-(1-model.rvalue**2)
        * (len(veri)-1)/serbestlik,
    "Model standart hatasi": model_sh,
    "F": (model.slope/model.stderr)**2,
    "Artik serbestlik derecesi": serbestlik,
    "G1=10 ortalama tahmini": model.intercept+10*model.slope}
for ad, deger in ozet.items():
    print(f"{ad}: {deger:.15g}")

import matplotlib.pyplot as plt

sekil, eksenler = plt.subplots(1, 3, figsize=(15, 4))
sirali = np.argsort(ilk_not)
eksenler[0].scatter(ilk_not, son_not, alpha=.6)
eksenler[0].plot(ilk_not[sirali], tahmin[sirali],
                 color="red")
eksenler[0].set(xlabel="G1", ylabel="G3", title="G1 - G3")
eksenler[1].scatter(zpred, zresid, alpha=.6)
eksenler[1].axhline(0, color="black", linestyle="--")
eksenler[1].set(xlabel="ZPRED", ylabel="ZRESID",
                title="Artik - Tahmin")
eksenler[2].hist(zresid, bins=15, edgecolor="black")
eksenler[2].set(xlabel="ZRESID", ylabel="Frekans",
                title="Artik histogrami")
plt.tight_layout(); plt.show()