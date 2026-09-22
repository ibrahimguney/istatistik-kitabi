"""V1–V4 için salt okunur dosya, sonuç ve kitap bağlantısı denetimi."""

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


OUTPUT = Path("build/vakalar-ortak-kabul-2026-09-13")
CASES = {
    "V1": {"folder": "v1-colt-park", "count": 12,
           "command": "build/colt-park-2026-09-13/kontrol.py",
           "chapters": {"v1-colt-park": [5], "v1-colt-park-rastgelelestirme": []},
           "bindings": {"chapters/11-bagimsiz-eslestirilmis-t.tex": "v1-colt-park",
                        "chapters/09-bootstrap-rastgelelestirme.tex": "v1-colt-park-rastgelelestirme"}},
    "V2": {"folder": "v2-nhanes", "count": 11,
           "command": "companion/vakalar/v2-nhanes/verify_delivery.py",
           "chapters": {"v2-nhanes": [5, 5, 5], "v2-nhanes-sonuclar": []},
           "bindings": {"chapters/06-ornekleme.tex": "v2-nhanes",
                        "chapters/vakalar/v2-nhanes.tex": "v2-nhanes-sonuclar"}},
    "V3": {"folder": "v3-eslesme", "count": 14,
           "command": "companion/vakalar/v3-eslesme/verify.py",
           "chapters": {"v3-eslesme": [5, 5]},
           "bindings": {"chapters/11-bagimsiz-eslestirilmis-t.tex": "v3-eslesme"}},
    "V4": {"folder": "v4-star98", "count": 9,
           "command": "companion/vakalar/v4-star98/verify.py",
           "chapters": {"v4-star98": [5, 5]},
           "bindings": {"chapters/15-coklu-regresyon.tex": "v4-star98"}},
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_check(root, expected_count):
    manifest = root / "manifest.csv"
    if not manifest.exists():
        return {"pass": False, "reason": "manifest_missing", "entries": 0, "rows": []}
    with manifest.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    checked = []
    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            checked.append({"path": row["path"], "pass": False, "reason": "unsafe_path"})
            continue
        path = relative if row["path"].startswith("companion/") else root / relative
        item = {"path": str(path), "expected_sha256": row["sha256"], "exists": path.is_file()}
        if path.is_file():
            content = path.read_bytes()
            item.update(actual_sha256=digest(path), bytes=len(content))
            item["pass"] = item["actual_sha256"] == row["sha256"] and (
                "bytes" not in row or len(content) == int(row["bytes"]))
            if not item["pass"]:
                item["one_missing_terminal_LF"] = hashlib.sha256(content + b"\n").hexdigest() == row["sha256"]
        else:
            item["pass"] = False
        checked.append(item)
    valid = bool(rows) and (expected_count is None or len(rows) == expected_count)
    valid = valid and len({row["path"] for row in rows}) == len(rows)
    return {"pass": valid and all(row["pass"] for row in checked), "entries": len(rows), "rows": checked}


def chapter_check(case):
    errors, counts, files = [], {}, []
    for name, expected in case["chapters"].items():
        path = Path("chapters/vakalar") / (name + ".tex")
        files.append(str(path))
        if not path.is_file():
            errors.append("missing: " + str(path))
            continue
        text = path.read_text()
        counts[name] = [len(re.findall(r"\\item\b", part))
                        for part in re.findall(r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}", text, re.S)]
        if counts[name] != expected:
            errors.append("task_structure: " + name)
        for target in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text):
            if not Path(target).is_file():
                errors.append("missing_graphic: " + target)
        for target in re.findall(r"\\input\{([^}]+)\}", text):
            if not Path(target + ("" if target.endswith(".tex") else ".tex")).is_file():
                errors.append("missing_input: " + target)
    for parent, child in case["bindings"].items():
        path = Path(parent)
        if not path.exists() or "\\input{chapters/vakalar/" + child + "}" not in path.read_text():
            errors.append("missing_binding: " + parent + " -> " + child)
    return {"pass": not errors, "errors": errors, "enumerate_counts": counts, "files": files,
            "scope": "static inclusion, graphics and task structure; not a new PDF layout audit"}


def zip_check():
    path = Path("prism-uploads/DEMO_J.zip")
    if not path.exists():
        return {"exists": False}
    try:
        with zipfile.ZipFile(path) as archive:
            invalid = archive.testzip()
            raw = archive.read("DEMO_J.xpt")
        data = pd.read_sas(io.BytesIO(raw), format="xport")
        return {"exists": True, "zip_sha256": digest(path), "crc_pass": invalid is None,
                "xpt_bytes": len(raw), "xpt_sha256": hashlib.sha256(raw).hexdigest(),
                "shape": list(data.shape), "new_numeric_case_accepted": False,
                "scope": "readability only; does not restore missing V2 analysis or validate its variance"}
    except Exception as error:
        return {"exists": True, "error": type(error).__name__ + ": " + str(error)}


def protected_snapshot():
    paths = set()
    for case in CASES.values():
        root = Path("companion/vakalar") / case["folder"]
        paths.update(path for path in root.rglob("*") if path.is_file())
        paths.update(Path("chapters/vakalar") / (name + ".tex") for name in case["chapters"])
    paths.update(Path("companion/data").rglob("*.csv"))
    return {str(path): digest(path) for path in sorted(paths) if path.is_file()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    output = parser.parse_args().output_dir
    output.mkdir(parents=True, exist_ok=True)
    before = protected_snapshot()
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "cases": {},
              "source_clearance_automated": False, "learning_effect_verified": False}
    for name, case in CASES.items():
        root = Path("companion/vakalar") / case["folder"]
        manifest = manifest_check(root, case["count"])
        chapters = chapter_check(case)
        if not Path(case["command"]).exists():
            numeric = {"pass": False, "reason": "verifier_missing", "command": case["command"]}
        else:
            try:
                process = subprocess.run([sys.executable, "-B", case["command"]],
                                         capture_output=True, text=True, timeout=120)
                (output / (name.lower() + ".log")).write_text(process.stdout + process.stderr)
                numeric = {"pass": process.returncode == 0, "returncode": process.returncode,
                           "command": case["command"], "log": str(output / (name.lower() + ".log"))}
            except subprocess.TimeoutExpired:
                numeric = {"pass": False, "reason": "timeout", "command": case["command"]}
        result["cases"][name] = {"manifest": manifest, "numeric": numeric, "chapters": chapters,
                                 "technical_pass": manifest["pass"] and numeric["pass"] and chapters["pass"]}
    result["v2_upload"] = zip_check()
    result["protected_files_unchanged"] = before == protected_snapshot()
    result["protected_files"] = len(before)
    result["all_technical_pass"] = result["protected_files_unchanged"] and all(
        case["technical_pass"] for case in result["cases"].values())
    (output / "sonuc.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"cases": {name: case["technical_pass"] for name, case in result["cases"].items()},
                      "protected_files_unchanged": result["protected_files_unchanged"],
                      "all_technical_pass": result["all_technical_pass"]}, indent=2))
    return 0 if result["all_technical_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())