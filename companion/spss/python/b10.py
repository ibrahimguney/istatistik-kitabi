import pandas as pd
import numpy as np
from scipy import stats, optimize

veri = pd.read_csv("companion/spss/csv/b10.csv")
assert veri.shape == (395, 10)
assert not veri.isna().any().any()
assert veri.pass10.eq((veri.g3 >= 10).astype(int)).all()
sonuc = stats.ttest_1samp(veri.g3, 10,
                         alternative="two-sided")
aralik = sonuc.confidence_interval(.95)
ortalama = veri.g3.mean()
standart_sapma = veri.g3.std(ddof=1)
ozet = dict(n=len(veri), ort=ortalama, ss=standart_sapma,
    sh_ort=standart_sapma/np.sqrt(len(veri)),
    t=sonuc.statistic, df=len(veri)-1,
    p_iki_yonlu=sonuc.pvalue, fark=ortalama-10,
    etki_d=(ortalama-10)/standart_sapma,
    ort_alt=aralik.low, ort_ust=aralik.high)
for ad, deger in ozet.items():
    print(f"{ad}: {deger:.13f}")
print(int((veri.g3 == 0).sum()))

def guc(hacim):
    serbestlik = hacim - 1
    kritik = stats.t.ppf(.975, serbestlik)
    kayma = np.sqrt(hacim) / 4.581442611
    return (stats.nct.cdf(-kritik, serbestlik, kayma)
            + stats.nct.sf(kritik, serbestlik, kayma))

n_kesirli = optimize.brentq(
    lambda hacim: guc(hacim)-.80, 2, 1000)
n_plan = int(np.ceil(n_kesirli))
assert guc(n_plan-1) < .80 <= guc(n_plan)
print("n_kesirli:", n_kesirli, "n_plan:", n_plan)
print("guc_plan:", guc(n_plan))
print("n_bir_eksik:", n_plan-1,
      "guc_bir_eksik:", guc(n_plan-1))