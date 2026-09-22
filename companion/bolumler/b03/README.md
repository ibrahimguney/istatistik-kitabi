# B03 — Betimsel istatistik

**Yerel hazırlık:** 9 Eylül 2026. Ders sürümü Bölüm 3; kapsamlı sürüm Bölüm 3.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Ortalama, medyan ve örneklem standart sapmasını birlikte yorumlamak.
- Çeyrekleri aynı yöntemle hesaplamak; IQR ve aykırı değer sınırlarını bulmak.
- Histogram sınıflarını, kutu sınırlarını ve bıyıkları doğru okumak.
- Uç gözlemi silmeden duyarlılık karşılaştırması yapmak.

## Örnek ve kapsam

[Örnek 01](ornek-01/README.md), kitaptaki Python ve R bloklarında bulunan
**2, 3, 3, 4, 13 saat** verisini ortak CSV'den okur. Beş satır yapay öğretim
gözlemidir; gerçek öğrencilerin kayıtları değildir. `companion/spss`
altındaki gerçek veri uygulamasıyla aynı veri veya aynı analiz değildir.
Ek veri indirme ya da başka bölümlerin dosyaları gerekmez.

| İçerik | Dosya |
|---|---|
| Ortak veri ve sözlük | `ornek-01/veri.csv`, `ornek-01/veri-sozlugu.csv` |
| Python / R çözümü | `ornek-01/cozum.py`, `ornek-01/cozum.R` |
| SPSS sözdizimi ve metin yedeği | `ornek-01/analiz.sps`, `ornek-01/analiz.sps.txt` |
| 26 sayısal kontrol değeri | `ornek-01/beklenen-sonuclar.csv` |
| Adım adım çözüm | [Örnek çözümü](ornek-01/cozum.md) |
| Histogram ve kutu grafiği açıklaması | [Grafik rehberi](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtları | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Test kapsamı ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b03/ornek-01
python cozum.py --check --grafik
```

Gelecekte yalnız eşlikçi paketin yayımlandığı depo kökünden ilk komut
`cd bolumler/b03/ornek-01` olacaktır. R kurulumu olan bilgisayarda aynı
örnek klasöründe `Rscript cozum.R --check --grafik` kullanılır.
SPSS için çalışma dizini ve çıktı okuma adımları örneğin README'sindedir.

## Sonuç ve doğrulama sınırı

Ortalama 5, medyan 3, örneklem varyansı 20,5; Q1=3, Q3=4 ve IQR=1.
Python'da 26 kontrol geçti ve iki panelli grafik üretildi. R/SPSS kaynakları
hazırdır fakat bu ortamda yorumlayıcıları bulunmadığından çalıştırılmadı.
Python kontrolünün geçmesi üç yazılımı uçtan uca doğrulamaz.

Kodların temel örneği yalnız okuma yapar. `--grafik` seçeneği ilgili dilin
`ciktilar/` altındaki PNG'sini oluşturur veya yeniler; CSV'yi değiştirmez.
Kullanım koşulları toplu yayın öncesinde belirlenecek; bu hazırlıkla yeni
bir açık lisans, ZIP veya GitHub yayını oluşturulmadı.