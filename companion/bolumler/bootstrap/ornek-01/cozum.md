# Çözüm ve yorum

## Bootstrap ortalaması

Beş gözlemin ortalaması 5, örneklem standart sapması 4,5276925691'dir.
Ampirik dağılımın varyansı (payda 5) 16,4 olduğundan bootstrap ortalamasının
koşullu varyansı 16,4/5 = 3,28 ve standart hatası 1,8110770276 olur.
3.125 sıralı yeniden örneklemin tam sayımı aynı değerleri verir.

Tam dağılımın merkezi 5, minimumu 2 ve maksimumu 13'tür. Type 7 ile yüzde
2,5 ve 97,5 yüzdelikleri 2,6 ve 9,0 bulunur. Yüzde 95 yüzdelik bootstrap
aralığı **[2,6; 9,0]** olarak raporlanır. SPSS çözümü yüzdelik sıralarını
`1+(B-1)*p` ile hesaplayarak komşu iki sıra arasında interpolasyon yapar.

Bu sonuç gözlenen beş değerin ampirik dağılımına koşulludur. Gözlem sayısı
çok küçük ve 13 değeri etkili olduğundan aralığın gerçek evrende yüzde 95
kapsama sağlayacağı garanti edilmez. Tam sayım, Monte Carlo hatasını
kaldırır; veri seçimi yanlılığını veya bağımlılığı düzeltmez. Ortalama için
bootstrap yanlılığının burada sıfır olması, örneklemin temsili olduğunu
kanıtlamaz. İadeli bireysel örnekleme bağımsız gözlem varsayımına dayanır.

## Tam permütasyon testi

A ortalaması 8, B ortalaması 3; gözlenen A−B farkı 5'tir. Altı gözlemden
üçüne A etiketi vermenin 20 yolu vardır. Farklar −5 ile 5 arasındadır;
mutlak farkı en az 5 olan iki atama bulunduğundan çift yönlü tam p değeri
**2/20 = 0,10** olur. Bütün atamalar sayıldığı için `(uç+1)/(tekrar+1)`
Monte Carlo düzeltmesi yapılmaz. Yazılım eşitlik karşılaştırmasında 10^-12
mutlak sayısal tolerans kullanır.

Yüzde 5 düzeyinde sıfır hipotezi reddedilemez; bu, grupların eşitliğinin
kanıtı değildir. Etiketlerin değiştirilebilirliği gerekir; rastgele atama
bu koşulu sağlayabilir. Yalnız ortalamaların eşit olması, farklı dağılım
ve varyanslar altında sıradan etiket permütasyonunu tek başına gerekçelendirmez.

## Grafik açıklaması

`ciktilar/python/bootstrap-permutasyon.png` iki ayrı olasılık kütlesini
gösterir. Solda bootstrap ortalamaları ve kesikli çizgilerle 2,6/9,0
sınırları; sağda 20 atamanın ortalama farkları bulunur. Sağdaki turuncu
uç sütunlar −5 ve 5 olup her birinin olasılığı 0,05'tir. Grafik normal
bir eğriye zorlanmaz. SPSS histogramlarının binleri bu kütle grafiğinden
farklı olabilir; sayısal karşılaştırma `LIST` tablolarıyla yapılmalıdır.