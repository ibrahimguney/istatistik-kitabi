# Doğrulama kaydı

Kayıt güncellemesi: 23 Eylül 2026. Kapsam: paketin özgün, yapay öğretim verileri.

- Python: `--check` başarılı. `scripts/check_new_packages.py` bağımsız formül kontrolleri ve hatalı sütun reddini de denetler.
- R: kullanıcı kendi Windows/RStudio ortamında `source("cozum.R")` çalıştırdı; tüm çıktı etiketleri ve değerlerini `beklenen-sonuclar.csv` ile `stopifnot` kullanarak karşılaştırdı. Başarı mesajı paylaşılan ekran görüntüsünde görüldü. Bağıl tolerans 1e-8, mutlak tolerans 1e-10.
- SPSS 29: kullanıcı tarafından çalıştırılan analiz tabloları, R/Python referanslarıyla ekranda gösterilen basamaklar düzeyinde karşılaştırıldı. Bu, otomatik ve tam hassasiyetli bir SPSS testi değildir.
- R ve SPSS bu depo güncellemesini yapan ortamda çalıştırılmadı; bu yazılımlara ilişkin kanıt kullanıcı tarafından paylaşılan çıktılardır.
- Beklenen CSV, Python çıktısından oluşturulmuştur; R karşılaştırması ve ayrı formül denetimleri ek kontrol sağlar. Bu kayıt bütün kitabın, tüm olası girdilerin veya istatistiksel varsayımların doğrulandığı anlamına gelmez.

## Kontrol edilen sonuçlar

- N=12; son ölçümde 11 geçerli, 1 eksik (%8,33) gözlem. Eksik gözlem ikinci gruptadır.
- Grup son ölçüm ortalamaları 60,6667 ve 58,6000; standart sapmalar 7,63326 ve 7,16240.
- Son ölçümü eksik kişinin ön ölçümü 40; gözlenenlerin ön ölçüm ortalaması 53,1818.
- İlk SPSS denemesinde son sütununun tamamı eksik okunmuştur. Noktalı ondalık ayarı eklendikten sonra yeniden çalıştırılan çıktı yukarıdaki değerlerle eşleşmiştir.

## SPSS veri okuma ayarı

Sözdiziminde `GET DATA` öncesine `SET DECIMAL=DOT.` eklendi. CSV dosyalarındaki noktalı ondalık değerlerin Türkçe bölgesel ayarda da okunması amaçlanır. Çalışma klasörünü seçip sözdiziminin tamamını çalıştırın; geçerli/eksik gözlem sayılarını denetleyin.

Sürümler ve durumlar: [DOGRULAMA.json](DOGRULAMA.json).
