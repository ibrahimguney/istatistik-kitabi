# B14 yöntem seçimi ve sınav yanıtı rehberi

## Önce soru, sonra formül

| Araştırma hedefi / gözlem yapısı | Başlangıç yöntemi | Yanıtta unutulmaması gereken |
|---|---|---|
| Tek ortalamayı tahmin etmek | Standart hata ve güven aralığı | Hedef evren ortalaması; aralık bireyler için değildir |
| Tek ortalamayı referansla karşılaştırmak | Tek örneklem t | Referans ve yön önceden belirlenir |
| İki bağımsız nicel grup | Welch t | Bağımsızlık; eşit varyans varsayımı zorunlu değildir |
| Aynı kişilerin iki nicel ölçümü | Eşleştirilmiş t | Tam çiftler, fark yönü ve farkların dağılımı |
| Tek kategorik dağılım ve belirli kuramsal oranlar | Ki-kare uyum iyiliği | Kategoriler, kuramsal oranlar ve beklenen sayılar |
| İki kategorik değişken / bağımsız gözlemler | Çapraz tablo ve Pearson bağımsızlık testi | Yüzde paydası, beklenen sayılar; seyrek 2×2 için kesin yöntem değerlendirmesi |
| Aynı kişilerin iki ikili ölçümü | McNemar gibi eşleştirilmiş ikili yöntem | Kişi bazlı geçişler; bağımsız çapraz tablo testiyle karıştırılmaz |
| İki nicel değişkenin doğrusal ilişki gücü | Pearson korelasyonu | Saçılım, doğrusal biçim; nedensellik değildir |
| Nicel yanıtı tek açıklayıcıyla öngörmek | Basit doğrusal regresyon | Hata modeli, öngörü noktası ve aralık türü |

Bu tablo son karar makinesi değildir. Örnekleme, bağımsızlık, ölçüm anlamı
ve yönteme özgü koşullar ayrıca değerlendirilir. Küçük p veren yöntemi
seçmek, koşul kontrolü yapmak değildir. Bootstrap, çoklu regresyon ve
ANOVA kapsamlı sürümün ayrı paketlerine aittir; bu rehberde çalıştırılmış
analizler olarak sunulmaz. Oran aralığı da ortalama t aralığına otomatik çevrilmez.

## Altı adımlı yanıt şablonu

1. **Tanımla:** Hedef evren, parametre, değişken türü ve gözlem birimi nedir?
2. **Seç:** Yöntem neden bu araştırma sorusuna ve bağımsız/eşleşmiş yapıya uygundur?
3. **Kontrol et:** Hangi koşullar gerekli; hangileri mevcut bilgiyle doğrulanamıyor?
4. **Hesapla:** Tahmin, SE, df, istatistik, p, aralık ve uygun etki büyüklüğünü yaz.
5. **Karar ver:** Önceden belirlenmiş α ve test yönüyle karar ver; p'yi yuvarlayarak eşik kararı verme.
6. **Yorumla:** İşareti, büyüklüğü, belirsizliği ve tasarım/genelleme sınırlarını bağlamla açıkla.

## B14 için kendi kendine kontrol

- D=son−ön ve μ_D yazdım mı?
- 24 tam çift ile 48 bağımsız kişi iddiasını ayırdım mı?
- Standart sapma 6 ile standart hata yaklaşık 1,2247'yi ayırdım mı?
- Sadece “anlamlı” demek yerine negatif farkı ve güven aralığını verdim mi?
- d_z'nin hangi standart sapmayla hesaplandığını belirttim mi?
- Ölçek yönünü ve kontrol grubu bulunmadığını yorumladım mı?
- Ham veri yokken normal dağılım/aykırı değer kontrolü yapılmış gibi yazmaktan kaçındım mı?

Bu liste resmi notlandırma anahtarı veya otomatik puanlayıcı değildir.
[Çözümlü örnek](ornek-01/cozum.md) ve [karma alıştırmalar](alistirmalar.md)
ile birlikte kullanılabilir.