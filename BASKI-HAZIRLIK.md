# Baskı hazırlık durumu

> Not: Yayının PDF e-kitap olarak hazırlanmasına karar verilmiştir. Bu dosya,
> ileride basılı sürüm istenmesi durumunda kullanılmak üzere korunmaktadır.

Denetim tarihi: 22 Eylül 2026

## Tamamlanan kontroller

- İç blok 372 sayfa ve çift sayfa sayısındadır.
- Kesim ölçüsü 152,4 × 228,6 mm'dir.
- Kapak arka kapak + sırt + ön kapak biçiminde tek sayfadır.
- Kapakta dört kenarda 3 mm taşma payı vardır.
- İç blok ve kapak PDF/X-4 olarak üretilebilmektedir.
- Her iki PDF'de XMP metadata ve çıktı profili gömülüdür.
- Kullanılan fontların tamamı gömülüdür.
- Çözülmemiş kaynakça atfı, çapraz başvuru veya LaTeX hatası yoktur.
- Raster grafiklerin etkin çözünürlüğü 348–429 dpi arasındadır.
- Kapak, iç kapak ve metadata birleşik kitap başlığıyla uyumludur.

## Doğrulanmış baskı çıktıları

- İç blok: `build/press/interior/main-pdfx4.pdf`
- Kapak: `build/press/cover/cover-print-pdfx4.pdf`

Bu dosyalar proje kökünde `./build-print.sh` komutuyla yeniden üretilir.

## Dışarıdan kesinleştirilmesi gereken bilgiler

1. ISBN
2. Yayınevi yayın numarası
3. Matbaanın seçtiği kâğıt, cilt türü ve buna bağlı kesin sırt genişliği

Bu bilgiler `print-config.tex` dosyasına girildiğinde iç künye ve kapak birlikte
güncellenir. Mevcut 18 mm sırt genişliği yalnız geçici prova değeridir.

## Renk notu

Kitaptaki dört raster grafik PDF/X-4 içinde RGB olarak ve 300 dpi üzerinde
korunmaktadır. PDF/X-4 çıktı profili gömülüdür. Matbaa ayrıca önceden CMYK'ya
dönüştürülmüş görseller talep ederse kullanılacak ICC profili matbaadan
alınmalı; dönüşüm o profile göre yapılmalıdır.