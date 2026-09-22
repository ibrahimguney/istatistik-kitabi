"""Read-only checks: XLSX round trip, raw-data computations and package links.
Does NOT execute SPSS or claim Excel/SPSS application compatibility.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from scipy import stats
from chapter_code import chapter_code, package_files
from build_package import opening, clean

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'companion/spss'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def check():
    source = pd.read_csv(OUT / 'raw/student-mat.csv', sep=';')
    assert source.shape == (395, 33)
    assert not source.isna().any().any()
    assert source.school.value_counts().to_dict() == {'GP': 349, 'MS': 46}
    assert source.sex.value_counts().to_dict() == {'F': 208, 'M': 187}
    for col in ['G1', 'G2', 'G3']:
        assert source[col].between(0, 20).all()
    assert (source.G3 == 0).sum() == 38
    result = json.loads((OUT / 'results/checks.json').read_text())
    values = {key: item['value'] for key, item in result['values'].items()}
    y = source.G3.to_numpy(dtype=float)
    mean, sd = np.mean(y), np.sqrt(np.sum((y-y.mean())**2)/(len(y)-1))
    se = sd/np.sqrt(len(y))
    t = (mean-10)/se
    independent = {'MatMean': mean, 'MatSD': sd, 'MatSE': se,
                   'MatT': t, 'MatP': 2*stats.t.sf(abs(t),len(y)-1),
                   'MatPHat': np.mean(y>=10)}
    for key, val in independent.items():
        assert np.isclose(values[key], val, rtol=1e-12, atol=1e-12), key
    X = np.column_stack([np.ones(len(y)), source.G1])
    intercept, slope = np.linalg.lstsq(X, y, rcond=None)[0]
    assert np.isclose(values['RegSlope'], slope)
    assert np.isclose(values['RegIntercept'], intercept)
    obs = np.array([[75, 133], [55, 132]])
    expected = obs.sum(1)[:,None]*obs.sum(0)[None,:]/obs.sum()
    assert np.isclose(values['Chi'],np.sum((obs-expected)**2/expected))
    assert np.array_equal(result['crosstab'], obs)
    assert len(result['sampling_ids']['srs']) == 40
    assert len(set(result['sampling_ids']['srs'])) == 40
    assert len(set(result['sampling_ids']['stratified'])) == 40
    for name, info in result['sources'].items():
        assert hashlib.sha256((OUT/'raw'/name).read_bytes()).hexdigest() == info['sha256']
    for i in range(1,15):
        code=f'b{i:02d}'
        csv = pd.read_csv(OUT/'csv'/f'{code}.csv')
        with zipfile.ZipFile(OUT/'excel'/f'{code}.xlsx') as z:
            assert z.testzip() is None
            for name in z.namelist():
                if name.endswith('.xml') or name.endswith('.rels'): ET.fromstring(z.read(name))
            book = ET.fromstring(z.read('xl/workbook.xml'))
            assert [s.attrib['name'] for s in book.find('s:sheets',NS)] == ['veri','sozluk','kaynak']
            root = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
            rows=[]
            for row in root.findall('s:sheetData/s:row',NS):
                vals=[]
                for cell in row.findall('s:c',NS):
                    if cell.attrib.get('t') == 'inlineStr': vals.append(cell.find('s:is/s:t',NS).text)
                    else: vals.append(float(cell.find('s:v',NS).text))
                rows.append(vals)
            assert rows[0] == list(csv.columns), code
            assert len(rows)-1 == len(csv), code
            assert np.allclose(np.asarray(rows[1:]),csv.to_numpy(),rtol=1e-12,atol=1e-12),code
        if i not in [4,5]:
            assert len(csv) == 395 and np.array_equal(csv.g3, source.G3)
            assert np.array_equal(csv.pass10,(source.G3>=10).astype(int))
        else: assert len(csv)==2000 and 'rep' in csv
        sps=(OUT/'syntax'/f'{code}.sps').read_text()
        opening=(OUT/'syntax'/f'open-{code}.sps').read_text()
        assert sps == chapter_code(ROOT,i,'prismSPSS'), code
        assert (OUT/'r'/f'{code}.R').read_text() == chapter_code(ROOT,i,'prismR'), code
        assert (OUT/'python'/f'{code}.py').read_text() == chapter_code(ROOT,i,'prismPythonApp'), code
        assert opening == expected_opening(i,csv), code
        assert f"SAVE OUTFILE='companion/spss/sav/{code}.sav'." in opening
        for flag in ['FILTER OFF.','WEIGHT OFF.','SPLIT FILE OFF.']: assert flag in opening
        for referenced in re.findall(r"(?:INSERT FILE|GET FILE|/FILE)='([^']+)'", sps + opening):
            if referenced.endswith('.sav'):
                assert f"SAVE OUTFILE='{referenced}'." in (OUT/'syntax/open-b01.sps').read_text(), referenced
            else:
                assert (ROOT/referenced).is_file(), referenced
        if 'REGRESSION' in sps:
            reg=sps[sps.index('REGRESSION'):]
            assert reg.index('/STATISTICS') < reg.index('/DEPENDENT') < reg.index('/METHOD')
        chapter = ROOT/'chapters/spss'/f'{code}.tex'
        assert chapter.exists()
        text = chapter.read_text()
        assert '\\lstinputlisting' not in text, code
    validate_csv_frames(source)
    assert (OUT/'syntax/open-b01-excel.sps').read_text() == expected_opening(1,clean(source),excel=True)
    definitions=set(re.findall(r'\\newcommand\{\\(SP[A-Za-z]+)\}',(OUT/'results/values.tex').read_text()))
    uses=set()
    for p in (ROOT/'chapters/spss').glob('b*.tex'):
        uses.update(re.findall(r'\\(SP[A-Za-z]+)',p.read_text()))
    assert uses <= definitions, uses-definitions
    manifest=pd.read_csv(OUT/'manifest.csv')
    assert manifest.file.is_unique
    assert set(manifest.file) == {path.relative_to(OUT).as_posix() for path in package_files(OUT)}
    for item in manifest.itertuples():
        assert hashlib.sha256((OUT/item.file).read_bytes()).hexdigest() == item.sha256,item.file
    print('PASS: 14 XLSX/CSV round trips, raw-data checks, numerical cross-checks,')
    validate_pilot()
    print('SPSS dependencies, all SPSS/R/Python chapter blocks, source/manifest hashes and B01 pilot.')
    print('IBM SPSS and Excel were not executed; runtime/import validation remains external.')

expected_opening = opening


def validate_csv_frames(source):
    frame = clean(source)
    scores = frame.g3.to_numpy(dtype=float)
    rng = np.random.default_rng(2026)
    draws = rng.choice(scores, size=(2000, 100), replace=True)
    simulation = pd.DataFrame({'rep': np.arange(1, 2001)})
    for size in [5, 30, 100]:
        simulation[f'ort{size}'] = draws[:, :size].mean(axis=1)
        simulation[f'z{size}'] = ((simulation[f'ort{size}'] - scores.mean())
                                 / (scores.std(ddof=0) / np.sqrt(size)))
    design = frame.copy()
    design['srs40'] = 0
    design['strat40'] = 0
    rng = np.random.default_rng(2026)
    design.loc[rng.choice(len(frame), 40, replace=False), 'srs40'] = 1
    for school, size in [(1, 35), (2, 5)]:
        indices = design.index[design.school == school].to_numpy()
        design.loc[rng.choice(indices, size, replace=False), 'strat40'] = 1
    design['strw'] = np.where(design.school == 1, 349 / 35, 46 / 5)
    for number in range(1, 15):
        expected = {4: simulation[['rep','ort5','ort30']], 5: simulation, 6: design}.get(number,frame)
        pd.testing.assert_frame_equal(pd.read_csv(OUT/'csv'/f'b{number:02d}.csv'), expected,
                                      check_dtype=False, atol=1e-12, rtol=1e-12)


def validate_pilot():
    pilot = OUT/'pilot-b01'
    manifest = json.loads((pilot/'manifest.json').read_text())
    for name, digest in manifest.items():
        relative = Path(name)
        assert not relative.is_absolute() and '..' not in relative.parts, name
        assert hashlib.sha256((pilot/relative).read_bytes()).hexdigest() == digest, name
    assert len(manifest) == 9
    assert (pilot/'companion/spss/syntax/b01.sps').read_text() == chapter_code(ROOT,1,'prismSPSS')
    for filename in ['open-b01.sps','open-b01-excel.sps']:
        assert (pilot/'companion/spss/syntax'/filename).read_bytes() == (OUT/'syntax'/filename).read_bytes()
    assert (pilot/'companion/spss/csv/b01.csv').read_bytes() == (OUT/'csv/b01.csv').read_bytes()
    assert (pilot/'b01.R').read_text() == chapter_code(ROOT,1,'prismR')
    assert (pilot/'b01.py').read_text().startswith(chapter_code(ROOT,1,'prismPythonApp'))


if __name__ == '__main__':
    check()