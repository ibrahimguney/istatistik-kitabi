# Örnek 01 — Çalışma, devamsızlık ve ayarlanmış ilişki

## Veri

`veri.csv`, saat=2,4,6,8 ile devamsızlık=0,1,2'nin 12 birleşimidir.
Kitaptaki R `expand.grid` düzeni korunur: saat en hızlı değişen sütundur.
Hata dizisi 1,−1,−1,1,−2,2,2,−2,1,−1,−1,1 olarak elle belirlenmiştir.
Puanlar 40+2×saat−3×devamsızlık+hata ile hesaplanır. Rastgele çekim veya
rastgele örnekleme yapılmamıştır; tohum gerekmez. Gerçek katılımcı yoktur.

`yeni.csv`, saat=5, devamsızlık=2 noktasını içerir; bu satır modeli
uydurmak için kullanılmaz. `veri-sozlugu.csv` birimleri ve eksik veri
kurallarını, `uretim-kaydi.json` kaynakları ve üretim bilgilerini kaydeder.
Ham CSV'lerde eksik/sonsuz veri kabul edilmez; sessiz satır silme yapılmaz.

## Çalıştırma

Terminalde önce bu `ornek-01` klasörüne geçin:

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

Python için NumPy, pandas, SciPy; grafik için Matplotlib gerekir.
R, standart kurulumdaki `lm`, `confint`, `predict` ve yardımcı regresyonları
kullanır; VIF için ek paket gerekmez. Python modeli QR ayrıştırmasıyla
uydurur. İki açıklayıcı için VIF=1/(1−r²) hesabı kullanılır; bu kısayol
keyfi sayıda açıklayıcıya doğrudan genellenmemelidir.

`--check` 66 değeri, etiket ve sıra dahil `beklenen-sonuclar.csv` ile
karşılaştırır. Çoğu ölçüde mutlak/bağıl tolerans 1e-9'dur; p değerlerinde
mutlak tolerans sıfır, bağıl tolerans 1e-8'dir. Böylece küçük p değerini
sıfır yazmak kontrolden geçmez. Grafik seçeneği çıktı PNG'sini yeniler;
girdi dosyalarını değiştirmez. R/SPSS kontrolleri henüz gerçek ortamda yapılmadı.

SPSS'te çalışma dizinini bu klasör yapın ve `analiz.sps` çalıştırın.
Uzantı aktarımda kaybolursa `analiz.sps.txt` dosyasını `.sps` adıyla kopyalayın.
Menü karşılığı Analyze > Regression > Linear; bağımlı değişken puan,
bağımsız değişkenler saat ve devamsızlık, yöntem Enter'dır. Coefficients,
Model Summary, ANOVA ve Collinearity Diagnostics tablolarını okuyun.
Betik aynı hesapları merkezlenmiş çapraz çarpımlarla ayrıca yapar;
REGRESSION'ın kaydettiği uydurulan/artık değerlerle yan yana gösterir.

SPSS LIST eşleştirmesi: b0/se0/t0/p0/alt0/ust0 sabit terim,
b1/... saat, b2/... devamsızlık katsayısıdır. `hacim` Python/R'deki n,
`f_degeri` F istatistiğidir. Son LIST `yeni.csv` için ortalama güven ve
bireysel öngörü aralıklarını verir. Yeni satır eğitim verisine eklenmez.
SPSS'in LISTWISE seçeneğine rağmen paket eksik veri kabul etmez; önce
Python doğrulamasını çalıştırın. Ekran yuvarlamasını ve bilimsel gösterimi
dikkate alın. Hazır `.sav`/`.spv` çıktısı sunulmaz.

## Yeniden üretim

```bash
python uret.py
```

`yeniden-veri.csv` üretir; var olan dosyanın üzerine yazmaz.
`--cikti deneme.csv` ile başka göreli dosya adı seçilebilir.
Kaynak veri korunur; üretim tamamen deterministiktir. Kaydedilen ortamda
çıktının ortak CSV ile byte düzeyinde eşitliği doğrulandı.

Değişik veri veya yeni nokta denenirse eski `--check` referansının
başarısız olması normaldir; eski beklenen dosyayı otomatik güncellemeyin.
Kod, gözlenen açıklayıcı aralığı dışında kalan yeni noktalar için uyarı verir;
aralık içinde olmak da model geçerliliğinin kanıtı değildir.

## Yorum ve kaynaklar

[Açıklamalı çözüm](cozum.md), [grafik açıklaması](grafik-aciklamasi.md).
Katsayılar koşullu ilişkiyi betimler; nedensellik çıkarımı değildir.
Hatalar kolay sayısal kontrol için tasarlandığından p değerleri ve aralıklar
gerçek bir evrene ilişkin kanıt olarak kullanılamaz. VIF=1; bağımsızlık,
normal hata, sabit varyans veya doğru model biçimini doğrulamaz.

9 Eylül 2026'da incelenen resmî belgeler:

- R `lm`: `https://www.stat.ethz.ch/R-manual/R-devel/library/stats/html/lm.html`
- R `predict.lm`: `https://www.stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.lm.html`
- IBM REGRESSION: `https://www.ibm.com/docs/en/spss-statistics/31.0.0?topic=reference-regression`

Belge incelemesi R/SPSS çalıştırma sınaması değildir.