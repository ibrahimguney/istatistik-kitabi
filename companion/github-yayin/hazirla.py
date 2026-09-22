from pathlib import Path
import hashlib
import re
import subprocess
import sys
import tempfile
import zipfile


def manifest(dosyalar):
    return "".join(
        hashlib.sha256(icerik).hexdigest() + "  " + ad + "\n"
        for ad, icerik in sorted(dosyalar.items())
    ).encode("utf-8")


def arsiv_yaz(hedef, dosyalar):
    with zipfile.ZipFile(hedef, "w", compression=zipfile.ZIP_DEFLATED) as arsiv:
        for ad, icerik in sorted(dosyalar.items()):
            arsiv.writestr(ad, icerik)


def main():
    betik_dizini = Path(__file__).parent
    companion = betik_dizini.parent
    kaynak = companion / "bolumler" / "b01"
    spss = (kaynak / "ornek-01" / "analiz.sps.txt").read_bytes()
    (kaynak / "ornek-01" / "analiz.sps").write_bytes(spss)
    adlar = [
        "README.md", "DOGRULAMA.md", "alistirmalar.md", "cozumler.md",
        "ornek-01/README.md", "ornek-01/cozum.md", "ornek-01/veri.csv",
        "ornek-01/veri-sozlugu.csv", "ornek-01/beklenen-sonuclar.csv",
        "ornek-01/cozum.py", "ornek-01/cozum.R", "ornek-01/analiz.sps",
    ]
    yerel = {ad: (kaynak / ad).read_bytes() for ad in adlar}
    yerel["MANIFEST.sha256"] = manifest(yerel)
    (kaynak / "MANIFEST.sha256").write_bytes(yerel["MANIFEST.sha256"])
    yayin = dict(yerel)
    for ad in ["ornek-01/README.md"]:
        yayin[ad] = yayin[ad].replace(
            b"companion/bolumler/b01/ornek-01", b"bolumler/b01/ornek-01"
        ).replace("Kitap projesinin".encode(), "GitHub deposunun".encode()).replace(
            "kitap projesinin".encode(), "GitHub deposunun".encode()
        )
    yayin["README.md"] = yayin["README.md"].replace(
        "Paket yerel pilottur; GitHub'a yüklenmemiştir.".encode(),
        "Bu paket B01 pilot sürümüdür.".encode(),
    )
    yayin["DOGRULAMA.md"] = yayin["DOGRULAMA.md"].replace(
        "3. GitHub yayını öncesinde depo adresi ve kullanım koşullarını belirleyin.".encode(),
        "3. Kamuya açık kullanım koşullarını yazarla netleştirin.".encode(),
    )
    yayin.pop("MANIFEST.sha256")
    yayin["MANIFEST.sha256"] = manifest(yayin)
    depo = {"bolumler/b01/" + ad: icerik for ad, icerik in yayin.items()}
    depo["README.md"] = (betik_dizini / "DEPO-README.md").read_bytes()
    with tempfile.TemporaryDirectory(prefix="b01-yayin-kontrol-", dir=companion) as gecici:
        dizin = Path(gecici)
        for ad, icerik in depo.items():
            hedef = dizin / ad
            hedef.parent.mkdir(parents=True, exist_ok=True)
            hedef.write_bytes(icerik)
        for belge in dizin.rglob("*.md"):
            for baglanti in re.findall(r"\]\(([^)]+)\)", belge.read_text()):
                if not baglanti.startswith(("http:", "https:", "#")):
                    if not (belge.parent / baglanti).exists():
                        raise ValueError(f"Eksik baglanti: {belge.name}: {baglanti}")
        subprocess.run(
            [sys.executable, "cozum.py", "--check"],
            cwd=dizin / "bolumler" / "b01" / "ornek-01", check=True,
        )
    arsiv_yaz(companion / "b01-uygulama-paketi.zip",
              {"b01/" + ad: icerik for ad, icerik in yerel.items()})
    arsiv_yaz(companion / "istatistik-uygulamalari-b01.zip", depo)
    print("Yerel paketler hazir. GitHub'a yukleme yapilmadi.")


if __name__ == "__main__":
    main()