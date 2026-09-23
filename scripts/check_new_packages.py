"""Run independent numerical checks and exercise each new package's CLI.
Requires numpy, pandas and scipy. Does not claim R or SPSS runtime validation.
"""
from pathlib import Path
import subprocess, sys, tempfile, shutil, math
import numpy as np
import pandas as pd
from scipy import stats
ROOT=Path(__file__).resolve().parents[1]
SLUGS=['eksik-veri','nonparametrik','guvenirlik','laboratuvar']
def close(a,b): np.testing.assert_allclose(a,b,rtol=1e-8,atol=1e-10)
def ref(slug):
    x=pd.read_csv(ROOT/'companion/bolumler'/slug/'ornek-01/beklenen-sonuclar.csv')
    return dict(zip(x.olcut,x.deger))
# Known hand-checkable sums and means from the printed examples.
s=ref('eksik-veri');close(s['n'],12);close(s['eksik_son'],1);close(s['ortalama_1'],364/6);close(s['ortalama_2'],293/5)
# Pairwise win counting is independent of SciPy's rank implementation.
p=ROOT/'companion/bolumler/nonparametrik/ornek-01';d=pd.read_csv(p/'veri.csv');a=d.loc[d.grup==1,'puan'].to_numpy();b=d.loc[d.grup==2,'puan'].to_numpy()
u=sum(float(x>y)+.5*float(x==y) for x in a for y in b);s=ref('nonparametrik');close(u,s['U_1'])
_,ties=np.unique(np.r_[a,b],return_counts=True);N=len(a)+len(b)
variance=len(a)*len(b)/12*(N+1-sum(ties**3-ties)/(N*(N-1)))
close(2*stats.norm.sf(abs((u-len(a)*len(b)/2)/math.sqrt(variance))),s['p_asimptotik'])
close(s['isaret_p_kesin'],2*(math.comb(12,0)+math.comb(12,1))/2**12)
f=pd.read_csv(p/'esli.csv').fark.to_numpy();ranks=stats.rankdata(abs(f));pos=ranks[f>0].sum();_,t=np.unique(abs(f),return_counts=True)
v=(12*13*25-sum(t**3-t)/2)/24
close(min(pos,78-pos),s['wilcoxon_W_min']);close(2*stats.norm.sf(abs((pos-39)/math.sqrt(v))),s['wilcoxon_p_asimptotik'])
d=pd.read_csv(p/'uc-grup.csv');ranks=stats.rankdata(d.puan);H=12/(30*31)*sum(ranks[d.grup==g].sum()**2/10 for g in [1,2,3])-3*31
_,t=np.unique(d.puan,return_counts=True);H/=1-sum(t**3-t)/(30**3-30);close(H,s['kruskal_H'])
# Alpha computed from the covariance matrix, plus printed book benchmark.
d=pd.read_csv(ROOT/'companion/bolumler/guvenirlik/ornek-01/veri.csv');d.M4=6-d.M4
cov=np.cov(d.to_numpy(),rowvar=False,ddof=1);alpha=5/4*(1-np.trace(cov)/cov.sum());close(alpha,ref('guvenirlik')['alpha']);assert round(alpha,6)==.963643
# Independent direct formulas for paired t and simple regression.
d=pd.read_csv(ROOT/'companion/bolumler/laboratuvar/ornek-01/veri.csv');s=ref('laboratuvar');delta=(d.son-d['on']).to_numpy()
close(sum(d.son)/16,59.5);close(np.mean(delta)/(np.std(delta,ddof=1)/4),s['esli_t'])
slope=np.dot(d.saat-d.saat.mean(),d.son-d.son.mean())/np.dot(d.saat-d.saat.mean(),d.saat-d.saat.mean());close(slope,s['regresyon_egim'])
for slug in SLUGS:
    source=ROOT/'companion/bolumler'/slug/'ornek-01'
    with tempfile.TemporaryDirectory() as temp:
        work=Path(temp)/'example';shutil.copytree(source,work)
        subprocess.run([sys.executable,'cozum.py','--check'],cwd=work,check=True,capture_output=True)
        # Wrong schema must fail before analysis, including without --check.
        data=pd.read_csv(work/'veri.csv');data=data.rename(columns={data.columns[0]:'unexpected'});data.to_csv(work/'veri.csv',index=False)
        result=subprocess.run([sys.executable,'cozum.py'],cwd=work,capture_output=True)
        assert result.returncode!=0,slug
    print(slug+': numerical checks and invalid-input rejection PASS')
print('Python checks passed; R/SPSS require separate runtime validation.')
