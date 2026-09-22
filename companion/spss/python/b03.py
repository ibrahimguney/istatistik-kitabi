import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

d = pd.read_csv("companion/spss/csv/b03.csv")
assert not d.isna().any().any()
print(d[["g3", "absences"]].agg(
    ["count", "mean", "std", "median", "min", "max"]))
print(stats.ttest_1samp(d.g3, 0).confidence_interval(.95))
print(stats.ttest_1samp(d.absences, 0).confidence_interval(.95))
fig, axes = plt.subplots(2, 2)
for row, v in enumerate(["g3", "absences"]):
    axes[row, 0].hist(d[v], bins=15)
    axes[row, 0].set_title(v)
    axes[row, 1].boxplot(d[v]); axes[row, 1].set_title(v)
plt.tight_layout(); plt.show()