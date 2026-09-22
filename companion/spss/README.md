# IMO301 — Literatür verisiyle SPSS uygulamaları

Ders sürümünün 14 bölümüne ait uygulama kodları b01–b14'tür. Kapsamlı
sürümde basılı bölüm numaraları değişse de uygulama kodları değişmez.
Kaynak matematik verisi tüm gözlemsel uygulamalarda ortaktır; dosyalar
14 farklı araştırmanın verileri veya 14 bağımsız örneklem değildir.

## Kaynak, lisans ve dönüşümler

Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning
Repository. DOI: 10.24432/C5TG7T.
Kaynak: https://archive.ics.uci.edu/dataset/320/student+performance
Lisans: CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
Kaynak/lisans kontrol tarihi: 9 Eylül 2026.

Yüklenen student-mat.csv: 395 satır, 33 değişken. raw/student-mat.csv özgün
sütunları korur. Analiz dosyalarında seçilmiş sütunlar yeniden kodlanır;
yapay sıra numarası id ile öğretim amaçlı pass10=(g3>=10) eklenir.
Sıfır notlar korunur, boş hücre yoktur. school: GP=1/MS=2; sex: F=1/M=2.
studytime ordinaldir; 1–4 kodları saat sayıları değildir. absences için gün
veya saat birimi varsayılmamıştır. Tüm değişken tanımları Excel'in sozluk
sayfasındadır. Her çalışma kitabının kaynak sayfasında atıf/lisans vardır.
İki okulun gözlemsel verisinden genelleme/bağımsızlık/nedensellik sonucu
kendiliğinden çıkarılamaz. Testler bağımsız gözlemler modeliyle öğretim içindir.
İleride student-por.csv eklense bile bu paketin 14 uygulaması matematik
verisini kullanır; iki dosya id üzerinden birleştirilmez.

## Güncel dağıtım — 13 Eylül 2026

Analiz dosyalarının tek kaynağı `chapters/spss/b01.tex`–`b14.tex`
içindeki SPSS, R ve Python bloklarıdır. Çok bloklu uygulamalar sırayla
birleştirilir; R'nin etkileşimli `file.choose()` alternatifi toplu dosyaya
ikinci veri okuma komutu olarak eklenmez. Küçük yapay öğretim paketleri
`companion/bolumler` altında ayrıdır; bu klasör literatür uygulamalarını taşır.

## Çalıştırma

Çalışma dizini `companion` klasörünü içeren paket kökü olmalıdır.
SPSS'te `syntax/bXX.sps` dosyasını açıp tamamını çalıştırın:

- B01 CSV açan `open-b01.sps` dosyasını çağırır ve `sav/b01.sav` oluşturur.
- B02/B03 aynı hazırlığı yeniden yapar, ardından bu SAV dosyasını açar.
  Önceden üretilmiş veya eski bir etkin veri dosyasına bağımlı kalmaz.
- B08 `open-b08.sps` üzerinden Excel'in `veri` sayfasını açar.
- Diğer bölümler basılı CSV açma bloklarını içerir. Filtre, ağırlık ve
  dosya bölme başlangıçta kapatılır; her uygulamayı baştan çalıştırın.

Menüyle ilerlerken bölümün veri açma bloğunu `EXECUTE` dahil çalıştırın;
B01–B03 için `open-b01.sps`, B08 için `open-b08.sps` kullanın. Tam analiz
ile menü yolunu, özellikle seçim/özetleme sonrasında, karıştırmayın.
Ayrıca üretilen diğer `open-bXX.sps` dosyaları yalnız veri hazırlığı içindir.
B01'in `open-b01-excel.sps` dosyası alternatif Excel denemesi içindir.

R ve Python dosyalarını paket kökünden çalıştırın:

```text
Rscript companion/spss/r/b14.R
python companion/spss/python/b14.py
```

CSV dosyalarını ve klasör yapısını koruyun; XX yerine ilgili uygulama
kodunu kullanın. Python grafik pencereleri etkileşimli çalışmada açılır.
B10 güç komutu için bölümdeki sürüm koşulu geçerlidir.

## Doğrulama kapsamı

Burada IBM SPSS ve R yeniden çalıştırılmamıştır. Bölümlerde belirtilen
kullanıcı SPSS/R çıktılarıyla yapılan karşılaştırmalar, yerel çalışma
zamanı testi değildir. Python kodları ve dosya bütünlüğü yerel olarak
kontrol edilir. Kullanıcı çıktılarının kapsamı her bölümde ayrıca yazılıdır.

Hazır SAV/SPV çıktısı dağıtılmaz. SAV dosyalarını SPSS oluşturur. Excel
ZIP/XML ve CSV hücre eşitliği, gerçek Excel veya SPSS içe aktarma testi
değildir. B01'de bildirilen Excel açma sorunu giderilmiş sayılmaz; CSV
pilotu esas alınır. B08 Excel içe aktarımı ayrıca kullanıcı ortamında
sınanmalıdır. Yazılımların sayısal uyumu istatistiksel varsayımları kanıtlamaz.

## Dosyalar

- `csv/bXX.csv`: kayıtlar; B04/B05 benzetim, B06 seçim göstergeleri içerir.
- `excel/bXX.xlsx`: aynı veri, ayrıca `sozluk` ve `kaynak` sayfaları.
- `syntax/bXX.sps`: kitaptaki bütün SPSS blokları; `open-bXX.sps`: veri açma.
- `r/bXX.R`, `python/bXX.py`: kitaptaki analiz bloklarının çalıştırılabilir kopyaları.
- `results/values.tex`, `results/checks.json`: Python kontrol değerleri ve kaynak özetleri.
- `chapter-map.csv`: kod, kaynak, kayıt ve değişken sayısı.
- `manifest.csv`: güncel ana dağıtımın SHA-256 envanteri.
- `manifest-history/`: üzerine yazılmadan saklanan önceki ana manifestler.
- `pilot-b01/manifest.json`: ayrı pilotun dokuz dosyalık manifesti;
  pilotun önceki manifestleri kendi `manifest-history/` klasöründedir.

Ana manifest pilotu veya geçmiş manifestleri kapsamaz; pilot ayrı denetlenir.
B04/B05 satırları öğrenci değildir. B06 ağırlığı yalnız nokta tahmininin
öğretimi içindir; tasarım-temelli standart hata sağlamaz. B14'ün pozitif
notlu alt grubu ana veri yerine geçmez. Sıfır notlar ana analizde korunur.

## Yeniden üretim

```text
python -B companion/spss/build_package.py
python -B companion/spss/build_b01_pilot.py
python -B companion/spss/validate_package.py
```

Üretici mevcut ham veri ve CSV baytlarını korur, bunları beklenen içerikle
karşılaştırır; veri farkını sessizce düzeltmez. Excel, dışa aktarılan kodlar
ve Python referans sonuçları yeniden üretilir. Yeni manifest yazılmadan
önce eski manifest içerik özetiyle adlandırılarak saklanır. Kod değişikliği
sonrası yeni hash, tek başına doğruluk kanıtı değildir: denetleyiciyi de
çalıştırın. Denetleyici bütün basılı blokları ve tüm CSV sütunlarını kontrol
eder; başarısız bir assert komutun başarısız bitmesine neden olur.

İlk onarımın öncesi/sonrası ve test kayıtları
`build/eslestirme-2026-09-13/` altındadır. Kökteki
`docs/denetim/TUTARLILIK-KONTROLU.md` kontrol ve onarım kapsamlarını ayırır.
12 Eylül tarihli bütünlük sayıları tarihsel kayıttır; yeni sürüme ait değildir.
Eski `butunluk_onar.py.txt` yerine yukarıdaki güncel üretim akışını kullanın.