import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
d = pd.read_csv('veri.csv')
assert list(d.columns)==['grup','puan']
assert not d.isna().any().any() and d.grup.isin([1,2]).all()
x=d.loc[d.grup==1,'puan'].to_numpy(); y=d.loc[d.grup==2,'puan'].to_numpy()
assert len(x)>1 and len(y)>1 and np.isfinite(d.puan).all()
r=stats.mannwhitneyu(x,y,alternative='two-sided',method='asymptotic',use_continuity=False)
s={'n_1':len(x),'n_2':len(y),'medyan_1':np.median(x),'medyan_2':np.median(y),'U_1':r.statistic,'U_min':min(r.statistic,len(x)*len(y)-r.statistic),'p_asimptotik':r.pvalue,'ustunluk':r.statistic/(len(x)*len(y)),'sira_biserial':2*r.statistic/(len(x)*len(y))-1}
esli=pd.read_csv('esli.csv'); uc=pd.read_csv('uc-grup.csv')
assert list(esli.columns)==['fark','sifir'] and not esli.isna().any().any() and (esli.sifir==0).all()
assert np.isfinite(esli.fark).all() and (esli.fark!=0).any()
f=esli.fark.to_numpy()
w=stats.wilcoxon(f,alternative='two-sided',zero_method='wilcox',method='approx',correction=False)
sg=stats.binomtest((f>0).sum(),(f!=0).sum(),p=.5,alternative='two-sided')
assert list(uc.columns)==['grup','puan'] and not uc.isna().any().any() and uc.grup.isin([1,2,3]).all() and np.isfinite(uc.puan).all()
groups=[uc.loc[uc.grup==g,'puan'].to_numpy() for g in [1,2,3]]
assert all(len(g)>1 for g in groups)
kw=stats.kruskal(*groups)
s.update({'wilcoxon_W_min':w.statistic,'wilcoxon_p_asimptotik':w.pvalue,'isaret_p_kesin':sg.pvalue,'kruskal_H':kw.statistic,'kruskal_p':kw.pvalue,'epsilon_kare':(kw.statistic-2)/(len(uc)-3)})
out=pd.DataFrame(list(s.items()),columns=['olcut','deger'])
print(out.to_string(index=False))
out.to_csv('sonuclar-python.csv',index=False)
if args.check:
    ref=pd.read_csv('beklenen-sonuclar.csv')
    if list(ref.olcut)!=list(out.olcut): raise AssertionError('Sonuç etiketleri farklı.')
    np.testing.assert_allclose(out.deger,ref.deger,rtol=1e-8,atol=1e-10)
    print('KONTROL BAŞARILI')
