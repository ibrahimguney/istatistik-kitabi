# B10 — Tip I–Tip II hata, test gücü ve tek örneklem t testi

**Yerel paket.** Ders sürümü Bölüm 10; kapsamlı sürüm Bölüm 11.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Tek örneklemin özetinden t testi, güven aralığı ve Cohen d hesaplamak.
- Gözlenen örneklem standart sapması ile planlanan evren standart sapmasını ayırmak.
- Tip I hata, belirli bir alternatif altındaki Tip II hata ve gücü yorumlamak.
- İki ret bölgesini de içeren ileriye dönük güçten gerekli tam sayı hacmi bulmak.

[Örnek 01](ornek-01/README.md) iki ayrı dosya kullanır:

- `veri.csv`: Kitaptaki gözlenen özet; n=25, ortalama=55, s=10,
  referans=50, çift yönlü α=0,05.
- `plan.csv`: Yeni çalışma için önceden gerekçelendirilecek varsayımlar;
  n=34, gerçek fark=5, evren standart sapması=10, α=0,05, hedef güç=0,80.

İki dosyada sayıların benzeşmesi, planın gözlenen p-değerinden türetildiği
anlamına gelmez. Betikler planlama girdilerini test sonucundan kopyalamaz.
Her CSV tek özet/plan satırıdır; 25 veya 34 ham gözlem uydurulmaz.
Kitabın SPSS bölümündeki 395 öğrenci notu ve 1 puanlık hedef fark planı
bu küçük öğretim örneğinden ayrıdır.

| İçerik | Dosya |
|---|---|
| Ortak özet ve plan | `ornek-01/veri.csv`, `ornek-01/plan.csv` |
| Veri sözlüğü ve kaynak | `ornek-01/veri-sozlugu.csv`, `ornek-01/kaynak-kaydi.json` |
| Python / R / SPSS | `ornek-01/cozum.py`, `ornek-01/cozum.R`, `ornek-01/analiz.sps` |
| SPSS metin yedeği | `ornek-01/analiz.sps.txt` |
| 30 kontrol değeri | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [güç eğrisi](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtlar | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b10/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünden ilk komut `cd bolumler/b10/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
kullanılır. SPSS adımları örneğin README'sindedir.

## Durum ve sınırlar

Python'da 30 sayısal kontrol geçti; güç eğrisi üretildi. R/SPSS kodları
bu ortamda çalıştırılmadı. Rastgele işlem, benzetim veya tohum yoktur.
Hesaplar bağımsız normal gözlemler modeline dayanır; ham veri olmadığından
normallik/aykırı değer denetimi yapılmaz. Model dışı kümelenme ve kayıplar
planlanan 34 gözleme otomatik olarak dahil değildir.

Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Yayın koşulları toplu
hazırlık sonunda belirlenecek; kendiliğinden açık lisans atanmadı.