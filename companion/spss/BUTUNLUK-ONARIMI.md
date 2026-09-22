# SPSS paketinin bütünlük onarımı

**13 Eylül 2026 güncellemesi:** Aşağıdaki 12 Eylül işlemi tarihsel
kayıttır. Güncel bölüm bloklarıyla eşleştirme için `README.md` içindeki
`build_package.py`, `build_b01_pilot.py`, `validate_package.py` akışını
kullanın. Eski manifestler `manifest-history/` altında korunur.
Eski onarım betiğinin `--apply` yolu artık kullanılmaz. Güncel kontrol
ve onarım kaydı `docs/denetim/TUTARLILIK-KONTROLU.md` içindedir.

12 Eylül 2026: ana paketin 61 ve B01 pilotunun 8 kaydı özgün manifest
özetleriyle bire bir eşleşti. IBM SPSS ve R çalıştırılmadı.

## Önce yalnız kontrol edin

Proje kökünden, mevcut Python + NumPy/pandas/SciPy ortamında:

```
python companion/spss/butunluk_onar.py.txt
```

Varsayılan komut paket dosyalarını değiştirmez; build altında envanter,
hazırlık çıktıları, yedekler ve rapor oluşturabilir. Güncel onarılmış
kopyada `DRY RUN 0 changes; 69 manifest entries` beklenir.

Doğrulanabilen düzeltmeleri yedekleyerek uygulamak için:

```
python companion/spss/butunluk_onar.py.txt --apply
python companion/spss/validate_package.py
```

Aracı veya onaylanmış manifestleri rastgele başka dosyalarla değiştirmeyin.
Mevcut dosyadaki fark, izin verilen satır sonu dönüşümleriyle özgün SHA-256
özetine ulaşmıyorsa araç durur; sayısal farkı normalleştirme adı altında gizlemez.
CSV hücreleri ve JSON nesneleri ayrıca karşılaştırılır.

Eksik dosyalar için mevcut `build_package.py`, B01 kitap komutları ve pilot
verisi kullanılır; bütün adaylar yazmadan önce özgün manifestle karşılaştırılır.
Desteklenmeyen eksik dosya veya açıklanamayan fark varsa paket değiştirilmez.
Manifestler yenilenmez. Paket verileri SPSS/R ile analiz edilmiş sayılmaz.

## Neler değişti?

- 42 ana paket dosyası ve 3 pilot dosyası eksik yerlere eklendi.
- 18 ana paket ve 4 pilot dosyası yalnız satır sonları bakımından düzeltildi.
- Ham CSV dahil bu metin dosyalarının bayt özetleri değişti; veri hücreleri aynı kaldı.
- Özgün iki manifestin baytları değişmedi.

12 Eylül 2026 sadeleştirmesinden sonra eski yedekler ve ayrıntılı
önce/sonra özetleri `arsiv/temizlik-oncesi-2026-09-12.zip` içindeki
`build/butunluk-onarimi-2026-09-12/` yolunda saklanır.
Yeni çalıştırmalar yine `build/` altında yeni işlem klasörü oluşturur.

Gerçek klasördeki sayısal ve bütünlük kontrolü, tekrar çalıştırmada sıfır
değişiklik sonucu ve geçici kopyada sayısal bozulmayı reddetme testi geçti.
Geçmiş denetim günlükleri de bu arşivdedir. Yedekleri doğrulamadan silmeyin.

## Sonraki adım

SPSS 29'da B01 pilotunu çalıştırıp SPV/PDF çıktısını karşılaştırın.
Önceki sohbette tamamlandığı belirtilen üç ek SPSS uygulaması bu çalışma
alanında bulunamadı; onları veya 302 sayfalık sürümü bu kontrol onaylamaz.
Bu araç kitap bölümleri oluşturmaz ve GitHub'a yükleme yapmaz.