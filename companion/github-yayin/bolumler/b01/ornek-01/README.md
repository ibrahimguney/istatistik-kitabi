# Örnek 01 — Beş öğrencilik veriyi tanıma

## Soru ve veri

Bir satır ve sütun neyi gösteriyor? Hangi değişkenler nicel, hangisi
kategorik? Program frekansları ve oranları ile devam ve başarı ortalamaları
nedir? Hangi sonuçları çıkaramayız?

Üç çözüm de **bu klasördeki `veri.csv` dosyasını okur**. Virgül sütun,
nokta ondalık ayırıcıdır. İlk satır değişken adlarıdır. Sözlük
`veri-sozlugu.csv` içindedir. Kodlar özgün veriyi değiştirmez; çıktı konsola
veya SPSS çıktı penceresine gider.

## Çalışma dizini

Komutları `ornek-01` klasörünün içinden çalıştırın. GitHub deposunun
kökündeyseniz önce:

```sh
cd bolumler/b01/ornek-01
```

Bağımsız B01 paketinde `b01/ornek-01` klasörüne geçin. Dosyayı başka bir
klasörden çağırmak çalışma dizinini otomatik olarak değiştirmez.

## Python

Gereksinim: Python 3 ve pandas. Betik paket kurmaz veya veri indirmez.

```sh
python cozum.py
python cozum.py --check
```

İlk komut 18 satırlık özeti, ikincisi ayrıca beklenen değerlerle
karşılaştırmayı verir. Başarılı kontrol mesajı:

```text
DOGRULANDI: 18 kontrol degeri eslesiyor.
```

## R

Standart R kurulumu yeterlidir; ek paket gerekmez.

```sh
Rscript cozum.R
Rscript cozum.R --check
```

R konsolunda çalışma dizini bu klasörken `source("cozum.R")` da özeti
üretir; bu kullanım `--check` kontrolünü başlatmaz. Kontrol için terminal
komutunu kullanın veya sonucu CSV ile karşılaştırın.

## SPSS

1. Kaydedilmemiş başka çalışmanız varsa önce kaydedin.
2. SPSS çalışma dizinini bu `ornek-01` klasörüne ayarlayın. Çalışma dizini
   bu GitHub deposunun köküyse Syntax penceresinde bir kez
   `CD 'bolumler/b01/ornek-01'.` çalıştırın. Zaten örnek
   klasöründeyseniz bu komutu tekrar çalıştırmayın.
3. `analiz.sps` dosyasını açıp tamamını çalıştırın. Dosyayı açmak tek
   başına çalışma dizinini ayarlamaz.
4. Dictionary çıktısında üç değişkeni ve ölçme düzeylerini inceleyin.
5. Frequencies ve Descriptives tablolarını beklenen değerlerle karşılaştırın.

SPSS yüzdeleri 60 ve 40 olarak gösterebilir; CSV'deki oranlar 0.6 ve
0.4'tür. SPSS çıktısının kontrol CSV'siyle karşılaştırılması elledir;
otomatik CSV dışa aktarımı bu pilotun kapsamında değildir.

## Kontrolün sınırı

**R ve SPSS bu hazırlama ortamında çalıştırılmamıştır.** Python kontrolü,
diğer iki yazılımın gerçek çalıştırma testinin yerine geçmez. Bölümün
`DOGRULAMA.md` dosyasında yapılan kontroller listelenir.

Kontrol CSV'si yalnız özgün beş satır içindir. Alıştırmada veri değişirse
aynı kontrolün geçmesi beklenmez. Python/R betikleri boş veri, eksik hücre
ve geçersiz program etiketinde bilerek durur; bu bir eksik veri analiz
yöntemi değildir. SPSS betiği aynı otomatik girdi kontrollerini uygulamaz;
veri sözlüğü ve frekans çıktısı ayrıca incelenmelidir.

[Açıklamalı çözüm](cozum.md) · [Alıştırmalar](../alistirmalar.md) ·
[Yanıtlar](../cozumler.md)

## Sözdizimi başvuruları

IBM SPSS Statistics: *Subcommands for TYPE=TXT (GET DATA command)* ve
*Variable measurement level*. Kontrol tarihi: 9 Eylül 2026.

- https://www.ibm.com/docs/en/spss-statistics/cd?topic=data-subcommands-typetxt-get-command
- https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=view-variable-measurement-level