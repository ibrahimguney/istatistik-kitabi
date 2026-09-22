# B06 — Örnekleme yöntemleri

**Yerel hazırlık:** 9 Eylül 2026. Ders sürümü Bölüm 6; kapsamlı sürüm Bölüm 6.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Basit rastgele seçim ile tabakalı seçimin tasarım farkını açıklamak.
- Örnekleme çerçevesi, dahil edilme olasılığı ve tasarım ağırlığını ayırmak.
- Kayıtlı seçim göstergesini seçilme olasılığıyla karıştırmamak.
- Ağırlık toplamının gerçek seçilen kişi sayısı olmadığını göstermek.

[Örnek 01](ornek-01/README.md), kitaptaki Python/R uygulamasının **12 kişilik
yapay çerçevesini** kullanır. Üç sınıfta dörder birim vardır. Basit seçimde
altı kişi; tabakalı seçimde her sınıftan iki kişi geri koymadan seçilir.
Gerçek öğrenciler veya kişisel veriler kullanılmaz. `companion/spss`
içindeki 395 gerçek kayıt üzerinden 40 kişilik seçim uygulaması ayrı örnektir.

| İçerik | Dosya |
|---|---|
| Ortak çerçeve ve seçim göstergeleri | `ornek-01/veri.csv` |
| Veri sözlüğü ve üretim kaydı | `ornek-01/veri-sozlugu.csv`, `ornek-01/uretim-kaydi.json` |
| Python yeniden üretimi | `ornek-01/uret.py` |
| Ortak veri için Python / R | `ornek-01/cozum.py`, `ornek-01/cozum.R` |
| R'nin kendi üreteciyle yeni seçim | `ornek-01/secim.R` |
| SPSS ve metin yedeği | `ornek-01/analiz.sps`, `ornek-01/analiz.sps.txt` |
| Seçilen kimlikleri de içeren 29 kontrol | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [seçim haritası](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtları | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b06/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünden ilk komut `cd bolumler/b06/ornek-01` olur.
R kurulu bilgisayarda `Rscript cozum.R --check --grafik` ortak veriyi çözer.
`Rscript secim.R` farklı bir seçim yapar; Python kimlikleriyle birebir
aynılık beklenmez. SPSS ve yeniden üretim ayrıntıları örneğin README'sindedir.

## Durum

Python'da 29 kontrol geçti ve seçim haritası üretildi. Bu kayıtlı basit
seçimde de sınıf frekansları 2/2/2 çıktı; bu durum basit rastgele seçimin
her zaman dengeli sınıf sayısı verdiği anlamına gelmez.
R/SPSS betikleri bu ortamda çalıştırılmadı. Kaynak CSV normal analizde
değiştirilmez. Yeni ZIP, commit veya GitHub yüklemesi yapılmadı; yayın
koşulları toplu hazırlık sonunda belirlenecek, açık lisans kendiliğinden atanmadı.