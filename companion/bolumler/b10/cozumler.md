# B10 alıştırma çözümleri

1. Test dosyasındaki 10, örneklem standart sapması s'dir; plan dosyasındaki
   10, yeni çalışma için varsayılan evren standart sapması σ'dır.
   Aynı sayı olmaları aynı kaynaktan türetildiklerini göstermez. Satırlar
   katılımcı değil özet/plan kayıtlarıdır; ham veri üretilmemiştir.
2. SE=10/√25=2, df=24, t=(55−50)/2=2,5.
3. p=0,0196541751, H0 α=0,05'te reddedilir.
   Gözlenen d=(55−50)/10=0,5'tir; pratik önem ayrıca gerekçelendirilir.
4. Aralık [50,8722028767; 59,1277971233], genişlik 8,2555942465'tir.
   50 aralık dışında kalır; aynı modeldeki çift yönlü testle uyumludur.
5. SE=1, df=99, t=5 olur. Ortalama aralığı yaklaşık [53,0158; 56,9842]'dir.
   Planın varsayımları ayrı tutulduğu için n=34'ün planlanan gücü
   0,8077775013 olarak kalır. Özet değişikliği gerçekten 75 yeni gözlem
   toplandığı anlamına gelmez; bu yalnız bir duyarlılık alıştırmasıdır.
6. Tip I hata, μ=50 doğruyken H0'ı reddetmektir. Tip II hata,
   gerçek fark planlanan 5 puan iken reddedememektir. Birincisi α=0,05;
   ikincisi n=34 ve verilen modelde β≈0,1922'dir. β her alternatifte aynı değildir.
7. Plan d=0,5; λ=0,5√34=2,9154759474;
   güç=0,8077775013, β=0,1922224987.
   `strict=TRUE` gerçek etkinin ters yönündeki ret bölgesini de güç hesabına katar.
8. n=33 gücü 0,7953658415<0,80; n=34 gücü 0,8077775013≥0,80.
   En küçük yeterli tam sayı 34'tür; hacim aşağı yuvarlanmaz.
9. Planlanan d=0,25; n=34 gücü 0,2934081849, gereken hacim 128'dir.
   Daha küçük gerçek farkı aynı hata oranlarıyla belirlemek daha çok gözlem ister.
10. Gereken hacim 44'tür. n=34 gücü hâlâ 0,8077775013'tür;
    hedef gücü değiştirmek sabit tasarımın gerçek gücünü değiştirmez.
11. n=34 gücü 0,5765038584, %80 hedef için gereken hacim 51'dir.
    Daha küçük α aynı hacimde ret eşiğini zorlaştırır; güç düşer.
    Yalnız plan α'sı değiştirildiğinden gözlenen testin p-değeri ve aralığı değişmez.
12. Planlama gücü, veri toplanmadan önce bilimsel açıdan önemli fark ve
    makul evren standart sapmasıyla hesaplanmalıdır; gözlenen p'den
    geriye doğru güç üretmek yeni kanıt sağlamaz. 34 yalnız verilen
    bağımsız normal gözlemler modeli, fark, σ, α ve hedef güç için yeterlidir.
    Kümelenme ve kayıplar ayrıca ele alınır; yeterli güç anlamlı sonucu garanti etmez.

Sayısal yanıtlar Python'da denetlendi; R/SPSS'te çalıştırma kontrolü bekliyor.
Yuvarlama yalnız raporlamada yapıldı. Değiştirilmiş girdilerle özgün 30
kontrolün geçmesi beklenmez.