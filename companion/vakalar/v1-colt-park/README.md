# V1 — Colt Park bloklu deney öğretim paketi

13 Eylül 2026. Bağımsız ek pakettir; eski `companion` ve SPSS manifestlerini
değiştirmez. Kitapta ana B11 ve kapsamlı yeniden örnekleme bölümünde kullanılır.

## Kaynak ve atıf

Villa-Galaviz, E., Smart, S. M., Ward, S. E., Fraser, M. D. ve Memmott, J.
(2023). *Fertilization using manure minimizes the trade-offs between
biodiversity and forage production in agri-environment scheme grasslands*.
PLOS ONE 18(10), e0290843. `https://doi.org/10.1371/journal.pone.0290843`

- Veri: S1 Data, `https://doi.org/10.1371/journal.pone.0290843.s001`.
- Yöntem: S1 File, `https://doi.org/10.1371/journal.pone.0290843.s002`.
- Kaynak yayın © 2023 Villa-Galaviz ve arkadaşları; Creative Commons
  Attribution kapsamında. PLOS'un CC BY 4.0 kullanım açıklaması ve lisans
  koşulları için `https://creativecommons.org/licenses/by/4.0/` kaydedilmiştir.
  Eklerde ayrıca bir hak kısıtlaması görülmedi. Kaynak yazarları bu öğretim
  uyarlamasını onaylamış gibi sunulamaz; kaynak atfı ve lisans kaydı korunmalıdır.
- Uyarlama: İbrahim Güney istatistik kitabı için dört değişkenlik aktarım,
  tek yanıt ve iki rejim seçimi, tam atama sayımı, tamamlayıcı blok modeli.
  Bu işlemler özgün araştırmanın tüm analizlerinin yeniden üretimi değildir.

## Ham dosyalar ve köken

`raw/s1-data.xlsx`, kullanıcının `prism-uploads/S1 Data_2.xlsx` yüklemesinin;
`raw/s1-methods.pdf`, `prism-uploads/S1_2.pdf` yüklemesinin değişmemiş
kopyasıdır. `prism-uploads/S1_2.xlsx` ilk Excel ile bayt düzeyinde aynıdır;
R kodu değildir. İki kopya birleştirilmedi. Kaynak web sunucusundan bağımsız
yeniden indirme yapılamadığından hash, sunucuyla eşitlik değil alınan
yüklemenin sabitlenmesi anlamına gelir.

XLSX SHA-256: `ebe2ec9480ba8498585a1b8527ab92ad0db1b4bbb2f85ba27a2e61b705412e10`.
PDF'nin özeti `manifest.csv` içindedir. PDF okuyucusu bazı nesne işaretçileri
için onarım uyarısı verdi; yöntem sayfası ve atama şekli metin/görüntü olarak
okundu, özgün PDF yeniden yazılmadı.

## Veri kabulü ve kapsam

Excel sayfaları README, DATA ve boş Sheet1'dir. DATA 24 × 14'tür; boş hücre
yoktur. Blok × rejim sayımları her hücrede 2'dir. Yöntem ekinin 2. sayfası
ve 3. sayfadaki atama şekli bu yapıyla eşleşir. Ana makalenin blok içi
parsel sayısını anlatan cümlesi yerine ayrıntılı ek ve çapraz sayımlar
esas alınmıştır. Ana makale/ekte başlangıç yılı ve tohum dönemleri de
aynı biçimde verilmediğinden kesin kuruluş yılı bu vakada kullanılmaz.

`data.csv` bütün 24 satırı, `comparison.csv` yalnız FYM ve kontrolün 12
satırını içerir. Dört sütun `dictionary.csv` ile açıklanır. Fiziksel parsel
kimliği, yıllık ham ölçümler ve saha atama tutanağı verilmediğinden bunlar
doğrulanmış sayılmaz. DATA satırlarına bir saha numarası uydurulmadı.
Ölçüm birimi, Excel README'deki m2 ile PDF s. 2'deki gram açıklaması
birlikte okunarak g/m2 olarak tanımlandı; hektara veya toplam parsel
ağırlığına dönüşüm yapılmadı. Yıllar bağımsız tekrar sayılmadı.

## Çalıştırma

Proje kökünde:

```sh
python -B companion/vakalar/v1-colt-park/analyze.py
```

Python, NumPy, pandas, SciPy ve matplotlib kullanılır. Ortamda openpyxl
olmadığından XLSX bu sabit kaynak için standart kütüphanenin ZIP/XML
okuyucusuyla açılır; formül çalıştırılmaz. Kaynak hash'i değişirse betik
durur. Bu okuyucu genel amaçlı Excel içe aktarma aracı değildir.

Betik CSV'leri, `results.json`, `comparison.png` ve ayrı `manifest.csv`
envanterini yeniden üretir. Ham dosyalara dokunmaz. Manifest güncel çıktı
envanteridir; bilinmeyen veri değişikliğini onaylayan eski referans değildir.

## Analiz ve sınırlar

Blok başına iki FYM ve iki kontrol korunarak 6 × 6 × 6 = 216 atamanın
tamamı sayılır; NPK ve NPK+FYM yerleri koşullamada sabit tutulur. Testin
keskin sıfırı seçilen rejimlerin her ilgili parselde aynı yanıtı vermesidir.
İstatistik üç blok ortalama farkının eşit ağırlıklı ortalamasıdır.
Mutlak değer bakımından en az gözlenen kadar uç atamalar sayılır;
yuvarlama eşitlikleri için 1e-10 tolerans vardır. Tam sayımda +1 düzeltmesi
ve rastgele tohum kullanılmaz. Bu sayı, eş olasılıklı blok içi atamanın
koşullu dağılımıdır; parsellerin yerleri bloklar arasında değiştirilmez.

Fark 171,4875107167 g/m2; tam iki yönlü p = 2/216'dır. Ek güven aralığı
`Y = sabit + FYM + blok_TWO + blok_THREE + hata` modelinin klasik t
aralığıdır: df = 8, %95 GA [106,546115; 236,428906] g/m2. Ortak eklemeli
etki, bağımsız normal hatalar ve sabit hata varyansı varsayar. Tam testin
tersine çevrilmiş aralığı veya varsayımsız belirsizlik ölçüsü değildir.
Rastgele atama normal hata varsayımını doğrulamaz.

Özgün R eki yüklenmedi/çalıştırılmadı. Bu dar Python uygulaması, özgün
R sonuçlarının ya da çok göstergeli optimum rejim iddiasının doğrulaması
değildir. SPSS uygulaması eklenmedi. Rastgele atama bu deney içindeki
karşılaştırmayı destekler; parseller arası etkileşimsizlik, uygulama ve
izlem koşulları önemlidir. Saha tüm çayırların olasılıklı örneklemi olarak
belgelenmediğinden geniş evren genellemesi yapılmaz.