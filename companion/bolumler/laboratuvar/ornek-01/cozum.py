import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
d = pd.read_csv('veri.csv')
assert list(d.columns)==['id','grup','on','son','saat']
assert not d.isna().any().any() and d.id.is_unique and d.grup.isin([1,2]).all()
assert d[['on','son']].apply(lambda x:x.between(0,100)).all().all() and d.saat.between(0,40).all()
d['degisim']=d.son-d['on']
a=d.loc[d.grup==1,'son']; b=d.loc[d.grup==2,'son']
assert len(a)>1 and len(b)>1
paired=stats.ttest_rel(d.son,d['on']); welch=stats.ttest_ind(a,b,equal_var=False)
r=stats.pearsonr(d.saat,d.son); lm=stats.linregress(d.saat,d.son)
ga=stats.t.interval(.95,len(d)-1,loc=d.son.mean(),scale=stats.sem(d.son))
s={'n':len(d),'son_ortalama':d.son.mean(),'degisim_ortalama':d.degisim.mean(),'ga_alt':ga[0],'ga_ust':ga[1],'esli_t':paired.statistic,'esli_p':paired.pvalue,'welch_t':welch.statistic,'welch_p':welch.pvalue,'pearson_r':r.statistic,'pearson_p':r.pvalue,'regresyon_sabit':lm.intercept,'regresyon_egim':lm.slope}
# Başlangıç puanı ve grup için ayarlı OLS modeli; katsayılar A referanslıdır.
X=np.column_stack([np.ones(len(d)), d['on'], (d.grup==2).astype(int)])
assert np.linalg.matrix_rank(X)==3
beta=np.linalg.lstsq(X,d.son,rcond=None)[0]
s.update(dict(zip(['ayarli_sabit','ayarli_on','ayarli_grup_B'],beta)))
table=pd.crosstab(d.grup,d.degisim>=7).reindex(index=[1,2],columns=[False,True],fill_value=0)
fisher=stats.fisher_exact(table.to_numpy(),alternative='two-sided')
s['fisher_p']=fisher.pvalue
out=pd.DataFrame(list(s.items()),columns=['olcut','deger'])
print(out.to_string(index=False))
out.to_csv('sonuclar-python.csv',index=False)
if args.check:
    ref=pd.read_csv('beklenen-sonuclar.csv')
    if list(ref.olcut)!=list(out.olcut): raise AssertionError('Sonuç etiketleri farklı.')
    np.testing.assert_allclose(out.deger,ref.deger,rtol=1e-8,atol=1e-10)
    print('KONTROL BAŞARILI')
