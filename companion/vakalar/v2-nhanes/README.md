# V2 — NHANES sayısal öğretim paketi

Teslim 03, 13 Eylül 2026. Bu paket, korunması kontrol edilen üç küçük
Python dosyasının devamıdır. Girdi mevcut `prism-uploads/DEMO_J.zip`;
yeni ham veya kişi düzeyi CSV kopyası oluşturulmaz. Bu ZIP paket için
zorunlu dış girdidir; yalnız bu klasörü kopyalamak çalıştırmaya yetmez.
Kaynak ve kullanım kaydı `source.json`, sözlük `dictionary.csv` içindedir.
İstatistiksel toplu analiz yapılır; kişileri tanımlama veya kimlikli
verilerle birleştirme yoktur. Bu not hukuki uygunluk onayı değildir.

## Analiz tanımı

2017–2018 ABD kurum dışı sivil nüfusunun 20+ alt evreninde 60+ oranı.
WTINT2YR görüşme ağırlığı; SDMVSTRA/SDMVPSU maskelenmiş varyans birimleri.
Kaynak 9254 × 46; seçili alanlarda eksik veya uygunsuz kod varsa durulur.
Diğer alanlardaki eksikler nedeniyle bütün dosyada tam kayıt seçilmez.
357 sıfır yaş kodunun çok küçük okuyucu artığı 1e-10 tamsayı toleransıyla
bellekte normalleştirilir. Ham baytlar değişmez. 80 kodu 80 ve üzeridir.

Pay A=sum(w*d*y), payda B=sum(w*d), oran p=A/B. Kişi katkısı
z=w*d*(y-p)/B; PSU toplamları Z_hj. Taylor varyansı
sum_h[m_h/(m_h-1)*sum_j(Z_hj-mean_j Z_hj)^2] olarak hesaplanır.
Çocuklar silinmez; alt evren katkıları sıfırdır. Sonlu evren düzeltmesi
yoktur. Burada bütün 15 tabaka/30 PSU alt evrene katkı verir, df=15.
%95 aralık p ± t(0.975,df)*SE; yaklaşık t-Wald öğretim aralığıdır.
NCHS'nin bütün oran yayımlama koşullarını karşılama veya resmî bir CDC
tahminini aynen yeniden üretme iddiası yoktur. Aralık kapsam/yanıtsızlık
yanlılığını ölçmez; bugünkü veya Türkiye nüfusuna doğrudan genellenmez.

## Dosyalar ve tekrar çalıştırma

Proje kökünde:

```sh
python -B companion/vakalar/v2-nhanes/check_source.py
python -B companion/vakalar/v2-nhanes/analyze.py
python -B companion/vakalar/v2-nhanes/verify.py
python -B companion/vakalar/v2-nhanes/export.py
python -B companion/vakalar/v2-nhanes/verify_delivery.py
```

İlk üç komut yalnız ekrana yazar. Üretici `results.json`, 30 satırlık
`psu.csv` ve kitap makroları `values.tex` dosyalarını yazar; manifesti
değiştirmez. Ayrı klasöre üretim için `--output-dir` seçeneği vardır.
Manifest diğer 11 paket dosyasının SHA-256/boyut referansıdır; dış ZIP
hash'i kaynak kontrolünde ayrıca doğrulanır. Beklenmeyen hash farkında
manifest yenilenmemeli; yalnız son LF farkı varsa bile ayrı kaydedilmelidir.

`verify.py` bağımsız pay/payda kovaryans hesabını; `verify_delivery.py`
manifesti, kaydedilen çıktıların yeniden üretimini, kaynak/PSU sayımlarını
ve kitap bağlantılarını kontrol eder. XPT okuyucusu ve t kritik değeri
ortaktır; R/SPSS veya R survey çalıştırılması değildir. Yapay bozuk
girdiler yalnız bellekte sınanır. Kontrol kodları dosyaları değiştirmez.

Sonuç JSON'undaki `complete_delivery_accepted: false` önceki hesap
fonksiyonunun kapsam sınırıdır; o fonksiyon tek başına dosya/kitap
teslimini onaylamaz. Bu teslimin yerel teknik sonucu ayrı teslim
denetleyicisindedir. Yeni dosyaların oturumlar arası kalıcılığı, öğrenci
pilotu ve dört vakanın birlikte kabulü bununla doğrulanmış sayılmaz.
Kayıt: `V2-KUCUK-TESLIM-03.md`.