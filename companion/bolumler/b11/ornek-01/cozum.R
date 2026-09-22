SUTUNLAR <- c("hacim_1", "ortalama_1", "standart_sapma_1", "hacim_2", "ortalama_2",
               "standart_sapma_2", "cift_sayisi", "ortalama_fark", "fark_sapmasi", "alfa")

hazirla <- function(veri) {
  if (!identical(names(veri), SUTUNLAR) || nrow(veri) != 1) stop("Tek ozet satiri ve dogru sutun sirasi gerekli.")
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu sayisal ozet gerekli.")
  hacimler <- unlist(veri[c("hacim_1", "hacim_2", "cift_sayisi")])
  if (any(hacimler < 2 | hacimler != floor(hacimler))) stop("Hacimler en az 2 olan tam sayilar olmali.")
  if (any(unlist(veri[c("standart_sapma_1", "standart_sapma_2", "fark_sapmasi")]) <= 0)) {
    stop("Bu paket pozitif standart sapmalar gerektirir.")
  }
  if (veri$alfa <= 0 || veri$alfa >= 1) stop("Alfa 0 ile 1 arasinda olmali.")
  veri
}

test_ozeti <- function(fark, standart_hata, serbestlik, alfa) {
  t_degeri <- fark / standart_hata
  p_degeri <- 2 * pt(abs(t_degeri), df = serbestlik, lower.tail = FALSE)
  kritik <- qt(1 - alfa / 2, df = serbestlik)
  hata_payi <- kritik * standart_hata
  sonuc <- c(standart_hata = standart_hata, serbestlik = serbestlik, t = t_degeri,
              p_cift = p_degeri, kritik_t = kritik, hata_payi = hata_payi,
              alt_sinir = fark - hata_payi, ust_sinir = fark + hata_payi,
              genislik = 2 * hata_payi, reddet_cift = as.integer(p_degeri < alfa))
  if (any(!is.finite(sonuc))) stop("Test sayisal olarak hesaplanamadi.")
  sonuc
}

hesapla <- function(veri) {
  veri <- hazirla(veri)
  katki_1 <- veri$standart_sapma_1^2 / veri$hacim_1
  katki_2 <- veri$standart_sapma_2^2 / veri$hacim_2
  toplam <- katki_1 + katki_2
  serbestlik <- toplam^2 / (katki_1^2 / (veri$hacim_1 - 1) + katki_2^2 / (veri$hacim_2 - 1))
  fark <- veri$ortalama_1 - veri$ortalama_2
  welch <- c(katki_1 = katki_1, katki_2 = katki_2, fark = fark,
              test_ozeti(fark, sqrt(toplam), serbestlik, veri$alfa))
  eslesmis <- c(test_ozeti(veri$ortalama_fark, veri$fark_sapmasi / sqrt(veri$cift_sayisi),
                          veri$cift_sayisi - 1, veri$alfa), dz = veri$ortalama_fark / veri$fark_sapmasi)
  sonuc <- data.frame(degisken = c(rep("girdi", 10), rep("welch", 13), rep("eslesmis", 11)),
                       olcu = c(names(veri), names(welch), names(eslesmis)),
                       deger = c(unlist(veri), welch, eslesmis), row.names = NULL)
  if (any(!is.finite(sonuc$deger))) stop("Sonlu sonuc hesaplanamadi.")
  sonuc
}

kontrol_et <- function(sonuc, beklenen) {
  if (!identical(names(beklenen), c("degisken", "olcu", "deger")) ||
      !identical(sonuc$degisken, beklenen$degisken) || !identical(sonuc$olcu, beklenen$olcu)) {
    stop("Kontrol etiketleri veya sirasi uyusmuyor.")
  }
  if (!is.numeric(beklenen$deger) || any(!is.finite(beklenen$deger)) ||
      any(!is.finite(sonuc$deger))) stop("Sonlu kontrol degerleri gerekli.")
  tolerans <- pmax(1e-9, 1e-9 * pmax(abs(sonuc$deger), abs(beklenen$deger)))
  if (any(abs(sonuc$deger - beklenen$deger) > tolerans)) stop("Kontrol degerleri uyusmuyor.")
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}

grafik_kaydet <- function(veri) {
  veri <- hazirla(veri)
  sonuc <- hesapla(veri)
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/fark-araliklari.png", width = 1500, height = 600, res = 150)
  on.exit(dev.off())
  par(mfrow = c(1, 2))
  basliklar <- c(welch = "Welch: Grup 1 - Grup 2", eslesmis = "Eslestirilmis: son - on")
  for (grup in names(basliklar)) {
    tablo <- sonuc[sonuc$degisken == grup, ]
    ozet <- setNames(tablo$deger, tablo$olcu)
    aralik <- ozet[c("alt_sinir", "ust_sinir")]
    pay <- .35 * ozet["hata_payi"]
    plot(NA, xlim = range(c(0, aralik)) + c(-pay, pay), ylim = c(-.5, .6), yaxt = "n", ylab = "",
         xlab = "Evren ortalama farki (puan)",
         main = paste(basliklar[grup], sprintf("p = %.6f", ozet["p_cift"]), sep = "\n"))
    segments(aralik[1], 0, aralik[2], 0, col = "#087F5B", lwd = 2)
    points(mean(aralik), 0, col = "#087F5B", pch = 19)
    abline(v = 0, lty = 2, col = "#555555")
    for (uc in aralik) {
      segments(uc, -.06, uc, .06, col = "#087F5B")
      text(uc, .15, sprintf("%.4f", uc))
    }
    legend("bottomright", legend = paste("Guven duzeyi:", 1 - veri$alfa), bty = "n", cex = .8)
  }
  cat("Grafik: ciktilar/r/fark-araliklari.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()