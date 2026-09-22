import argparse
from pathlib import Path
import platform

import numpy as np
import pandas as pd


def uret():
    rng = np.random.default_rng(2026)
    cekimler = rng.binomial(1, 0.40, size=(10000, 50))
    return pd.DataFrame({"tekrar": np.arange(1, 10001), "basari": cekimler.sum(axis=1)})


def main():
    parser = argparse.ArgumentParser(description="B07: ortak Bernoulli benzetimini yeniden uret")
    parser.add_argument("--cikti", default="yeniden-benzetim.csv")
    secenek = parser.parse_args()
    hedef = Path(secenek.cikti)
    if hedef.is_absolute() or ".." in hedef.parts:
        raise ValueError("Ornek klasoru icinde goreli bir cikti yolu gerekli.")
    with hedef.open("x", encoding="utf-8", newline="") as stream:
        uret().to_csv(stream, index=False, lineterminator="\n")
    print(f"Uretildi: {hedef}; PCG64, tohum=2026, p=0.40, n=50, tekrar=10000")
    print(f"Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}")


if __name__ == "__main__":
    main()