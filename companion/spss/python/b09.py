import pandas as pd
import numpy as np
from scipy import stats

veri = pd.read_csv("companion/spss/csv/b09.csv")
assert veri.shape == (395, 10)
assert not veri.isna().any().any()
assert veri.pass10.eq((veri.g3 >= 10).astype(int)).all()
gozlem_sayisi = len(veri)
ortalama = veri.g3.mean()
standart_sapma = veri.g3.std(ddof=1)
standart_hata = standart_sapma / np.sqrt(gozlem_sayisi)
sonuc = stats.ttest_1samp(
    veri.g3, popmean=10, alternative="two-sided")
ortalama_alt, ortalama_ust = stats.t.interval(
    .95, df=gozlem_sayisi-1,
    loc=ortalama, scale=standart_hata)
ozet = pd.Series({
    "n": gozlem_sayisi, "ort": ortalama, "ss": standart_sapma,
    "sh_ort": standart_hata, "t": sonuc.statistic,
    "df": gozlem_sayisi-1, "p_iki_yonlu": sonuc.pvalue,
    "fark": ortalama-10,
    "ort_alt": ortalama_alt, "ort_ust": ortalama_ust,
    "fark_alt": ortalama_alt-10, "fark_ust": ortalama_ust-10
})
print(ozet.to_string(float_format=lambda deger: f"{deger:.13f}"))
print(int(veri.g3.eq(0).sum()))