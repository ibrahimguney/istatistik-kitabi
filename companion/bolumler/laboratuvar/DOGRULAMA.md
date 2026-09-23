# Doğrulama kaydı

Kayıt güncellemesi: 23 Eylül 2026. Kapsam: paketin özgün, yapay öğretim verileri.

- Python: `--check` başarılı. `scripts/check_new_packages.py` bağımsız formül kontrolleri ve hatalı sütun reddini de denetler.
- R: kullanıcı kendi Windows/RStudio ortamında `source("cozum.R")` çalıştırdı; tüm çıktı etiketleri ve değerlerini `beklenen-sonuclar.csv` ile `stopifnot` kullanarak karşılaştırdı. Başarı mesajı paylaşılan ekran görüntüsünde görüldü. Bağıl tolerans 1e-8, mutlak tolerans 1e-10.
- SPSS 29: kullanıcı tarafından çalıştırılan analiz tabloları, R/Python referanslarıyla ekranda gösterilen basamaklar düzeyinde karşılaştırıldı. Bu, otomatik ve tam hassasiyetli bir SPSS testi değildir.
- R ve SPSS bu depo güncellemesini yapan ortamda çalıştırılmadı; bu yazılımlara ilişkin kanıt kullanıcı tarafından paylaşılan çıktılardır.
- Beklenen CSV, Python çıktısından oluşturulmuştur; R karşılaştırması ve ayrı formül denetimleri ek kontrol sağlar. Bu kayıt bütün kitabın, tüm olası girdilerin veya istatistiksel varsayımların doğrulandığı anlamına gelmez.

## Kontrol edilen sonuçlar

- N=16; son ölçüm ortalaması 59,5; %95 güven aralığı [56,3566; 62,6434]. Ortalama değişim 5,375.
- Eşli t=11,152, sd=15, p<0,001. Son ortalamasının güven aralığı ile değişimin güven aralığı [4,34771; 6,40229] farklıdır.
- Welch t=1,204, sd=13,331, iki yönlü p=0,249. SPSS'de eşit varyans varsayılmayan satır kullanılır.
- Saat ile son ölçüm Pearson r=0,981, p<0,001; basit regresyonda sabit=44,598 ve saat eğimi=3,137.
- Ön ölçüme göre düzeltilmiş regresyon: sabit=4,411, ön ölçüm katsayısı=1,050, grup_B katsayısı=−3,500.
- Yüksek artış çapraz tablosu [[2,6],[8,0]]; Fisher iki yönlü kesin p=0,007 (R: yaklaşık 0,006993007).

## SPSS veri okuma ayarı

Sözdiziminde `GET DATA` öncesine `SET DECIMAL=DOT.` eklendi. CSV dosyalarındaki noktalı ondalık değerlerin Türkçe bölgesel ayarda da okunması amaçlanır. Çalışma klasörünü seçip sözdiziminin tamamını çalıştırın; geçerli/eksik gözlem sayılarını denetleyin.

Sürümler ve durumlar: [DOGRULAMA.json](DOGRULAMA.json).
