"""V1/V3/V4 eski manifestlerini koruyan sınırlı, açık onarım."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

MANIFESTS = {
    "v1-colt-park": "0a81782a5d45edb892bece535e708be3397cf2055df9ac619aa396579c758de0",
    "v3-eslesme": "3c92b6c57be1683899fa4bff781bac2ad228e4dafeebfc80cb2c25fcc96620d1",
    "v4-star98": "dd28f2334333bee8f117886ca17158d5326a85775324107f92711ed5dd4a2f85",
}
COUNTS = {"v1-colt-park": 12, "v3-eslesme": 14, "v4-star98": 9}
SOURCES = {
    "companion/vakalar/v1-colt-park/raw/s1-data.xlsx": "prism-uploads/S1 Data_2.xlsx",
    "companion/vakalar/v1-colt-park/raw/s1-methods.pdf": "prism-uploads/S1_2.pdf",
}
SHARED = {"companion/data/raw/star98_statsmodels.csv",
          "companion/data/clean/star98_districts.csv"}


def digest(content):
    return hashlib.sha256(content).hexdigest()


def regular_path(workspace, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Güvensiz yol: " + str(path))
    current = workspace
    for component in path.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError("Sembolik bağlantı onarılmaz: " + str(current))
    return current


def repair_plan(workspace=Path(".")):
    entries, repairs = [], []
    for folder, reference in MANIFESTS.items():
        root = Path("companion/vakalar") / folder
        manifest = regular_path(workspace, root / "manifest.csv").read_bytes()
        if digest(manifest.removesuffix(b"\n")) != reference:
            raise ValueError("Manifest referansı değişmiş: " + folder)
        rows = list(csv.DictReader(io.StringIO(manifest.decode("utf-8"))))
        if len(rows) != COUNTS[folder] or len({row["path"] for row in rows}) != len(rows):
            raise ValueError("Manifest envanteri geçersiz: " + folder)
        for row in rows:
            relative = Path(row["path"]) if row["path"].startswith("companion/") else root / row["path"]
            if not relative.is_relative_to(root) and str(relative) not in SHARED:
                raise ValueError("Paket dışı yol: " + str(relative))
            path = regular_path(workspace, relative)
            before = path.read_bytes() if path.is_file() else None
            action, source = "exact", None
            if before is not None and digest(before) == row["sha256"]:
                after = before
            elif before is not None and path.suffix in {".md", ".csv", ".py", ".json"} and digest(before + b"\n") == row["sha256"]:
                before.decode("utf-8")
                after, action = before + b"\n", "append_terminal_LF"
            elif before is None and str(relative) in SOURCES:
                source = SOURCES[str(relative)]
                after = regular_path(workspace, source).read_bytes()
                if digest(after) != row["sha256"]:
                    raise ValueError("Yükleme eski hashle eşleşmiyor: " + source)
                action = "restore_missing_source"
            else:
                raise ValueError("Kanıtlanmamış fark veya eksik dosya: " + str(relative))
            if "bytes" in row and len(after) != int(row["bytes"]):
                raise ValueError("Beklenen boyut eşleşmiyor: " + str(relative))
            entry = {"path": str(relative), "action": action, "source": source,
                     "before_sha256": digest(before) if before is not None else None,
                     "after_sha256": digest(after), "before_bytes": len(before) if before is not None else None,
                     "after_bytes": len(after)}
            entries.append(entry)
            if action != "exact":
                repairs.append((path, before, after, entry))
    return entries, repairs


def apply_repairs(workspace=Path(".")):
    entries, repairs = repair_plan(workspace)
    for path, before, after, entry in repairs:
        current = path.read_bytes() if path.is_file() else None
        if current != before:
            raise ValueError("Ön kontrolden sonra dosya değişmiş: " + str(path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(after)
        if digest(path.read_bytes()) != entry["after_sha256"]:
            raise ValueError("Yazım sonrası hash eşleşmedi: " + str(path))
    _, remaining = repair_plan(workspace)
    if remaining:
        raise AssertionError("Onarım sonrası eksik işlem var")
    return entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Doğrulanan onarımları açıkça uygula")
    arguments = parser.parse_args()
    try:
        entries = apply_repairs() if arguments.apply else repair_plan()[0]
        result = {"mode": "apply" if arguments.apply else "plan", "manifest_entries": len(entries),
                  "changes": [entry for entry in entries if entry["action"] != "exact"],
                  "manifest_references": MANIFESTS, "pass": True,
                  "scope": "File restoration only; numerical and source clearance checks are separate"}
    except (ValueError, OSError, AssertionError) as error:
        result = {"pass": False, "error": str(error)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)