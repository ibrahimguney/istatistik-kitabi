# Öğrenci çalışma alanı

Ana giriş `index.html`; 20 bölüm için kalıcı adresler `bolumler/b01/`–`bolumler/b20/` biçimindedir. Bu numaralar **birleşik kitabın** numaralarıdır. `companion/bolumler` altındaki eski paket adları değiştirilmez.

## Güncelleme

```bash
python scripts/build_student_site.py
python -m http.server 8765
```

Tarayıcıda `http://localhost:8765` açılır. Üretici Python standart kitaplığıyla çalışır. Başlık/paket eşleştirmeleri üreticide, görünüm `web/style.css`, arama ve ders etiketleri `web/app.js` içindedir. Üretilen HTML dosyaları da sürüm kontrolüne alınır; sunucuda derleme gerekmez.

Bölüm sırası `main.tex`, ders düzeyleri `frontmatter/izlence-rotasi-combined.tex` esas alınarak hazırlanmıştır. Kitap sırası veya ders rotası değiştiğinde üreticideki eşleştirmeler birlikte güncellenmelidir. Üretici 20 kaynak bölüm bulunmasını ve indirme dosyalarının varlığını denetler.

## İçerik sınırları

- Ders seçimi konuları gizlemez; temel, destek, ileri okuma, uygulama ve tekrar düzeylerini gösterir.
- 3, 16, 17 ve 19. bölümlerde bağımsız indirme paketi eşleştirilmemiştir. Sayfaları bölüm kaynağına ve mevcut okuma başlıklarına yönlendirir.
- 14 ve 15. bölümler aynı korelasyon/regresyon paketini paylaşır. `b10` paketi 10 ve 11. bölümlerde kullanılır.
- Ayrıntılı uygulama rehberleri ve alıştırmalar GitHub'ın okunabilir dosya görünümünde açılır. Bu sürüm tam metin HTML kitap değildir.
- R/Python/SPSS kodları değiştirilmedi ve bu web düzenlemesinde yeniden çalıştırılmadı. Orijinal doğrulama kayıtları sayfalardan erişilebilir.
- PDF dosyası varsayılmaz; “Yayımlar” proje Releases sayfasına gider.
- İzleme, analitik, harici font veya çalışma zamanında üçüncü taraf JavaScript kullanılmaz.

## GitHub Pages

Mevcut Pages yayını `main` dalının kökünden yapılıyorsa bu değişiklikler birleştirildiğinde kökteki `index.html` açılır. Farklı bir yayın kaynağı kullanılıyorsa Pages ayarı ayrıca kontrol edilmelidir. `.nojekyll` statik dosyaların Jekyll işlemine gerek duymadan sunulmasını sağlar. Göreli bağlantılar `/istatistik-kitabi/` alt yoluyla uyumludur.
