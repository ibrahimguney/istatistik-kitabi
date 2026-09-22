# B12 alıştırma çözümleri

1. Satırlar kategori çiftlerinin sayım özetleridir; N=30+10+20+20=80.
   Frekans sütununu yok saymak analizi dört gözlem üzerinden yanlış kurar.
2. Satır yüzdesi 30/40=%75; sütun yüzdesi 30/50=%60;
   toplam yüzdesi 30/80=%37,5. Paydalar farklı soruları yanıtlar.
3. İki satırda da beklenenler (25,15)'tir; en küçük beklenen 15'tir.
4. Katkılar (1,5/3) ve (1,5/3); χ²=16/3≈5,3333333333.
5. df=1, p=0,0209213353. %5 düzeyinde H0 reddedilir; %1 düzeyinde
   reddedilemez. p değişmez; bu paketin betikleri sabit %5 kararını raporlar.
6. Artıklar (+1,−1,2909944487) ve (−1,+1,2909944487)'dir.
   Her birinin karesi hücre katkısını verir. Artıkların işaretleri örüntüyü
   gösterir; hücre bazında bağımsız anlamlılık kararları değildir.
7. V=√((16/3)/80)=0,2581988897. V negatif olmayan büyüklük ölçüsüdür;
   yön ve hangi grupta başarı fazlalığı olduğu satır oranlarıyla açıklanır.
8. Genel χ², p ve V aynı kalır; satır oranları ve artık satırları
   kategori adlarıyla birlikte yer değiştirir. CSV satır sırasını değiştirmek
   ise etiketleri değiştirmek değildir ve hiçbir sayısal sonucu değiştirmez.
9. N=160, χ²=32/3≈10,6666666667 olur; V ve satır oranları aynı kalır,
   p küçülür. Pearson artıkları √2 ile çarpılır. Bu hesap yalnız daha büyük
   bağımsız bir örneklem aynı oranları üretirse geçerli bir duyarlılık
   senaryosudur; kayıt kopyalamak bağımsız bilgi veya örneklem yaratmaz.
10. Gözlenenler beklenenlere eşittir: χ²=0, p=1, V=0, bütün artıklar 0.
    Bu örneklemde sapma yoktur; evrende bağımsızlık kanıtlanmış olmaz.
11. Her satırın beklenenleri (2,5;1,5), en küçüğü 1,5'tir.
    Bu pilot tüm beklenenleri en az 5 istediğinden durur. Tasarım uygunsa
    Fisher kesin testi gibi bir yöntem ayrıca değerlendirilir; p üretmek
    için frekans şişirme veya keyfî kategori birleştirme yapılmaz.
12. Ölçümler aynı kişilere ait olduğu için bağımsız değildir.
    Eşleştirilmiş ikili değişimin incelenmesinde McNemar testi düşünülebilir;
    kişi bazında eşleşmiş geçiş sayıları gerekir. İki ayrı başarı yüzdesi
    bu geçişleri yeniden kurmaya yetmez.

Sayısal yanıtlar Python'da denetlendi; R/SPSS'te çalıştırma kontrolü bekliyor.
Yuvarlama yalnız raporlamada yapıldı. Değişmiş tabloyla özgün 32 kontrolün
geçmesi beklenmez.