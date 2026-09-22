hazirla <- function(veri) {
  if (!identical(names(veri), c("fark", "standart_hata", "serbestlik", "null_degeri", "alfa")) || nrow(veri) != 1) {
    stop("Tek satirda fark, standart_hata, serbestlik, null_degeri, alfa ozeti gerekli.")
  }
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu ve eksiksiz sayisal ozet gerekli.")
  if (veri$standart_hata <= 0 || veri$serbestlik <= 0) stop("SE ve serbestlik pozitif olmali.")
  if (veri$alfa <= 0 || veri$alfa >= 1) stop("Alfa 0 ile 1 arasinda olmali.")
  veri
}

test_hesapla <- function(veri) {
  temiz <- hazirla(veri)
  t_degeri <- (temiz$fark - temiz$null_degeri) / temiz$standart_hata
  p_cift <- 2 * pt(abs(t_degeri), df = temiz$serbestlik, lower.tail = FALSE)
  p_ust <- pt(t_degeri, df = temiz$serbestlik, lower.tail = FALSE)
  p_alt <- pt(t_degeri, df = temiz$serbestlik)
  kritik <- qt(1 - temiz$alfa / 2, df = temiz$serbestlik)
  hata_payi <- kritik * temiz$standart_hata
  alt_sinir <- temiz$fark - hata_payi
  ust_sinir <- temiz$fark + hata_payi
  sonuc <- c(t = t_degeri, p_cift = p_cift, p_ust = p_ust, p_alt = p_alt,
              reddet_cift = as.integer(p_cift < temiz$alfa), reddet_alfa001 = as.integer(p_cift < 0.01),
              reddet_ust = as.integer(p_ust < temiz$alfa), reddet_alt = as.integer(p_alt < temiz$alfa),
              guven_duzeyi = 1 - temiz$alfa, kritik_t = kritik, hata_payi = hata_payi,
              alt_sinir = alt_sinir, ust_sinir = ust_sinir, genislik = 2 * hata_payi,
              null_aralikta = as.integer(alt_sinir <= temiz$null_degeri && temiz$null_degeri <= ust_sinir))
  if (any(!is.finite(sonuc))) stop("Test veya aralik sayisal olarak hesaplanamadi.")
  sonuc
}

hesapla <- function(veri) {
  temiz <- hazirla(veri)
  sonuc <- test_hesapla(temiz)
  data.frame(degisken = c(rep("girdi", 5), rep("test", 8), rep("aralik", 7)),
             olcu = c(names(temiz), names(sonuc)),
             deger = c(as.numeric(unlist(temiz)), as.numeric(sonuc)), stringsAsFactors = FALSE)
}

kontrol_et <- function(sonuc, beklenen) {
  if (!identical(names(beklenen), c("degisken", "olcu", "deger")) ||
      !identical(sonuc$degisken, beklenen$degisken) ||
      !identical(sonuc$olcu, beklenen$olcu)) stop("Kontrol etiketleri uyusmuyor.")
  if (!is.numeric(beklenen$deger) || anyNA(beklenen$deger) ||
      any(!is.finite(beklenen$deger)) || any(!is.finite(sonuc$deger))) stop("Sonlu kontrol gerekli.")
  tolerans <- pmax(1e-9, 1e-9 * pmax(abs(sonuc$deger), abs(beklenen$deger)))
  if (any(abs(sonuc$deger - beklenen$deger) > tolerans)) stop("Kontrol uyusmazligi.")
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}

grafik_kaydet <- function(veri) {
  temiz <- hazirla(veri)
  sonuc <- test_hesapla(temiz)
  sinir <- max(5, abs(sonuc["t"]) + 1, sonuc["kritik_t"] + 1)
  eksen <- seq(-sinir, sinir, length.out = 2001)
  yogunluk <- dt(eksen, df = temiz$serbestlik)
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/test-ve-aralik.png", width = 1650, height = 600, res = 150)
  on.exit(dev.off())
  par(mfrow = c(1, 2))
  plot(eksen, yogunluk, type = "l", col = "#1F4E79", xlab = "H0 altinda t", ylab = "Yogunluk",
       main = paste("Cift yonlu p =", format(sonuc["p_cift"], digits = 5)))
  for (indis in list(eksen <= -abs(sonuc["t"]), eksen >= abs(sonuc["t"]))) {
    polygon(c(eksen[indis][1], eksen[indis], tail(eksen[indis], 1)),
            c(0, yogunluk[indis], 0), col = "#8FB8D8", border = NA)
  }
  abline(v = c(-abs(sonuc["t"]), abs(sonuc["t"])), lty = 3, col = "#1F4E79")
  aralik <- sonuc[c("alt_sinir", "ust_sinir")]
  sinirlar <- range(c(aralik, temiz$null_degeri)) + c(-.3, .3) * sonuc["hata_payi"]
  plot(NA, xlim = sinirlar, ylim = c(-.5, .7), yaxt = "n", ylab = "",
       xlab = "Evren farki delta (fark birimi)", main = paste("Guven duzeyi:", 1 - temiz$alfa))
  segments(aralik[1], 0, aralik[2], 0, col = "#087F5B", lwd = 2)
  points(temiz$fark, 0, pch = 19, col = "#087F5B")
  abline(v = temiz$null_degeri, lty = 2, col = "#555555")
  for (uc in aralik) {
    segments(uc, -.06, uc, .06, col = "#087F5B")
    text(uc, .2, sprintf("%.4f", uc))
  }
  cat("Grafik: ciktilar/r/test-ve-aralik.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE)
cat("Ana cift yonlu karar:", if (test_hesapla(veri)["reddet_cift"] == 1) "H0 reddedilir" else "H0 reddedilemez", "\n")
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()