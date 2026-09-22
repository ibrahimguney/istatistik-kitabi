# B12 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: (30,10)/(20,20) frekans tablosu,
düzeltmesiz Pearson bağımsızlık testi. Ders sürümü Bölüm 12; kapsamlı Bölüm 13.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ve Matplotlib
  3.10.8 ile `python cozum.py --check --grafik` geçti. 32 değer
  1e-9 mutlak/bağıl toleransla eşleşti.
- Referans χ² tam kesir aritmetiğiyle 16/3 olarak hesaplandı; df=1 için
  p, `math.erfc(sqrt(chi2/2))` normal-kare özdeşliğiyle üretildi.
  `chi2_contingency` sonuçları referans CSV'sine kopyalanmadı.
- Kitaptaki Python bloğu ayrıca çalıştırıldı; gözlenen/beklenen tablo,
  katkılar, Pearson artıkları, χ², p, df ve V eşleşti. Kitaptaki R
  matrisinin dört girdisi, satır yönü ve düzeltme seçimi kaynakta karşılaştırıldı.
- Veri sözlüğünün sütun sırası CSV ile, SHA-256 kaynak kaydıyla eşleşti.
  Hesaplama özgün veri çerçevesini değiştirmedi.
- 21 geçersiz girdi reddedildi: eksik/fazla satır, yanlış sütun adı/sırası,
  fazla sütun; eksik etiket/frekans, bilinmeyen kategori, yinelenen hücre;
  negatif/kesirli/sonsuz/metin/mantıksal frekans; boş satır/sütun ve sıfır tablo.
- Ayrı bir geçerli sayım tablosu olan (3,1)/(2,2), en küçük beklenen
  frekans 1,5 olduğu için bu pilotun Pearson koşulundan geçemedi.
- Beş ek tabloda χ² açık formülle, p normal-kare özdeşliğiyle karşılaştırıldı.
  En küçük beklenenin tam 5 olması ve gözlenen sıfır hücre içeren fakat
  pozitif kenar toplamlı tablo da kontrol edildi.
- CSV satır sırasını değiştirmek sonuç tablosunu değiştirmedi. Grup veya
  sonuç etiketlerini değiştirmek χ²/p/V'yi korudu; artık hücreleri etiketlerle
  birlikte yer değiştirdi. Satır oranları her satırda 1'e toplandı.
- Sayımları ikiye katlamak χ²'yi ikiye, Pearson artıklarını √2 katına
  çıkardı; V ve satır oranları değişmedi, p küçüldü. Kayıt kopyalamanın
  bağımsız gözlem yaratmadığı alıştırma çözümünde belirtildi.
- (25,15)/(25,15) tablosunda χ²=0, p=1, V=0 ve sıfır artıklar doğrulandı;
  bu tablo için grafik üretimi de başarıyla çalıştı.
- Pearson artıklarının kareleri katkılarla eşleşti. Düzeltilmiş
  standartlaştırılmış artıkların farklı sayılar verdiği kontrol edildi.
  Yates düzeltmesi açıldığında p'nin değiştiği ayrıca doğrulandı.
- SPSS'te kullanılan kenar toplamı/beklenen frekans mantığı Python
  gruplamasıyla denetlendi; bu işlem SPSS yorumlayıcısı testi değildir.
- Paket geçici başka bir klasöre kopyalandı; Python kontrolü ve grafik
  üretimi geçti. Değişmiş frekans, seyrek tablo, yanlış kontrol değeri ve
  ters sıralı kontrol tablosu ayrı ayrı başarısız çıkış üretti.
  Kaynak paket dosyaları değişmedi.
- PNG açılarak incelendi; yüzdeler, kategori adları ve işaretli artık
  etiketleri okunabilir. Grafik açıklaması renkleri ve artık türünü açıklar.

## İncelenen fakat çalıştırılmayanlar

- R kodunun parantez dengesi, CSV sıralaması, `correct=FALSE`, `residuals`
  seçimi ve satır öncelikli 32 sonuç düzeni kaynak üzerinden incelendi.
- SPSS CROSSTABS hücre seçenekleri, WEIGHT, AGGREGATE ve SIG.CHISQ
  sözdizimi IBM belgeleriyle karşılaştırıldı. Başvurular örneğin README'sindedir.
  Betikte ağırlık kapatma ve sayım ağırlığı ile ham satır sayısı ayrımı incelendi.
- `analiz.sps` ile `analiz.sps.txt` byte düzeyinde aynıdır.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda bulunmuyor. Kodları gerçek yorumlayıcılarında
çalıştırılmadı; R grafiği veya SPSS `.sav`/`.spv` çıktısı üretilmedi.
Python'un geçmesi üç yazılımda uçtan uca eşitlik kanıtı değildir.

1. Örnek klasöründe `Rscript cozum.R --check --grafik` çalıştırın;
   32 değerin eşleştiğini doğrulayın, grafiği ve `sessionInfo()`yu kaydedin.
2. SPSS'te girdileri ve beklenen sayı koşulunu elle kontrol edin; çalışma
   dizinini örnek klasörü yapıp `analiz.sps` çalıştırın. LIST ve ağırlıklı
   Crosstabs sonuçlarını kontrol CSV'siyle karşılaştırın. N=80 olduğunu,
   Pearson satırının seçildiğini ve sonunda ağırlığın kapandığını doğrulayın.
3. Satır yüzdesini kontrol dosyasının 0–1 oranıyla karşılaştırırken 100
   çarpanını ve ekran yuvarlamasını dikkate alın; sürümü ve gerçek sonucu kaydedin.
4. Gözlem bağımsızlığı, örnekleme tasarımı ve kategori tanımları ayrıca
   incelenmelidir; beklenen frekans kontrolü bunların yerine geçmez.

## Bütünlük ve yayın

`MANIFEST.json`, kendisi dışındaki B12 dağıtım dosyalarının SHA-256
özetlerini listeler. Dosyalar değişirse manifest ve ilgili doğrulama kaydı
yenilenmelidir. `.sps` görünmüyorsa `.sps.txt` yedeğinden geri getirilebilir.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Kitabın LaTeX dosyaları
bu paket için değiştirilmedi; PDF derlemesi gerekmedi.