"""Bağımsız CSV/Fraction hesabı ve V4 kabul kapılarının denetimi."""

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import pandas as pd

from analyze import summarize


ROOT = Path(__file__).parent
PROJECT = ROOT.parents[2]


def main():
    with (PROJECT / "companion/data/raw/star98_statsmodels.csv").open() as stream:
        raw = list(csv.DictReader(stream))
    pairs = [(int(float(row["NABOVE"])), int(float(row["NBELOW"]))) for row in raw]
    equal = sum((Fraction(above, above + below) for above, below in pairs), Fraction()) / len(pairs)
    pooled = Fraction(sum(above for above, below in pairs), sum(above + below for above, below in pairs))
    result = json.loads((ROOT / "results.json").read_text())
    assert len(pairs) == result["records"] == 303
    assert result["above_total"] == 108418 and result["below_total"] == 159193
    assert result["count_total"] == 267611
    for key, value in [("equal_rate", equal), ("pooled_rate", pooled),
                       ("pooled_minus_equal_pp", 100 * (pooled - equal)),
                       ("covariance_divided_by_mean_count", pooled - equal)]:
        assert math.isclose(result[key], float(value), rel_tol=0, abs_tol=1e-12), key
    with (ROOT / "aggregates.csv").open() as stream:
        derived = list(csv.DictReader(stream))
    assert len(derived) == 303
    for number, (source, row) in enumerate(zip(raw, derived), start=2):
        assert int(float(row["district_id"])) == int(float(source["DISTRICT_ID"]))
        assert int(row["source_line"]) == number
        above, below = int(float(source["NABOVE"])), int(float(source["NBELOW"]))
        assert float(row["above"]) == above and float(row["below"]) == below
        assert float(row["total"]) == above + below
        assert math.isclose(float(row["rate"]), above / (above + below), abs_tol=1e-14)
    assert math.isclose(sum(float(row["size_weight"]) for row in derived), 1)
    assert math.isclose(sum(float(row["equal_weight"]) for row in derived), 1)
    assert math.isclose(sum(float(row["pooled_contribution"]) for row in derived), float(pooled))
    counts = pd.DataFrame([(index, *pair) for index, pair in enumerate(pairs, 1)],
                          columns=["district_id", "above", "below"])
    for seed in [7, 2026]:
        _, reordered = summarize(counts.sample(frac=1, random_state=seed))
        assert math.isclose(reordered["equal_rate"], float(equal))
        assert math.isclose(reordered["pooled_rate"], float(pooled))
    bad_cases = []
    for column, value in [("above", -1), ("below", float("nan")), ("above", 0.5),
                          ("district_id", 2), ("district_id", float("inf"))]:
        changed = counts.astype(float).copy()
        changed.loc[0, column] = value
        bad_cases.append(changed)
    zero = counts.copy()
    zero.loc[0, ["above", "below"]] = 0
    bad_cases.extend([zero, counts.iloc[:0]])
    for changed in bad_cases:
        try:
            summarize(changed)
        except ValueError:
            pass
        else:
            raise AssertionError("Geçersiz girdi kabul edildi")
    valid_zero = counts.copy()
    valid_zero.loc[0, "above"] = 0
    summarize(valid_zero)
    with (ROOT / "synthetic-margins.csv").open() as stream:
        synthetic = list(csv.DictReader(stream))
    for scenario, expected_gap in [("A", Fraction(3, 5)), ("B", Fraction(-3, 5))]:
        rows = [row for row in synthetic if row["scenario"] == scenario]
        assert len(rows) == 2
        assert sum(int(row["above"]) for row in rows) == 50
        assert sum(int(row["below"]) for row in rows) == 50
        assert all(int(row["above"]) + int(row["below"]) == 50 for row in rows)
        rates = {row["group"]: Fraction(int(row["above"]), 50) for row in rows}
        assert rates["low_income"] - rates["other"] == expected_gap
    with (ROOT / "manifest.csv").open() as stream:
        manifest = list(csv.DictReader(stream))
    assert len({row["path"] for row in manifest}) == len(manifest)
    assert len(manifest) == 9
    for row in manifest:
        assert hashlib.sha256((PROJECT / row["path"]).read_bytes()).hexdigest() == row["sha256"]
    print(json.dumps({"verified": True, "source_rows": 303, "invalid_inputs_rejected": len(bad_cases),
                      "permutation_checks": 2, "synthetic_scenarios": 2, "manifest_entries": len(manifest)}, indent=2))


if __name__ == "__main__":
    main()