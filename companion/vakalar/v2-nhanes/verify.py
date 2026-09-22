"""Pay/payda kovaryansıyla bağımsız sayısal kontrol; veri dosyası yazmaz."""

import json
import math
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy.stats import t

from analyze import calculate
from check_source import read_source


def independent_result(source):
    groups = defaultdict(list)
    adult_count = older_count = 0
    for age, weight, stratum, psu in source[
            ["RIDAGEYR", "WTINT2YR", "SDMVSTRA", "SDMVPSU"]].itertuples(index=False, name=None):
        adult = age >= 20
        older = age >= 60
        adult_count += int(adult)
        older_count += int(older)
        groups[(int(round(stratum)), int(round(psu)))].append(
            (weight if older else 0.0, weight if adult else 0.0))
    totals = {key: (math.fsum(row[0] for row in rows), math.fsum(row[1] for row in rows))
              for key, rows in groups.items()}
    numerator = math.fsum(pair[0] for pair in totals.values())
    denominator = math.fsum(pair[1] for pair in totals.values())
    proportion = numerator / denominator
    numerator_variance = denominator_variance = covariance = 0.0
    strata = sorted({key[0] for key in totals})
    for stratum in strata:
        first, second = totals[(stratum, 1)], totals[(stratum, 2)]
        numerator_difference = first[0] - second[0]
        denominator_difference = first[1] - second[1]
        numerator_variance += numerator_difference ** 2
        denominator_variance += denominator_difference ** 2
        covariance += numerator_difference * denominator_difference
    variance = (numerator_variance + proportion ** 2 * denominator_variance
                - 2 * proportion * covariance) / denominator ** 2
    domain_units = [key for key, pair in totals.items() if pair[1] > 0]
    degrees = len(domain_units) - len({key[0] for key in domain_units})
    standard_error = math.sqrt(variance)
    critical = float(t.ppf(0.975, degrees))
    return {
        "records": len(source), "adults": adult_count, "older": older_count,
        "strata": len(strata), "psus": len(groups),
        "adult_strata": len({key[0] for key in domain_units}), "adult_psus": len(domain_units),
        "weighted_numerator": numerator, "weighted_denominator": denominator,
        "weighted_proportion": proportion, "unweighted_proportion": older_count / adult_count,
        "taylor_variance": variance, "standard_error": standard_error,
        "design_df": degrees, "confidence_level": .95, "t_critical": critical,
        "ci_lower": proportion - critical * standard_error,
        "ci_upper": proportion + critical * standard_error,
    }


def compare(actual, expected):
    for key, value in expected.items():
        if not math.isclose(actual[key], value, rel_tol=1e-11, abs_tol=1e-12):
            raise AssertionError(f"{key}: {actual[key]} != {value}")


def verify():
    source = read_source()
    untouched = source.copy(deep=True)
    result = calculate(source)
    compare(result, independent_result(source))
    compare(result, {"records": 9254, "adults": 5569, "older": 2150,
                     "strata": 15, "psus": 30, "adult_psus": 30, "design_df": 15})
    shuffled = calculate(source.sample(frac=1, random_state=2026))
    compare(shuffled, independent_result(source))
    scaled = source.copy(deep=True)
    scaled["WTINT2YR"] *= 7
    scaled_result = calculate(scaled)
    compare(scaled_result, independent_result(scaled))
    compare(scaled_result, {key: result[key] for key in
                           ["weighted_proportion", "taylor_variance", "ci_lower", "ci_upper"]})
    domain = source.copy(deep=True)
    selected = (domain.SDMVSTRA == 134) & (domain.SDMVPSU == 1)
    domain.loc[selected, "RIDAGEYR"] = 0
    domain_result = calculate(domain)
    compare(domain_result, independent_result(domain))
    compare(domain_result, {"records": 9254, "psus": 30, "adult_psus": 29,
                            "adult_strata": 15, "design_df": 14})
    mutations = [("WTINT2YR", 0), ("RIDAGEYR", np.nan), ("RIDAGEYR", 20.5),
                 ("RIDAGEYR", 81), ("SDDSRVYR", 9), ("SEQN", source.SEQN.iloc[1]),
                 ("SDMVPSU", 3), ("SDMVSTRA", 999)]
    for name, value in mutations:
        invalid = source.copy(deep=True)
        invalid.loc[invalid.index[0], name] = value
        try:
            calculate(invalid)
        except ValueError:
            continue
        raise AssertionError("Hatalı girdi kabul edildi: " + name)
    empty_domain = source.copy(deep=True)
    empty_domain["RIDAGEYR"] = 0
    try:
        calculate(empty_domain)
    except ValueError:
        pass
    else:
        raise AssertionError("Boş alt evren kabul edildi")
    pd.testing.assert_frame_equal(source, untouched)
    return {
        "numeric_check_pass": True, "independent_covariance_check": True,
        "row_order_invariance": True, "weight_scale_invariance": True,
        "domain_psus_and_df_checked": True, "invalid_inputs_rejected": len(mutations),
        "empty_domain_rejected": True, "source_unchanged": True,
        "reader_is_shared": True, "survey_software_crosscheck": False,
        "complete_delivery_accepted": False,
        "result": result,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))