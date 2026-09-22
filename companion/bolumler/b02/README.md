# B02 — Evren, örneklem ve veri türleri

**Ders sürümü:** Bölüm 2. **Kapsamlı sürüm:** Bölüm 2.

B01'in ardından ikinci yerel paket. Kitaptaki dört öğrencilik **yapay
öğretim verisi**, R/Python/SPSS için aynı CSV'den okunur. GitHub yüklemesi
tüm bölüm paketleri tamamlandıktan sonraya bırakılmıştır.

## Öğrenme hedefleri

- Gözlem birimini, hedef evreni ve örneklemi ayırt etmek.
- Aynı sayının bağlama göre parametre veya istatistik olabileceğini açıklamak.
- Okul türünü nominal, sınıfı sıralı, sınav puanını nicel olarak tanımlamak.
- Kategori frekansı ve oranını puan ortalamasıyla karıştırmamak.
- Küçük bir betimsel farkı nedensellik veya temsil kanıtı saymamak.

## Çalışma sırası

1. [Veri ve çalıştırma yönergesini](ornek-01/README.md) okuyun.
2. [Veri sözlüğündeki](ornek-01/veri-sozlugu.csv) sınıflamayı gerekçelendirin.
3. R, Python veya SPSS çözümünü çalıştırın; özgün veride kontrol tablosuyla karşılaştırın.
4. [Açıklamalı çözümü](ornek-01/cozum.md) inceleyin.
5. [Alıştırmaları](alistirmalar.md) çözün; sonra [yanıtlara](cozumler.md) bakın.

## Dosyalar

- `ornek-01/veri.csv`: Dört satır ve üç değişken.
- `ornek-01/veri-sozlugu.csv`: Tanımlar, kodlar, birimler ve eksik değer kuralı.
- `ornek-01/cozum.py`, `ornek-01/cozum.R`: Ortak 23 satırlık özeti hesaplayan kodlar.
- `ornek-01/analiz.sps`: SPSS veri açma, ölçme düzeyi ve özetleme komutları.
- `ornek-01/analiz.sps.txt`: Aynı SPSS betiğinin taşınabilir metin kopyası.
- `ornek-01/beklenen-sonuclar.csv`: Özgün veri için 23 kontrol değeri.
- [DOGRULAMA.md](DOGRULAMA.md): Yapılan kontroller ve bekleyen R/SPSS çalıştırmaları.
- `MANIFEST.json`: Paket dosyalarının SHA-256 özetleri; kendisini kapsamaz.

## Kaynak ve kapsam

Veri, kitabın `chapters/02-evren-orneklem.tex` ve `chapters/r/b02.tex`
örnekleriyle aynıdır. Kitap veriyi kod içinde oluştururken bu paket CSV'den
okur. Otomatik kitap–depo eşitlemesi kurulmuş değildir; bu sürümde değerler
karşılaştırılarak doğrulanır. Asıl veri değişirse kitapla eşleşme yeniden denetlenmelidir.

Bu dört satır UCI Student Performance verisi değildir. Kitaptaki 395
öğrencilik SPSS B02 uygulamasından ayrı bir öğretim örneğidir; onun çıktıları
buradaki kontrol tablosuyla karşılaştırılmaz. Veri gerçek öğrenci kaydı değildir.

B02 henüz GitHub'a yüklenmedi; B01'in eski ZIP'lerine dahil edilmedi. Nihai
toplu yayın paketine daha sonra alınacaktır. Açık kaynak lisansı kendiliğinden
atanmamıştır; yayın koşulları yazarın kararına bırakılmıştır.