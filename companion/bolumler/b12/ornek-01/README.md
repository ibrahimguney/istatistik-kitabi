# Örnek 01 — Dört hücreden Pearson bağımsızlık testi

## Veri ve koşullar

`veri.csv` sütunları `grup`, `sonuc`, `frekans`tır. Her kategori çifti
bir kez bulunmalıdır. Python/R satırları Birinci/İkinci ve Başarılı/Başarısız
sırasına getirir; dosyada satırların yer değiştirmesi sonucu değiştirmez.
Etiketler kodda ASCII ile `Birinci`, `Ikinci`, `Basarili`, `Basarisiz` yazılır.

Frekanslar negatif olmayan tam sayı sayımlarıdır; oran, yüzde veya örnekleme
ağırlığı değildir. Sıfır hücre mümkündür, fakat boş satır/sütun kabul edilmez.
Bütün beklenen sayılar en az 5 değilse Python/R bu pilotun Pearson hesabını
hata vererek durdurur. Bu, tüm ki-kare uygulamaları için evrensel tek kural
iddiası değil, kitaptaki kontrolün bu küçük paketteki kapsam sınırıdır.
Seyrek 2×2 tabloda tasarıma uygun Fisher kesin testi gibi yöntemler ayrıca
değerlendirilir; otomatik test değişimi veya kategori birleştirme yapılmaz.

Beklenen sayıların yeterli olması gözlemlerin bağımsız olduğunu kanıtlamaz.
Her kişi tek hücreye katkıda bulunmalı; tekrarlı/eşleşmiş ikili ölçümler bu
bağımsızlık testiyle analiz edilmemelidir. Kümeli veya karmaşık örneklem
ağırlıklarına ilişkin düzeltmeler bu paketin dışındadır.

## Çalıştırma

Tüm komutları **bu örnek klasöründe** çalıştırın:

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

Python NumPy, pandas, SciPy; grafik için Matplotlib kullanır. R standart
kurulum işlevlerini kullanır. Betikler paket kurmaz veya veri indirmez.
`--check` 32 değeri etiket/sıra ve 1e-9 mutlak/bağıl toleransla kontrol eder;
uyuşmazlıkta başarısız çıkış verir. Sürümler konsola yazılır.
`--grafik` kendi PNG'sini oluşturur/yeniler; girdi CSV değişmez.

Alıştırmalarda klasör kopyasını kullanın ve frekansları değiştirince
`--check` olmadan çalıştırın. Özgün kontrol dosyası yeni tablonun referansı
değildir; kontrol geçsin diye beklenen değerleri değiştirmeyin.

## Sonuç haritası

- Dörder `gozlenen`, `beklenen`, `katki`, `pearson_artik`, `satir_orani` satırı: 20 değer.
- Genel toplam, iki satır ve iki sütun toplamı: 5 değer.
- χ², df, p, Cramér V, en küçük beklenen frekans, α ve ret göstergesi: 7 değer.

Oranlar 0–1, grafikte ve SPSS Crosstabs'ta satır yüzdeleri 0–100 ölçeğindedir.
`reddet=1` H0 reddedilir, 0 reddedilemez demektir. Karar yuvarlanmamış p<0,05
ile verilir; eşitlikte ret yoktur. α bu sürümde sabit bir betik ayarıdır,
CSV sütunu veya komut satırı seçeneği değildir.

Python `correction=False`, R `correct=FALSE` kullanır. 2×2 tabloda yazılım
varsayılanındaki Yates düzeltmesi aynı sonuç değildir. R `residuals`,
(O−E)/√E Pearson artığıdır; `stdres` farklı ölçeklendirilmiş artıktır.
Bunlar karıştırılmaz, hücrelere otomatik ayrı anlamlılık yıldızı eklenmez.
Cramér V burada 2×2 için √(χ²/N)'dir; daha büyük tablo kodu değildir.

## SPSS

1. Açık dosyalarınızı kaydedin ve çalışma dizinini bu örnek klasörüne ayarlayın.
2. CSV'de tam dört kategori çifti, tam sayı frekanslar ve pozitif kenar
   toplamları olduğunu elle denetleyin. Beklenen frekanslar 5'in altındaysa
   bu pilotun Pearson sonucunu raporlamayın; Python/R bu durumda durur,
   SPSS betiği aynı otomatik engeli içermez.
3. `analiz.sps` dosyasını çalıştırın. Dosya görünmüyorsa `analiz.sps.txt`
   kopyasını UTF-8 ile `analiz.sps` adıyla kaydedin.
4. İlk LIST tablosu her hücrede gözlenen/beklenen, katkı, Pearson artığı,
   satır oranı ve kenar toplamlarını verir. Kontrol CSV'sindeki ilgili
   kategori anahtarlarıyla karşılaştırın; aynı toplamın dört satırda
   tekrarlanması dört kez toplanacağı anlamına gelmez.
5. `WEIGHT BY frekans` ile Crosstabs'ta dört satır değil 80 gözlem temsil
   edilir. Bu bir **sayım ağırlığıdır**, örnekleme ağırlığı değildir.
   `Pearson Chi-Square` satırını okuyun, `Continuity Correction` satırını değil.
   Cramér V'yi ve satır yüzdelerini kontrol edin.
6. `SRESID`, Crosstabs'taki Pearson artığıdır. `RESID` ham O−E farkı,
   `ASRESID` ise düzeltilmiş standartlaştırılmış artıktır. Ek LIST çıktısında
   `pearson_artik` formülü doğrudan gösterilir.
7. Betik ağırlığı kapatıp `B12Ozet` kopyasında hücre katkılarını toplar;
   `SIG.CHISQ` ile p'yi hesaplar. Son LIST, test değerlerini kontrol için verir.
   Sonunda `B12Hucreler` etkin, ağırlık kapalıdır. Betiği ortasında keserseniz
   devam etmeden önce `WEIGHT OFF.` çalıştırın.

SPSS sıfır ağırlıklı kayıtları Crosstabs analizine katmaz; bu pakette boş
kenar toplamları reddedilir ve sıfır hücre özet LIST tablosunda korunur.
SPSS otomatik `--check` veya grafik sunmaz. Kod bu ortamda çalıştırılmadı;
hazır `.sav`/`.spv` verilmedi. Ekran yuvarlamasına dikkat edip sürümü ve
gerçek kontrol sonucunu doğrulama kaydına ekleyin.

## Teknik başvurular

- [SciPy chi2_contingency](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.contingency.chi2_contingency.html)
- [R chisq.test](https://www.stat.ethz.ch/R-manual/R-devel/library/stats/html/chisq.test.html)
- [IBM Crosstabs hücre seçenekleri](https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=crosstabs-cells-subcommand-command)
- [IBM Weight Cases](https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=transformations-weight-cases)
- [IBM AGGREGATE](https://www.ibm.com/docs/en/spss-statistics/32.0.0?topic=reference-aggregate)
- [IBM kuyruk olasılığı işlevleri](https://www.ibm.com/docs/en/spss-statistics/31.0.0?topic=functions-tail-probability)

Belgelerin incelenmesi yorumlayıcı testi değildir.
[Açıklamalı çözüm](cozum.md) · [Grafik açıklaması](grafik-aciklamasi.md)