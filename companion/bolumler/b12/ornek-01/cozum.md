# Açıklamalı çözüm

## 1. Toplamlar ve yüzdeler

N=30+10+20+20=80; satır toplamları 40 ve 40; sütun toplamları 50 ve 30'dur.
Birinci grupta başarı oranı 30/40=0,75; ikinci grupta 20/40=0,50'dir.
Bunlar %75 ve %50 satır yüzdeleridir. Birinci gruptaki başarılıların tüm
örneklem içindeki payı 30/80=%37,5 farklı bir soruyu yanıtlar.

H0: Grup ve başarı kategorisi bağımsızdır. H1: Bağımsız değildir.
İki gruptaki başarı oranlarının farklı olması bu 2×2 tabloda ilişki örüntüsüdür.

## 2. Beklenen frekans ve hücre katkısı

`E = satır toplamı × sütun toplamı / N`.
Her satırda beklenen değerler 40×50/80=25 ve 40×30/80=15'tir.

| Hücre | Gözlenen O | Beklenen E | Katkı (O−E)²/E | Pearson artığı (O−E)/√E |
|---|---:|---:|---:|---:|
| Birinci–Başarılı | 30 | 25 | 1 | +1 |
| Birinci–Başarısız | 10 | 15 | 1,6666666667 | −1,2909944487 |
| İkinci–Başarılı | 20 | 25 | 1 | −1 |
| İkinci–Başarısız | 20 | 15 | 1,6666666667 | +1,2909944487 |

Katkılar negatif olamaz; her katkı ilgili Pearson artığının karesidir.
Pozitif artık beklenenden fazla, negatif artık beklenenden az sayım demektir.
Artıkların birbirinden bağımsız dört test istatistiği olduğu varsayılmaz.

## 3. Genel test ve ilişki büyüklüğü

χ²=1+5/3+1+5/3=16/3≈5,3333333333.
Serbestlik derecesi (2−1)(2−1)=1'dir.

`p = P(χ²₁ ≥ 5,3333333333) = 0,0209213353`.

Bu, **süreklilik düzeltmesiz Pearson** testidir. α=0,05'te bağımsızlık
hipotezi reddedilir. Cramér V=√(χ²/80)=0,2581988897'dir. V negatif olmaz;
ilişkinin yönünü veya nedenselliğini göstermez. Örüntü satır yüzdeleri ve
artıklarla açıklanır, pratik önem bağlamla değerlendirilir.

Örnek rapor: “Birinci grupta başarı %75, ikinci grupta %50'dir.
Pearson χ²(1, N=80)=5,3333, p=0,02092, Cramér V=0,2582;
Yates düzeltmesi uygulanmamıştır. En küçük beklenen frekans 15'tir.”

## 4. Sınırlar

Beklenen sayılar bu pilotun sayısal koşulunu sağlar; bu, rastgele örnekleme
ve bağımsızlık doğrulaması değildir. Anlamlı ilişki, grup üyeliğinin başarıyı
nedensel olarak değiştirdiğini göstermez. p, bağımsızlığın doğru olma
olasılığı veya ilişkinin büyüklüğü değildir. Reddetmeme de bağımsızlığı
kanıtlamaz. Kayıtların aynı kişilerin ön/son sonuçları olması halinde
bağımsızlık testi yerine eşleşmiş ikili veriye uygun yöntem düşünülmelidir.

Bu paket kesin p-değeri veya otomatik hücre bazlı çoklu karşılaştırma
üretmez. Pearson artığı ile R `stdres` aynı nicelik değildir.