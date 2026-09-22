# Açıklamalı çözüm

## 1. Korelasyon ve regresyon doğrusu

n=16, ortalama saat=4,75 ve ortalama puan=59,5'tir.
Merkezli toplamlar Sxx=51, Syy=522 ve Sxy=160 olur.

`r = 160/√(51×522) = 0,9806175085`.

`b₁ = Sxy/Sxx = 3,1372549020`, `b₀ = 59,5−b₁×4,75 = 44,5980392157`.

Model: `tahmin edilen puan = 44,5980392157 + 3,1372549020 × saat`.
Bir saat daha yüksek çalışma süresi, bu modelde ortalama puanda yaklaşık
3,1373 puanlık artışla ilişkilidir; her birey için garanti veya nedensel
müdahale etkisi değildir. Sabit terim 0 saatteki model değeridir; 0 saat
veride gözlenmemiştir, bilimsel yorumu ayrıca gerekçelendirilmelidir.

## 2. Belirsizlik ve uyum

SSE=20,0392156863, df=14 ve MSE=1,4313725490'dır.
Eğim standart hatası 0,1675294852; t(14)=18,7265835514 olur.
Çift yönlü p≈**2,6183120271×10⁻¹¹**'dir; sıfır değildir.

| Katsayı | Tahmin | Yüzde 95 güven aralığı |
|---|---:|---|
| Sabit | 44,5980392157 | [42,7747146801; 46,4213637512] |
| Eğim | 3,1372549020 | [2,7779398923; 3,4965699117] |

R²=1−SSE/Syy=0,9616106979=r². Bu veride puanların ortalama etrafındaki
kareler toplamının yaklaşık %96,16'sı modelle açıklanır; öğrencilerin
%96,16'sı doğru tahmin edildi demek değildir. Yeni veri başarısı ölçülmedi.

## 3. Altı saat için iki farklı aralık

Nokta tahmini 63,4215686275 puandır. h₀=1/n+(6−ortalama saat)²/Sxx olsun.

- Ortalama yanıt standart hatası √(MSE×h₀)=0,3651220480.
- Yeni birey öngörüsünün standart hatası √(MSE×(1+h₀))=1,2508743578.
- Yüzde 95 **ortalama yanıt güven aralığı**: [62,6384597194; 64,2046775355].
- Yüzde 95 **yeni birey öngörü aralığı**: [60,7387099566; 66,1044272983].

İki aralık aynı merkezde, farklı hedefler içindir; bireysel değişkenlik
ikinci aralıkta ayrıca yer alır. Bunlar tek noktadaki aralıklardır, tüm
doğruyu aynı anda kapsayan eşzamanlı güven bantları değildir.

6 saat gözlenen 2–8 saat aralığındadır. 20 saatin matematiksel öngörüsü
107,3431372549 puandır; bu dışa taşırmadır. Doğrusal model aralık dışında
anlamlı veya uygulanabilir sonuç garanti etmez, puan sınırını kendiliğinden uygulamaz.

## 4. Artık ve raporlama

İlk satırda 5 saat/60 puan için tahmin 60,2843137255,
artık −0,2843137255'tir. 6 saat/65 puan gözleminde artık
+1,5784313725'tir; gözlenen puan tahminden bu kadar yüksektir.
Sabit terimli en küçük karelerde artıkların toplamı sayısal tolerans içinde
sıfırdır; bu özellik tek başına modelin doğru kurulduğunu kanıtlamaz.

Örnek rapor: “16 gözlemde r=0,9806; eğim 3,1373 puan/saat,
%95 GA [2,7779; 3,4966], t(14)=18,7266, p≈2,62×10⁻¹¹,
R²=0,9616 bulundu. Altı saat için ortalama öngörü 63,4216 puandır;
ortalama yanıt ve yeni birey aralıkları ayrı raporlanmıştır.”

Bu rapora veri kaynağı, ölçüm zamanı, örnekleme yöntemi ve tanı grafikleri
üzerinden koşul değerlendirmesi eklenmelidir. Otomatik değişken seçimi,
aykırı kayıt silme veya nedensel etki hesabı yapılmamıştır.