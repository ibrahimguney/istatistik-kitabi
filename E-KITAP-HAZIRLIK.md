# E-kitap hazırlık durumu

Denetim tarihi: 22 Eylül 2026

## Dijital sürüm özellikleri

- PDF e-kitap için tek taraflı sayfa düzeni kullanılır.
- Ön ve arka kapak, aynı renk ve istatistik görseli ailesini kullanan
  çözünürlükten bağımsız vektör tasarımlardır.
- Bölümler sağ sayfaya zorlanmadığından gereksiz boş sayfalar kaldırılır.
- İç bağlantılar, kaynakça atıfları ve internet adresleri tıklanabilirdir.
- PDF açıldığında yer imleri panelinin gösterilmesi istenir.
- Türkçe belge dili, başlık, yazar, konu, anahtar sözcükler ve telif bilgisi
  PDF metadata ve XMP metadata içinde bulunur.
- Fontlar PDF içine gömülür.
- Sabit mizanpaj; 6 × 9 inç kitap ölçüsü, 10/12 punto Libertinus gövde
  yazısı, yaklaşık 75 karakterlik satır ve profesyonel kitap kenar boşlukları
  kullanır.
- Nokta tahmini, ANOVA ve parametrik olmayan yöntemlerde beş ölçeklenebilir
  yöntem seçimi/karar şeması bulunur.
- Eksik veri ve veri kalitesi için MCAR--MAR--MNAR, çoklu atama, duyarlılık
  analizi ve Python--SPSS--R uygulamalarını içeren bağımsız bölüm bulunur.
- Yirmi bölümün tamamında öğrenme hedefi, hazırlık/ön koşul, temel kavram,
  çözümlü uygulama, karar-hata kontrolü, kaynak ve uygulama-yansıtma
  bileşenlerinden oluşan ortak pedagojik omurga kullanılır.
- Basılı sürüm ve PDF/X dosyaları ayrı tutulur.

## Doğrulanan çıktı

- Dosya: `ebook.pdf`
- Sayfa sayısı: 381
- PDF yer imi: 429
- Tıklanabilir bağlantı: 1.503
- Gömülü font ailesi: 8; gömülmemiş font yoktur.
- XMP yazar bilgisi: İbrahim Güney
- Belge dili: `tr-TR`
- Açılış görünümü: yer imleri paneli
- Çözülmemiş atıf veya çapraz başvuru: yok
- LaTeX derleme hatası: yok

## Üretim

Proje kökünde:

```sh
./build-ebook.sh
```

Nihai dağıtım dosyası `ebook.pdf` olarak oluşturulur.

## Yayıncıdan alınabilecek bilgiler

- E-kitap için ayrı ISBN/e-ISBN atanmışsa `print-config.tex` içindeki
  `\BookISBN` alanına yazılmalıdır.
- Yayınevi yayın numarası varsa `\BookPublicationNumber` alanına yazılmalıdır.

Bu bilgiler henüz verilmediyse e-kitap teknik olarak üretilebilir; ancak
resmî yayınevi dağıtımından önce künye bilgilerinin tamamlanması önerilir.

## Erişilebilirlik notu

Mevcut PDF; aranabilir metin, yer imleri ve bağlantılar içerir. PDF/UA
etiketleme ve ekran okuyucu okuma sırası için ayrıca erişilebilirlik denetimi
gerekir. Yayınevi PDF/UA uyumlu teslim istiyorsa bu çalışma ayrı bir yayın
profili olarak ele alınmalıdır.