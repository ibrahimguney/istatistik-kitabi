import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version, PackageNotFoundError
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import subprocess
import sys


PAKETLER = [f"b{number:02}" for number in range(1, 15)] + [
    "bootstrap", "coklu-regresyon", "anova"
]


def ozet(icerik):
    return hashlib.sha256(icerik).hexdigest()


def hash_durumu(dosya, beklenen):
    if not dosya.is_file():
        return {"durum": "eksik"}
    icerik = dosya.read_bytes()
    hesaplanan = ozet(icerik)
    if hesaplanan == beklenen:
        return {"durum": "eslesiyor", "sha256": hesaplanan}
    try:
        icerik.decode("utf-8")
    except UnicodeDecodeError:
        return {"durum": "aciklanamayan_fark", "sha256": hesaplanan}
    adaylar = {
        "son_LF_eklenince_eslesiyor": icerik + b"\n",
        "CRLF_donusumuyle_eslesiyor": icerik.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"),
        "CRLF_ve_son_satirla_eslesiyor": (icerik.replace(b"\r\n", b"\n").rstrip(b"\n") + b"\n").replace(b"\n", b"\r\n"),
    }
    for durum, aday in adaylar.items():
        if ozet(aday) == beklenen:
            return {"durum": durum, "sha256": hesaplanan}
    return {"durum": "aciklanamayan_fark", "sha256": hesaplanan}


def manifest_yollari(dosyalar):
    sonuc = {}
    for kaynak_ad, beklenen in dosyalar.items():
        yol = PurePosixPath(kaynak_ad.replace("\\", "/"))
        ad = str(yol)
        if (yol.is_absolute() or ".." in yol.parts or ad == "." or
                ":" in ad or not isinstance(beklenen, str) or
                not re.fullmatch(r"[0-9a-f]{64}", beklenen)):
            raise ValueError(f"Gecersiz manifest girdisi: {kaynak_ad}")
        if ad in sonuc:
            raise ValueError(f"Yinelenen manifest yolu: {kaynak_ad}")
        sonuc[ad] = (kaynak_ad, beklenen)
    return sonuc


def paket_kontrol(kok, kod):
    dizin = kok / kod
    kayit = {"paket": kod, "mevcut": dizin.is_dir()}
    if not kayit["mevcut"]:
        return kayit
    ornek = dizin / "ornek-01"
    zorunlu = ["README.md", "DOGRULAMA.md", "alistirmalar.md", "cozumler.md"]
    zorunlu += ["ornek-01/" + ad for ad in (
        "README.md", "veri.csv", "veri-sozlugu.csv", "cozum.py", "cozum.R",
        "analiz.sps", "analiz.sps.txt", "beklenen-sonuclar.csv", "cozum.md"
    )]
    kayit["eksik_temel_dosyalar"] = [ad for ad in zorunlu if not (dizin / ad).is_file()]
    manifest = dizin / "MANIFEST.json"
    kayit["manifest"] = {"mevcut": manifest.is_file(), "dosyalar": {}}
    if manifest.is_file():
        try:
            belge = json.loads(manifest.read_text(encoding="utf-8"))
            if belge.get("algorithm") != "SHA-256" or not isinstance(belge.get("files"), dict):
                raise ValueError("Desteklenmeyen manifest bicimi")
            yollar = manifest_yollari(belge["files"])
            for ad, (kaynak_ad, beklenen) in yollar.items():
                durum = hash_durumu(dizin / ad, beklenen)
                durum["manifest_yolu"] = kaynak_ad
                durum["beklenen_sha256"] = beklenen
                if durum["durum"] == "eksik" and ad.endswith(".sps"):
                    durum["metin_yedegi"] = hash_durumu(dizin / (ad + ".txt"), beklenen)
                kayit["manifest"]["dosyalar"][ad] = durum
            kayit["manifest"]["listelenmeyen"] = sorted(
                dosya.relative_to(dizin).as_posix() for dosya in dizin.rglob("*")
                if dosya.is_file() and dosya != manifest and "__pycache__" not in dosya.parts
                and dosya.relative_to(dizin).as_posix() not in yollar
            )
        except (ValueError, TypeError, OSError) as hata:
            kayit["manifest"]["hata"] = str(hata)
    kayit["python_sozdizimi"] = []
    for dosya in sorted(dizin.rglob("*.py")):
        try:
            ast.parse(dosya.read_text(encoding="utf-8"), filename=str(dosya))
            durum = "gecti"
        except (SyntaxError, UnicodeError) as hata:
            durum = str(hata)
        kayit["python_sozdizimi"].append({"dosya": str(dosya.relative_to(dizin)), "durum": durum})
    ortam = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MPLBACKEND="Agg")
    try:
        sonuc = subprocess.run(
            [sys.executable, "-B", "cozum.py", "--check"], cwd=ornek,
            capture_output=True, text=True, timeout=120, env=ortam
        )
        eslesme = re.search(r"DOGRULANDI: (\d+) kontrol", sonuc.stdout)
        kayit["python"] = {
            "komut": "python -B cozum.py --check", "calisma_dizini": str(ornek),
            "cikis_kodu": sonuc.returncode,
            "gecti": sonuc.returncode == 0 and eslesme is not None,
            "kontrol_degeri_sayisi": int(eslesme.group(1)) if eslesme else 0,
            "stdout": sonuc.stdout, "stderr": sonuc.stderr
        }
    except (subprocess.TimeoutExpired, OSError) as hata:
        kayit["python"] = {"gecti": False, "hata": str(hata), "kontrol_degeri_sayisi": 0}
    spss, yedek = ornek / "analiz.sps", ornek / "analiz.sps.txt"
    kayit["spss_kopyalari_esit"] = (
        spss.read_bytes() == yedek.read_bytes() if spss.is_file() and yedek.is_file() else None
    )
    return kayit


def main():
    parser = argparse.ArgumentParser(description="17 bolum paketinin salt okunur Python ve manifest denetimi")
    parser.add_argument("--rapor", help="Yeni JSON raporu; mevcut dosyanin uzerine yazilmaz")
    secenek = parser.parse_args()
    hedef = Path(secenek.rapor) if secenek.rapor else None
    if hedef and (hedef.is_absolute() or ".." in hedef.parts or hedef.exists()):
        parser.error("Rapor yolu goreli ve yeni bir dosya olmali.")
    kok = Path(os.path.relpath(Path(__file__).parent))
    surumler = {"python": platform.python_version()}
    for paket in ["numpy", "pandas", "scipy", "matplotlib", "statsmodels"]:
        try:
            surumler[paket] = version(paket)
        except PackageNotFoundError:
            surumler[paket] = "bulunamadi"
    rapor = {
        "tarih_utc": datetime.now(timezone.utc).isoformat(),
        "kapsam": "17 bolum paketi; Python referanslari, AST ve MANIFEST.json. R/SPSS calistirilmaz.",
        "surumler": surumler,
        "yorumlayici_yolda_mevcut": {ad: shutil.which(ad) is not None for ad in ["Rscript", "spss", "pspp"]},
        "paketler": []
    }
    for kod in PAKETLER:
        kayit = paket_kontrol(kok, kod)
        rapor["paketler"].append(kayit)
        sonuc = kayit.get("python", {})
        print(f"{kod}: " + (f"Python {'GECTI' if sonuc.get('gecti') else 'BASARISIZ'}; {sonuc.get('kontrol_degeri_sayisi', 0)} deger" if kayit["mevcut"] else "PAKET EKSIK"), flush=True)
    mevcut = [kayit for kayit in rapor["paketler"] if kayit["mevcut"]]
    hashler = Counter(durum["durum"] for kayit in mevcut for durum in kayit["manifest"]["dosyalar"].values())
    rapor["ozet"] = {
        "beklenen_paket": len(PAKETLER), "mevcut_paket": len(mevcut),
        "eksik_paketler": [kayit["paket"] for kayit in rapor["paketler"] if not kayit["mevcut"]],
        "python_gecen": sum(kayit["python"]["gecti"] for kayit in mevcut),
        "eslesen_kontrol_degeri": sum(kayit["python"]["kontrol_degeri_sayisi"] for kayit in mevcut if kayit["python"]["gecti"]),
        "manifest_durumlari": dict(hashler)
    }
    basarili = len(mevcut) == len(PAKETLER) and all(
        kayit["python"]["gecti"] and not kayit["eksik_temel_dosyalar"]
        and kayit["spss_kopyalari_esit"] is True
        and kayit["manifest"]["mevcut"] and not kayit["manifest"].get("hata")
        and not kayit["manifest"].get("listelenmeyen")
        and all(durum["durum"] == "gecti" for durum in kayit["python_sozdizimi"])
        and all(durum["durum"] == "eslesiyor" for durum in kayit["manifest"]["dosyalar"].values())
        for kayit in mevcut
    )
    rapor["yerel_denetim_gecti"] = basarili
    if hedef:
        with hedef.open("x", encoding="utf-8") as dosya:
            json.dump(rapor, dosya, ensure_ascii=False, indent=2)
            dosya.write("\n")
    print(json.dumps(rapor["ozet"], ensure_ascii=False, indent=2))
    print("R/SPSS calistirma, bilimsel inceleme ve yayin izinleri bu denetimin disindadir.")
    return 0 if basarili else 1


if __name__ == "__main__":
    sys.exit(main())