# B01 ilk GitHub yüklemesi — tarihsel not

Güncel birleşik kitap deposu:
https://github.com/ibrahimguney/istatistik-kitabi

**Tarihsel durum:** 9 Eylül 2026 tarihinde bu ortamdan yükleme yapılamadı. GitHub'a
Git bağlantısı `CONNECT tunnel failed, response 403` hatası verdi.
Oturum açılmış GitHub istemcisi de bulunmuyor. Uzak depoda değişiklik yapılmadı;
GitHub'a gönderilmiş bir commit veya sürüm etiketi yoktur.

## Hazır yayın dosyaları

- `github-b01-yukleme.zip`: Açıldığında doğrudan depo kökü yapısını verir.
- `github-b01-paket.json`: 16 yayın dosyasının tam metni ve SHA-256 özetleri.
  Özellikle `.sps` veya ZIP dosyaları çalışma ortamları arasında taşınmazsa
  içeriği kaybetmemek için metin biçiminde korunmuştur.

Paket yalnız depo README'si, bölüm haritası, `.gitignore` ve B01 uygulamasını
kapsar. Kitap PDF'si/LaTeX kaynakları ve diğer veri paketleri dahil değildir.
R/SPSS çalıştırma doğrulaması bekliyor; bu durum yayın README'sinde açıktır.
Bir açık kaynak lisansı eklenmemiştir.

## Tarayıcıdan yükleme

1. ZIP'i indirin ve açın. ZIP dosyasını tek başına depoya yüklemeyin.
2. GitHub'da kendi hesabınızla hedef depoyu açın.
3. Boş depo ekranındaki dosya yükleme bağlantısını veya görünüyorsa
   **Add file → Upload files** seçeneğini kullanın.
4. Açılan ZIP'in **içeriğini** sürükleyin: `README.md`, `BOLUM-HARITASI.csv`,
   `.gitignore` ve `bolumler/`. Üstte fazladan bir `github-yayin` klasörü
   oluşmamalı. `bolumler` klasörünü sürüklemek alt dizinleri korur.
5. Mesajı `B01 pilot uygulama paketini ekle` olarak yazın; mevcut ekrandaki
   commit/onay düğmesiyle değişikliği kaydedin.
6. Depo kökünde README'nin göründüğünü ve B01 bağlantılarının açıldığını
   kontrol edin. `ornek-01` altında CSV, R, Python ve SPSS dosyalarının
   dördünün de bulunduğunu doğrulayın.

GitHub resmi yönergesi:
https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

## ZIP görünmüyorsa metin yedeğinden üretme

`github-b01-paket.json` ve `github-b01-paketini-ac.txt` dosyalarını aynı
klasöre indirin. Python bulunan bilgisayarınızda o klasörde:

```sh
python github-b01-paketini-ac.txt
```

Betik standart Python kütüphanelerini kullanır; kurulum, bağlantı veya
GitHub şifresi gerektirmez. `.txt` uzantısı taşınabilir metin olarak saklamak
içindir; dosyanın içeriği Python kodudur. Dosya adını değiştirmeden Python
ile çalıştırabilirsiniz. `github-b01-hazir/` klasörü ve `github-b01-hazir.zip`
oluşur; bunları yukarıdaki adımlarla yükleyebilirsiniz. Mevcut hedef klasör
veya ZIP varsa betik bunları silmez, durur.

## Yerel kontrol

Yayın klasörünün kökünden:

```sh
cd bolumler/b01/ornek-01
python cozum.py --check
```

Beklenen mesaj: `DOGRULANDI: 18 kontrol degeri eslesiyor.`