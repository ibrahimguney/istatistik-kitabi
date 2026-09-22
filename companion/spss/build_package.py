"""Build the IMO301 literature-data/SPSS package from uploaded Student Performance CSV or ZIP files.

Uses only the standard library, numpy, pandas and scipy. No SPSS execution is
claimed. Generated workbooks and calculations require validation with the real data.
Run from the project root: python companion/spss/build_package.py
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import math
import platform
import zipfile
from xml.sax.saxutils import escape
import numpy as np
import pandas as pd
import scipy
from scipy import stats
from chapter_code import chapter_code, archive_manifest, package_files

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'companion/spss'
SEED = 2026
REPEATS = 2000

# Variable names are ASCII for SPSS portability; original categorical codes are
# explicitly mapped, never inferred from alphabetical order.
DICT = {
 'id': ('Dosya içi sıra numarası; özgün öğrenci kimliği değildir', '1..N; mat ve por arasında eşleştirme anahtarı DEĞİL', 'nominal'),
 'school': ('Okul', '1=GP; 2=MS', 'nominal'),
 'sex': ('Kaynak dosyasındaki cinsiyet kodu', '1=F; 2=M', 'nominal'),
 'age': ('Yaş', 'Tamamlanmış yıl', 'scale'),
 'studytime': ('Haftalık çalışma süresi kategorisi; saat sayısı değildir', '1:<2; 2:2-5; 3:5-10; 4:>10 saat (kaynak kategorileri)', 'ordinal'),
 'absences': ('Devamsızlık sayısı', 'Kaynakta sayım; gün veya saat olduğu varsayılmadı', 'scale'),
 'g1': ('Birinci dönem notu', '0..20; sıfır eksik kodu değildir', 'scale'),
 'g2': ('İkinci dönem notu', '0..20; sıfır eksik kodu değildir', 'scale'),
 'g3': ('Yıl sonu notu', '0..20; sıfır eksik kodu değildir', 'scale'),
 'pass10': ('Eğitim amaçlı türetilmiş eşik göstergesi', '1:g3>=10; 0:g3<10; kurum kararı yerine kullanılmaz', 'nominal'),
 'srs40': ('Sonlu dosyadan geri koymadan seçilen 40 kayıt', '1=seçilen; 0=seçilmeyen; numpy PCG64 tohum 2026', 'nominal'),
 'strat40': ('Okula göre tabakalı seçilmiş 40 kayıt', 'GP:35; MS:5; 1=seçilen; 0=seçilmeyen', 'nominal'),
 'strw': ('Örnekleme öğretimi için tabaka ağırlığı', 'GP:349/35; MS:46/5; yalnız seçilmiş 40 kayıtta kullanılır', 'scale'),
 'rep': ('Benzetim tekrar numarası; öğrenci değildir', '1..2000', 'nominal'),
 'ort5': ('n=5 örneklem ortalaması', 'Matematik g3 ampirik dağılımından geri koyarak çekim', 'scale'),
 'ort30': ('n=30 örneklem ortalaması', 'Matematik g3 ampirik dağılımından geri koyarak çekim', 'scale'),
 'ort100': ('n=100 örneklem ortalaması', 'Matematik g3 ampirik dağılımından geri koyarak çekim', 'scale'),
 'z5': ('Standartlaştırılmış n=5 ortalaması', '(ort5-ampirik ortalama)/(ampirik sigma/sqrt(5))', 'scale'),
 'z30': ('Standartlaştırılmış n=30 ortalaması', '(ort30-ampirik ortalama)/(ampirik sigma/sqrt(30))', 'scale'),
 'z100': ('Standartlaştırılmış n=100 ortalaması', '(ort100-ampirik ortalama)/(ampirik sigma/sqrt(100))', 'scale'),
}

SOURCE_NAMES = ('student-mat.csv', 'student-por.csv', 'student.txt', 'student-merge.R')


def read_archive(data, origin, depth=0):
    """Read named members without extracting paths onto the filesystem."""
    if depth > 3:
        raise ValueError('ZIP nesting exceeds 3.')
    found = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for item in z.infolist():
            name = Path(item.filename).name.lower()
            if name not in SOURCE_NAMES and not name.endswith('.zip'):
                continue
            if item.file_size > 20_000_000:
                raise ValueError('Source member exceeds 20 MB: ' + item.filename)
            raw = z.read(item)
            location = origin + '!' + item.filename
            incoming = {name: (raw, location)} if name in SOURCE_NAMES else read_archive(raw, location, depth+1)
            for key, value in incoming.items():
                if key in found and found[key][0] != value[0]:
                    raise ValueError('Conflicting source copies: ' + key)
                found[key] = value
    return found


def load_sources():
    """Find loose CSVs or ZIP files at the announced upload locations."""
    folders = [OUT, ROOT / 'student', ROOT]
    found = {}
    for folder in folders:
        if not folder.exists():
            continue
        for name in SOURCE_NAMES:
            candidates = [folder / name]
            if folder != ROOT:
                candidates += sorted(folder.rglob(name))
            for path in candidates:
                if path.is_file() and name not in found:
                    found[name] = (path.read_bytes(), path.relative_to(ROOT).as_posix())
        if 'student-mat.csv' in found:
            return found
    for folder in folders:
        if not folder.exists():
            continue
        candidates = sorted(folder.glob('*.zip') if folder == ROOT else folder.rglob('*.zip'))
        for path in candidates:
            payload = read_archive(path.read_bytes(), path.relative_to(ROOT).as_posix())
            if 'student-mat.csv' in payload:
                found.update(payload)
                return found
    raise FileNotFoundError(
        'Veri bulunamadi: companion/spss klasorune student-mat.csv veya '
        'onu iceren student.zip yukleyin. student-por.csv istege baglidir.')


def clean(d):
    result = pd.DataFrame({'id': np.arange(1, len(d)+1),
                           'school': d.school.map({'GP':1, 'MS':2}),
                           'sex':d.sex.map({'F':1,'M':2})})
    for c in ['age','studytime','absences','G1','G2','G3']:
        result[c.lower()] = d[c]
    result['pass10'] = (d.G3 >= 10).astype(int)
    assert not result.isna().any().any()
    return result


def colname(n):
    s=''
    while n:
        n, r = divmod(n-1,26); s=chr(65+r)+s
    return s


def worksheet(rows):
    data=[]
    for r,row in enumerate(rows,1):
        cells=[]
        for c,v in enumerate(row,1):
            ref=f'{colname(c)}{r}'
            if isinstance(v,(int,float,np.integer,np.floating)):
                assert math.isfinite(v)
                cells.append(f'<c r="{ref}"><v>{v}</v></c>')
            else:
                cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(v))}</t></is></c>')
        data.append(f'<row r="{r}">'+''.join(cells)+'</row>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
      '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
      '<sheetData>'+''.join(data)+'</sheetData></worksheet>')


def xlsx(path, frame, origin):
    sheets=[('veri',[list(frame.columns)]+frame.values.tolist()),
      ('sozluk',[['degisken','anlam','kod_birim','olcme_duzeyi']]+
       [[c,*DICT[c]] for c in frame.columns]),
      ('kaynak', [['alan','deger'], ['kaynak',origin],
       ['atif','Cortez (2008), Student Performance, UCI, doi:10.24432/C5TG7T'],
       ['lisans','CC BY 4.0; https://creativecommons.org/licenses/by/4.0/'],
       ['donusum','Analiz icin secili degiskenler, acik kodlama ve turetim; build_package.py'],
       ['uyari','mat/por bagimsiz iki grup degildir; id kaynak kimligi degildir'],
       ['dogrulama','Beklenen sonuclar Python ile; IBM SPSS burada calistirilmadi']])]
    ns='http://schemas.openxmlformats.org/package/2006/relationships'
    rel='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    parts={
      '_rels/.rels':f'<Relationships xmlns="{ns}"><Relationship Id="rId1" Type="{rel}/officeDocument" Target="xl/workbook.xml"/></Relationships>',
      'xl/workbook.xml':'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="'+rel+'"><sheets>'+''.join(f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>' for i,(name,_) in enumerate(sheets,1))+'</sheets></workbook>',
      'xl/_rels/workbook.xml.rels':f'<Relationships xmlns="{ns}">'+''.join(f'<Relationship Id="rId{i}" Type="{rel}/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,4))+'</Relationships>',
      '[Content_Types].xml':'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'+''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1,4))+'</Types>'}
    for i,(_,rows) in enumerate(sheets,1): parts[f'xl/worksheets/sheet{i}.xml']=worksheet(rows)
    with zipfile.ZipFile(path,'w') as z:
        for name,text in parts.items():
            info=zipfile.ZipInfo(name,date_time=(2026,9,9,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,text.encode('utf-8'))


def opening(number,frame,excel=False):
    if excel or number == 8:
        text=f"""GET DATA /TYPE=XLSX
 /FILE='companion/spss/excel/b{number:02d}.xlsx'
 /SHEET=NAME 'veri' /CELLRANGE=FULL /READNAMES=ON.
"""
    else:
        formats = ' '.join(f'{column} ' + ('F8.0' if pd.api.types.is_integer_dtype(frame[column])
                                         else 'F24.16') for column in frame.columns)
        text=f"""SET DECIMAL=DOT.
GET DATA /TYPE=TXT
 /FILE='companion/spss/csv/b{number:02d}.csv'
 /ENCODING='UTF8'
 /ARRANGEMENT=DELIMITED /DELCASE=LINE
 /DELIMITERS="," /QUALIFIER='"'
 /FIRSTCASE=2
 /VARIABLES={formats}.
"""
    text+="""FILTER OFF.
WEIGHT OFF.
SPLIT FILE OFF.
"""
    for c in frame.columns:
        # ASCII labels in syntax; full Turkish definitions in workbook dictionary.
        label=DICT[c][0].translate(str.maketrans('çğıöşüÇĞİÖŞÜ','cgiosuCGIOSU')).replace("'",'')
        text+=f"VARIABLE LABELS {c} '{label}'.\nVARIABLE LEVEL {c} ({DICT[c][2].upper()}).\n"
    if 'g3' in frame:
        text+="""VALUE LABELS school 1 'GP' 2 'MS'
 /sex 1 'F' 2 'M'
 /studytime 1 '<2 saat' 2 '2-5 saat' 3 '5-10 saat' 4 '>10 saat'
 /pass10 0 'G3<10' 1 'G3>=10'.
FORMATS id school sex age studytime absences g1 g2 g3 pass10 (F8.0).
"""
    text+=f"EXECUTE.\nSAVE OUTFILE='companion/spss/sav/b{number:02d}.sav'.\n"
    return text


def main():
    sources = load_sources()
    frames = {}
    for name, n in [('mat', 395), ('por', 649)]:
        key = f'student-{name}.csv'
        if key not in sources:
            continue
        source = pd.read_csv(io.BytesIO(sources[key][0]), sep=';')
        if source.shape != (n, 33) or source.isna().any().any():
            raise ValueError(f'{key}: expected {n} complete rows and 33 columns; got {source.shape}.')
        frames[name] = clean(source)
    for d in ['raw','excel','csv','syntax','sav','results','r','python']:
        (OUT/d).mkdir(parents=True,exist_ok=True)
    for name, (raw, _) in sources.items():
        path = OUT/'raw'/name
        if path.exists():
            if path.read_bytes().replace(b'\r\n', b'\n').rstrip(b'\n') != raw.replace(b'\r\n', b'\n').rstrip(b'\n'):
                raise ValueError(f'Existing raw data differs: {path}')
            sources[name] = (path.read_bytes(), sources[name][1])
        else:
            path.write_bytes(raw)
    context_name = 'mat'  # Course applications consistently use the uploaded mathematics data.
    m, p = frames['mat'], frames[context_name]
    y = m.g3.to_numpy(dtype=float)
    rng=np.random.default_rng(SEED)
    draws=rng.choice(y,size=(REPEATS,100),replace=True)
    sim=pd.DataFrame({'rep':np.arange(1,REPEATS+1)})
    for n in [5,30,100]:
        sim[f'ort{n}']=draws[:,:n].mean(axis=1)
        sim[f'z{n}']=(sim[f'ort{n}']-y.mean())/(y.std(ddof=0)/math.sqrt(n))
    design=m.copy(); design['srs40']=0;design['strat40']=0
    rng=np.random.default_rng(SEED);design.loc[rng.choice(len(m),40,replace=False),'srs40']=1
    for school,n in [(1,35),(2,5)]:
        ix=design.index[design.school==school].to_numpy()
        design.loc[rng.choice(ix,n,replace=False),'strat40']=1
    design['strw']=np.where(design.school==1,349/35,46/5)
    mapping=[]
    for i in range(1,15):
        name=context_name if i in [2,7] else 'mat'
        d=frames[name]
        origin=f'student-{name}.csv; gozlem verisi, {len(d)} kayit'
        if i==4:d=sim[['rep','ort5','ort30']];origin='student-mat.csv G3 ampirik dagilimindan 2000 benzetim; ogrenci kaydi DEGIL'
        if i==5:d=sim;origin='student-mat.csv G3 ampirik dagilimindan 2000 benzetim; ogrenci kaydi DEGIL'
        if i==6:d=design;origin+='; sonlu cerceve ogretim orneklemesi'
        xlsx(OUT/'excel'/f'b{i:02d}.xlsx',d,origin)
        csv_path = OUT/'csv'/f'b{i:02d}.csv'
        if csv_path.exists():
            pd.testing.assert_frame_equal(pd.read_csv(csv_path), d,
                check_dtype=False, atol=1e-12, rtol=1e-12)
        else:
            d.to_csv(csv_path,index=False)
        (OUT/'syntax'/f'open-b{i:02d}.sps').write_text(opening(i,d),encoding='utf-8')
        syntax=chapter_code(ROOT,i,'prismSPSS')
        (OUT/'syntax'/f'b{i:02d}.sps').write_text(syntax,encoding='utf-8')
        (OUT/'r'/f'b{i:02d}.R').write_text(chapter_code(ROOT,i,'prismR'),encoding='utf-8')
        (OUT/'python'/f'b{i:02d}.py').write_text(chapter_code(ROOT,i,'prismPythonApp'),encoding='utf-8')
        mapping.append({'uygulama':f'b{i:02d}','kaynak':origin,'kayit':len(d),'degisken':len(d.columns)})
    mapping_path = OUT/'chapter-map.csv'
    if mapping_path.exists():
        pd.testing.assert_frame_equal(pd.read_csv(mapping_path), pd.DataFrame(mapping))
    else:
        pd.DataFrame(mapping).to_csv(mapping_path,index=False)
    (OUT/'syntax/open-b01-excel.sps').write_text(opening(1,m,excel=True),encoding='utf-8')
    V={}; tables={}
    def put(key,value,places=3):
        V[key]={'value':float(value),'places':places}
    def summary(prefix,d):
        g=d.g3; n=len(g); ci=stats.t.interval(.95,n-1,loc=g.mean(),scale=stats.sem(g))
        for key,val,places in [('N',n,0),('Mean',g.mean(),3),('SD',g.std(),3),('SE',stats.sem(g),3),('Var',g.var(),3),('Median',g.median(),1),('Zero',(g==0).sum(),0),('Pass',d.pass10.sum(),0),('PHat',d.pass10.mean(),4),('CILow',ci[0],3),('CIHigh',ci[1],3)]:put(prefix+key,val,places)
    summary('Mat',m);summary('Context',p)
    put('ContextPSE',math.sqrt(p.pass10.mean()*(1-p.pass10.mean())/len(p)),4)
    for key,val in [('AbsMean',m.absences.mean()),('AbsSD',m.absences.std()),('AbsMax',m.absences.max())]:put(key,val)
    for title,n in [('Five',5),('Thirty',30),('Hundred',100)]:
        put('Sim'+title+'Mean',sim[f'ort{n}'].mean());put('Sim'+title+'SD',sim[f'ort{n}'].std());put('Theory'+title+'SE',y.std(ddof=0)/math.sqrt(n))
    put('EmpSigma',y.std(ddof=0));put('SimZMean',sim.z100.mean());put('SimZSD',sim.z100.std());put('SimCoverage',100*(sim.z100.abs()<=1.96).mean(),2)
    sr=design[design.srs40==1];st=design[design.strat40==1]
    put('SrsMean',sr.g3.mean());put('SrsSD',sr.g3.std());put('StratMean',np.average(st.g3,weights=st.strw))
    ph=m.pass10.mean();n=len(m);zz=stats.norm.ppf(.975);den=1+zz**2/n
    center=(ph+zz**2/(2*n))/den;half=zz*math.sqrt(ph*(1-ph)/n+zz**2/(4*n**2))/den
    put('WilsonLow',center-half,4);put('WilsonHigh',center+half,4)
    tt=stats.ttest_1samp(m.g3,10);put('MatT',tt.statistic);put('MatP',tt.pvalue,4);put('MatD',(m.g3.mean()-10)/m.g3.std(),4)
    # Prospective power under normal IID observations; 1 point is an illustrative,
    # prespecified target, not the observed effect.
    def power(n):
        crit=stats.t.ppf(.975,n-1);nc=math.sqrt(n)/m.g3.std()
        return stats.nct.sf(crit,n-1,nc)+stats.nct.cdf(-crit,n-1,nc)
    plan=next(n for n in range(2,10000) if power(n)>=.80)
    put('PlanN',plan,0);put('PlanPower',power(plan),4)
    a=m.loc[m.sex==1,'g3'];b=m.loc[m.sex==2,'g3'];welch=stats.ttest_ind(a,b,equal_var=False)
    ci=welch.confidence_interval()
    for key,value in [('FemaleN',len(a)),('MaleN',len(b)),('FemaleMean',a.mean()),('MaleMean',b.mean()),('WelchT',welch.statistic),('WelchDF',welch.df),('WelchP',welch.pvalue),('WelchDiff',a.mean()-b.mean()),('WelchLow',ci.low),('WelchHigh',ci.high)]:put(key,value,4 if key=='WelchP' else 3)
    pair=stats.ttest_rel(m.g3,m.g1);ci=pair.confidence_interval()
    for key,value in [('PairDiff',(m.g3-m.g1).mean()),('PairT',pair.statistic),('PairP',pair.pvalue),('PairLow',ci.low),('PairHigh',ci.high),('PairDZ',(m.g3-m.g1).mean()/(m.g3-m.g1).std())]:put(key,value,5 if key=='PairP' else 3)
    c=pd.crosstab(m.sex,m.pass10);chi=stats.chi2_contingency(c,correction=False)
    put('Chi',chi.statistic);put('ChiP',chi.pvalue,4);put('CramerV',math.sqrt(chi.statistic/len(m)));put('MinExpected',chi.expected_freq.min());put('FemalePassPct',100*c.loc[1,1]/len(a),2);put('MalePassPct',100*c.loc[2,1]/len(b),2)
    fit=stats.linregress(m.g1,m.g3);crit=stats.t.ppf(.975,len(m)-2)
    for key,value in [('RegR',fit.rvalue),('RegRSq',fit.rvalue**2),('RegSlope',fit.slope),('RegIntercept',fit.intercept),('RegSlopeLow',fit.slope-crit*fit.stderr),('RegSlopeHigh',fit.slope+crit*fit.stderr),('RegAtTen',fit.intercept+10*fit.slope)]:put(key,value)
    positive=m[m.g3>0];put('PositiveN',len(positive),0);put('PositiveMean',positive.g3.mean());put('PositiveSD',positive.g3.std())
    macros=['% Generated by companion/spss/build_package.py; independent reference values.']
    for key,d in V.items():
        value=f"{d['value']:.{d['places']}f}".replace('.','{,}')
        macros.append('\\newcommand{\\SP'+key+'}{\\ensuremath{'+value+'}}')
    (OUT/'results'/'values.tex').write_text('\n'.join(macros)+'\n',encoding='utf-8')
    result={'warning':'Independent Python calculations, not IBM SPSS output.','seed':SEED,'replicates':REPEATS,'values':V,'crosstab':c.values.tolist(),'expected':chi.expected_freq.tolist(),'sampling_ids':{'srs':sr.id.tolist(),'stratified':st.id.tolist()},'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__},'context_dataset':context_name,'sources':{name:{'origin':origin,'sha256':hashlib.sha256(raw).hexdigest()} for name,(raw,origin) in sources.items()}}
    (OUT/'results'/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest=[]
    for f in package_files(OUT):
        manifest.append([f.relative_to(OUT).as_posix(),hashlib.sha256(f.read_bytes()).hexdigest()])
    archive_manifest(OUT/'manifest.csv')
    with (OUT/'manifest.csv').open('w',newline='',encoding='utf-8') as fh:
        w=csv.writer(fh);w.writerow(['file','sha256']);w.writerows(manifest)
    print('Built 14 XLSX, 14 analysis SPS + 14 data-opening SPS; SPSS not executed.')
    print('Prospective power minimum n:',plan)

if __name__=='__main__': main()