# V3 — Eşleşme, anahtar kökeni ve ölçümlerin anlamı

13 Eylül 2026. B11'e eklenen tamamlayıcı vakadır; yeni saha verisi veya
bağımsız tekrar araştırması değildir. Eski B11 analizleri ve veri paketleri
değiştirilmez. Amaç t testini tekrar etmek değil, çiftlerin doğru
kurulmasını, hata denetimini ve ölçümlerin yorum sınırını öğretmektir.

## Kaynak ve izlenebilirlik

Cortez, P. (2008), *Student Performance*, UCI, DOI 10.24432/C5TG7T.
Kaynak sayfası: `https://archive.ics.uci.edu/dataset/320/student+performance`
(erişim: 13 Eylül 2026). Sayfa CC BY 4.0 kaydı taşır. Veri atfı korunur;
bu paket mevcut matematik verisinden türetilmiş bir öğretim uyarlamasıdır,
kaynak sahibinin onayı gibi sunulmaz. G1 ilk dönem, G3 yıl sonu notudur;
eşdeğer sınav veya rastgele müdahale protokolü varsayılmaz.

`raw/student-mat.csv`, `companion/spss/raw/student-mat.csv` dosyasının
değişmemiş kopyasıdır; 395 × 33'tür. SHA-256:
`041d88ddca1da9fb8a1a9261bbf090d2f7c75625c228392e1077c2cf656051e8`.
`raw/b11.csv` yerel B11 dosyasının, `raw/b14-summary.csv` ayrı küçük
B14 örneğinin değişmemiş kopyalarıdır. Kaynak sunucusuyla yeni bir bayt
karşılaştırması iddia edilmez; kaynak/yerel sürüm sabitlenir.

`id`, B11 üreticisinin dosya sırasından oluşturduğu yerel anahtardır.
G1 ve G3'e bölmeden önce korunmuştur. `source_line=id+1`, başlık dahil
matematik CSV'sindeki satırı gösterir. Bu numaralar gerçek öğrenci kimliği
veya matematik–Portekizce birleştirme anahtarı değildir. Teknik eşleşme,
saha kayıtlarının bağımsız kimlik denetimi değildir.

## Yeniden üretim

Proje kökünde kurulu pandas/numpy/scipy/matplotlib ile:

```sh
python -B companion/vakalar/v3-eslesme/analyze.py
python -B companion/vakalar/v3-eslesme/verify.py
```

İlk komut türetilmiş CSV/JSON ve grafiği yeniler; ham dosyaları veya
manifesti değiştirmez. İkincisi kaynak çiftlerini ayrı standart-kütüphane
CSV okuyucusu ve anahtar sözlükleriyle karşılaştırır; mevcut B11 t ve
aralık değerleriyle uyumu kontrol eder. Bu kontrol yeni test sonucu
olarak sunulmaz. R/SPSS yeniden çalıştırılmamıştır.

Dosyalar:

- `g1.csv`, `g3-reversed.csv`: anahtar korunmuş iki ölçüm tablosu; ikincisi
  kasıtlı ters sırada, fakat notları değiştirilmemiştir.
- `paired.csv`: denetlenmiş 395 çift, kaynak satırı ve G3−G1 farkı.
- `difference-counts.csv`, `differences.png`: yalnız doğru çiftlerin dağılımı.
- `results.json`: gerçek betimleme ve açıkça geçersiz olarak etiketlenmiş
  sıra hatası gösterimi; yanlış çiftlerden p veya aralık hesaplanmaz.
- `teaching-scenarios.json`: özgün ve ters sıralı doğru tablolar yanında
  dört ayrı yapay hata denemesinin teknik kabul/ret kayıtları.
- `dictionary.csv`, `manifest.csv`: değişken tanımları ve 14 dosyanın özeti.

## Kabul kapıları ve yapay denemeler

Boş/geçersiz/çoğul anahtarlar birleştirmeden önce denetlenir. Dış
birleştirme eşleşmeyenleri korur; iki tarafta anahtarı olup notu eksik
olanlar ayrıca sayılır. `audit_pairing` içindeki `accepted`, yalnız
bu teknik kontrollerden geçiştir; kimliğin kökenini kanıtlamaz.
Kaynakla karşılaştırma ayrı kapıdır. Yeniden numaralandırılmış yanlış
anahtarların teknik kontrolden geçebileceği ayrıca test edilir.

| Bellekte yapılan öğretim müdahalesi | Beklenen denetim |
| --- | --- |
| G3'te id=1 satırını kaldırma | 394 anahtar eşleşmesi, 394 tam çift; G1'de karşılıksız id=1 |
| G3'te id=1 satırını yineleme | Çoğul anahtar; birleşim ve analiz reddedilir |
| G3'te id=1 notunu boş bırakma | 395 anahtar eşleşmesi, 394 tam çift |
| Yalnız G3'e id=1001 ekleme | Karşılıksız G3 anahtarı; analiz reddedilir |

Bu dört müdahale yalnız ayrı bellek kopyalarında uygulanır; gerçek
kayıtlarda bu hatalar bulunduğu iddia edilmez. Hiçbir satır otomatik
olarak silinmez, not doldurulmaz veya yinelenen kaydın ilki seçilmez.
Eksik çiftle analiz kararı verilmesi gerekiyorsa yeni kayıt kapsamı,
gerekçe ve sınırlılıklar ayrıca tanımlanmalıdır; bu paket bunu yapmaz.

Gerçek çiftlerde ortalama −0,493670886076, SS 2,762481677462; negatif,
sıfır ve pozitif farklar sırasıyla 159, 93, 143'tür. G3=0 olan 38 kayıt
geçerli kabul edilmiştir. Hatalı sıraya göre 394 ortak değişse de ortalama
aynı kalır; yanlış farkların SS'si 5,337049456065 olur. Bu, kullanılabilir
alternatif sonuç değil, eşleşme hatasının gösterimidir.

Küçük B14 dosyasındaki 24 çiftin özeti ayrı öğretim girdisidir. Ham
kimlik, eksik eş veya fark dağılımı bu özetten yeniden kurulmaz. Küçük
örnek bu 395 kayda eklenmez veya ondan üretilmiş gibi gösterilmez.

Teknik belge: `https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html`.
Özellikle boş anahtarların eşleşebilmesi nedeniyle boşluk kontrolü
birleştirmeden önce yapılır. `outer`, `indicator`, `validate="one_to_one"`
seçenekleri birlikte kullanılır. Sayısal kontroller `1e-12` bağıl toleransla;
B11'in altı basamaklı çıktıları `5e-7` mutlak toleransla karşılaştırılır.
Grafik baytları yazılım sürümü değişince farklılaşabilir; sayısal eşitlik
ile manifest eşitliğini ayırın, farkı incelemeden manifesti yenilemeyin.