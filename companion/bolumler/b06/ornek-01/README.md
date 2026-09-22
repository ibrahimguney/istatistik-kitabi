# B06 / Örnek 01 — Basit ve tabakalı seçim

## Ortak veri ve kaynak

Kitabın Bölüm 6 Python/R öğretim çerçevesi: kimlikler 1–12, sınıflar 1/2/3.
1–4 kimlikleri birinci, 5–8 ikinci, 9–12 üçüncü sınıftadır. Her tabakada dört
birim vardır. Veri yapaydır; öğrenci isimleri veya gerçek notlar içermez.

`veri.csv` UTF-8, virgülle ayrılmış dört sütunlu bir dosyadır:

- `id`: Yapay öğrenci kimliği; sayısal görünür fakat nominaldir.
- `sinif`: Sınıf düzeyi; 1<2<3 düzeninde sıralı kategoridir, puan değildir.
- `basit`: Bu kayıtlı basit rastgele seçimde 1=seçildi, 0=seçilmedi.
- `tabakali`: Bu kayıtlı tabakalı seçimde 1=seçildi, 0=seçilmedi.

Bir satır çerçevedeki bir birimdir; seçilmeyenler de dosyada kalır.
Göstergeler **olasılık değil gerçekleşmiş seçim sonucudur**. Her kişinin
iki tasarımda da ilk-derece dahil edilme olasılığı 0,5'tir; seçilmemiş
birimlerin olasılığı 0 olarak yeniden tanımlanmaz.

## Çalıştırma

Kitap kökünden `cd companion/bolumler/b06/ornek-01`; bağımsız eşlikçi depo
kökünden `cd bolumler/b06/ornek-01` kullanın. Tüm komutlar örnek klasöründe
çalışır. Klasör bütünüyle taşınabilir; kitabın diğer dosyaları gerekmez.

### Python — ortak seçimleri inceleme

```bash
python cozum.py --check
python cozum.py --check --grafik
```

Python, NumPy ve pandas gerekir; grafik seçeneği Matplotlib kullanır.
Sınanan ortam Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, Matplotlib 3.10.8.
Betik paket kurmaz. `--check` 29 etiket/değeri 1e-9 mutlak/bağıl toleransla
karşılaştırır; **sıralanmış seçili kimlikleri de** kontrol eder. Aynı sınıf
sayılarını veren farklı bir seçim, özgün kayıtla eşleşmiş sayılmaz.
Grafik `ciktilar/python/secim-haritasi.png` dosyasını oluşturur veya yeniler.

### R — aynı CSV ile çözüm

```bash
Rscript cozum.R --check
Rscript cozum.R --check --grafik
```

Standart R yeterlidir. Ortak CSV'den yeni seçim yapılmaz; kaydedilmiş
iki gösterge çözülür. `sessionInfo()` çıktısı verilir. RStudio'da aynı
çalışma dizininde `source("cozum.R")` sayıları gösterir. Kontrol/grafik için ayrıca:

```r
kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
grafik_kaydet(veri)
```

R grafiği ayrı `ciktilar/r/secim-haritasi.png` dosyasına yazılır.
**R burada çalıştırılmadı; aynı CSV ile sayısal eşleşme henüz çalışma testiyle doğrulanmadı.**

### IBM SPSS — aynı kayıtlı seçimleri inceleme

1. Açık verilerinizi kaydedin; çalışma dizinini bu örnek klasörü yapın.
   SPSS kitap kökünde başlatılmışsa `CD 'companion/bolumler/b06/ornek-01'.`
   kullanılabilir. Sözdizimini açmak tek başına çalışma dizinini değiştirmez.
2. `analiz.sps` çalıştırın. Uzantı taşınmıyorsa `analiz.sps.txt` yedeğini
   aynı klasörde `analiz.sps` adıyla kaydedin.
3. İlk listede 12 benzersiz kimliği ve kimlik-sınıf eşleşmesini kontrol edin.
   Dictionary'de kimlik/göstergeler nominal, sınıf ordinal olmalıdır.
   Çerçeve frekansları 4/4/4; her seçim göstergesinin 1 frekansı 6 olmalıdır.
4. Basit seçimin listesi **1,3,6,8,11,12**, tabakalı seçimin listesi
   **1,4,7,8,11,12** olmalı. Her listede olasılık 0,5 ve ağırlık 2 görünmelidir.
5. Seçili sınıf frekansları bu dosyada her iki tasarımda 2/2/2; seçilmiş
   kayıtlar üzerindeki ağırlık toplamları 12, Descriptives N değeri 6 olmalıdır.

SPSS yeni rastgele seçim yapmaz; yalnız ortak kayıtları inceler. Her
`TEMPORARY / SELECT IF` etkisi ardından gelen tek çıktı işlemiyle sınırlıdır;
12 kişilik kaynak çerçeve kalıcı olarak daraltılmaz. Betik `WEIGHT OFF`
kullanır; ağırlıkları sütun olarak hesaplar, `WEIGHT BY` uygulamaz. Ağırlık
hesabı karmaşık örnekleme standart hatası üretmez. SPSS için otomatik
29 satırlık test, `.sav` veya `.spv` çıktısı sunulmuyor; çalıştırma bekliyor.

## Seçimleri yeniden üretme

### Python'da kayıtlı seçimin üretimi

```bash
python uret.py
```

Varsayılan çıktı `yeniden-uretilen.csv` olur. `--cikti deneme.csv` ile başka
bir yeni dosya seçilebilir. Mevcut dosya üzerine yazılmaz; mutlak yol veya
`..` kabul edilmez. Alt klasör kullanılacaksa önceden var olmalıdır.
Kaynak `veri.csv` normal üretim çağrısında değişmez.

Üretici kitabın `DataFrame.sample(n=6, random_state=2026)` ve sınıfa göre
`GroupBy.sample(n=2, random_state=2026)` adımlarını kullanır; geri koyma yoktur.
**Her çağrıya ayrı olarak aynı 2026 değeri verilir.** İki tasarımın çekimleri
birbirinden bağımsız tekrarlar gibi sunulmaz. Kimlikler çakışabilir; iki
bağımsız öğrenci grubu testi için hazırlanmış veri değildir.
Aynı kayıtlı sürümlerde yeni CSV'nin byte özeti kaynakla eşleşmelidir;
sürüm, çerçeve sırası veya üreteç değişirse yalnız tohumdan aynılık çıkarılmaz.
Ayrıntılar `uretim-kaydi.json` içindedir.

### R'de yeni seçim

```bash
Rscript secim.R
```

Bu betik R'nin üretecini açıkça seçer, `set.seed(2026)` ile önce basit,
sonra her sınıftan ikişer kişi seçer. Kitaptaki R akışıdır; Python'un iki
ayrı `random_state` çağrısıyla aynı akış değildir. `ciktilar/r/yeni-secim.csv`
yazılır, mevcut dosya üzerine yazılmaz. Seçim listeleri, sınıf sayıları,
tabakalı ağırlık toplamı ve R sürümü gösterilir. **Burada çalıştırılmadı.**

Yeni R kimliklerinin Python kimlikleriyle aynı olması beklenmez. Altı
farklı kimlik, tabakalı 2/2/2 sayıları, 0,5 olasılık ve ağırlık 2 koşullarını
inceleyin. Yeni veriyi ortak CSV'nin yerine koyup özgün kimliklere karşı
`--check` yapmayın. Yapısal tasarım kontrolü ile kayıtlı seçimin birebir
kontrolü farklıdır.

## Kontrol sınırları

- Pilot, 1–12 kimlikli ve sabit kimlik-sınıf eşleşmeli çerçeve içindir;
  genel amaçlı bir örnekleme yazılımı değildir. Başka tabaka büyüklükleri
  alıştırmalarda ayrı hesaplanır, ana CSV değiştirilmez.
- Python/R dosya şemasını, eksiksizliği, sonluluğu, 0/1 göstergelerini,
  basit seçimin altı birimini ve tabakalı seçimin her sınıfta iki birimini
  denetler. Sınıf sıralı kategori olarak tutulur; kimlik/sınıf ortalaması alınmaz.
- `--check` olmadan geçerli başka seçimleri çözmek mümkündür; `--check`
  yalnız dağıtılan sabit seçimi doğrular. Satır sırasını değiştirmek
  kimlikleri değiştirmez, sonuçları etkilemez.
- Seçim göstergesi kurallarının sağlanması rastgeleliğin kanıtı değildir.
  Tohum/üretim kaydı ve kodun yöntemi ayrıca incelenir. Çerçevedeki eksiklik
  veya yanıtsızlık, başarılı yazılım kontrolüyle giderilmiş olmaz.
- Dahil edilme olasılığı basitte n/N, tabakalının her tabakasında n_h/N_h;
  ağırlık tersidir. Bu eşit tabakalı pilotta hepsi 0,5 ve 2 olur. Tekrarsız
  seçim, öğrencilerin dahil edilme göstergelerinin bağımsız olması demek değildir.

## Teknik kaynaklar

9 Eylül 2026 tarihinde incelenen resmi başvurular:

- pandas `DataFrame.sample`: <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html>
- pandas `GroupBy.sample`: <https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.sample.html>
- R `sample` / `sample.int`: <https://stat.ethz.ch/R-manual/R-devel/library/base/html/sample.html>

Kaynak incelemesi R/SPSS çalışma testi değildir. [Doğrulama kaydı](../DOGRULAMA.md)
yapılan ve bekleyen kontrolleri ayırır.