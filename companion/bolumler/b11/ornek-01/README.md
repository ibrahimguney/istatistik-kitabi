# Örnek 01 — Özetlerden iki farklı t testi

## Veri yapısı ve varsayımlar

`veri.csv` içindeki ilk altı sütun bağımsız grupların özetleridir. Sonraki
üç sütun ayrı bir eşleştirilmiş örneğin tam çift sayısı, ortalama farkı ve
**fark puanlarının** örneklem standart sapmasıdır. `alfa` her iki örnek
soruya uygulanan anlamlılık düzeyidir. Sayısal ayrıntılar veri sözlüğündedir.

Welch yaklaşımı eşit evren varyansı gerektirmeden iki bağımsız grup
ortalamasını karşılaştırır; bağımsızlık gereksinimini ortadan kaldırmaz.
Eşleştirilmiş testte farklı kişilerin farkları bağımsız olmalıdır; küçük
örneklemde farkların dağılımı ve aykırı değerler önemlidir. Ön/son sütunların
ayrı standart sapmaları tek başına farkların standart sapmasını vermez.
Özet veriden Levene testi, normallik grafiği veya eşleşme denetimi yapılmaz.
Welch testi sonradan bir Levene p-değerine bakılarak seçilmemiştir.

Hacimler en az 2 tam sayı, α 0 ile 1 arasında olmalıdır. Bu öğretim paketi
üç standart sapmanın da pozitif olmasını şart koşar; sabit veri grupları
kapsam dışıdır. Negatif veya sıfır ortalama farkı geçerlidir. Girdi
kontrolleri Python/R'de yapılır; SPSS'te ayrıca elle kontrol gerekir.

## Çalıştırma

Komutları **bu örnek klasöründe** çalıştırın:

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

Python NumPy, pandas, SciPy; grafik için Matplotlib kullanır. R standart
kurulum işlevlerini kullanır. Betikler paket kurmaz veya veri indirmez.
`--check`, 34 değeri etiket/sıra ve 1e-9 mutlak/bağıl toleransla kontrol
eder; uyuşmazlıkta başarısız çıkış verir. Sürüm bilgileri konsola yazılır.
`--grafik` yalnız kendi PNG'sini oluşturur/yeniler; girdi CSV değişmez.

Alıştırmalar için klasörün kopyasını alın, girdiyi değiştirip `--check`
olmadan çalıştırın. Özgün kontrol CSV'si yeni veri için geçerli değildir;
yalnız kontrol geçsin diye referans değerleri değiştirmeyin.

## Çıktı haritası

- `girdi`: 10 özet/ayar değeri.
- `welch`: Varyans katkıları, ortalama farkı ve 10 test/aralık sonucu; 13 satır.
- `eslesmis`: 10 test/aralık sonucu ve d_z; 11 satır.

`reddet_cift=1` H0 reddedilir, 0 reddedilemez demektir. Karar tam duyarlıklı
p<α ile verilir; eşitlikte ret yoktur. Aralıklar `1-alfa` düzeyindedir.
Her testte sıfır hipotezi ilgili evren ortalama farkının sıfır olmasıdır.
İki ayrı öğretim sorusunda α=0,05 kullanımı birden çok test için ailece
hata oranının %5 kontrol edildiği iddiası değildir; çoklu test düzeltmesi yapılmaz.

Python ve R özet formüllerini uygular; özetleri ham gözlem gibi
`ttest_ind`, `ttest_rel` veya `t.test` işlevlerine vermez. Ham veriyle
çalışılırken Welch için `equal_var=False` / `var.equal=FALSE`, eşleşmiş
vektörler için `ttest_rel` / `paired=TRUE` kullanılır. Bu pakette hazır
ham gözlem bulunmadığından bu çağrılar çalıştırılmaz. Welch serbestlik
derecesi tam sayıya yuvarlanmaz. Bağımsız gruplar için pooled Cohen d veya
Hedges g üretilmez; standartlaştırılmamış fark raporlanır. d_z yalnız
farkların standart sapmasını payda alan eşleştirilmiş etki büyüklüğüdür.

## SPSS

1. Açık dosyalarınızı kaydedin; çalışma dizinini bu örnek klasörüne ayarlayın.
2. `analiz.sps` dosyasını çalıştırın. Dosya görünmüyorsa `analiz.sps.txt`
   kopyasını UTF-8 ile `analiz.sps` adıyla kaydedin.
3. CSV'nin tek satır, doğru sütun sırası ve geçerli değerlerle geldiğini
   elle denetleyin. Betik özet satırını T-TEST'te ham kişi gibi kullanmaz;
   COMPUTE, CDF.T ve IDF.T ile formülleri uygular.
4. Dictionary ve üç LIST tablosunu kontrol CSV'siyle karşılaştırın.
   İlk tablo 10 girdiyi, ikinci Welch'in 13 değerini, üçüncü eşleştirilmiş
   testin 11 değerini aynı sırayla gösterir. Sürümü ve sonucu kaydedin.

SPSS'te `w_` öneki Welch, `es_` eşleştirilmiş testtir; `se` standart hata,
`df` serbestlik, `p` çift yönlü p, `kritik` kritik t, `pay` hata payı,
`alt/ust` aralık uçları, `reddet` ret göstergesidir. `w_fark` kontrolün
Welch `fark` alanıdır. `katki_1`, `katki_2`, `dz` adları aynıdır.
Ekran yuvarlaması ve değer etiketlerini dikkate alın.

SPSS otomatik girdi doğrulaması, `--check` veya grafik sunmaz; bu ortamda
çalıştırılmadı. Hazır `.sav`/`.spv` çıktısı üretilmedi.

## Teknik başvurular

- [SciPy özet istatistiklerden Welch testi](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind_from_stats.html)
- [R t.test: var.equal ve paired seçenekleri](https://www.stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html)
- [IBM CDF.T ve IDF.T işlevleri](https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=reference-glossary)

Belgelerin incelenmesi yorumlayıcı testi değildir.
[Açıklamalı çözüm](cozum.md) · [Grafik açıklaması](grafik-aciklamasi.md)