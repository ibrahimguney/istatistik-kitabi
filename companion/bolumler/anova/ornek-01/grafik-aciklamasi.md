# ANOVA grafiklerinin metin karşılığı

Python `ciktilar/python/anova-tukey.png` iki panelden oluşur.
Solda A/B/C ortalamaları 70/75/82 ve ±1 standart sapma çubukları
6/7/5 gösterilir. **Bu çubuklar güven aralığı veya standart hata değildir.**
Çubukların örtüşmesinden ANOVA/Tukey kararı çıkarılmaz.

Sağda A−B, A−C, B−C için Tukey %95 eşzamanlı fark aralıkları vardır.
Dikey kesikli çizgi sıfırdır. A−B aralığı sıfırı içerir; A−C ve B−C
aralıkları bütünüyle negatiftir. B−C'nin üst sınırı yaklaşık −0,2857 ile
sıfıra yakındır fakat negatiftir. Grafik tam duyarlıkla hesaplanan aralıkları kullanır.

R grafiği yalnız Tukey fark panelini içerir ve `ciktilar/r/tukey-araliklari.png`
adıyla üretilir; burada çalıştırılmadı. Welch için bireysel ölçüm ya da
artık grafiği çizilmedi; bunlar grup özetlerinden elde edilemez.