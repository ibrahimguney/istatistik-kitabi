import pandas as pd
import numpy as np
from scipy import stats

d = pd.read_csv("companion/spss/csv/b01.csv")
assert not d.isna().any().any()
d["school"] = pd.Categorical(d.school.map({1:"GP", 2:"MS"}))
d["sex"] = pd.Categorical(d.sex.map({1:"F", 2:"M"}))
d["studytime"] = pd.Categorical(
    d.studytime, categories=[1, 2, 3, 4], ordered=True)
d.info()
print(d.isna().sum())
print(d.school.value_counts()); print(d.sex.value_counts())
print(d[["age", "g1", "g2", "g3"]].agg(
    ["count", "mean", "std", "min", "max"]))

import sys, scipy
print("Python:", sys.version)
print("pandas:", pd.__version__)
print("numpy:", np.__version__)
print("scipy:", scipy.__version__)