# B03 — Alıştırma çözümleri

1. Bir satır bir yapay öğrenci gözlemidir; değişken çalışma süresidir,
   sayısal/oran ölçeğindedir ve birimi saattir. 0 gerçek bir süre değeri
   olabilir; eksik kayıtla aynı değildir. Eksik süre 0 ile doldurulmaz.
2. Toplam 25; ortalama 5; medyan 3; mod 3 (iki kez görülür).
3. Kareler toplamı 82; örneklem varyansı 82/4=20,5 saat²; standart sapma
   √20,5≈4,527693 saat. Beş kayıt sonlu evren olarak tanımlanırsa evren
   varyansı 82/5=16,4 saat². Paket ilkini hesaplar.
4. Beş sayı özeti (2;3;3;4;13); IQR=1; sınırlar 1,5 ve 5,5.
   Yalnız 13 aykırı işaretlenir; sınırlar üzerindeki değerler işaretlenmez.
5. Bıyıklar sınırlar içinde kalan en uç gözlemlere uzanır: 2 ve 4.
   Üst bıyık 4'tür fakat maksimum 13'tür. Maksimum bu grafikte ayrı noktadır.
6. Frekanslar 1/3/0/0/1. Tam 3 ikinci sınıfa, tam 15 son sınıfa girer.
   Son sınıf sağdan kapalıdır; toplam frekans gözlem sayısına eşittir.
7. Kalan veri 2,3,3,4: ortalama 3, medyan 3. Ortalama 2 azalır, medyan aynı
   kalır. Kayıt hatasına veya dışlama kuralına dair ayrı kanıt gerekir;
   bu hesap tek başına silme gerekçesi değildir.
8. Yeni veri 2,3,3,4,23: ortalama 7, medyan 3, örneklem varyansı 80,5,
   standart sapma yaklaşık 8,972179. Q1=3, Q3=4, IQR=1; sınırlar yine
   1,5/5,5. Yalnız 23 işaretlenir. Histogram sağ ucu 24 olur; 23 kaybolmaz.
9. Yeni veri 4,5,5,6,15: ortalama 7, medyan 5; standart sapma değişmez
   (yaklaşık 4,527693). Q1=5, Q3=6, IQR=1; sınırlar 3,5 ve 7,5.
   15 işaretlenir. Genel duyarlılık alanı hâlâ tam 13'ü dışlama senaryosudur;
   bu yeni verideki 15'i kendiliğinden çıkarmaz.
10. Dakikalar 120,180,180,240,780: ortalama 300, medyan 180; varyans
    20,5×60²=73800 dakika²; standart sapma 60√20,5≈271,661554 dakika;
    IQR=60 dakika. Q1=180, Q3=240; sınırlar 90 ve 330. Birim değişince
    `saat` etiketiyle rapor verilmez. Paket girdi sütunu saat beklediği için
    dönüşümü ayrı bir hesapta yapın, referans CSV'ye kaydetmeyin.
11. Bütün değerler 13 ise Q1=Q3=13, IQR=0, varyans=0, aykırı sayısı=0.
    Sınıra eşit olmak dışına çıkmak değildir. 13'ler çıkarılırsa hacim 0;
    ortalama ve medyan tanımsızdır (Python NaN, R NA). 0 diye raporlanamaz.
12. Örnek rapor: “Beş yapay gözlemde ortalama çalışma süresi 5 saat
    (s=4,53), medyan 3 saat (IQR=1) bulundu. 13 saatlik kayıt 1,5 IQR
    kuralıyla işaretlendi; varsayımsal olarak çıkarıldığında ortalama
    3 saate inerken medyan değişmedi. Bu duyarlılık karşılaştırması bir
    silme kararı değildir ve yapay örnek gerçek öğrenci evrenine genellenemez.”

## Dönüşümleri kodla kontrol etme

Bu kodları `ornek-01` çalışma dizininde çalıştırın. Özgün CSV değişmez.
Python'da 8 ve 9. sorular:

```python
import pandas as pd
from cozum import hesapla

veri = pd.read_csv("veri.csv")
degistirilmis = veri.copy()
degistirilmis.loc[degistirilmis["saat"] == 13, "saat"] = 23
print(hesapla(degistirilmis))
print(hesapla(veri.assign(saat=veri["saat"] + 2)))
```

R'de aynı karşılaştırma (R çalışma testi burada yapılmadı):

```r
source("cozum.R")
degistirilmis <- veri
degistirilmis$saat[degistirilmis$saat == 13] <- 23
print(hesapla(degistirilmis))
print(hesapla(transform(veri, saat = saat + 2)))
```

Dakika dönüşümünü ayrı sayısal vektörde yapın; Python'da `dakika = veri["saat"] * 60`,
R'de `dakika <- veri$saat * 60`. Python'da `dakika.var(ddof=1)` ve
`dakika.std(ddof=1)`; R'de `var(dakika)` ve `sd(dakika)` kullanılır.
`beklenen-sonuclar.csv` yalnız özgün örneğin kontrol dosyasıdır, alıştırma
verisine göre değiştirilmez.