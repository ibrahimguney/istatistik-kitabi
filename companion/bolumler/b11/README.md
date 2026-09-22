# B11 — Bağımsız ve eşleştirilmiş örneklem t testleri

**Yerel paket.** Ders sürümü Bölüm 11; kapsamlı sürüm Bölüm 12.
GitHub yüklemesi bütün bölüm paketleri tamamlandıktan sonra yapılacak.

## Öğrenme hedefleri

- Araştırma desenine göre bağımsız ve eşleştirilmiş karşılaştırmayı ayırmak.
- Özetlerden Welch t testi ve kesirli serbestlik derecesini hesaplamak.
- Kişi bazlı farkların özetiyle eşleştirilmiş t testi ve d_z hesaplamak.
- Fark yönünün t, etki büyüklüğü ve güven aralığına etkisini açıklamak.

[Örnek 01](ornek-01/README.md), kitabın Python/R uygulamalarındaki iki
**ayrı** öğretim örneğini kullanır:

- Bağımsız gruplar: n₁=30, ortalama₁=78, s₁=8; n₂=28, ortalama₂=72, s₂=10.
  Fark yönü Grup 1 eksi Grup 2'dir.
- Eşleştirilmiş örnek: 20 tam çift; son−ön fark ortalaması=4,2,
  farkların standart sapması=5. Bu çiftler ilk iki grubun eşleştirilmesi değildir.

`veri.csv` tek geniş özet satırıdır; 58 bağımsız veya 20 eşleşmiş ham kayıt
üretilmez. İki test de sıfır farkı çift yönlü, α=0,05 ile sınar. Tek satır,
tek öğrenci anlamına gelmez. Spector verisi ve kitabın 395 öğrenci notlu
SPSS uygulaması ayrı örneklerdir; bu pilot onları gerektirmez.

| İçerik | Dosya |
|---|---|
| Ortak özet, sözlük, kaynak | `ornek-01/veri.csv`, `ornek-01/veri-sozlugu.csv`, `ornek-01/kaynak-kaydi.json` |
| Python / R / SPSS | `ornek-01/cozum.py`, `ornek-01/cozum.R`, `ornek-01/analiz.sps` |
| SPSS metin yedeği | `ornek-01/analiz.sps.txt` |
| 34 kontrol değeri | `ornek-01/beklenen-sonuclar.csv` |
| Açıklamalı çözüm ve grafik | [Çözüm](ornek-01/cozum.md), [grafik açıklaması](ornek-01/grafik-aciklamasi.md) |
| 12 alıştırma ve yanıtlar | [Sorular](alistirmalar.md), [çözümler](cozumler.md) |
| Doğrulama ve bütünlük | [Doğrulama](DOGRULAMA.md), `MANIFEST.json` |

## Hızlı başlangıç

Kitap proje kökünden:

```bash
cd companion/bolumler/b11/ornek-01
python cozum.py --check --grafik
```

Bağımsız eşlikçi depo kökünde ilk komut `cd bolumler/b11/ornek-01` olur.
R kurulu bilgisayarda aynı klasörde `Rscript cozum.R --check --grafik`
kullanılır. SPSS adımları örneğin README'sindedir.

## Durum

Python'da 34 sayısal kontrol geçti; iki ayrı fark aralığının grafiği üretildi.
R/SPSS bu ortamda çalıştırılmadı. Rastgele işlem veya tohum yoktur.
Ham gözlemler olmadığından dağılım, aykırı değerler ve eşleşme doğruluğu
bu paketle denetlenemez. Yeni ZIP, commit veya GitHub yüklemesi yapılmadı;
yayın koşulları toplu hazırlık sonunda belirlenecek, açık lisans kendiliğinden atanmadı.