# B07 — Alıştırma çözümleri

1. Altı olumlu, dört olumsuz: p-hat=0,60;
   SE=√(0,60×0,40/10)=√0,024≈0,154919.
2. Parametre bilinmeyen evren oranı p; tahmin edici X/n; gerçekleşmiş
   tahmin bu örnekte 6/10=0,60. p=0,40 ayrı benzetimin bilinen model
   değeridir; ilk örneğin gerçek oranı olarak kabul edilmez.
3. Olay ters çevrilince dört olumlu kalır: oran 0,40. Çarpım 0,40×0,60
   değişmediği için SE yine √0,024'tür. Hedef olayın anlamı değişmiştir.
4. n=11 ve olumlu sayısı 7: oran 7/11≈0,636364;
   SE=√[(7/11)(4/11)/11]=√(28/1331). Eski referans CSV bu yeni veri için kullanılmaz.
5. Altı tane 1 kalır: oran 1, yerine-koyma SE'si 0. Bu, yanlış veri silmenin
   sonucudur; p'nin kesin 1 olduğu veya belirsizlik olmadığı kanıtlanmaz.
   Gerçekten bütün yanıtların 1 olduğu küçük örneklerde de bu formülün
   sıfır vermesi kesinlik anlamına gelmez.
6. SE_25≈0,097980, SE_400≈0,024495. Hacim 16 katına, SE dörtte birine gider.
7. E(X/50)=0,40, yanlılık 0. Var=MSE=0,40×0,60/50=0,0048;
   SE=√0,0048≈0,069282.
8. Var=MSE=0,24/200=0,0012, SE≈0,034641. Varyans/MSE dörtte birine,
   SE yarısına iner. Benzetim tekrarını değil tek örneklemin hacmini artırdık.
9. Özdeşlikte B bölenli varyans kullanılır. B−1 bölenli s² verilirse
   V_B=((B−1)/B)s². Ampirik MSE=V_B+(ampirik yanlılık)².
10. Modelde oran tahmin edicisi yansızdır; ampirik merkez rassaldır.
    Merkezin Monte Carlo SE'si √(0,0048/10000)≈0,000692820.
    −0,001582 farkı yaklaşık −2,28 Monte Carlo SE'dir. Bu tek gözlenen
    sapma kuramsal yanlılık kanıtı değildir.
11. E(X)=20; E(T)=21/52≈0,403846. Yanlılık 21/52−2/5=1/260≈0,003846.
    Var(X)=12 olduğundan Var(T)=12/52²=3/676. MSE(T)=3/676+1/260²
    =301/67600≈0,004452663. Bu, 0,0048'den küçüktür: yanlı bir tahmin
    edici bu model noktasında daha düşük MSE verebilir. Her p için veya
    her örneklemde daha iyi olduğu sonucu çıkarılmaz.
12. Ortak CSV için aynı 21 özeti dar toleransla bekleriz. Yeni R benzetiminde
    tohum aynı olsa bile algoritma/üreteç farklı olabilir; tek tek sayılar
    yerine kuramsal merkez, SE ve MSE çevresindeki Monte Carlo değişkenliği
    değerlendirilir. Yeni sonuçlar eski referansa uydurulmaz.

## İleri hesabı kodla kontrol etme

Python'da tam kesirlerle:

```python
from fractions import Fraction

bias = Fraction(21, 52) - Fraction(2, 5)
variance = Fraction(12, 52**2)
mse = variance + bias**2
print(bias, variance, mse, float(mse))
print(mse < Fraction(24, 5000))
```

R eşdeğeri (bu ortamda çalıştırılmadı):

```r
bias <- 21 / 52 - 0.40
variance <- 12 / 52^2
mse <- variance + bias^2
c(bias = bias, variance = variance, mse = mse,
  mse_oran_tahmini = 0.40 * 0.60 / 50)
```

Bu alternatif tahmin edici ana benzetim CSV'sinin veri üretim modelini
veya referans kontrollerini değiştirmez; ayrı bir kuramsal karşılaştırmadır.