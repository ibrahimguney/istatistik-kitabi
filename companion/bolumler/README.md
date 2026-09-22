# Bölüm bazlı uygulama paketleri

Bölümler yerelde sırayla hazırlanıyor. GitHub yüklemesi, ders sürümündeki
14 bölüm ve kapsamlı sürümün üç ek paketi tamamlandıktan sonra tek yayın
paketiyle yapılacak. Hedef depo: `ibrahimguney/istatistik-kitabi`.
Bölüm paketleri bu deponun `companion/bolumler/` dizininde yayımlanır.

## Son toplu kontrol — 10 Eylül 2026

17 paket mevcut; 545 Python referansı ve 278 dosya hash'i eşleşti. Eksik
SPSS dosyaları geri yüklendi, satır sonları eski manifestlere göre onarıldı;
B01 için yeni manifest oluşturuldu. 17 SPSS/metin yedek çifti aynıdır.
R/SPSS yorumlayıcıları ortamda bulunmadığından çalışma testleri bekliyor.
[Yeni kayıt](../toplu-kontrol-onarim-2026-09-10.json) ve
[R/SPSS rehberi](../RSPS_KONTROL.md).

| Kod | Konu | Ders / kapsamlı bölüm | Yerel durum | Python | R / SPSS |
|---|---|---|---|---|---|
| [B01](b01/README.md) | İstatistiksel düşünme ve araştırma süreci | 1 / 1 | Dosyalar tamam | 18 kontrol geçti | Çalıştırma bekliyor |
| [B02](b02/README.md) | Evren, örneklem ve veri türleri | 2 / 2 | Dosyalar tamam | 23 kontrol geçti | Çalıştırma bekliyor |
| [B03](b03/README.md) | Betimsel istatistik | 3 / 3 | Dosyalar tamam | 26 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B04](b04/README.md) | Örnekleme dağılımları | 4 / 4 | Dosyalar tamam | 28 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B05](b05/README.md) | Merkezi limit teoremi ve standart hata | 5 / 5 | Yüklenen dosyalar doğrulandı | 24 kontrol geçti; 14 hash eşleşti | Çalıştırma bekliyor |
| [B06](b06/README.md) | Örnekleme yöntemleri | 6 / 6 | Dosyalar tamam | 29 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B07](b07/README.md) | Nokta tahmini | 7 / 7 | Dosyalar tamam | 21 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B08](b08/README.md) | Güven aralıkları | 8 / 8 | Dosyalar tamam | 19 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B09](b09/README.md) | Hipotez testleri | 9 / 10 | Dosyalar tamam | 20 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B10](b10/README.md) | Tip I–Tip II hata, güç ve tek örneklem t testi | 10 / 11 | Dosyalar tamam | 30 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B11](b11/README.md) | Bağımsız ve eşleştirilmiş t testleri | 11 / 12 | Dosyalar tamam | 34 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B12](b12/README.md) | Kategorik veriler ve ki-kare bağımsızlık testi | 12 / 13 | Dosyalar tamam | 32 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B13](b13/README.md) | Korelasyon ve basit doğrusal regresyon | 13 / 14 | Dosyalar tamam | 62 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [B14](b14/README.md) | Genel sınava hazırlık | 14 / 17 | Dosyalar tamam | 17 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [bootstrap](bootstrap/README.md) | Bootstrap ve rastgeleleştirme | — / 9 | Yerelde hazır | 26 kontrol geçti; 19 hash eşleşti | Çalıştırma bekliyor |
| [coklu-regresyon](coklu-regresyon/README.md) | Çoklu doğrusal regresyon | — / 15 | Dosyalar tamam | 66 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |
| [anova](anova/README.md) | ANOVA, Tukey ve Welch | — / 16 | Dosyalar tamam | 70 kontrol geçti; grafik üretildi | Çalıştırma bekliyor |

Her pakette veri sözlüğü, ortak CSV, üç dilde çözüm, beklenen sayısal sonuçlar,
alıştırmalar, yanıtlar ve ayrı doğrulama kaydı bulunur. R/SPSS kodunun hazır
olması, bu yazılımlarda çalıştırılarak doğrulandığı anlamına gelmez.

Küçük yapay öğretim örnekleri `companion/spss` içindeki gerçek veri
uygulamalarından ayrıdır. Aynı sayıda gözlem veya aynı analiz oldukları
varsayılmamalıdır. Çoklu regresyon paketi kapsamlı sürümün 15. bölümü
için hazırlandı. ANOVA kapsamlı sürümün 16. bölümüdür. Bootstrap yeniden
oluşturularak kapsamlı sürümün 9. bölümüne eşlendi; ders sürümündeki B09
hipotez testleri paketiyle karıştırılmamalıdır.

B05 kullanıcı tarafından yüklenen dosyalardan doğrulandı; içeriği veya
manifesti değiştirilmedi. Windows yol ayırıcılarını okumak için denetleyici
uyarlandı. Bootstrap'ın [ZIP ve metin aktarım seçenekleri](../README.md#bootstrap-aktarımı)
vardır; yerel test, kullanıcı tarafındaki aktarımı kanıtlamaz.

B01 için daha önce oluşturulan ZIP ve yükleme taslakları yalnız B01'i
kapsar; yeni bölümlerin eklendiği nihai paket değildir. Yayın koşulları
ayrıca belirlenecek; kendiliğinden açık kaynak lisansı atanmayacaktır.