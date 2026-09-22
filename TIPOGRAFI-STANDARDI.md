# Kitap tipografi ve sayfa standardı

Denetim tarihi: 22 Eylül 2026

Bu proje sabit mizanpajlı akademik ders kitabı olarak tasarlanmıştır. Tek bir
evrensel kitap mizanpajı bulunmadığından ölçüler, uluslararası akademik ve
profesyonel yayıncılıkta yaygın olan okunabilirlik ilkelerine göre birlikte
değerlendirilmiştir.

## Sayfa ve metin alanı

- Kesim ölçüsü: 152,4 × 228,6 mm (6 × 9 inç).
- E-kitap kenarları: sol/sağ 17 mm, üst 18 mm, alt 21 mm.
- Basılı sürüm kenarları: iç 19 mm, dış 15 mm, üst 18 mm, alt 21 mm.
- Metin genişliği: 118,4 mm; gövde yazısında yaklaşık 70–75 karakterlik satır.
- Basılı sürüm çift taraflı ve sağ sayfadan bölüm açılışlıdır; PDF e-kitap
  tek taraflıdır ve gereksiz boş sayfa üretmez.

## Yazı aileleri ve ritim

- Gövde: Libertinus Serif, 10 punto ve yaklaşık 12 punto temel satır aralığı.
- Başlıklar: Libertinus Sans; gövdeden açıkça ayrılan fakat aynı aileyle
  uyumlu hiyerarşi.
- Matematik: Libertinus Math; metin rakamlarıyla görsel uyumlu.
- Kod: Libertinus Mono; küçük puntoya rağmen x-yüksekliği gövdeyle eşleştirilir.
- Gövde paragrafları arasında ek boşluk yoktur; ilk satır girintisi 1,25 em'dir.
- Bölüm ve alt bölüm öncesi/sonrası aralıklar kitap genelinde açıkça
  tanımlanmıştır.

## Dizgi ilkeleri

- Türkçe heceleme `babel` ile yürütülür.
- `microtype` ile optik kenar taşması kullanılır; XeLaTeX'te güvenilir olmayan
  font genişletmesi kapalıdır.
- Çok satırlı şekil ve tablo açıklamaları sola hizalıdır; tek satırlı
  açıklamalar ortalanır.
- Kitap tablolarında dikey çizgi yerine `booktabs` kuralları kullanılır.
- Dul ve yetim satırlar, başlıkların sayfa sonunda yalnız kalması ve kötü
  sözcük bölmeleri yüksek cezalarla sınırlandırılır.
- Metin, tablo, şekil, kod ve bilgi kutusu aralıkları tutarlı bir dikey ritim
  oluşturacak biçimde tanımlanır.

## Renk ve çıktı

- Ana metin siyah; başlıklar koyu mavi ve yüksek karşıtlıklıdır.
- Renk, tek başına bilgi taşımaz; kutu başlıkları ve biçimsel ayrımlar da
  kullanılır.
- E-kitapta bağlantılar görünür; baskı ve PDF/X profillerinde bağlantılar
  baskı görünümünü etkilemez.
- Fontların tamamı PDF içine gömülür.

Bu değerler kitabın ortak mizanpaj profilidir. Yayıncı farklı bir kesim ölçüsü
veya kurumsal şablon isterse sayfa geometrisi yeniden hesaplanmalı; yalnızca
PDF ölçeklenerek dönüştürülmemelidir.