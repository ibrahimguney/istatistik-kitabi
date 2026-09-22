# B04 — Örnekleme dağılımları

**Yerel hazırlık:** 9 Eylül 2026. Ders sürümü Bölüm 4; kapsamlı sürüm Bölüm 4.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Evren dağılımını, tek bir örneklemi ve örnekleme dağılımını ayırmak.
- Geri koymalı iki bağımsız çekimin bütün sıralı sonuçlarını oluşturmak.
- Örneklem ortalamasının beklenen değerini, varyansını ve standart hatasını bulmak.
- Tam olasılık dağılımıyla benzetim çıktısının neden farklı bölenler kullandığını açıklamak.

## Seçilen örnek

[Örnek 01](ornek-01/README.md), kitabın Bölüm 4 **R uygulamasındaki**
{2,4,6,8} yapay evrenini temel alır. Her değer 1/4 olasılıkla çekilir;
geri koymalı iki bağımsız çekimin 16 sıralı sonucu eksiksiz listelenir.
Python/R aynı listeyi evren dosyasından yeniden oluşturup ortak CSV ile
karşılaştırır; SPSS ortak 16 satırlık CSV'yi analiz eder.

Bu örnek, bölümün Python kutusundaki normal evrenden 5000 tekrarlı
benzetim **değildir**. `companion/spss` içindeki gerçek matematik notlarından
2000 tekrarlı uygulama da ayrı bir örnektir. Üçünün veri ve çıktıları
birbirine karıştırılmaz. B04 pilotu dış veri ve rastgele sayı gerektirmez.

## İçindekiler

| İçerik | Dosya |
|---|---|
| Yapay evren ve bütün sıralı sonuçlar | `ornek-01/evren.csv`, `ornek-01/veri.csv` |
| Veri sözlüğü | `ornek-01/veri-sozlugu.csv` |
| Python / R | `ornek-01/cozum.py`, `ornek-01/cozum.R` |
| SPSS ve metin yedeği | `ornek-01/analiz.sps`, `ornek-01/analiz.sps.txt` |
| 28 kontrol değeri | `ornek-01/beklenen-sonuclar.csv` |
| Adım adım çözüm | [Örnek çözümü](ornek-01/cozum.md) |
| Dağılım grafiği | [Grafik açıklaması](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtları | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Kontrol kapsamı ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b04/ornek-01
python cozum.py --check --grafik
```

Gelecekte yalnız eşlikçi dosyaların bulunduğu depo kökünden ilk komut
`cd bolumler/b04/ornek-01` olur. R kurulu bilgisayarda aynı örnek klasöründe
`Rscript cozum.R --check --grafik` kullanılır. SPSS adımları örneğin README'sindedir.

## Durum

Python'da 28 sayısal kontrol geçti ve karşılaştırma grafiği üretildi.
R/SPSS betikleri hazır, ancak bu ortamda çalıştırılmadı. Bekleyen kontroller
`DOGRULAMA.md` içinde açıkça ayrıldı. Kaynak CSV'ler değiştirilmez;
`--grafik` yalnız ilgili dilin PNG'sini oluşturur veya yeniler.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Kullanım koşulları toplu
yayın öncesinde belirlenecek; kendiliğinden açık lisans atanmadı.