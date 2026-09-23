# İstatistik

## Öğrenci çalışma alanı

[Bölümler, ders rotaları ve uygulama dosyaları](https://ibrahimguney.github.io/istatistik-kitabi/) · [Siteyi güncelleme rehberi](web/README.md)


## Veri Okuryazarlığından İstatistiksel Çıkarıma

İbrahim Güney tarafından hazırlanan bu proje, IMO301 İstatistik ve PDR209
Temel İstatistik için geliştirilen iki kitabın içerikleri silinmeden,
yinelenen anlatımlar ayıklanarak oluşturulmuş 20 bölümlük birleşik ders
kitabıdır.

Depo; kitabın LaTeX kaynaklarını, görsel kapaklarını, bölüm alıştırmalarını,
Python–R–SPSS uygulamalarını, veri sözlüklerini ve yeniden üretilebilir
eşlikçi dosyaları birlikte içerir.

## Kitabın kapsamı

Kitap araştırma süreci ve veri kalitesinden başlayarak aşağıdaki ana yolu
izler:

1. veri, araştırma, betimleme ve eksik veri,
2. örnekleme değişkenliği, tahmin ve güven aralıkları,
3. hipotez testleri, etki büyüklüğü ve grup karşılaştırmaları,
4. kategorik veri, korelasyon ve regresyon,
5. parametrik olmayan yöntemler ve ölçek güvenirliği,
6. bütünleştirici veri analizi ve yöntem seçimi.

Ayrıntılı bölüm kaynağı ve birleştirme kararları
[`BIRLESTIRME-HARITASI.md`](BIRLESTIRME-HARITASI.md) dosyasındadır.

## Hızlı başlangıç

XeLaTeX, `latexmk` ve `makeindex` bulunan bir sistemde varsayılan e-kitabı
üretmek için:

```sh
./build-ebook.sh
```

Komut, proje kökünde `ebook.pdf` dosyasını oluşturur. `main.tex` doğrudan
derlendiğinde de e-kitap profili kullanılır:

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Matbaaya yönelik PDF/X-4 iç blok ve taşmalı kapak için:

```sh
./build-print.sh
```

Derlenmiş PDF dosyaları Git geçmişine alınmaz; doğrulanmış dağıtım
dosyalarının GitHub Releases üzerinden yayımlanması önerilir.

## Dizin yapısı

- `main.tex`: varsayılan PDF e-kitap girişi
- `main-pdfx4.tex`: PDF/X-4 baskı iç bloğu
- `cover-print.tex`: arka kapak, sırt ve ön kapağı içeren baskı formu
- `frontmatter/`: ön kapak, iç kapak çevresi ve kullanım rehberleri
- `chapters/`: korunmuş ve birleşik ana bölümler
- `chapter-exercises/`: çözümlü bölüm alıştırmaları
- `appendix/`, `backmatter/`: ekler, sözlük, kaynakça ve kapak
- `companion/`: veri, kod, SPSS dosyaları ve bölüm paketleri
- `assets/`: kitapta kullanılan görseller ve kurumsal logo
- `sources/`: önceki kitap projelerinden korunan düzenlenebilir kaynaklar

## Eşlikçi uygulamalar

`companion/` klasöründe bölüm bazlı R, Python ve SPSS uygulamaları bulunur.
Veri kaynağı, gözlem birimi ve kullanım sınırları veri sözlüklerinde ayrıca
belirtilir. Bütün üretim ve kontrol akışını çalıştırmak için:

```sh
python companion/code/run_all.py
```

Python doğrulamasının geçmesi, R veya SPSS kodunun ilgili yazılımda ayrıca
çalıştırıldığı anlamına gelmez. Doğrulama kayıtları bölüm klasörlerinde
saklanır.

## Önceki projeler

Birleşik kitap aşağıdaki iki çalışma alanından geliştirilmiştir:

- `ibrahimguney/istatistik`
- `ibrahimguney/temelistatistik`

Bu depolar tarihsel kaynak ve önceki sürüm olarak korunabilir; yeni birleşik
çalışmanın ana deposu `ibrahimguney/istatistik-kitabi`dır.

## Atıf

Akademik kullanım için [`CITATION.cff`](CITATION.cff) dosyasındaki bilgi
kullanılabilir. GitHub arayüzü bu dosyadan “Cite this repository” çıktısı
üretebilir.

## Haklar ve kullanım koşulları

Depodaki mevcut kullanım koşulları [`LICENSE.md`](LICENSE.md) dosyasında
açıklanmıştır. Şimdilik genel bir açık kaynak veya açık kitap lisansı
verilmemektedir; aksi ayrıca belirtilmedikçe kitap metni ve özgün materyaller
üzerindeki tüm haklar saklıdır. Üçüncü taraf veri setleri ve yazılımlar kendi
kaynaklarında belirtilen kullanım koşullarına tabidir.