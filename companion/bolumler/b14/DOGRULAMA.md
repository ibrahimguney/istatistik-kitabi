# B14 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: 24 tam çiftin son−ön fark özeti ve sınav rehberi.
Ders sürümü Bölüm 14; kapsamlı sürüm Bölüm 17.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi toplu hazırlık tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ve Matplotlib
  3.10.8 ile `python cozum.py --check --grafik` geçti. 4 girdi ve 13
  test/aralık sonucu olmak üzere 17 değer 1e-9 mutlak/bağıl toleransla eşleşti.
- SE ve t cebirsel olarak, p ve kritik değer açık t yoğunluğunun sayısal
  integrali ve kök bulmayla referans dosyasına hesaplandı. Çözümdeki
  `stats.t.sf/ppf` çıktıları referansa kopyalanmadı.
- Kitaptaki Python bloğu çalıştırıldı; t, p ve aralık uçları eşleşti.
  R bloğunun üç özet girdi ataması CSV ile karşılaştırıldı; bu bir R çalışma testi değildir.
- Veri sözlüğü sütun sırası CSV ile, SHA-256 kaynak kaydıyla eşleşti.
  Hesaplama özgün veri çerçevesini değiştirmedi.
- 21 geçersiz girdi reddedildi: boş/iki satırlı veri, yanlış sütun adı/sırası,
  fazla sütun; dört sütunda eksik değer; çift sayısı=1/2,5/mantıksal,
  sonsuz veya metin fark, sıfır/negatif fark sapması, α=0/1/5/−0,01.
- Farkın işaretini çevirmek t ve d_z işaretlerini, aralık uçlarının yönünü
  değiştirdi; çift yönlü p aynı kaldı. Pozitif ölçek dönüşümünde t/p/d_z
  değişmezliği ve SE/aralıkların ölçeklenmesi doğrulandı.
- Sıfır farkta t=0, p=1, d_z=0, ret yok ve sıfır aralıkta bulundu;
  bu girdiyle grafik üretimi de geçti.
- α=0,01 ile p'nin değişmediği, ret kararının değiştiği ve %99 aralığın
  genişleyip sıfırı içerdiği doğrulandı. p=α eşitliğinde ret yoktur.
  Kritik t'nin mutlak değerinin 1e-6 altı/üstünde test-aralık uyumu denetlendi.
- Çift sayısı 2 için df=1 kabul edildi. Çift sayısı 96'ya çıkarıldığında
  SE'nin yarılanması, t'nin iki katına çıkması ve d_z'nin değişmemesi kontrol edildi.
- Karma korelasyon/regresyon sorusunun b₁=2, b₀=52, R²=0,25,
  X=7 öngörüsü=66, t(48)=4 ve p<0,001 aritmetiği ayrıca denetlendi.
  Bu hesaplar özgün 17 kontrol satırına dahil değildir.
- Paket geçici başka bir klasöre kopyalandı; Python kontrolü ve grafik
  üretimi geçti. Değişmiş fark yönü, değişmiş α, yanlış kontrol değeri
  ve ters sıralı kontrol tablosu ayrı ayrı başarısız çıkış üretti.
  Kaynak paket dosyaları değişmedi.
- PNG açılarak incelendi; negatif ortalama fark, aralık uçları ve sıfır
  çizgisi okunabilir. Açıklama, evren ortalama aralığını bireysel fark
  dağılımından ve nedensel etki iddiasından ayırır.

## İncelenen fakat çalıştırılmayanlar

- R kodunun parantez dengesi, CSV başvurusu, çift yönlü kuyruk ve 17
  satırlık sonuç düzeni kaynak üzerinden incelendi.
- SPSS CDF.T/IDF.T formülleri IBM belgeleriyle karşılaştırıldı; kaynaklar
  örneğin README'sindedir. `analiz.sps` ve `analiz.sps.txt` byte düzeyinde aynıdır.
- Sınav rehberi ve karma alıştırmalar yöntem gerekçelerini destekler;
  bütün yöntemleri çalıştıran test paketi veya otomatik notlandırıcı değildir.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda bulunmuyor; kodları gerçek yorumlayıcılarında
çalıştırılmadı. R grafiği veya SPSS `.sav`/`.spv` çıktısı üretilmedi.
Python'un geçmesi üç yazılımda uçtan uca sonuç eşitliği kanıtı değildir.

1. Örnek klasöründe `Rscript cozum.R --check --grafik` çalıştırın;
   17 değerin eşleştiğini doğrulayın, grafiği ve `sessionInfo()`yu kaydedin.
2. SPSS'te tek özet satırını elle doğrulayın; çalışma dizinini örnek
   klasörü yapıp `analiz.sps` çalıştırın. İki LIST tablosunu kontrol
   CSV'siyle karşılaştırın; sürümü ve gerçek sonucu kaydedin.
3. Gerçek araştırmada eşleşmeler, tam çiftler, fark dağılımı ve örnekleme
   koşulları ayrıca denetlenmelidir; bu özet bunları doğrulamaz.

## Bütünlük ve toplu yayın

`MANIFEST.json`, kendisi dışındaki B14 dağıtım dosyalarının SHA-256
özetlerini listeler. Dosyalar değişirse manifest ve ilgili doğrulama kaydı
yenilenmelidir. `.sps` görünmüyorsa `.sps.txt` yedeğinden geri getirilebilir.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Kitabın LaTeX dosyaları
bu paket için değiştirilmedi; PDF derlemesi gerekmedi.

B14'ün hazır olması bütün yayın paketinin tamamlandığı anlamına gelmez:
B05 bu çalışma kopyasında eksik, bootstrap/çoklu regresyon/ANOVA paketleri
henüz hazırlanmamış ve R/SPSS çalıştırma doğrulamaları beklemektedir.