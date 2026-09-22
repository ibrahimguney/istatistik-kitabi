# Örnek 01 — yeniden örnekleme ile iki ayrı soru

## Girdiler

- `veri.csv`: Beş yapay gözlem; kimlikler 1–5, değerler 2, 3, 3, 4, 13.
- `permutasyon.csv`: Altı yapay gözlem; A grubunda 7, 8, 9, B grubunda 2, 3, 4.
- `veri-sozlugu.csv`: Değişkenler ve plan sütunlarının anlamları.
- `bootstrap-plan.csv`: 5^5 = 3.125 sıralı, iadeli gözlem-kimliği örneklemi.
- `permutasyon-plan.csv`: 20 etiket ataması; ilk üç kimlik A, son üç B.
- `beklenen-sonuclar.csv`: Tam sayım için 26 bağımsız hesaplanmış kontrol değeri.

Planlar sonuç tablosu değildir: yazılımlar bu kimliklerle ham CSV'deki
sayılara erişip istatistikleri yeniden hesaplar. İki ayrı 3 değeri iki ayrı
gözlemdir; tekilleştirilmez. Plan sırası `sira` ile tanımlıdır. Dosyalardaki
satırları karıştırmak, kimlikleri ve `sira` değerlerini değiştirmediğiniz
sürece Python/R sonuçlarını değiştirmez.

## Python

Proje kökünden:

```bash
python companion/bolumler/bootstrap/ornek-01/cozum.py --check
python companion/bolumler/bootstrap/ornek-01/cozum.py --check --grafik --benzetim
```

Temel hesap ve kontrol yalnız standart kütüphaneyi kullanır; grafik seçeneği
Matplotlib gerektirir. Betik veri yollarını kendi konumundan bulur.
`--grafik`, `ciktilar/python/bootstrap-permutasyon.png` dosyasını yeniden
üretir ve varsa üzerine yazar; ham veriler ve referans CSV değiştirilmez.

Planları ayrı, henüz bulunmayan bir klasörde üretmek için örnek klasöründen:

```bash
python uret.py --hedef yeniden-planlar
```

Bu komut yalnız iki plan CSV'sini üretir. Mevcut hedefe yazmayı reddeder.
Öğretim paketi sabit 5 ve 6 gözlem için tasarlanmıştır; genel amaçlı bir
analiz kütüphanesi değildir. Python/R, sonlu ve mutlak değeri en çok 10^12
olan sayısal girdileri kabul eder; orijinal referanslar değişmiş veriye uymaz.

## R

Önce çalışma dizinini bu `ornek-01` klasörüne getirin:

```bash
Rscript cozum.R --check
Rscript cozum.R --check --grafik --benzetim
```

Ek R paketi gerekmez. `sessionInfo()` çıktısı sürümleri gösterir. R grafiği
`ciktilar/r/bootstrap-permutasyon.png` yoluna yazılır. R burada çalıştırılmadı.

## IBM SPSS

Çalışmanızı kaydedin ve yeni bir SPSS oturumunda çalışma dizinini bu örnek
klasörüne ayarlayın. `analiz.sps` dosyasının tamamını çalıştırın. Dosya
aktarılmamışsa byte düzeyinde aynı olan `analiz.sps.txt` kopyasını `.sps`
adıyla kaydedebilirsiniz. Betik CSV'leri okur; lookup tablolarını `MATCH FILES`
ile birleştirir, ortalamaları ve farkları hesaplar, iki histogram ile 15 ve
11 ölçülük `LIST` çıktıları oluşturur. Referans CSV ile bu çıktıları
karşılaştırın. Özel Bootstrap modülü veya Python/R eklentisi kullanılmaz.

SPSS betiği Python/R'deki sıkı girdi doğrulayıcısını uygulamaz. Önce Python
kontrolünü ve manifesti doğrulayın; SPSS uyarılarını göz ardı etmeyin.
SPSS çalıştırılmadı; hazır `.sav` veya `.spv` çıktısı yoktur.

## Tam sayım ve Monte Carlo

26 referans, rastgelelik içermeyen tam sayımdır. `--benzetim` ayrıca 2026
tohumuyla 10.000 bootstrap tekrarı yapar; bu çıktı kontrol CSV'sine dahil
değildir. Python ve R'nin aynı tohumla aynı rastgele diziyi üretmesi
beklenmez. Tam dağılımın varyansında payda 3.125, sonlu Monte Carlo tekrarları
üzerinden SE tahmininde payda 9.999 kullanılır. SPSS yalnız tam sayımı yapar.
Yüzdelikler üç çözümde de doğrusal interpolasyonla type 7 tanımına eşlenir.

## Teknik kaynaklar

- R quantile: `https://www.stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html`
- IBM MATCH FILES TABLE: `https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=files-table-subcommand-match-command`
- IBM AGGREGATE: `https://www.ibm.com/docs/en/spss-statistics/32.0.0?topic=reference-aggregate`

Belgeler kaynak incelemesini destekler; yorumlayıcıda çalışma testi yerine geçmez.