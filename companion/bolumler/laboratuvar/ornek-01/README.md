# Bütünleştirici analiz laboratuvarı: Örnek 01

Kaynak: `chapters/pdr/14-uygulama-laboratuvari.tex`. Kitaptaki sayısal öğretim örneği; yapay veri, 16 gözlem. Gruplar dosyada A=1, B=2 kodlanmıştır. Veriler yeniden rassal üretilmemiştir.

## Çalıştırma

Veri, sözlük, beklenen sonuçlar ve seçtiğiniz kodu aynı klasöre indirin. Terminali **bu klasörde** açın.

- Python: NumPy, pandas ve SciPy kurulu olmalıdır. `python cozum.py --check`
- R: ek paket gerekmez. `Rscript cozum.R --check`. RStudio’da önce çalışma dizinini bu klasör yapın; `source("cozum.R")` sonuçları verir, otomatik kontrol için terminal komutunu kullanın.
- SPSS 29: `analiz.sps.txt` dosyasını `analiz.sps` adıyla kaydedin. `CD 'örnek klasörünüzün tam yolu'.` komutuyla çalışma dizinini seçin; sonra sözdizimini çalıştırın. CSV virgülle ayrılmıştır, ondalık işareti noktadır. Geçerli N ve değişken türlerini kontrol edin.

Python ve R `sonuclar-python.csv` / `sonuclar-r.csv` üretir. `--check` etiketleri ve değerleri `beklenen-sonuclar.csv` ile (bağıl 1e-8, mutlak 1e-10 tolerans) karşılaştırır. Bu referans yalnız özgün veri içindir; alıştırma verinizi ayrı kopyada değiştirin.

Welch sonucu SPSS’te “Equal variances not assumed” satırıyla karşılaştırılır. Ayarlı modelde grup A referanstır.

## Çıktıyı okuma

[Adım adım yorum](cozum.md), [alıştırmalar](../alistirmalar.md), [yanıtlar](../cozumler.md), [doğrulama durumu](../DOGRULAMA.md).

Örneklem standart sapmasında bölen n−1’dir. Bu küçük öğretim örneklerinin p-değerleri gerçek bir araştırma bulgusu olarak sunulmamalıdır. Varsayımlar araştırma tasarımı ve veri incelemesiyle ayrıca değerlendirilir.
