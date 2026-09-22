# Örnek 01 — Açıklamalı çözüm

## 1. Özetten standart hataya

Verilenler n=25, ortalama=72, örneklem standart sapması s=10.
SE=s/√n=10/5=**2 puan**, serbestlik derecesi **24**.
Tek CSV satırı bu 25 gözlemin özetidir, bir gözlem değildir.

## 2. İki güven aralığı

| Ölçü | Yüzde 95 | Yüzde 99 |
|---|---:|---:|
| Güven düzeyi | 0,95 | 0,99 |
| Alpha | 0,05 | 0,01 |
| Kantilde kullanılan olasılık | 0,975 | 0,995 |
| Kritik t (df=24) | 2,063898562 | 2,796939505 |
| Hata payı | 4,127797123 | 5,593879010 |
| Alt sınır | 67,872202877 | 66,406120990 |
| Üst sınır | 76,127797123 | 77,593879010 |
| Tam genişlik | 8,255594247 | 11,187758019 |

Yüzde 95 aralık: **72 ± 4,127797**, yani **[67,8722;76,1278]**.
Yüzde 99 aralık: **72 ± 5,593879**, yani **[66,4061;77,5939]**.
Tam duyarlıklı 19 kontrol, `beklenen-sonuclar.csv` içindedir.

Yüzde 99 aralık daha geniştir; aynı veri ve daha yüksek güven düzeyiyle
daha fazla parametre değeri aralığa dahil edilir. Nokta tahmini 72,
standart hata 2 ve df=24 değişmez; değişen kritik değerdir.

## 3. Sık karışıklıklar

- **10 ile 2 aynı değildir:** 10 tek gözlemlerin örneklem standart sapması,
  2 ortalama için tahmin edilen standart hatadır.
- **4,1278 ile 8,2556 aynı değildir:** ilki yüzde 95 hata payı,
  ikincisi aralığın tam genişliğidir.
- **0,95 ile 0,975 aynı iş değildir:** 0,95 merkezi kapsama düzeyi,
  0,975 pozitif kritik t'nin kümülatif olasılığıdır.
- **72 bilinen evren ortalaması değildir:** örneklem ortalaması ve aralık merkezidir.
- **19 kontrolün geçmesi varsayımların geçmesi değildir:** ham veri
  olmadığından dağılımı ve aykırı değerleri inceleyemedik.

## 4. Kısa rapor

> Verilen n=25, ortalama=72 ve s=10 özetlerinden, bağımsız gözlemler ve
> uygun normal evren modeli varsayımı altında ortalama için yüzde 95
> t güven aralığı [67,87;76,13], yüzde 99 aralık [66,41;77,59] hesaplandı.
> Daha yüksek güven düzeyi daha geniş aralık verdi. Ham gözlemler
> bulunmadığından dağılım ve aykırı değer koşulları ayrıca doğrulanamadı.

Tekrarlanan aynı örnekleme ve aralık kurma yöntemi altında, varsayımlar
sağlandığında aralıkların belirtilen oranı sabit evren ortalamasını kapsar.
Bu iki aralık, tek tek puanların yayılımını veya sabit parametrenin bu
hesaplanmış aralıktaki olasılığını göstermez.