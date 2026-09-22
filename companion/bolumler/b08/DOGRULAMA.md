# B08 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: n=25, ortalama=72, s=10 özetinden yüzde 95
ve yüzde 99 iki taraflı t güven aralıkları. Ham gözlem üretilmedi.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ve
  Matplotlib 3.10.8 ile `python cozum.py --check --grafik` çalıştı.
  19 kontrol değeri 1e-9 mutlak/bağıl toleransla eşleşti; grafik üretildi.
- Kitabın Bölüm 8 Python listesi ayrı çalıştırıldı: üç özet girdi ve
  yüzde 95 aralık paketle eşleşti. R kaynağındaki hacim=25, ortalama=72,
  standart sapma=10 değerleri ayrı olarak çıkarılıp doğrulandı.
- Veri sözlüğünün üç alanı CSV ile aynı. Hesaplamalar girdi veri
  çerçevesini değiştirmedi. Kaynak kaydındaki SHA-256 değeri doğrulandı.
- Referans kritik değerler `stats.t.ppf` kullanılmadan, Student t
  yoğunluğunun gamma fonksiyonlu ifadesi, sayısal integral ve kök bulmayla
  hesaplandı. Aynı SciPy kurulumunda farklı bir hesap yolu kullanıldı;
  bu kontrol R/SPSS çalışma testinin yerine geçmez.
- Yüzde 90/95/99 kritik değerlerinin negatif ve pozitif sınırları arasında
  t yoğunluğu ayrıca integre edildi; alanlar ilgili güven düzeyleriyle
  1e-10 mutlak tolerans içinde eşleşti. `stats.t.interval` çıktılarıyla
  da sınırlar karşılaştırıldı; bu ikinci SciPy çağrısı bağımsız bir yazılım testi değildir.
- Aralık merkezlerinin 72 olduğu, genişliğin hata payının iki katı olduğu
  ve yüzde 99 aralığın yüzde 95'i, onun da yüzde 90'ı kapsadığı doğrulandı.
  Kitabın dört ondalıkla verilen sınırlarıyla yuvarlama uyumu kontrol edildi.
- Ortalama +5 olduğunda sınırların +5 kaydığı; ortalama ve s iki katına
  çıktığında sınırların iki katına çıktığı; s yarıya indiğinde genişliğin
  tam yarıya indiği ayrıca doğrulandı.
- n=100 ve s=10 için SE=1, df=99 ve yüzde 95 sınırlar yaklaşık
  70,015783/73,984217 bulundu. Kritik t de değiştiği için genişliğin
  eski genişliğin yarısından biraz küçük olduğu kontrol edildi.
- 1,96 ile hesaplanan yaklaşık normal aralığın t aralığından dar olduğu,
  negatif ortalamanın geçerli kaldığı ve n=2 için hesap yapılabildiği denetlendi.
- 16 hatalı özet reddedildi: boş veri, iki satır, yanlış sütun adı, yanlış
  sütun sırası, fazla sütun, eksik ortalama, sonsuz s, n=0, n=1, kesirli n,
  s=0, negatif s, metin n, mantıksal n, negatif n ve sonsuz n.
- Sekiz hatalı güven düzeyi reddedildi: 0, 1, 95, negatif değer, NaN,
  sonsuz, mantıksal değer ve metin. Yüzde gösterimiyle olasılık gösterimi
  karıştırıldığında sessizce yanlış aralık üretilmedi.
- Örnek klasörü geçici başka bir klasöre kopyalandı; `--check --grafik`
  orada da çalıştı. Değiştirilmiş ortalama, değiştirilmiş referans değeri
  ve ters sıralanmış referans tablosu ayrı ayrı sıfırdan farklı çıkış kodu verdi.
- Grafik görsel olarak incelendi: iki güven düzeyi, dört uç değeri,
  72 merkezi ve yatay puan ekseni okunur. İki aralık ortak ölçekte;
  yüzde 99 çizgisi daha geniş. Grafik ham veri veya kapsama benzetimi gibi sunulmadı.
- SPSS dosyası ve `.sps.txt` yedeğinin byte eşliği, yerel belge
  bağlantıları ve manifest SHA-256 değerleri doğrulandı.

## İncelenen fakat çalıştırılmayanlar

R kodunun ayraç dengesi, `qt((1+duzey)/2, df=n-1)` kullanımı, giriş
kontrolleri, 19 satırlık çıktı düzeni ve grafik kaynak üzerinden incelendi.
Bu bir R yorumlayıcısı testi değildir.

SPSS kodunda `IDF.T`, özetlerden SE/serbestlik hesabı ve iki LIST tablosu
incelendi. IDF.T imzası IBM'in resmi ters dağılım belgesiyle karşılaştırıldı.
SciPy ve R t dağılımı belgeleri de incelendi; bağlantılar örneğin README'sindedir.
SPSS gerçek çıktısı üretilmedi.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda çalıştırılmadı. R grafiği, `.sav` veya `.spv`
çıktısı üretilmedi. Python kontrolünün geçmesi üç ortamda sonuç eşitliğinin
uçtan uca doğrulandığı anlamına gelmez.

1. R kurulu bilgisayarda örnek klasöründen `Rscript cozum.R --check --grafik`
   çalıştırın. 19 kontrolün ve iki aralığın eşleşmesini inceleyin;
   `sessionInfo()` çıktısını kaydedin.
2. SPSS'te aynı klasörü çalışma dizini yapıp `analiz.sps` çalıştırın.
   Tek özet satırı, n=25, SE=2, df=24 ve yüzde 95/99 aralıklarını kontrol
   edin. Ekran yuvarlamasını dikkate alın; SPSS sürümünü kaydedin.
3. Gerçek çalıştırma sonuçlarını bu kayda ekleyin. Yeni veya değiştirilmiş
   kod için eski doğrulama kaydını kanıt olarak kullanmayın.

## Yorum ve bütünlük sınırı

Bu kontroller aralık hesabının aritmetiğine yöneliktir. Bağımsızlık,
normal modele uygunluk, aykırı değerler veya örnekleme çerçevesi bu tek
özet satırından doğrulanamaz. Yüzde 95/99 için kapsama benzetimi yapılmadı;
“gözlemlenen kapsama oranı” raporlanmıyor. Rastgele işlem ve tohum yoktur.

`kaynak-kaydi.json` girdi ve referans yöntemi ayrıntılarını,
`MANIFEST.json` kendisi dışındaki B08 dağıtım dosyalarının SHA-256
özetlerini içerir. Grafik ve SPSS metin yedeği dahildir. Dosya değişirse
ilgili özetler yenilenmelidir. SPSS uzantısı arayüzde aktarılmıyorsa
`.sps.txt` yedeğini aynı klasörde `.sps` adıyla geri oluşturun.

Kitabın LaTeX dosyaları değiştirilmedi; PDF derlemesi yapılmadı.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. B01 arşivleri B08'i içermez.