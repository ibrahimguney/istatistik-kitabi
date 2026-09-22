# Bootstrap doğrulama kaydı

Tarih: 10 Eylül 2026. Kapsam: kapsamlı sürüm Bölüm 9'un iki yapay örneği.
Yerel paket hazırlandı; GitHub'a veya kullanıcının bilgisayarına yükleme
bu kayıtla doğrulanmış değildir.

## Çalıştırılarak doğrulananlar

- Python 3.13.15 ile `python -S -B cozum.py --check`: 26 referans değeri
  10^-9 mutlak/bağıl toleransla eşleşti. Temel hesap üçüncü taraf paket kullanmaz.
- Referanslar çözüm fonksiyonundan kopyalanmadı: bootstrap toplam dağılımı
  sayım evrişimi ve rasyonel aritmetikle; permütasyonlar altı bitlik maskeler
  üzerinden bağımsız hesaplandı. NumPy varyansı ve yüzdelikleri ayrıca eşleşti.
- 3.125 benzersiz kimlik dizisi, 20 benzersiz atama, bir tek yönlü uç atama
  doğrulandı. Veri ve plan girdileri hesaplama tarafından değiştirilmedi.
- On iki hatalı girdi reddedildi: eksik satır, yanlış başlık, NaN, sonsuz,
  boş hücre, yinelenen kimlik, kesirli kimlik, sınır üstü sayı, yanlış grup,
  eksik bootstrap planı, yinelenen plan sırası ve geçersiz permütasyon.
- Dört girdi CSV'sinin satırları ters çevrilince sonuçlar değişmedi.
- Bütün bootstrap gözlemlerine 10 ekleme alıştırması sayısal olarak sınandı.
- Geçici başka bir klasöre kopyalanan çözüm 26 kontrolü geçti. Değiştirilmiş
  veri ve değiştirilmiş referans ayrı ayrı sıfırdan farklı çıkış kodu verdi.
- `uret.py` iki planı byte düzeyinde aynı üretti; mevcut hedefe yazmayı reddetti.
- `--grafik` çalıştı; iki panelli PNG görsel olarak incelendi.
- `--benzetim` çalıştı: Python SE 1,8026769169, yüzdelikler 2,6 / 9,2.
  Bu rastgele çıktı 26 tam sayım referansına dahil değildir.
- `analiz.sps` ve `analiz.sps.txt` byte düzeyinde aynı.

## Çalıştırılmayanlar

Rscript, IBM SPSS ve PSPP bu ortamın PATH'inde bulunmuyor. R ve SPSS
betikleri çalıştırılmadı; R/SPSS sonuç eşitliği doğrulanmadı. Kaynak incelemesi
çalışma testi değildir. SPSS'in LOOKUP/AGGREGATE akışı ve type 7 sıra hesabı
incelendi; IBM/R belgeleri örnek README'sindedir. `.sav`/`.spv` çıktısı yoktur.

## Kalan adımlar

1. R'de örnek klasöründen `Rscript cozum.R --check` çalıştırıp 26 değeri ve
   `sessionInfo()` çıktısını kaydedin.
2. SPSS'te örnek klasörünü çalışma dizini yapıp betiği çalıştırın. İki LIST
   tablosundaki 15+11 ölçüyü referanslarla karşılaştırıp sürümü kaydedin.
3. Aktarım sonrası manifesti yeniden denetleyin. Yeni çıktılar veya dosya
   değişiklikleri mevcut manifesti güncelleme gerektirir; eski kayıt yeni
   kodun doğrulandığı anlamına gelmez.

`MANIFEST.json` kendisi dışındaki paket dosyalarının SHA-256 özetlerini içerir.
Kitabın LaTeX kaynakları değiştirilmedi; PDF derlemesi yapılmadı.