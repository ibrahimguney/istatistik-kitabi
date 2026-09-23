# Doğrulama kaydı

Kayıt güncellemesi: 23 Eylül 2026. Kapsam: paketin özgün, yapay öğretim verileri.

- Python: `--check` başarılı. `scripts/check_new_packages.py` bağımsız formül kontrolleri ve hatalı sütun reddini de denetler.
- R: kullanıcı kendi Windows/RStudio ortamında `source("cozum.R")` çalıştırdı; tüm çıktı etiketleri ve değerlerini `beklenen-sonuclar.csv` ile `stopifnot` kullanarak karşılaştırdı. Başarı mesajı paylaşılan ekran görüntüsünde görüldü. Bağıl tolerans 1e-8, mutlak tolerans 1e-10.
- SPSS 29: kullanıcı tarafından çalıştırılan analiz tabloları, R/Python referanslarıyla ekranda gösterilen basamaklar düzeyinde karşılaştırıldı. Bu, otomatik ve tam hassasiyetli bir SPSS testi değildir.
- R ve SPSS bu depo güncellemesini yapan ortamda çalıştırılmadı; bu yazılımlara ilişkin kanıt kullanıcı tarafından paylaşılan çıktılardır.
- Beklenen CSV, Python çıktısından oluşturulmuştur; R karşılaştırması ve ayrı formül denetimleri ek kontrol sağlar. Bu kayıt bütün kitabın, tüm olası girdilerin veya istatistiksel varsayımların doğrulandığı anlamına gelmez.

## Kontrol edilen sonuçlar

- N=12, beş madde; M4 ters puanlandıktan sonra Cronbach alfa=0,964 (R: 0,9636430). Karşılaştırma standartlaştırılmamış alfayladır.
- Düzeltilmiş madde–toplam korelasyonları: 0,934; 0,831; 0,880; 0,965; 0,890.
- Madde silinirse alfa: 0,949; 0,966; 0,958; 0,944; 0,957.
- Toplam puan ortalaması 16,6667. Ters puanlama öncesi alfa=0,2942370 R referans kontrolünde doğrulandı; paylaşılan SPSS tabloları ters puanlama sonrası sonuçları kapsar.

## SPSS veri okuma ayarı

Sözdiziminde `GET DATA` öncesine `SET DECIMAL=DOT.` eklendi. CSV dosyalarındaki noktalı ondalık değerlerin Türkçe bölgesel ayarda da okunması amaçlanır. Çalışma klasörünü seçip sözdiziminin tamamını çalıştırın; geçerli/eksik gözlem sayılarını denetleyin.

Sürümler ve durumlar: [DOGRULAMA.json](DOGRULAMA.json).
