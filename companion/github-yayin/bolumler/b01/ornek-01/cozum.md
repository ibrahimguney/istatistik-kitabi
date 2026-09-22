# Açıklamalı çözüm

## Veri yapısı

Her satır bir öğrencidir. Beş gözlem, üç değişken vardır; eksik hücre yoktur.
Devam nicel/oran; başarı nicel ve bu öğretim örneğinde aralık ölçeği
varsayımıyla; program nominal kategoriktir. Gerçek bir başarı ölçeğinin
özellikleri bu küçük tablodan doğrulanamaz. 80 puan, 40 puanın iki katı
başarı anlamına gelmez; program etiketlerinin ortalaması alınmaz.

## Hesap

| Büyüklük | Hesap | Sonuç |
|---|---|---:|
| Ortalama devam | (8 + 10 + 7 + 12 + 9) / 5 | 9,2 saat |
| Ortalama başarı | (68 + 75 + 64 + 83 + 72) / 5 | 72,4 puan |
| A frekansı | A etiketli satır sayısı | 3 |
| A oranı | 3 / 5 | 0,60 = %60 |
| B frekansı | B etiketli satır sayısı | 2 |
| B oranı | 2 / 5 | 0,40 = %40 |

Devam 7–12 saat, başarı 64–83 puan arasındadır. Her değişkende geçerli
sayısı 5, eksik sayısı 0'dır. Kontrol CSV'si bu bilgileri 18 satırda toplar.

## Rapor ve yorum

“Beş gözlemlik öğretim verisinde ortalama devam 9,2 saat, ortalama başarı
72,4 puandır. Üç gözlem A (%60), iki gözlem B (%40) programındadır.
Tabloda eksik değer bulunmamaktadır.”

Bu sayılar yalnız beş satırı betimler. Veriler yapaydır; rastgele örnekleme
veya rastgele atama bilgisi yoktur. Üniversite evreninin ortalaması,
programın etkisi veya devamın başarıya nedensel etkisi olarak raporlanamaz.