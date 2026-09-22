"""V2 küçük teslim 02: alt evren hesabı; yalnız standart çıktıya yazar."""

import json

import numpy as np
from scipy.stats import t

from check_source import check_frame, read_source


def calculate(source):
    checks = check_frame(source)
    data = source[["RIDAGEYR", "WTINT2YR", "SDMVSTRA", "SDMVPSU"]].copy()
    age = np.rint(data.RIDAGEYR).astype(int)
    data["adult"] = (age >= 20).astype(int)
    data["older"] = (age >= 60).astype(int)
    data["weighted_adult"] = data.WTINT2YR * data.adult
    data["weighted_older"] = data.WTINT2YR * data.adult * data.older
    denominator = float(data.weighted_adult.sum())
    numerator = float(data.weighted_older.sum())
    if denominator <= 0:
        raise ValueError("Alt evren paydası pozitif olmalı")
    proportion = numerator / denominator
    data["linearized"] = (data.weighted_older - proportion * data.weighted_adult) / denominator
    psu_totals = data.groupby(["SDMVSTRA", "SDMVPSU"]).linearized.sum()
    variance = 0.0
    for _, group in psu_totals.groupby(level="SDMVSTRA"):
        count = len(group)
        if count < 2:
            raise ValueError("Tek PSU tabakası için otomatik düzeltme yok")
        variance += count / (count - 1) * float(((group - group.mean()) ** 2).sum())
    degrees = checks["adult_psus"] - checks["adult_strata"]
    if degrees <= 0:
        raise ValueError("Alt evren serbestlik derecesi pozitif olmalı")
    standard_error = float(np.sqrt(variance))
    critical = float(t.ppf(0.975, degrees))
    return {
        "records": checks["records"], "adults": checks["adults"], "older": checks["older"],
        "strata": checks["strata"], "psus": checks["psus"],
        "adult_strata": checks["adult_strata"], "adult_psus": checks["adult_psus"],
        "weighted_numerator": numerator, "weighted_denominator": denominator,
        "weighted_proportion": proportion,
        "unweighted_proportion": checks["older"] / checks["adults"],
        "taylor_variance": variance, "standard_error": standard_error,
        "design_df": degrees, "confidence_level": 0.95, "t_critical": critical,
        "ci_lower": proportion - critical * standard_error,
        "ci_upper": proportion + critical * standard_error,
        "method": "Full-design Taylor linearization; no FPC; domain df; approximate t-Wald interval",
        "source_xpt_sha256": checks["xpt_sha256"],
        "complete_delivery_accepted": False,
    }


if __name__ == "__main__":
    print(json.dumps(calculate(read_source()), ensure_ascii=False, indent=2))