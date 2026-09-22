"""V2 dosya manifesti, kaydedilmiş çıktılar ve kitap bağlantısı kontrolü."""

import csv
import hashlib
import json
from pathlib import Path

from check_source import read_source
from export import ROOT, artifacts
from verify import compare, independent_result, verify


EXPECTED = {"check_source.py", "analyze.py", "verify.py", "export.py", "verify_delivery.py",
            "README.md", "dictionary.csv", "source.json", "results.json", "psu.csv", "values.tex"}


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    with (ROOT / "manifest.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    check(len(rows) == len(EXPECTED) and {row["path"] for row in rows} == EXPECTED,
          "Manifest envanteri eksik veya yinelenen")
    for row in rows:
        content = (ROOT / row["path"]).read_bytes()
        matches = len(content) == int(row["bytes"]) and hashlib.sha256(content).hexdigest() == row["sha256"]
        suffix = " (yalnız son LF eksik)" if hashlib.sha256(content + b"\n").hexdigest() == row["sha256"] else ""
        check(matches, "Manifest uyuşmazlığı: " + row["path"] + suffix)
    numeric = verify()
    source = read_source()
    for name, text in artifacts(source).items():
        check((ROOT / name).read_bytes() == text.encode("utf-8"), "Yeniden üretim: " + name)
    saved = json.loads((ROOT / "results.json").read_text())
    compare(saved, independent_result(source))
    with (ROOT / "psu.csv").open(newline="") as stream:
        psus = list(csv.DictReader(stream))
    keys = {(int(row["SDMVSTRA"]), int(row["SDMVPSU"])) for row in psus}
    check(len(psus) == len(keys) == 30, "PSU envanteri")
    for row in psus:
        stratum, psu = int(row["SDMVSTRA"]), int(row["SDMVPSU"])
        records = source.loc[(source.SDMVSTRA == stratum) & (source.SDMVPSU == psu)]
        adult = records.RIDAGEYR >= 20
        older = records.RIDAGEYR >= 60
        expected = {"records": len(records), "adults": int(adult.sum()), "older": int(older.sum()),
                    "weighted_adult": float(records.loc[adult, "WTINT2YR"].sum()),
                    "weighted_older": float(records.loc[older, "WTINT2YR"].sum())}
        expected["linearized"] = (expected["weighted_older"] - saved["weighted_proportion"] *
                                  expected["weighted_adult"]) / saved["weighted_denominator"]
        compare({key: float(row[key]) for key in expected}, expected)
    chapter = Path("chapters/vakalar/v2-nhanes-sonuclar.tex").read_text()
    parent = Path("chapters/vakalar/v2-nhanes.tex").read_text()
    check("\\input{companion/vakalar/v2-nhanes/values.tex}" in chapter, "Kitap değer bağlantısı")
    check("\\input{chapters/vakalar/v2-nhanes-sonuclar}" in parent, "Vaka sonuç bağlantısı")
    check("\\input{chapters/vakalar/v2-nhanes}" in Path("chapters/06-ornekleme.tex").read_text(), "B06 bağlantısı")
    macros = [line.split("}", 1)[0].split("{")[1] for line in (ROOT / "values.tex").read_text().splitlines()]
    check(all(macro in chapter for macro in macros), "Kitapta kullanılmayan çıktı makrosu")
    print(json.dumps({"delivery_check_pass": True, "manifest_entries": len(rows),
                      "saved_outputs_reproduced": True, "numeric_check_pass": numeric["numeric_check_pass"],
                      "chapter_binding_pass": True, "psu_rows": len(psus),
                      "cross_session_persistence_verified": False,
                      "all_four_cases_accepted": False}, indent=2))


if __name__ == "__main__":
    main()