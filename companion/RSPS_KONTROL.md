# R ve SPSS doğrulama akışı — 10 Eylül 2026

## Şu anda doğrulanan durum

17 paketin Python çözümleri 545 referans değeri geçti; 278 manifest girdisi
byte düzeyinde eşleşti. 17 `.sps` dosyası ve aynı içerikte metin yedeği var.
Bu çalışma kopyasında eksik olan 16 `.sps` dosyası yedeklerinden geri
getirildi; 222 dosyada yalnız eski manifestle eşleşen satır sonu biçimi
geri yüklendi. Mevcut manifestler değiştirilmedi. B01 için 13 girdilik
**yeni** manifest oluşturuldu; bu, geçmiş dosya özgünlüğünün kanıtı değildir.

- [Onarım kaydı](dosya-onarim-2026-09-10.json): Önce/sonra hash ve işlem nedeni.
- [Python/bütünlük sonucu](toplu-kontrol-onarim-2026-09-10.json).
- [R erişim sonucu](r-kontrol-2026-09-10.json): 17 paket **çalıştırılmadı**.
- [SPSS dosya hazırlığı](spss-hazirlik-2026-09-10.json): CSV başvuruları ve kopyalar kontrol edildi; SPSS çalıştırılmadı.

Rscript, R, SPSS ve PSPP komutları ortamda bulunamadı. Yeni yazılım kurulmadı.
Python'da başarılı hesap veya R sürücüsünün taklit çıktılarla sınanması,
gerçek R/SPSS çalıştırması değildir. Bölüm içindeki eski DOGRULAMA kayıtları
tarihsel kapsamlarını korur; bu rapor onların yerine yapılmamış test yazmaz.

## Windows R Console: Python gerektirmeyen seçenek

`r-toplu-kontrol.R.txt` dosyasını indirin. R Console'da
`source(file.choose(), encoding="UTF-8")` çalıştırıp önce bu metin betiğini
seçin. Betiğin açtığı ikinci pencerede bilgisayarınızdaki
`companion/bolumler/b01/ornek-01/cozum.R` dosyasını seçin.

B01 dahil 17 paket kontrol edilir; hepsi geçerse 545 pozitif referans
beklenir. Her paket bağımsız Rscript işleminde ve geçici veri kopyasında
çalışır. Pozitif kontrol geçince yalnız geçici kopyada bir referans
bozulur; betiğin bunu hata kodu 1 ile reddetmesi de aranır. Negatif testin
logunda hata bulunması bu nedenle beklenir. Paket kodlarının ANOVA dahil
mevcut toleransları korunur; otomatik olarak gevşetilmez.

`companion/r-toplu-sonuc-*` altında `ozet.csv`, R oturumu, paket logları
ve giriş dosyalarının MD5 kayıtları oluşur. MD5 kayıtları girdileri
belgelemek içindir; paket SHA-256 manifest denetiminin yerine geçmez.
Kaynak veriler/referanslar ve önceki sonuç klasörleri değiştirilmez.
Eksik/hatalı paket diğer paketlerin denetlenmesini engellemez. Grafik,
benzetim ve SPSS bu testin kapsamı dışındadır. `GECTI` için hem pozitif
hem negatif kontrol gerekir; `eslesen` yalnız pozitif kontrol sayısıdır.

Bu yardımcı burada R/Windows üzerinde çalıştırılmadı. Kaynak akışı ve
paket sözleşmeleri incelendi; gerçek çalışma sonucu kullanıcının
bilgisayarından gelecek `ozet.csv` ve loglarla değerlendirilecek.
B01 için paylaşılan ekran görüntüsünde 18 kontrolün R 4.6.0 ile geçtiği
görüldü; bu, diğer paketlerin veya negatif testin geçtiğini göstermez.

## R: kurulu olduğu bilgisayarda toplu çalıştırma

Tüm `companion` klasörünü aynı dizin yapısıyla bilgisayarınıza alın. Proje
kökünde, Python ve Rscript erişilebilirken:

```bash
python companion/bolumler/r_kontrol.py --rapor companion/r-sonuc-bilgisayar.json
```

Rscript PATH'te değilse `--rscript` seçeneğine proje kökünden göreli çalıştırılabilir
dosya yolu verilebilir. Script her örneği geçici bağımsız klasöre kopyalar,
`Rscript --vanilla cozum.R --check` çalıştırır; başarı mesajındaki kontrol
sayısını referans CSV'nin satır sayısıyla karşılaştırır. Ardından **yalnız
geçici kopyada** ilk referans değerini değiştirerek kodun bunu reddettiğini
kontrol eder. Kaynak veri ve referanslar değiştirilmez. Grafik/benzetim
seçenekleri bu toplu testin kapsamı dışındadır.

R oturum bilgisi, giriş dosyalarının hash'leri, stdout/stderr, çıkış kodları
ve pozitif/negatif testler JSON'a kaydedilir. Mevcut raporun üzerine yazılmaz.
Çıkış kodu 0 tüm paketlerin geçtiğini; 1 test/çalıştırma hatasını; 2 Rscript'in
bulunmadığını belirtir. İkinci çalıştırmada yeni rapor adı seçin. İlk R testinde
hata çıkarsa referansları değiştirmeyin; raporu incelemek üzere paylaşın.
ANOVA çözümünün Tukey için belgelenmiş toleransları korunur.

R kaynak belgesi: `https://www.stat.ethz.ch/R-manual/R-devel/library/utils/html/Rscript.html`

## SPSS: gerçek uygulamada yapılacak kontroller

[spss-kontrol-formu.csv](spss-kontrol-formu.csv) başlangıçta bütün paketleri
`calistirilmadi` olarak listeler. Bir satırı yalnız gerçek sonuç elde edince
uygun durumla güncelleyin. Dosyanın var olması veya sözdizimi renklendirmesi
bir çalışma testi değildir.

Her paket için:

1. Önce kendi açık çalışmanızı kaydedin. Ayrı bir temiz SPSS oturumunda
   çalışma dizinini ilgili `companion/bolumler/<paket>/ornek-01` klasörüne getirin.
2. O klasördeki `analiz.sps` dosyasının tamamını çalıştırın; Hata/Uyarı
   mesajlarını inceleyin. `.sps` görünmüyorsa `.sps.txt` yedeğini kullanmadan
   önce dosya bütünlüğünü onarın; yalnız uzantıyı değiştirmek hash farkını çözmez.
3. Üretilen tabloları **o paketin** `beklenen-sonuclar.csv`, `cozum.md` ve
   README açıklamalarıyla karşılaştırın. Çıktıda olmayan bir ölçüyü geçti
   saymayın; formda karşılaştırılan ölçü sayısını ve eksik/farklı ölçüleri yazın.
4. Yüzde/oran birimlerini, varyansın paydasını, fark yönünü, tek/çift yönü,
   süreklilik düzeltmesini ve yuvarlamayı eşleştirin. Ekranda az basamakla
   gösterilmiş p değerini tam duyarlıklı CSV gibi değerlendirmeyin.
5. SPSS sürümü, çalışma tarihi ve tüm hata/uyarıları forma yazın. Viewer
   çıktısını paket kodu içeren ayrı bir `.spv` dosyasına kaydedin. Örnek
   klasöründe `OUTPUT SAVE OUTFILE='b01-kontrol.spv'.` kullanılabilir;
   başka bir pakette kodu değiştirin ve mevcut sonuç dosyasını ezmeyin.
6. Formu, SPV çıktılarıyla birlikte paylaşın. R raporu SPSS'in geçtiğini,
   SPSS'te bir tablonun eşleşmesi bütün referansların geçtiğini kanıtlamaz.

SPV ve R sonuçlarını dağıtım paketlerinin dışında saklayın; yeni dosyalar
paket manifestinde listelenmez. Bir pakette yalnız bazı ölçüler görünüyorsa
formda `kismi`; hata varsa `basarisiz`; tüm karşılaştırmalar tamamlanmışsa
`gecti` yazın. Hiç çalıştırılmamış satır `calistirilmadi` kalmalıdır.

IBM çıktı kaydetme örneği: `https://www.ibm.com/docs/en/spss-statistics/32.0.0?topic=reference-output-new`

## Yayın durumu

Dosya bütünlüğü engelleri bu çalışma kopyasında giderildi; R ve SPSS'in
uçtan uca doğrulandığı iddiasıyla yayın yapılmamalı. Henüz GitHub'a yükleme
veya lisans ataması yapılmadı. Aktarım sonrası `python companion/bolumler/kontrol.py`
komutunu yeniden çalıştırın; dosya panelinin aktarım davranışı bu testle doğrulanmaz.

## Aktarımda dosya veya satır sonu kaybı olursa

`dagitim_onar.py.txt` dosyasını `companion` içinde tutun. Proje kökünden:

```bash
python companion/dagitim_onar.py.txt
python companion/dagitim_onar.py.txt --uygula
python companion/bolumler/kontrol.py
```

İlk komut yalnız planı gösterir. İkinci komut, tüm dosyalar için ön inceleme
başarılıysa, eksik `.sps` dosyalarını ve yalnız kayıtlı hash'e eşlenebilen
satır sonlarını onarır. Bilinmeyen içerik farkında veya eksik manifestte
hiçbir dosyayı değiştirmeden durur. Yeni referans/manifest uydurmaz.
Bu araç geçici kopyada eksik dosya, satır sonu kaybı ve değiştirilmiş içerikle
sınandı. Kaynakta yapılan bilinçli düzenlemeleri geri almak için kullanılmaz.
## Bütün paketleri SPSS'te birlikte çalıştırma

B01'deki INSERT dosya erişimi sorunundan sonra, komut gövdeleri gömülü
[hazırlayıcı](spss-toplu-hazirla.R.txt) eklendi. R bu araçla yalnız yeni bir
çalıştırma klasörü oluşturur; analiz SPSS'te yapılır. [Ayrıntılı adımlar](SPSS_TOPLU_KONTROL.md)
ve ayrı PDF/SPV çıktılarıyla insan incelemesi gerekir. Birleşik betik
hataları otomatik olarak sınıflandırmaz ve kontrol formunu geçti olarak doldurmaz.