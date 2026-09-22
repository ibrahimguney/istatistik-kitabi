# B04 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: {2,4,6,8} evreninden geri koymalı, bağımsız,
eşit olasılıklı iki çekimin 16 sıralı sonucu (`ornek-01`).
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, Matplotlib 3.10.8 ile
  `python cozum.py --check --grafik` çalıştı. 28 sayısal kontrol değeri
  1e-9 mutlak/bağıl toleransla eşleşti; karşılaştırma grafiği üretildi.
- Evren değerleri kitabın Bölüm 4 R kodundan çıkarılarak `evren.csv` ile
  karşılaştırıldı: 2,4,6,8. Python kutusundaki normal benzetimle aynı veri
  olduğu iddia edilmedi; o örnek ayrı tutuldu.
- Üretilen 16 sıralı çift `veri.csv` ile satır ve sütun düzeyinde eşleşti.
  Her iki CSV'nin alanları veri sözlüğüyle aynı. Hesaplar kaynak veri
  çerçevelerini değiştirmedi. Evren ve çift satırlarının ters çevrilmesi
  aynı sonuç tablosunu verdi.
- Bağımsız 4×4 ortalama tablosu, Python `Fraction` kesir aritmetiği ve
  `statistics` ile toplam 80, kareli sapmalar toplamı 40, evren varyansı 5,
  tam dağılım varyansı 5/2 ve 15 bölenli varyans 8/3 doğrulandı.
- Ortalama frekansları 1/2/3/4/3/2/1, en az 7 olasılığı 3/16 ve tam 5
  olasılığı 1/4 bağımsız sayımla doğrulandı.
- 18 hatalı girdi reddedildi. Sekiz evren durumu: boş, tek değer, yinelenen
  değer, yanlış sütun, eksik değer, sonsuz değer, metin ve mantıksal değer.
  On çift tablosu durumu: boş, eksik çift, fazla çift, bir çift yerine
  başka çiftin yinelenmesi, eksik hücre, sonsuz hücre, metin, yanlış sütun
  sırası, evrende olmayan değer ve geri koymasız 12 satırlık liste.
- Farklı büyüklükte ve negatif/sıfır/ondalık değer içeren üç ek evrenle
  merkez ve σ²/2 ilişkisi sınandı; kodda yalnız özgün sayılar sabitlenmedi.
- +10 kaydırma ve ×2 ölçekleme yanıtları; kaydırılmış evrende 17 eşiğinin
  3/16 olasılığı ayrıca kontrol edildi.
- Geri koymalı n=4 için 256 sonuç, merkez 5, varyans 5/4; geri koymasız
  n=2 için 12 sonuç, merkez 5, varyans 5/3 ve 2/2/4/2/2 frekansları
  kesir aritmetiğiyle doğrulandı. Bunlar ana n=2 geri koymalı CSV'yi değiştirmedi.
- Örnek klasörü geçici başka bir klasöre kopyalandı; `--check --grafik`
  orada da çalıştı. Eksiltilmiş çift tablosu, değiştirilmiş evren,
  değiştirilmiş kontrol değeri ve ters sıralı kontrol tablosu ayrı ayrı
  sıfırdan farklı çıkış kodu verdi.
- Python grafiği görsel olarak incelendi: iki panel ortak eksenlerde,
  merkez 5 çizgileri görünür, olasılık ekseni sıfırdan başlıyor. Grafik
  açıklaması, gösterilen ayrık dağılımları ve standart sapma farkını anlatıyor.
- SPSS dosyası ile `.sps.txt` yedeğinin byte eşliği, yerel belge bağlantıları
  ve `MANIFEST.json` SHA-256 özetleri doğrulandı.

## İncelenen fakat çalıştırılmayanlar

R kodunun ayraç dengesi, `expand.grid` sıralaması, CSV karşılaştırması,
28 satırlık çıktı düzeni ve kareli sapma ortalaması kaynak üzerinden
incelendi. Bu bir R yorumlayıcısı testi değildir.

SPSS kaynak kodunda çapraz tablo, çift ortalamaları, AGGREGATE ile
kareli sapma ortalamaları ve yüzde sütun grafiği incelendi. R `expand.grid`
ve IBM AGGREGATE/GRAPH resmi belgelerine başvuruldu; bağlantılar örneğin
README'sindedir. SPSS çıktısı çalıştırılarak doğrulanmadı.

## Bekleyen doğrulamalar

Bu ortamda R ve IBM SPSS çalıştırılmadı. R grafiği, `.sav` veya `.spv`
dosyası üretilmedi. Python'un geçmesi üç yazılımda sonuç eşitliğinin
uçtan uca doğrulandığı anlamına gelmez.

1. R kurulu bilgisayarda örnek klasöründen `Rscript cozum.R --check --grafik`
   çalıştırın. 28 kontrolün eşleşmesini ve grafik özetlerini inceleyin;
   `sessionInfo()` çıktısını kaydedin.
2. SPSS'te çalışma dizinini örnek klasörü yapıp `analiz.sps` çalıştırın.
   Çapraz tablonun 16 hücresinin her birinde 1, toplamda 16 gözlem olmalı.
   README'deki liste/frekans kontrolünü izleyin. Yüzdeleri olasılıkla
   karşılaştırırken 100'e bölün; yuvarlamayı dikkate alın ve sürümü kaydedin.
3. Gerçek sonuçları bu kayda ekleyin; belge, veri veya kod değişirse
   bütünlük manifestini yenileyin. Kaynak incelemesini çalışma testi saymayın.

## Bütünlük ve yayın

`MANIFEST.json`, kendisi dışındaki B04 dağıtım dosyalarının SHA-256
özetlerini içerir. Python grafiği ve SPSS metin yedeği de kapsamdadır.
Dosyalar değişirse manifest yeniden üretilmelidir; eski doğrulama kaydı
sonradan değiştirilmiş kodun kanıtı değildir. Arayüz `.sps` uzantısını
aktarmıyorsa `.sps.txt` kopyasını aynı klasörde `.sps` adıyla geri oluşturun.

Kitabın LaTeX dosyaları değiştirilmedi; PDF derlemesi gerekmedi.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. B01 arşivleri B04'ü içermez.