# B01 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: beş satırlık `ornek-01` pilotu.

## Yapılan kontroller

- Python 3.13.15, pandas 2.3.3 ile `python cozum.py --check`
  çalıştırıldı; 18 kontrol değeri 1e-9 mutlak/bağıl toleransla eşleşti.
- CSV'nin üç sütunu ve beş satırı, kitaptaki Python ve R örneklerinin
  gömülü değerleriyle ayrı ayrı karşılaştırıldı; eşleşti.
- Veri sözlüğünün değişken sırası CSV ile eşleşti.
- Python hesabının girdi veri çerçevesini değiştirmediği doğrulandı.
- Boş veri, yanlış sütun adı, eksik hücre, sonsuz sayısal değer, geçersiz
  program etiketi ve negatif devam süresi olmak üzere altı hatalı girdi
  Python çözümü tarafından reddedildi.
- Sabit ekleme, yeni öğrenci ekleme ve program ortalamalarıyla ilgili
  alıştırmaların sayısal yanıtları ayrıca hesaplandı.
- R kodunun parantez dengesi ve ortak CSV başvurusu incelendi.
- SPSS'in CSV okuma ve ölçme düzeyi komutları IBM belgeleriyle karşılaştırıldı.

## Yapılmayan kontroller

R ve IBM SPSS bu ortamda bulunmadığından bu iki betik gerçek yorumlayıcılarında
çalıştırılmadı. R sözdiziminin incelenmesi çalışma testi değildir; SPSS için
hazır `.sav` veya `.spv` çıktısı sunulmuyor. Üç yazılımda sonuç eşitliği
henüz uçtan uca doğrulanmış değildir.

## Kullanıcı bilgisayarında kalan adımlar

1. Örnek klasöründe `Rscript cozum.R --check` çalıştırın; 18 değerin
   eşleştiğini doğrulayın ve R sürümünü kaydedin.
2. Aynı çalışma dizininde `analiz.sps` dosyasını SPSS'te çalıştırın.
   Dictionary, Frequencies ve Descriptives tablolarını kontrol CSV'siyle
   karşılaştırın; yüzde/oran dönüşümünü dikkate alın ve SPSS sürümünü kaydedin.
3. Açık kaynak lisansı seçilmeden önce kullanım koşullarını belirleyin.

## Bütünlük

`MANIFEST.sha256`, kendisi dışındaki B01 dosyalarının SHA-256 özetlerini
listeler. ZIP, bu dosyaların anlık dağıtım kopyasıdır. Dosyalar değişirse
manifest ve ZIP yeniden üretilmelidir; eski doğrulama kaydı yeni sonuçların
kanıtı sayılmamalıdır. Kitabın derleme girdileri bu pilot için değiştirilmedi.