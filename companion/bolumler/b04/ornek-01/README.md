# B04 / Örnek 01 — Tam sayımla örnekleme dağılımı

## Soru ve ortak veri

{2,4,6,8} evreninden geri koyarak iki bağımsız çekim yapılıyor. Her çekimde
her değer eşit olasılıklı. Bütün sıralı sonuçlardan örneklem ortalamasının
dağılımını, standart hatasını ve P(ortalama ≥ 7) olasılığını bulun.

- `evren.csv`: Tek `deger` sütununda dört farklı yapay evren değeri.
  Bir satır bir olası evren değeridir. Bu örnekte her satırın ağırlığı 1/4'tür.
- `veri.csv`: `ilk,ikinci` sütunlarında evrenin Kartezyen çarpımı; 16 satır.
  Bir satır, **iki çekimden oluşan bir sıralı örneklemdir**, tek öğrenci değildir.
  Her satırın tasarım olasılığı 1/16'dır. (2,4) ile (4,2) ayrı sonuçlardır.
- `veri-sozlugu.csv`: Her iki dosyanın alanlarını tanımlar. Birimler soyut
  sayısal birimlerdir; gerçek öğrenci kaydı veya fiziksel mutlak sıfır iddiası yoktur.

Kaynak Bölüm 4'ün R öğretim örneğidir. Normal benzetim ve literatür verili
SPSS örneğiyle aynı değildir. CSV'ler UTF-8, virgülle ayrılmış, ondalık
noktası kullanan dosyalardır. Eksik veya sonsuz değer kabul edilmez.
Evrenin farklı değerlerden oluşması ve eşit ağırlıklar bu pilotun sözleşmesidir;
tekrarlanan evren kayıtları veya eşit olmayan ağırlıklar farklı model gerektirir.

## Çalıştırma

Kitap kökünden `cd companion/bolumler/b04/ornek-01`; bağımsız eşlikçi depo
kökünden `cd bolumler/b04/ornek-01` kullanın. Komutlar bu örnek klasöründen
çalıştırılır. Klasörün tamamı başka yere taşınabilir; kitap dosyaları gerekmez.

### Python

```bash
python cozum.py --check
python cozum.py --check --grafik
```

Python, NumPy ve pandas; grafik için ayrıca Matplotlib gerekir. Betik paket
kurmaz. Sınanan ortam: Python 3.13.15, NumPy 2.4.1, pandas 2.3.3 ve
Matplotlib 3.10.8. `--check`, etiket/sıra ile 28 sayısal değeri 1e-9
mutlak/bağıl toleransla karşılaştırır; uyuşmazlık hata koduyla biter.
`--grafik`, `ciktilar/python/ornekleme-dagilimi.png` dosyasını yeniler.

### R

```bash
Rscript cozum.R --check
Rscript cozum.R --check --grafik
```

Standart R yeterlidir; ek paket gerekmiyor. Betik `sessionInfo()` verir.
RStudio'da çalışma dizini bu klasörken `source("cozum.R")` çıktıyı gösterir;
tek başına kontrol/grafik seçeneklerini çalıştırmaz. Ayrıca şu komutlar kullanılabilir:

```r
kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
grafik_kaydet(evren, veri)
```

R grafiği ayrı `ciktilar/r/ornekleme-dagilimi.png` dosyasına yazılır.
**R bu ortamda çalıştırılmadı; bu dosya önceden üretilmiş değildir.**

### IBM SPSS

1. Açık veri dosyalarınızı kaydedin. Çalışma dizinini bu örnek klasörü yapın.
   SPSS kitap kökünden başlatıldıysa bir kez
   `CD 'companion/bolumler/b04/ornek-01'.` çalıştırılabilir. Sözdizimi
   dosyasını açmak tek başına çalışma dizinini değiştirmez.
2. `analiz.sps` çalıştırın. Uzantı arayüzde taşınmıyorsa aynı klasördeki
   `analiz.sps.txt` kopyasını `analiz.sps` adıyla kaydedin.
3. Dictionary'de iki sayısal/Scale alanı kontrol edin. Çapraz tabloda ilk ve
   ikinci çekim kategorileri 2/4/6/8, **16 hücrenin her biri 1**, toplam 16
   olmalıdır. Eksik kayıt olmamalıdır. Fark varsa devam etmeyin.
4. Hesaplanan listeyi kontrol edin: evren ortalaması 5, evren varyansı 5,
   evren standart sapması √5; ortalamaların merkezi 5, varyansı 2,5,
   standart hatası √2,5 ve yanlılığı 0. İki standart hata hesabı aynı olmalı.
5. Frequencies tablosunda 2–8 ortalamalarının frekansları 1/2/3/4/3/2/1
   olmalı. Yüzdeleri **100'e bölerek** kontrol CSV'sindeki olasılıklarla karşılaştırın.
   `p_en_az_7=0,1875`, `p_esit_5=0,25` liste çıktısında görünmeli.

SPSS bu ortamda çalıştırılmadı; `.sav`/`.spv` çıktısı ve SPSS için otomatik
28 satırlık `--check` sunulmuyor. SPSS yalnız ortak `veri.csv` dosyasını okur;
evren özetini ilk sütundaki eşit tekrarlar üzerinden hesaplar. Bu, yalnız
bütün 16 çiftin birer kez yer aldığı doğrulanırsa doğrudur. Python/R ise
evren dosyasından tüm çiftleri yeniden oluşturarak bu bütünlüğü de denetler.

## Hesaplama sözleşmesi

- Tasarım geri koymalı, bağımsız, eşit olasılıklı **n=2** çekimdir. `N=4`
  evrenin büyüklüğü, `n=2` tek örneklemin hacmi, `16` tüm sıralı sonuçların
  sayısıdır. Bunlar birbirinin yerine kullanılmaz.
- Python `product`, R `expand.grid` ile çiftleri oluşturur. R sürümünde
  sütun oluşturma sırası, ortak CSV'nin satır sırasını elde edecek şekilde
  seçilir. Sonuç hesaplarında sıra önemsizdir: aynı çiftlerin aynı sayıda
  bulunması denetlenir; CSV'nin satırlarını karıştırmak dağılımı değiştirmez.
- Eksik/fazla çift, aynı çiftin yinelenmesi veya evrende olmayan değer
  Python/R'de hatadır. `--check` olmadan da bu tasarım denetimi yapılır.
- Evren varyansında bölen 4; ortalamaların tam dağılımında bölen **16**'dır.
  `var(ortalamalar)` veya `std(ddof=1)` burada doğru tam dağılım hesabı değildir.
  Kodlar kareli sapmaların ortalamasını alır; SPSS'te de aynı işlem açıkça yapılır.
- Standart hata, tek gözlemin standart sapması değil, **örneklem ortalamasının
  dağılımının standart sapmasıdır**. Kuramsal kontrol `sqrt(5/2)` olur.
- Geri koymalı tasarıma sonlu evren düzeltmesi uygulanmaz. Geri koymasız
  seçim ayrı bir alıştırmadır; ana CSV'den köşegenleri silip aynı referans
  dosyasına karşı `--check` yapmayın.
- Tam sayımda benzetim hatası yoktur; kayan nokta yuvarlaması ayrı konudur.
  Rastgele işlem/tohum kullanılmaz. Bu pakette diller arası tohum eşitliği
  veya aynı rastgele çekimleri üretme varsayımı yoktur.
- Grafik ayrık olasılıkları gösterir, yoğunluk histogramı değildir.
  Python/R iki panelde ortak eksen ölçeği kullanır. SPSS yerleşik grafiğinde
  düşey eksen **yüzde**dir; Python/R'deki olasılık ekseniyle aynı sayı ölçeği değildir.

Alıştırma için evreni değiştirirseniz çiftleri kodla yeniden üretin ve ayrı
nesnelerde çalışın. `beklenen-sonuclar.csv` özgün örneğin referansıdır;
alıştırma sonuçlarına uydurulmaz. CSV'ler normal çalışmada yeniden yazılmaz.

## Okuma ve teknik başvurular

[Adım adım çözüm](cozum.md), [grafik açıklaması](grafik-aciklamasi.md),
[alıştırmalar](../alistirmalar.md), [yanıtlar](../cozumler.md).
9 Eylül 2026 tarihindeki kaynak incelemesinde kullanılan resmi belgeler:

- R `expand.grid`: <https://stat.ethz.ch/R-manual/R-devel/library/base/html/expand.grid.html>
- IBM SPSS `AGGREGATE`: <https://www.ibm.com/docs/en/spss-statistics/32.0.0?topic=reference-aggregate>
- IBM SPSS `GRAPH`, yüzde sütunları: <https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=reference-graph>

Bu kaynakların incelenmesi R/SPSS çalışma testi değildir.