# B14 karma alıştırma çözümleri

1. Aynı kişiler ölçüldüğünden eşleştirilmiş t; D=son−ön,
   hedef μ_D; H0: μ_D=0, H1: μ_D≠0. İki ayrı bağımsız örneklem varsayılmaz.
2. İki ölçüm aynı kişiye aittir. Analiz 24 kişi farkıyla yapılır;
   df=23'tür. Kişiler arası bağımsızlık yine değerlendirilmelidir.
3. s_D=6 bireysel farkların yayılımıdır; SE=6/√24=1,2247448714,
   ortalama farkın örnekleme belirsizliğini temsil eder.
4. t=−2,6127890590, çift yönlü p=0,0155576312. İşaret fark tanımına
   bağlıdır; test yönü sonradan p küçültmek için değiştirilmez.
5. Aralık [−5,7335777990;−0,6664222010], genişlik 5,0671555981'dir.
   Sıfırı içermez; aynı çift yönlü %5 testle uyumludur. Bireysel fark
   dağılımının aralığı değildir.
6. d_z=−0,5333333333. Son−ön tanımıyla son puan daha düşüktür.
   Düşmenin anlamı ölçeğin yönüne bağlıdır; her öğrenciye veya nedensel
   müdahale etkisine genellenmez.
7. Ortalama fark +3,2, t=+2,6127890590, d_z=+0,5333333333;
   çift yönlü p aynı kalır. Aralık [+0,6664222010;+5,7335777990] olur.
   Yön etiketleri de ön−son diye değiştirilmelidir.
8. p değişmez; 0,0155576312>0,01 olduğundan H0 reddedilemez.
   Betikte α=0,01 yapılırsa aralık %99 olur, genişler ve sıfırı içerir.
   Reddetmeme eşdeğerlik veya “değişim yok” kanıtı değildir.
9. Bağımsız iki nicel grup için koşulları değerlendirilmiş Welch t;
   aynı kişilerin nicel ölçümleri için farklar üzerinden eşleştirilmiş t.
   İki sınıfın hacimlerinin eşit olması eşleşme yaratmaz; sınıf kümelenmesi
   varsa kişiler otomatik bağımsız kabul edilmez.
10. Bağımsız kategorik gözlemlerde çapraz tablo/Pearson testi ve beklenen
    frekanslar değerlendirilir. Aynı kişilerin ikili geçişleri bağımlıdır;
    McNemar gibi eşleştirilmiş yöntemler düşünülür. Tek başına iki başarı
    oranı hangi kişinin durum değiştirdiğini göstermez.
11. Eğim=r×s_Y/s_X=2, sabit=60−2×4=52; doğru Y_tahmin=52+2X.
    R²=0,25; X=7 için öngörü 66'dır. t=0,5√(48/(1−0,25))=4,
    df=48 ve klasik çift yönlü p<0,001'dir. İlişki nedensel artış
    değildir; verilen özet X'in gözlenen aralığını belirtmediğinden 7'nin
    iç değer mi dışa taşırma mı olduğu ayrıca kontrol edilmelidir.
12. Kolayda/gönüllü seçim kütüphaneyi kullanmayanları ve yanıtlamayanları
    farklı temsil edebilir. Büyük n rastgele hatayı azaltabilse de seçim
    yanlılığını kendiliğinden kaldırmaz. Hedef evren ve seçim mekanizması
    açıklanmadan bütün üniversite için temsil iddiası kurulmaz.

Sayısal yanıtlar Python'da denetlendi; R/SPSS çalıştırma kontrolleri bekliyor.
17 otomatik kontrol yalnız ana eşleştirilmiş örneğe aittir; karma soruların
yöntem gerekçeleri otomatik puanlanmaz.