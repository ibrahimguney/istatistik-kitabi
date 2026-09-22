# Açıklamalı çözüm

## 1. Hipotez ve standartlaştırma

Ana soru evren farkının δ0=0 değerinden farklı olup olmadığıdır:
H0: δ=0; H1: δ≠0. Önceden seçilmiş anlamlılık düzeyi α=0,05'tir.

`t = (fark - null_degeri) / standart_hata = (2,1 - 0) / 1 = 2,1`.
Bu, tahminin sıfır hipotezi değerinden 2,1 standart hata uzaklıkta olduğunu
söyler; farkın 2,1 standart sapma büyüklüğünde olduğunu söylemez.

## 2. Kuyruk olasılığı ve karar

T, H0 altında 49 serbestlik dereceli t değişkeni olmak üzere:

| Nicelik | Değer |
|---|---:|
| Çift yönlü p = P(\|T\| ≥ 2,1) | 0,0409000890 |
| Üst yönlü p = P(T ≥ 2,1) | 0,0204500445 |
| Alt yönlü p = P(T ≤ 2,1) | 0,9795499555 |
| Çift yönlü, α=0,05 | H0 reddedilir |
| Çift yönlü, α=0,01 | H0 reddedilemez |

Üst yönlü karşılaştırma H1: δ>0, alt yönlü karşılaştırma H1: δ<0 içindir;
yönlü sıfır hipotezlerinin sınırında δ=0 ile hesap yapılır. Bunlar sonuçtan
sonra seçilecek alternatifler değildir. Üst p burada çift yönlü p'nin
yarısıdır; t negatif olsaydı sabit üst alternatif için böyle olmazdı.

Betikler kitapta olduğu gibi **p < α** kuralını kullanır; eşitlikte reddetmez.
Kararlar ekranda yuvarlanan p ile değil tam duyarlıklı değerle verilir.
p, H0'ın doğru olma olasılığı değildir: H0 modeli altında en az bu kadar
uç bir test istatistiğinin kuyruk olasılığıdır.

## 3. İki taraflı yüzde 95 güven aralığı

Kritik değer `t(0,975;49)=2,0095752371` ve hata payı
`2,0095752371 × 1 = 2,0095752371` olur.

`2,1 ± 2,0095752371 = [0,0904247629; 4,1095752371]`.

Tam genişlik 4,0191504743'tür. Bu aralık **evren farkı** içindir; tek tek
öğrencilerin notlarını kapsayan bir aralık değildir. Sıfırı içermemesi,
aynı modeldeki çift yönlü α=0,05 kararıyla uyumludur. Yüzde 95 aralık,
tek yönlü testin birebir karşılığı olarak kullanılmamalıdır.
Sınırda, sayısal yuvarlama çok küçük tutarsızlıklar üretebilir; kapalı
aralık uçları içerir ve kararlar yuvarlanmamış değerlerle incelenmelidir.

## 4. Örnek rapor ve sınırlılık

“Verilen özet altında fark tahmini 2,10, standart hatası 1,00'dır;
t(49)=2,10, çift yönlü p=0,04090 ve yüzde 95 güven aralığı
[0,0904; 4,1096] bulunmuştur. α=0,05 düzeyinde sıfır fark hipotezi
reddedilir.”

Bu rapora araştırma deseni, örnekleme yöntemi, farkın birimi ve bilimsel
önem eşiği eklenmeden pratik önem ya da nedensellik ileri sürülemez.
Reddetmeme de etkisizlik veya eşdeğerlik kanıtı değildir. Ham veri ve
çalışma deseni verilmediği için model varsayımları bu pakette doğrulanamaz.