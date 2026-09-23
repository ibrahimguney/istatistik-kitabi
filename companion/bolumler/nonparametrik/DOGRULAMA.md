# Doğrulama kaydı

Kayıt güncellemesi: 23 Eylül 2026. Kapsam: paketin özgün, yapay öğretim verileri.

- Python: `--check` başarılı. `scripts/check_new_packages.py` bağımsız formül kontrolleri ve hatalı sütun reddini de denetler.
- R: kullanıcı kendi Windows/RStudio ortamında `source("cozum.R")` çalıştırdı; tüm çıktı etiketleri ve değerlerini `beklenen-sonuclar.csv` ile `stopifnot` kullanarak karşılaştırdı. Başarı mesajı paylaşılan ekran görüntüsünde görüldü. Bağıl tolerans 1e-8, mutlak tolerans 1e-10.
- SPSS 29: kullanıcı tarafından çalıştırılan analiz tabloları, R/Python referanslarıyla ekranda gösterilen basamaklar düzeyinde karşılaştırıldı. Bu, otomatik ve tam hassasiyetli bir SPSS testi değildir.
- R ve SPSS bu depo güncellemesini yapan ortamda çalıştırılmadı; bu yazılımlara ilişkin kanıt kullanıcı tarafından paylaşılan çıktılardır.
- Beklenen CSV, Python çıktısından oluşturulmuştur; R karşılaştırması ve ayrı formül denetimleri ek kontrol sağlar. Bu kayıt bütün kitabın, tüm olası girdilerin veya istatistiksel varsayımların doğrulandığı anlamına gelmez.

## Kontrol edilen sonuçlar

- Mann–Whitney: her grupta n=10; medyanlar 8 ve 5,5; küçük U=11,5; SPSS Z=−2,955 ve asimptotik iki yönlü p=0,003 (R: yaklaşık 0,003125644).
- SPSS'nin ayrıca verdiği kesin p=0,002, bağlı sıralar için düzeltilmemiştir; paket referansı asimptotik p ile karşılaştırılır.
- Wilcoxon: küçük sıra toplamı 2; SPSS Z=−2,921, p=0,003 (R: yaklaşık 0,003494174). SPSS çıktısı sifir−fark yönündedir; sıra işaretleri R'deki fark yönüne göre ters olabilir. Mann–Whitney tablosundaki W=66,5 farklı bir istatistiktir.
- İşaret testi: iki yönlü kesin p=0,006 (R: 0,00634765625).
- Kruskal–Wallis: H=21,908, sd=2, p<0,001; üç grupta toplam n=30.

## SPSS veri okuma ayarı

Sözdiziminde `GET DATA` öncesine `SET DECIMAL=DOT.` eklendi. CSV dosyalarındaki noktalı ondalık değerlerin Türkçe bölgesel ayarda da okunması amaçlanır. Çalışma klasörünü seçip sözdiziminin tamamını çalıştırın; geçerli/eksik gözlem sayılarını denetleyin.

Sürümler ve durumlar: [DOGRULAMA.json](DOGRULAMA.json).
