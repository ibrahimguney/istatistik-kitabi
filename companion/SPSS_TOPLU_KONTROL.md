# SPSS toplu çalıştırma — 10 Eylül 2026

## Neden ayrı bir hazırlayıcı var?

B01'de `INSERT FILE='analiz.sps.txt'` dosya erişim hatası verdi; aynı
komutlar doğrudan Syntax penceresine yapıştırılınca çıktı oluştu. Bu nedenle
hazırlayıcı, 17 bölümün mevcut SPSS komutlarını kendi içinde taşır ve tek
bir çalıştırma dosyasında birleştirir. Kullanıcının bilgisayarında bölüm
başına `.sps` veya `.sps.txt` bulunması gerekmez; CSV girdileri gerekir.
Kitabın veya bölüm paketlerinin kaynak dosyaları değiştirilmez.

## 1. R'de hazırlık

`companion/spss-toplu-hazirla.R.txt` dosyasını bilgisayarınıza indirin.
R Console'da:

```r
source(file.choose(), encoding = "UTF-8")
```

İlk pencerede bu hazırlayıcıyı, ikinci pencerede bilgisayarınızdaki
`companion/bolumler/b01/ornek-01/cozum.R` dosyasını seçin. R burada analiz
**yapmaz**; paket kökünü bulur, gerekli CSV'leri kontrol eder ve yeni bir
`companion/spss-toplu-sonuc-*` klasöründe kopyalarını oluşturur. Kopyalar
MD5 ile kaynaklarıyla karşılaştırılır; bu kayıt paket SHA-256 denetiminin
yerine geçmez. Eksik CSV varsa hazırlık durur; eksik değer uydurulmaz.

Yeni klasörde şunlar hazırlanır:

- `spss-toplu.sps` ve aynı içeriğin `spss-toplu.sps.txt` yedeği.
- Bölüm başına `b02-tek.sps.txt` gibi ayrı tekrar çalıştırma dosyaları.
- `girdiler/<paket>/` içinde yalnız kullanılan CSV'ler ve referans tablosu.
- `kontrol-formu.csv`, girdi MD5 kayıtları ve hazırlayan R oturumu.
- `ONCE-OKUYUN.txt`.

Başlangıçta kontrol formunun bütün satırları `CALISTIRILMADI` durumundadır.
B01 önceki ekran görüntüsünde kontrol edilmiş olsa da bu yeni toplu koşunun
henüz gerçekleştiği varsayılmaz. Referans sayıları toplamı 545'tir; SPSS
bu referansların tümünü otomatik olarak karşılaştırmaz.

## 2. SPSS'te çalıştırma

**Önce açık veri, Syntax ve Viewer çalışmalarınızı kaydedin. Temiz bir SPSS
oturumu kullanın.** Hazırlanan betik `NEW FILE` ve yeni veri okuma komutları
kullanır; açık ve kaydedilmemiş çalışmanız varken başlatmayın.

R'nin ekranda gösterdiği yeni klasördeki `spss-toplu.sps` dosyasını SPSS
Syntax penceresinde açın. `Run > All` ile dosyanın tamamını çalıştırın.
Dosyayı UTF-8 olarak açın; Türkçe karakter içeren yolları kontrol edin.
Elle CD yolu girmeniz veya INSERT kullanmanız gerekmez: hazırlayıcı,
seçtiğiniz yerel klasörden gerekli yolları üretir. Her bölüm başlamadan
boş veri oluşturulur, ondalık ayırıcı nokta seçilir ve bölümün girdi
klasörüne geçilir; bölümün özgün hesap komutları korunur.

Her bölüm ayrı Viewer belgesine yönlendirilir. Betik, bölüm sonunda
`b01.spv` / `b01.pdf` gibi iki çıktı kaydetmeyi dener. Sonuçlar yeni
`spss-toplu-sonuc-*` klasörünün kökündedir. `b01`–`b14`, `bootstrap`,
`coklu-regresyon`, `anova` için toplam 17 çift hedeflenir.

**SPV/PDF oluşması, komutların hatasız veya sonuçların doğru olduğunu
kanıtlamaz.** Dosyalar hata mesajları da içerebilir. Akış bütün paketleri
çalıştırmayı dener; otomatik `GECTI` yazmaz. Hata, eksik çıktı veya kesilen
akış varsa diğer paketlerin geçtiğini varsaymayın.

Aynı SPSS betiğini ikinci kez çalıştırmak kendi sonuç dosyalarının üzerine
yazar. Yeni deneme için R hazırlayıcısını yeniden çalıştırın; yeni sonuç
klasörü oluşturulur. Paketlerin kaynak CSV'leri değiştirilmez.

## 3. Paylaşım ve karşılaştırma

PDF'leri ZIP içinde paylaşın; bütün SPV dosyalarını da bilgisayarınızda
saklayın. PDF dışa aktarması başarısızsa ilgili Viewer ekranını ve hata
mesajını paylaşın. İnceleme sırasında frekanslar, paydalar, test yönleri,
yüzde/oran birimleri, aralıklar ve mevcut toleranslar bölüm bazında
karşılaştırılmalıdır. Yeni çalışma R sonuçlarını değiştirmez; R'nin
başarılı olması SPSS'in doğrulandığı anlamına gelmez.

`kontrol-formu.csv` gerçek inceleme sonrası doldurulur. Görünmeyen veya
karşılaştırılmamış ölçüleri geçti saymayın. SPSS sürümünü ayrıca bildirin.

## Burada yapılan hazırlık kontrolleri

- 17 gömülü komut gövdesi kaynak `.sps.txt` dosyalarıyla satır düzeyinde eşleşti.
- CSV başvuruları ve toplam 545 referans satırı kontrol edildi.
- Geçici kopyalarda bütün gerekli girdilerin byte düzeyinde eşitliği sınandı.
- Bölümler arasında adlandırılmış veri kümelerinin çakışmadığı kontrol edildi.
- R metninde tırnak/parantez dengesi ve üretim akışı incelendi.

Bu ortamda R veya IBM SPSS bulunmadığından hazırlayıcı R'de, birleşik betik
SPSS'te çalıştırılmadı. Bu incelemeler gerçek yorumlayıcı testi değildir.
Kaynak dosya hash'leri `spss-toplu-kaynaklar.json` içindedir; bölüm komutları
değişirse hazırlayıcı da güncellenmelidir. GitHub'a yükleme yapılmadı.

## IBM kaynakları

- OUTPUT NEW: `https://www.ibm.com/docs/en/spss-statistics/31.0.0?topic=reference-output-new`
- OUTPUT SAVE: `https://www.ibm.com/docs/en/spss-statistics/31.0.0?topic=reference-output-save`
- OUTPUT EXPORT: `https://www.ibm.com/docs/en/spss-statistics/31.0.0?topic=reference-output-export`