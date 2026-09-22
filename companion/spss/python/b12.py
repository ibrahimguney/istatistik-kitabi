import pandas as pd
import numpy as np
from scipy import stats

veri = pd.read_csv("companion/spss/csv/b12.csv")
assert veri.shape == (395, 10)
assert not veri.isna().any().any()
assert veri.id.is_unique
assert veri.sex.isin([1, 2]).all()
assert veri.pass10.isin([0, 1]).all()
assert veri.pass10.eq((veri.g3 >= 10).astype(int)).all()
tablo = pd.crosstab(veri.sex, veri.pass10).reindex(
    index=[1, 2], columns=[0, 1], fill_value=0)
tablo.index = ["F", "M"]
tablo.columns = ["10_alti", "10_ve_uzeri"]
ki_kare, p_degeri, serbestlik, beklenen = (
    stats.chi2_contingency(tablo, correction=False))
yuzdeler = 100 * tablo.div(tablo.sum(axis=1), axis=0)
artiklar = (tablo.to_numpy()-beklenen)/np.sqrt(beklenen)
print("satir:", len(veri), "sutun:", veri.shape[1])
print("eksik:", int(veri.isna().sum().sum()))
print("sifir_not:", int((veri.g3 == 0).sum()))
print(tablo)
print("Satir toplamlari:", tablo.sum(axis=1).to_dict())
print("Sutun toplamlari:", tablo.sum(axis=0).to_dict())

for baslik, degerler in [
    ("Satir yuzdeleri", yuzdeler.to_numpy()),
    ("Beklenen sayimlar", beklenen),
    ("Pearson hucre artiklari", artiklar)
]:
    print(baslik)
    cerceve = pd.DataFrame(degerler,
        index=tablo.index, columns=tablo.columns)
    print(cerceve.to_string(
        float_format=lambda sayi: f"{sayi:.13f}"))

ozet = dict(n=int(tablo.to_numpy().sum()),
    ki_kare=ki_kare, df=serbestlik, p=p_degeri,
    min_beklenen=beklenen.min(),
    bes_alti_hucre=int((beklenen < 5).sum()),
    cramer_v=np.sqrt(ki_kare/len(veri)))
for ad, deger in ozet.items():
    print(f"{ad}: {deger:.13f}")