# Tanı grafiklerinin metin karşılığı

`ciktilar/python/coklu-regresyon-tani.png` iki paneldir.
Solda x ekseni uydurulan puan, y ekseni gözlenen−uydurulan artıktır.
Artıklar sıfır çizgisinin iki yanına ±1 ve ±2 seviyelerine yerleşir.
Aynı konuma düşen noktalar üst üste gelebilir; bu örnekte her nokta bağımsız
bir gerçek öğrenci gözlemi olarak yorumlanmamalıdır.

Sağda normal Q-Q grafiğinde sıralı artıklar normal kuramsal kantillerle
karşılaştırılır. Ayrık ve tasarlanmış artık dizisi gerçek normal hata
örneklemi değildir. Grafik güzel görünse bile hata varsayımları kanıtlanmaz.

R aynı iki tanı türünü üretir, ancak çizgi ve kantil varsayılanları bire bir
aynı değildir: Python SciPy probplot uyum çizgisi, R qqline çeyreklik
çizgisi kullanır. Piksel eşitliği beklenmez. R grafiği burada üretilmedi.