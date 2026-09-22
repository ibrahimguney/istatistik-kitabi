# Açıklamalı çözüm

## Model ve katsayılar

Uydurulan model: **puan = 40 + 2×saat − 3×devamsızlık**.
12 gözlem ve sabit dahil üç katsayı olduğundan artık serbestlik derecesi 9'dur.
Hata kareler toplamı SSE=24, toplam kareler SST=336, MSE=24/9=2,666667;
artık standart sapması √MSE≈1,632993'tür.

| Terim | Katsayı | Standart hata | %95 güven aralığı |
|---|---:|---:|---|
| Sabit | 40 | 1,290994 | [37,079568; 42,920432] |
| Saat | 2 | 0,210819 | [1,523095; 2,476905] |
| Devamsızlık | −3 | 0,577350 | [−4,306057; −1,693943] |

Devamsızlık aynı tutulduğunda bir saatlik fark iki puanlık beklenen farkla
ilişkilidir. Saat aynı tutulduğunda bir günlük devamsızlık farkı −3 puanla
ilişkilidir. Bu tasarlanmış ilişkiler nedensel etki tahmini değildir.
Sabit terim sıfır saat/sıfır gün noktasına karşılık gelir; saat=0 gözlenen
2–8 aralığının dışındadır, bu yüzden gerçek veri yorumunda ayrıca dikkat gerekir.

## Uyum ve VIF

R²=13/14≈0,928571; düzeltilmiş R²≈0,912698.
F(2,9)=58,5; modelin ortak eğim sıfır hipotezi için p≈0,000006957.
Bunlar model-temelli hesaplama örnekleridir; gerçek evrene kanıt değildir.

Tam dengeli 4×3 tasarımda iki açıklayıcının merkezlenmiş çapraz çarpımı
sıfırdır; iki VIF de 1 olur. Düşük VIF yalnız doğrusal çoklu bağlantı
sorununun bu açıklayıcılarda görülmediğini belirtir; dışlanmış değişken,
hatalı fonksiyon biçimi, nedensellik veya artık varsayımları hakkında garanti vermez.

## Yeni nokta

Beş saat ve iki gün için öngörü **44 puan**.
Yeni noktanın h değeri 5/24; ortalama SE'si √(5/9)≈0,745356,
bireysel öngörü SE'si √(29/9)≈1,795055'tir.

- Ortalama yanıtın model-temelli %95 güven aralığı: **[42,31389; 45,68611]**.
- Yeni tek bireyin model-temelli %95 öngörü aralığı: **[39,93930; 48,06070]**.

İkinci aralık yeni bireyin hata değişkenliğini de içerdiği için daha geniştir.
Aynı beş saatte devamsızlık bir güne inerse öngörü **47** olur.
Bu üç puanlık farkın bir müdahalenin nedensel etkisi olduğu söylenemez.

## Tanı ve sınırlar

Artıklar üretimde belirlenen ±1 ve ±2 değerleridir; rastgele normal hatalar
değildir. Grafikler tanı okumayı öğretir, normal hata veya bağımsızlık
varsayımını doğrulamaz. Gerçek kullanımda araştırma tasarımı, doğrusal
model biçimi, sabit hata varyansı, aykırı/etkili gözlemler ve tahmin
aralıkları için hata dağılımı ayrıca değerlendirilmelidir.