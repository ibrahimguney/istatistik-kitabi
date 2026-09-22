# B06 — Alıştırma çözümleri

1. `id` nominal kimlik, `sinif` 1<2<3 sıralı kategori; göstergeler nominal
   0/1 seçim durumudur. 0 eksik kayıt veya sıfır seçilme olasılığı değildir.
   Kimlik/sınıf ortalamasını bir başarı puanı gibi yorumlamayız.
2. Çerçeve N=12, her örneklem n=6. Tabakalarda N_h=4, seçilen n_h=2.
3. Basitte 6/12, tabakalının her sınıfında 2/4: π=0,5, w=2.
   1/12 tek ilk çekilişe, 6/12 altı kişilik örneğe dahil olmaya karşılık gelir.
4. 6×2=12. Gerçek seçilen kişi sayısı 6'dır; ağırlık toplamı 12 yeni kayıt yaratmaz.
5. Basit: 1,3,6,8,11,12; tabakalı: 1,4,7,8,11,12. Ortak dört kimlik:
   1,8,11,12. Bu örtüşme kendi başına seçim hatası değildir.
6. Hayır. 1,2,3,4,5,6 geçerli bir basit örneklemdir; sınıf sayıları 4/2/0.
   Tabakalı tasarımda bu örneklem geçersizdir. Basit seçimin dengeli
   görünmesi tasarımlar arasındaki farkı ortadan kaldırmaz.
7. Basit: C(12,6)=924. Tabakalı: C(4,2)³=216. Basitte dengeli seçim
   olasılığı 216/924=18/77≈0,233766. Basit seçimi denge sağlanana kadar
   tekrarlamak aynı tasarım değildir.
8. Basitte π=3/12=0,25, w=4, toplam 3×4=12. Her sınıftan bir kişi
   seçen tabakalı tasarımda π=1/4, w=4, toplam 12; ama sınıf temsili
   garantisi yine yalnız tabakalı tasarımdadır.
9. π değerleri 2/4=0,5; 2/8=0,25; 2/12=1/6. Ağırlıklar 2,4,6.
   Toplam 2×2+2×4+2×6=24, gerçek örneklem hacmi 6. Bu, ana paketten
   farklı çerçevedir; pilotun sabit 2 ağırlığını bu duruma taşımayın.
10. Düzeltmez. Listede olmayan hedef birimlerin seçilme olasılığı sıfırdır.
    Listede olup bu çekimde seçilmeyenlerin ise tasarım olasılığı pozitif
    olabilir. Yeni rastgele tohum eksik sınıfı listeye eklemez.
11. Ham toplam 5×2=10 olur. Ağırlıkları 12/10 ile ölçeklemek toplamı
    düzeltir, fakat yanıt verme mekanizmasının yol açtığı yanlılığı
    kendiliğinden gidermez; ek varsayım ve uygun düzeltme gerekir.
12. Hata olmak zorunda değildir: üreteç, algoritma ve tohum kullanma akışı
    farklı olabilir. `cozum.R` ortak CSV'nin sabit kimliklerini okuduğundan
    aynı 29 kontrolü hedefler. `secim.R` yeni bir seçim yapar: altı farklı
    kimlik ve tabakalı 2/2/2 koşulları doğrulanır; eski kimliklere eşitlik aranmaz.

## İleri çalışmayı kodla kontrol etme

Bu bağımsız hesaplar kaynak dosyalarını değiştirmez. Python:

```python
from math import comb
from fractions import Fraction

basit_sayisi = comb(12, 6)
tabakali_sayisi = comb(4, 2) ** 3
print(basit_sayisi, tabakali_sayisi, Fraction(tabakali_sayisi, basit_sayisi))
for tabaka_hacmi in [4, 8, 12]:
    print(2 / tabaka_hacmi, tabaka_hacmi / 2)
```

R eşdeğeri (bu ortamda çalıştırılmadı):

```r
basit_sayisi <- choose(12, 6)
tabakali_sayisi <- choose(4, 2)^3
c(basit_sayisi, tabakali_sayisi, tabakali_sayisi / basit_sayisi)
tabaka_hacmi <- c(4, 8, 12)
data.frame(olasilik = 2 / tabaka_hacmi, agirlik = tabaka_hacmi / 2)
```

Ağırlıkların doğru hesaplanması tek başına tasarıma uygun standart hata
üretmez. Bu dosyada sonuç değişkeni bulunmadığından bir ağırlıklı not
ortalaması veya karşılaştırma testi hesaplanmaz.