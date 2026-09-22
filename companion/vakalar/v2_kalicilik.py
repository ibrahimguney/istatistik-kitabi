"""V2 için katı bayt ve açıkça seçilen terminal-lf-v1 kabulü."""

import argparse
import contextlib
import csv
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("companion/vakalar/v2-nhanes")
EXPECTED = {"check_source.py", "analyze.py", "verify.py", "export.py", "verify_delivery.py",
            "README.md", "dictionary.csv", "source.json", "results.json", "psu.csv", "values.tex"}
LF_ALLOWED = {"README.md", "dictionary.csv", "export.py", "psu.csv", "results.json",
              "source.json", "values.tex", "verify_delivery.py"}
MANIFEST_HASH_WITHOUT_FINAL_LF = "5d0839cae54e0d01b1ca21ed790df4cdfc06330d4a66829168c6e00f954dafd7"


def digest(content):
    return hashlib.sha256(content).hexdigest()


def difference(actual, expected_size, expected_hash):
    if len(actual) == expected_size and digest(actual) == expected_hash:
        return "exact"
    if len(actual) + 1 == expected_size and digest(actual + b"\n") == expected_hash:
        return "one_missing_terminal_LF"
    return "other_difference"


def accepted_entry(name, status, policy):
    return status == "exact" or (policy == "terminal-lf-v1" and name in LF_ALLOWED
                                 and status == "one_missing_terminal_LF")


def lf_repairs(root=None):
    root = ROOT if root is None else root
    manifest = (root / "manifest.csv").read_bytes()
    if digest(manifest.removesuffix(b"\n")) != MANIFEST_HASH_WITHOUT_FINAL_LF:
        raise ValueError("Manifest referansı değişmiş; onarım yapılmadı")
    rows = list(csv.DictReader(io.StringIO(manifest.decode("utf-8"))))
    if len(rows) != len(EXPECTED) or {row["path"] for row in rows} != EXPECTED:
        raise ValueError("Manifest envanteri geçersiz; onarım yapılmadı")
    repairs = []
    for row in rows:
        path = root / row["path"]
        if path.is_symlink():
            raise ValueError("Sembolik bağlantı onarılmaz: " + str(path))
        content = path.read_bytes()
        content.decode("utf-8")
        status = difference(content, int(row["bytes"]), row["sha256"])
        if not accepted_entry(row["path"], status, "terminal-lf-v1"):
            raise ValueError("LF dışında fark; onarım yapılmadı: " + str(path))
        if status == "one_missing_terminal_LF":
            repairs.append((path, content, row["sha256"]))
    return repairs


def restore_terminal_lf(root=None):
    repairs = lf_repairs(root)
    changes = []
    for path, before, expected_hash in repairs:
        if path.read_bytes() != before:
            raise ValueError("Dosya ön kontrolden sonra değişmiş: " + str(path))
        path.write_bytes(before + b"\n")
        after = path.read_bytes()
        if digest(after) != expected_hash:
            raise ValueError("Onarım sonrası hash eşleşmedi: " + str(path))
        changes.append({"path": str(path), "before_sha256": digest(before),
                        "after_sha256": digest(after), "bytes_added": 1})
    return changes


def audit(policy="strict"):
    if policy not in {"strict", "terminal-lf-v1"}:
        raise ValueError("Bilinmeyen teslim kuralı")
    protected = [path for path in ROOT.iterdir() if path.is_file()]
    protected += [Path("prism-uploads/DEMO_J.zip"),
                  Path("chapters/vakalar/v2-nhanes.tex"),
                  Path("chapters/vakalar/v2-nhanes-sonuclar.tex"),
                  Path("chapters/06-ornekleme.tex")]
    before = {str(path): digest(path.read_bytes()) for path in protected if path.is_file()}
    manifest_bytes = (ROOT / "manifest.csv").read_bytes()
    manifest_reference_pass = digest(manifest_bytes.removesuffix(b"\n")) == MANIFEST_HASH_WITHOUT_FINAL_LF
    with (ROOT / "manifest.csv").open(newline="") as stream:
        manifest = list(csv.DictReader(stream))
    if len(manifest) != len(EXPECTED) or {row["path"] for row in manifest} != EXPECTED:
        raise AssertionError("Manifest envanteri eksik veya yinelenen")
    entries = []
    for row in manifest:
        path = ROOT / row["path"]
        content = path.read_bytes() if path.is_file() else None
        entries.append({"path": row["path"], "expected_bytes": int(row["bytes"]),
                        "expected_sha256": row["sha256"],
                        "actual_bytes": len(content) if content is not None else None,
                        "actual_sha256": digest(content) if content is not None else None,
                        "status": difference(content, int(row["bytes"]), row["sha256"])
                        if content is not None else "missing"})
    report = {"checked_date": datetime.now(timezone.utc).date().isoformat(),
              "acceptance_policy": policy, "manifest_reference_pass": manifest_reference_pass,
              "manifest_entries": entries, "strict_delivery_pass": False,
              "terminal_LF_only_content_check_pass": False,
              "policy_delivery_pass": False, "numeric_check_pass": None,
              "all_four_cases_accepted": False}
    safe_to_check = manifest_reference_pass and all(
        accepted_entry(row["path"], row["status"], "terminal-lf-v1") for row in entries)
    if not safe_to_check:
        report["error"] = "Referans veya dosya bütünlüğü başarısız; paket kodları çalıştırılmadı"
        return report
    for row in entries:
        (ROOT / row["path"]).read_bytes().decode("utf-8")
    sys.path.insert(0, str(ROOT))
    from check_source import read_source
    from export import artifacts
    from verify import compare, independent_result, verify
    from verify_delivery import main as strict_check

    strict_error = None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            strict_check()
    except (AssertionError, OSError, ValueError) as error:
        strict_error = str(error)
    numeric = verify()
    source = read_source()
    saved = json.loads((ROOT / "results.json").read_text())
    compare(saved, independent_result(source))
    output_checks = {}
    for name, text in artifacts(source).items():
        expected = text.encode("utf-8")
        output_checks[name] = difference((ROOT / name).read_bytes(), len(expected), digest(expected))
    chapter = Path("chapters/vakalar/v2-nhanes-sonuclar.tex").read_text()
    parent = Path("chapters/vakalar/v2-nhanes.tex").read_text()
    macros = [line.split("}", 1)[0].split("{")[1]
              for line in (ROOT / "values.tex").read_text().splitlines()]
    chapter_pass = (
        "\\input{companion/vakalar/v2-nhanes/values.tex}" in chapter
        and "\\input{chapters/vakalar/v2-nhanes-sonuclar}" in parent
        and "\\input{chapters/vakalar/v2-nhanes}"
        in Path("chapters/06-ornekleme.tex").read_text()
        and len(macros) == 9 and all(macro in chapter for macro in macros))
    content_pass = (all(accepted_entry(row["path"], row["status"], "terminal-lf-v1") for row in entries)
                    and all(accepted_entry(name, value, "terminal-lf-v1")
                            for name, value in output_checks.items())
                    and numeric["numeric_check_pass"] and chapter_pass)
    unchanged = all(digest(Path(path).read_bytes()) == value for path, value in before.items())
    report.update({"strict_delivery_pass": strict_error is None, "strict_error": strict_error,
            "terminal_LF_only_content_check_pass": content_pass,
            "policy_delivery_pass": unchanged and (strict_error is None if policy == "strict" else content_pass),
            "numeric_check_pass": numeric["numeric_check_pass"],
            "independent_saved_result_pass": True,
            "regenerated_outputs": output_checks, "chapter_binding_pass": chapter_pass,
            "protected_files_unchanged": unchanged,
            "protected_sha256": before,
            "scope": "Policy acceptance does not imply byte identity or acceptance of all four cases"})
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", choices=("strict", "terminal-lf-v1"), default="strict")
    parser.add_argument("--restore-terminal-lf", action="store_true",
                        help="Yalnız eski hashle kanıtlanan eksik son LF'leri yaz, ardından denetle")
    arguments = parser.parse_args()
    restored = []
    try:
        if arguments.restore_terminal_lf:
            restored = restore_terminal_lf()
        report = audit(arguments.policy)
    except (AssertionError, OSError, ValueError) as error:
        report = {"acceptance_policy": arguments.policy, "policy_delivery_pass": False,
                  "error": str(error), "all_four_cases_accepted": False}
    report["restoration_requested"] = arguments.restore_terminal_lf
    report["restored_files"] = restored
    report["unchanged_scope"] = "Read-only audit after any explicitly requested restoration"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["policy_delivery_pass"] else 1)