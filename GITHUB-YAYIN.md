# Yeni GitHub deposuna ilk yükleme

Prism, çalışma sırasında oluşturulan `.bundle` ve yeni ZIP dosyalarını proje
dosya ağacında kalıcı olarak tutmadığı için yükleme paketi kullanılmaz.
Birleşik kitap, **MAT301-PDR209** projesinin bilgisayara indirilen kopyasından
GitHub'a gönderilir.

## 1. Projeyi bilgisayara alma

Prism'den MAT301-PDR209 projesini indirin/dışa aktarın ve arşivi bilgisayarınızda
açın. Terminali açılmış proje klasöründe çalıştırın.

## 2. Yayımlanmayacak dosyaları ayırma

GitHub'a göndermeden önce aşağıdaki büyük veya üretilmiş dosyaları proje
klasöründen çıkarın ya da `.gitignore` içine ekleyin:

- `Mist.zip`
- `Tist.zip`
- `main.pdf` ve diğer derlenmiş PDF'ler
- `build/`
- LaTeX geçici dosyaları (`*.aux`, `*.log`, `*.toc`, `*.out` vb.)

Kitap kaynakları, kapaklar, `assets/`, `chapters/`, `companion/`, veri ve kod
dosyaları korunmalıdır.

## 3. GitHub'a gönderme

```sh
git init -b main
git add .
git commit -m "Birleşik istatistik kitabının ilk yayını"
git remote add origin https://github.com/ibrahimguney/istatistik-kitabi.git
git push -u origin main
```

Klasörde daha önce Git başlatılmışsa ilk komut atlanabilir. `origin` zaten
tanımlıysa `git remote add` yerine şu komut kullanılır:

```sh
git remote set-url origin https://github.com/ibrahimguney/istatistik-kitabi.git
```

GitHub parola kabul etmez; tarayıcıyla oturum açma, kişisel erişim belirteci,
SSH anahtarı veya GitHub Desktop kullanılmalıdır.

## 4. Yüklemeden sonra

1. Depo ana sayfasında `README.md` dosyasını kontrol edin.
2. PDF e-kitabı Git geçmişine eklemek yerine **Releases** bölümünde `v1.0.0`
   etiketiyle yayımlayın.
3. Eski iki depoya birleşik depoya yönlendiren kısa bir açıklama ekleyin.