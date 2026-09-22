# Örnek 01 — Grup özetlerinden ANOVA, Tukey ve Welch

## Girdiler ve sınırlar

`veri.csv`, klasik ANOVA için üç grup özetidir. `welch.csv`, eşit olmayan
varyans örneğinin üç ayrı grup özetidir. Sütunlar `grup,n,ortalama,standart_sapma`;
grup etiketleri A,B,C sırasındadır. Standart sapmalar grup içinde n−1
paydalı örneklem standart sapmalarıdır; varyans veya standart hata değildir.
Toplam hacimler sırasıyla 30 ve 40'tır; dosyalar bireysel ölçümleri içermez.

`ciftler.csv` yalnız karşılaştırma kimliklerini taşır: 1=A–B, 2=A–C,
3=B–C; grup kodları 1=A, 2=B, 3=C. SPSS bunu grup özetlerine eşler.
Python komutu haritanın doğru olduğunu denetler; Python hesap fonksiyonu
çiftleri A,B,C'den kendisi oluşturur. R haritayı okuyup doğrular.
`veri-sozlugu.csv` tüm alanları, `kaynak-kaydi.json` kitap kaynaklarını açıklar.

Özetlerden normallik, aykırı gözlem, Levene testi veya bireysel artık grafiği
elde edilemez. Bunları yapabilmek için sahte bireysel ölçüm oluşturulmadı.

## Çalıştırma

Önce terminalde bu `ornek-01` klasörüne geçin:

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

Python: NumPy, pandas, SciPy; grafik için Matplotlib. R: temel kurulum
fonksiyonları yeterlidir. `--check` 70 sayısal değeri, etiket ve sıra dahil
`beklenen-sonuclar.csv` ile karşılaştırır. `--grafik` ilgili PNG'yi yeniden
yazar; CSV girdileri değişmez. R/SPSS betikleri burada çalıştırılmadı.

R, özetlerden doğrudan formülleri hesaplar; bu üç satırı `aov` veya
`oneway.test` komutlarına ham veriymiş gibi vermez. Aynı nedenle SPSS
betiği ONEWAY çalıştırmaz ve WEIGHT BY n kullanmaz: bu, grup içi yayılımı
kaybeder. SPSS'te çalışma dizinini bu klasör yapıp `analiz.sps` çalıştırın.
Dosya uzantısı kaybolursa aynı içerikli `analiz.sps.txt` yedeğini `.sps`
adıyla kaydedin. Hazır `.sav`/`.spv` çıktısı yoktur.

SPSS LIST tabloları sırayla girdileri, klasik sonuçları, üç Tukey çiftini ve
Welch sonucunu gösterir. `kritik_q` R/Python'daki `q_kritik`, `duzeltme_toplami`
Welch `duzeltme`, `pay_welch` Welch `pay` değeridir. SPSS ek karar sütunları da
basar. Küçük p değerlerinde bilimsel gösterimi kullanın; 0,000 görüntüsü p=0
değildir. SPSS girdileri Python kadar kapsamlı denetlemez; önce Python
kontrolünü çalıştırın. SPSS sıralı A,B,C satırlarını 1,2,3 ile eşler.

## Yöntem ve sayısal tolerans

Klasik ANOVA ortak MSE kullanır. Tukey'de A−B, A−C, B−C fark yönleri
sabitlenmiştir. `se_q=sqrt(MSE/2*(1/n_i+1/n_j))`; bu, farkın olağan
standart hatasının √2'ye bölünmüş halidir. Kritik değer üç grup ve 27 hata
serbestliği için studentized range dağılımından gelir. R `qtukey/ptukey`,
Python `studentized_range.ppf/sf`, SPSS `IDF.SRANGE/CDF.SRANGE` kullanır;
parametre sırası olasılık veya q, grup sayısı, hata serbestliğidir.

Python denetimi olağan ölçülerde mutlak/bağıl 1e-9; p değerlerinde mutlak
0 ve bağıl 1e-8 tolerans kullanır. Referans Tukey sonuçları SciPy'nin
studentized_range çağrısını kopyalamak yerine ayrı Gauss–Hermite/Gauss–Laguerre
integrasyonu ve kök aramasıyla hesaplandı.

R'nin resmî belgesi `qtukey` için dördüncü ondalık basamak doğruluğu belirtir.
Bu yüzden R kontrolünde q-kritik için mutlak 1e-4; Tukey yarı genişlik/alt/üst
sınırlarında 1e-4×se_q+1e-8; düzeltilmiş p değerlerinde 1e-6 tolerans kullanılır.
Diğer hesaplar sıkı toleransı korur; pozitif referans p değeri sıfırla eşleşemez.
Bu toleranslar gerçek R çalışma testinin yerine geçmez. SPSS sonuçlarını da
bu yaklaşık sayısal sınırlar ve ekran yuvarlamasıyla değerlendirin.

Welch ayrı CSV'den n/s² ağırlıkları ve payda serbestlik düzeltmesiyle
hesaplanır. Klasik örneğin ortak MSE/Tukey aralıkları Welch örneğine taşınmaz;
Games–Howell gibi ek karşılaştırmalar bu pakette uygulanmadı.

## Yeniden kaydetme

```bash
python uret.py
```

Kitaptaki iki özet ile karşılaştırma haritasını `yeniden-ozetler/` içine
kaydeder. Klasör varsa durur; `--cikti deneme` ile başka göreli alt klasör
seçilebilir. Ham gözlem üretmez, mevcut CSV'leri değiştirmez, rastgele tohum
gerektirmez. Kaydedilen ortamda üç CSV'nin byte eşitliği doğrulandı.

## Kaynaklar ve yorum

[Açıklamalı çözüm](cozum.md), [grafik açıklaması](grafik-aciklamasi.md).
Klasik ANOVA/Tukey için bağımsız gözlemler, grup içi yaklaşık normallik ve
ortak hata varyansı modeli gerekçelendirilmelidir. Welch varyans eşitliği
zorunluluğunu kaldırır; bağımsızlık veya örnekleme tasarımı sorunlarını çözmez.
Bu yapay özetler yöntem gösterimidir, gerçek bir araştırma sonucu değildir.

9 Eylül 2026'da incelenen resmî belgeler:

- R Tukey: `https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Tukey.html`
- SciPy: `https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.studentized_range.html`
- IBM dağılım fonksiyonları: `https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=expressions-random-variable-distribution-functions`
- IBM komut başvurusu: `https://public.dhe.ibm.com/software/analytics/spss/documentation/statistics/26.0/en/client/Manuals/IBM_SPSS_Statistics_Command_Syntax_Reference.pdf`