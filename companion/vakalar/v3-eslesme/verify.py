from collections import Counter
from hashlib import sha256
from pathlib import Path
import csv
import json
import math
import statistics

import numpy as np
import pandas as pd
from scipy import stats

from analyze import audit_pairing


ROOT = Path(__file__).parent


def main():
    with (ROOT / "raw/student-mat.csv").open(newline="") as stream:
        source = list(csv.DictReader(stream, delimiter=";"))
    with (ROOT / "g1.csv").open(newline="") as stream:
        first = {int(row["id"]): int(row["g1"]) for row in csv.DictReader(stream)}
    with (ROOT / "g3-reversed.csv").open(newline="") as stream:
        final_rows = list(csv.DictReader(stream))
        final = {int(row["id"]): int(row["g3"]) for row in final_rows}
    assert set(first) == set(final) == set(range(1, 396))
    differences = []
    for record_id, row in enumerate(source, 1):
        assert first[record_id] == int(row["G1"]) and final[record_id] == int(row["G3"])
        differences.append(final[record_id] - first[record_id])
    result = json.loads((ROOT / "results.json").read_text())
    assert result["negative"] == sum(value < 0 for value in differences) == 159
    assert result["zero"] == differences.count(0) == 93
    assert result["positive"] == sum(value > 0 for value in differences) == 143
    assert result["g3_zero_count"] == sum(value == 0 for value in final.values()) == 38
    assert result["pairs"] == 395 and result["minimum"] == -12 and result["maximum"] == 4
    np.testing.assert_allclose(result["mean"], statistics.mean(differences), rtol=1e-12)
    np.testing.assert_allclose(result["sd"], statistics.stdev(differences), rtol=1e-12)
    with (ROOT / "paired.csv").open(newline="") as stream:
        pairs = list(csv.DictReader(stream))
    assert len(pairs) == 395
    for row in pairs:
        record_id = int(row["id"])
        assert int(row["source_line"]) == record_id + 1
        assert int(row["g1"]) == first[record_id] and int(row["g3"]) == final[record_id]
        assert int(row["difference"]) == differences[record_id - 1]
    with (ROOT / "difference-counts.csv").open(newline="") as stream:
        counts = {int(row["difference"]): int(row["count"]) for row in csv.DictReader(stream)}
    assert counts == dict(Counter(differences))
    wrong = [int(row["g3"]) - first[position] for position, row in enumerate(final_rows, 1)]
    assert sum(wrong) == sum(differences) == -195
    np.testing.assert_allclose(statistics.stdev(wrong), result["wrong_positional_demo"]["sd"])
    assert sum(int(row["id"]) != position for position, row in enumerate(final_rows, 1)) == 394
    audits = json.loads((ROOT / "teaching-scenarios.json").read_text())
    assert audits["reversed_order_keyed_join"]["complete_pairs"] == 395
    assert audits["artificial_missing_final_row_id1"]["first_only_ids"] == [1]
    assert audits["artificial_missing_final_row_id1"]["complete_pairs"] == 394
    assert audits["artificial_duplicate_final_id1"]["final_duplicate_ids"] == [1]
    assert audits["artificial_missing_grade_id1"]["matched_ids"] == 395
    assert audits["artificial_missing_grade_id1"]["complete_pairs"] == 394
    assert audits["artificial_extra_final_id1001"]["final_only_ids"] == [1001]
    first_frame = pd.read_csv(ROOT / "g1.csv")
    final_frame = pd.read_csv(ROOT / "g3-reversed.csv")
    for seed in [7, 2026]:
        audit, shuffled = audit_pairing(first_frame.sample(frac=1, random_state=seed),
                                       final_frame.sample(frac=1, random_state=seed + 1))
        assert audit["accepted"]
        np.testing.assert_array_equal(shuffled.g3 - shuffled.g1, differences)
    invalid_key = final_frame.copy().astype({"id": float})
    invalid_key.loc[0, "id"] = np.nan
    assert not audit_pairing(first_frame, invalid_key)[0]["accepted"]
    invalid_grade = final_frame.copy()
    invalid_grade.loc[0, "g3"] = 21
    assert not audit_pairing(first_frame, invalid_grade)[0]["accepted"]
    reassigned = final_frame.copy()
    reassigned["id"] = first_frame.id.to_numpy()
    mechanical, incorrectly_linked = audit_pairing(first_frame, reassigned)
    assert mechanical["accepted"]
    assert not np.array_equal(incorrectly_linked.g3, [final[record_id] for record_id in first])
    old_test = stats.ttest_rel(list(final.values()), [first[record_id] for record_id in final])
    np.testing.assert_allclose(old_test.statistic, -3.551703, rtol=0, atol=5e-7)
    standard_error = statistics.stdev(differences) / math.sqrt(395)
    interval = statistics.mean(differences) + np.array([-1, 1]) * stats.t.ppf(.975, 394) * standard_error
    np.testing.assert_allclose(interval, [-.766937, -.220405], rtol=0, atol=5e-7)
    small = pd.read_csv(ROOT / "raw/b14-summary.csv")
    np.testing.assert_allclose(small.iloc[0].to_numpy(), [24, -3.2, 6, .05])
    inventory = pd.read_csv(ROOT / "manifest.csv")
    assert inventory.path.is_unique and len(inventory) == 14
    for row in inventory.itertuples(index=False):
        raw = (ROOT / row.path).read_bytes()
        assert len(raw) == row.bytes and sha256(raw).hexdigest() == row.sha256
    print(json.dumps({"verified": True, "source_pairs_compared": len(differences),
                      "artificial_cases_checked": 4, "permutation_checks": 2,
                      "reassigned_key_provenance_check": True,
                      "existing_b11_t_ci_compatible": True, "manifest_files": len(inventory),
                      "new_hypothesis_test_reported": False}, indent=2))


if __name__ == "__main__":
    main()