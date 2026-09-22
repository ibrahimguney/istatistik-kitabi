# B09 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: `ornek-01` fark/standart hata özeti.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.
Ders sürümü Bölüm 9; kapsamlı sürüm Bölüm 10.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ve Matplotlib
  3.10.8 ile `python cozum.py --check --grafik` başarıyla çalıştı.
  20 kontrol değeri 1e-9 mutlak/bağıl toleransla eşleşti.
- Referans p-değeri, t yoğunluğunun açık formülünün sayısal integraliyle;
  kritik değer ise bu integralin kök bulmayla terslenmesiyle elde edildi.
  Çözümdeki `stats.t.sf/ppf` çıktıları referans dosyasına kopyalanmadı.
- Kitaptaki Python bloğu ayrıca çalıştırıldı; p-değeri ve aralık uçları
  eşleşti. R bloğunun dört sayısal girdi ataması CSV ile karşılaştırıldı.
- Beş sütunun sırası veri sözlüğüyle, CSV özeti kaynak kaydındaki SHA-256
  ile eşleşti. Hesaplama girdi veri çerçevesini değiştirmedi.
- 19 hatalı girdi reddedildi: boş/iki satırlı veri, yanlış sütun adı/sırası,
  fazla sütun, eksik/sonsuz/mantıksal/metin fark, sıfır/negatif/eksik SE,
  sıfır/negatif df, α=0/1/5/−0,01 ve sonsuz sıfır hipotezi değeri.
- İşaret çevirme, fark ve SE'yi ikiyle çarpma, tahmin ve sıfır hipotezi
  değerine aynı sabiti ekleme, farkı sıfır yapma ve SE'yi yarılama sınandı.
  Alıştırmaların sayısal yanıtları kontrol edildi.
- α=0,01'de aynı p ile karar değişimi, yüzde 99 aralık, δ0=1 testi,
  pozitif kesirli df ve p=α eşitliğinde reddetmeme kontrol edildi.
  Kritik t'nin 1e-6 altı/üstünde test-aralık uyumu doğrulandı.
- t=−100, −10, −2,1, 0, 2,1, 10, 100 için kuyruk toplamı ve
  çift yönlü p=2×küçük kuyruk ilişkisi kontrol edildi; çift yönlü
  olasılıklar bu sınanan değerlerde pozitif kaldı.
- Paket geçici başka bir klasöre kopyalandı; Python kontrolü ve grafik
  üretimi geçti. Değiştirilmiş girdi, değiştirilmiş kontrol değeri ve
  ters sıralı kontrol tablosu ayrı ayrı başarısız çıkış üretti.
  Kaynak paket dosyaları bu sınamalar sırasında değişmedi.
- Python PNG'si açılarak incelendi; iki kuyruk, aralık uçları ve sıfır
  çizgisi görünür. Grafik açıklaması boyalı p bölgesi ile α ret bölgesini ayırır.

## İncelenen fakat çalıştırılmayanlar

- R kodunun CSV başvurusu, 20 satırlık çıktı düzeni, kuyruk yönleri ve
  parantez dengesi kaynak üzerinden incelendi; bu bir yorumlayıcı testi değildir.
- SPSS `CDF.T`/`IDF.T` işlevleri IBM belgeleriyle karşılaştırıldı; teknik
  bağlantılar örneğin README'sindedir. SPSS özet satırına formül uygular;
  ham gözlem uydurmaz. Otomatik girdi doğrulaması SPSS betiğinde bulunmaz.
- `analiz.sps` ve `analiz.sps.txt` dosyaları byte düzeyinde aynıdır.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda bulunmuyor; betikleri bu ortamda çalıştırılmadı.
R grafiği veya SPSS `.sav`/`.spv` çıktısı üretilmedi. Python kontrollerinin
geçmesi üç yazılımda uçtan uca sonuç eşitliği kanıtı değildir.

1. R ortamında örnek klasöründen `Rscript cozum.R --check --grafik`
   çalıştırın; 20 değerin eşleştiğini doğrulayın, grafiği ve `sessionInfo()`yu kaydedin.
2. SPSS'te örnek klasörünü çalışma dizini yapıp `analiz.sps` çalıştırın;
   üç LIST tablosunu kontrol CSV'siyle karşılaştırın. Ekran yuvarlaması ve
   değer etiketlerini dikkate alın. Sürümü ve gerçek kontrol sonucunu kaydedin.
3. Model ve örnekleme varsayımlarını gerçek bir araştırmaya uygulamadan önce
   ayrıca denetleyin; bu öğretim özeti o doğrulamaların yerine geçmez.

## Bütünlük ve yayın

`MANIFEST.json`, kendisi dışındaki B09 dağıtım dosyalarının SHA-256
özetlerini listeler. Dosyalar değişirse manifest yenilenmeli; değiştirilmiş
kod için eski doğrulama kaydı kanıt sayılmamalıdır. SPSS dosyası taşınmazsa
`.sps.txt` kopyasından `.sps` adıyla geri getirilebilir.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Kitabın LaTeX dosyaları
bu paket için değiştirilmedi; PDF derlemesi gerekmedi.