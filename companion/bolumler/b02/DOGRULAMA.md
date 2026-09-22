# B02 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: dört öğrencilik `ornek-01` öğretim verisi.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, pandas 2.3.3 ile `python cozum.py --check`
  başarıyla çalıştı; 23 kontrol değeri 1e-9 mutlak/bağıl toleransla eşleşti.
- Ortak CSV, Bölüm 2'deki Python ve R bloklarının değerleriyle ayrı ayrı
  karşılaştırıldı; üç sütun ve dört gözlem aynı.
- Okul türünün sırasız kategori, sınıfın 1 < 2 < 3 düzeninde sıralı kategori
  olarak tutulduğu Python'da doğrulandı.
- Hesaplama özgün veri çerçevesini değiştirmiyor; sütun sırası sözlükle aynı.
- On geçersiz girdi reddedildi: boş veri, yanlış sütun adı, yanlış sütun sırası,
  eksik puan, eksik sınıf, sonsuz puan, bilinmeyen okul etiketi, sınıf 4,
  sınıf 1.5 ve sayısal olmayan puan.
- Genel toplam 298 ve devlet okulu toplamı 217, CSV kayıtlarından bağımsız
  temel aritmetik hesabıyla doğrulandı.
- Yeni `Ozel,3,85` satırı için genel ortalama 76,6, özel okul ortalaması 83,
  özel okul oranı 0,40 ve sınıf frekansları 2/1/2 olarak doğrulandı.
- Özel okul kaydı çıkarılınca o kategorinin frekans/oranı 0, ortalaması
  `NaN` oldu; boş grup yanlışlıkla sıfır puanla temsil edilmedi.
- Paket girdileri geçici başka bir klasöre kopyalanıp Python kontrolü
  çalıştırıldı; bu sınama kitabın dizin düzenine bağımlılık olmadığını gösterdi.
- Aynı kopyada değiştirilmiş veri ve değiştirilmiş beklenen sonuç dosyası
  ayrı ayrı `--check` başarısızlığı oluşturdu.

## İncelenen fakat çalıştırılmayanlar

- R kodunun parantezleri, CSV okuma, kategori sırası ve 23 satırlık çıktı
  düzeni kaynak üzerinden incelendi. Bu bir R yorumlayıcısı testi değildir.
- SPSS'te `sinif` için ORDINAL tanımı ve yalnız `puan` için ortalama
  hesaplanması kontrol edildi. MEANS ve VARIABLE LEVEL kullanımı IBM
  belgeleriyle karşılaştırıldı; kaynaklar örneğin README'sindedir.
- `analiz.sps` ve `analiz.sps.txt` dosyalarının byte düzeyinde aynı olduğu doğrulandı.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda bulunmuyor. R/SPSS betikleri bu ortamda
çalıştırılmadı; `.sav` veya `.spv` çıktısı üretilmedi. Python'un geçmesi,
üç yazılımda sonuç eşitliğinin uçtan uca doğrulandığı anlamına gelmez.

1. Kendi R ortamınızda örnek klasöründen `Rscript cozum.R --check` çalıştırın.
   23 değerin eşleştiğini ve sınıfın sıralı faktör olduğunu kontrol edin;
   `sessionInfo()` çıktısını kaydedin.
2. SPSS'te aynı klasörü çalışma dizini yapıp `analiz.sps` çalıştırın.
   Dictionary, Frequencies, Descriptives ve Means çıktılarını kontrol
   CSV'siyle karşılaştırın; yüzdeleri ve ekran yuvarlamasını dikkate alın.
3. Bu kontrollerin gerçek sonuçlarını ve sürümlerini kayda ekleyin.

## Bütünlük ve yeniden üretim

`MANIFEST.json`, B02 klasöründeki kendisi dışındaki dağıtım ve SPSS metin
yedeği dosyalarının SHA-256 özetlerini listeler. Belge veya kod değişirse
manifest yeniden üretilmeli; değiştirilmiş kod için eski doğrulama kaydı
kanıt sayılmamalıdır. SPSS dosyası taşınmazsa `.sps.txt` kopyası `.sps`
adıyla kaydedilebilir. Bu bölüm için yeni bir ZIP veya GitHub yayını
hazırlanmadı; bütün bölümler sonunda tek yayın paketi oluşturulacak.

Kitabın LaTeX dosyaları bu çalışmada değiştirilmedi; PDF derlemesi gerekmedi.