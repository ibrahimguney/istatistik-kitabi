"""Package chapter 1 without changing the book or claiming SPSS/R execution.

Run from the project root: python companion/spss/build_b01_pilot.py
Generated files are under companion/spss/pilot-b01 and in the adjacent ZIP.
"""
from pathlib import Path
import hashlib
import base64
import json
import re
import textwrap
import zipfile

import pandas as pd
import build_package as source
from chapter_code import chapter_code, archive_manifest


def main():
    root = source.ROOT
    target = source.OUT / 'pilot-b01'
    csv_path = source.OUT / 'csv/b01.csv'
    frame = pd.read_csv(csv_path)
    raw = pd.read_csv(source.OUT / 'student-mat.csv', sep=';')
    pd.testing.assert_frame_equal(frame, source.clean(raw))
    assert frame.shape == (395, 10) and not frame.isna().any().any()

    def block(style):
        return chapter_code(root, 1, style)

    contents = {
        'README.md': (source.OUT / 'PILOT-B01-WINDOWS.md').read_bytes(),
        'companion/spss/csv/b01.csv': csv_path.read_bytes(),
        'companion/spss/syntax/open-b01.sps': source.opening(1, frame).encode(),
        'companion/spss/syntax/open-b01-excel.sps': source.opening(1, frame, excel=True).encode(),
        'companion/spss/syntax/b01.sps': block('prismSPSS').encode(),
        'companion/spss/sav/README.txt': b'SAV is created by SPSS; no SPSS output is supplied.\n',
        'b01.R': block('prismR').encode(),
        'b01.py': (block('prismPythonApp') +
                   '\nimport sys, scipy\n'
                   'print("Python:", sys.version)\n'
                   'print("pandas:", pd.__version__)\n'
                   'print("numpy:", np.__version__)\n'
                   'print("scipy:", scipy.__version__)\n').encode(),
    }
    for name, data in contents.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    excel_name = 'companion/spss/excel/b01.xlsx'
    excel = target / excel_name
    excel.parent.mkdir(parents=True, exist_ok=True)
    source.xlsx(excel, frame, 'Student Performance: student-mat.csv; UCI')
    contents[excel_name] = excel.read_bytes()
    manifest = {name: hashlib.sha256(data).hexdigest()
                for name, data in contents.items()}
    contents['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    archive_manifest(target / 'manifest.json')
    (target / 'manifest.json').write_bytes(contents['manifest.json'])
    archive = source.OUT / 'b01-windows-spss29-csv.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in contents.items():
            entry = zipfile.ZipInfo(name, date_time=(2026,9,13,0,0,0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, data)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name, digest in manifest.items():
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
    installer = root / 'B01-PAKET-OLUSTUR.py.txt'
    template = installer.read_text(encoding='utf-8')
    payload = archive.read_bytes()
    encoded = '\n'.join(textwrap.wrap(base64.b64encode(payload).decode('ascii'), 76))
    template, count = re.subn(
        r'PAYLOAD = """.*?"""',
        lambda match: 'PAYLOAD = """\n' + encoded + '\n"""',
        template, count=1, flags=re.S)
    assert count == 1
    template, count = re.subn(
        r"EXPECTED_SHA256 = '[0-9a-f]{64}'",
        lambda match: f"EXPECTED_SHA256 = '{hashlib.sha256(payload).hexdigest()}'",
        template, count=1)
    assert count == 1
    template = template.replace('b01-windows-spss29.zip', archive.name)
    installer.write_text(template, encoding='utf-8')
    print(f'Created {archive.relative_to(root)}: {len(contents)} files')


if __name__ == '__main__':
    main()