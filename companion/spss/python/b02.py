import pandas as pd
import numpy as np
from scipy import stats

d = pd.read_csv("companion/spss/csv/b02.csv")
assert not d.isna().any().any()
for v in ["school", "sex", "studytime"]:
    print(d[v].value_counts().sort_index())
    print(100*d[v].value_counts(normalize=True).sort_index())
print(d[["age", "g3"]].agg(
    ["count", "mean", "std", "min", "max"]))