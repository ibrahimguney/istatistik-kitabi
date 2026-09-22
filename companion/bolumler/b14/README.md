# B14 — Genel sınava hazırlık

**Yerel paket.** Ders sürümü Bölüm 14; kapsamlı sürüm Bölüm 17.
Bu, ders sürümünün son bölüm paketidir; bütün yayın hazırlıklarının
bittiği anlamına gelmez. B05 dosyalarının bu çalışma kopyasında eksik oluşu,
üç kapsamlı sürüm ek paketi ve R/SPSS çalıştırma kontrolleri ayrıca bekliyor.
GitHub yüklemesi toplu hazırlık tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Araştırma hedefi, değişken türü ve gözlem ilişkisine göre yöntem seçmek.
- Eşleştirilmiş farkı yönü, belirsizliği ve etki büyüklüğüyle raporlamak.
- Yazılımın sayısal kontrolüyle yöntem gerekçesini birbirinden ayırmak.
- Tahmin, test, ilişki ve nedensellik sorularını bir sınav yanıtında doğru konumlandırmak.

[Örnek 01](ornek-01/README.md), kitabın aynı 24 öğrencide son−ön farkı
örneğini kullanır: ortalama fark −3,2 puan, farkların standart sapması 6,
çift yönlü α=0,05. Tek CSV satırı bir **özet**tir; 24 ham fark veya 48
bireysel ölçüm uydurulmaz. Kitabın 395 kayıtlı SPSS genel uygulaması ve
sıfır puan duyarlılık analizi ayrı örneklerdir; bu pilot onları çalıştırmaz.

| İçerik | Dosya |
|---|---|
| Ortak özet, sözlük, kaynak | `ornek-01/veri.csv`, `ornek-01/veri-sozlugu.csv`, `ornek-01/kaynak-kaydi.json` |
| Python / R / SPSS | `ornek-01/cozum.py`, `ornek-01/cozum.R`, `ornek-01/analiz.sps` |
| SPSS metin yedeği | `ornek-01/analiz.sps.txt` |
| 17 sayısal kontrol | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [grafik açıklaması](ornek-01/grafik-aciklamasi.md) |
| Yöntem seçimi ve yanıt şablonu | [Sınav rehberi](sinav-rehberi.md) |
| 12 karma alıştırma ve yanıtlar | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b14/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünde ilk komut `cd bolumler/b14/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
kullanılır. SPSS adımları örneğin README'sindedir.

## Durum

Python'da 17 sayısal kontrol geçti; fark aralığı grafiği üretildi.
R/SPSS bu ortamda çalıştırılmadı. Sınav rehberi ve karma alıştırmalar
pedagojik kaynaklardır; 17 kontrol bütün yöntemleri test eden bir sistem
veya sınav yanıtlarını otomatik puanlayan bir araç değildir.
Rastgele işlem/tohum yoktur. Yeni ZIP, commit veya GitHub yüklemesi yapılmadı;
yayın koşulları ayrıca belirlenecek, kendiliğinden açık lisans atanmadı.