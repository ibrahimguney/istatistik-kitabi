import pandas as pd
import numpy as np

veri = pd.read_csv("companion/spss/csv/b07.csv")
assert veri.shape == (395, 10)
assert not veri.isna().any().any()
assert veri.pass10.eq((veri.g3 >= 10).astype(int)).all()
gozlem_sayisi = len(veri)
ortalama = veri.g3.mean()
standart_sapma = veri.g3.std(ddof=1)
oran = veri.pass10.mean()
frekans = veri.pass10.value_counts().sort_index()
print(frekans); print(100 * frekans / gozlem_sayisi)
print(pd.Series({
    "n": gozlem_sayisi, "ort": ortalama, "ss": standart_sapma,
    "sh_ort": standart_sapma / np.sqrt(gozlem_sayisi),
    "oran": oran,
    "sh_oran": np.sqrt(oran*(1-oran)/gozlem_sayisi)
}))
print(int((veri.g3 == 0).sum()))