GRUPLAR <- c("Birinci", "Ikinci")
SONUCLAR <- c("Basarili", "Basarisiz")
ALFA <- 0.05

hazirla <- function(veri) {
  if (!identical(names(veri), c("grup", "sonuc", "frekans")) || nrow(veri) != 4) {
    stop("Dort hucre ve grup, sonuc, frekans sutunlari gerekli.")
  }
  if (anyNA(veri) || any(duplicated(veri[c("grup", "sonuc")]))) stop("Eksik veya yinelenen hucre.")
  if (!all(veri$grup %in% GRUPLAR) || !all(veri$sonuc %in% SONUCLAR)) stop("Kategori etiketleri gecersiz.")
  if (!is.numeric(veri$frekans) || any(!is.finite(veri$frekans)) ||
      any(veri$frekans < 0 | veri$frekans != floor(veri$frekans))) stop("Negatif olmayan tam sayi frekans gerekli.")
  temiz <- veri[order(match(veri$grup, GRUPLAR), match(veri$sonuc, SONUCLAR)), ]
  rownames(temiz) <- NULL
  gozlenen <- matrix(temiz$frekans, nrow = 2, byrow = TRUE)
  if (any(rowSums(gozlenen) <= 0) || any(colSums(gozlenen) <= 0)) stop("Bos satir veya sutun kabul edilmez.")
  temiz
}

tablolar <- function(veri) {
  temiz <- hazirla(veri)
  gozlenen <- matrix(temiz$frekans, nrow = 2, byrow = TRUE, dimnames = list(GRUPLAR, SONUCLAR))
  beklenen <- outer(rowSums(gozlenen), colSums(gozlenen)) / sum(gozlenen)
  if (any(beklenen < 5)) stop("Bu pilot tum beklenen frekanslari >=5 ister; uygun kesin yontemi degerlendirin.")
  sonuc <- chisq.test(gozlenen, correct = FALSE)
  list(gozlenen = gozlenen, beklenen = sonuc$expected,
       katki = (gozlenen - sonuc$expected)^2 / sonuc$expected,
       pearson_artik = sonuc$residuals, satir_orani = prop.table(gozlenen, margin = 1),
       ki_kare = unname(sonuc$statistic), p = sonuc$p.value, serbestlik = unname(sonuc$parameter))
}

hesapla <- function(veri) {
  tablo <- tablolar(veri)
  hucreler <- paste(rep(GRUPLAR, each = 2), rep(SONUCLAR, times = 2), sep = "_")
  adlar <- c("gozlenen", "beklenen", "katki", "pearson_artik", "satir_orani")
  sonuc <- do.call(rbind, lapply(adlar, function(ad) {
    data.frame(degisken = ad, olcu = hucreler, deger = as.vector(t(tablo[[ad]])))
  }))
  gozlenen <- tablo$gozlenen
  toplamlar <- c(toplam = sum(gozlenen), satir_Birinci = sum(gozlenen[1, ]),
                 satir_Ikinci = sum(gozlenen[2, ]), sutun_Basarili = sum(gozlenen[, 1]),
                 sutun_Basarisiz = sum(gozlenen[, 2]))
  test <- c(ki_kare = tablo$ki_kare, serbestlik = tablo$serbestlik, p = tablo$p,
            cramer_v = sqrt(tablo$ki_kare / sum(gozlenen)), min_beklenen = min(tablo$beklenen),
            alfa = ALFA, reddet = as.integer(tablo$p < ALFA))
  sonuc <- rbind(sonuc, data.frame(degisken = "toplamlar", olcu = names(toplamlar), deger = unname(toplamlar)),
                 data.frame(degisken = "test", olcu = names(test), deger = unname(test)))
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
  tablo <- tablolar(veri)
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/oranlar-artiklar.png", width = 1500, height = 600, res = 150)
  on.exit(dev.off())
  par(mfrow = c(1, 2))
  yuzdeler <- t(tablo$satir_orani * 100)
  konumlar <- barplot(yuzdeler, beside = TRUE, col = c("#087F5B", "#1F4E79"),
                      ylim = c(0, 115), ylab = "Satir yuzdesi", main = "Grup icindeki sonuc oranlari")
  text(konumlar, yuzdeler + 4, sprintf("%.1f%%", yuzdeler), cex = .8)
  legend("topright", legend = SONUCLAR, fill = c("#087F5B", "#1F4E79"), cex = .8)
  artik <- tablo$pearson_artik
  sinir <- max(1, abs(artik))
  renkler <- colorRampPalette(c("#B2182B", "white", "#2166AC"))(101)
  plot(NA, xlim = c(.5, 2.5), ylim = c(.5, 2.5), xaxt = "n", yaxt = "n", xlab = "", ylab = "",
       main = "Pearson artiklari (O-E)/sqrt(E)")
  axis(1, at = 1:2, labels = SONUCLAR)
  axis(2, at = c(2, 1), labels = GRUPLAR, las = 1)
  for (satir in 1:2) {
    for (sutun in 1:2) {
      dikey <- 3 - satir
      renk <- round((artik[satir, sutun] / sinir + 1) * 50) + 1
      rect(sutun - .5, dikey - .5, sutun + .5, dikey + .5, col = renkler[renk], border = "white")
      text(sutun, dikey, sprintf("%+.4f", artik[satir, sutun]),
           col = if (abs(artik[satir, sutun]) > .6 * sinir) "white" else "black")
    }
  }
  cat("Grafik: ciktilar/r/oranlar-artiklar.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", stringsAsFactors = FALSE, check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()