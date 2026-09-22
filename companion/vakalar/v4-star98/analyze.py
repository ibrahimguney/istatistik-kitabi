"""STAR98: eşit satır ağırlığı ve toplam sayım oranı; yalnız betimleme."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).parent
PROJECT = ROOT.parents[2]
INPUTS = {
    "companion/data/raw/star98_statsmodels.csv":
        "a4f7f69ad8062358fd497f3e414df467b6b5332676854983bebe8c0dc9ace540",
    "companion/data/clean/star98_districts.csv":
        "bd92e4cfe7d222c48d30b54321be39fd7fa7995be87f17e0c1d3f94ce5ecaf13",
}


def summarize(counts):
    required = ["district_id", "above", "below"]
    if list(counts.columns) != required or counts.empty:
        raise ValueError("Beklenen sütunlar ve en az bir kayıt gerekli")
    values = counts.to_numpy(dtype=float)
    if not np.isfinite(values).all() or not np.equal(values, np.floor(values)).all():
        raise ValueError("Eksiksiz sonlu tamsayılar gerekli")
    if counts.district_id.duplicated().any() or (counts.district_id <= 0).any():
        raise ValueError("Pozitif ve benzersiz yerel anahtar gerekli")
    if (counts[["above", "below"]] < 0).any().any():
        raise ValueError("Negatif sayım kabul edilmez")
    table = counts.copy()
    table["total"] = table.above + table.below
    if (table.total <= 0).any():
        raise ValueError("Sıfır paydalı satır kabul edilmez")
    table["rate"] = table.above / table.total
    table["equal_weight"] = 1 / len(table)
    table["size_weight"] = table.total / table.total.sum()
    table["pooled_contribution"] = table.size_weight * table.rate
    equal = float(table.rate.mean())
    pooled = float(table.above.sum() / table.total.sum())
    covariance = float(np.mean((table.total - table.total.mean()) * (table.rate - equal)))
    result = {
        "records": len(table),
        "above_total": int(table.above.sum()),
        "below_total": int(table.below.sum()),
        "count_total": int(table.total.sum()),
        "equal_rate": equal,
        "pooled_rate": pooled,
        "pooled_minus_equal_pp": 100 * (pooled - equal),
        "minimum_count": int(table.total.min()),
        "maximum_count": int(table.total.max()),
        "covariance_divided_by_mean_count": covariance / float(table.total.mean()),
        "scope": "local_303_aggregate_records_not_population_inference",
        "inference_computed": False,
    }
    return table, result


def main():
    for name, expected in INPUTS.items():
        if hashlib.sha256((PROJECT / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Kaynak sürümü değişmiş: {name}")
    raw = pd.read_csv(PROJECT / "companion/data/raw/star98_statsmodels.csv")
    clean = pd.read_csv(PROJECT / "companion/data/clean/star98_districts.csv")
    if raw.shape != (303, 23) or clean.shape != (303, 19):
        raise ValueError("Kaynak boyutları uyuşmuyor")
    counts = raw[["DISTRICT_ID", "NABOVE", "NBELOW"]].copy()
    counts.columns = ["district_id", "above", "below"]
    table, result = summarize(counts)
    expected = table.sort_values("district_id")
    observed = clean.sort_values("district_id")
    for derived, source in [("district_id", "district_id"),
                            ("above", "above_median_count"),
                            ("below", "below_median_count"),
                            ("total", "tested_count")]:
        if not np.array_equal(expected[derived].to_numpy(), observed[source].to_numpy()):
            raise ValueError(f"Ham/temiz eşleşmesi başarısız: {source}")
    if not np.allclose(expected.rate, observed.above_median_rate, rtol=0, atol=1e-14):
        raise ValueError("Oran aktarımı uyuşmuyor")
    table.insert(1, "source_line", np.arange(2, len(table) + 2))
    table.to_csv(ROOT / "aggregates.csv", index=False, float_format="%.15g")
    (ROOT / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()