# B13 alıştırma çözümleri

1. Her satır aynı gözleme ait saat/puan çiftidir. Sütunları ayrı sıralamak
   eşleşmeyi bozup farklı veri üretir. Satırları çift olarak taşımak genel
   modeli korur; kontrol dosyasındaki satır anahtarlarının sırası yine değişir.
2. Sxx=51, Syy=522, Sxy=160; r=0,9806175085,
   eğim=160/51=3,1372549020, sabit=59,5−eğim×4,75=44,5980392157.
3. Bir saat daha yüksek çalışma, modelin koşullu ortalamasında yaklaşık
   3,1373 puan daha yüksek son test puanıyla ilişkilidir. Her öğrenciye
   aynı artışı veya müdahaleyle bu artışın oluşacağını garanti etmez.
4. SSE=20,0392156863, df=14, MSE=1,4313725490,
   R²=0,9616106979. Açıklanan kareler toplamı payıdır; sınıflandırma
   doğruluğu değildir ve yeni örneklem performansını ölçmez.
5. SE_eğim=0,1675294852; t(14)=18,7265835514;
   p≈2,6183120271×10⁻¹¹; aralık [2,7779398923;3,4965699117].
   Çok küçük olasılık sıfır değildir; p için bilimsel gösterim kullanılmalıdır.
6. Nokta tahmini 63,4215686275; ortalama yanıt aralığı
   [62,6384597194;64,2046775355], yeni birey aralığı
   [60,7387099566;66,1044272983]. Birey aralığı ek hata değişkenliği içerir.
7. İlk artık 60−60,2843137255=−0,2843137255;
   ikinci 65−63,4215686275=+1,5784313725'tir.
8. r ve eğim aynı, sabit 54,5980392157 olur. Tahminler ve aralık uçları
   10 artar, artıklar değişmez. Aynı saat için modelin belirsizlik genişlikleri korunur.
9. Bir dakikalık eğim 3,1372549020/60=0,0522875817 puan/dakikadır;
   r değişmez. 6 saat için yeni açıklayıcı değer 360 dakika olmalıdır;
   6 dakika aynı öngörü sorusu değildir. `model_hesapla(veri, yeni_saat=360)`
   birimi değiştirilmiş veriyle kullanılabilir; varsayılan grafik etiketleri de uyarlanmalıdır.
10. 44,5980392157+3,1372549020×20=107,3431372549 puandır.
    20 saat, 2–8 saat gözlem aralığının dışındadır. Modelin doğrusal
    davranışı veya puan ölçeği o bölgede doğrulanmadığından güvenilir saha sonucu değildir.
11. r değişmez. Ters eğim Sxy/Syy=160/522≈0,3065134100 saat/puan;
    eski eğimin tersi 51/160=0,31875'tir, eşit değildir. İki regresyon
    farklı yöndeki artık karelerini en aza indirir; r²<1 iken bu ayrım önemlidir.
12. Veri girişi, ölçüm süreci, doğrusal biçim, değişen hata varyansı ve
    etkili gözlemler bağlamla birlikte incelenir; kayıtlar otomatik silinmez.
    Küçük örneklemde grafiğin görünümü koşulları kanıtlamaz. Yüksek R²,
    bağımsızlık, model uygunluğu veya nedensellik kontrolünün yerine geçmez.

Sayısal yanıtlar Python'da denetlendi; R/SPSS çalıştırma kontrolleri bekliyor.
Değiştirilmiş girdilerle özgün 62 kontrolün geçmesi beklenmez.