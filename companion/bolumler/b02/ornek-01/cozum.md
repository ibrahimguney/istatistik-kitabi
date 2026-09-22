# B02 açıklamalı çözüm

## 1. Birim ve değişkenler

Her satır bir öğrencidir; dört gözlem ve üç değişken vardır. `okul_turu`
nominal kategoriktir. `sinif` sıralı kategoriktir; kodların doğal sırası
vardır ama bunları süre veya başarı puanı gibi toplamak anlamlı değildir.
`puan` niceldir; eşit puan farklarının anlamlı olduğu öğretim varsayımıyla
aralık ölçeğinde ele alınır. Gerçek bir ölçeğin özellikleri bu tablodan
kanıtlanamaz. SPSS'teki Scale etiketi aralık/oran ayrımını tek başına çözmez.

## 2. Frekanslar ve oranlar

| Değişken | Kategori | Frekans | Oran | Yüzde |
|---|---|---:|---:|---:|
| Okul türü | Devlet | 3 | 0,75 | 75 |
| Okul türü | Özel | 1 | 0,25 | 25 |
| Sınıf | 1 | 2 | 0,50 | 50 |
| Sınıf | 2 | 1 | 0,25 | 25 |
| Sınıf | 3 | 1 | 0,25 | 25 |

Her değişkenin frekans toplamı 4, oran toplamı 1'dir. Eksik hücre olmadığı
için geçerli gözlem sayıları 4'tür. Okul frekanslarıyla sınıf frekansları
ayrı dağılımlardır; bunları toplayıp sekiz bağımsız öğrenci varmış gibi yorumlamayın.

## 3. Puan özetleri

- Genel toplam: 72 + 81 + 68 + 77 = 298; ortalama: 298/4 = **74,5**.
- En küçük puan **68**, en büyük puan **81**'dir.
- Devlet okulu toplamı: 72 + 68 + 77 = 217; ortalama: 217/3 = **72,3333**.
- Özel okulda yalnız bir gözlem vardır; ortalama bu tek puana, **81**'e eşittir.

Genel ortalama okul ortalamalarının basit ortalaması değildir:
(72,3333 + 81)/2 = 76,6667 farklıdır. Okul hacimleriyle ağırlıklandırmak gerekir:
(3 × 72,3333 + 1 × 81)/4 ≈ 74,5. Kod ara hesapları yuvarlamaz.

## 4. Parametre mi, istatistik mi?

Hedef evren bu dört kayıt olarak tanımlanan sonlu öğretim evreniyse, tamamı
listelenmiştir; 74,5 evren ortalamasıdır. Hedef daha geniş bir öğrenci
kitlesiyse bu dört satırın ortalaması bir örneklem istatistiğidir. Bunun
uygun bir evren tahmini olduğunu söylemek ayrıca örnekleme tasarımı gerektirir.
Gerçekte burada veriler yapaydır; gerçek bir öğrenci evreni hakkında kanıt değildir.

## 5. Örnek rapor

“Dört gözlemlik öğretim verisinde üç kayıt devlet (%75), bir kayıt özel
okul (%25) kategorisindedir. Sınıf düzeylerinin frekansları sırasıyla 2, 1
ve 1; genel puan ortalaması 74,5'tir. Veri yalnız verilen örneği betimler.”

Özel–devlet farkı yaklaşık 8,6667 puandır. Tek özel okul gözlemi ve yapay
veri ile okul türünün nedensel etkisi, temsili veya anlamlılık testi hakkında
bir araştırma sonucu üretilemez. Puanı yüksek olan kategori otomatik olarak
“daha iyi okul türü” ilan edilmemelidir.