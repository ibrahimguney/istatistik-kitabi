hazirla <- function(veri) {
  if (!identical(names(veri), c("n", "ortalama", "s")) || nrow(veri) != 1) {
    stop("Tek satirda n, ortalama, s ozeti gerekli; bu ham veri degildir.")
  }
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu ve eksiksiz sayisal ozet gerekli.")
  if (veri$n < 2 || veri$n != floor(veri$n)) stop("n en az 2 olan tam sayi olmali.")
  if (veri$s <= 0) stop("Bu pilot pozitif orneklem standart sapmasi gerektirir.")
  veri
}

aralik_hesapla <- function(veri, duzey) {
  temiz <- hazirla(veri)
  if (!is.numeric(duzey) || length(duzey) != 1 || !is.finite(duzey) || duzey <= 0 || duzey >= 1) {
    stop("Guven duzeyi 0 ile 1 arasinda olmali; 95 yerine 0.95 kullanin.")
  }
  standart_hata <- temiz$s / sqrt(temiz$n)
  kritik <- qt((1 + duzey) / 2, df = temiz$n - 1)
  hata_payi <- kritik * standart_hata
  sonuc <- c(guven_duzeyi = duzey, alpha = 1 - duzey, kritik_t = kritik,
              hata_payi = hata_payi, alt_sinir = temiz$ortalama - hata_payi,
              ust_sinir = temiz$ortalama + hata_payi, genislik = 2 * hata_payi)
  if (any(!is.finite(sonuc))) stop("Aralik sayisal olarak hesaplanamadi.")
  sonuc
}

hesapla <- function(veri) {
  temiz <- hazirla(veri)
  sonuc <- data.frame(degisken = rep("ozet", 5),
    olcu = c("hacim", "ortalama", "orneklem_sd", "standart_hata", "serbestlik"),
    deger = c(temiz$n, temiz$ortalama, temiz$s, temiz$s / sqrt(temiz$n), temiz$n - 1),
    stringsAsFactors = FALSE)
  for (index in 1:2) {
    duzey <- c(0.95, 0.99)[index]
    aralik <- aralik_hesapla(temiz, duzey)
    sonuc <- rbind(sonuc, data.frame(degisken = rep(c("GA95", "GA99")[index], 7),
                  olcu = names(aralik), deger = as.numeric(aralik)))
  }
  sonuc
}

kontrol_et <- function(sonuc, beklenen) {
  if (!identical(names(beklenen), c("degisken", "olcu", "deger")) ||
      !identical(sonuc$degisken, beklenen$degisken) ||
      !identical(sonuc$olcu, beklenen$olcu)) stop("Kontrol etiketleri uyusmuyor.")
  if (!is.numeric(beklenen$deger) || anyNA(beklenen$deger) ||
      any(!is.finite(beklenen$deger)) || any(!is.finite(sonuc$deger))) stop("Sonlu kontrol degerleri gerekli.")
  tolerans <- pmax(1e-9, 1e-9 * pmax(abs(sonuc$deger), abs(beklenen$deger)))
  if (any(abs(sonuc$deger - beklenen$deger) > tolerans)) stop("Kontrol uyusmazligi.")
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}

grafik_kaydet <- function(veri) {
  temiz <- hazirla(veri)
  aralik95 <- aralik_hesapla(temiz, 0.95)
  aralik99 <- aralik_hesapla(temiz, 0.99)
  genislik <- aralik99["genislik"]
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/guven-araliklari.png", width = 1350, height = 525, res = 150)
  on.exit(dev.off())
  par(mar = c(4, 6, 3, 1))
  plot(NA, xlim = c(aralik99["alt_sinir"], aralik99["ust_sinir"]) + c(-0.15, 0.15) * genislik,
       ylim = c(-0.5, 1.6), yaxt = "n", xlab = "Evren ortalamasi icin aralik (puan)", ylab = "",
       main = paste("n=", temiz$n, "; ortalama=", temiz$ortalama, "; s=", temiz$s))
  axis(2, at = 0:1, labels = c("%99 guven", "%95 guven"), las = 1)
  abline(v = temiz$ortalama, col = "grey", lty = 3)
  for (index in 1:2) {
    aralik <- list(aralik95, aralik99)[[index]]
    konum <- 2 - index
    renk <- c("#1F4E79", "#087F5B")[index]
    segments(aralik["alt_sinir"], konum, aralik["ust_sinir"], konum, col = renk, lwd = 2)
    points(temiz$ortalama, konum, pch = 19, col = renk)
    for (uc in aralik[c("alt_sinir", "ust_sinir")]) {
      segments(uc, konum - 0.08, uc, konum + 0.08, col = renk)
      text(uc, konum + 0.23, sprintf("%.4f", uc))
    }
  }
  cat("Grafik: ciktilar/r/guven-araliklari.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()