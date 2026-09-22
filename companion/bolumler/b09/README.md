# B09 — Hipotez testleri

**Yerel paket.** Ders sürümü Bölüm 9; kapsamlı sürüm Bölüm 10.
Kapsamlı sürümde araya giren bootstrap bölümü bu paketin konusu değildir.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Bir fark tahmini, standart hatası ve serbestlik derecesinden t istatistiğini hesaplamak.
- Çift yönlü ve önceden belirlenmiş tek yönlü alternatifleri ayırmak.
- p-değeri, anlamlılık düzeyi ve güven aralığı arasındaki ilişkiyi açıklamak.
- İstatistiksel anlamlılığı pratik önemden ve H0'ın doğru olma olasılığından ayırmak.

[Örnek 01](ornek-01/README.md), kitaptaki Python/R örneğinin
**fark=2,1, standart hata=1, serbestlik=49** özetini kullanır.
Ana test H0: δ=0, H1: δ≠0 ve α=0,05 içindir. Tek satır bir özet kaydıdır;
ham gözlem değildir. Serbestlik derecesinden tek başına örneklem büyüklüğü
veya araştırma deseni çıkarılmaz; gözlem uydurulmaz. Kitabın SPSS bölümündeki
395 öğrenci notunun 10 ile karşılaştırılması ayrı bir gerçek veri uygulamasıdır.

| İçerik | Dosya |
|---|---|
| Ortak özet ve veri sözlüğü | `ornek-01/veri.csv`, `ornek-01/veri-sozlugu.csv` |
| Kaynak ve kontrol yöntemi | `ornek-01/kaynak-kaydi.json` |
| Python / R çözümleri | `ornek-01/cozum.py`, `ornek-01/cozum.R` |
| SPSS ve metin yedeği | `ornek-01/analiz.sps`, `ornek-01/analiz.sps.txt` |
| 20 sayısal kontrol | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [grafik açıklaması](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtları | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b09/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünden ilk komut `cd bolumler/b09/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
kullanılır. SPSS adımları örneğin README'sindedir.

## Durum

Python'da 20 kontrol geçti; iki panelli test/güven aralığı grafiği üretildi.
Kuyruk olasılığı ve kritik değer ayrıca açık t yoğunluğunun sayısal integrali
ve kök bulma ile doğrulandı. R/SPSS bu ortamda çalıştırılmadı.
Rastgele işlem veya tohum yoktur. Kaynak CSV değiştirilmez; `--grafik`
yalnız ilgili çıktı PNG'sini oluşturur veya yeniler.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Yayın koşulları toplu
hazırlık sonunda belirlenecek; kendiliğinden açık lisans atanmadı.