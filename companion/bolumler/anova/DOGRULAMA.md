# ANOVA doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsamlı sürüm Bölüm 16'nın iki ayrı öğretim özeti.
Ham bireysel veri üretilmedi; kitap LaTeX girdileri değiştirilmedi.
GitHub yüklemesi, yeni ZIP veya lisans ataması yapılmadı.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ile
  `python cozum.py --check --grafik`: 70 sayısal kontrol değeri eşleşti.
  Bu, 70 ayrı test senaryosu değil karşılaştırılan referans sayısıdır.
- Klasik kareler toplamları ve Welch ağırlık/düzeltmeleri bağımsız tam
  kesir hesabıyla oluşturuldu. F sağ kuyrukları bu iki örnekte pay
  serbestliği 2 için kapalı biçimle ayrıca hesaplandı.
- Tukey kritik değeri ve düzeltilmiş p değerleri bağımsız studentized range
  integralinden hesaplandı: 160 noktalı Gauss–Hermite/Gauss–Laguerre ve kök
  araması. Kritik noktadaki CDF, 96 ve 160 noktayla 0,95'i 1e-11 içinde verdi.
- statsmodels `anova_generic` ile klasik ve Welch F, p ve payda serbestlikleri
  ayrı ayrı karşılaştırıldı; eşleşti. Bu sınamada sahte ham gözlem kullanılmadı.
- Girdiler hesaplama sırasında değişmedi.
- 14 bozuk özet, iki yöntem girişinde ayrı ayrı sınandı; 28 ret gerçekleşti:
  boş veri, yanlış sütun adı/sırası, yinelenen/eksik grup, n=1, kesirli/negatif n,
  sıfır/negatif s, eksik ortalama, sonsuz s, metin ortalama ve mantıksal n.
- NaN, değiştirilmiş sayı, ters etiket sırası ve sıfıra yuvarlanmış p içeren
  dört referans dosyası reddedildi.
- Eşit ortalamalarda F=0, p=1; bütün Tukey p'leri 1 bulundu. Negatif omega²
  tahmini korunuyor, sessizce sıfıra kırpılmıyor.
- Ortalamalara sabit ekleme ve ortalama/sapmaları birlikte ölçekleme
  sınamalarında F, p ve etki büyüklüklerinin değişmezliği doğrulandı.
- Geçici bağımsız klasörde kontrol geçti; yeniden kaydedilen üç CSV byte
  düzeyinde eşleşti. Mevcut/çalışma/üst dizine çıktı yazma istekleri reddedildi.
- Değiştirilmiş grup ortalaması ve yanlış karşılaştırma haritası ayrı ayrı
  `--check` başarısızlığı oluşturdu.
- Ortalama±SD ve Tukey grafikleri üretildi ve görsel olarak incelendi.

## R ve SPSS için kalanlar

Rscript, IBM SPSS ve PSPP bu ortamda yok; R/SPSS betikleri çalıştırılmadı.
Kaynak ve resmî belgeler incelendi; bu yorumlayıcı testi değildir.

1. `Rscript cozum.R --check --grafik` çalıştırın; 70 değeri ve `sessionInfo()`
   çıktısını kaydedin. Tukey fonksiyonları için README'deki özel toleranslar geçerlidir.
2. SPSS'te aynı örnek dizininde `analiz.sps` çalıştırın; girdi, klasik,
   Tukey ve Welch LIST tablolarını karşılaştırın; sürümü kaydedin.
3. Küçük p ve kesirli serbestlik derecelerini ekranda yuvarlamadan kontrol edin.
   Üç yazılım arasında sonuç eşitliği henüz uçtan uca doğrulanmış değildir.

## Bütünlük

`MANIFEST.json` kendisi ve Python önbellekleri dışındaki dağıtım dosyalarını
kapsar. `.sps` ve `.sps.txt` byte düzeyinde aynıdır. Dosya değişirse manifest
ve doğrulama kaydı yeniden değerlendirilmelidir; manifest yenilemek tek
başına analiz doğrulaması değildir. Bu kayıt diğer paketlerin durumunu yeniden onaylamaz.