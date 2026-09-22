# B13 — Korelasyon ve basit doğrusal regresyon

**Yerel paket.** Ders sürümü Bölüm 13; kapsamlı sürüm Bölüm 14.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Pearson korelasyonu, regresyon eğimi ve R²'yi farklı nicelikler olarak yorumlamak.
- Sabit terimli doğrusal modelde katsayı aralıkları, tahminler ve artıkları hesaplamak.
- Ortalama yanıt güven aralığı ile yeni birey öngörü aralığını ayırmak.
- Saçılım, artık ve Q-Q grafikleriyle model koşullarını tartışmak; nedensellik ve dışa taşırmadan kaçınmak.

[Örnek 01](ornek-01/README.md), kitaptaki 16 satırlık çalışma saati/son test
öğretim verisini ortak CSV'ye taşır. Her satırın iki ölçümü birlikte tutulur.
Model `puan ~ saat` ve sabit terim içerir; yeni öngörü noktası 6 saat,
aralık düzeyi %95'tir. Gözlenen çalışma süreleri 2–8 saattir.
Kitabın 395 öğrenci notlu SPSS örneği ayrı bir gerçek veri uygulamasıdır;
bu pilot onu gerektirmez.

| İçerik | Dosya |
|---|---|
| Ortak veri, sözlük, kaynak | `ornek-01/veri.csv`, `ornek-01/veri-sozlugu.csv`, `ornek-01/kaynak-kaydi.json` |
| Python / R / SPSS | `ornek-01/cozum.py`, `ornek-01/cozum.R`, `ornek-01/analiz.sps` |
| SPSS metin yedeği | `ornek-01/analiz.sps.txt` |
| 62 kontrol değeri | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [tanı grafikleri](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtlar | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b13/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünde ilk komut `cd bolumler/b13/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
kullanılır. SPSS adımları örneğin README'sindedir.

## Durum

Python'da 62 kontrol geçti; dört panelli grafik üretildi. Çok küçük
p-değeri ayrı bağıl toleransla denetlendi; sıfır yazılması kontrolü geçmez.
R/SPSS bu ortamda çalıştırılmadı. Rastgele işlem veya tohum yoktur.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı; yayın koşulları toplu
hazırlık sonunda belirlenecek, kendiliğinden açık lisans atanmadı.