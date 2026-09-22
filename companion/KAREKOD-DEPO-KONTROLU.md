# Yeni depo ve bölüm sonu karekodları — 11 Eylül 2026

## Sonuç ve kapsam

`ibrahimguney/istatistik` deposunun `main` dalındaki `bolumler` dizini,
B01–B14 ile bootstrap, çoklu regresyon ve ANOVA olmak üzere 17 paket
klasörünü listeliyor. Bölüm sonu bağlantıları bu yapıya göre eklendi.
Bu, nihai yayın veya bütün dosyaların doğruluğu için onay değildir.

Web üzerinden dizin yapısı ve örnek paket sayfaları incelendi; deponun
bütün dosyaları indirilerek Python/R/SPSS ve SHA-256 denetimi yeniden
çalıştırılmadı. README'deki eski test sayıları yeni bir çalıştırmanın
sonucu olarak kabul edilmedi. GitHub üzerinde dosya değişikliği yapılmadı.

## Yayındaki eksikler

- B01 `ornek-01` dizininde `analiz.sps.txt` var, `analiz.sps` görünmüyor.
  README ise `analiz.sps` açılmasını istiyor. Özgün komut dosyası tamamlanıp
  manifestle karşılaştırılmalı. Diğer paketlerin bütün dosyaları için de
  indirilmiş depo kopyasında toplu bütünlük denetimi yapılmalı.
- Bölümler README'sinde eski `istatistik-uygulamalari` hedefi ve henüz
  yükleme yapılmadığı ifadeleri kalmış. Yeni depo adı ve ön yayın durumu
  yazılmalı. GitHub kökünde `companion` klasörü yok; GitHub için yönergeler
  `bolumler/b01/ornek-01` gibi yollar kullanmalı. Kitap projesindeki yerel
  `companion/bolumler/...` yolları ise doğrudur.
- `data/raw` altında STAR98 ve Spector CSV'leri de yayımlanmış. Deponun
  kendi README'si bu gerçek verilerin kamuya yeniden dağıtılmasından önce
  izin durumunun doğrulanmasını istiyor. Bu konu netleştirilmeden dağıtımın
  tamamına yayın onayı verilmemeli; gerekirse gerçek veri ve türevleri
  yayımlanacak kapsamdan ayrılmalı. Bu inceleme hukuki izin tespiti değildir.
- Toplu IBM SPSS doğrulaması tamamlanmış sayılmıyor. Önceki yerel test
  raporları, yayımlanan dosyalarla eşleştirilerek belgelenmeli.

## Kitaptaki uygulama

- Ortak görünüm ve depo adresi: `frontmatter/bolum-paketleri.tex`.
- Çağrılar: `main.tex` içinde her bölüm girdisinin hemen arkasında.
- Tam eşleştirme: `companion/karekod-hedefleri.csv`.
- Ders sürümünde 14, kapsamlı sürümde 17 karekod bulunur.
- Kapsamlı sürümün 9. bölümü `bootstrap`, 10. bölümü `b09`,
  17. bölümü `b14` paketine gider. Paket kodu bölüm sayacından türetilmez.
- Karekod ve tıklanabilir metin aynı bölüm klasörüne yönelir. Karekodlar
  LaTeX tarafından üretilir; harici karekod hizmeti kullanılmaz.
- Kutuda ön yayın ve bekleyen SPSS doğrulaması açıkça belirtilir.

Bu bağlantılar `main` dalındaki güncellenebilir paketleri gösterir;
sabit bir baskı sürümüne kilitlenmiş değildir. Basımdan önce depo/dal/paket
adları sabitlenmeli, sürüm kaydı tutulmalı ve basılı boyutta telefonla
okutma sınaması yapılmalıdır. Telefonla okutma bu ortamda yapılmadı.

## İncelenen çevrim içi sayfalar

- https://github.com/ibrahimguney/istatistik
- https://github.com/ibrahimguney/istatistik/tree/main/bolumler
- https://github.com/ibrahimguney/istatistik/tree/main/bolumler/b01/ornek-01
- https://github.com/ibrahimguney/istatistik/tree/main/bolumler/b05
- https://github.com/ibrahimguney/istatistik/tree/main/bolumler/bootstrap
- https://github.com/ibrahimguney/istatistik/tree/main/bolumler/coklu-regresyon
- https://github.com/ibrahimguney/istatistik/tree/main/bolumler/anova
- https://github.com/ibrahimguney/istatistik/tree/main/data/raw

## Yerel derleme kontrolü

11 Eylül 2026'da her giriş üç XeLaTeX geçişiyle derlendi:

- `build/ders/main.pdf`: 213 sayfa; 14 bölüm bağlantısı.
- `build/kapsamli/main-kapsamli.pdf`: 259 sayfa; 17 bölüm bağlantısı.
- PDF URI hedefleri eşleştirme tablosuyla karşılaştırıldı; kapsamlı sürümün
  paket sırası da eşleşti. Yardımcı dosyalardaki karekod hedefleri ve matris
  boyutları denetlendi. Bu kontrol, bağımsız karekod çözümleme testi değildir.
- Son günlüklerde taşma (Overfull), tanımsız referans veya atıf yok.
- Her iki derlemede mevcut `companion/spss/syntax/b01.sps`–`b14.sps`
  eksikliklerine ilişkin 14 uyarı devam ediyor. Bu dosyalar bölüm paketlerinin
  `ornek-01/analiz.sps` dosyalarından farklıdır; bu görevde değiştirilmedi.
- B01 karekod sayfası ve önceki sayfa görsel olarak incelendi; kutu bölünmüyor.
  Yer olmadığında karekod bir sonraki sayfaya taşınıyor.

## Güncel hedef — 22 Eylül 2026

Birleşik kitap ve bölüm paketleri bundan sonra
`https://github.com/ibrahimguney/istatistik-kitabi` deposunda tutulur.
Kitaptaki karekodların güncel yolu `companion/bolumler/<paket>` biçimindedir.
Yukarıdaki bağlantılar önceki depo üzerinde yapılan tarihsel denetimi
belgelemek amacıyla korunmuştur.