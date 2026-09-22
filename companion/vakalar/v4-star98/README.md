# V4 — Aynı sayımlar, farklı hedefler

Kontrol tarihi: 13 Eylül 2026. Bu paket mevcut STAR98 verisinin dar
betimsel uyarlamasıdır; yeni saha verisi, yeni regresyon veya evren için
güven aralığı üretmez. Kapsamlı sürümün çoklu regresyon bölümüne bağlıdır.

## Kaynak ve birim sınırı

statsmodels resmî veri açıklaması, STAR 1998 matematik sonucunu 9. sınıf
öğrencilerinin sayımları; satırları 303 birleşik okul bölgesi olarak tanımlar.
Aynı sayfanın Notes kısmı counties dediğinden idari birim adlandırması
çelişkilidir. Burada bölge sözcüğü Description tanımına dayanır; özgün
coğrafi liste veya saha birimleri bağımsız doğrulanmış sayılmaz.
Dağıtıcı bu dosyanın özgün kaynağın bir alt kümesi olduğunu belirtir.
Bu nedenle toplamlar bütün California veya ABD öğrencilerine genellenmez.

Kaynak: `https://www.statsmodels.org/stable/datasets/generated/star98.html`
(erişim 13 Eylül 2026); sayfanın gösterdiği eser Jeff Gill,
*Generalized Linear Models: A Unified Approach*. Bu aşamada özgün eserin
tam veri eki edinilmedi. NABOVE/NBELOW adları korunur; tam medyana eşit
puanların işlemi kaynak açıklamasında ayrıntılandırılmadığından yeni eşik
kuralı türetilmez. Payda yalnız bu iki sütunun toplamıdır.

Yerel kaynaklar `companion/data/raw/star98_statsmodels.csv` ve
`companion/data/clean/star98_districts.csv` değiştirilmeden okunur.
`companion/code/00_prepare_data.py` yerel DISTRICT_ID'yi sıradan üretir;
bu gerçek bölge kodu değildir. Sayım ve oran aktarımı anahtarla kontrol edilir.
Girdi hash'leri analyze.py içinde sabittir; manifest hem girdileri hem bu
paketin yedi dosyasını kapsar. Bu, sunucuyla yeni bayt karşılaştırması değil,
yerel veri sürümünün kaydıdır.

Yerel `companion/data/dictionaries/provenance.txt` ve dağıtıcı, özgün yazarın
haklarını koruduğunu ve izinli dağıtımı belirtir. Bu uyarlama yeni bir lisans
veya kitap için bağımsız yeniden dağıtım izni vermez. Yeni ham kopya eklenmez;
mevcut kaynağa atıf ve dağıtım koşulları korunur. Yayın öncesi izin denetimi
ayrı kabul maddesidir.

## Analiz tanımı

303 satırın tamamı; NABOVE ve NBELOW sonlu, eksiksiz, negatif olmayan
tamsayılar; toplam pozitif olmalıdır. Geçerli sıfır pay korunur; eksik
değer doldurulmaz, uygunsuz satır otomatik çıkarılmaz. Eşit ağırlıklı
oran ortalaması ile toplam NABOVE / toplam (NABOVE + NBELOW) hesaplanır.
İki hedef aynı veriyle farklıdır; büyüklük ağırlığı örnekleme ağırlığı değildir.
Örnekleme/bağımsızlık modeli kurulmadığından p veya güven aralığı yoktur.

```sh
python -B companion/vakalar/v4-star98/analyze.py
python -B companion/vakalar/v4-star98/verify.py
```

İlk komut yalnız `aggregates.csv` ve `results.json` üretir; manifesti
yenilemez. İkinci komut standart CSV okuyucusu ve tam rasyonel aritmetikle
sonuçları bağımsız hesaplar; giriş kapılarını ve kaynak eşleşmesini denetler.
Sürüm/hash değişirse fark incelenmeden manifest yenilenmemelidir.

`synthetic-margins.csv` iki tamamen yapay 100 kişilik tabloyu içerir.
Her birinde 50 düşük gelirli ve 50 diğer kişi; toplam 50 üst, 50 alt
sonuç vardır. Buna rağmen grup içi oran farkı birinde +0,6, diğerinde
−0,6'dır. Bunlar STAR98'in gerçek bireyleri değildir; gerçek analize eklenmez.
Gösterim, toplulaştırılmış marjinlerden bireysel ilişkinin belirlenemediğini
anlatır; tek başına gerçek veride Simpson terslenmesi bulunduğu iddiası değildir.

R/SPSS çalıştırılmaz; mevcut regresyon katsayıları değiştirilmez. Öğrenci
pilot çalışması yapılmadı. Birim adlandırması ve yayın izni sınırlılıkları
nedeniyle bütün kaynak kabul ölçütlerinin kapandığı iddia edilmez.