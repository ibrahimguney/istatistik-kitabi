# B11 alıştırma çözümleri

1. İlk örnekte 58 kişi iki bağımsız gruptadır. İkinci örnekte 20 tam
   çiftin kişi bazlı farkları analiz edilir; bu iki örnek ayrıdır.
   Eşit hacim eşleşme kanıtı değildir, eşleşme tasarımla belirlenir.
2. Katkılar 2,1333333333 ve 3,5714285714;
   SE=2,3884643403, df=51,7113093118.
3. Fark=6; t=2,5120743479; p=0,0151628686;
   yüzde 95 aralık [1,2065586920; 10,7934413080]. α=0,05'te ret vardır.
4. 56 eşit varyanslı birleşik testin serbestliğidir; Welch farklı formül
   kullanır. 52'ye yuvarlamak da p ve kritik değeri değiştirir; tam duyarlık korunur.
5. SE=1,1180339887; df=19; t=3,7565942022; p=0,0013357333;
   d_z=0,84; aralık [1,8599279679; 6,5400720321].
6. Fark=−6 ve t=−2,5120743479 olur. df ve çift yönlü p değişmez.
   Aralık [−10,7934413080; −1,2065586920]'dır. Hacim ve standart sapmalar
   da kendi gruplarıyla birlikte yer değiştirmelidir.
7. Ortalama fark=−4,2; t=−3,7565942022, d_z=−0,84;
   p=0,0013357333 aynı kalır. Aralık [−6,5400720321; −1,8599279679]'dır.
   Rapor ve grafik yön tanımları da ön−son olarak güncellenmelidir.
8. Ortalamalara ortak 10 eklemek farkı, SE'yi, t/p/df'yi ve Welch
   fark aralığını değiştirmez. Tüm puanları pozitif 2 ile ölçeklemek her
   farkı, SE'yi ve aralık uçlarını ikiye katlar; t/p/df ve d_z değişmez.
   İki grup ortalamasına sabit eklemekle fark ortalamasına sabit eklemek aynı işlem değildir.
9. Welch p≈0,01516>0,01: H0 reddedilemez. Eşleştirilmiş
   p≈0,001336<0,01: H0 reddedilir. p'ler değişmez; aralıklar artık
   yüzde 99 olur. Reddetmeme “fark yoktur” kanıtı değildir.
10. SE=5/√80=0,5590169944, t=7,5131884044, df=79 ve d_z=0,84 olur.
    SE yarıya, t iki katına değişir. Bu bir duyarlılık hesabıdır;
    gerçek yeni gözlemler geldiğinde ortalama fark ve s_D de değişebilir.
11. s_D=√(s_son²+s_ön²−2r s_son s_ön).
    r=0,50 için s_D=8; r=0,75 için s_D=√32≈5,6568542495.
    Bu yeni varsayım özgün s_D=5 girdisinin yerine kendiliğinden geçmez.
12. Tam çift analizi için n=34, df=33'tür. Ortalama fark ve fark
    standart sapması aynı 34 çift üzerinden yeniden hesaplanmalıdır.
    Eksikliğin nedenleri temsil ve yanlılık açısından incelenmelidir;
    iki ölçümü farklı kişilerden tamamlamak eşleşmeyi bozar.

Sayısal yanıtlar Python'da denetlendi; R/SPSS'te çalıştırma kontrolü bekliyor.
Yuvarlama yalnız raporlamada yapıldı. Değiştirilmiş girdilerle özgün
34 kontrolün geçmesi beklenmez.