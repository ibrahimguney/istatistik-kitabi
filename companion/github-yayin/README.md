# İstatistik uygulamaları

**İbrahim Güney — İstatistik: Veri Okuryazarlığından İstatistiksel Çıkarıma**

Birleşik kitabın öğrenciye yönelik kod, veri ve çözümlü uygulamaları için
hazırlanmış tarihsel B01 pilot yayın paketi.
İlk paket **B01 pilot uygulamasıdır**; kitabın tamamını veya bütün gerçek veri
paketlerini içermez.

## Bölümler

| Kod | Konu | Ders sürümü | Kapsamlı sürüm | Durum |
|---|---|---:|---:|---|
| [B01](bolumler/b01/README.md) | İstatistiksel düşünme ve araştırma süreci | 1 | 1 | Pilot |

B02 ve sonraki bölüm paketleri henüz bu depoya dahil değildir.

## B01 ile başlayın

1. [Bölüm girişini](bolumler/b01/README.md) okuyun.
2. [Örnek yönergesindeki](bolumler/b01/ornek-01/README.md) adımlarla R,
   Python veya SPSS çözümünü çalıştırın.
3. [Alıştırmaları](bolumler/b01/alistirmalar.md) çözün;
   ardından [yanıtlarla](bolumler/b01/cozumler.md) karşılaştırın.

Python ve pandas bulunan bir ortamda depo kökünden:

```sh
cd bolumler/b01/ornek-01
python cozum.py --check
```

Aynı klasörde R kurulumu varsa:

```sh
Rscript cozum.R --check
```

SPSS çalışma dizinini de aynı örnek klasörüne ayarlayın ve `analiz.sps`
dosyasını çalıştırın. Üç yazılımın girdisi aynı `veri.csv` dosyasıdır.

## Doğrulama durumu

- **Python:** 18 sayısal kontrol değeri doğrulandı.
- **R:** Kod hazır; gerçek R ortamında çalıştırma kontrolü bekliyor.
- **SPSS:** Sözdizimi hazır; gerçek SPSS ortamında çalıştırma kontrolü bekliyor.

Ayrıntılar [B01 doğrulama kaydındadır](bolumler/b01/DOGRULAMA.md).
Python kontrolünün geçmesi R ve SPSS'in çalıştırıldığı anlamına gelmez.

## Veri ve kapsam

B01 verisi kitap için hazırlanmış beş satırlık **yapay öğretim örneğidir**;
gerçek öğrenci verisi ve 395 öğrencilik UCI uygulaması değildir.
Veri sözlüğü, sınırlılıklar ve kaynak açıklaması bölüm klasöründedir.
Kitabın LaTeX kaynakları ve PDF'si bu pilot paketin kapsamına dahil değildir.

## Kullanım koşulları

Henüz açık kaynak lisansı seçilmemiştir. Kitap, kod ve veri için izin ve
lisans kapsamı yazar tarafından ayrıca belirlenecektir; bu README bir açık
lisans izni vermez.