# B13 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: 16 saat/puan çifti, sabit terimli basit
regresyon ve 6 saat için %95 ortalama yanıt/yeni birey aralıkları.
Ders sürümü Bölüm 13; kapsamlı sürüm Bölüm 14.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ve Matplotlib
  3.10.8 ile `python cozum.py --check --grafik` geçti. 30 genel değer,
  16 tahmin ve 16 artık olmak üzere 62 kontrol eşleşti.
- Çoğu değerde 1e-9 mutlak/bağıl tolerans; `p_egim` için mutlak tolerans
  0, bağıl tolerans 1e-8 kullanıldı. Gerek hesap sonucunda gerek referansta
  küçük p'nin sıfırla değiştirilmesi kontrol hatası oluşturdu.
- Referans merkezli toplamlar, katsayılar, tahminler, artıklar ve SSE
  Fraction tam kesir aritmetiğiyle üretildi. Kritik t ve p açık t yoğunluğu,
  sayısal integral ve kök bulmayla hesaplandı; ana çözüm çıktısı kopyalanmadı.
- Kitaptaki Python bloğu grafik oluşturmadan önceki kısmına kadar
  çalıştırıldı; iki girdi dizisi, katsayılar, Pearson r, küçük p, tahminler
  ve artıklar eşleşti. R bloğunun iki girdi vektörü CSV ile karşılaştırıldı.
- Katsayılar SciPy `linregress` ve ayrı NumPy `lstsq` hesabıyla;
  standart hatalar (X'X) tersine dayalı kovaryans matrisiyle doğrulandı.
  `pearsonr` p-değeri eğim testinin p'siyle bağıl toleransta eşleşti.
- 6 saatin ortalama yanıt standart hatası ayrıca tasarım vektörü ve
  kovaryans matrisiyle denetlendi. Birey SE²−ortalama SE²=MSE ilişkisi ve
  birey aralığının daha geniş oluşu kontrol edildi.
- Veri sözlüğünün sütun sırası CSV ile, SHA-256 kaynak kaydıyla eşleşti;
  hesaplama özgün veri çerçevesini değiştirmedi. Tekrarlanan ölçüm
  çiftlerinin silinmediği ve n=16'nın korunduğu doğrulandı.
- 20 geçersiz veri reddedildi: sıfır/bir/iki satır; yanlış sütun adı/sırası,
  fazla sütun; her sütunda eksik/pozitif sonsuz/negatif sonsuz/mantıksal/metin
  veya sabit değer; negatif saat ve tam doğrusal uyum.
  Dört geçersiz yeni saat değeri (negatif, sonsuz, eksik, mantıksal) de reddedildi.
- Üç satırlı, tam doğrusal olmayan örnek kabul edildi. Sıfır eğimli fakat
  iki değişkeni de değişken olan örnekte r=0 ve p=1 elde edildi.
- Artık toplamı ve saat ile artık iç çarpımı sayısal toleransta sıfır;
  bu sabit terimli tek açıklayıcılı modelde R²=r² ilişkisi doğrulandı.
- Puana sabit ekleme, saati dakikaya dönüştürme, puan işaretini çevirme
  ve ters regresyon alıştırmaları denetlendi. Dakika dönüşümünde öngörü
  noktası da 360 yapıldı. 20 saat öngörüsü yalnız dışa taşırma örneği olarak hesaplandı.
- Satırları çiftler halinde ters çevirmek genel modeli korudu; tahmin ve
  artıklar satırlarla birlikte taşındı. Özgün satır bazlı kontrolün bu
  sıralamayla geçmemesi ayrıca doğrulandı.
- Paket geçici başka bir klasöre kopyalandı; Python kontrolü ve grafik
  üretimi geçti. Değişmiş puan, yeniden sıralanmış satırlar, sıfıra
  çevrilmiş referans p ve ters sıralı kontrol tablosu ayrı ayrı başarısız
  çıkış üretti. Kaynak paket dosyaları değişmedi.
- Son PNG açılarak incelendi; saçılım/doğru, artık, Q-Q ve iki öngörü
  aralığı panelinin etiketleri okunabilir. Alt kuyruk sapmaları açıklamada
  belirtilmiş, normallik sağlanmış veya kayıt silinmeli diye raporlanmamıştır.

## İncelenen fakat çalıştırılmayanlar

- R kaynak kodunun parantez dengesi, `lm`/`confint`/`predict` çağrıları,
  aralık türleri ve 62 satırlık çıktı düzeni incelendi.
- SPSS REGRESSION seçenekleri IBM belgeleriyle karşılaştırıldı;
  yerleşik tahmin/artık kaydı ile formül kontrolü, %95 katsayı aralığı
  ve bilimsel p gösterimi kaynak üzerinden incelendi.
  `analiz.sps` ve `analiz.sps.txt` byte düzeyinde aynıdır.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda bulunmuyor; kodları gerçek yorumlayıcılarında
çalıştırılmadı. R grafiği veya SPSS `.sav`/`.spv` çıktısı üretilmedi.
Python'un geçmesi üç yazılımda uçtan uca eşitlik kanıtı değildir.

1. Örnek klasöründe `Rscript cozum.R --check --grafik` çalıştırın;
   62 değerin eşleştiğini doğrulayın, grafiği ve `sessionInfo()`yu kaydedin.
2. SPSS'te eksiksiz veri ve satır eşleşmesini doğrulayın; örnek klasörünü
   çalışma dizini yapıp `analiz.sps` çalıştırın. Coefficients, Model Summary
   ve LIST tablolarını kontrol CSV'siyle karşılaştırın. Yerleşik/formül
   tahminlerinin eşleşmesini ve küçük p'nin sıfır olmadığını denetleyin.
3. Gerçek sürüm ve sonuçları kayda ekleyin. Örnekleme bağımsızlığı, model
   biçimi, hata varyansı ve çıkarım koşulları ayrıca değerlendirilmelidir.
   Formal normallik/etki testi veya dış örneklem doğrulaması yapılmadı.

## Bütünlük ve yayın

`MANIFEST.json`, kendisi dışındaki B13 dağıtım dosyalarının SHA-256
özetlerini listeler. Dosyalar değişirse manifest ve ilgili doğrulama kaydı
yenilenmelidir. `.sps` görünmüyorsa `.sps.txt` yedeğinden geri getirilebilir.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Kitabın LaTeX dosyaları
bu paket için değiştirilmedi; PDF derlemesi gerekmedi.