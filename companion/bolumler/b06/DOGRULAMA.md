# B06 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: 12 kişilik yapay çerçeveden basit n=6 ve
üç sınıfın her birinden n_h=2 tabakalı seçim; geri koyma yok, tohum 2026.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3 ve Matplotlib 3.10.8 ile
  `python cozum.py --check --grafik` çalıştı. 29 kontrol 1e-9 mutlak/bağıl
  toleransla eşleşti. Kontrol tablosu sayılarla birlikte seçilen kimlikleri de içerir.
- Kitabın Bölüm 6 Python listesi ayrı çalıştırıldı; çerçeve ve seçimler
  ortak CSV ile eşleşti. Sıralı basit kimlikler 1/3/6/8/11/12;
  tabakalı kimlikler 1/4/7/8/11/12 bulundu. R kaynağındaki 12 kişilik
  çerçeve, tohum ve altı kişilik basit seçim tasarımı kaynak üzerinden kontrol edildi.
- Veri sözlüğü dört CSV alanıyla aynı. Hesaplama girdi veri çerçevesini
  değiştirmedi. Satırların ters çevrilmesi aynı sonuç tablosunu verdi;
  sınıf Python'da 1<2<3 sıralı kategori olarak tutuldu.
- Bütün 924 basit ve 216 tabakalı sırasız örneklem kombinasyonlarıyla
  ayrıca sayıldı. Her bir kimlik basitte 462/924, tabakalıda 108/216
  oranında yer aldı; iki dahil edilme olasılığı da kesir aritmetiğiyle 1/2.
- Basit tasarımda dengeli 2/2/2 sayılı örneklemler 216 tane bulundu:
  216/924=18/77. Sabit kayıttaki denge tasarım garantisi diye yorumlanmadı.
- 1/2/3/4/5/6 kimliklerinden oluşan geçerli başka basit seçim kabul edildi;
  sınıf frekansları 4/2/0 çıktı. Sıfır gözlemli sınıf yanlışlıkla atılmadı.
  Tabakalı seçimde aynı tahsis reddedildi.
- 17 hatalı girdi reddedildi: boş veri, eksik satır, fazla satır, yanlış
  sütun adı, yanlış sütun sırası, eksik değer, sonsuz değer, metin,
  mantıksal sütun, yinelenen kimlik, kesirli kimlik, bilinmeyen sınıf,
  hatalı kimlik-sınıf eşleşmesi, kesirli gösterge, negatif gösterge,
  yanlış basit örneklem hacmi ve yanlış tabakalı tahsis.
- Farklı 4/8/12 tabaka hacimlerinde ikişer seçim için ağırlık toplamı
  24 olarak ayrıca hesaplandı. Bu farklı çerçeve ana pilot dosyasına uygulanmadı.
- Örnek klasörü geçici başka bir klasöre kopyalandı; `--check --grafik`
  orada da çalıştı. `python uret.py` kaynak CSV ile byte düzeyinde aynı
  yeni dosya üretti. İkinci çağrı üzerine yazmayı reddetti; dosya değişmedi.
  `../` içeren çıktı yolu reddedildi.
- Basit seçimde aynı sınıftaki 1 yerine 2 seçilerek farklı ama geçerli
  bir kayıt oluşturuldu. Normal analiz geçti, kimlikleri de karşılaştıran
  `--check` başarısız oldu. Değiştirilmiş kontrol değeri ve ters sıralı
  referans tablosu da ayrı ayrı sıfırdan farklı çıkış kodu verdi.
- Seçim haritası görsel olarak incelendi: 12 kimlik, üç sınıf sınırı,
  dolu/boş seçim noktaları ve etiketler okunur; noktalar ortak CSV ile uyumlu.
- SPSS dosyası ile `.sps.txt` yedeği byte düzeyinde aynı. Yerel belge
  bağlantıları, üretim kaydındaki veri özeti ve manifest SHA-256 değerleri denetlendi.

## İncelenen fakat çalıştırılmayanlar

`cozum.R` ve `secim.R` ayraç dengesi ve kaynak akışı incelendi. İlki ortak
seçim CSV'sini çözer; ikincisi R'nin kendi üreteciyle yeni seçim yapar.
Bu kaynak incelemesi R yorumlayıcısında çalıştırma testi değildir.

SPSS'te nominal/ordinal düzeyler, seçim göstergeleri, olasılık/ağırlık
sütunları ve her çıktı öncesinde ayrı geçici seçim incelendi. Kalıcı kayıt
silme veya `WEIGHT BY` uygulanmadı. pandas seçim ve R örnekleme resmi
belgelerine başvuruldu; bağlantılar örneğin README'sindedir.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda çalıştırılmadı. R grafiği veya yeni R seçim CSV'si,
`.sav`/`.spv` çıktısı üretilmedi. Python'un geçmesi üç yazılımda sonuç
aynılığının uçtan uca doğrulandığı anlamına gelmez.

1. R kurulu bilgisayarda örnek klasöründen `Rscript cozum.R --check --grafik`
   çalıştırın. Ortak CSV üzerinde 29 kontrolü, kimlik listelerini ve grafiği
   inceleyin; `sessionInfo()` çıktısını kaydedin.
2. Ayrı olarak `Rscript secim.R` çalıştırın. Her iki seçimde altı farklı
   kimlik, tabakalıda 2/2/2 ve ağırlık toplamı 12 koşullarını kontrol edin.
   R'nin yeni seçimini eski Python kimliklerine eşitlemeye çalışmayın.
3. SPSS'te çalışma dizinini örnek klasörü yapıp `analiz.sps` çalıştırın.
   Ortak kimlikleri, sınıf sayılarını, olasılık 0,5, ağırlık 2 ve seçilen
   altı kayıt üzerindeki ağırlık toplamı 12'yi kontrol edin. Veri setinde
   12 çerçeve satırının kaldığını doğrulayın ve sürümü kaydedin.
4. Gerçek çalışma sonuçlarını kayda ekleyin. Değişen kod/veri için eski
   doğrulama kaydını yeni sonuçların kanıtı olarak kullanmayın.

## Bütünlük ve yayın

`uretim-kaydi.json` CSV üretim ayrıntıları ve SHA-256 özetini,
`MANIFEST.json` kendisi dışındaki B06 dağıtım dosyalarının SHA-256
özetlerini içerir. Grafik ve SPSS metin yedeği dahildir. Dosya değişirse
ilgili özetler yeniden üretilmelidir. SPSS uzantısı arayüzde taşınmazsa
`.sps.txt` kopyasını aynı klasörde `.sps` adıyla geri oluşturun.

Kitabın LaTeX dosyaları değiştirilmedi; PDF derlemesi yapılmadı.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. B01 arşivleri B06'yı içermez.