# B10 doğrulama kaydı

Tarih: 9 Eylül 2026. Kapsam: tek örneklem t testi özeti ve ayrı güç planı.
**Yayın durumu:** Yerelde hazır; GitHub yüklemesi bütün bölümler tamamlanınca yapılacak.
Ders sürümü Bölüm 10; kapsamlı sürüm Bölüm 11.

## Çalıştırılarak doğrulananlar

- Python 3.13.15, NumPy 2.4.1, pandas 2.3.3, SciPy 1.17.0 ve Matplotlib
  3.10.8 ile `python cozum.py --check --grafik` geçti. 30 değer
  1e-9 mutlak/bağıl toleransla eşleşti.
- Kontrol p-değeri ve kritik t değerleri merkezi t yoğunluğunun açık
  formülünü sayısal integral/kök bulmayla değerlendirerek hesaplandı.
- Güç ayrıca T=(Z+λ)/√(V/df) temsiliyle denetlendi: bağımsız normal Z ve
  ki-kare V altında iki koşullu normal kuyruğun toplamı V üzerinden
  integre edildi. Referans üretiminde `stats.nct` kullanılmadı.
  n=2–33 güçleri %80 altında, n=34 gücü %80 üstünde bulundu.
- Kitaptaki Python bloğu çalıştırıldı; t, p, güven aralığı ve n=34 gücü
  eşleşti. Kitaptaki R bloğunun gözlenen özet atamaları ve planlama
  parametreleri kaynak üzerinden karşılaştırıldı.
- İki CSV'nin sütun sırası veri sözlüğüyle, bütünlük özetleri kaynak
  kaydıyla eşleşti. Hesaplama girdi veri çerçevelerini değiştirmedi.
- 37 geçersiz CSV girdisi reddedildi: iki dosya için boş/iki satırlı,
  yanlış sütun adı/sırası, fazla sütun; hacim=1/2,5/eksik/sonsuz/mantıksal/metin,
  sıfır/negatif standart sapma ve α=0/1/5; ayrıca sıfır plan farkı ve
  hedef güç=0,01/0,05/1/eksik. Güç yardımcı işlevinin üç geçersiz girdisi de reddedildi.
- Gözlenen hacmi 100 yapmak plan sonuçlarını değiştirmedi; plan farkını
  2,5 yapmak gözlenen test sonuçlarını değiştirmedi. Konum kaydırma ve
  pozitif ölçek değişiminde t/p/d ve güven aralığı dönüşümleri kontrol edildi.
- Üç etki büyüklüğü ve üç α/hedef bileşimi olmak üzere dokuz planda ikili
  arama, küçükten büyüğe tam sayı taramasıyla aynı en küçük hacmi verdi.
  Her çözümde hedefe ulaşıldığı ve bir önceki hacmin yetersizliği denetlendi.
- n=2, 25, 33, 34, 100 için sıfır etkide ret olasılığı α'ya eşleşti;
  etki işaretini çevirme çift yönlü gücü değiştirmedi. SPSS'te kullanılan
  iki kuyruk formülü aynı SciPy dağılımı üzerinden ayrıca karşılaştırıldı;
  bu kontrol SPSS yorumlayıcısı testi değildir.
- En küçük hacim 2 olduğunda önceki hacmin gücü NaN olarak bırakıldı.
  Çok küçük etki için 10000 gözlem arama sınırının aşılması açık hata üretti.
- Alıştırma sonuçları denetlendi: küçük etki için n=128, %90 hedef için
  n=44 ve α=0,01 altında %80 hedef için n=51 bulundu.
- Örnek başka bir geçici klasöre kopyalandı; Python kontrolü ve grafik
  üretimi geçti. Değişmiş test girdisi, değişmiş plan girdisi, yanlış kontrol
  değeri ve ters sıralı kontrol tablosu ayrı ayrı başarısız çıkış üretti.
  Kaynak paket dosyaları değişmedi.
- PNG açılarak incelendi; iki etki eğrisi, %80 hedefi ve n=34 işareti
  okunabilir. Grafik açıklaması teorik güç ile gözlenen p-değerini ayırır.

## İncelenen fakat çalıştırılmayanlar

- R kodunun parantez dengesi, iki CSV başvurusu, 30 satırlık çıktı sırası,
  `power.t.test` tek örneklem/çift yön/`strict=TRUE` seçenekleri incelendi.
- IBM belgelerindeki `NCDF.T`, dağılım işlevleri ve `LOOP–END LOOP`
  sözdizimiyle SPSS kaynak kodu karşılaştırıldı. Bağlantılar örneğin
  README'sindedir. `analiz.sps` ile `analiz.sps.txt` byte düzeyinde aynıdır.

## Bekleyen doğrulamalar

R ve IBM SPSS bu ortamda bulunmuyor. Betikleri gerçek yorumlayıcılarında
çalıştırılmadı; R grafiği veya SPSS `.sav`/`.spv` çıktısı üretilmedi.
Python'un geçmesi üç yazılımın uçtan uca eşitliği anlamına gelmez.

1. Örnek klasöründe `Rscript cozum.R --check --grafik` çalıştırın;
   30 kontrolün eşleştiğini doğrulayın ve `sessionInfo()`yu kaydedin.
2. SPSS'te iki CSV'nin tek satır ve geçerli olduğunu elle kontrol edin,
   örnek klasörünü çalışma dizini yapıp `analiz.sps` çalıştırın. Dört LIST
   tablosunu kontrol CSV'siyle karşılaştırın; sürümü ve sonucu kaydedin.
3. Ham veri, bağımsızlık, normallik, önem eşiği, kümelenme ve kayıpları gerçek
   araştırma bağlamında ayrıca değerlendirin; bu özet bunları doğrulamaz.

## Bütünlük ve yayın

`MANIFEST.json`, kendisi dışındaki B10 dağıtım dosyalarının SHA-256
özetlerini listeler. Dosyalar değişirse manifest ve ilgili doğrulama kaydı
yenilenmelidir. `.sps` dosyası taşınmazsa metin yedeğinden geri getirilebilir.
Yeni ZIP, commit veya GitHub yüklemesi yapılmadı. Kitabın LaTeX dosyaları
bu paket için değiştirilmedi; PDF derlemesi gerekmedi.