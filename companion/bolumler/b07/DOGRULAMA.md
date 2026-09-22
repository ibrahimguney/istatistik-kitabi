# B07 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: on yapay ikili yanıt ve ayrı p=0,40, n=50
Bernoulli modelinde 10000 tekrar; tohum 2026.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3 ve Matplotlib 3.10.8 ile
  `python cozum.py --check --grafik` çalıştı. 21 kontrol değeri 1e-9
  mutlak/bağıl toleransla eşleşti; iki panelli grafik üretildi.
- Kitabın Bölüm 7 Python listesi ayrı çalıştırıldı: on yanıt, 10000
  satırın başarı toplamı ve örneklem oranları ortak CSV'lerle tam eşleşti.
  R kaynağından çıkarılan yanıt dizisi de aynı; R benzetim tasarımının
  10000 tekrar ve p=0,40 olduğu kaynak üzerinden kontrol edildi.
- Sözlüğün alanları iki CSV'nin sütunlarıyla aynı. Kaynak veri çerçeveleri
  hesaplamada değiştirilmedi; iki dosyanın satır sırasının ters çevrilmesi
  aynı sonuç tablosunu verdi. Üretim kaydındaki iki dosya özeti doğrulandı.
- Referans sayılar çözümün NumPy hesabından ayrı olarak `statistics` ve
  `Fraction` ile hesaplandı. Ampirik MSE, B bölenli varyans ve ampirik
  yanlılığın karesi toplamına tam kesirlerle eşit bulundu.
  V_B=((B−1)/B)s² ilişkisi de tam olarak doğrulandı.
- Binom(50,0,40) modelinin 51 olası başarı sayısı için olasılıklar tam
  kesirlerle toplandı: toplam 1, örneklem oranının merkezi 2/5 ve MSE'si
  3/625=0,0048. Bu kontrol benzetim çekimlerinden bağımsızdır.
- İleri alıştırmadaki T=(X+1)/52 için aynı tam dağılımdan MSE=301/67600
  bulundu; 0,0048'den küçük olduğu doğrulandı. Sonuç yalnız bu model
  noktasına aittir; her p için üstünlük iddiası yapılmadı.
- Ampirik merkez farkı altı kuramsal Monte Carlo SE içinde, ampirik MSE
  kuramsal MSE'nin yüzde 5'i içinde bulundu. Bu yakınlık kontrolleri
  sabit CSV'nin 1e-9 özet eşleşme testinden ayrı tutuldu.
- n=25→400 hacim değişiminde yaklaşık SE'nin dörtte birine; n=50→200
  değişiminde kuramsal SE'nin yarısına inmesi ayrıca kontrol edildi.
- Geçerli sınır durumları denendi: bütün yanıtlar 0 veya 1 olduğunda
  yerine-koyma SE'si 0 çıktı. İki benzetim tekrarında başarı sayıları
  0 ve 50 iken MSE 0,26 olarak doğrulandı. Bu sınırları eksik veya
  geçersiz diye reddetmek yerine yorum sınırlamaları açıklandı.
- 20 hatalı girdi reddedildi. Yanıt tarafında yedi durum: boş veri,
  yanlış sütun adı, eksik, ikili olmayan tam sayı, kesir, metin, mantıksal
  değer. Benzetimde 13 durum: boş, tek tekrar, yanlış sütun sırası,
  eksik başarı, sonsuz başarı, negatif başarı, 51 başarı, kesirli başarı,
  yinelenen kimlik, atlanan kimlik, metin başarı, sıfır kimlik, kesirli kimlik.
- Örnek klasörü geçici başka bir klasöre kopyalandı; `--check --grafik`
  orada da çalıştı. `python uret.py` çıktısı ortak benzetim CSV'siyle byte
  düzeyinde aynı oldu. İkinci çağrı üzerine yazmayı reddetti, dosya
  değişmedi. `../` içeren çıktı yolu reddedildi.
- Bir yanıtın, bir benzetim başarı sayısının ve bir referans kontrol
  değerinin değiştirilmesi; referans satır sırasının ters çevrilmesi,
  ayrı ayrı sıfırdan farklı `--check` çıkış kodu verdi.
- Grafik görsel olarak incelendi: sol panelde 0/1 oranları 0,4/0,6,
  sağ panelde 0–1 aralığında ayrık benzetim göreli frekansları ve 0,40
  referans çizgisi görünür. Eksenler ve başlıklar okunur; yoğunluk ile
  göreli frekans ayrımı açıklamada korunur.
- SPSS dosyası ile `.sps.txt` yedeği byte düzeyinde aynı. Yerel belge
  bağlantıları ve manifest SHA-256 değerleri kontrol edildi.

## İncelenen fakat çalıştırılmayanlar

`cozum.R` ve `benzetim.R` kaynak akışı ve ayraç dengesi bakımından
incelendi. Ortak veri çözümüyle yeni R benzetimi ayrı tutuldu.
Bu inceleme R yorumlayıcısında çalışma testi değildir.

SPSS'te iki ayrı CSV'nin açılması, nominal yanıt tanımı, yerine-koyma
SE'sinin açık hesaplanması, B ve B−1 varyansları ile MSE ayrışımı kaynak
üzerinden incelendi. NumPy/R binom üreteci resmi belgelerine başvuruldu;
bağlantılar örneğin README'sindedir. SPSS gerçek çıktısı üretilmedi.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda çalıştırılmadı. R grafiği veya yeni R benzetim
CSV'si, `.sav`/`.spv` çıktısı üretilmedi. Python kontrolünün geçmesi üç
ortamda sonuç eşitliğinin uçtan uca kanıtı değildir.

1. R kurulu bilgisayarda örnek klasöründen `Rscript cozum.R --check --grafik`
   çalıştırın. 21 kontrolü, MSE ayrışımını ve grafiği inceleyin;
   `sessionInfo()` çıktısını kaydedin.
2. Ayrı olarak `Rscript benzetim.R` çalıştırın. Yeni sonuçları kuramsal
   merkez, SE ve MSE çevresinde değerlendirin; eski Python sayılarına
   birebir eşleşme beklemeyin veya referans dosyasını değiştirmeyin.
3. SPSS'te çalışma dizinini örnek klasörü yapıp `analiz.sps` çalıştırın.
   İlk veri için 10 yanıt, 6 olumlu, oran 0,6 ve `se_hat`≈0,154919;
   ikinci için 10000 tekrar ve çözüm tablosundaki sayıları kontrol edin.
   Her aşamadaki satır birimini, varyans bölenini ve yuvarlamayı gözetin;
   SPSS sürümünü kaydedin.
4. Gerçek çalışma sonuçlarını bu kayda ekleyin; değiştirilmiş kod/veri
   için eski kontrol kaydını yeni sonuçların kanıtı saymayın.

## Bütünlük ve yayın

`uretim-kaydi.json` kaynak ve benzetim CSV'lerinin üretim ayrıntıları ile
SHA-256 değerlerini; `MANIFEST.json` kendisi dışındaki B07 dağıtım
dosyalarının özetlerini tutar. Grafik ve SPSS metin yedeği de kapsamdadır.
Dosyalar değişirse ilgili özetler yenilenmelidir. SPSS uzantısı arayüzde
aktarılmıyorsa `.sps.txt` yedeğini aynı klasörde `.sps` adıyla geri oluşturun.

Kitabın LaTeX dosyaları değiştirilmedi; PDF derlemesi yapılmadı.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. B01 arşivleri B07'yi içermez.