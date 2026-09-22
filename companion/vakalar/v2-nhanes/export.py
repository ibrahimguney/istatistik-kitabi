"""V2 sonuçlarını üretir; referans manifestini değiştirmez."""

import argparse
import json
from pathlib import Path

from analyze import calculate
from check_source import read_source


ROOT = Path("companion/vakalar/v2-nhanes")


def artifacts(source=None):
    source = read_source() if source is None else source
    result = calculate(source)
    data = source[["SDMVSTRA", "SDMVPSU", "RIDAGEYR", "WTINT2YR"]].copy()
    data["SDMVSTRA"] = data.SDMVSTRA.round().astype(int)
    data["SDMVPSU"] = data.SDMVPSU.round().astype(int)
    data["adult"] = (data.RIDAGEYR >= 20).astype(int)
    data["older"] = (data.RIDAGEYR >= 60).astype(int)
    data["weighted_adult"] = data.WTINT2YR * data.adult
    data["weighted_older"] = data.WTINT2YR * data.older
    data["linearized"] = (data.weighted_older - result["weighted_proportion"] *
                          data.weighted_adult) / result["weighted_denominator"]
    psu = data.groupby(["SDMVSTRA", "SDMVPSU"]).agg(
        records=("adult", "size"), adults=("adult", "sum"), older=("older", "sum"),
        weighted_adult=("weighted_adult", "sum"), weighted_older=("weighted_older", "sum"),
        linearized=("linearized", "sum")).reset_index()
    macros = {"VtwoN": str(result["records"]), "VtwoAdults": str(result["adults"]),
              "VtwoOlder": str(result["older"]), "VtwoDf": str(result["design_df"])}
    for name, key in {"VtwoWeighted": "weighted_proportion", "VtwoUnweighted": "unweighted_proportion",
                      "VtwoSE": "standard_error", "VtwoLower": "ci_lower", "VtwoUpper": "ci_upper"}.items():
        macros[name] = f"{100 * result[key]:.4f}".replace(".", "{,}")
    values = "".join("\\newcommand{\\" + name + "}{" + value + "}\n" for name, value in macros.items())
    return {"results.json": json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            "psu.csv": psu.to_csv(index=False, float_format="%.17g"), "values.tex": values}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    output = parser.parse_args().output_dir
    content = artifacts()
    output.mkdir(parents=True, exist_ok=True)
    for name, text in content.items():
        (output / name).write_text(text, encoding="utf-8")
    print("Üretildi: " + ", ".join(content) + "; manifest değiştirilmedi")


if __name__ == "__main__":
    main()