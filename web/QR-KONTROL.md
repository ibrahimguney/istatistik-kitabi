# Bölüm sonu karekodları

23 Eylül 2026 güncellemesi, birleşik kitabın 20 ana bölümünü kapsar.

`frontmatter/bolum-paketleri.tex` içindeki `\bolumbaglantisi` makrosu bölüm sayacından iki basamaklı numarayı üretir. Örnek: bölüm 3 için `https://ibrahimguney.github.io/istatistik-kitabi/bolumler/b03/index.html`. QR, tıklanabilir başlık ve basılı URL aynı hedefi kullanır. Kaynak LaTeX bağlantısı ikincil bağlantı olarak korunur.

## Prism'de uygulanması

1. GitHub'daki güncel `frontmatter/bolum-paketleri.tex` dosyasını Prism projesine aktarın veya projenin mevcut GitHub eşitleme yöntemiyle alın.
2. Kitabı yeniden derleyin ve yeni PDF'yi indirin. Önceden indirilmiş veya basılmış PDF'lerdeki karekodlar kendiliğinden değişmez.
3. Yeni PDF'den 3, 16, 17 ve 19. bölüm karekodlarını telefon kamerasıyla okutun. Adresin ilgili `bolumler/bNN/index.html` sayfasını açtığını kontrol edin.

## Kontrol kapsamı

- `main.tex` sırasındaki 20 bölümün her birinde tek bölüm bağlantısı bulundu; kaynak yolları ve 20 öğrenci sayfası eşleştirildi.
- Gerçek QR makrosu kitabın 152,4 × 228,6 mm sayfa boyutu ve 17 mm yatay kenar boşluklarıyla ayrı bir 20 sayfalık XeLaTeX kontrol belgesinde derlendi. Ortamda kitap fontu bulunmadığından kontrol belgesinde DejaVu kullanıldı; tam kitap derlemesi yapılmadı.
- Kontrol PDF'sindeki 20 karekod görüntüden çözüldü ve tıklanabilir PDF hedefleriyle eşleştirildi.
- 20 canlı bölüm adresinin HTTP yanıtı, bölüm numarası ve mobil viewport etiketi kontrol edildi.
- CSS'de 850 ve 560 piksel altındaki düzen kuralları mevcut. Bu inceleme gerçek telefon veya mobil tarayıcı görsel testi yerine geçmez.
- Mobil görsel/etkileşim kontrolü tamamlanmadı: tarayıcı eyleminin otomatik onay incelemesi kullanım sınırı nedeniyle çalışamadı. iPhone/Safari'de kamera ile okutma, yatay taşma, indirme ve gezinme kontrolü bekliyor.

Bölüm sırası değiştirilirse portal üreticisinin eşleştirmeleri ve karekodlar birlikte yeniden kontrol edilmelidir.
