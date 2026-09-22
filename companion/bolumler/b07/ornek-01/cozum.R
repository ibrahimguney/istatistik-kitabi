sayisal_kontrol <- function(veri, sutunlar, en_az) {
  if (!identical(names(veri), sutunlar) || nrow(veri) < en_az) stop("Sema veya satir sayisi gecersiz.")
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu ve eksiksiz sayisal veri gerekli.")
}

hazirla <- function(veri, benzetim) {
  sayisal_kontrol(veri, "yanit", 1)
  if (!all(veri$yanit %in% c(0, 1))) stop("Yanitlar 0/1 olmali.")
  sayisal_kontrol(benzetim, c("tekrar", "basari"), 2)
  temiz <- benzetim[order(benzetim$tekrar), ]
  if (!all(temiz$tekrar == seq_len(nrow(temiz)))) stop("Tekrar kimlikleri uyusmuyor.")
  if (any(temiz$basari < 0 | temiz$basari > 50 | temiz$basari != floor(temiz$basari))) {
    stop("Basari sayisi 0..50 arasinda tam sayi olmali.")
  }
  list(gozlem = veri, tekrarlar = temiz)
}

hesapla <- function(veri, benzetim) {
  temiz <- hazirla(veri, benzetim)
  yanit <- temiz$gozlem$yanit
  oran <- mean(yanit)
  tahminler <- temiz$tekrarlar$basari / 50
  merkez <- mean(tahminler)
  yanlilik <- merkez - 0.40
  varyans <- mean((tahminler - merkez)^2)
  data.frame(
    degisken = c(rep("gozlem", 6), rep("p_hat_060", 2), rep("benzetim", 13)),
    olcu = c("hacim", "olumlu", "olumsuz", "oran", "yaklasik_se", "yaklasik_varyans",
             "se_25", "se_400", "tekrar_sayisi", "orneklem_hacmi", "gercek_oran", "merkez",
             "yanlilik", "varyans_B", "varyans_Beksi1", "ampirik_se", "mse", "mse_ayrisimi",
             "kuramsal_yanlilik", "kuramsal_se", "kuramsal_mse"),
    deger = c(length(yanit), sum(yanit), length(yanit) - sum(yanit), oran,
              sqrt(oran * (1 - oran) / length(yanit)), oran * (1 - oran) / length(yanit),
              sqrt(0.60 * 0.40 / 25), sqrt(0.60 * 0.40 / 400),
              length(tahminler), 50, 0.40, merkez, yanlilik, varyans, var(tahminler),
              sd(tahminler), mean((tahminler - 0.40)^2), varyans + yanlilik^2,
              0, sqrt(0.40 * 0.60 / 50), 0.40 * 0.60 / 50), stringsAsFactors = FALSE)
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

grafik_kaydet <- function(veri, benzetim) {
  temiz <- hazirla(veri, benzetim)
  frekans <- as.numeric(table(factor(temiz$gozlem$yanit, levels = 0:1))) / nrow(veri)
  adetler <- as.numeric(table(factor(temiz$tekrarlar$basari, levels = 0:50))) / nrow(benzetim)
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/oran-tahmini.png", width = 1500, height = 600, res = 150)
  on.exit(dev.off())
  par(mfrow = c(1, 2))
  barplot(frekans, names.arg = c("0", "1"), ylim = c(0, 1), col = "#8FB8D8",
          xlab = "Ikili yanit", ylab = "Gozlenen oran", main = paste("Gozlenen ornek: n=", nrow(veri)))
  plot((0:50) / 50, adetler, type = "h", lwd = 4, xlim = c(0, 1), ylim = c(0, max(adetler) * 1.1),
       col = "#1F4E79", xlab = "Oran tahmini", ylab = "Benzetim goreli frekansi",
       main = paste("n=50; tekrar=", nrow(benzetim)))
  abline(v = 0.40, col = "#087F5B", lty = 2)
  cat("Grafik: ciktilar/r/oran-tahmini.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
benzetim <- read.csv("benzetim.csv", check.names = FALSE)
sonuc <- hesapla(veri, benzetim)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri, benzetim)
sessionInfo()