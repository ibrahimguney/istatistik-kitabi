# B04 — Alıştırma çözümleri

1. Evren dosyasında satır bir olası değerdir; çift dosyasında satır iki
   çekimli bir örneklemdir. N=4 evren büyüklüğü, n=2 tek örneklemin hacmi,
   16 bütün sıralı sonuçların sayısıdır; 16 öğrencilik bir örneklem değildir.
2. Çekim sırası farklıdır. Her birinin olasılığı 1/16, ortalaması 3'tür.
   Aynı ortalamayı vermeleri tek bir eşit ağırlıklı sonuç oldukları anlamına gelmez.
3. Ortalama değerleri 2,3,4,5,6,7,8; frekansları 1,2,3,4,3,2,1;
   olasılıklar frekans/16'dır. Farklı ortalamalara yol açan çift sayıları
   farklıdır; 1/7 atamak bu ağırlıkları kaybettirir.
4. μ=5, kareli sapmalar toplamı 20, evren varyansı 20/4=5, σ=√5≈2,236068.
5. Ağırlıklı ortalamalar toplamı 80/16=5; kareli sapmalar toplamı
   40/16=2,5; standart hata √2,5≈1,581139. Kuramsal değer √5/√2 ile aynıdır.
6. 40/15=8/3≈2,666667. Bu, 16 sayının n−1 bölenli örneklem varyansıdır;
   burada ise bütün eşit olasılıklı dağılım listelendiğinden bölen 16 olmalıdır.
7. En az 7: (6,8),(8,6),(8,8), olasılık 3/16=0,1875.
   Tam 5: (2,8),(4,6),(6,4),(8,2), olasılık 4/16=0,25.
8. Yeni evren 12,14,16,18: beklenen ortalama 15, varyans yine 2,5,
   standart hata yine √2,5. Yeni ortalama ≥17, eski ortalama ≥7 ile aynı
   olaydır; olasılık 3/16. Betikteki `p_en_az_7` eşiği sabit 7'dir;
   kaydırılmış evren için 17 eşiğini ayrı hesaplamak gerekir.
9. Yeni evren 4,8,12,16: beklenen ortalama 10; varyans 4×2,5=10;
   standart hata 2√2,5=√10≈3,162278. Varyans katsayının karesiyle,
   standart hata katsayının mutlak değeriyle değişir.
10. 4⁴=256 sıralı sonuç; merkez 5; varyans 5/4=1,25;
    standart hata √1,25≈1,118034. Ana betik n=2 için hazırlanmıştır;
    n=4 ayrı bir hesap olarak yapılır, ana referans CSV'si kullanılmaz.
11. Aynı birim iki kez seçilemediğinden dört köşegen çift çıkar: 12 sıralı
    sonuç kalır. Ortalamalar 3,4,5,6,7; frekanslar 2,2,4,2,2; olasılıklar
    bu frekansların 12'ye bölümüdür. Merkez 5, kareli sapmalar toplamı 20,
    varyans 20/12=5/3≈1,666667; standart hata √(5/3)≈1,290994.
    Sonlu evren düzeltmeli formül √(5/2)×√((4−2)/(4−1)) aynı sonucu verir.
    Bu geri koymasız tasarım ana paketle aynı değildir.
12. Kuramsal standart hata 10/√25=2. 25 tek örneklemin hacmi,
    5000 benzetim tekrar sayısıdır. 5000 ortalama, bütün normal dağılımı
    tüketmez; hesaplanan standart sapma benzetim değişkenliği nedeniyle
    2'nin yakınında olabilir. Burada tam dağılım değil tekrar örneklemi
    özetlendiğinden kitaptaki `ddof=1` kullanımı B04 tam sayımıyla çelişmez.

## Ayrı tasarımları kodla kontrol etme

Aşağıdaki kodlar `ornek-01` çalışma dizininde çalıştırılır, kaynak dosyaları değiştirmez.
Python'da n=4 ve geri koymasız n=2 için:

```python
from itertools import product
import numpy as np
import pandas as pd

kaynak = pd.read_csv("evren.csv")["deger"].tolist()
ort4 = np.array([np.mean(cekisler) for cekisler in product(kaynak, repeat=4)])
print(len(ort4), ort4.mean(), ort4.var(ddof=0), ort4.std(ddof=0))
ort2 = np.array([(ilk + ikinci) / 2 for ilk, ikinci in product(kaynak, repeat=2)
                 if ilk != ikinci])
print(len(ort2), ort2.mean(), ort2.var(ddof=0), ort2.std(ddof=0))
```

R eşdeğeri (burada çalıştırılmadı):

```r
kaynak <- read.csv("evren.csv")$deger
ort4 <- rowMeans(expand.grid(rep(list(kaynak), 4)))
c(length(ort4), mean(ort4), mean((ort4 - mean(ort4))^2),
  sqrt(mean((ort4 - mean(ort4))^2)))
ciftler <- expand.grid(ilk = kaynak, ikinci = kaynak)
ort2 <- rowMeans(ciftler[ciftler$ilk != ciftler$ikinci, ])
c(length(ort2), mean(ort2), mean((ort2 - mean(ort2))^2),
  sqrt(mean((ort2 - mean(ort2))^2)))
```

Geri koymasız kodda değerlerin farklı olması koşulu, bu pilotun evreninde
her değerin tek bir birimi temsil etmesi sayesinde uygundur. Değerleri
tekrarlanan gerçek bir evrende farklı birimleri değer eşitsizliğiyle
ayıramazsınız; birim kimlikleri gerekir.