# B02 alıştırma çözümleri

1. Birim öğrenci; okul türü nominal kategorik, sınıf sıralı kategorik,
   puan niceldir. Puan için aralık ölçeği öğretim varsayımı kullanılmıştır.
2. Sınıf düzeyleri sıralanır; kodlar nicel bir ölçüm birimi değildir.
   Sırayı koruyan 10/20/30 etiketleri de sıralı kategoridir. Kod ortalaması
   değişebilir; öğrencilerin gerçek sınıf dağılımı değişmez. Pilot kodun
   sözlüğü 1–3 beklediği için 10/20/30 değişikliği kod/sözlük uyarlaması gerektirir.
3. Devlet: 3/4 = 0,75 = %75. Özel: 1/4 = 0,25 = %25.
4. Sınıf 1: 2/4 = 0,50; sınıf 2: 1/4 = 0,25; sınıf 3: 1/4 = 0,25.
   En sık görülen sınıf 1'dir; bu başarı düzeyini göstermez.
5. Genel: 298/4 = 74,5. Devlet: 217/3 = 72,3333. Özel: 81/1 = 81.
   Okul türü için değil, okul türüne göre gruplandırılmış **puan** için ortalama alınır.
6. Eşit okul ağırlıkları 76,6667 verir; gruplar eşit büyüklükte değildir.
   Doğru gözlem ağırlıkları 3/4 ve 1/4'tür. (3/4) × (217/3) + (1/4) × 81 = 74,5.
   Bunlar kayıtları birleştirme ağırlıklarıdır; açıklanmamış bir araştırmanın
   tasarım ağırlıkları olarak yorumlanmamalıdır.
7. Dört kaydın tamamı sonlu hedef evrense 74,5 parametredir. Daha geniş
   hedef evrende bir örneklem istatistiğidir. Olasılıklı örnekleme bilgisi
   olmadan temsil iddia edilemez; burada kayıtların yapay olduğu da unutulmamalıdır.
8. Hayır. Hedef evren, örnekleme çerçevesi, seçim olasılıkları, kapsam ve
   yanıt vermeme bilgileri gerekir. Küçük bir dosyadaki oran evren oranını kanıtlamaz.
9. Beş gözlem olur. Genel ortalama (298 + 85)/5 = 76,6; devlet oranı 3/5 = 0,60,
   özel oranı 2/5 = 0,40; özel okul ortalaması (81 + 85)/2 = 83'tür.
   Sınıf frekansları 2, 1, 2; oranları 0,40, 0,20, 0,40 olur.
   Özgün veri için hazırlanan `--check` kontrolünün artık başarısız olması beklenir.
10. Özel frekansı 0, oranı 0'dır; gözlem olmadığından puan ortalaması
    tanımsızdır. Python/R pilotlarında `NaN` görünür; bu sıfır puan demek değildir.
    Kalan üç devlet kaydının ortalaması 72,3333 olur.
11. Eksik gözlem sıfır puan değildir; sıfır eklemek ortalamayı düşürebilir
    ve eksikliği gizler. Betiğin durması veri denetimidir, eksikliğin nedeni
    ve uygun analiz yöntemi konusunda bilimsel karar değildir.
12. Örnek: “Dört gözlemlik öğretim verisinde devlet okulu kategorisi %75,
    özel okul kategorisi %25 paya sahiptir; genel puan ortalaması 74,5'tir.
    Bu yapay veri yalnız verilen örneği betimler; okul türünün etkisi veya
    daha geniş bir evrenin özellikleri hakkında kanıt sunmaz.”