# Alıştırma yanıtları

1. Aynı devamsızlıkta bir saatlik fark, modelde iki puanlık beklenen farkla ilişkilidir.
2. Aynı çalışma saatinde bir günlük devamsızlık farkı −3 puanla ilişkilidir.
   Bu yapay örnek nedensel etki kanıtı vermez.
3. 40+2×5−3×2=44; 40+2×5−3×1=47.
4. df=12−3=9; MSE=24/9=8/3≈2,666667.
5. R²=1−24/336≈0,928571; düzeltilmiş R² açıklayıcı sayısını ve serbestlik
   derecesini dikkate alır: 1−(1−R²)×11/9≈0,912698.
6. Dengeli tasarımda açıklayıcılar doğrusal olarak ilişkisizdir. VIF=1,
   bağımsız/normal/sabit varyanslı hata veya doğru nedensel modeli doğrulamaz.
7. 2±2,262157×0,210819; yaklaşık [1,523095;2,476905].
8. İlki belirli açıklayıcılardaki ortalama yanıtı, ikincisi yeni tek yanıtı
   kapsar; ikincisi ek hata varyansından dolayı daha geniştir.
9. Sabit 50 olur; eğimler 2 ve −3 kalır. Artıklar, SSE, R² ve VIF değişmez.
10. Dakika katsayısı 2/60=1/30 olur. Beş saat yerine 300 dakika kullanılırsa
    öngörü yine 44'tür. Katsayı birimi değişir; modelin öngörüsü değişmez.
11. Tasarım tam doğrusal bağlantılı olur; ayrı eğimler tanımlanamaz.
    Python/R kontrolü bu rank eksikliğini reddeder; rastgele bir katsayı çözümü sunmaz.
12. Saatin koşullu eğimi β_saat+β_etkileşim×devamsızlık olur.
    Ana saat katsayısı yalnız devamsızlık=0 için eğimi verir. Bu paketin
    çekirdek modeli etkileşim içermez; soru kavramsal genişletmedir.