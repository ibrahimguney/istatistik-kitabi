"""Restore only manifest-proven line endings and missing SPS text copies."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from kontrol import PAKETLER, manifest_yollari


def restore(content, expected):
    normalized = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    candidates = [content, normalized, normalized.rstrip(b'\n'),
                  normalized.rstrip(b'\n') + b'\n']
    candidates += [candidate.replace(b'\n', b'\r\n') for candidate in candidates]
    for candidate in candidates:
        if hashlib.sha256(candidate).hexdigest() == expected:
            return candidate
    raise ValueError('Content difference is not explained by line endings')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    arguments = parser.parse_args()
    base = Path('companion/bolumler')
    changes = {}
    manifests = {}
    for code in PAKETLER:
        manifest = base/code/'MANIFEST.json'
        manifests[manifest] = manifest.read_bytes()
        document = json.loads(manifests[manifest])
        for name, (_, expected) in manifest_yollari(document['files']).items():
            path = base/code/name
            original = path.read_bytes() if path.exists() else None
            if original is None:
                if path.suffix != '.sps':
                    raise ValueError(f'Unsupported missing file: {path}')
                content = Path(str(path) + '.txt').read_bytes()
            else:
                content = original
            try:
                replacement = restore(content, expected)
            except ValueError as error:
                raise ValueError(f'{path}: {error}') from error
            if original != replacement:
                changes[path] = (original, replacement)
    if arguments.apply and changes:
        backup = Path('build/eslestirme-2026-09-13/kucuk-once.zip')
        backup.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(backup, 'x', zipfile.ZIP_DEFLATED) as archive:
            for path, (original, _) in changes.items():
                if original is not None:
                    archive.writestr(str(path), original)
            for path, content in manifests.items():
                archive.writestr(str(path), content)
        with zipfile.ZipFile(backup) as archive:
            assert archive.testzip() is None
            for path, (original, _) in changes.items():
                if original is not None:
                    assert archive.read(str(path)) == original
        for path, (_, replacement) in changes.items():
            path.write_bytes(replacement)
    for path, content in manifests.items():
        assert path.read_bytes() == content
    print(json.dumps({'apply': arguments.apply, 'changes': len(changes),
        'missing_sps': sum(original is None for original, _ in changes.values()),
        'line_endings': sum(original is not None for original, _ in changes.values()),
        'original_manifests_preserved': len(manifests)}, indent=2))


if __name__ == '__main__':
    main()