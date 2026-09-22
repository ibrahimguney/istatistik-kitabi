# Çoklu doğrusal regresyon — kapsamlı sürüm

**Paket: `coklu-regresyon`; kapsamlı sürüm Bölüm 15. Ders sürümünde yok.**
Yerelde hazırlandı; GitHub'a yüklenmedi, ZIP veya yeni lisans oluşturulmadı.

[Örnek 01](ornek-01/README.md), kitabın R uygulamasındaki 12 satırlık yapay
veriyi kullanır: puan = 40 + 2 × saat − 3 × devamsızlık + belirlenmiş hata.
Bu gerçek öğrenci veya okul bölgesi verisi değildir. Paket çekirdek toplamsal
iki açıklayıcılı modeli kapsar; bölümün gerçek veri analizi ve etkileşim
modellerinin tamamını yeniden üretme iddiası taşımaz.

- Ortak `veri.csv`, öngörü noktası `yeni.csv`, veri sözlüğü ve kaynak kaydı.
- Python, temel R ve SPSS çözümleri; SPSS metin yedeği.
- Katsayılar, model uyumu, VIF, katsayı güven aralıkları, ortalama güven
  ve bireysel öngörü aralıkları; satır bazlı uydurulan değerler/artıklar.
- [12 alıştırma](alistirmalar.md), [yanıtlar](cozumler.md), tanı grafikleri
  ve [doğrulama kaydı](DOGRULAMA.md).

**66 Python kontrol değeri eşleşti.** R ve SPSS burada çalıştırılmadı.
Bütünlük özetleri `MANIFEST.json` içindedir. Kitabın LaTeX dosyaları
bu çalışma kapsamında değiştirilmedi; örnek bağımsız klasörde çalışabilir.