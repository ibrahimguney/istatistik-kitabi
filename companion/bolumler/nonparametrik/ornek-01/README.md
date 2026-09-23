# Parametrik olmayan yöntemler: Örnek 01

Kaynak: `chapters/pdr/13-nonparametrik.tex`. Kitaptaki sayısal öğretim örneği; yapay veri, 20 gözlem. Gruplar dosyada A=1, B=2 kodlanmıştır. Veriler yeniden rassal üretilmemiştir.

## Çalıştırma

Veri, sözlük, beklenen sonuçlar ve seçtiğiniz kodu aynı klasöre indirin. Terminali **bu klasörde** açın.

- Python: NumPy, pandas ve SciPy kurulu olmalıdır. `python cozum.py --check`
- R: ek paket gerekmez. `Rscript cozum.R --check`. Bu komut Terminal içindir. RStudio Console için aşağıdaki adımları kullanın.
- SPSS 29: `analiz.sps.txt` dosyasını `analiz.sps` adıyla kaydedin. `CD 'örnek klasörünüzün tam yolu'.` komutuyla çalışma dizinini seçin; sonra sözdizimini çalıştırın. CSV virgülle ayrılmıştır, ondalık işareti noktadır. Dosyaya eklenmiş `SET DECIMAL=DOT.` satırı dahil tüm sözdizimini çalıştırın. Geçerli N ve değişken türlerini kontrol edin.

Python ve R `sonuclar-python.csv` / `sonuclar-r.csv` üretir. `--check` etiketleri ve değerleri `beklenen-sonuclar.csv` ile (bağıl 1e-8, mutlak 1e-10 tolerans) karşılaştırır. Bu referans yalnız özgün veri içindir; alıştırma verinizi ayrı kopyada değiştirin.

Bu paket Mann–Whitney (veri.csv, 20 kişi), Wilcoxon ve işaret (esli.csv, 12 çift) ve Kruskal–Wallis (uc-grup.csv, 30 kişi) örneklerini içerir. Üç veri dosyasını da kodlarla aynı klasöre indirin. Bu dosyalar farklı öğretim örnekleridir; satırları birleştirmeyin. Python ve R iki yönlü, bağ düzeltmeli asimptotik hesap kullanır; süreklilik düzeltmesi kapalıdır. Wilcoxon: sıfır farklar dışlanır, bağlı sıralar düzeltilir; asimptotik iki yönlü p, süreklilik düzeltmesizdir. R pozitif sıra toplamını, Python küçük sıra toplamını raporlayabilir; ortak tabloda W_min kullanılır. İşaret testi iki yönlü kesin binom testidir. Kruskal–Wallis bağ düzeltmelidir; anlamlı sonuç hangi çiftlerin farklı olduğunu söylemez. SPSS için küçük U ile U_min karşılaştırılır. p-değeri karşılaştırmasında yöntem ayarları aynı olmalıdır.

Kaynaklar: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html ve https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html

## Çıktıyı okuma

[Adım adım yorum](cozum.md), [alıştırmalar](../alistirmalar.md), [yanıtlar](../cozumler.md), [doğrulama durumu](../DOGRULAMA.md).

Örneklem standart sapmasında bölen n−1’dir. Bu küçük öğretim örneklerinin p-değerleri gerçek bir araştırma bulgusu olarak sunulmamalıdır. Varsayımlar araştırma tasarımı ve veri incelemesiyle ayrıca değerlendirilir.

## RStudio Console ile doğrulama

`cozum.R` dosyasını açın. **Session → Set Working Directory → To Source File Location** ile örnek klasörünü seçin. Console'a şu R kodunu girin (`Rscript` komutu Console'a yazılmaz):

```r
source("cozum.R")
ref <- read.csv("beklenen-sonuclar.csv")
stopifnot(
  identical(out$olcut, ref$olcut),
  all(abs(out$deger - ref$deger) <= 1e-10 + 1e-8 * abs(ref$deger))
)
cat("KONTROL BASARILI\n")
```

Başarı mesajı özgün verinin referansla eşleştiğini gösterir. Ayrıntılı yazılım kontrol kaydı: [DOGRULAMA.md](../DOGRULAMA.md).
