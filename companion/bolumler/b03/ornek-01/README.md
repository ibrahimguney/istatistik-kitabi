# B03 / Örnek 01 — Merkez, yayılım ve aykırı değer

## Soru ve veri

Çalışma süreleri 2, 3, 3, 4 ve 13 saat olan beş yapay gözlem için merkezi,
yayılımı ve aykırı değer sınırlarını bulun. Histogramla kutu grafiğini
karşılaştırın. 13 saatlik kayıt dışarıda bırakıldığında merkez nasıl değişir?

Bir satır bir yapay öğrenci gözlemi, `saat` sütunu haftalık çalışma süresidir.
Öğrenci kimliği bulunmaz. Süre oran ölçeğinde sayısaldır; bu örneğin tam sayı
kullanması süreyi sıralı kategori yapmaz. Veri kaynağı kitabın Bölüm 3
Python/R öğretim örneğidir; dış veri indirilmez. CSV UTF-8, ayırıcı virgül,
ondalık işareti noktadır. Sütun sözlüğü `veri-sozlugu.csv` içindedir.

## Çalıştırma

Tüm komutları **bu örneğin klasöründe** çalıştırın. Kitap kökünden
`cd companion/bolumler/b03/ornek-01`; gelecekteki bağımsız eşlikçi depo
kökünden `cd bolumler/b03/ornek-01` kullanın. Tek dosyayı değil bu klasörün
tamamını taşıyın. Betikler kitabın başka dosyalarına başvurmaz.

### Python

```bash
python cozum.py --check
python cozum.py --check --grafik
```

Python, NumPy ve pandas gerekir; grafik seçeneği ayrıca Matplotlib kullanır.
Bu ortamda Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, Matplotlib 3.10.8 ile
sınandı. Betik paket kurmaz. `--check`, 26 satırın etiketlerini, sırasını ve
sayılarını 1e-9 mutlak/bağıl toleransla denetler; uyuşmazlık hata koduyla biter.
`--grafik`, `ciktilar/python/betimsel-grafikler.png` dosyasını yeniler.

### R

```bash
Rscript cozum.R --check
Rscript cozum.R --check --grafik
```

Standart R işlevleri yeterlidir; ek paket gerekmez. Çalışma dizini bu klasör
olmak koşuluyla RStudio'da `source("cozum.R")` sayısal sonuçları gösterir,
fakat tek başına `--check` denetimini veya grafik kaydını başlatmaz.
Etkileşimli oturumda ayrıca:

```r
kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
grafik_kaydet(veri)
```

R çıktısı `ciktilar/r/betimsel-grafikler.png` yoluna yazılır; Python grafiğinin
üzerine yazılmaz. Betik `sessionInfo()` çıktısını verir. **R burada çalıştırılmadı.**

### IBM SPSS

1. Açık veri dosyalarınızı kaydedin. SPSS'in çalışma dizinini bu örnek klasörü
   yapın; sözdizimi dosyasını açmak tek başına dizini değiştirmez. SPSS kitap
   proje kökünde başlatıldıysa bir kez `CD 'companion/bolumler/b03/ornek-01'.`
   çalıştırılabilir. Başka bir dizindeyseniz önce uygun çalışma dizinini seçin.
2. `analiz.sps` dosyasını çalıştırın. Bu uzantı arayüzde görünmüyorsa
   `analiz.sps.txt` kopyasını **aynı klasörde** `analiz.sps` adıyla kaydedin.
3. Dictionary'de `saat` sayısal/Scale olmalı. Frekans tablosunda 2/3/4/13
   değerlerinin sıklıkları 1/2/1/1, geçerli gözlem 5, eksik gözlem 0 olmalı.
   Veri farklıysa devam etmeden sözlükle ve CSV ile karşılaştırın.
4. Descriptives'te toplam 25, ortalama 5, örneklem varyansı 20,5 ve standart
   sapma yaklaşık 4,5277; Frequencies'te medyan 3 olmalı.
5. Kodun ürettiği `q1`, `q3`, `iqr`, `alt_sinir`, `ust_sinir` listesini
   3/4/1/1,5/5,5 ile karşılaştırın. `aykiri=1` yalnız 13 saat için çıkmalı.
6. Son geçici seçimin Frequencies çıktısında geçerli gözlem 4, ortalama 3,
   medyan 3 olmalı. `TEMPORARY` seçimi ana veriden kayıt silmez.

SPSS bu ortamda çalıştırılmadı; `.sav`/`.spv` çıktısı sunulmuyor ve SPSS için
26 satırlık otomatik `--check` testi yok. Kaynak kod eksiksiz bu beş gözleme
göre hazırlanmıştır; yeni veride eksik/negatif süre denetimini kullanıcı
yapmalıdır. Python ve R bu tür girdileri hata vererek reddeder.

## Hesaplama sözleşmesi

- Varyans ve standart sapma **örneklem** hesabıdır: bölen `n-1`.
- Python `quantile(method="linear")`, R `quantile(type=7)` kullanır. SPSS
  kodu sıralı gözlemlerden `h=1+(n-1)p` konumuyla aynı doğrusal enterpolasyonu
  açıkça hesaplar; varsayılan yüzdelik tablosunun yöntemine dayanmaz.
- Aykırılık, `Q1-1,5 IQR` altına veya `Q3+1,5 IQR` üstüne **kesin** geçiştir.
  Sınır üzerindeki bir gözlem bu kurala göre aykırı sayılmaz. Kutu bıyıkları
  sınırlara değil, sınırlar içinde kalan en uç gözlemlere uzanır.
- Python/R kutu grafikleri aynı hesaplanmış özeti `bxp` ile çizer. Kitaptaki
  temel R `boxplot` çağrısının Tukey menteşeleri burada type 7 ile aynıdır;
  başka örneklerde aynı olmak zorunda değildir. SPSS'in yerleşik EXAMINE
  grafiği de ayrı yönteme dayanabilir: karşılaştırmada kodun hesapladığı
  çeyrek ve sınır listesini esas alın.
- Python/R histogram sınıfları `[0,3)`, `[3,6)`, `[6,9)`, `[9,12)`, `[12,15]`:
  sayılar 1/3/0/0/1'dir. Yalnız son sınıf sağ ucunu da içerir. Yeni süre 15'i
  aşarsa sağ uç, 3'ün yeterli ilk katına uzar; sınıf genişliği yine 3 saattir.
  R grafiğinde `fuzz=0` ile sınıra yakın değerler için ek tolerans kapatılır.
  SPSS'in yerleşik histogramı otomatik sınıflar seçebilir; görüntüsünün bu
  beş sütunla aynı olması beklenmez. Ortak sınıf frekansları CSV'den kontrol edilir.
- `duyarlilik_13_haric` yalnız değeri 13 olan kayıtların varsayımsal olarak
  çıkarıldığı özetleri verir; bütün aykırıları silen bir algoritma değildir.
  Veri dosyası değişmez. Hiç kayıt kalmazsa hacim 0, ortalama/medyan NaN veya
  NA'dır; 0 puan/saat gibi gösterilmez.
- Python/R en az iki gözlem, tek `saat` sütunu, sonlu ve negatif olmayan
  sayısal girdiler bekler. Sıfır geçerli süredir; eksik değerin yerine konmaz.

`beklenen-sonuclar.csv` yalnız özgün beş gözleme aittir. Alıştırma kopyalarını
bu referansa uydurmayın; değiştirilmiş veriyle `--check` başarısızlığı beklenir.
Ekran yuvarlaması CSV'deki tam duyarlığı değiştirmez. Rastgele işlem yoktur;
tohum gerekmiyor. Grafikler piksel eşitliğiyle değil, veri ve özetlerle karşılaştırılır.

## Okuma ve yorum

[Adım adım çözüm](cozum.md), [grafik açıklaması](grafik-aciklamasi.md),
[alıştırmalar](../alistirmalar.md) ve [yanıtlar](../cozumler.md).
13 saat bir kontrol işaretidir, veri giriş hatası olduğuna dair kanıt değildir.
Yapay örnekten öğrenci evrenine genelleme yapılmaz.

## Teknik kaynaklar

9 Eylül 2026 tarihinde kaynak incelemesi için başvuruldu; bağlantıların
incelenmesi R/SPSS çalışma testi değildir.

- R: `quantile`, `hist`, `bxp` resmi yardım sayfaları:
  <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html>
  <https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/hist.html>
  <https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/bxp.html>
- NumPy: `histogram` sınıf uçlarının tanımı:
  <https://numpy.org/doc/stable/reference/generated/numpy.histogram.html>
- IBM SPSS: AGGREGATE ve EXAMINE başvuruları:
  <https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=aggregate-overview-command>
  <https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=examine-percentiles-subcommand-command>