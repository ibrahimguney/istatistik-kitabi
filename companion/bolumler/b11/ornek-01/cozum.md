# Açıklamalı çözüm

## 1. İki bağımsız grup: Welch testi

H0: μ₁−μ₂=0; H1: μ₁−μ₂≠0. Gözlenen fark 78−72=6 puandır.
Varyans katkıları s₁²/n₁=64/30=2,1333333333 ve
s₂²/n₂=100/28=3,5714285714'tür.

`SE = √(64/30 + 100/28) = 2,3884643403`.

`df = (64/30 + 100/28)² / [(64/30)²/29 + (100/28)²/27] = 51,7113093118`.

Serbestlik derecesi kesirlidir; 51 veya 52'ye yuvarlanmaz. Eşit varyanslı
testteki n₁+n₂−2=56 ile değiştirilmez. Bu, Welch–Satterthwaite yaklaşımıdır.

`t = 6/SE = 2,5120743479`, çift yönlü `p=0,0151628686`.
Kritik t≈2,0069134913, hata payı≈4,7934413080 ve yüzde 95 fark aralığı:

`[1,2065586920; 10,7934413080]`.

α=0,05'te H0 reddedilir. Örnek rapor: “Grup 1−Grup 2 farkı 6,00 puan;
Welch t(51,7113)=2,5121, çift yönlü p=0,01516,
yüzde 95 GA [1,2066; 10,7934].” Nedensellik için bu test tek başına yeterli değildir.

## 2. Ayrı bir eşleştirilmiş örnek

20 tam çift için kişi bazlı fark D=son−ön olarak tanımlıdır.
H0: μ_D=0; H1: μ_D≠0. Ortalama fark 4,2, farkların standart sapması 5'tir.

- SE_D=5/√20=1,1180339887.
- df=20−1=19; iki sütun bulunması df=39 veya 40 bağımsız kişi yaratmaz.
- t=4,2/SE_D=3,7565942022, çift yönlü p=0,0013357333.
- d_z=4,2/5=0,84; payda farkların standart sapmasıdır.
- Kritik t≈2,0930240544; hata payı≈2,3400720321.
- Yüzde 95 fark aralığı [1,8599279679; 6,5400720321].

α=0,05'te H0 reddedilir. Örnek rapor: “20 tam çiftte son−ön farkı
4,20 puan (s_D=5,00); t(19)=3,7566, çift yönlü p=0,001336,
d_z=0,84, yüzde 95 GA [1,8599; 6,5401].”

## 3. Sonucu doğru yorumlamak

İki aralık da evren **ortalama farkı** içindir; ham puanların ya da tek tek
öğrencilerin değişimlerinin %95'ini kapsadıkları söylenemez. İkisi de sıfırı
dışlar ve ilgili çift yönlü α=0,05 testleriyle uyumludur. Sınırdaki sayısal
kararlar yuvarlanmış p veya aralık uçlarından verilmemelidir.

Bu iki örnek aynı veri üzerinde yarışan yöntemler değildir. Eşleştirilmiş
p daha küçük diye uygun tasarım belirlenmez; gözlemler arası ilişki testten
önce bilinir. İki aralığın farklı genişlikleri tek başına bir yöntemin
üstünlüğünü veya iki etkinin birbirinden farklı olduğunu kanıtlamaz.

Eşleştirmelerin doğru kurulması, tam çiftlerin seçimi, bağımsızlık ve
fark dağılımı ham verilerle kontrol edilmelidir. Ön ve son ölçümlerin
ortalamaları, standart sapmaları veya korelasyonu bu özetten ayrı ayrı
bulunamaz. İstatistiksel anlamlılık pratik önem ya da nedensellik değildir;
reddetmeme de eşdeğerlik kanıtı değildir.