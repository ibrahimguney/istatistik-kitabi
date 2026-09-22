# Örnek 01 — Yöntemden rapora eşleştirilmiş değişim

## Veri ve tasarım

`veri.csv` tek satırda 24 tam çift, −3,2 ortalama son−ön farkı,
6 fark standart sapması ve 0,05 anlamlılık düzeyi içerir.
Burada çift, aynı öğrencinin ön ve son ölçümüdür; 24 öğrenci vardır,
48 bağımsız öğrenci yoktur. Farkların standart sapması, iki zamanın
standart sapmalarının farkı veya standart hata değildir.

Hedef parametre evrendeki son−ön farklarının ortalaması μ_D'dir.
H0: μ_D=0; H1: μ_D≠0. Eşleştirilmiş t testi, kişi bazlı farklara
uygulanan tek örneklem t hesabıdır. Farkların kişiler arasında bağımsızlığı,
aykırı değerler ve küçük örneklemde dağılım koşulları değerlendirilmelidir.
Ham farklar verilmediğinden bu kontroller burada yapılamaz.

CSV sütunları sözlükteki sırada ve sayısal olmalıdır. Tam çift sayısı en
az 2 tam sayı, fark standart sapması pozitif, α 0 ile 1 arasında olmalıdır.
Sıfır veya pozitif ortalama fark da geçerlidir. Eksik değerler sessizce
silinmez; Python/R geçersiz girdileri reddeder. SPSS'te elle kontrol gerekir.

## Çalıştırma

Komutları **bu örnek klasöründe** çalıştırın:

```bash
python cozum.py --check --grafik
Rscript cozum.R --check --grafik
```

Python NumPy, pandas, SciPy; grafik için Matplotlib kullanır. R standart
kurulum işlevlerini kullanır. Betikler paket kurmaz veya veri indirmez;
Python sürümleri ve R'de `sessionInfo()` konsola yazılır.
`--grafik` kendi PNG'sini oluşturur/yeniler, CSV'yi değiştirmez.

`--check`, 4 girdi ve 13 test/aralık sonucunu 1e-9 mutlak/bağıl toleransla
karşılaştırır. Etiket ve sıra da aynı olmalıdır; uyuşmazlık başarısız çıkış
üretir. Bu, kullanılan yöntemin bilimsel gerekçesinin doğrulandığı anlamına gelmez.
Alıştırmalarda klasör kopyasını kullanın; girdiyi değiştirince `--check`
olmadan çalıştırın. Özgün kontrol dosyası yeni girdinin referansı değildir.

## Sonuç haritası

`standart_hata`, `serbestlik`, `t`, `p_cift`, `dz` temel hesapları;
`kritik_t`, `hata_payi`, `alt_sinir`, `ust_sinir`, `genislik` aralığı gösterir.
`guven_duzeyi=1-alfa`dır. `reddet=1`, H0 reddedilir; 0, reddedilemez demektir.
`p<alfa` kullanılır, eşitlikte ret yoktur. `sifir_aralikta=1` sıfır kapalı
aralıkta, 0 dışarıda demektir. Karar ve aralık yorumunu yuvarlanmamış
sayılarla yapın; eşik noktasındaki sayısal duyarlılığı dikkate alın.

## SPSS

1. Açık dosyalarınızı kaydedin; çalışma dizinini bu örnek klasörüne ayarlayın.
2. Tek özet satırını ve veri sözlüğündeki koşulları elle denetleyin.
3. `analiz.sps` dosyasını çalıştırın; görünmüyorsa `analiz.sps.txt` kopyasını
   UTF-8 ile `analiz.sps` adıyla kaydedin.
4. Dictionary ve iki LIST tablosunu kontrol CSV'siyle karşılaştırın.
   SPSS'teki `t_degeri`, kontrolün `t` alanıdır; diğer adlar aynıdır.
   Etiketler ve ekran yuvarlamasını dikkate alıp sürümü ve sonucu kaydedin.

SPSS betiği özet satırını 24 kişinin ham verisi gibi T-TEST'e vermez;
COMPUTE, CDF.T ve IDF.T ile formülleri uygular. Otomatik girdi doğrulaması,
`--check` veya grafik yoktur. SPSS bu ortamda çalıştırılmadı; `.sav`/`.spv`
çıktısı sunulmadı. R sözdiziminin incelenmesi de R çalışma testi değildir.

## Teknik başvurular

- [R Student t dağılımı](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/TDist.html)
- [IBM CDF.T ve IDF.T işlevleri](https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=reference-glossary)

[Açıklamalı çözüm](cozum.md) · [Grafik açıklaması](grafik-aciklamasi.md)