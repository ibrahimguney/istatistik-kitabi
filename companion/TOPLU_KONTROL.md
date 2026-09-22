# Toplu kontrol — 10 Eylül 2026

## Son güncelleme — dosya onarımı sonrası

[Onarım sonrası kayıt](toplu-kontrol-onarim-2026-09-10.json): 17 paket,
545 Python referansı, 278 eşleşen hash; yerel dosya/sayısal denetimi geçti.
Bu kopyada 16 eksik SPSS dosyası ve 222 satır sonu farkı giderildi. Mevcut
manifestler korunurken B01 için yeni bir bütünlük başlangıcı oluşturuldu.
[Önce/sonra kayıtları](dosya-onarim-2026-09-10.json) ayrı tutuldu.

R/SPSS çalışma testi yapılmadı. [R raporu](r-kontrol-2026-09-10.json) bütün
paketleri çalıştırılmadı olarak kaydeder. Gerçek bilgisayar testleri için
[rehber](RSPS_KONTROL.md) hazırlandı. GitHub'a yükleme yapılmadı.

Aşağıdaki bölümler önceki denetimlerin tarihsel kayıtlarıdır.

## Güncelleme — B05 yüklemesi ve bootstrap sonrası

10 Eylül 2026 tarihli [yeni kayıt](toplu-kontrol-bootstrap-2026-09-10.json):
17 paket mevcut, 545 Python referansı geçti. B05'in 14 ve bootstrap'ın 19
manifest girdisi byte düzeyinde eşleşti. B05 manifestindeki Windows yolları
denetleyicide taşınabilir biçime çevrilerek okundu; dosyalar değiştirilmedi.
Bootstrap metin aktarıcısı ayrı klasörde açıldı, 19 hash ve 26 sayısal kontrol
tekrar geçti; mevcut hedefe yazma reddedildi.

Toplu denetim hâlâ `1` ile biter: diğer 15 paketin `.sps` dosyaları eksik,
B01 manifesti yok; eski manifestlerde 201 son-LF ve 4 CRLF/son-satır farkı var.
Manifestlerdeki 14 eksik girdiye ek olarak B01'in `.sps` dosyası da eksiktir.
R/SPSS çalıştırılmadı. GitHub yayını yapılmadı.

## Önceki denetim (tarihsel kayıt)

Aşağıdaki 15 paket / 495 değer bilgisi önceki çalışma kopyasına aittir;
yeni yükleme ve bootstrap hazırlığından sonraki durum değildir.

**Sonuç: Mevcut paketlerin Python sayısal kontrolleri geçti; eksiksiz toplu
GitHub yayınına henüz hazır değiliz.** Bu denetimde yükleme yapılmadı.

## Kapsam ve kanıt

Ders sürümünün 14 paketi ile bootstrap, çoklu regresyon ve ANOVA olmak üzere
17 paket beklendi; 15 paket klasörü bulundu. Denetim bu çalışma kopyasının
anlık durumunu gösterir; önceki konuşmalardaki dosyaların korunduğunu varsaymaz.

- [Ana denetim kaydı](toplu-kontrol-2026-09-10.json): Paket envanteri, Python
  komutlarının tam çıktıları, çıkış kodları, sürümler, AST ve dosya bazında SHA-256 sonuçları.
- [Ek sınamalar](toplu-kontrol-ek-sinamalar-2026-09-10.json): Bağımsız klasörde
  çalıştırma, değiştirilmiş referansı reddetme, PNG okuma ve yerel bağlantı kontrolleri.
- [Yeniden çalıştırılabilir denetleyici](bolumler/kontrol.py): Paketlerin
  mevcut `cozum.py --check` komutlarını çalıştırır; veriyi, kodu ve manifesti değiştirmez.

## Sayısal sonuçlar

| Paket | Eşleşen referans değeri | Python sonucu |
|---|---:|---|
| B01 | 18 | Geçti |
| B02 | 23 | Geçti |
| B03 | 26 | Geçti |
| B04 | 28 | Geçti |
| B05 | — | Paket klasörü eksik |
| B06 | 29 | Geçti |
| B07 | 21 | Geçti |
| B08 | 19 | Geçti |
| B09 | 20 | Geçti |
| B10 | 30 | Geçti |
| B11 | 34 | Geçti |
| B12 | 32 | Geçti |
| B13 | 62 | Geçti |
| B14 | 17 | Geçti |
| Bootstrap | — | Paket klasörü eksik |
| Çoklu regresyon | 66 | Geçti |
| ANOVA | 70 | Geçti |
| **Toplam** | **495** | **15 mevcut paketin tamamı geçti** |

495 sayısı eşleşen referans değerlerinin toplamıdır; bağımsız test senaryosu
sayısı veya bütün bilimsel yorumların doğruluğunun kanıtı değildir. Her paket
kendi mevcut toleranslarını kullandı; beklenen değerler yeniden üretilmedi.

Ek olarak:

- 15 örneğin tamamı, kitap dizininden bağımsız geçici klasörlere kopyalanıp
  `--check` ile tekrar çalıştırıldı; hepsi geçti.
- Her kopyada beklenen sonuç CSV'sinin ilk `deger` hücresi 1 artırıldı;
  15 komutun tamamı sıfır olmayan çıkış koduyla bu değişikliği reddetti.
  Bu sınama yalnız bu referans değişikliğini kapsar; tüm hatalı girdileri kapsamaz.
- Mevcut paketlerdeki 19 Python dosyası AST ayrıştırmasından geçti.
  Yardımcı üretim betikleri bu sırada çalıştırılmadı.
- 13 PNG, Pillow ile açılıp dosya yapısı doğrulandı. Bu bir görsel/pedagojik
  inceleme değildir; grafikler yeniden üretilmedi.
- Paketlerin Markdown dosyalarında taranan doğrudan yerel bağlantılarda eksik
  hedef bulunmadı. Kod bloklarındaki dosya adları ve çevrim içi adresler bu
  bağlantı sınamasının kapsamına alınmadı; `.sps` eksikleri ayrı dosya
  envanterinden saptandı.
- Denetleyicinin hash sınıflandırması beş küçük senaryoyla sınandı:
  tam eşleşme, eksik son LF, CRLF ve son satır farkı, içerik farkı, eksik dosya.
- Ek sınamalar öncesi ve sonrası hash envanteri karşılaştırıldı; mevcut
  paket dosyalarında değişiklik veya yeni dosya oluşumu saptanmadı.

## Dosya bütünlüğü

B01 için `MANIFEST.json` veya eski `MANIFEST.sha256` dosyası bulunamadı;
B01'in geçmiş dağıtım bütünlüğü doğrulanamadı. Diğer 14 JSON manifestindeki
232 dosya girdisi şu şekilde sınıflandı:

| Durum | Girdi sayısı |
|---|---:|
| SHA-256 tam eşleşmesi (13 PNG) | 13 |
| Dosyanın sonuna tek LF eklenince eski hash eşleşiyor | 201 |
| CRLF ve son satır düzeni geri getirildiğinde eski hash eşleşiyor | 4 |
| Manifestte kayıtlı ama bulunmayan `.sps` | 14 |
| Bu dönüşümlerle açıklanamayan içerik farkı | 0 |

Bu dönüşümler yalnız bellekte denenmiştir; dosyalar düzeltilmedi, eski
manifestler yeni hashlerle değiştirilmedi. Satır sonu farkı açıklanabilse
bile mevcut dosyalar **byte düzeyinde eski manifestleri geçmiyor**.
Bulgular aktarım/satır sonu değişikliğiyle uyumludur; değişikliğin ne zaman
ve hangi araçla gerçekleştiği bu denetimden belirlenemez.

B01 dahil **15 paketin tamamında `analiz.sps` eksik**, `analiz.sps.txt`
yedeği ise mevcut. Manifestli 14 pakette yedeğin sonuna LF eklendiğinde,
manifestteki `.sps` hash'iyle eşleşiyor. B01 için böyle bir geçmiş hash
karşılaştırması yapılamıyor. Manifestli paketlerde ayrıca listelenmemiş
başka dağıtım dosyası bulunmadı.

## Çalıştırılmayanlar ve sınırlar

- `Rscript`, `spss` ve `pspp` çalıştırılabilirleri PATH üzerinde bulunmadı.
  R ve SPSS betikleri çalıştırılmadı; üç yazılımda uçtan uca eşitlik onayı yok.
  PATH kontrolü bilgisayarın her yerinde yazılım bulunmadığını kanıtlamaz.
- Kaynak kayıtlarındaki kitap/veri hash'leri ayrıca yeniden doğrulanmadı;
  örneklerin LaTeX metniyle içerik eşleştirmesi yeniden yapılmadı.
- Önceki `DOGRULAMA.md` dosyalarındaki ayrıntılı senaryoların tamamı yeniden
  çalıştırılmadı. Tarihsel kayıtlar değiştirilmedi.
- Eski gerçek veri hattı (`companion/code/run_all.py`), veri izinleri,
  LaTeX/PDF derlemesi, B01'e özel eski ZIP/yükleme taslakları ve uzak GitHub
  deposu denetlenmedi. Bu çalışma bölüm bazlı yerel paketlerle sınırlıdır.

Kullanılan sürümler: Python 3.13.15, NumPy 2.4.1, pandas 2.3.3,
SciPy 1.17.0, Matplotlib 3.10.8, statsmodels 0.14.6.

## Tekrar çalıştırma

Proje kökünde:

```bash
python companion/bolumler/kontrol.py
```

Yeni tarihli/isimli bir JSON raporu kaydetmek için:

```bash
python companion/bolumler/kontrol.py --rapor companion/toplu-kontrol-yeni.json
```

Rapor yolu göreli olmalı; mevcut raporun üzerine yazılmaz. Denetleyici eksik
paket, başarısız Python kontrolü, eksik dosya/manifest veya hash farkında
`1` çıkış kodu döndürür. Bu çalıştırmada alınan `1`, Python hesaplarının
başarısızlığından değil paket ve bütünlük eksiklerinden kaynaklandı.
`0` sonucu da R/SPSS doğrulaması veya yayın izni yerine geçmez.

Denetleyici ana kayıttaki kontrolleri tekrarlar. Bağımsız kopya/negatif
sınamalar, PNG okuma ve Markdown bağlantı taraması bu sefer ayrıca yürütüldü;
`kontrol.py` bunları otomatik tekrar etmez.

## Yayın öncesi sıra

1. B05 ve bootstrap klasörlerini geri getirin veya yeniden hazırlayın;
   bu paketlerin sayısal kontrollerini çalıştırın.
2. SPSS dosyalarını metin yedeklerinden geri oluşturun. Manifestli 14 pakette
   mevcut hash kanıtını kullanın; B01'i ayrıca inceleyin.
3. Satır sonu politikasını belirleyip kanıtlanan farkları giderin. B01 için
   inceleme sonrasında yeni bir manifest hazırlayın. Eski manifestlerin
   yalnızca yeniden hesaplanması geçmiş bütünlüğün kanıtı sayılmaz.
4. R/SPSS çalışma kontrollerini uygun ortamlarda tamamlayıp gerçek sonuçları
   kaydedin; tamamlanamazsa yayını açıkça ön sürüm ve kısmi doğrulama olarak etiketleyin.
5. Toplu denetimi yeniden çalıştırın; kullanım koşulları ve sürüm bilgilerini
   kesinleştirdikten sonra nihai dağıtım paketini hazırlayın.

Bu denetimde ZIP oluşturulmadı, lisans atanmadı ve GitHub'a yükleme yapılmadı.