# Örnek 01 — Adım adım çözüm

## 1. Evren ve tasarım

Evren değerleri 2,4,6,8; her birinin tek çekimde olasılığı 1/4'tür.
Ortalama (2+4+6+8)/4=**5**. Sapmalar −3,−1,1,3; kareler toplamı 20.
Tam evren varyansı 20/4=**5**; standart sapması **√5≈2,236068**.

Geri koymalı iki bağımsız çekimde 4×4=**16 sıralı sonuç** vardır. Her birinin
olasılığı (1/4)(1/4)=1/16. Her satır iki çekimden oluşan bir örneklemdir.
Örneğin (2,4) ve (4,2) farklı sıralı sonuçlardır; ikisinin de ortalaması 3'tür.

## 2. On altı örneklem ortalaması

Satırlar ilk, sütunlar ikinci çekimi gösterir; hücreler ortalamadır:

| İlk / ikinci | 2 | 4 | 6 | 8 |
|---|---:|---:|---:|---:|
| 2 | 2 | 3 | 4 | 5 |
| 4 | 3 | 4 | 5 | 6 |
| 6 | 4 | 5 | 6 | 7 |
| 8 | 5 | 6 | 7 | 8 |

Bir hücre bir sonuçtur. Aynı ortalama birden fazla hücrede görülebilir;
ortalama değerlerini tekilleştirip eşit ağırlık vermek doğru değildir.

| Ortalama | Frekans | Olasılık |
|---|---:|---:|
| 2 | 1 | 1/16 = 0,0625 |
| 3 | 2 | 2/16 = 0,125 |
| 4 | 3 | 3/16 = 0,1875 |
| 5 | 4 | 4/16 = 0,25 |
| 6 | 3 | 3/16 = 0,1875 |
| 7 | 2 | 2/16 = 0,125 |
| 8 | 1 | 1/16 = 0,0625 |
| Toplam | 16 | 1 |

## 3. Merkez, varyans ve standart hata

Beklenen değer = (2×1+3×2+4×3+5×4+6×3+7×2+8×1)/16 = 80/16 = **5**.
Yanlılık E(ortalama)−μ = 5−5 = **0**.

Ortalamaların 5'ten kareli sapmalarının frekansla ağırlıklı toplamı
9×1+4×2+1×3+0×4+1×3+4×2+9×1 = **40**.
Tam dağılım varyansı 40/16=**2,5**; standart hata **√2,5≈1,581139**.
Kuramsal formül de σ/√n = √5/√2 = √2,5 verir.

Buradaki 16 satır, bilinmeyen bir dağılımdan rastgele alınan 16 tekrar değil,
bütün eşit olasılıklı sonuçlardır. Bu nedenle 15'e bölünmez. 15'e bölmek
40/15=2,666667 verir; bu farklı nicelik aranan tam dağılım varyansı değildir.
Tek gözlemin standart sapması 2,236068 ile ortalamanın standart hatası
1,581139 birbirinden ayrılır; aralarındaki oran 1/√2'dir.

## 4. Olay olasılıkları

Ortalaması en az 7 olan çiftler **(6,8), (8,6), (8,8)**:
P(ortalama ≥ 7)=3/16=**0,1875**.

Ortalaması tam 5 olanlar **(2,8), (4,6), (6,4), (8,2)**:
P(ortalama = 5)=4/16=**0,25**.

## 5. Kısa rapor

> Dört eşit olasılıklı yapay değerden geri koymalı iki bağımsız çekimin
> 16 sıralı sonucu eksiksiz listelendi. Örneklem ortalamasının beklenen
> değeri 5, varyansı 2,5 ve standart hatası yaklaşık 1,5811 bulundu.
> Ortalamanın en az 7 olması olasılığı 0,1875'tir. Sonuçlar benzetim
> yaklaşımı değil, belirtilen sonlu tasarımın tam dağılım hesabıdır.

Bu yapay evrenin hesapları gerçek öğrenciler hakkında genelleme veya bir
seçim yanlılığının giderildiği iddiasını desteklemez.