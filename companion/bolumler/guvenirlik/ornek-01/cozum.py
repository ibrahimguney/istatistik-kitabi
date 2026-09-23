import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
d = pd.read_csv('veri.csv')
assert list(d.columns)==['M1','M2','M3','M4','M5']
assert not d.isna().any().any() and d.isin([1,2,3,4,5]).all().all()
def alpha(x):
    k=x.shape[1]; v=x.sum(axis=1).var(ddof=1)
    if len(x)<2 or k<2 or v<=0: raise ValueError('Alfa için yeterli değişkenlik yok.')
    return k/(k-1)*(1-x.var(ddof=1).sum()/v)
x=d.copy(); x['M4']=6-x['M4']
s={'n':len(x),'alpha_ham':alpha(d),'alpha':alpha(x),'toplam_ortalama':x.sum(axis=1).mean()}
for col in x:
    rest=x.drop(columns=col)
    s[col+'_duzeltilmis_r']=x[col].corr(rest.sum(axis=1))
    s[col+'_silinirse_alpha']=alpha(rest)
out=pd.DataFrame(list(s.items()),columns=['olcut','deger'])
print(out.to_string(index=False))
out.to_csv('sonuclar-python.csv',index=False)
if args.check:
    ref=pd.read_csv('beklenen-sonuclar.csv')
    if list(ref.olcut)!=list(out.olcut): raise AssertionError('Sonuç etiketleri farklı.')
    np.testing.assert_allclose(out.deger,ref.deger,rtol=1e-8,atol=1e-10)
    print('KONTROL BAŞARILI')
