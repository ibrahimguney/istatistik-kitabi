# B08 — Güven aralıkları

**Yerel hazırlık:** 9 Eylül 2026. Ders sürümü Bölüm 8; kapsamlı sürüm Bölüm 8.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Özet istatistiklerden evren ortalaması için iki taraflı t güven aralığı kurmak.
- Güven düzeyi, kritik değer, standart hata, hata payı ve tam genişliği ayırmak.
- Yüzde 95 ile yüzde 99 aralıklarının neden farklı genişlikte olduğunu açıklamak.
- Ham gözlem olmadan dağılım ve aykırı değer denetiminin yapılamayacağını görmek.

[Örnek 01](ornek-01/README.md), kitaptaki Python/R uygulamasının
**n=25, ortalama=72, s=10** özetini kullanır. Dosya tek özet satırıdır;
25 gözlem veya üç kişilik ham veri değildir. Yeni gözlemler uydurulmaz.
Bu pilot ortalamanın t aralığına odaklanır; `companion/spss` içindeki
395 not kaydına dayalı ortalama/Wilson oran aralıkları ayrı bir uygulamadır.

| İçerik | Dosya |
|---|---|
| Ortak özet ve veri sözlüğü | `ornek-01/veri.csv`, `ornek-01/veri-sozlugu.csv` |
| Kaynak ve kontrol yöntemi | `ornek-01/kaynak-kaydi.json` |
| Python / R çözümleri | `ornek-01/cozum.py`, `ornek-01/cozum.R` |
| SPSS ve metin yedeği | `ornek-01/analiz.sps`, `ornek-01/analiz.sps.txt` |
| 19 sayısal kontrol | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [grafik açıklaması](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtları | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b08/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünden ilk komut `cd bolumler/b08/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
kullanılır. SPSS adımları örneğin README'sindedir.

## Durum

Python'da 19 kontrol geçti ve iki güven aralığını karşılaştıran grafik
üretildi. Kritik değerler ayrıca t yoğunluğunu sayısal integral ve kök
bulma ile tersleyerek denetlendi. R/SPSS bu ortamda çalıştırılmadı.
Rastgele işlem, benzetim veya tohum yoktur; üç yazılım aynı özetten aynı
aralıkları hesaplamak üzere hazırlanmıştır. Kaynak veri değişmez; grafik
seçeneği yalnız ilgili PNG'yi oluşturur veya yeniler.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Yayın koşulları toplu
hazırlık sonunda belirlenecek; açık lisans kendiliğinden atanmadı.