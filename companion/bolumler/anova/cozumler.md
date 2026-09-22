# Alıştırma yanıtları

1. Satırlar grup özetidir; klasik toplam N=30'dur. Üç ortalamayı ham
   gözlem gibi analiz etmek grup içi 990 kareler toplamını kaybettirir.
2. (10×70+10×75+10×82)/30=75,666667; df_grup=2, df_hata=27.
3. Verilen s, grup içi n−1 paydalı örneklem standart sapmasıdır;
   SS_hata=9×36+9×49+9×25=990.
4. F=(726,666667/2)/(990/27)=9,909091.
5. Eta²=726,666667/1716,666667≈0,423301;
   omega²=(726,666667−2×36,666667)/(1716,666667+36,666667)≈0,372624.
   Omega² hata varyansı için düzeltme içerir; aynı formül değildir.
6. Hayır. Genel hipotez bütün ortalamaların eşitliğidir; çiftler ayrıca incelenir.
7. A–B farkı −5 olsa da aile düzeyi %5'te fark gösterilemedi;
   bu, iki grubun eşdeğer olduğunun kanıtı değildir.
8. C–A farkı +12, aralık [5,285705;18,714295] olur; p değişmez.
9. SE_fark=√2×se_q. Studentized range standardizasyonunda bu √2 faktörü önemlidir.
10. Ağırlık n/s²'dir. Yaklaşık df_payda=18,162110 doğrudan F dağılımına
    girer; erken yuvarlama p değerini gereksiz değiştirir.
11. Hayır. Veriler ve varsayımlar farklıdır; klasik ortak MSE kullanılmaz.
    Games–Howell gibi uygun ek karşılaştırmalar ayrı bir analiz olarak planlanabilir.
12. +10 yalnız merkezleri kaydırır; farklar, F ve p değişmez. Ortalamalar
    ve s birlikte ikiyle çarpılırsa SS ve MSE dört kat, fark/aralıklar iki kat
    olur; F, p ve etki büyüklükleri değişmez. Yalnız ortalamaları değiştirip
    standart sapmaları sabit tutmak aynı birim dönüşümü değildir.