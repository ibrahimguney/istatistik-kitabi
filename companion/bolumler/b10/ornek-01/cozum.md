# Açıklamalı çözüm

## 1. Gözlenen örneklem: tek örneklem t testi

H0: μ=50, H1: μ≠50, α=0,05. Verilen özet n=25, ortalama=55 ve s=10'dur.

- SE = s/√n = 10/5 = 2.
- df = n−1 = 24.
- t = (55−50)/2 = 2,5.
- Çift yönlü p = 2P(T24 ≥ 2,5) = 0,0196541751.
- Cohen d = (55−50)/10 = 0,5; bu, gözlenen standartlaştırılmış farktır.

p<0,05 olduğundan H0 reddedilir. d, p-değeri değildir; d=0,5'e yalnız
etiket yapıştırmak yerine puan farkının bağlamı ve belirsizliği açıklanmalıdır.

## 2. Evren ortalaması için güven aralığı

Kritik t(0,975;24)=2,0638985616, hata payı=4,1277971233'tür.
Yüzde 95 aralık:

`55 ± 4,1277971233 = [50,8722028767; 59,1277971233]`.

Genişlik 8,2555942465'tir. Aralık **evren ortalaması** içindir; öğrencilerin
%95'inin bu puanlarda olduğu anlamına gelmez. Referans 50'yi içermemesi
aynı modeldeki çift yönlü testin kararıyla uyumludur.

Örnek rapor: “n=25, ortalama=55,00, s=10,00; t(24)=2,50,
çift yönlü p=0,01965, d=0,50, yüzde 95 GA [50,8722; 59,1278].”
Ham gözlemler verilmediğinden dağılım, aykırı değerler ve bağımsızlık bu
pakette doğrulanamaz; rapora örnekleme tasarımı ve ölçüm bağlamı eklenmelidir.

## 3. Yeni çalışma: ileriye dönük güç

Veri toplamadan önce gerçek farkın 5 puan ve evren standart sapmasının
10 puan olduğu varsayılsın. Planlanan standartlaştırılmış fark Δ/σ=0,5'tir.
Bu varsayımlar gözlenen d ile otomatik doldurulmaz; bağımsız gerekçe ister.

n=34 için df=33, kritik t≈2,0345152974 ve merkez dışılık
λ=(Δ/σ)√n≈2,9154759474 olur. H0 altındaki merkezi t kritik sınırları,
alternatif altındaki merkezi olmayan t dağılımında değerlendirilir:

`Güç = P(T33,λ < −kritik) + P(T33,λ > kritik) = 0,8077775013`.

Bu iki ret bölgesinin toplamıdır; R'deki `strict=TRUE` bunun içindir.
Belirtilen alternatif ve tasarım altında β=1−güç=0,1922224987'dir.
Güç bir model olasılığıdır; tek bir araştırmanın anlamlı çıkacağı garantisi,
H0'ın yanlış olma olasılığı veya gözlenen sonucun güvenilirlik puanı değildir.

## 4. En küçük tam sayı örneklem

| Bağımsız gözlem sayısı | Planlanan güç |
|---|---:|
| 33 | 0,7953658415 |
| 34 | 0,8077775013 |

%80 hedef için 33 yetmez, 34 yeterlidir. Paket aramasında en küçük tam sayı
34 bulunur; kesirli hacim hesabı en yakın tam sayıya değil **yukarı**
yuvarlanmalıdır. Kümelenme, ölçüm kaybı ve çalışmadan ayrılmalar bu hesapta
yoktur; sahaya alınacak kişi sayısı otomatik olarak 34 kabul edilmemelidir.

Tip I hata, μ=50 doğruyken reddetmektir; model altında α ile kontrol edilir.
Tip II hata, burada planlanan alternatif doğruyken reddedememektir; β,
seçilen gerçek farka ve tasarıma bağlıdır. “Gözlenen güç” hesaplayarak
p-değerini yeniden yorumlamak bu ileriye dönük hesabın yerine geçmez.