# B11 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: iki bağımsız grubun özeti ve ayrı bir
20 çiftlik örneğin fark özeti. Ders sürümü Bölüm 11; kapsamlı sürüm Bölüm 12.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ve Matplotlib
  3.10.8 ile `python cozum.py --check --grafik` geçti. 34 değer
  1e-9 mutlak/bağıl toleransla eşleşti.
- Welch varyans katkıları ve df referansı tam kesir aritmetiğiyle üretildi.
  İki testin p ve kritik değerleri açık t yoğunluğu, sayısal integral ve
  kök bulmayla hesaplandı; çözümün `stats.t.sf/ppf` çıktıları kopyalanmadı.
- Kitaptaki Python bloğunun yalnız özet istatistik kısmı çalıştırıldı;
  Welch ve eşleştirilmiş t/p değerleri eşleşti. Spector dosyasını okuyan
  gerçek veri kısmı bu pilotun kapsamı dışında tutuldu ve çalıştırılmadı.
- Kitaptaki R örneğinin grup vektörleri ve üç eşleştirilmiş girdi ataması
  CSV ile karşılaştırıldı. Bu, R yorumlayıcısı testi değildir.
- Veri sözlüğü sütun sırası CSV ile, kaynak kaydındaki SHA-256 girdiyle
  eşleşti. Hesaplama özgün veri çerçevesini değiştirmedi.
- 37 geçersiz girdi reddedildi: boş/iki satırlı veri, yanlış sütun adı/sırası,
  fazla sütun; her sütunda eksik değer; üç hacim alanında 1/2,5/mantıksal
  değer; üç sapma alanında sıfır/negatif değer; sonsuz ortalama/ortalama farkı,
  metin ortalaması ve α=0/1/5/−0,05.
- Grupların hacim/ortalama/sapmalarını birlikte yer değiştirmek Welch t ve
  aralık yönünü çevirdi; df/p değişmedi. Eşleştirilmiş fark yönünü çevirmek
  t ve d_z işaretlerini çevirdi; çift yönlü p değişmedi.
- Bağımsız grubun girdisini değiştirmek eşleştirilmiş sonucu, eşleştirilmiş
  girdiyi değiştirmek Welch sonucunu etkilemedi. Konum ve pozitif ölçek
  dönüşümleri, sıfır fark ve α=0,01 sonuçları denetlendi.
- Her iki testte p=α eşitliğinde reddetmeme kontrol edildi. Çift sayısı
  80 olduğunda SE'nin yarılanması, t'nin iki katına çıkması ve d_z'nin
  değişmemesi doğrulandı. Alıştırmalardaki korelasyon–fark sapması hesapları yapıldı.
- Dört farklı hacim/sapma düzeninde özet formülü, SciPy
  `ttest_ind_from_stats(..., equal_var=False)` ile eşleşti; n=2 ve
  belirgin dengesiz hacim/sapma durumları da bu karşılaştırmaya dahildi.
- Paket geçici başka bir klasöre kopyalandı; Python kontrolü ve grafik
  üretimi geçti. Değişmiş bağımsız grup girdisi, değişmiş eşleşmiş fark,
  yanlış kontrol değeri ve ters sıralı kontrol tablosu ayrı ayrı başarısız
  çıkış üretti. Kaynak paket dosyaları değişmedi.
- PNG açılarak incelendi; iki aralık, yönler, sıfır çizgileri ve uç
  etiketleri okunabilir. Grafik açıklaması farklı yatay ölçekleri ve
  örneklerin ayrı oluşunu açıkça belirtir.

## İncelenen fakat çalıştırılmayanlar

- R kodunun parantez dengesi, CSV başvurusu, 34 satırlık çıktı sırası,
  Welch kesirli df ve eşleştirilmiş fark formülleri incelendi.
- SPSS `CDF.T`/`IDF.T` kullanımı IBM belgeleriyle karşılaştırıldı;
  teknik başvurular örneğin README'sindedir. `analiz.sps` ve
  `analiz.sps.txt` dosyaları byte düzeyinde aynıdır.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda bulunmuyor; kodları gerçek yorumlayıcılarında
çalıştırılmadı. R grafiği veya SPSS `.sav`/`.spv` çıktısı üretilmedi.
Python'un geçmesi üç yazılımda uçtan uca eşitlik kanıtı değildir.

1. Örnek klasöründe `Rscript cozum.R --check --grafik` çalıştırın;
   34 değerin eşleştiğini doğrulayın, grafiği ve `sessionInfo()`yu kaydedin.
2. SPSS'te girdi satırını elle doğrulayın, çalışma dizinini örnek klasörü
   yapıp `analiz.sps` çalıştırın. Üç LIST tablosunu kontrol CSV'siyle
   karşılaştırın; değer etiketleri/yuvarlamayı dikkate alın ve sürümü kaydedin.
3. Gerçek araştırmada bağımsızlık, eşleşme doğruluğu, tam çiftlerin seçimi,
   fark dağılımı ve pratik önem ayrıca incelenmelidir. Özet veriden bu
   kontroller yapılmış gibi raporlanmamalıdır.

## Bütünlük ve yayın

`MANIFEST.json`, kendisi dışındaki B11 dağıtım dosyalarının SHA-256
özetlerini listeler. Dosyalar değişirse manifest ve ilgili doğrulama kaydı
yenilenmelidir. `.sps` görünmüyorsa `.sps.txt` yedeğinden geri getirilebilir.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Kitabın LaTeX dosyaları
bu paket için değiştirilmedi; PDF derlemesi gerekmedi.