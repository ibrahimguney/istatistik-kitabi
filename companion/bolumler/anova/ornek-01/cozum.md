# Açıklamalı çözüm

## Klasik ANOVA

A/B/C grupları için n=10/10/10, ortalama=70/75/82 ve s=6/7/5.
Genel ortalama 75,666667; grup kareler toplamı 726,666667,
hata kareler toplamı 990, toplam kareler 1716,666667'dir.
Serbestlik dereceleri 2 ve 27; MS_grup=363,333333; MSE=36,666667.

**F(2,27)=9,909091; p≈0,0005927.** Genel eşit ortalamalar hipotezi %5
ile reddedilir. Bu, üç çiftin tamamının farklı olduğu anlamına gelmez.
Eta-kare≈0,423301; omega-kare≈0,372624. Bunlar aynı etki büyüklüğü formülü
değildir. Omega-karenin formülü bazı verilerde negatif tahmin verebilir;
bu paket değeri sessizce sıfıra kırpmaz.

## Tukey karşılaştırmaları

q-kritik≈3,506426, se_q≈1,914854; aralık yarı genişliği≈6,714295.

| Çift | İlk−ikinci fark | %95 eşzamanlı aralık | Düzeltilmiş p | %5 kararı |
|---|---:|---|---:|---|
| A–B | −5 | [−11,714295; 1,714295] | 0,173955 | Fark gösterilemedi |
| A–C | −12 | [−18,714295; −5,285705] | 0,000400 | Fark gösterildi |
| B–C | −7 | [−13,714295; −0,285705] | 0,039742 | Fark gösterildi |

A–B aralığının sıfır içermesi eşdeğerlik kanıtı değildir. Üç ayrı düzeltilmemiş
t testi yerine aile düzeyi çoklu karşılaştırma yöntemi kullanılmıştır.
R `TukeyHSD` çıktısında ters yönlü C−A gibi etiketler görülürse farkın
ve aralık uçlarının işaret/yönü eşleştirilmeden sayılar karşılaştırılmaz.
Bu pakette özetlerden hesaplandığı için doğrudan `TukeyHSD` çağrısı yoktur.

## Welch örneği

Bu ayrı örnekte n=12/20/8, ortalamalar=70/76/84, s=3/10/5.
Ağırlıklar n/s² olduğundan merkez≈73,064748'dir; sıradan N-ağırlıklı
ortalama olan 75,8 ile karıştırılmamalıdır. Düzeltme toplamı≈0,146826,
F payına uygulanan düzeltme çarpanı≈1,036706'dır.

**F≈25,326470; df=(2;18,162110); p≈0,000005578.**
Payda serbestliği kesirlidir; 18'e yuvarlanarak hesap yapılmaz.
Genel test anlamlıdır; hangi çiftlerin farklı olduğunu tek başına belirlemez.
Klasik örnekteki Tukey sonuçlarını bu farklı özetlere uygulamak yanlıştır.

## Özetlerin sınırı

Üç satır otuz ya da kırk bireysel gözlemi yeniden kurmaz. Normallik,
Levene testi, bireysel aykırı değerler ve gerçek örnekleme bağımsızlığı
bu özetlerden doğrulanamaz. Sonuçlar kitaptaki varsayımsal hesapların
çözümleridir; gerçek bir evrene genelleme veya nedensellik kanıtı değildir.