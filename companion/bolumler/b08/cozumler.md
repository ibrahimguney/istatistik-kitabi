# B08 — Alıştırma çözümleri

1. Tek satır bütün örneklemin özetidir; n=25 gerçek gözlem sayısını bildirir.
   25,72,10'u ham gözlem kabul etmek n=3 ve farklı ortalama/standart sapma
   üretir. Özet istatistiklerle yapılan hesap yerine geçmez.
2. SE=10/√25=2, df=25−1=24. s bireysel yayılımı özetler; hata payı,
   SE'nin seçilen güven düzeyine uygun kritik t ile çarpımıdır.
3. Merkezi olasılık 0,95; dışarıda kalan 0,05 iki kuyruğa 0,025'er bölünür.
   Pozitif sınırın kümülatif olasılığı 0,975. Kritik t≈2,063899;
   hata payı≈4,127797; aralık [67,872203;76,127797], genişlik≈8,255594.
4. Kritik t≈2,796940; hata payı≈5,593879;
   aralık [66,406121;77,593879], genişlik≈11,187758.
   Nokta tahmini 72, SE=2 ve df=24 değişmez; kritik değer artar.
5. Kritik t≈1,710882; aralık [68,578236;75,421764], genişlik≈6,843528.
   Genişlik sırası yüzde 90 < yüzde 95 < yüzde 99.
6. Ortalama 5 puan arttığı için iki sınır da 5 artar:
   [72,872203;81,127797]. SE, kritik değer ve genişlik değişmez.
7. SE=20/√25=4. Kritik t değişmez; eski sınırlar ve genişlik iki katına:
   [135,744406;152,255594], genişlik≈16,511188. Birim dönüşümünde
   hem ortalama hem standart sapma dönüştürülmelidir.
8. SE=1, df=99, kritik t≈1,984217;
   aralık [70,015783;73,984217], genişlik≈3,968434.
   SE tam yarıya iner; df arttığı için kritik t de küçülür. Bu nedenle
   tam genişlik eski genişliğin yarısından biraz daha küçüktür.
   Burada aynı s=10 özetinin verildiği varsayılır; yeni veride s sabit kalmak zorunda değildir.
9. SE=1, df=24 değişmez. Aralık [69,936101;74,063899], genişlik≈4,127797.
   Kritik değer aynı kaldığından hata payı ve genişlik tam yarıya iner.
10. 72±1,96×2=[68,08;75,92], genişlik 7,84. 1,96, yüzde 95 standart
    normal kritik değerin yuvarlanmış halidir ve df=24 t kritiğinden
    küçüktür. Bilinmeyen evren standart sapması yerine s kullanıldığı
    bu küçük örneklem için sırf dar aralık elde etmek amacıyla z'ye geçilmez.
11. Uygun model ve tekrarlanan aynı yöntem altında kurulan aralıkların
    yüzde 95'i sabit evren ortalamasını kapsar. Hesaplanmış aralığa
    sabit parametre için bu olasılığı atamayız. Aralık bireysel puanların
    değil evren ortalamasının belirsizliğine yöneliktir.
12. Ham dağılım, çarpıklık, etkili aykırı değerler ve veri hataları bu üç
    özetten denetlenemez. Bağımsızlık ve örnekleme çerçevesi için tasarım
    bilgisi de gerekir. Keyfî kırpma yöntem/kapsama özelliğini değiştirir;
    uydurma puanlar bilinmeyen ham verinin kanıtı değildir.

## Senaryoları kodla kontrol etme

Bu komutları `ornek-01` çalışma dizininde kullanın; CSV değişmez.
Python:

```python
import pandas as pd
from cozum import aralik_hesapla

veri = pd.read_csv("veri.csv")
print(aralik_hesapla(veri, 0.90))
print(aralik_hesapla(veri.assign(n=100), 0.95))
print(aralik_hesapla(veri.assign(ortalama=77), 0.95))
print(aralik_hesapla(veri.assign(ortalama=144, s=20), 0.95))
```

R eşdeğeri (bu ortamda çalıştırılmadı):

```r
source("cozum.R")
aralik_hesapla(veri, 0.90)
aralik_hesapla(transform(veri, n = 100), 0.95)
aralik_hesapla(transform(veri, ortalama = 77), 0.95)
aralik_hesapla(transform(veri, ortalama = 144, s = 20), 0.95)
```

Özgün 19 kontrol bu alıştırma girdilerine ait değildir; sonuçları eşleştirmek
amacıyla `beklenen-sonuclar.csv` değiştirilmez.