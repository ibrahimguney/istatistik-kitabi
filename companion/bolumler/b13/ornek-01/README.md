# Örnek 01 — Çalışma saati ve son test puanı

## Veri ve model

`veri.csv` 16 satır, `saat` ve `puan` olmak üzere iki sütundur. Her satırdaki
iki değer aynı gözleme aittir; sütunları birbirinden bağımsız sıralamayın.
Tekrarlanan (saat, puan) çiftleri otomatik silinmez; farklı gözlemler aynı
ölçümleri taşıyabilir. Bağımsızlık ve kimlik doğrulaması bu sayılardan çıkarılamaz.

Betikler en az üç tamamlanmış sayısal satır, sonlu değerler, negatif olmayan
saat ve her iki değişkende değişkenlik gerektirir. Eksik satırlar sessizce
silinmez. Tam veya sayısal olarak tama yakın doğru üzerinde bulunan veride
artık varyansı güvenilir biçimde hesaplanamadığından bu çıkarım paketi durur.
Bu sınır, böyle verilerden betimsel bir doğru çizilemez anlamına gelmez.

Model sabit terimli tek açıklayıcılı OLS'dir. Doğrusal koşullu ortalama,
bağımsız hatalar ve sabit hata varyansı değerlendirilmelidir; klasik t ve
öngörü aralıklarının küçük örneklemdeki yorumu normal hata modeline dayanır.
Grafikleri üretmek bu koşulların sağlandığını kanıtlamaz. Pearson r'nin
klasik testi için de uygun örnekleme/dağılım varsayımları gerekir.

## Çalıştırma ve kontrol

Komutları **bu örnek klasöründe** çalıştırın:

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

Python NumPy, pandas, SciPy; grafik için Matplotlib kullanır. R standart
kurulumdaki `lm`, `confint` ve `predict` işlevlerini kullanır. Betikler
paket kurmaz veya veri indirmez; sürümler konsola yazılır.
`--grafik` kendi PNG'sini oluşturur/yeniler, kaynak CSV değişmez.

Kontrol tablosu 30 genel değer, 16 uydurulan değer ve 16 ham artık içerir.
`satir_01` gibi anahtarlar CSV satır sırasına karşılık gelir; kalıcı kişi
kimliği değildir. Satırları birlikte sıralamak genel modeli korur ama
satır bazlı kontrol eşleştirmesini değiştirir.

Çoğu değerde 1e-9 mutlak/bağıl tolerans uygulanır. `p_egim` için mutlak
tolerans **0**, bağıl tolerans **1e-8**'dir; yaklaşık 2,62e-11 olan sayı
sıfırla değiştirilirse kontrol başarısız olur. Etiketler, sıralar ve sonlu
olma da denetlenir. Uyuşmazlık başarısız çıkış verir.

Değişiklikleri klasör kopyasında yapın ve özgün referans için `--check`
kullanmayın. Betiklerin varsayılanı 6 saat ve %95 aralıktır; komut satırında
öngörü noktası seçeneği yoktur. Alıştırma hesabında Python/R
`model_hesapla(veri, yeni_saat=20)` işlevi kullanılabilir. Bu işlev matematiksel
öngörüyü verir; aralık dışında kullanımı güvenli bulduğu anlamına gelmez.
Grafik varsayılan 6 saati gösterir. α iki dilde `ALFA`, SPSS'te .975 kritik
kuantil ayarıyla %5'tir; değiştirildiğinde tüm yazılımların ayarları eşleştirilmelidir.

## Çıktılar

- `sxx`, `syy`, `sxy`: Merkezli kareler/çarpımlar toplamları; `sse`: artık kareler toplamı.
- `mse`: SSE/(n−2); `r_kare`: 1−SSE/Syy. Bu sabit terimli tek açıklayıcılı modelde R²=r².
- `egim`, `sabit`, standart hataları ve alt/üst sınırları: katsayı tahminleri ve %95 aralıklar.
- `t_egim`, `p_egim`: H0: eğim=0 için çift yönlü t testi, df=n−2.
- `ongoru`: 6 saatteki ortak nokta tahmini; `ortalama_alt/ust` evren ortalaması için,
  `birey_alt/ust` aynı modelden yeni bağımsız birey için aralıktır.
- `uydurulan` ve `artik`: her satır için tahmin ve gözlenen−tahmin farkı.

Standartlaştırılmış Beta ile puan/saat birimli eğim karıştırılmaz.
Korelasyonun klasik sıfır testi ile eğimin testi burada aynı sayısal p'yi
verir; paket ayrı korelasyon güven aralığı veya çoklu regresyon üretmez.

## SPSS

1. Açık dosyalarınızı kaydedin; çalışma dizinini bu örnek klasörüne ayarlayın.
2. Eksiksiz veri ve doğru saat/puan eşleşmesini elle doğrulayın. SPSS'in
   listwise eksik veri işlemi Python/R'nin eksik veri reddiyle aynı değildir;
   eksikli dosyada bu pilotun sonuçlarını karşılaştırmayın.
3. `analiz.sps` dosyasını çalıştırın; görünmüyorsa `analiz.sps.txt` kopyasını
   UTF-8 ile `analiz.sps` adıyla kaydedin. Betik Correlations ve Regression
   tablolarını, ardından formüllerle ek kontrol değerlerini üretir.
4. Coefficients tablosunda standartlaştırılmamış B ve %95 sınırlarını,
   Model Summary'de R²'yi okuyun. İlk LIST'te yerleşik regresyonun
   `uydurulan_spss`/`artik_spss` değerleri formülün `uydurulan`/`artik`
   değerleriyle yan yana bulunur; kontrol CSV'sindeki satırlarla eşleştirin.
5. `B13Ozet` kopyasının LIST tablosu 30 genel kontrolü verir. Küçük p
   bilimsel gösterimle yazdırılır. Ekrandaki `.000` değerini p=0 diye
   raporlamayın. Sonunda `B13Veri` yeniden etkinleştirilir.

SPSS'te otomatik `--check`, Python/R'deki girdi korumaları veya bu paketin
dört panelli grafiği yoktur. Kod bu ortamda çalıştırılmadı; `.sav`/`.spv`
verilmedi. Gerçek kontrol sonucunu ve sürümü doğrulama kaydına ekleyin.

## Teknik başvurular

- [SciPy linregress](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html)
- [R lm](https://www.stat.ethz.ch/R-manual/R-devel/library/stats/html/lm.html)
- [R predict.lm: güven ve öngörü aralıkları](https://www.stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.lm.html)
- [IBM REGRESSION](https://www.ibm.com/docs/en/spss-statistics/31.0.0?topic=reference-regression)

[Açıklamalı çözüm](cozum.md) · [Grafik açıklaması](grafik-aciklamasi.md)