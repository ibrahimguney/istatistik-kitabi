"""V2 ilk küçük teslim: ZIP/XPT kaynağını salt okunur denetler."""

import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE = Path("prism-uploads/DEMO_J.zip")
ZIP_HASH = "59729eceecff56b43bce8ce512bb15a3ff47ae96db6914fd9807e19391de4861"
XPT_HASH = "c0b46e0345ea19404928656277c8b0d10b0cca348a9b2fe4fc3c67e8b7ee73ec"
COLUMNS = ["SEQN", "SDDSRVYR", "RIDAGEYR", "WTINT2YR", "SDMVSTRA", "SDMVPSU"]


def read_source():
    content = SOURCE.read_bytes()
    if hashlib.sha256(content).hexdigest() != ZIP_HASH:
        raise ValueError("ZIP referans hash'i uyuşmuyor; dosya değiştirilmedi")
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP CRC kontrolü geçmedi")
        if archive.namelist().count("DEMO_J.xpt") != 1:
            raise ValueError("Tek bir DEMO_J.xpt üyesi gerekli")
        raw = archive.read("DEMO_J.xpt")
    if len(raw) != 3412720 or hashlib.sha256(raw).hexdigest() != XPT_HASH:
        raise ValueError("XPT boyutu veya referans hash'i uyuşmuyor")
    return pd.read_sas(io.BytesIO(raw), format="xport")


def check_frame(source):
    if source.shape != (9254, 46) or not set(COLUMNS).issubset(source.columns):
        raise ValueError("Beklenen kaynak boyutu veya sütunları yok")
    data = source[COLUMNS].copy()
    if not np.isfinite(data.to_numpy()).all():
        raise ValueError("Seçili alanlarda eksik veya sonlu olmayan değer")
    normalized = {}
    for name in ["SEQN", "SDDSRVYR", "RIDAGEYR", "SDMVSTRA", "SDMVPSU"]:
        rounded = np.rint(data[name])
        if not np.allclose(data[name], rounded, rtol=0, atol=1e-10):
            raise ValueError("Tamsayı kod bekleniyor: " + name)
        normalized[name] = int((data[name] != rounded).sum())
        data[name] = rounded.astype(int)
    if not data.SEQN.is_unique:
        raise ValueError("Yinelenen SEQN")
    if not (data.SDDSRVYR == 10).all():
        raise ValueError("Beklenmeyen dönem kodu")
    if not data.RIDAGEYR.between(0, 80).all():
        raise ValueError("Yaş kodu 0–80 aralığında olmalı")
    if not (data.WTINT2YR > 0).all():
        raise ValueError("Sonlu pozitif görüşme ağırlığı gerekli")
    if set(data.SDMVSTRA) != set(range(134, 149)):
        raise ValueError("Varyans tabakaları uyuşmuyor")
    codes = data.groupby("SDMVSTRA").SDMVPSU.agg(set)
    if not all(group == {1, 2} for group in codes):
        raise ValueError("Her tabakada PSU 1 ve 2 gerekli")
    adults = data.RIDAGEYR >= 20
    older = data.RIDAGEYR >= 60
    adult_units = data.loc[adults, ["SDMVSTRA", "SDMVPSU"]].drop_duplicates()
    return {
        "source_check_pass": True,
        "zip_sha256": ZIP_HASH,
        "xpt_sha256": XPT_HASH,
        "source_shape": list(source.shape),
        "selected_fields": COLUMNS,
        "records": len(data),
        "adults": int(adults.sum()),
        "older": int(older.sum()),
        "strata": len(codes),
        "psus": len(data[["SDMVSTRA", "SDMVPSU"]].drop_duplicates()),
        "adult_strata": int(adult_units.SDMVSTRA.nunique()),
        "adult_psus": len(adult_units),
        "integer_codes_normalized_in_memory": normalized,
        "numeric_case_accepted": False,
        "files_written": False,
        "cross_session_persistence_verified": False,
    }


if __name__ == "__main__":
    print(json.dumps(check_frame(read_source()), ensure_ascii=False, indent=2))