# Örnek 01 — Çözüm ve yorum

## 1. Çerçeve ve seçilen kimlikler

N=12; sınıfların her birinde N_h=4 birim bulunur. Toplam örneklem hacmi
n=6; tabakalı tasarımda her sınıftan n_h=2 kişi seçilir.

| Tasarım | Seçilen kimlikler (artan sırada) | Sınıf frekansları |
|---|---|---|
| Basit rastgele | 1, 3, 6, 8, 11, 12 | 2 / 2 / 2 |
| Tabakalı | 1, 4, 7, 8, 11, 12 | 2 / 2 / 2 |

Kimlik sırası seçim sırası değildir; karşılaştırmayı kolaylaştırmak için
sıralanmıştır. Bu sonuçlar kayıtlı Python seçimine aittir. R kendi yeni
seçimini yaparsa kimlikler değişebilir; ortak CSV'yi okursa aynı kayıtları çözer.

**Basit seçimdeki 2/2/2 dağılımı bu çekimin sonucudur, garanti değildir.**
Örneğin 1,2,3,4,5,6 geçerli bir altı kişilik basit örneklemdir ve sınıf
sayıları 4/2/0'dır. Tabakalı tasarımda böyle bir örneklem mümkün değildir.

## 2. Dahil edilme olasılığı ve ağırlık

Basit rastgele, geri koymasız seçimde π_i=n/N=6/12=**0,5**.
Tabakalı seçimde π_i=n_h/N_h=2/4=**0,5**. Her iki tasarımda temel
örnekleme ağırlığı w_i=1/π_i=**2**.

Bu π, belirli bir kişinin altı kişilik örneğe **en az bir kez dahil edilmesi**
olasılığıdır. Tek bir ilk çekilişte seçilme olasılığı 1/12 ile karıştırılmaz.
Geri koyma olmadığından aynı tasarımda kimlik tekrar etmez.

Her örneklemde altı ağırlığın toplamı 6×2=**12** olur. Bu, altı kişi yerine
12 gerçek kişiden veri alındığı anlamına gelmez. Tam çerçeve, eksiksiz
uygulama ve yanıtsızlık yokluğu varsayımları altında ağırlık toplamı çerçeve
büyüklüğünü temsil eder. Bu özellik bütün tasarımlar için sabit toplam garantisi değildir.

## 3. Neden tasarımlar aynı değil?

Basit tasarımda 12 içinden 6 kişilik **924** farklı sırasız örneklem mümkündür.
Tabakalı tasarımda her sınıftan 4 içinden 2 seçim yapılır: 6×6×6=**216**.
Dengeli sınıf sayılı basit örneklemler de 216 tanedir; olasılık
216/924=**18/77≈0,233766**. Basit seçimi dengeli çıkana kadar tekrar etmek
özgün basit rastgele tasarım değildir; bu pilotun eşit tabakalı koşullu
seçim kümesine geçilmiş olur.

İki tasarımda tek kişilik dahil edilme olasılıkları aynı olsa da örneklem
kümeleri ve birlikte seçilme olasılıkları farklıdır. Dolayısıyla aynı
bireysel ağırlıklar aynı tasarım veya aynı standart hata demek değildir.

## 4. Yorumun sınırı

Bu dosyada puan, gelir veya süre gibi bir sonuç değişkeni yoktur. Kimliklerin
ortalaması anlamlı bir başarı ölçüsü değildir; bu nedenle ağırlıklı not
ortalaması veya standart hata uydurulmaz. Uygulama yalnız seçim ve tasarım
ağırlıklarına odaklanır. Gerçek analizde tasarım bilgisi standart hata
hesabına da taşınmalıdır.

> Üç sınıfta dörder yapay birim bulunan çerçeveden, basit rastgele ve
> sınıfa göre tabakalı tasarımlarla altışar birim geri koymadan seçildi.
> Her iki tasarımda dahil edilme olasılığı 0,5, temel ağırlık 2 ve seçilen
> ağırlıkların toplamı 12'dir. Tabakalı tasarım her sınıftan iki birimi
> garanti eder; basit seçimde gözlenen aynı denge yalnız bu çekime aittir.

Bir sınıf çerçevede yoksa o sınıftaki hedef birimlerin seçilme olasılığı
sıfırdır. Kalan listeyi rastgele seçmek veya ağırlıkları toplamak bu kapsam
hatasını ortadan kaldırmaz.