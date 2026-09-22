from hashlib import sha256
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).parent
RAW_SHA256 = "041d88ddca1da9fb8a1a9261bbf090d2f7c75625c228392e1077c2cf656051e8"


def audit_pairing(first, final):
    report = {"first_rows": len(first), "final_rows": len(final),
              "accepted": False}
    for name, frame, grade in [("first", first, "g1"), ("final", final, "g3")]:
        if list(frame.columns) != ["id", grade]:
            raise ValueError("Beklenen sutunlar id ve donem notudur.")
        numeric = pd.to_numeric(frame.id, errors="coerce")
        report[f"{name}_invalid_ids"] = int((
            numeric.isna() | ~np.isfinite(numeric) | numeric.le(0)
            | numeric.ne(np.floor(numeric))
        ).sum())
        report[f"{name}_duplicate_ids"] = frame.loc[
            frame.id.duplicated(keep=False), "id"].drop_duplicates().tolist()
    if any(report[f"{name}_invalid_ids"] or report[f"{name}_duplicate_ids"]
           for name in ["first", "final"]):
        report["reason"] = "invalid_or_duplicate_key"
        return report, None
    pairs = first.merge(final, on="id", how="outer", validate="one_to_one",
                        indicator=True, sort=True)
    report["first_only_ids"] = pairs.loc[pairs._merge.eq("left_only"), "id"].tolist()
    report["final_only_ids"] = pairs.loc[pairs._merge.eq("right_only"), "id"].tolist()
    matched = pairs._merge.eq("both")
    report["matched_ids"] = int(matched.sum())
    invalid_grade = pd.Series(False, index=pairs.index)
    for grade in ["g1", "g3"]:
        values = pd.to_numeric(pairs[grade], errors="coerce")
        invalid_grade |= (values.isna() | ~np.isfinite(values)
                          | ~values.between(0, 20) | values.ne(np.floor(values)))
    report["invalid_grade_matched_ids"] = pairs.loc[matched & invalid_grade, "id"].tolist()
    report["complete_pairs"] = int((matched & ~invalid_grade).sum())
    if report["first_only_ids"] or report["final_only_ids"] or report["invalid_grade_matched_ids"]:
        report["reason"] = "unmatched_key_or_invalid_measurement"
        return report, None
    report["accepted"] = True
    report["reason"] = "complete_one_to_one"
    return report, pairs[["id", "g1", "g3"]].copy()


def summarize(difference):
    return {"pairs": len(difference), "mean": float(difference.mean()),
            "sd": float(difference.std(ddof=1)), "median": float(difference.median()),
            "minimum": int(difference.min()), "maximum": int(difference.max()),
            "negative": int(difference.lt(0).sum()), "zero": int(difference.eq(0).sum()),
            "positive": int(difference.gt(0).sum())}


def main():
    raw_path = ROOT / "raw/student-mat.csv"
    if sha256(raw_path.read_bytes()).hexdigest() != RAW_SHA256:
        raise ValueError("Ham kaynak degisti; once yeni surum incelenmeli.")
    source = pd.read_csv(raw_path, sep=";")
    book = pd.read_csv(ROOT / "raw/b11.csv")
    assert source.shape == (395, 33) and book.shape == (395, 10)
    np.testing.assert_array_equal(book.id, np.arange(1, 396))
    np.testing.assert_array_equal(source[["G1", "G3"]], book[["g1", "g3"]])
    first = book[["id", "g1"]].copy()
    final = book[["id", "g3"]].copy()
    reversed_final = final.iloc[::-1].reset_index(drop=True)
    accepted, pairs = audit_pairing(first, reversed_final)
    assert accepted["accepted"] and accepted["complete_pairs"] == 395
    pairs["source_line"] = pairs.id + 1
    pairs["difference"] = pairs.g3 - pairs.g1
    summary = summarize(pairs.difference)
    wrong_difference = reversed_final.g3 - first.g1
    wrong = summarize(wrong_difference)
    wrong["wrong_partner_ids"] = int(reversed_final.id.ne(first.id).sum())
    wrong["status"] = "artificial_invalid_positional_pairing_not_a_study_result"
    summary["g3_zero_count"] = int(pairs.g3.eq(0).sum())
    summary["source_sha256"] = RAW_SHA256
    summary["new_independent_study"] = False
    summary["wrong_positional_demo"] = wrong
    missing_grade = final.copy().astype({"g3": float})
    missing_grade.loc[missing_grade.id.eq(1), "g3"] = np.nan
    scenarios = {
        "original": final,
        "reversed_order_keyed_join": reversed_final,
        "artificial_missing_final_row_id1": final.loc[final.id.ne(1)].copy(),
        "artificial_duplicate_final_id1": pd.concat([final, final.iloc[[0]]], ignore_index=True),
        "artificial_missing_grade_id1": missing_grade,
        "artificial_extra_final_id1001": pd.concat([
            final, pd.DataFrame({"id": [1001], "g3": [10]})], ignore_index=True),
    }
    audits = {name: audit_pairing(first, frame)[0] for name, frame in scenarios.items()}
    assert [name for name, audit in audits.items() if audit["accepted"]] == [
        "original", "reversed_order_keyed_join"]
    first.to_csv(ROOT / "g1.csv", index=False)
    reversed_final.to_csv(ROOT / "g3-reversed.csv", index=False)
    pairs.to_csv(ROOT / "paired.csv", index=False)
    counts = pairs.difference.value_counts().sort_index().rename_axis("difference").reset_index(name="count")
    counts.to_csv(ROOT / "difference-counts.csv", index=False)
    for name, value in [("results.json", summary), ("teaching-scenarios.json", audits)]:
        (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    figure, axis = plt.subplots(figsize=(6.2, 3.1), layout="constrained")
    axis.bar(counts.difference, counts["count"], color="#416b8c", width=.8)
    axis.axvline(0, color="#333333", linestyle="--", linewidth=.8)
    axis.set(xlabel="G3 − G1 (puan)", ylabel="Kayıt sayısı",
             title="Doğrulanmış 395 çiftin fark dağılımı",
             xticks=np.arange(-12, 5, 2), xlim=(-12.8, 4.8))
    figure.savefig(ROOT / "differences.png", dpi=180,
                   metadata={"Software": "V3 eslesme"})
    plt.close(figure)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()