from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parent
BLOCKS = ["ONE", "TWO", "THREE"]
TREATMENTS = ["No Fertilizer", "FYM", "NPK", "NPK+FYM"]
SOURCE_SHA256 = "ebe2ec9480ba8498585a1b8527ab92ad0db1b4bbb2f85ba27a2e61b705412e10"
NAMESPACE = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def read_source(path):
    if sha256(path.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("Kaynak XLSX degisti; yeni surum once incelenmeli.")
    with ZipFile(path) as archive:
        assert archive.testzip() is None
        strings = [
            "".join(node.itertext())
            for node in ET.fromstring(archive.read("xl/sharedStrings.xml"))
        ]
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets = workbook.findall("m:sheets/m:sheet", NAMESPACE)
        data_sheet = next(sheet for sheet in sheets if sheet.get("name") == "DATA")
        relation_id = data_sheet.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )
        relations = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        target = next(node.get("Target") for node in relations if node.get("Id") == relation_id)
        assert target.startswith("worksheets/") and ".." not in target
        worksheet = ET.fromstring(archive.read("xl/" + target))
        records = []
        for row in worksheet.findall("m:sheetData/m:row", NAMESPACE):
            values = [None] * 14
            for cell in row:
                assert cell.find("m:f", NAMESPACE) is None
                column = "".join(char for char in cell.get("r") if char.isalpha())
                assert len(column) == 1 and "A" <= column <= "N"
                value = cell.find("m:v", NAMESPACE)
                if value is not None:
                    content = value.text
                    values[ord(column) - ord("A")] = (
                        strings[int(content)] if cell.get("t") == "s" else float(content)
                    )
            records.append((int(row.get("r")), values))
    frame = pd.DataFrame([values for _, values in records[1:]], columns=records[0][1])
    assert frame.shape == (24, 14) and not frame.isna().any().any()
    assert frame["Block"].isin(BLOCKS).all()
    assert frame["Treatment"].isin(TREATMENTS).all()
    counts = pd.crosstab(frame["Block"], frame["Treatment"]).reindex(
        index=BLOCKS, columns=TREATMENTS
    )
    assert counts.eq(2).all().all()
    selected = frame[["Block", "Treatment", "Mean dry matter (2011-2014)"]].copy()
    selected.columns = ["block", "treatment", "dry_matter_g_m2"]
    selected.insert(0, "source_row", [number for number, _ in records[1:]])
    assert selected.source_row.is_unique
    assert np.isfinite(selected.dry_matter_g_m2).all()
    assert selected.dry_matter_g_m2.ge(0).all()
    return selected, counts


def analyze(frame):
    pair = frame[frame.treatment.isin(["No Fertilizer", "FYM"])].copy()
    assert len(pair) == 12
    block_summary = pair.pivot_table(
        index="block", columns="treatment", values="dry_matter_g_m2", aggfunc="mean"
    ).reindex(BLOCKS)
    block_summary["difference"] = block_summary["FYM"] - block_summary["No Fertilizer"]
    observed = float(block_summary.difference.mean())
    possibilities = []
    for block in BLOCKS:
        values = pair.loc[pair.block == block, "dry_matter_g_m2"].to_numpy()
        assert len(values) == 4
        differences = []
        for treated in combinations(range(4), 2):
            mask = np.zeros(4, dtype=bool)
            mask[list(treated)] = True
            differences.append(values[mask].mean() - values[~mask].mean())
        possibilities.append(differences)
    distribution = np.array([np.mean(choice) for choice in product(*possibilities)])
    assert len(distribution) == 216
    assert np.isclose(distribution.mean(), 0, atol=1e-10)
    np.testing.assert_allclose(np.sort(distribution), -np.sort(distribution)[::-1], atol=1e-10)
    extreme = int(np.count_nonzero(np.abs(distribution) >= abs(observed) - 1e-10))
    response = pair.dry_matter_g_m2.to_numpy()
    design = np.column_stack([
        np.ones(len(pair)), pair.treatment.eq("FYM").astype(float),
        pair.block.eq("TWO").astype(float), pair.block.eq("THREE").astype(float),
    ])
    coefficients = np.linalg.lstsq(design, response, rcond=None)[0]
    residual = response - design @ coefficients
    degrees = len(pair) - np.linalg.matrix_rank(design)
    variance = float(residual @ residual / degrees)
    standard_error = float(np.sqrt(variance * np.linalg.inv(design.T @ design)[1, 1]))
    interval = coefficients[1] + np.array([-1, 1]) * stats.t.ppf(.975, degrees) * standard_error
    np.testing.assert_allclose(coefficients[1], observed, atol=1e-10)
    summary = {
        "source_shape": [24, 14], "analysis_n": len(pair), "blocks": len(BLOCKS),
        "control_mean": float(pair.loc[pair.treatment.eq("No Fertilizer"), "dry_matter_g_m2"].mean()),
        "fym_mean": float(pair.loc[pair.treatment.eq("FYM"), "dry_matter_g_m2"].mean()),
        "difference_g_m2": observed, "assignments": len(distribution),
        "extreme_assignments": extreme, "exact_two_sided_p": extreme / len(distribution),
        "model_standard_error": standard_error, "model_residual_df": int(degrees),
        "model_ci95_low": float(interval[0]), "model_ci95_high": float(interval[1]),
        "model_residual_sd": float(np.sqrt(variance)),
        "unit": "g/m2", "outcome_period": "2011-2014 mean",
        "original_R_executed": False,
    }
    return pair, block_summary, distribution, summary


def main():
    frame, counts = read_source(ROOT / "raw/s1-data.xlsx")
    pair, blocks, distribution, summary = analyze(frame)
    frame.to_csv(ROOT / "data.csv", index=False, float_format="%.17g")
    pair.to_csv(ROOT / "comparison.csv", index=False, float_format="%.17g")
    blocks.to_csv(ROOT / "block-means.csv", float_format="%.17g")
    counts.to_csv(ROOT / "allocation-counts.csv")
    pd.DataFrame({"difference_g_m2": distribution}).to_csv(
        ROOT / "randomization.csv", index=False, float_format="%.17g"
    )
    (ROOT / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
    figure, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for offset, treatment, color in [(-.12, "No Fertilizer", "#1F4E79"), (.12, "FYM", "#B45F06")]:
        subset = pair[pair.treatment.eq(treatment)]
        positions = subset.block.map({block: index for index, block in enumerate(BLOCKS)})
        axes[0].scatter(positions + offset, subset.dry_matter_g_m2, label=treatment, color=color)
    axes[0].set_xticks(range(3), BLOCKS)
    axes[0].set(xlabel="Blok", ylabel="Kuru madde (g/m2)")
    axes[0].legend(fontsize=8)
    axes[1].hist(distribution, bins=19, color="#1F4E79", edgecolor="white")
    axes[1].axvline(summary["difference_g_m2"], color="#B45F06", label="Gozlenen fark")
    axes[1].axvline(-summary["difference_g_m2"], color="#B45F06", linestyle="--")
    axes[1].set(xlabel="FYM - kontrol (g/m2)", ylabel="Atama sayisi")
    axes[1].legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(ROOT / "comparison.png", dpi=180)
    plt.close(figure)
    paths = [path for path in ROOT.rglob("*") if path.is_file()
             and path.name != "manifest.csv" and "__pycache__" not in path.parts]
    pd.DataFrame([
        {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()}
        for path in sorted(paths)
    ]).to_csv(ROOT / "manifest.csv", index=False)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()