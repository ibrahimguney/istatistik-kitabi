# Örnek 01 — Adım adım çözüm

## 1. Merkez

Sıralı veri: 2, 3, 3, 4, 13. Toplam 25, gözlem sayısı 5 olduğundan ortalama
25/5 = **5 saat**. Üçüncü gözlem medyandır: **3 saat**. En sık değer de 3'tür
(iki gözlem); burada mod ve medyanın eşitliği genel bir kural değildir.

## 2. Yayılım

Ortalamadan sapmalar −3, −2, −2, −1, 8; kareleri 9, 4, 4, 1, 64'tür.
Kareler toplamı **82**. Örneklem varyansı 82/(5−1) = **20,5 saat²**;
örneklem standart sapması √20,5 = **4,527692569 saat**. Açıklık 13−2 = 11 saat.
Varyansın birimi saat², standart sapmanın birimi saattir.

Bu beş gözlem ayrıca bütün sonlu evren olarak tanımlansaydı evren varyansı
82/5 = 16,4 olurdu. Paket örneklem varyansını raporlar; bu iki bölen karıştırılmaz.

## 3. Çeyrekler ve aykırılık

Type 7 konumu `h=1+(n−1)p` ile Q1 için h=2, Q3 için h=4 elde edilir.
Dolayısıyla Q1=3, Q3=4; beş sayı özeti **(2; 3; 3; 4; 13)**.
IQR = 4−3 = **1 saat**. Alt sınır 3−1,5=**1,5**; üst sınır 4+1,5=**5,5**.
Yalnız 13 üst sınırı aşar. Beş sayı özetinin maksimumu 13 olarak kalır;
13'ün aykırı diye işaretlenmesi onu maksimum olmaktan çıkarmaz.

Kutu 3–4 arasında; medyan 3'te kutunun sol kenarıyla çakışıktır. Bıyıklar
**2 ve 4**'tedir; 1,5 ve 5,5 bıyık uçları değil karşılaştırma sınırlarıdır.
13 ayrı nokta olarak gösterilir. Üst bıyık Q3 ile çakıştığı için uzamış
bir çizgi gibi görünmez.

## 4. Histogram

| Süre aralığı | Frekans | Oran |
|---|---:|---:|
| [0, 3) | 1 | 0,20 |
| [3, 6) | 3 | 0,60 |
| [6, 9) | 0 | 0 |
| [9, 12) | 0 | 0 |
| [12, 15] | 1 | 0,20 |
| Toplam | 5 | 1 |

3 saatlik iki gözlem ikinci sınıftadır. Boş sınıfları gizlememek, 13 saatlik
kaydın diğer dört kayıttan uzaklığını görünür kılar. Eşit genişlikli sınıflarda
grafiğin düşey ekseni frekanstır; yoğunluk veya yüzde değildir.

## 5. Duyarlılık ve kısa rapor

13 dışarıda bırakılırsa 2, 3, 3, 4 kalır: toplam 12, ortalama **3**, medyan
**3**. Ortalama 2 saat azalır; medyan değişmez. Bu karşılaştırma ana CSV'yi
silmez/değiştirmez; bir gözlemi çıkarmanın sonucunu görünür kılar.

> Beş yapay gözlemin çalışma süresi ortalaması 5 saat (s=4,53), medyanı
> 3 saat (IQR=1) bulundu. 13 saatlik gözlem 1,5 IQR kuralıyla işaretlendi.
> Bu gözlem dışarıda bırakıldığında ortalama 3 saate inerken medyan 3 saatte
> kaldı. Çıkarma işlemi yalnız duyarlılık karşılaştırmasıdır; kayıt silme
> veya gerçek öğrenci evrenine genelleme gerekçesi değildir.

Sayısal denetim dosyası `beklenen-sonuclar.csv` toplam 26 kayıt içerir.
R/SPSS çalışma doğrulaması için [doğrulama kaydını](../DOGRULAMA.md) izleyin.