# Çoklu regresyon doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsamlı sürüm Bölüm 15'in 12 satırlık yapay R örneği.
GitHub yüklemesi/ZIP yayını yapılmadı. Kitabın LaTeX dosyaları değiştirilmedi.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ile
  `python cozum.py --check --grafik` çalıştı: 66 kontrol değeri eşleşti.
  Bunlar 66 ayrı test senaryosu değil sayısal referans değerleridir.
- Kitaptaki hata dizisi ve `expand.grid` satır düzeni CSV ile karşılaştırıldı.
- SymPy tam kesirli matris hesabıyla katsayılar 40/2/−3, SSE=24 ve yeni
  noktanın h=5/24 değeri ayrıca doğrulandı. Referans p değerleri düzenlenmiş tamamlanmamış
  beta fonksiyonu yoluyla hesaplandı; çözüm t/F sağ kuyruklarını kullanır.
- statsmodels 0.14.6 ile bağımsız model uyduruldu; katsayılar, yeni öngörü,
  ortalama SE'si, ortalama güven ve bireysel öngörü aralıkları eşleşti.
- Girdi veri çerçeveleri değiştirilmedi.
- Artık–uydurulan ve normal Q-Q grafikleri üretildi ve görsel olarak incelendi.
- 20 hatalı girdi reddedildi: boş/yetersiz veri, yanlış sütun/sıra,
  eksik/sonsuz/metin/mantıksal değer, negatif saat/gün, kesirli gün,
  sabit açıklayıcı, tam doğrusal bağlantı, sabit yanıt, kusursuz uyum;
  ayrıca boş/çok satırlı/eksik/negatif/kesirli yeni nokta.
- Dört bozuk referans reddedildi: NaN, değiştirilmiş sayı, ters etiket
  sırası ve sıfıra yuvarlanmış p değerleri.
- Saat sütununa 0,4×devamsızlık eklenerek ilişkili açıklayıcı tasarımı denendi;
  eğimler 2 ve −3,8; VIF>1; dönüştürülmüş yeni noktada öngörü 44 oldu.
- Geçici bağımsız klasörde Python kontrolü geçti. `uret.py` CSV'yi byte
  düzeyinde yeniden üretti. Mevcut çıktı/veri üzerine ve üst dizine yazma reddedildi.
- Değiştirilmiş puan verisi `--check` başarısızlığı oluşturdu.

## Bekleyen çalışma kontrolleri

Rscript, IBM SPSS ve PSPP burada bulunmuyor. R/SPSS betikleri kaynak üzerinden
incelendi; resmî `lm`, `predict.lm` ve REGRESSION belgeleri örnek README'sinde
kayıtlıdır. Bu inceleme çalışma testi değildir; `.sav`/`.spv` üretilmedi.

1. Örnek dizininde `Rscript cozum.R --check --grafik` çalıştırın; 66 değeri
   ve `sessionInfo()` çıktısını kaydedin.
2. SPSS'te aynı çalışma dizininde `analiz.sps` çalıştırın. Coefficients,
   Model Summary, ANOVA, VIF ve LIST sonuçlarını referanslarla karşılaştırın.
3. SPSS sürümünü ve gerçek çıktıları kaydedin. Küçük p değerlerinde bilimsel
   gösterimi kullanın; ekranda 0,000 görünmesi p=0 değildir.

## Bütünlük ve sınırlar

`MANIFEST.json` kendisi ve Python önbellekleri dışındaki dağıtım dosyalarını
kapsar. `.sps` ve `.sps.txt` aynı içeriğe sahiptir. Dosya değişikliğinde
manifest ve doğrulama kaydı yeniden değerlendirilmelidir. Manifest yenilemek
analiz doğrulaması değildir. Bu kayıt yalnız yeni çoklu regresyon paketini
kapsar; diğer bölüm dosyalarının varlığını veya önceki testlerini yeniden onaylamaz.