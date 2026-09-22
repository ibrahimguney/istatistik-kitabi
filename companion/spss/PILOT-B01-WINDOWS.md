# Bölüm 1 pilotu — IBM SPSS Statistics 29 / Windows

12 Eylül 2026'da kullanıcı tarafından paylaşılan SPSS ekran görüntüsünde
(`prism-uploads/image_14.png`, kitap projesinde; ZIP'e dahil değildir)
CSV üzerinden temel analiz sonuçları beklenen değerlerle eşleşti:
395 kayıt, GP 349 / MS 46, F 208 / M 187, g3 ortalaması 10,42 ve
standart sapması 4,581. Kullanıcı çıktıyı yerel spss klasörüne kaydettiğini
bildirdi. Daha sonra yüklenen `prism-uploads/b01-spss-sonuc.png.spv`
dosyasının XML yapısı incelendi: aktif veri yolu
`C:/B01-SPSS-CSV/companion/spss/sav/b01.sav`; değişken bilgileri,
değer etiketleri, frekanslar ve betimsel istatistik tabloları mevcut.
SPV içindeki ikili sayısal hücreler burada çözümlenmedi.
`prism-uploads/image_16.png` ile dört değişkenin N, minimum, maksimum,
ortalama ve standart sapmaları ayrıca görsel olarak doğrulandı:
yaş 395/15/22/16,70/1,276; g1 395/3/19/10,91/3,319;
g2 395/0/19/10,71/3,762; g3 395/0/20/10,42/4,581.
Valid N (listwise) 395'tir.

Excel içe aktarmada “All sheets in Excel file appear to be empty” hatası
alındı; bu sorun çözülmüş sayılmıyor. Bu sürüm CSV'yi varsayılan kullanır.
Yeni CSV paketiyle kullanıcı ortamından alınan betimsel sonuçlar doğrulandı.
SAV yolu çıktıda görülüyor; SAV dosyasının kendisi ve tüm değer etiketleri
ayrıca incelenmedi. Bu kanıt SPSS 29 sürüm doğrulaması değildir.
Burada IBM SPSS çalıştırılmadı.

12 Eylül 2026'da yüklenen `prism-uploads/b01_R.txt` içindeki R sonuçları
projedeki `companion/spss/csv/b01.csv` üzerinden yeniden hesaplanan
değerlerle karşılaştırıldı. Okul (GP 349 / MS 46) ve cinsiyet
(F 208 / M 187) frekansları ile age, g1, g2 ve g3 değişkenlerinin
N, ortalama, standart sapma, minimum ve maksimum değerleri, çıktıda
gösterilen altı ondalık basamakta eşleşti. SPSS ekranındaki yuvarlanmış
betimsel değerlerle de uyumludur. Dosya frekans tablolarıyla başlıyor;
`str(d)` ve eksik değer sayımlarının çıktıları bulunmadığından bunlar
kullanıcının R çıktısından ayrıca doğrulanmadı.

12 Eylül 2026'da yüklenen `prism-uploads/b01_python.txt` incelendi:
395 satır ve 10 sütun mevcut; tüm sütunlarda eksik değer sayısı sıfır.
Okul ve cinsiyet frekansları beklenen sayılarla eşleşti. Dört değişkenin
20 betimsel hücresi, hem CSV'den yeniden hesaplanan değerlerle hem de
R çıktısıyla gösterilen altı ondalık basamakta eşleşti; SPSS ekranındaki
yuvarlanmış değerlerle de uyumludur. Çıktıda hata mesajı bulunmuyor.
Çıktının bildirdiği ortam: Python 3.14.0, pandas 2.3.3, NumPy 2.4.0,
SciPy 1.16.3. Temel sonuç karşılaştırması tamamlandı; yukarıdaki Excel,
SAV ve R çıktı kapsamı sınırlamaları geçerliliğini koruyor.
Doğrulanmış frekans ve betimsel tablolar ile ortak rapor
`chapters/spss/b01.tex` dosyasına işlendi.

## 1. Paketi açın

Güncel `B01-PAKET-OLUSTUR.py.txt` dosyasını Python ile çalıştırın;
yanında `b01-windows-spss29-csv.zip` oluşturur. Eski ZIP'in üzerine yazmaz.
ZIP'in tümünü yeni bir klasöre çıkarın; önceki sonuç dosyalarını koruyun.
Örneğin `C:/B01-SPSS-CSV` klasörünün içinde `companion`, `b01.R`, `b01.py`
ve bu README bulunmalı; iç içe ikinci bir paket klasörü olmamalı.
Farklı klasör kullanabilirsiniz; aşağıdaki örnek yolu buna göre değiştirin.
Dosyaları ZIP içinden çalıştırmayın. Klasörün yazılabilir olması gerekir.

Bu pilot internete bağlanmadan, paket içindeki sabit veri kopyasıyla çalışır.
SPSS, R ve Python aynı CSV dosyasını okur. Excel kopyası ve
`open-b01-excel.sps` alternatif deneme için korunur; varsayılan analiz
bunları kullanmaz.
Ham `student-mat.csv` dosyasını bu hazırlanmış CSV'nin yerine koymayın.

## 2. Önce IBM SPSS 29

Mevcut çalışmalarınızı kaydedin; komutlar aktif veri setini değiştirir.
Yeni bir Syntax penceresinde aşağıdaki komutu kendi klasörünüze uyarlayıp
çalıştırın (tırnaklar ve sondaki nokta gereklidir):

```spss
CD 'C:/B01-SPSS-CSV'.
```

Ardından `File > Open > Syntax` ile
`companion/spss/syntax/b01.sps` dosyasını açın ve `Run > All` seçin.
Bu dosya `open-b01.sps` dosyasını çağırır; CSV verisini açar, etiketleri
tanımlar, `companion/spss/sav/b01.sav` dosyasını oluşturur ve analiz yapar.
Aynı adla mevcut SAV varsa üzerine yazılır.

Beklenen tablolar: veri sözlüğü, okul ve cinsiyet frekansları,
yaş ile g1/g2/g3 betimsel istatistikleri. Hata/uyarı varsa silmeyin.
Çıktı penceresinde dosyayı `companion/spss/b01-csv-sonuc.spv` adıyla kaydedin.
`File > Export` yolunda PDF biçimini ve tüm çıktıları seçerek ayrıca
`companion/spss/b01-csv-sonuc.pdf` oluşturun. Yalnız seçili tabloyu dışa aktarmayın.
PDF'yi ve çalıştırdığınız `.sps` dosyalarını projeye yükleyin;
SPV'yi de arşiv için saklayın. Önce bu sonuçları birlikte kontrol edelim.

## 3. Sonra R

R çalışma dizinini paketin açıldığı klasör yapın. R konsolunda:

```r
setwd("C:/B01-SPSS-CSV")
sink("b01_R.txt", split=TRUE)
source("b01.R", echo=TRUE)
sessionInfo()
sink()
```

`source` hata verirse yine `sink()` çalıştırıp çıktı yönlendirmesini kapatın;
hata mesajını da paylaşın. Kod yalnız temel R işlevlerini kullanır.
`b01_R.txt` ve `b01.R` dosyalarını gönderin. R burada çalıştırılmadı.

## 4. En son Python

Paket klasöründe Windows terminali açın. Python ortamınızda pandas,
NumPy ve SciPy bulunmalıdır. Kitaptaki kod aynen bu bağımlılıkları kullanır.

```text
python b01.py > b01_python.txt 2>&1
```

`python` yerine yalnız `py` çalışıyorsa aynı komutta onu kullanın.
Dosyanın sonunda Python ve paket sürümleri de yazdırılır.
`b01_python.txt` ve `b01.py` dosyalarını gönderin. Eksik paket veya başka
hata olursa hata metnini paylaşın; onu da çıktı dosyası kaydeder.

## Kontrol listesi ve yorum

- Aynı 395 kayıt, aynı 10 değişken, eksik hücre yok.
- Okul: GP 349, MS 46; cinsiyet kodları: F 208, M 187.
- g3 ortalaması yaklaşık 10,415; örneklem standart sapması 4,581.
- g3=0 kayıtları korunur; sıfır, eksik veri kodu değildir.
- studytime 1–4 sıralı kategori kodudur, doğrudan saat sayısı değildir.
- Bunlar karşılaştırma değerleridir; kullanıcı CSV ekran görüntüsüyle yapılan
  kontrol yukarıda belirtilmiştir. R çalıştırma kanıtı değildir.

13 Eylül 2026 eşleştirmesinde pilot kodları güncel B01 kitap bloklarından
yeniden üretildi. Paylaşılan çıktıların karşılaştırmaları kitapta
IBM SPSS → R → Python sırasıyla yer alır; bu, burada SPSS/R'nin yeniden
çalıştırıldığı anlamına gelmez. Pilotun dokuz dosyası ayrı manifestle
denetlenir; önceki manifestler kitap projesinde korunur.

## Kaynak ve dönüşüm

Cortez, P. (2008). Student Performance. UCI Machine Learning Repository.
DOI: 10.24432/C5TG7T. Lisans: CC BY 4.0.
https://archive.ics.uci.edu/dataset/320/student+performance
https://creativecommons.org/licenses/by/4.0/

Matematik dosyasından seçilmiş değişkenler yeniden kodlandı; dosya içi id ve
öğretim amaçlı pass10 eklendi. Excel'in `sozluk` ve `kaynak` sayfalarını
okuyun. Veriler iki okulun gözlemsel kayıtlarıdır; bu özetler daha geniş
bir evrene temsil veya nedensellik kanıtı sayılmaz.

SPSS 29 menü ve dışa aktarma başvuru kaynağı:
IBM SPSS Statistics 29 Core System User's Guide, “Working with output”.
https://www.ibm.com/docs/SSLVMB_29.0.0/pdf/IBM_SPSS_Statistics_Core_System_User_Guide.pdf

`manifest.json`, paketteki veri ve kodların SHA-256 özetlerini içerir.
Bu özetler dosya sürümünü izlemek içindir; SPSS uyumluluk testi değildir.