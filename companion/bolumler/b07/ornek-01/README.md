# B07 / Örnek 01 — Oran tahmini, yanlılık ve MSE

## İki ayrı veri

`veri.csv`, tek `yanit` sütununda kitabın **1,0,1,1,0,1,1,0,1,0**
dizisini içerir. Bir satır bir yapay ikili yanıttır; 1 olayın gerçekleşmesini,
0 gerçekleşmemesini gösterir. Altı olumlu yanıt bulunur. Veri gerçek öğrenci
kaydı değildir; 0 eksik gözlem değildir.

`benzetim.csv` iki sütun ve 10000 satır içerir:

- `tekrar`: 1–10000 arasında benzersiz tekrar kimliği.
- `basari`: p=0,40 Bernoulli evreninden bağımsız 50 çekimdeki olumlu sayısı.

Bir benzetim satırı **50 gözlemli bir örneklemi** temsil eder. Başarı sayısı
0–50 arasında tam sayıdır; oran `basari/50` ile hesaplanır. Bu 10000 satır,
10000 kişilik bir araştırma örneklemi değildir. İlk on yanıttaki n=10 ile
benzetimdeki n=50 farklıdır. İlk verinin gerçek p'si bilinmiyor; ikinci
modelde p=0,40 tasarım gereği biliniyor.

Dosyalar UTF-8, virgülle ayrılmıştır. Yalnız tam sayı girdileri saklanır;
oranlar hesap sırasında üretilir. Python kaynağı `binomial(1, .40,
size=(10000, 50))` ile 500000 Bernoulli çekimi yapar ve satır başarı
toplamlarını kaydeder. Ham 0/1 matrisi depolanmaz. Üretim kaydı ve iki
CSV'nin SHA-256 değerleri `uretim-kaydi.json` içindedir.

## Çalıştırma

Kitap kökünden `cd companion/bolumler/b07/ornek-01`; bağımsız eşlikçi depo
kökünden `cd bolumler/b07/ornek-01` kullanın. Tüm komutlar bu örnek
klasöründe çalışır. Klasör bütünüyle taşınabilir, kitap dosyaları gerekmez.

### Python — ortak veriden çözüm

```bash
python cozum.py --check
python cozum.py --check --grafik
```

Python, NumPy ve pandas; grafik için Matplotlib gerekir. Sınanan sürümler
Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, Matplotlib 3.10.8. Betik paket kurmaz.
`--check`, 21 özet değerinin etiketlerini/sırasını ve sayılarını 1e-9
mutlak/bağıl toleransla karşılaştırır. Bu, sabit verinin yeniden
hesaplanmış özetine yönelik bir kontroldür; dosya bütünlüğü ayrıca SHA-256
ile denetlenir. Grafik `ciktilar/python/oran-tahmini.png` dosyasını yeniler.

### R — aynı iki CSV ile çözüm

```bash
Rscript cozum.R --check
Rscript cozum.R --check --grafik
```

Standart R yeterlidir. Yeni çekim yapılmaz; iki ortak CSV okunur.
RStudio'da çalışma dizini bu klasörken `source("cozum.R")` sayıları gösterir.
Kontrol ve grafik için ayrıca:

```r
kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
grafik_kaydet(veri, benzetim)
```

Betik `sessionInfo()` çıktısını verir. R grafiği ayrı
`ciktilar/r/oran-tahmini.png` dosyasına yazılır. **R burada çalıştırılmadı;
ortak veri üzerindeki sayısal eşleşme henüz gerçek R testiyle doğrulanmadı.**

### IBM SPSS — ortak veriyi özetleme

1. Açık veri dosyalarını kaydedin. Çalışma dizinini bu örnek klasörü yapın.
   SPSS kitap kökünde başlatılmışsa `CD 'companion/bolumler/b07/ornek-01'.`
   kullanılabilir. Sözdizimini açmak tek başına çalışma dizinini değiştirmez.
2. `analiz.sps` çalıştırın. Uzantı taşınmıyorsa `analiz.sps.txt` yedeğini
   aynı klasörde `analiz.sps` adıyla kaydedin.
3. İlk veri `B07Yanit` adıyla açılır. Frequencies'te 10 geçerli, eksik olmayan
   yanıt; 1 için 6, 0 için 4 kayıt olmalı. Liste çıktısında p-hat=0,6,
   yerine-koyma varyansı 0,024 ve SE≈0,154919 görünmeli.
4. **İlk veride DESCRIPTIVES'in Std. Error of Mean sütunu aynı formül değildir:**
   örneklem standart sapmasını kullanır; bu pilotta yaklaşık 0,163299
   verir. İstenen oran SE'si kodun açıkça hesapladığı `se_hat` değeridir.
5. İkinci dosya `B07Benzetim` adıyla açılır ve aktif veri olur. N=10000,
   tahminin 0–1 aralığında olması ve [çözüm tablosundaki](cozum.md) merkez,
   yanlılık, varyanslar, SE ve MSE kontrol edilir. Her satırda n=50 modelinin
   geçerli olduğunu unutmayın. Başarı sayıları eksiksiz ve 0–50 arasında olmalı.
6. Benzetimde **Std. Deviation**, ampirik SE'dir; Std. Error of Mean bu
   sayıyı tekrar √10000'e böler, farklı bir niceliktir.

SPSS iki veriyi ayrı ayrı açar; on yanıt ile 10000 tekrar birleştirilmez.
AGGREGATE sonuçları `MODE=ADDVARIABLES` ile satırlara eklenir; tek satırlık
LIST görüntüsü, veri setinin bir gözleme indirildiği anlamına gelmez.
Geçici seçim yalnız ilgili liste çıktısına uygulanır. `WEIGHT BY` yoktur.
SPSS yerleşik histogramının sınıfları/ekseni Python/R ayrık frekans grafiğiyle
aynı olmayabilir. **SPSS çalıştırılmadı; otomatik 21 satırlık SPSS kontrolü,
`.sav` veya `.spv` çıktısı sunulmuyor.**

## Ortak benzetimi yeniden üretme

```bash
python uret.py
```

Varsayılan yeni dosya `yeniden-benzetim.csv` olur; `--cikti deneme.csv`
ile başka bir yeni dosya seçilebilir. Mevcut dosyanın üzerine yazılmaz,
mutlak yol ve `..` kabul edilmez; alt klasörler önceden var olmalıdır.
`veri.csv` ve `benzetim.csv` normal yeniden üretim çağrısında değiştirilmez.
Kayıtlı ortamda yeni benzetim CSV'si kaynakla byte düzeyinde eşleşmelidir.
Başka sürüm veya algoritmada yalnız aynı tohumdan byte eşitliği çıkarılmaz.

## R'de bağımsız yeni benzetim

```bash
Rscript benzetim.R
```

R betiği üreteci açıkça seçer, `set.seed(2026)` ve
`rbinom(10000, size=50, prob=0.40)` ile doğrudan başarı sayıları üretir.
Bu, Python'da 50 ayrı Bernoulli çekimini toplamakla aynı olasılık modelidir;
aynı algoritma/rastgele sayı akışı değildir. Yeni dosya
`ciktilar/r/yeni-benzetim.csv` olur; mevcut dosya üzerine yazılmaz.

R'nin yeni benzetimi için merkez≈0,40, SE≈0,069282 ve MSE≈0,0048
beklenir; kaydedilmiş Python sayılarına birebir eşitlik beklenmez.
Kaynak CSV'yi yeni veriyle değiştirmeyin veya referansı yeni benzetime
uydurmayın. Bu R betiği de burada çalıştırılmadı.

## Hesaplama sözleşmesi

- İlk veride yaklaşık SE, bilinmeyen p yerine p-hat konularak
  `sqrt(p_hat*(1-p_hat)/n)` ile bulunur. Bu bir güven aralığı veya
  örneklemin rastgele seçildiğine ilişkin kanıt değildir.
- `p_hat_060` etiketli n=25 ve n=400 kontrolleri sabit p-hat=0,60 için
  ayrı duyarlılık hesaplarıdır; CSV'de bu hacimlerde yeni yanıtlar yoktur.
- Benzetimde gerçek p=0,40 ve n=50 sabittir. Merkez, tekrar oranlarının
  ortalaması; ampirik yanlılık bu merkez eksi 0,40'tır. MSE, her tekrarın
  0,40'tan karesel hatasının **B bölenli** ortalamasıdır.
- Tam ampirik özdeşlik `MSE = varyans_B + ampirik_yanlilik²` biçimindedir.
  `varyans_B` tekrar merkezinden kareli sapmaları B'ye böler. Ampirik SE
  ise örneklem standart sapmasıdır: `sqrt(varyans_Beksi1)`. B−1 varyansını
  doğrudan özdeşliğe koymak küçük ama gerçek bir fark doğurur.
- Kuramsal olarak oran tahmin edicisi yansızdır; MSE=Var=p(1−p)/n=0,0048.
  Sonlu tekrarda ampirik MSE/yanlılık tam bu değerlere eşit olmak zorunda değildir.
- Python/R, yanıtların 0/1 olmasını, en az bir yanıtı; benzetimin en az
  iki tekrarını, 1..B arasında benzersiz kimliklerini ve tam sayı 0..50
  başarılarını denetler. Sıfır geçerli değerdir, eksik yerine konmaz.
- Bütün yanıtlar aynı olduğunda bu yaklaşık SE formülü 0 verir. Bu,
  gerçek belirsizliğin sıfır veya p'nin kesin 0/1 olduğunu kanıtlamaz.
  Küçük örneklem ve uç oranlarda yaklaşım özellikle dikkatle yorumlanır.
- Satır sırası sonuçları değiştirmez. Özetlerin eşleşmesi bütün dosyanın
  birebir aynı olduğunu kanıtlamaz; veri özeti bunun için ayrıca tutulur.

## Teknik kaynaklar

9 Eylül 2026 tarihinde incelenen resmi belgeler:

- NumPy binomial üreteci:
  <https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html>
- R binom dağılımı ve `rbinom`:
  <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Binomial.html>

Bu kaynakların incelenmesi R/SPSS çalışma testi değildir.
[Doğrulama kaydı](../DOGRULAMA.md) yapılan ve bekleyen kontrolleri ayırır.