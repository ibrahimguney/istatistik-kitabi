import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

d = pd.read_csv("companion/spss/csv/b05.csv")
assert not d.isna().any().any()
print(d[["ort5", "ort30", "ort100", "z5", "z100"]].agg(
    ["count", "mean", "std"]))
kapsama = d.z100.abs() <= 1.96
print(kapsama.value_counts().sort_index())
print(100*kapsama.mean())
fig, axes = plt.subplots(1, 2)
for ax, v in zip(axes, ["z5", "z100"]):
    ax.hist(d[v], bins=np.linspace(-5, 5, 41), density=True)
    grid = np.linspace(-5, 5, 1000)
    ax.plot(grid, stats.norm.pdf(grid)); ax.set_title(v)
    ax.set_xlim(-5, 5); ax.set_ylim(0, .6)
    for sinir in [-1.96, 1.96]:
        ax.axvline(sinir, linestyle="--", color="gray")
plt.tight_layout(); plt.show()