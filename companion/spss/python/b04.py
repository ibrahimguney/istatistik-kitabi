import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

d = pd.read_csv("companion/spss/csv/b04.csv")
assert not d.isna().any().any()
print(d[["ort5", "ort30"]].agg(
    ["count", "mean", "std", "min", "max"]))
fig, axes = plt.subplots(1, 2)
for ax, v in zip(axes, ["ort5", "ort30"]):
    x = d[v]
    ax.hist(x, bins=np.arange(0, 20.5, .5), density=True)
    grid = np.linspace(0, 20, 1000)
    ax.plot(grid, stats.norm.pdf(grid, x.mean(), x.std()))
    ax.set_title(v)
    ax.set_xlim(0, 20); ax.set_ylim(0, .6)
plt.tight_layout(); plt.show()