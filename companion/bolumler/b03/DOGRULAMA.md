# B03 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: beş gözlemli `ornek-01` yapay öğretim verisi.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3 ve Matplotlib 3.10.8 ile
  `python cozum.py --check --grafik` başarıyla çalıştı. 26 kontrol değeri
  1e-9 mutlak/bağıl toleransla eşleşti; histogram ve kutu grafiği üretildi.
- Ortak CSV'nin tek sütunu ve beş değeri, Bölüm 3'ün Python ve R kaynak
  bloklarından ayrı ayrı çıkarılarak karşılaştırıldı: 2, 3, 3, 4, 13.
  Veri sözlüğünün sütun adı aynı; hesaplama girdi veri çerçevesini değiştirmiyor.
- Toplam 25, ortalama 5, medyan/mod 3, sapma kareleri toplamı 82, örneklem
  varyansı 20,5 ve evren varyansı 16,4 temel Python aritmetiği/`statistics`
  ile ayrıca hesaplandı. `statistics.quantiles(method="inclusive")`
  çeyrekleri 3/3/4 verdi; bu kontrol NumPy hesabından ayrıdır.
- Dokuz geçersiz girdi reddedildi: boş veri, tek gözlem, yanlış sütun adı,
  fazla sütun, eksik süre, sonsuz süre, negatif süre, sayısal olmayan süre
  ve mantıksal değerlerden oluşan süre sütunu.
- Histogram frekansları 1/3/0/0/1 olarak doğrulandı. 0/3/6/9/12/15 sınır
  girdilerinde frekanslar 1/1/1/1/2 oldu; son sağ uç kaybolmadı. Sıfır,
  3'ün hemen altındaki değer ve 15 üstündeki değerle toplam sayım korundu.
- Kutu grafiği özeti bıyıkları 2/4, aykırı değer 13 ve sınırları 1,5/5,5
  verdi. Dört gözlemli 2/3/3/4 karşılaştırmasında type 7 çeyrekleri
  2,75/3,25 olarak bulundu; beş gözleme özgü konumlar sabit kodlanmadı.
- 13→23, bütün değerlere +2 ve saat→dakika dönüşümlerinin merkez/yayılım,
  çeyrek ve aykırılık yanıtları ayrıca doğrulandı. 23 saat için histogram
  sağ ucu 24'e uzadı. Özgün CSV bu denemelerde değiştirilmedi.
- Bütün değerler 13 olduğunda aykırı sayısı 0; `duyarlilik_13_haric`
  hacmi 0, ortalama/medyan NaN oldu. Sıfırlardan oluşan veri geçerli kaldı,
  varyansı 0 çıktı. Bu işlemler çalışma zamanı uyarısı üretmedi.
- Örnek klasörü geçici başka bir klasöre kopyalandı; `--check --grafik`
  orada da çalıştı. Değiştirilmiş veri, değiştirilmiş kontrol değeri ve
  ters sıralanmış kontrol tablosu ayrı ayrı sıfırdan farklı çıkış kodu verdi.
- Üretilen Python grafiği görsel olarak incelendi: eksenler/başlıklar okunur,
  frekans ekseni sıfırdan başlar, 13 saatlik nokta görünür, boş sınıflar
  korunur. Grafik açıklaması görüntüdeki veri özetlerini açıklar.
- `analiz.sps` ile `analiz.sps.txt` dosyalarının byte düzeyinde aynı olduğu
  doğrulandı. Yerel belge bağlantıları ve manifest özetleri kontrol edildi.

## İncelenen fakat çalıştırılmayanlar

R kodunun ayraç dengesi, CSV başvurusu, 26 satırlık çıktı düzeni, type 7
çeyrek seçimi ve grafik için `bxp` özeti kaynak üzerinden incelendi.
R `hist` ve `bxp` yardım belgelerine başvuruldu. **Bu inceleme R yorumlayıcısı
testi değildir.**

SPSS'te veri içe aktarma, SCALE tanımı, örneklem betimlemeleri, sıralama ve
AGGREGATE ile açık çeyrek hesabı, geçici duyarlılık seçimi kaynak üzerinden
incelendi. Teknik başvurular örneğin README'sinde bulunur. Yerleşik SPSS
grafiklerinin sınıf/çeyrek varsayılanları Python/R ile aynı kabul edilmedi.

## Bekleyen doğrulamalar

Bu ortamda R ve IBM SPSS çalıştırılamadı; `.sav`/`.spv` veya R grafiği
üretilmedi. Python'un geçmesi üç yazılımda sonuç eşitliğinin uçtan uca
kanıtı değildir. Yayından önce:

1. R kurulu bilgisayarda örnek klasöründen `Rscript cozum.R --check --grafik`
   çalıştırın. 26 kontrolü, grafik özetlerini ve `sessionInfo()` çıktısını kaydedin.
2. IBM SPSS'te aynı klasörü çalışma dizini yapıp `analiz.sps` çalıştırın.
   README'deki çıktı kontrol sırasını izleyin; Q1/Q3 için açık hesaplanan
   listeyi esas alın. Görüntü yuvarlamasını hesaba katın; SPSS sürümünü kaydedin.
3. Gerçek çalıştırma sonuçlarını bu kayda ekleyin. İncelemeyi çalışma testi
   gibi sunmayın; değişen dosyalar için manifesti yenileyin.

## Bütünlük ve yeniden üretim

`MANIFEST.json`, kendisi dışındaki B03 dağıtım dosyalarının SHA-256
özetlerini içerir. Python PNG'si ve SPSS metin yedeği de bu kapsamdadır.
Belge, veri, betik veya grafik yenilenirse manifest yeniden üretilmelidir;
eski kontrol kaydı değiştirilmiş kodun kanıtı değildir. SPSS uzantısı
arayüzde taşınmazsa `.sps.txt` kopyasını `.sps` adıyla geri oluşturun.

Kitabın LaTeX dosyaları değiştirilmedi; PDF derlemesi yapılmadı. Yeni ZIP,
commit veya GitHub yüklemesi hazırlanmadı. Mevcut B01 arşivleri B03'ü içermez.