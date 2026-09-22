# Cozum ve yorum
E(ortalama)=10, Var(ortalama)=100/n, SE=10/sqrt(n).
Ampirik SE tekrar ortalamalarinin B-1 paydali standart sapmasidir.
Sapma sutunu tekrar merkezi eksi 10; kuramsal yanlilik kaniti degildir.
B artinca Monte Carlo oynakligi azalir; n sabitken hedef SE degismez.
n artinca ortalamalar daralir; ham ustel evren degismez.
n=30 her evren icin normallik garantisi degildir; bagimsizlik ve sonlu varyans gerekir.
Ayni CSV'nin ozetleri 1e-9 toleransla karsilastirilir; bu tolerans kuramsal hedefe uzaklik degildir.
Grafiklerin eksen olceklerini okuyun; panel genisligi tek basina yayilim olcusu degildir.

| Degisken | Olcu | Deger |
|---|---|---:|
| n1 | n | 1 |
| n1 | B | 10000 |
| n1 | merkez | 9.850940111 |
| n1 | ampirik_se | 10.00651769 |
| n1 | kuramsal_se | 10 |
| n1 | varyans | 100 |
| n1 | sapma | -0.1490598894 |
| n5 | n | 5 |
| n5 | B | 10000 |
| n5 | merkez | 9.976486031 |
| n5 | ampirik_se | 4.481203621 |
| n5 | kuramsal_se | 4.472135955 |
| n5 | varyans | 20 |
| n5 | sapma | -0.0235139688 |
| n30 | n | 30 |
| n30 | B | 10000 |
| n30 | merkez | 9.964918484 |
| n30 | ampirik_se | 1.826794594 |
| n30 | kuramsal_se | 1.825741858 |
| n30 | varyans | 3.333333333 |
| n30 | sapma | -0.03508151559 |
| ek | se25 | 2 |
| ek | se100 | 1 |
| ek | hacim_carpani | 4 |