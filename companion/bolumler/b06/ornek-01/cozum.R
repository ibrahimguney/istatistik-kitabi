hazirla <- function(veri) {
  if (!identical(names(veri), c("id", "sinif", "basit", "tabakali")) || nrow(veri) != 12) {
    stop("Bu pilot 12 kisilik cerceveyi bekler.")
  }
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu ve eksiksiz sayisal degerler gerekli.")
  temiz <- veri[order(veri$id), ]
  if (!all(temiz$id == 1:12) || !all(temiz$sinif == rep(1:3, each = 4))) {
    stop("Kimlik-sinif eslesmesi kitap cercevesiyle uyusmuyor.")
  }
  if (!all(as.matrix(temiz[c("basit", "tabakali")]) %in% c(0, 1))) stop("Gostergeler 0/1 olmali.")
  if (sum(temiz$basit) != 6 || !all(tapply(temiz$tabakali, temiz$sinif, sum) == 2)) {
    stop("Orneklem buyuklugu veya tabaka tahsisi uyusmuyor.")
  }
  temiz$sinif <- factor(temiz$sinif, levels = 1:3, ordered = TRUE)
  temiz
}

hesapla <- function(veri) {
  temiz <- hazirla(veri)
  sonuc <- data.frame(degisken = rep("cerceve", 3),
                      olcu = c("hacim", "benzersiz_id", "sinif_sayisi"),
                      deger = c(nrow(temiz), length(unique(temiz$id)), nlevels(temiz$sinif)),
                      stringsAsFactors = FALSE)
  for (tasarim in c("basit", "tabakali")) {
    secilen <- temiz[temiz[[tasarim]] == 1, ]
    olasilik <- if (tasarim == "basit") nrow(secilen) / nrow(temiz) else 2 / 4
    agirlik <- 1 / olasilik
    sonuc <- rbind(sonuc, data.frame(degisken = rep(tasarim, 13),
      olcu = c("orneklem_hacmi", "dahil_edilme_olasiligi", "tasarim_agirligi", "agirlik_toplami",
               paste0("sinif_", 1:3, "_frekans"), paste0("secilen_id_", 1:6)),
      deger = c(nrow(secilen), olasilik, agirlik, nrow(secilen) * agirlik,
                as.numeric(table(secilen$sinif)), secilen$id)))
  }
  sonuc
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
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/secim-haritasi.png", width = 1500, height = 525, res = 150)
  on.exit(dev.off())
  par(mar = c(4, 7, 3, 1))
  plot(NA, xlim = c(0.5, 12.5), ylim = c(-0.5, 2.8), xaxt = "n", yaxt = "n",
       xlab = "Yapay ogrenci kimligi", ylab = "", main = "Kayitli secimler: dolu nokta secilen birim")
  axis(1, at = 1:12)
  axis(2, at = 0:2, labels = c("Tabakali", "Basit rastgele", "Cerceve"), las = 1)
  abline(v = c(4.5, 8.5), lty = 3, col = "grey")
  text(c(2.5, 6.5, 10.5), 2.4, paste("Sinif", 1:3))
  points(temiz$id, rep(2, 12), pch = 19, col = "#555555")
  for (index in 1:2) {
    tasarim <- c("basit", "tabakali")[index]
    konum <- 2 - index
    points(temiz$id, rep(konum, 12), pch = 1, col = "grey")
    secilen <- temiz$id[temiz[[tasarim]] == 1]
    points(secilen, rep(konum, length(secilen)), pch = 19, col = c("#1F4E79", "#087F5B")[index])
  }
  cat("Grafik: ciktilar/r/secim-haritasi.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()