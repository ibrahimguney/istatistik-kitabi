# B01 alıştırma çözümleri

1. Birim öğrencidir; beş satır ve üç değişken vardır.
2. Devam nicel/oran; başarı nicel ve aralık ölçeği varsayımıyla; program
   nominal kategoriktir. Dosyadaki sayı biçimi tek başına ölçme düzeyini belirlemez.
3. A: 3, 0,60, %60. B: 2, 0,40, %40. Frekansların toplamı 5, oranların
   toplamı 1'dir.
4. Devam toplamı 46, ortalama 9,2; başarı toplamı 362, ortalama 72,4'tür.
5. Başarı ortalaması 77,4 olur; program oranları değişmez.
6. Altı gözlem vardır. A: 4/6 = 2/3; B: 2/6 = 1/3. Devam ortalaması
   57/6 = 9,5; başarı ortalaması 442/6 = 73,6667'dir. Eski kontrol dosyası
   özgün beş satırı tanımlar; yeni veride başarısız olması beklenir.
7. A: (68 + 75 + 72)/3 = 71,6667. B: (64 + 83)/2 = 73,5. B−A farkı
   1,8333 puandır. Rastgele atama ve karşılaştırılabilirlik bilgisi yoktur;
   veri de yapaydır. Bu fark nedensel etki olarak yorumlanamaz.
   Veri nesnesi oturumda yüklüyken R'de
   `tapply(veri$basari, veri$program, mean)`, Python'da
   `veri.groupby("program")["basari"].mean()` kullanılabilir.
8. Hayır; 1/2 yalnız kategori kodudur. Kodların ortalaması anlamlı değildir.
9. Eksiklik sıfır puan değildir; sıfır eklemek ortalamayı değiştirebilir ve
   eksikliğin nedenini gizler. Betiğin durması veri denetimidir; eksik veri
   için bilimsel yöntem seçiminin yerine geçmez.
10. Kayıtlar yapaydır ve olasılıklı örneklem olarak seçilmemiştir. Beş gözlem
    hedef evrenin kapsamı ve temsili hakkında kanıt sağlamaz. Daha fazla
    satır eklemek tek başına tasarım sorununu çözmez.