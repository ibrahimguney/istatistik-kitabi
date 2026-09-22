# B08 / Örnek 01 — Özet istatistiklerden t güven aralığı

## Veri ve hedef

Evren ortalaması için yüzde 95 ve yüzde 99 iki taraflı güven aralıkları
hesaplanacaktır. `veri.csv` dosyasının tek satırında:

- `n=25`: Özetlenen örneklemdeki gözlem sayısı.
- `ortalama=72`: Örneklem ortalaması, puan biriminde.
- `s=10`: n−1 bölenli örneklem standart sapması, puan biriminde.

**Bir satır bir öğrenciyi değil, bütün örneklemin özetini temsil eder.**
Üç sütunu üç gözlem gibi analiz etmeyin; özetlerden 25 ham puan
uydurmayın. Kitabın Bölüm 8 Python/R uygulamasındaki öğretim girdileridir;
gerçek kişisel kayıt içermez. Kaynak ve veri özeti `kaynak-kaydi.json`
içindedir. CSV UTF-8, virgülle ayrılmış ve ondalık noktası kullanan dosyadır.

## Çalıştırma

Kitap kökünden `cd companion/bolumler/b08/ornek-01`; bağımsız eşlikçi
paket kökünden `cd bolumler/b08/ornek-01` kullanın. Tüm komutlar bu
klasörde çalışır. Klasörün tamamı taşınabilir; diğer kitap dosyaları gerekmez.

### Python

```bash
python cozum.py --check
python cozum.py --check --grafik
```

Python, NumPy, pandas ve SciPy; grafik için ayrıca Matplotlib gerekir.
Sınanan sürümler Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0
ve Matplotlib 3.10.8. Betik paket kurmaz. `stats.t.ppf` ile kritik değer,
özetten SE ve iki sınır hesaplanır. `--check`, 19 etiketi ve sayısal değeri
1e-9 mutlak/bağıl toleransla karşılaştırır. Grafik dosyası
`ciktilar/python/guven-araliklari.png` olur; kaynak CSV değiştirilmez.

### R

```bash
Rscript cozum.R --check
Rscript cozum.R --check --grafik
```

Standart R yeterlidir; `qt` kullanılır. Aynı özetler okunur, yeniden
örnekleme yapılmaz. RStudio'da çalışma dizini bu klasörken
`source("cozum.R")` özetleri gösterir; kontrol ve grafik için ayrıca:

```r
kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
grafik_kaydet(veri)
```

`sessionInfo()` kaydedilir. R grafiği ayrı
`ciktilar/r/guven-araliklari.png` dosyasına yazılır. **R bu ortamda
çalıştırılmadı; gerçek R çıktısı veya doğrulanmış R grafiği sunulmuyor.**

### IBM SPSS

1. Açık verilerinizi kaydedin. Çalışma dizinini bu örnek klasörü yapın.
   SPSS kitap kökünde başlatılmışsa `CD 'companion/bolumler/b08/ornek-01'.`
   kullanılabilir. Sözdizimi dosyasını açmak çalışma dizinini değiştirmez.
2. `analiz.sps` çalıştırın. Uzantı arayüzde taşınmıyorsa `analiz.sps.txt`
   yedeğini aynı klasörde `analiz.sps` adıyla kaydedin.
3. `B08Ozet` veri seti tek satırdır. İlk listede n=25, ortalama=72, s=10,
   SE=2 ve serbestlik=24 görünmelidir. Veri dosyasının bir satır olması
   hesapta n=1 kullanılacağı anlamına gelmez.
4. Kod `IDF.T((1+duzey)/2,serbestlik)` ile kritik değeri hesaplar.
   Sonraki iki listeyi [çözüm tablosuyla](cozum.md) karşılaştırın:
   yüzde 95 aralık yaklaşık [67,8722;76,1278], yüzde 99 [66,4061;77,5939].
5. `duzey95=.95` ve `duzey99=.99` olasılıklardır. Buradaki fonksiyona
   95 veya 99 yazmayın. Sınırları karşılaştırırken ekran yuvarlamasını dikkate alın.

Bu özet dosyası üzerinde Explore veya One-Sample T Test çalıştırıp
sütunları ham gözlemler gibi analiz etmeyin. Betik yalnız açık COMPUTE
hesapları ve LIST kullanır; ağırlık uygulamaz, veri çoğaltmaz. Kaynak özetin
geçerliliğini SPSS'te ilk listeden kontrol edin: n≥2 tam sayı ve s>0 olmalı.
SPSS için otomatik 19 satırlık kontrol, `.sav` veya `.spv` çıktısı yoktur.
**SPSS burada çalıştırılmadı.**

## Hesaplama sözleşmesi

İki taraflı eşit kuyruklu aralık:

**ortalama ± t[(1+güven düzeyi)/2, n−1] × s/√n**.

- Standart hata s/√n, serbestlik derecesi n−1'dir. Burada s zaten
  örneklem standart sapmasıdır; onu tekrar n−1'e bölmeyin.
- Yüzde 95 için alpha=0,05 ve her kuyruk 0,025: kritik değer t'nin
  0,975 kantilidir. Yüzde 99 için 0,995 kantili kullanılır.
- `hata_payi` aralığın yarı genişliği, `genislik` bunun iki katıdır.
  Kritik değeri erken yuvarlamayın; yalnız gösterimde yuvarlayın.
- Python ve R giriş denetimi yalnız tek özet satırı, doğru sütun adları,
  sonlu sayısal değerler, n≥2 tam sayı ve pozitif s kabul eder. Bu pilot
  s=0 veya negatif s için sıfır genişlikli, güvenilir bir aralık üretmez;
  girdi/model değerlendirmesi gerektiğini hata vererek belirtir.
- Güven düzeyi işlevine 0<duzey<1 verilmelidir. Normal çalışmada 0,95 ve
  0,99 sabittir. Alıştırmalar için işlev 0,90 gibi başka geçerli düzeyleri
  de hesaplayabilir. Özgün 19 referans yalnız varsayılan girdilere aittir.
- Negatif bir ortalama matematiksel olarak dışlanmaz; puan ölçeğinin
  gerçek sınırları özetlerden belirlenemez. Aralıkları keyfî biçimde 0–100'e kırpmayın.
- Aynı veriyle yüzde 99 aralık yüzde 95'i kapsar. Bunlar iki bağımsız
  örneklem veya tekrarlanan bir kapsama deneyinin iki sonucu değildir.

## Varsayımlar ve yorum sınırı

Bağımsız ve aynı normal dağılımdan gelen gözlemlerde bu t yöntemi tam
kapsama özelliğine sahiptir; normallik yaklaşık olduğunda uygulama da
uygun koşullarda yaklaşık değerlendirilir. Özetler bağımsızlığı, çarpıklığı,
aykırı değerleri, kapsam hatasını veya yanıtsızlığı denetlemeye yetmez.
Bu paket aralıkların aritmetiğini doğrular; verinin bilimsel uygunluğunu kanıtlamaz.

Yüzde 95, **yöntemin tekrarlanan örneklemelerdeki kapsama oranıdır**.
Hesaplanmış aralıkta sabit parametrenin yüzde 95 olasılıkla bulunduğu
veya öğrencilerin yüzde 95'inin puanlarının bu aralıkta kaldığı şeklinde
okunmaz. Bu, tek kişinin puanı için tahmin aralığı değildir.

Gerçek ham veri elde olsaydı R'de `t.test(puan, conf.level=0.95)$conf.int`
kullanılabilirdi. Burada `puan` yerine `c(25,72,10)` yazmak üç sayıyı
ham gözlem kabul eder ve tamamen başka bir hesap yapar.

Rastgele işlem, tohum, üreteç veya yeni benzetim dosyası yoktur. Bu nedenle
ayrı bir yeniden veri üretim betiği gerekmez; aynı CSV doğrudan yeniden hesaplanır.

## Teknik kaynaklar

9 Eylül 2026 tarihinde incelenen resmi belgeler:

- SciPy Student t, `ppf` ve `interval`:
  <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html>
- R Student t ve `qt`:
  <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/TDist.html>
- IBM SPSS `IDF.T`:
  <https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=functions-inverse-distribution>

Kaynak incelemesi R/SPSS çalışma testi değildir.
[Doğrulama kaydı](../DOGRULAMA.md) yapılan ve bekleyen kontrolleri ayırır.