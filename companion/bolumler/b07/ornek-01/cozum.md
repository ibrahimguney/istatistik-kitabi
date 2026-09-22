# Örnek 01 — Açıklamalı çözüm

## 1. Gözlenen oran

On yapay yanıtın altısı 1, dördü 0: p-hat=6/10=**0,60**.
Yerine-koyma varyans tahmini 0,60×0,40/10=**0,024**;
yaklaşık SE=√0,024≈**0,154919**. Bu, bilinmeyen evren oranının kesin
0,60 olduğu veya örneklemenin doğru tasarlandığı anlamına gelmez.

Aynı p-hat=0,60 korunursa n=25 için SE≈**0,097980**, n=400 için
SE≈**0,024495**. Hacim 16 katına, SE dörtte birine gider.
Bu iki hesap yeni veri toplamadan yapılan formül karşılaştırmasıdır.

## 2. Ayrı Bernoulli benzetimi

Bu kısımda p=0,40 model gereği bilinir; on yanıtın p'si olduğu varsayılmaz.
X~Binom(50,0,40), tahmin edici X/50. Kuramsal merkez 0,40,
yanlılık 0, varyans ve MSE **0,0048**, standart hata **0,069282**.

Kaydedilmiş Python benzetimi:

| Ölçü | Değer (yuvarlanmış) |
|---|---:|
| Tekrar sayısı | 10000 |
| Tek örneklem hacmi | 50 |
| Ampirik merkez | 0,398418 |
| Ampirik yanlılık | −0,001582 |
| B bölenli varyans | 0,004846 |
| B−1 bölenli varyans | 0,004846 |
| Ampirik SE (B−1) | 0,069615 |
| Ampirik MSE | 0,004848 |
| Kuramsal MSE | 0,004800 |

İki varyans altı ondalık basamakta aynı görünebilir; tam duyarlıkta farklıdır.
`beklenen-sonuclar.csv` yuvarlanmamış kontrol sayılarını içerir. R/SPSS aynı
ortak dosyayı okuduğunda aynı özetler hedeflenir; bu ortamlarda çalıştırma testi bekliyor.

## 3. MSE ayrışımı ve bölenler

B tekrarın tahminlerini t_b, ortalamasını m, gerçek oranı p ile gösterelim.
Her tekrar için t_b−p=(t_b−m)+(m−p). Kareleri topladığımızda çapraz terim
sıfırdır, çünkü Σ(t_b−m)=0. Dolayısıyla:

**(1/B)Σ(t_b−p)² = (1/B)Σ(t_b−m)² + (m−p)².**

Sağdaki varyansın böleni B'dir. B−1 bölenli örneklem varyansından başlarsak
önce (B−1)/B ile çarparız. SE hesaplamak için kullanılan `sd` veya
`std(ddof=1)` değerinin karesini düzeltmeden koymak aynı özdeşliği vermez.

Model düzeyinde ise MSE(tahmin edici)=Var(tahmin edici)+Bias².
Örneklem oranı yansız olduğundan model MSE'si varyansa eşittir. Tek
benzetimde görülen −0,001582 merkez farkı kuramsal yanlılık değildir.

## 4. Üç farklı SE

- On gözlemli verinin yerine-koyma oran SE'si: yaklaşık 0,154919.
- n=50 oran tahmin edicisinin kuramsal SE'si: yaklaşık 0,069282.
- 10000 benzetim tahmininin ortalamasının Monte Carlo SE'si:
  0,069282/√10000≈0,000692820.

Ampirik merkez farkı yaklaşık −2,28 Monte Carlo SE'dir. Sonlu rassal
tekrarların her defasında tam 0,40 vermesi gerekmez. Daha çok tekrar bu
Monte Carlo belirsizliğini azaltır; gerçek örneklem hacmi 50'yi değiştirmez.

## 5. Kısa rapor

> On yapay ikili yanıtta örneklem oranı 0,60, yerine-koyma yöntemiyle
> yaklaşık standart hata 0,1549 bulundu. Ayrı p=0,40, n=50 Bernoulli
> benzetiminde 10000 tekrarın merkezi 0,398418, ampirik MSE'si yaklaşık
> 0,004848'dir. Sonuçlar kuramsal merkez 0,40 ve MSE 0,0048 çevresindedir;
> ilk verinin gerçek parametresi bu benzetim parametresiyle özdeşleştirilmez.

Bu pilot güven aralığı veya hipotez testi üretmez; küçük örneklemde normal
yaklaşımın geçerliliğini de varsayılan bir garanti olarak sunmaz.