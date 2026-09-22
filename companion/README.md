# İstatistik kitabı veri ve kod paketi

**13 Eylül 2026:** Literatür uygulamalarının güncel üretim ve denetim akışı
`spss/README.md` içindedir. Küçük öğretim paketleri için
`python -B companion/bolumler/kontrol.py` kullanılır. Önceki manifestle
kanıtlanan satır sonu/eksik SPSS kopyası onarımı, ayrı
`companion/bolumler/onar_satir_sonlari.py` aracındadır. Güncel sonuçlar
`docs/denetim/TUTARLILIK-KONTROLU.md` dosyasında kayıtlıdır; aşağıdaki
10 Eylül özeti tarihsel kontrolü anlatır.

Bu klasör, kitaptaki analizlerin gerçek verilerle ve yeniden üretilebilir
kodla yürütülmesi için ortak çalışma alanıdır. Paket üç ilkeye dayanır:

1. Ham veri değiştirilmez; analiz için yapılan bütün dönüşümler kodla üretilir.
2. Her değişkenin anlamı, birimi, eksik değer kuralı ve analiz düzeyi veri
   sözlüğünde açıklanır.
3. Her tablo ve şekil, sabit bir betikten yeniden üretilebilir.

## Tamamlayıcı V1 vakası — 13 Eylül 2026

Colt Park bloklu deneyinin ayrı veri, kaynak ve Python paketi
`vakalar/v1-colt-park/README.md` içindedir. Kendi manifesti vardır;
aşağıdaki tarihsel toplu denetimin kapsamına otomatik olarak dahil değildir.

## Tamamlayıcı V3 vakası — 13 Eylül 2026

Mevcut matematik kayıtlarında eşleşme, yerel anahtar kökeni ve ölçüm
anlamı için ayrı paket `vakalar/v3-eslesme/README.md` içindedir.
Kendi 14 girdili manifesti, gerçek çift dağılımı ve açıkça yapay olarak
etiketlenmiş hata denemeleri vardır. Eski B11 testleri değiştirilmez.

## Tamamlayıcı V4 vakası — 13 Eylül 2026

STAR98'in eşit bölge ağırlıklı ve toplam sayım oranlarını karşılaştıran
betimsel paket `vakalar/v4-star98/README.md` içindedir. İki açıkça yapay
tablo toplulaştırmanın bireysel ilişkiyi gizleyebildiğini gösterir. Mevcut
regresyon değiştirilmez; kaynak birimi ve yayın izni sınırlılıkları korunur.

## Toplu kontrol — 10 Eylül 2026

**17 pakette 545 Python referansı ve 278 dosya hash'i eşleşti.**
Eksik SPSS dosyaları metin yedeklerinden geri getirildi; satır sonları eski
manifestlerle eşleşecek şekilde onarıldı. B01 için yeni manifest oluşturuldu.
**R/SPSS çalışma kontrolleri henüz yapılmadı:** yorumlayıcılar bu ortamda yok.
[Yeni bütünlük kaydı](toplu-kontrol-onarim-2026-09-10.json),
[onarım işlemleri](dosya-onarim-2026-09-10.json) ve
[R/SPSS çalıştırma rehberi](RSPS_KONTROL.md).

Proje kökünden salt okunur sayısal ve dosya denetimi:

```bash
python companion/bolumler/kontrol.py
```

Eksik paket veya bütünlük farkı varsa komut `1` çıkış koduyla biter;
Python hesaplarının geçmesi bu sonucu tek başına değiştirmez.

## Bölüm bazlı yerel paketler

- [B01 — İstatistiksel araştırma süreci](bolumler/b01/README.md): Beş öğrencilik örnek; 18 Python kontrolü geçti.
- [B02 — Evren, örneklem ve veri türleri](bolumler/b02/README.md): Dört öğrencilik örnek; 23 Python kontrolü geçti.
- [B03 — Betimsel istatistik](bolumler/b03/README.md): Beş gözlem, histogram ve kutu grafiği; 26 Python kontrolü geçti.
- [B04 — Örnekleme dağılımları](bolumler/b04/README.md): 16 sıralı sonucun tam dağılımı ve grafik; 28 Python kontrolü geçti.
- [B05 — Merkezi limit teoremi ve standart hata](bolumler/b05/README.md): Yüklenen paket; 24 Python kontrolü ve 14 dosya özeti eşleşti.
- [B06 — Örnekleme yöntemleri](bolumler/b06/README.md): 12 kişilik çerçeveden basit ve tabakalı seçim; 29 Python kontrolü geçti.
- [B07 — Nokta tahmini](bolumler/b07/README.md): On ikili yanıt ve 10.000 tekrarlı oran benzetimi; 21 Python kontrolü geçti.
- [B08 — Güven aralıkları](bolumler/b08/README.md): Özet istatistiklerden yüzde 95/99 t aralıkları; 19 Python kontrolü geçti.
- [B09 — Hipotez testleri](bolumler/b09/README.md): Özet farktan çift/tek yönlü t testi ve güven aralığı; 20 Python kontrolü geçti.
- [B10 — Hata, güç ve tek örneklem t testi](bolumler/b10/README.md): Ayrı test özeti ve ileriye dönük güç planı; 30 Python kontrolü geçti.
- [B11 — Bağımsız ve eşleştirilmiş t testleri](bolumler/b11/README.md): İki ayrı özetten Welch ve eşleştirilmiş test; 34 Python kontrolü geçti.
- [B12 — Kategorik veriler ve ki-kare testi](bolumler/b12/README.md): 80 gözlemin 2×2 frekans tablosu, satır yüzdeleri ve Pearson artıkları; 32 Python kontrolü geçti.
- [B13 — Korelasyon ve basit regresyon](bolumler/b13/README.md): 16 gözlem, katsayı ve öngörü aralıkları, tanı grafikleri; 62 Python kontrolü geçti.
- [B14 — Genel sınava hazırlık](bolumler/b14/README.md): 24 çiftin son−ön özeti, yöntem seçimi ve karma alıştırmalar; 17 Python kontrolü geçti.
- [Bootstrap ve rastgeleleştirme — kapsamlı sürüm Bölüm 9](bolumler/bootstrap/README.md): 3.125 yeniden örneklem ve 20 etiket ataması; 26 Python kontrolü geçti.
- [Çoklu doğrusal regresyon — kapsamlı sürüm Bölüm 15](bolumler/coklu-regresyon/README.md): 12 yapay gözlem, VIF ve iki tür öngörü aralığı; 66 Python kontrolü geçti.
- [ANOVA — kapsamlı sürüm Bölüm 16](bolumler/anova/README.md): Grup özetlerinden klasik ANOVA, Tukey ve Welch; 70 Python kontrolü geçti.

Paketlerde ortak CSV, veri sözlüğü, R/Python/SPSS kodları, kontrol değerleri
ve yanıtlı alıştırmalar bulunur. Küçük yapay veriler aşağıdaki gerçek veri
paketlerinden ayrıdır. R ve SPSS çalıştırma kontrolleri bekliyor; her bölümün
`DOGRULAMA.md` kaydı yapılan ve yapılmayan kontrolleri ayırır.

[Tüm bölüm paketlerinin durumu](bolumler/README.md).
GitHub yüklemesi bütün bölümler tamamlandıktan sonra yapılacak. Önceden
hazırlanan B01 ZIP'leri ve yükleme taslakları yalnız B01'i kapsar; nihai toplu
paket değildir. B02–B04, B06–B14, çoklu regresyon ve ANOVA için ayrı bir yükleme veya ZIP hazırlanmadı.

## Klasörler

- `data/raw/`: Kaynaktan alındığı biçimiyle salt okunur veriler.
- `data/clean/`: Kitapta kullanılacak, açık adlandırılmış ve doğrulanmış veriler.
- `data/dictionaries/`: Veri sözlükleri, kaynak kataloğu ve bölüm eşleştirmesi.
- `code/`: Veriyi hazırlayan, doğrulayan ve örnek analizleri üreten betikler.
- `outputs/tables/`: Kodla üretilen sayısal çıktı tabloları.
- `outputs/figures/`: Kodla üretilen grafikler.

## Hızlı başlangıç

Proje kökünden şu komutlar çalıştırılır:

```bash
python companion/code/00_prepare_data.py
python companion/code/01_validate_data.py
python companion/code/02_chapter_examples.py
python companion/code/03_make_figures.py
python companion/code/05_resampling_examples.py
python companion/code/06_multiple_regression.py
python companion/code/04_record_environment.py
```

Tüm süreci tek komutla çalıştırmak için:

```bash
python companion/code/run_all.py
```

## Paketteki gerçek veriler

### STAR98 eğitim bölgeleri

California'daki 303 birleşik okul bölgesinin 1998 standartlaştırılmış
matematik sınavı sonuçları ile sosyoekonomik ve okul özelliklerini içerir.
Gözlem birimi öğrenciler değil okul bölgeleridir.

### Spector program etkililiği

32 öğrenci için not ortalaması, ekonomi testi puanı, programa katılım ve not
iyileşmesi değişkenlerini içerir. Küçük örneklem, koşul kontrolü ve kesin test
tartışmaları için özellikle uygundur.

Bu iki veri seti `statsmodels` dağıtımı içinden alınır. Özgün veri sahipleri
haklarını saklı tuttuğundan paket geliştirme ve öğretim amaçlı yerel kullanım
için hazırlanmıştır. Kamuya açık kitap ekinde yeniden dağıtılmadan önce izin
durumu yeniden doğrulanmalıdır. Açık lisanslı yayın adayları
`data/dictionaries/source_catalog.csv` dosyasında ayrıca listelenmiştir.

## Yeniden üretilebilirlik kuralları

- Betikler proje kökünden veya başka bir dizinden çalıştırılabilir.
- Rastgele örnekleme kullanılan her yerde tohum `2026` olarak kaydedilir.
- Ondalık yuvarlama yalnız çıktı üretiminde yapılır; analiz ara değerleri tam
  duyarlıkla korunur.
- Betikler mevcut dosyaları sessizce elle değiştirmez; temiz veri her zaman
  ham veriden yeniden oluşturulur.
- `01_validate_data.py` başarısız olursa sonraki analizler kullanılmamalıdır.
- `environment.txt` kullanılan yazılım sürümlerini, `manifest_sha256.csv` ise
  veri ve çıktı dosyalarının bütünlük özetlerini kaydeder.

## Yayına hazırlık

Yayımlanacak eşlikçi pakette şu dosyalar ayrıca tamamlanmalıdır:

- kalıcı depo adresi ve DOI,
- açık lisans metinleri,
- sürüm etiketi ve değişiklik günlüğü,
- kitap baskısı ile veri paketi sürümünün eşleştirilmesi,
- erişilebilir grafik açıklamaları,
- R ve SPSS eşdeğer betiklerinin gerçek yorumlayıcılarda doğrulanması.

## Bootstrap aktarımı

[Bootstrap ZIP](bootstrap-uygulama-paketi.zip) yalnız bootstrap paketini içerir.
ZIP görünmezse [tek dosyalık metin aktarıcı](bootstrap-aktar.py.txt) indirilip
`python bootstrap-aktar.py.txt` ile çalıştırılabilir; yeni `bootstrap-aktarim`
klasörünü oluşturur, mevcut hedefe yazmaz. Aktarıcı ve açılan paketin 26
kontrolü geçici klasörde sınandı. Bu, Prism dosya panelinde görünürlüğün veya
kullanıcının bilgisayarına aktarımın doğrulandığı anlamına gelmez. GitHub'a
yükleme yapılmadı; bu dosyalar nihai toplu yayın değildir.

## Bilgisayarınızda toplu R testi

```bash
python companion/bolumler/r_kontrol.py --rapor companion/r-sonuc-bilgisayar.json
```

Rscript kurulu ve erişilebilir olmalıdır. Script sürümleri, çıktıları ve
değiştirilmiş referansı reddetme kontrolünü yeni JSON raporuna kaydeder.
SPSS için [adımlar ve kayıt formu](RSPS_KONTROL.md) kullanılır.

### Windows R Console seçeneği

Python kullanmadan [R toplu kontrol betiğini](r-toplu-kontrol.R.txt) indirin.
R Console'da `source(file.choose(), encoding="UTF-8")` komutuyla bu dosyayı
seçin; ikinci pencerede `b01/ornek-01/cozum.R` dosyasını gösterin.
[İşleyiş ve rapor açıklaması](RSPS_KONTROL.md) rehberdedir. B01 dahil 17
paket yeniden sınanır; gerçek sonuçlar Windows'taki çalıştırma sonrasında
oluşur. Betik bu ortamda R ile çalıştırılmadı.
### SPSS: bütün bölümleri birlikte çalıştırma

[R ile SPSS hazırlayıcısı](spss-toplu-hazirla.R.txt), bölüm komutlarını tek
SPSS betiğinde birleştirir; `INSERT` dosya erişimine bağımlı değildir.
Girdileri ayrı klasöre kopyalar; analizleri R değil SPSS çalıştırır.
[Bölüm bölüm PDF/SPV kaydetme ve inceleme adımları](SPSS_TOPLU_KONTROL.md).
Hazırlayıcı ve birleşik SPSS akışı bu ortamda yorumlayıcılarında çalıştırılmadı.

## Proje ZIP birleştirmesi — 12 Eylül 2026

Arşivdeki B01–B14 ortak gerçek veri SPSS/R/Python uygulamaları kitaba
aktarıldı. Mevcut bölüm paketleri ve ayrı R alıştırmaları korunmuştur.
B01 Windows pilot yönergesi `spss/PILOT-B01-WINDOWS.md` dosyasındadır.
Bu aktarım SPSS/R çalışma zamanı doğrulaması veya GitHub yüklemesi değildir.
Ayrıntılı kapsam ve derleme kaydı `docs/denetim/PROJE-KONTROLU.md` dosyasındadır.