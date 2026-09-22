# B12 — Kategorik veriler ve ki-kare bağımsızlık testi

**Yerel paket.** Ders sürümü Bölüm 12; kapsamlı sürüm Bölüm 13.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Hücre frekansı, satır yüzdesi ve toplam yüzdesini ayırmak.
- Bağımsızlık altında beklenen frekansları ve Pearson hücre katkılarını hesaplamak.
- Düzeltmesiz Pearson testi, Pearson artığı ve Cramér V'yi yorumlamak.
- Sayısal koşulların bağımsız gözlem ve uygun örnekleme tasarımı yerine geçmediğini görmek.

[Örnek 01](ornek-01/README.md), kitaptaki Python/R tablosunu kullanır:

| Grup | Başarılı | Başarısız | Toplam |
|---|---:|---:|---:|
| Birinci | 30 | 10 | 40 |
| İkinci | 20 | 20 | 40 |
| Toplam | 50 | 30 | 80 |

CSV'nin dört satırı **dört hücreyi**, frekansların toplamı 80 gözlemi
ifade eder. Bireysel öğrenci kayıtları uydurulmaz. Kitabın 395 öğrenci
notlu SPSS örneği ayrı bir gerçek veri uygulamasıdır; bu pilot onu gerektirmez.

| İçerik | Dosya |
|---|---|
| Ortak frekans tablosu | `ornek-01/veri.csv` |
| Veri sözlüğü ve kaynak | `ornek-01/veri-sozlugu.csv`, `ornek-01/kaynak-kaydi.json` |
| Python / R / SPSS | `ornek-01/cozum.py`, `ornek-01/cozum.R`, `ornek-01/analiz.sps` |
| SPSS metin yedeği | `ornek-01/analiz.sps.txt` |
| 32 kontrol değeri | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [grafik açıklaması](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtlar | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b12/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünde ilk komut `cd bolumler/b12/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
kullanılır. SPSS adımları örneğin README'sindedir.

## Durum ve kapsam

Python'da 32 sayısal kontrol geçti; satır yüzdeleri ve Pearson artıkları
grafiği üretildi. R/SPSS bu ortamda çalıştırılmadı. Rastgele işlem veya
tohum yoktur; hesap asimptotik ki-kare dağılımını kullanır, kesin test değildir.
Bu pilot 2×2 tablo, sabit α=0,05 ve tüm beklenen frekanslar en az 5 koşuluyla
sınırlıdır. Uyum iyiliği, Fisher ve McNemar ayrı yöntemler olarak tartışılır;
burada çalıştırılmış ek analizler değildir.

Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Yayın koşulları toplu
hazırlık sonunda belirlenecek; kendiliğinden açık lisans atanmadı.