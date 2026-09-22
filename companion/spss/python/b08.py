import pandas as pd
import numpy as np
from scipy import stats

d = pd.read_csv("companion/spss/csv/b08.csv")
assert not d.isna().any().any()
mean_ci = stats.ttest_1samp(d.g3, 0).confidence_interval(.95)
print(mean_ci)
print(d.pass10.value_counts().sort_index())
n, p = len(d), d.pass10.mean()
z = stats.norm.ppf(.975); den = 1 + z*z/n
center = (p + z*z/(2*n))/den
half = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
wilson = (center-half, center+half)
print(p, wilson)