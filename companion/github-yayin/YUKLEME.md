# B01 ilk GitHub yüklemesi — tarihsel not

Güncel birleşik kitap deposu:
https://github.com/ibrahimguney/istatistik-kitabi

## Durum — 9 Eylül 2026

Kullanıcı yalnız B01 pilot paketinin ve depo giriş sayfasının yüklenmesini
onayladı. Bu ortamda GitHub kimlik bilgisi bulunamadı; terminalden GitHub
Git bağlantısı `CONNECT tunnel failed, response 403` hatası verdi.
**Hiçbir commit veya push yapılmadı; paket GitHub'a yüklenmedi.**

## Tarayıcıdan yükleme

1. `companion/istatistik-uygulamalari-b01.zip` dosyasını indirin ve açın.
2. GitHub'da kendi hesabınızla hedef depoyu açın.
3. Boş depodaki “uploading an existing file” bağlantısını veya mevcut
   depodaki “Add file → Upload files” seçeneğini kullanın.
4. ZIP'in içindeki **README.md dosyasını ve bolumler klasörünü** yükleme
   alanına sürükleyin. ZIP dosyasının kendisini veya dıştaki ZIP açma
   klasörünü tek bir dosya/üst klasör olarak yüklemeyin.
5. Commit mesajını `B01 pilot uygulama paketini ekle` yazıp değişiklikleri
   kaydedin. Depo bu sırada dolmuşsa aynı adlı dosyaları üzerine yazmadan
   önce inceleyin.
6. Depo kökünde README.md, altında bolumler/b01/ornek-01/veri.csv,
   cozum.R, cozum.py ve analiz.sps dosyalarının bulunduğunu kontrol edin.
7. B01 bağlantısını açın; README ve alıştırma bağlantılarını kontrol edin.

Python doğrulandı; R/SPSS çalışma kontrolleri bekliyor. Token veya parola
sohbete yazılmamalıdır; tarayıcıdaki normal GitHub oturumunuzu kullanın.

## Paketi yeniden üretme

Kitap projesinin kökünden:

```sh
python companion/github-yayin/hazirla.py
```

Bu komut yerel arşivleri ve manifesti yeniden üretir; ağa bağlanmaz,
GitHub'a yükleme veya commit yapmaz. SPSS kaynak metni `analiz.sps.txt`
içinde de korunur; dağıtıma gerçek `analiz.sps` adıyla alınır. Kitabın
LaTeX dosyaları dağıtım paketine dahil edilmez.

GitHub resmi yönergesi:
https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository