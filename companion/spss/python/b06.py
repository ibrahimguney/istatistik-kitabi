import pandas as pd
import numpy as np

veri = pd.read_csv("companion/spss/csv/b06.csv")
assert veri.shape == (395, 13)
assert not veri.isna().any().any()
basit = veri.loc[veri.srs40 == 1].copy()
tabakali = veri.loc[veri.strat40 == 1].copy()
assert len(basit) == len(tabakali) == 40
print(pd.DataFrame({
    "tam_dosya": veri.g3.agg(["count", "mean", "std"]),
    "basit_rastgele": basit.g3.agg(["count", "mean", "std"])
}))
okul = tabakali.school.map({1: "GP", 2: "MS"})
frekans = okul.value_counts().reindex(["GP", "MS"])
print(frekans); print(100 * frekans / len(tabakali))
print(len(tabakali)); print(tabakali.strw.sum())
print(np.average(tabakali.g3, weights=tabakali.strw))