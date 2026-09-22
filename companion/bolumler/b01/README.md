# B01 — İstatistiksel düşünme ve araştırma süreci

**Ders sürümü:** Bölüm 1. **Kapsamlı sürüm:** Bölüm 1.

Bu paket kitaptaki beş öğrencilik **yapay öğretim örneğinin** R, Python ve
SPSS çözümlerini içerir. Gerçek öğrenci kaydı veya araştırma bulgusu değildir.

## Amaç

Gözlem birimini ve değişken türlerini tanımak; frekans, oran ve ortalama
çıktısını okumak; betimleme, evrene genelleme ve nedenselliği ayırt etmek.

## Çalışma sırası

1. [Örnek yönergesini](ornek-01/README.md) ve veri sözlüğünü okuyun.
2. Bir yazılım seçerek ortak CSV dosyasını analiz edin.
3. [Açıklamalı çözüm](ornek-01/cozum.md) ve beklenen sonuçlarla karşılaştırın.
4. [Alıştırmaları](alistirmalar.md) çözün; sonra [yanıtları](cozumler.md) açın.
5. [Doğrulama kaydını](DOGRULAMA.md) inceleyin.

## Dosyalar

- `ornek-01/veri.csv`: Beş satır ve üç değişken.
- `ornek-01/veri-sozlugu.csv`: Tanım, birim, ölçme düzeyi ve eksik değer kuralı.
- `ornek-01/cozum.R`: Standart R işlevleriyle çözüm.
- `ornek-01/cozum.py`: Python ve pandas ile çözüm.
- `ornek-01/analiz.sps`: Aynı CSV için SPSS sözdizimi.
- `ornek-01/beklenen-sonuclar.csv`: 18 sayısal kontrol değeri.

## Gerçek veri uygulamasıyla karıştırmayın

Kitabın SPSS kısmında ayrıca 395 öğrencilik Student Performance örneği vardır.
O örneğin `b01.xlsx` ve `b01.sps` dosyaları mevcut çalışma alanında yoktur.
Buradaki `analiz.sps` beş satırlık örnek içindir; eksik gerçek veri betiğinin
yerine konulmamalıdır.

## Kaynak ve yayın durumu

Veri, kitabın `chapters/01-veri-arastirma.tex` ve `chapters/r/b01.tex`
dosyalarındaki küçük örnekten aktarılmıştır. Veri kaynağı olarak UCI
belirtilmemelidir. Değerler hazırlama sırasında kitapla karşılaştırılmıştır.
Kitapta veri kod içinde, bu pakette ortak CSV içinde tutulur; otomatik
kitap–depo eşitlemesi henüz kurulmamıştır.

Paket yerel pilottur; GitHub'a yüklenmemiştir. Yayın koşulları yazar
kararına bırakılmış, kendiliğinden açık kaynak lisansı atanmamıştır.