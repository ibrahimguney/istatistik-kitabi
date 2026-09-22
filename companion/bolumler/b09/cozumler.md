# B09 alıştırma çözümleri

1. Sütunlar fark tahmini, tahminin standart hatası, serbestlik derecesi,
   test edilen evren farkı ve anlamlılık düzeyidir. Tek satır bir özet
   kaydıdır. df'nin örneklem büyüklüğüyle bağıntısı kullanılan tasarıma ve
   yönteme bağlıdır; bu özetten hangi tasarımın kullanıldığı bilinmez.
2. t=(2,1−0)/1=2,1. SE tahminin örneklemeden örneklemeye değişkenliğini
   anlatır; gözlem değerlerinin standart sapması değildir.
3. p=0,0409000890<0,05: H0 reddedilir; `reddet_cift=1`.
   Bu, H0'ın yanlış olma olasılığının %95,91 olduğu anlamına gelmez.
4. Kritik=2,0095752371; hata payı=2,0095752371;
   aralık=[0,0904247629; 4,1095752371]; genişlik=4,0191504743.
   Sıfır dışarıdadır; aynı modelde çift yönlü α=0,05 testiyle uyumludur.
5. p değişmez (0,0409000890); α=0,01'de H0 reddedilemez.
   Ana aralık artık yüzde 99'dur: [−0,5799519736; 4,7799519736]; sıfırı içerir.
   `reddet_alfa001` zaten sabit %1 karşılaştırmasıdır; o alanın bulunması
   özgün %95 aralığın kendiliğinden %99'a dönüştüğü anlamına gelmez.
6. Üst p=0,0204500445, alt p=0,9795499555.
   Önceden üst alternatif seçilmişse α=0,05'te reddedilir; alt alternatifte
   reddedilemez. Veriyi gördükten sonra yön seçmek planlanan testin hata
   kontrolünü bozar; üç sonuç arasından en küçüğü raporlanmaz.
7. t=−2,1; çift yönlü p aynı, üst p=0,9795499555,
   alt p=0,0204500445 olur. Aralık [−4,1095752371; −0,0904247629]'dır.
   Sabit üst alternatif için p'yi otomatik olarak çift yönlü p'nin yarısı almak yanlıştır.
8. t=0, çift yönlü p=1, üst ve alt p=0,5;
   aralık [−2,0095752371; 2,0095752371], `null_aralikta=1`.
   Reddetmeme H0'ın ispatı değildir.
9. Fark=4,2, SE=2, δ0=0 olur; t ve bütün p-değerleri aynıdır.
   Aralık ve genişlik iki katına çıkar: [0,1808495257; 8,2191504743].
   Birim değiştirmek anlamlılık üretmez.
10. t=1,1; çift yönlü p=0,2767070487, H0 reddedilemez.
    Güven aralığı değişmez; [0,0904247629; 4,1095752371] artık test edilen
    1 değerini içerir. Aralık tahmin, SE, df ve güven düzeyine bağlıdır.
11. t=4,2; çift yönlü p=0,0001123023;
    aralık [1,0952123814; 3,1047876186]'dır. Hata payı yarıya iner.
    Örneklem büyüklüğünün değişimi bu özetten tek başına çıkarılamaz;
    SE'nin yalnız n'ye bağlı olduğu ayrıca varsayılmamıştır.
12. p, H0 modeli altında en az gözlenen kadar uç istatistiğin olasılığıdır;
    H0'ın doğru olma olasılığı değildir. %1 düzeyinde reddetmeme,
    etkisizliğin kanıtı değildir. Pratik önem için farkın birimi,
    bağlamı, güven aralığı ve önceden belirlenmiş önem eşiği gerekir.

Sayılar yalnız sunumda yuvarlandı. Değiştirilmiş girdilerle özgün 20 kontrolün
geçmesi beklenmez. Alıştırma sonuçları Python'da kontrol edildi; R/SPSS'te
çalıştırma doğrulaması henüz yapılmadı.