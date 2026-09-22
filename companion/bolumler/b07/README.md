# B07 — Nokta tahmini

**Yerel hazırlık:** 9 Eylül 2026. Ders sürümü Bölüm 7; kapsamlı sürüm Bölüm 7.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Parametre, tahmin edici ve gerçekleşmiş tahmini ayırmak.
- İkili yanıtlardan oran ve yerine-koyma yöntemiyle yaklaşık standart hata bulmak.
- Bernoulli örneklem oranının merkezini, yanlılığını ve MSE'sini incelemek.
- Ampirik standart sapmada B−1 ile ampirik MSE ayrışımında B bölenlerini karıştırmamak.

[Örnek 01](ornek-01/README.md), kitabın Bölüm 7 Python/R uygulamalarını
ortak dosyalara taşır. İki ayrı veri vardır: on yapay ikili yanıt ve p=0,40,
n=50 modelinden 10000 tekrarlı benzetim. İlk verinin bilinmeyen gerçek oranı
benzetimin p=0,40 parametresiyle özdeşleştirilmez. `companion/spss` içindeki
395 gerçek not kaydı üzerinden yapılan uygulama bu pilotun parçası değildir.

| İçerik | Dosya |
|---|---|
| On ikili yanıt | `ornek-01/veri.csv` |
| Ortak benzetim başarı sayıları | `ornek-01/benzetim.csv` |
| Sözlük ve üretim kaydı | `ornek-01/veri-sozlugu.csv`, `ornek-01/uretim-kaydi.json` |
| Python yeniden üretimi | `ornek-01/uret.py` |
| Ortak veriden Python / R çözümü | `ornek-01/cozum.py`, `ornek-01/cozum.R` |
| R'nin kendi üreteciyle benzetim | `ornek-01/benzetim.R` |
| SPSS ve metin yedeği | `ornek-01/analiz.sps`, `ornek-01/analiz.sps.txt` |
| 21 kontrol değeri | `ornek-01/beklenen-sonuclar.csv` |
| Çözüm ve grafik | [Açıklamalı çözüm](ornek-01/cozum.md), [grafik açıklaması](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtları | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b07/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünden ilk komut `cd bolumler/b07/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
ortak veriyi çözer. `Rscript benzetim.R` ise farklı rastgele sayılarla yeni
benzetim yapar; ortak referansla birebir eşleşmesi beklenmez.

## Durum

Python'da 21 sayısal kontrol geçti ve grafik üretildi. MSE ayrışımı ayrıca
kesir aritmetiğiyle doğrulandı. R/SPSS betikleri bu ortamda çalıştırılmadı.
Kaynak CSV'ler normal analizde değiştirilmez. Yeni ZIP, commit veya GitHub
yüklemesi yapılmadı; yayın koşulları toplu hazırlık sonunda belirlenecek,
açık lisans kendiliğinden atanmadı.