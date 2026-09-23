import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
d = pd.read_csv('veri.csv')
assert list(d.columns) == ['grup','on','son']
assert d.grup.isin([1,2]).all() and d['on'].between(0,100).all()
assert d.son.dropna().between(0,100).all()
s = {'n':len(d), 'eksik_son':d.son.isna().sum(), 'eksik_oran':d.son.isna().mean()}
for g in [1,2]:
    x=d.loc[d.grup==g,'son'].dropna()
    assert len(x)>1
    s.update({f'n_{g}':len(x),f'ortalama_{g}':x.mean(),f'ss_{g}':x.std(ddof=1)})
s['on_eksik_son'] = d.loc[d.son.isna(),'on'].mean()
s['on_gozlenen_son'] = d.loc[d.son.notna(),'on'].mean()
out=pd.DataFrame(list(s.items()),columns=['olcut','deger'])
print(out.to_string(index=False))
out.to_csv('sonuclar-python.csv',index=False)
if args.check:
    ref=pd.read_csv('beklenen-sonuclar.csv')
    if list(ref.olcut)!=list(out.olcut): raise AssertionError('Sonuç etiketleri farklı.')
    np.testing.assert_allclose(out.deger,ref.deger,rtol=1e-8,atol=1e-10)
    print('KONTROL BAŞARILI')
