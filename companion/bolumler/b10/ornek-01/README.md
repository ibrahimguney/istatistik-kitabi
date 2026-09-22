# Örnek 01 — Test sonucu ile yeni çalışma planını ayırmak

## Girdiler

`veri.csv` gözlenen tek örneklemin özetidir; `plan.csv` yeni çalışma
varsayımlarını tutar. Aynı sütun adı farklı rol taşıyabilir:
`veri.csv` içindeki `standart_sapma` örneklem s'si, `plan.csv` içindeki ise
planlama için varsayılan evren σ'sıdır. Ayrıntılar `veri-sozlugu.csv` içindedir.

Hacimler en az 2 olan tam sayılardır; standart sapmalar pozitif, α değerleri
0 ile 1 arasındadır. Bu paket sonlu hacim araması için planlanan farkı
sıfırdan farklı ve hedef gücü α ile 1 arasında ister. Girdi doğrulaması
Python/R'de yapılır; SPSS'te ayrıca elle kontrol gerekir.

## Çalıştırma

Tüm komutlar **bu örnek klasöründe**, iki CSV yan yana dururken çalıştırılır:

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

Python: NumPy, pandas, SciPy; grafik için Matplotlib gerekir. R yalnız
standart kurulum işlevlerini kullanır. Betikler paket kurmaz veya veri indirmez.
`--check` 30 kontrolü 1e-9 mutlak/bağıl toleransla karşılaştırır; etiket ve
sıra da denetlenir. Uyuşmazlık başarısız çıkış üretir. Python sürümleri ve
R'de `sessionInfo()` konsola yazılır. `--grafik` olmadan yalnız sonuç
tablosu yazılır. Grafik seçeneği kendi çıktı PNG'sini oluşturur/yeniler;
CSV'leri değiştirmez.

Alıştırmalar için klasörün kopyasını alın, ilgili girdiyi değiştirin ve
`--check` olmadan çalıştırın. Dağıtılan referans yalnız özgün girdilere aittir;
yeni girdilerin bu kontrolü geçmesi beklenmez.

## Çıktı tablosu

- `girdi`: Testin 5 girdi değeri; `plan_girdi`: Planın 5 girdi değeri.
- `test`: 11 sonuç; df, SE, t, çift yönlü p, Cohen d, kritik t,
  güven aralığı uçları, hata payı, genişlik ve ret göstergesi.
- `plan`: 9 sonuç; planlanan d, df, kritik t, merkez dışılık,
  güç, β, gereken en küçük hacim, bir önceki hacmin gücü ve gereken hacmin gücü.

Test aralığı `1-veri.csv:alfa` düzeyindedir. `reddet_cift=1` H0 reddedilir,
0 reddedilemez anlamındadır; kural yuvarlanmamış p<α'dır, eşitlikte ret yoktur.
Plan, yalnız `plan.csv` dosyasını kullanır. İki dosyanın α değerleri ayrı
amaçlarla değiştirilebilir; bunu raporda açıkça belirtin.

## Güç ve hacim hesabı

Python merkezi olmayan t dağılımının iki kuyruğunu toplar. R'de
`power.t.test(..., type="one.sample", alternative="two.sided", strict=TRUE)`
aynı iki ret bölgesini içerir. Yalnız gerçek etkinin yönündeki ret bölgesini
saymak bu paketle aynı tanım değildir.

Python/R tam sayı hacmi 2–10000 aralığında ikili aramayla bulur; SPSS
aynı aralıkta küçükten büyüğe tarar. Kitabın kesirli hacmi yukarı yuvarlama
sonucuyla birlikte, n=33'ün yetersiz ve n=34'ün yeterli olduğu da denetlenir.
Arama sınırı bilimsel bir üst sınır değildir. Hedef burada bulunamazsa
Python/R hata verir, SPSS `gereken_hacim` alanını eksik bırakır: bu durum
“çözüm yok” diye yorumlanmaz. Gerekli en küçük hacim 2 ise n=1 için t gücü
tanımlanmadığından `onceki_guc` Python'da NaN, R'de NA, SPSS'te eksik olur.
Bu sınır durumu özgün 30 kontrolün konusu değildir.

## SPSS

1. Açık dosyalarınızı kaydedin ve çalışma dizinini bu örnek klasörüne ayarlayın.
2. `analiz.sps` dosyasını açıp tamamını çalıştırın. Dosya görünmüyorsa
   `analiz.sps.txt` kopyasını UTF-8 ile `analiz.sps` adıyla kaydedin.
3. Her iki CSV'nin **tek satır** ve veri sözlüğündeki sırada olduğunu kontrol edin.
   Betik iki satırı sıra üzerinden birleştirir; birden fazla satıra uygun değildir.
4. Dictionary ve dört LIST tablosunu `beklenen-sonuclar.csv` ile karşılaştırın.
   `t_degeri` kontrolün `t` alanıdır. Plan girdileri SPSS'te `plan_hacim`,
   `plan_fark`, `plan_sapma`, `plan_alfa`, `hedef_guc` adlarını alır.
5. Görüntülenen etiketler ve yuvarlamayı dikkate alın; sürümü ve gerçek
   kontrol sonucunu bölümün doğrulama kaydına ekleyin.

SPSS özet satırını ham katılımcı gibi T-TEST'e vermez; formüller ve
`NCDF.T` ile hesaplar. Bir güç analizi menüsünün varlığını gerektiren
`POWER MEANS ONESAMPLE` komutu bu betiğe eklenmedi. SPSS betiğinde otomatik
`--check`, grafik veya Python/R'deki girdi denetimleri bulunmaz.
SPSS üst kuyruğunda `1-NCDF.T` kullanımı çok uç değerlerde duyarlılık
kaybedebilir; özgün örneğin kontrol değerleriyle karşılaştırma yapılmalıdır.
Hazır `.sav`/`.spv` verilmez; SPSS bu ortamda çalıştırılmadı.

## Teknik başvurular

- [SciPy merkezi olmayan t dağılımı](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nct.html)
- [R power.t.test ve strict seçeneği](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/power.t.test.html)
- [IBM dağılım işlevleri ve NCDF](https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=expressions-random-variable-distribution-functions)
- [IBM NCDF.T sözdizimi](https://www.ibm.com/docs/en/spss-statistics/32.0.0?topic=functions-cumulative-distribution)
- [IBM LOOP–END LOOP](https://www.ibm.com/docs/en/spss-statistics/cd?topic=reference-loop-end-loop)

Belgelerin incelenmesi çalışma testi değildir. [Çözüm](cozum.md) ve
[grafik açıklaması](grafik-aciklamasi.md) sayısal yorumları tamamlar.