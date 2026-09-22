# B07 — Alıştırmalar

Kaynak CSV'leri değiştirmeyin; yeni senaryoları ayrı hesaplayın.
Yanıtlar [cozumler.md](cozumler.md) içindedir.

1. On yanıttan oranı ve yerine-koyma yaklaşık SE'sini hesaplayın.
2. Parametre, tahmin edici ve gerçekleşmiş tahmini ayırın. İlk on yanıtın
   bilinmeyen p'si ile benzetimdeki 0,40 aynı kabul edilebilir mi?
3. Olay tanımını ters çevirip 1−yanit kullanın. Oran ve yaklaşık SE nasıl değişir?
4. Gözlenen örneğe bir olumlu yanıt ekleyin. Yeni oranı ve yaklaşık SE formülünü yazın.
5. Sıfırları yanlışlıkla eksik sayıp silerseniz oran ve yaklaşık SE ne olur?
   Bu sonuç kesinlik kanıtı mıdır?
6. p-hat=0,60 sabitken n=25 ve n=400 standart hatalarını ve aralarındaki oranı bulun.
7. p=0,40, n=50 için kuramsal yanlılığı, varyansı, MSE'yi ve SE'yi bulun.
8. Aynı modelde n=200 olursa varyans/MSE ve SE nasıl değişir?
9. Ampirik MSE=ampirik varyans+ampirik yanlılık² özdeşliğinde hangi bölen kullanılır?
   B−1 varyansını nasıl dönüştürürsünüz?
10. Ampirik yanlılık −0,001582 olduğunda neden hemen “oran tahmin edicisi yanlıdır” diyemeyiz?
    B=10000 benzetim merkezinin Monte Carlo SE'sini hesaplayın.
11. İleri çalışma: X~Binom(50,0,40) iken T=(X+1)/52 tahmin edicisinin
    yanlılığını ve MSE'sini bulun. Yansız X/50 ile karşılaştırın.
12. Ortak CSV'yi R'de çözmekle `rbinom` kullanarak yeni veri üretmek aynı
    doğrulama mıdır? İki durumda hangi eşitlik/yakınlık beklenir?