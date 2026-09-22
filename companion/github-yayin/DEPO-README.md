# İstatistik uygulamaları

İbrahim Güney'in *İstatistik: Veri Okuryazarlığından İstatistiksel
Çıkarıma* kitabı için bölüm bazlı uygulama paketleri.

## B01 pilot paketi

İlk paket, beş öğrencilik **yapay öğretim verisini** R, Python ve SPSS ile
incelemeyi amaçlar. Veri sözlüğü, çalıştırma yönergeleri, açıklamalı çözüm,
on alıştırma ve yanıtları birlikte sunulur.

| Kod | Konu | Ders sürümü | Kapsamlı sürüm | Durum |
|---|---|---:|---:|---|
| [B01](bolumler/b01/README.md) | İstatistiksel düşünme ve araştırma süreci | 1 | 1 | Pilot |

Diğer bölümlerin paketleri henüz bu ilk yayına dahil değildir.

## Hızlı başlangıç

Depoyu bilgisayarınıza aldıktan sonra depo kökünden:

```sh
cd bolumler/b01/ornek-01
python cozum.py --check
```

Python ve pandas gerekir. R kuruluysa aynı klasörde:

```sh
Rscript cozum.R --check
```

SPSS için aynı klasörü çalışma dizini yapın ve `analiz.sps` dosyasını
çalıştırın. Ayrıntılar [örnek yönergesindedir](bolumler/b01/ornek-01/README.md).

## Doğrulama durumu

- Python: özgün veriyle 18 sayısal kontrol değeri doğrulandı.
- R: kod hazır; gerçek R ortamında çalıştırma kontrolü bekliyor.
- SPSS: kod hazır; IBM SPSS içinde çalıştırma kontrolü bekliyor.

[Ayrıntılı doğrulama kaydı](bolumler/b01/DOGRULAMA.md).

## Kapsam ve kullanım

Bu ilk paket, kitabın LaTeX kaynaklarını, PDF'sini veya 395 öğrencilik
gerçek veri uygulamasını içermez. Küçük yapay veri, gerçek araştırma
bulgusu olarak sunulmamalıdır. Kitap, kod ve verinin yayın koşulları
ayrıca belirlenecektir; bu pilotta açık kaynak lisansı eklenmemiştir.