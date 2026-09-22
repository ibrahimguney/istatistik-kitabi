# Örnek 01 — Okul türü, sınıf ve puan

## Soru ve ortak girdi

Dört öğrenci için okul türü, sınıf düzeyi ve puan kaydedilmiştir. Hangi
özetler anlamlıdır? Genel ve okul türüne göre puan ortalamaları nedir?
Bu sayılar ne zaman örneklem istatistiği, ne zaman evren parametresidir?

Üç dil de **aynı `veri.csv` dosyasını** okur. Virgül sütun, nokta ondalık
ayırıcıdır; ilk satır değişken adlarıdır. `Ozel`, özel okul kategorisinin
ASCII etiketidir. Sıralama `1 < 2 < 3` olarak belirlenmiştir. Puanın ölçek
sınırları verilmediğinden kod 0–100 gibi ek bir sınır varsaymaz.

## Çalışma dizini

Kitap projesinin kökünden:

```sh
cd companion/bolumler/b02/ornek-01
```

İleride yalnız `bolumler/` içeren bağımsız eşlikçi depo kullanıldığında
karşılığı `cd bolumler/b02/ornek-01` olacaktır. Aşağıdaki komutları örneğin
klasöründen çalıştırın; dosyayı açmak çalışma dizinini kendiliğinden ayarlamaz.

## Python

Python 3 ve pandas gerekir. Kod kurulum veya veri indirme işlemi yapmaz.

```sh
python cozum.py
python cozum.py --check
```

Okul türü sırasız kategorik, sınıf sıralı kategorik yapılır. Sınıfın
aritmetik ortalaması alınmaz. Kontrolün beklenen son satırı:

```text
DOGRULANDI: 23 kontrol degeri eslesiyor.
```

## R

Standart R kurulumu yeterlidir; ek paket gerekmez.

```sh
Rscript cozum.R
Rscript cozum.R --check
```

`factor` nominal okul türünü, `ordered` sıralı sınıfı tanımlar. R konsolunda
çalışma dizini bu klasörken `source("cozum.R")` özeti üretir; konsoldaki bu
kullanım otomatik `--check` karşılaştırmasını başlatmaz. Kontrol için terminal
komutunu kullanın veya çıktı değerlerini CSV ile karşılaştırın.

## SPSS

1. Kaydedilmemiş başka çalışmalarınızı kaydedin.
2. Çalışma dizinini bu örnek klasörüne ayarlayın. Kitap projesinin kökündeyseniz
   Syntax penceresinde bir kez `CD 'companion/bolumler/b02/ornek-01'.`
   çalıştırabilirsiniz. Zaten örnek klasöründeyseniz bunu tekrar çalıştırmayın.
3. `analiz.sps` dosyasını açıp tamamını çalıştırın. Yalnız `.sps.txt` kopyası
   görünüyorsa onu bilgisayarınızda `analiz.sps` adıyla kaydedin; içeriği aynıdır.
4. Dictionary çıktısında `okul_turu` için nominal, `sinif` için ordinal,
   `puan` için scale tanımını kontrol edin.
5. Frequencies tablolarında okul ve sınıf frekanslarını inceleyin.
6. Descriptives çıktısında genel puan ortalamasını, Means tablosunda okul
   türüne göre ortalamaları okuyun. Sınıf için ortalama hesaplanmaz.

SPSS oranları yüzde olarak gösterebilir: 0.75 = %75, 0.25 = %25.
Tablolardaki ondalık basamak sayısı farklı olabilir; 72.33 ile
72.33333333333333 aynı hesabın farklı yuvarlanmış gösterimleridir. SPSS'te
CSV'ye otomatik çıktı aktarımı veya 23 satırlık otomatik karşılaştırma yoktur;
Dictionary ve özet tablolarını kontrol değerleriyle elle karşılaştırın.

## Girdi ve doğrulama sınırları

Özgün veride eksik hücre yoktur. Python/R çözümleri boş veri, eksik hücre,
geçersiz okul etiketi, 1–3 dışı sınıf kodu ve sonlu olmayan puanda durur.
Bu koruma genel bir eksik veri analiz yöntemi değildir. SPSS betiği aynı
otomatik korumaları uygulamaz; içe aktarma ve kodlar ayrıca denetlenmelidir.

Örnek kopyasında bir okul kategorisi tamamen çıkarılırsa frekansı 0 olur;
o grubun puan ortalaması Python/R'de `NaN` olur, 0 puan olarak yorumlanmaz.
Veri değiştirilince özgün kontrol CSV'sinin geçmesi beklenmez.

**R ve SPSS bu ortamda çalıştırılmamıştır.** Gerçek çalışma kontrolleri
[DOGRULAMA.md](../DOGRULAMA.md) kaydında ayrı izlenir. Python'un doğrulanması,
üç yazılımda sonuç eşitliğinin uçtan uca denendiği anlamına gelmez.

[Açıklamalı çözüm](cozum.md) · [Alıştırmalar](../alistirmalar.md) ·
[Yanıtlar](../cozumler.md)

## SPSS başvurusu

IBM SPSS Statistics, MEANS ve VARIABLE LEVEL komut belgeleri
(erişim: 9 Eylül 2026):

- https://www.ibm.com/docs/SSLVMB_sub/statistics_reference_project_ddita/spss/base/syn_means.html
- https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=preparation-setting-measurement-level-variables-unknown-measurement-level