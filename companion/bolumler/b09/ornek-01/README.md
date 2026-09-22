# Örnek 01 — Bir fark için t testi ve güven aralığı

## Girdi ve kapsam

`veri.csv` tek özet satırıdır: `fark=2.1`, `standart_hata=1`,
`serbestlik=49`, `null_degeri=0`, `alfa=0.05`.
Fark ve standart hata aynı birimdedir; birim kaynak örnekte belirtilmemiştir.
Standart hata, ham gözlemlerin standart sapması değildir. `serbestlik`
pozitif olmalıdır; kesirli değerler de kabul edilir. α için 5 değil 0.05 yazılır.

Bu hesap, ilgili test istatistiğinin H0 altında verilen serbestlikte t
modeline uyduğu varsayımıyla yapılır. Örnekleme tasarımı, bağımsızlık ve
modelin uygunluğu yalnız bu özetten denetlenemez. df=49 tek başına n=50,
eşleştirilmiş ölçüm veya iki bağımsız grup anlamına gelmez.

## Çalıştırma

Tüm komutlar **bu örnek klasöründe** çalıştırılır. Python için NumPy, pandas,
SciPy ve grafik seçeneğinde Matplotlib gerekir; R betiği standart kurulum
işlevlerini kullanır. Betikler paket kurmaz veya veri indirmez.

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

`--check`, 20 değeri `beklenen-sonuclar.csv` ile 1e-9 mutlak/bağıl toleransla
karşılaştırır; uyuşmazlıkta başarısız çıkış verir. Etiketler ve sıraları da
aynı olmalıdır. `--grafik` olmadan da sonuç tablosu ve ana karar yazdırılır.
Python sürümleri, R tarafında `sessionInfo()` konsola yazılır.

Alıştırmalar için önce klasörün kopyasını alın. Girdiyi değiştirdikten sonra
sadece `python cozum.py` veya `Rscript cozum.R` çalıştırın: dağıtılan kontrol
CSV'si özgün örneğe aittir, yeni girdinin `--check` sınamasının geçmesi beklenmez.
Referans sonuçları sadece kontrol geçsin diye değiştirmeyin.

## SPSS

1. Açık çalışma dosyalarınızı kaydedin. SPSS'in çalışma dizinini bu örnek
   klasörüne ayarlayın; göreli `veri.csv` yolu buraya göre çözülür.
2. `analiz.sps` dosyasını Syntax Editor'de açıp tamamını çalıştırın. Dosya
   bulunmuyorsa `analiz.sps.txt` kopyasını UTF-8 ile `analiz.sps` adıyla kaydedin.
3. Dictionary ve üç LIST tablosundaki 5 girdi, 8 test, 7 aralık değerini
   `beklenen-sonuclar.csv` ile karşılaştırın. SPSS'teki `t_degeri`, kontrol
   tablosunun `t` satırıdır. Değer etiketleri ve ekran yuvarlamasına dikkat edin.
4. Sürümü ve gerçek kontrol sonucunu bölümün doğrulama kaydına ekleyin.

SPSS betiği özet satırına formül uygular; ham gözlem gerektiren T-TEST
komutuna bir özet satırını öğrenciymiş gibi vermez. Sayısal girdi geçerliliği
SPSS'te ayrıca kontrol edilmelidir; Python/R'deki otomatik girdi denetimleri
SPSS betiğinde yoktur. SPSS otomatik `--check` veya grafik üretmez.
Hazır `.sav`/`.spv` çıktısı sunulmaz; SPSS bu ortamda çalıştırılmadı.

## Sonuçları okuma

- `reddet_*`: 1 ilgili H0 reddedilir, 0 reddedilemez; 0, H0 kanıtlandı demek değildir.
- `reddet_cift`, `reddet_ust`, `reddet_alt` girdi α'sını kullanır.
- `reddet_alfa001` yalnız çift yönlü testin sabit α=0,01 karşılaştırmasıdır.
- `null_aralikta`: 1 sıfır hipotezi değeri kapalı aralıkta, 0 aralık dışındadır.
- Güven aralığının düzeyi `1-alfa`dır; sabit α=0,01 karar sütunu ana aralığı değiştirmez.

Yönlü p-değerleri öğretim amaçlı karşılaştırmadır. Üç test içinden en küçük
p-değerini seçerek raporlamayın; alternatif ve α veriye bakmadan belirlenmelidir.
Ana rapor, kitapla uyumlu çift yönlü testtir.

[Açıklamalı çözüm](cozum.md) · [Grafik açıklaması](grafik-aciklamasi.md)

## Teknik başvurular

- [SciPy t dağılımı: sf, cdf ve ppf](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)
- [R Student t dağılımı: pt ve qt](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/TDist.html)
- [IBM SPSS işlev sözlüğü: CDF.T ve IDF.T](https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=reference-glossary)

SPSS üst kuyruğu t simetrisiyle `CDF.T(-t_degeri,serbestlik)` olarak
hesaplar; Python/R doğrudan üst kuyruk seçeneğini kullanır. Böylece küçük
üst kuyruk olasılığında 1'den neredeyse 1 çıkarma işleminden kaçınılır.
Belgelerin incelenmesi, ilgili yazılımda çalıştırma testi değildir.