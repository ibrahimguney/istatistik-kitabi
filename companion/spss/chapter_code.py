from pathlib import Path
import hashlib
import re


def chapter_code(root, number, style):
    path = root / 'chapters/spss' / f'b{number:02d}.tex'
    blocks = re.findall(r'\\begin\{lstlisting\}\[style=' + re.escape(style)
                        + r'\]\s*\n(.*?)\\end\{lstlisting\}', path.read_text(), re.S)
    if not blocks:
        raise ValueError(f'No {style} blocks: {path}')
    if style == 'prismR':
        blocks = [block for block in blocks if not re.fullmatch(
            r'\s*\w+\s*<-\s*read\.csv\(file\.choose\(\)\)\s*', block)]
    return '\n\n'.join(block.strip() for block in blocks) + '\n'


def archive_manifest(path):
    if path.is_file():
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        target = path.parent / 'manifest-history' / (digest + path.suffix)
        target.parent.mkdir(exist_ok=True)
        if target.exists() and target.read_bytes() != content:
            raise ValueError(f'Conflicting manifest archive: {target}')
        if not target.exists():
            target.write_bytes(content)


def package_files(out):
    paths = [out / 'chapter-map.csv', out / 'results/checks.json',
             out / 'results/values.tex']
    paths += list((out / 'raw').glob('*'))
    for number in range(1, 15):
        code = f'b{number:02d}'
        paths += [out / 'csv' / f'{code}.csv', out / 'excel' / f'{code}.xlsx',
                  out / 'syntax' / f'{code}.sps', out / 'syntax' / f'open-{code}.sps',
                  out / 'r' / f'{code}.R', out / 'python' / f'{code}.py']
    paths += [out / 'syntax/open-b01-excel.sps']
    paths += [out / name for name in ['build_package.py', 'validate_package.py',
              'chapter_code.py', 'build_b01_pilot.py']]
    return sorted(paths)