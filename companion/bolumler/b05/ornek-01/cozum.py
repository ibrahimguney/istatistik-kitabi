import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import statistics
import zipfile

HACIMLER = (1, 5, 30)
ALANLAR = ("tekrar", "ort1", "ort5", "ort30")
OLCULER = ("n", "B", "merkez", "ampirik_se",
           "kuramsal_se", "varyans", "sapma")

R_KODU = r'''
veri <- read.csv("veri.csv", check.names=FALSE)
stopifnot(identical(names(veri), c("tekrar","ort1","ort5","ort30")),
          nrow(veri)>1, all(vapply(veri,is.numeric,logical(1))),
          all(is.finite(as.matrix(veri))))
veri <- veri[order(veri$tekrar), ]
stopifnot(all(veri$tekrar==seq_len(nrow(veri))), all(veri[,-1]>=0))
olculer <- c("n","B","merkez","ampirik_se","kuramsal_se","varyans","sapma")
sonuc <- do.call(rbind,lapply(c(1,5,30),function(hacim) {
  degerler <- veri[[paste0("ort",hacim)]]
  data.frame(degisken=paste0("n",hacim),olcu=olculer,
    deger=c(hacim,nrow(veri),mean(degerler),sd(degerler),
            10/sqrt(hacim),100/hacim,mean(degerler)-10))
}))
sonuc <- rbind(sonuc,data.frame(degisken="ek",
  olcu=c("se25","se100","hacim_carpani"),deger=c(2,1,4)))
print(sonuc,row.names=FALSE,digits=12)
if ("--check" %in% commandArgs(TRUE)) {
  hedef <- read.csv("beklenen-sonuclar.csv")
  stopifnot(identical(names(hedef),names(sonuc)),
    identical(hedef$degisken,sonuc$degisken),
    identical(hedef$olcu,sonuc$olcu),is.numeric(hedef$deger),
    all(is.finite(hedef$deger)),
    all(abs(hedef$deger-sonuc$deger)<=pmax(1e-9,abs(hedef$deger)*1e-9)))
  cat("DOGRULANDI: 24 kontrol degeri eslesiyor.\n")
}
if ("--grafik" %in% commandArgs(TRUE)) {
  png("histogram-r.png",width=1500,height=500)
  par(mfrow=c(1,3))
  for (hacim in c(1,5,30)) {
    hist(veri[[paste0("ort",hacim)]],breaks=35,probability=TRUE,
         main=paste("n =",hacim),xlab="Orneklem ortalamasi")
    abline(v=10,col="blue",lwd=2)
  }
  dev.off()
}
sessionInfo()
'''

SPSS_KODU = r'''
SET DECIMAL=DOT.
GET DATA /TYPE=TXT /FILE='veri.csv' /ENCODING='UTF8'
 /ARRANGEMENT=DELIMITED /DELCASE=LINE /DELIMITERS="," /FIRSTCASE=2
 /VARIABLES=tekrar F8.0 ort1 F24.16 ort5 F24.16 ort30 F24.16.
WEIGHT OFF.
FILTER OFF.
SPLIT FILE OFF.
VARIABLE LEVEL tekrar (NOMINAL) ort1 ort5 ort30 (SCALE).
VARSTOCASES /MAKE ortalama FROM ort1 ort5 ort30
 /INDEX=sira /KEEP=tekrar /NULL=KEEP.
RECODE sira (1=1) (2=5) (3=30) INTO hacim.
SORT CASES BY hacim.
SPLIT FILE LAYERED BY hacim.
GRAPH /HISTOGRAM=ortalama.
SPLIT FILE OFF.
AGGREGATE OUTFILE=* /BREAK=hacim
 /tekrar_sayisi=N(ortalama) /merkez=MEAN(ortalama) /ampirik_se=SD(ortalama).
COMPUTE kuramsal_se=10/SQRT(hacim).
COMPUTE varyans=100/hacim.
COMPUTE sapma=merkez-10.
FORMATS merkez ampirik_se kuramsal_se varyans sapma (F18.10).
LIST hacim tekrar_sayisi merkez ampirik_se kuramsal_se varyans sapma.
COMPUTE se25=2.
COMPUTE se100=1.
COMPUTE hacim_carpani=4.
TEMPORARY.
SELECT IF hacim=1.
LIST se25 se100 hacim_carpani.
'''


def csv_yaz(yol, baslik, satirlar):
    with yol.open("w", encoding="utf-8", newline="") as dosya:
        yazici = csv.writer(dosya, lineterminator="\n")
        yazici.writerow(baslik)
        yazici.writerows(satirlar)


def oku(yol):
    with yol.open(encoding="utf-8", newline="") as dosya:
        okuyucu = csv.reader(dosya)
        if tuple(next(okuyucu, [])) != ALANLAR:
            raise ValueError("CSV sutunlari uyusmuyor.")
        satirlar = [tuple(map(float, satir)) for satir in okuyucu]
    if len(satirlar) < 2 or any(len(satir) != 4 for satir in satirlar):
        raise ValueError("En az iki tam satir gerekli.")
    if not all(math.isfinite(deger)
               for satir in satirlar for deger in satir):
        raise ValueError("Sonlu ve eksiksiz veri gerekli.")
    satirlar.sort()
    if any(satir[0] != sira
           for sira, satir in enumerate(satirlar, 1)):
        raise ValueError("Kimlikler benzersiz 1..B olmali.")
    if any(deger < 0 for satir in satirlar for deger in satir[1:]):
        raise ValueError("Ortalamalar negatif olamaz.")
    return satirlar


def hesapla(satirlar):
    sonuc = []
    for sutun, hacim in enumerate(HACIMLER, 1):
        degerler = [satir[sutun] for satir in satirlar]
        merkez = statistics.mean(degerler)
        degerler = (
            hacim, len(satirlar), merkez, statistics.stdev(degerler),
            10/math.sqrt(hacim), 100/hacim, merkez-10
        )
        sonuc.extend(
            (f"n{hacim}", olcu, deger)
            for olcu, deger in zip(OLCULER, degerler)
        )
    return sonuc + [
        ("ek", "se25", 2),
        ("ek", "se100", 1),
        ("ek", "hacim_carpani", 4)
    ]


def kontrol(sonuc, yol):
    with yol.open(encoding="utf-8", newline="") as dosya:
        okuyucu = csv.reader(dosya)
        if next(okuyucu, []) != ["degisken", "olcu", "deger"]:
            raise ValueError("Referans sutunlari uyusmuyor.")
        hedefler = list(okuyucu)
    if len(hedefler) != len(sonuc):
        raise ValueError("Referans satir sayisi farkli.")
    for gercek, hedef in zip(sonuc, hedefler):
        if len(hedef) != 3 or list(gercek[:2]) != hedef[:2]:
            raise ValueError("Referans etiketleri uyusmuyor.")
        deger = float(hedef[2])
        if not math.isfinite(deger) or not math.isclose(
                gercek[2], deger, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Referans degeri uyusmuyor.")
    print("DOGRULANDI: 24 kontrol degeri eslesiyor.")


def kur(hedef):
    if hedef.is_absolute() or ".." in hedef.parts or hedef == Path("."):
        raise ValueError("Goreli bir alt klasor secin.")
    if hedef.exists() or any(
            yol.is_symlink() for yol in (hedef, *hedef.parents)):
        raise ValueError(
            "Hedef mevcut veya sembolik baglanti; uzerine yazilmadi."
        )
    arsiv = hedef.with_name(hedef.name + "-paket.zip")
    if arsiv.exists():
        raise ValueError("ZIP zaten var; uzerine yazilmadi.")

    rng = random.Random(2026)
    sutunlar = [
        [
            math.fsum(
                rng.expovariate(0.1) for _ in range(hacim)
            ) / hacim
            for tekrar in range(10000)
        ]
        for hacim in HACIMLER
    ]
    satirlar = list(zip(range(1, 10001), *sutunlar))
    ornek = hedef / "ornek-01"
    hedef.mkdir(parents=True, exist_ok=False)
    ornek.mkdir()
    csv_yaz(ornek/"veri.csv", ALANLAR, satirlar)

    sonuc = []
    for hacim, degerler in zip(HACIMLER, sutunlar):
        merkez = math.fsum(degerler)/len(degerler)
        sapma = math.sqrt(
            math.fsum((deger-merkez)**2 for deger in degerler)
            / (len(degerler)-1)
        )
        degerler = (
            hacim, 10000, merkez, sapma,
            10/math.sqrt(hacim), 100/hacim, merkez-10
        )
        sonuc.extend(
            (f"n{hacim}", olcu, deger)
            for olcu, deger in zip(OLCULER, degerler)
        )
    sonuc += [
        ("ek", "se25", 2),
        ("ek", "se100", 1),
        ("ek", "hacim_carpani", 4)
    ]
    csv_yaz(
        ornek/"beklenen-sonuclar.csv",
        ("degisken", "olcu", "deger"), sonuc
    )
    kontrol(
        hesapla(oku(ornek/"veri.csv")),
        ornek/"beklenen-sonuclar.csv"
    )

    kaynak = Path(__file__).read_text(encoding="utf-8")
    (ornek/"cozum.py").write_text(kaynak, encoding="utf-8")
    (ornek/"cozum.R").write_text(R_KODU.lstrip(), encoding="utf-8")
    for ad in ("analiz.sps", "analiz.sps.txt"):
        (ornek/ad).write_text(SPSS_KODU.lstrip(), encoding="utf-8")

    csv_yaz(
        ornek/"veri-sozlugu.csv",
        ("degisken", "anlam", "olcek", "eksik_kurali"),
        [("tekrar", "Benzersiz tekrar kimligi",
          "nominal", "kabul edilmez")] +
        [
            (f"ort{hacim}", f"n={hacim} orneklem ortalamasi",
             "scale", "kabul edilmez")
            for hacim in HACIMLER
        ]
    )

    rehber = """# B05 — Merkezi limit teoremi ve standart hata

Bu yeni ogretim paketi ders/kapsamli surum Bolum 5 icindir.
Ustel evrenin ortalamasi ve standart sapmasi 10; n=1,5,30 ve B=10000.
Bir CSV satiri uc AYRI orneklemin ortalamalarini tasir; eslestirilmis veri degildir.
Bu betik Python random kullanir; onceki NumPy/R cekilislerinin aynisi DEGILDIR.
Tohum 2026; ham cekilisler degil ortalamalar saklanir. Gercek kisi verisi yoktur.

ornek-01 klasorunde:
- python cozum.py --check
- Rscript cozum.R --check --grafik
- SPSS calisma dizinini ayni klasor yapip analiz.sps calistirin.

Python ek paket gerektirmez. Grafik R/SPSS betiklerinde uretilir.
SPSS etkin veriyi degistirir; once acik calismanizi kaydedin.
SPSS temiz CSV icindir; Python/R girdi korumalarinin tumunu tekrarlamaz.
Iki LIST tablosunu kontrol CSV'siyle karsilastirin; yuvarlamayi dikkate alin.
Yeni paket icin python cozum.py --kur --hedef b05-yeni kullanilabilir.
Mevcut hedefin ve ZIP'in uzerine yazilmaz. Lisans atanmaz, GitHub'a yuklenmez.
"""
    (hedef/"README.md").write_text(rehber, encoding="utf-8")
    (ornek/"README.md").write_text(rehber, encoding="utf-8")

    yorum = """# Cozum ve yorum
E(ortalama)=10, Var(ortalama)=100/n, SE=10/sqrt(n).
Ampirik SE tekrar ortalamalarinin B-1 paydali standart sapmasidir.
Sapma sutunu tekrar merkezi eksi 10; kuramsal yanlilik kaniti degildir.
B artinca Monte Carlo oynakligi azalir; n sabitken hedef SE degismez.
n artinca ortalamalar daralir; ham ustel evren degismez.
n=30 her evren icin normallik garantisi degildir; bagimsizlik ve sonlu varyans gerekir.
Ayni CSV'nin ozetleri 1e-9 toleransla karsilastirilir; bu tolerans kuramsal hedefe uzaklik degildir.
Grafiklerin eksen olceklerini okuyun; panel genisligi tek basina yayilim olcusu degildir.
"""
    tablo = "\n| Degisken | Olcu | Deger |\n|---|---|---:|\n"
    tablo += "".join(
        f"| {ad} | {olcu} | {deger:.10g} |\n"
        for ad, olcu, deger in sonuc
    )
    (ornek/"cozum.md").write_text(yorum+tablo, encoding="utf-8")

    (hedef/"alistirmalar.md").write_text(
        "# Alistirmalar\n"
        "1. n=25/100 icin SE ve varyans?\n"
        "2. B dort katina cikarsa hedef SE?\n"
        "3. SE'yi yariya indirmek icin n?\n"
        "4. Ampirik sapma yanlilik kaniti mi?\n",
        encoding="utf-8"
    )
    (hedef/"cozumler.md").write_text(
        "# Yanitlar\n"
        "1. SE=2/1; varyans=4/1.\n"
        "2. Degismez; n sabit.\n"
        "3. n dort katina cikar.\n"
        "4. Hayir; sonlu benzetim sapmasidir.\n",
        encoding="utf-8"
    )
    kayit = {
        "python": platform.python_version(),
        "seed": 2026,
        "B": 10000,
        "hacimler": HACIMLER,
        "generator": "random.Random.expovariate(0.1)",
        "reference": "fsum/iki gecis varyans; cozum statistics.mean/stdev",
        "python_check": 24,
        "R_executed": False,
        "SPSS_executed": False
    }
    (ornek/"uretim-kaydi.json").write_text(
        json.dumps(kayit, indent=2), encoding="utf-8"
    )
    (hedef/"DOGRULAMA.md").write_text(
        "# Dogrulama\n"
        "Olusturma sirasinda 24 Python degeri eslesti.\n"
        "Referans fsum ile, cozum statistics ile hesaplandi.\n"
        "R/SPSS calistirilmadi; gercek ortamda kontrol edilmeli.\n"
        "Arayuz gorunurlugu ve kalicilik bu testle kanitlanmaz.\n",
        encoding="utf-8"
    )

    manifest = {
        str(yol.relative_to(hedef)):
        hashlib.sha256(yol.read_bytes()).hexdigest()
        for yol in sorted(hedef.rglob("*")) if yol.is_file()
    }
    (hedef/"MANIFEST.json").write_text(
        json.dumps({"algorithm": "SHA-256", "files": manifest}, indent=2),
        encoding="utf-8"
    )
    with zipfile.ZipFile(arsiv, "x", zipfile.ZIP_DEFLATED) as paket:
        for yol in sorted(hedef.rglob("*")):
            if yol.is_file():
                paket.write(
                    yol, str(Path("b05")/yol.relative_to(hedef))
                )
    print(f"OLUSTURULDU: {hedef}\nZIP: {arsiv}")


def main():
    parser = argparse.ArgumentParser(
        description="B05 olusturma ve Python cozumu"
    )
    secim = parser.add_mutually_exclusive_group(required=True)
    secim.add_argument("--kur", action="store_true")
    secim.add_argument("--check", action="store_true")
    parser.add_argument("--hedef", default="companion/bolumler/b05")
    args = parser.parse_args()
    if args.kur:
        kur(Path(args.hedef))
    else:
        ornek = Path(__file__).parent
        kontrol(
            hesapla(oku(ornek/"veri.csv")),
            ornek/"beklenen-sonuclar.csv"
        )


if __name__ == "__main__":
    main()