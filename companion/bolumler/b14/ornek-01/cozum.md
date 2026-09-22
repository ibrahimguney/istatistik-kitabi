# Açıklamalı çözüm: altı adımlı sınav yanıtı

## 1. Tanımla

Aynı öğrencilerin iki zamandaki puanları karşılaştırılıyor. D=son−ön
ve hedef μ_D, evrendeki ortalama farktır. Özet, 24 tam çift üzerinden
ortalama fark −3,2 ve fark standart sapması 6 verir. Hedef evrenin kimleri
kapsadığı ve örnekleme yöntemi sayısal özetten tek başına belirlenemez.

## 2. Yöntemi seç

Ölçümler aynı kişilere ait olduğundan eşleştirilmiş t testi uygundur;
iki bağımsız grup Welch testi değildir. Farklar üzerinde H0: μ_D=0,
H1: μ_D≠0 sınanır. Yön, sonuç görüldükten sonra tek yönlüye çevrilmez.

## 3. Koşulları belirt

Farklar kişiler arasında bağımsız olmalı; fark dağılımında aykırı değerler
ve yaklaşık normallik değerlendirilmelidir. Ham veri olmadığı için bu
koşulların sağlandığını iddia etmiyoruz. Eksik çiftler varsa n, ortalama
fark ve standart sapma aynı tamamlanmış çiftlerden yeniden hesaplanmalıdır.

## 4. Hesapla

- SE=6/√24=1,2247448714.
- df=24−1=23; t=−3,2/SE=−2,6127890590.
- Çift yönlü p=0,0155576312.
- Kritik t(0,975;23)=2,0686576104.
- Hata payı=2,5335777990; tam genişlik=5,0671555981.
- Yüzde 95 fark aralığı [−5,7335777990; −0,6664222010].
- d_z=−3,2/6=−0,5333333333.

d_z'nin paydası farkların standart sapmasıdır; bağımsız iki grubun
birleştirilmiş standart sapmasına dayalı Cohen d ile aynı tanım değildir.

## 5. Karar ver

p<0,05 olduğundan H0 reddedilir. Aynı model ve çift yönlü testte aralığın
sıfırı dışlaması bu kararla uyumludur. p, H0'ın doğru olma olasılığı değildir.
Sıfır aralık dışında diye her öğrencide azalma olduğu sonucuna varılmaz.

## 6. Bağlamda yorumla

“24 öğrencide son−ön puan farkı ortalama −3,20 (s_D=6,00) bulundu;
eşleştirilmiş t(23)=−2,61, çift yönlü p=0,01556,
yüzde 95 GA [−5,73; −0,67], d_z=−0,53. Son ölçüm ortalaması daha düşüktür.”

Kitaptaki bağlam kaygı puanıdır; azalmanın olumlu/olumsuz anlamı ölçeğin
yönü ve ölçüm özellikleriyle açıklanmalıdır. Kontrol grubu olmayan tasarımda
bu değişim yalnız eğitime bağlanamaz; pratik önem ve genelleme ayrıca
gerekçelendirilir. Bu istatistiksel rapor bireysel değerlendirme veya
bir uygulamanın etkililiğine dair tek başına kanıt değildir.