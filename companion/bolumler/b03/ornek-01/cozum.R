hazirla <- function(veri) {
  if (!identical(names(veri), "saat")) stop("CSV yalniz saat sutununu icermeli.")
  if (nrow(veri) < 2) stop("En az iki gozlem gerekli.")
  if (!is.numeric(veri$saat) || anyNA(veri$saat) ||
      any(!is.finite(veri$saat)) || any(veri$saat < 0)) {
    stop("Sureler eksiksiz, sayisal, sonlu ve negatif olmayan degerler olmali.")
  }
  veri
}

histogram_ozeti <- function(saat) {
  ust <- max(15, 3 * ceiling(max(saat) / 3))
  sinirlar <- seq(0, ust, by = 3)
  gruplar <- cut(saat, breaks = sinirlar, right = FALSE, include.lowest = TRUE)
  sayilar <- as.numeric(table(gruplar))
  etiketler <- paste0("[", head(sinirlar, -1), ";", tail(sinirlar, -1),
                      c(rep(")", length(sayilar) - 1), "]"))
  list(sinirlar = sinirlar, sayilar = sayilar, etiketler = etiketler)
}

kutu_ozeti <- function(saat) {
  ceyrek <- as.numeric(quantile(saat, c(0.25, 0.5, 0.75), type = 7))
  iqr <- ceyrek[3] - ceyrek[1]
  alt <- ceyrek[1] - 1.5 * iqr
  ust <- ceyrek[3] + 1.5 * iqr
  aykiri <- saat < alt | saat > ust
  list(q1 = ceyrek[1], medyan = ceyrek[2], q3 = ceyrek[3],
       alt = alt, ust = ust, aykiri = saat[aykiri],
       biyik_alt = min(saat[!aykiri]), biyik_ust = max(saat[!aykiri]))
}

hesapla <- function(veri) {
  saat <- hazirla(veri)$saat
  kutu <- kutu_ozeti(saat)
  duyarlilik <- saat[saat != 13]
  histogram <- histogram_ozeti(saat)
  data.frame(
    degisken = c(rep("veri", 2), rep("saat", 16),
                 rep("duyarlilik_13_haric", 3), rep("histogram", length(histogram$sayilar))),
    olcu = c("satir_sayisi", "degisken_sayisi", "gecerli", "eksik",
             "toplam", "ortalama", "medyan", "en_kucuk", "en_buyuk", "aciklik",
             "orneklem_varyansi", "orneklem_std", "q1", "q3", "iqr",
             "alt_sinir", "ust_sinir", "aykiri_sayisi", "hacim", "ortalama", "medyan",
             histogram$etiketler),
    deger = c(length(saat), 1, length(saat), 0, sum(saat), mean(saat), median(saat),
              min(saat), max(saat), diff(range(saat)), var(saat), sd(saat),
              kutu$q1, kutu$q3, kutu$q3 - kutu$q1, kutu$alt, kutu$ust,
              length(kutu$aykiri), length(duyarlilik),
              if (length(duyarlilik)) mean(duyarlilik) else NA_real_,
              if (length(duyarlilik)) median(duyarlilik) else NA_real_,
              histogram$sayilar),
    stringsAsFactors = FALSE
  )
}

kontrol_et <- function(sonuc, beklenen) {
  if (!identical(names(beklenen), c("degisken", "olcu", "deger")) ||
      nrow(sonuc) != nrow(beklenen) ||
      !identical(sonuc$degisken, beklenen$degisken) ||
      !identical(sonuc$olcu, beklenen$olcu)) stop("Kontrol etiketleri uyusmuyor.")
  if (!is.numeric(beklenen$deger) || anyNA(beklenen$deger) ||
      any(!is.finite(beklenen$deger)) || anyNA(sonuc$deger) ||
      any(!is.finite(sonuc$deger))) stop("Kontrol degerleri sonlu olmali.")
  fark <- abs(sonuc$deger - beklenen$deger)
  tolerans <- pmax(1e-9, 1e-9 * pmax(abs(sonuc$deger), abs(beklenen$deger)))
  if (any(fark > tolerans)) stop("Kontrol degeri uyusmuyor.")
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}

grafik_kaydet <- function(veri) {
  saat <- hazirla(veri)$saat
  kutu <- kutu_ozeti(saat)
  histogram <- histogram_ozeti(saat)
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/betimsel-grafikler.png", width = 1500, height = 600, res = 150)
  on.exit(dev.off())
  par(mfrow = c(1, 2))
  hist(saat, breaks = histogram$sinirlar, right = FALSE, include.lowest = TRUE,
       fuzz = 0, main = "Histogram", xlab = "Haftalik calisma suresi (saat)",
       ylab = "Frekans", col = "#8FB8D8", border = "white")
  ozet <- list(stats = matrix(c(kutu$biyik_alt, kutu$q1, kutu$medyan,
                               kutu$q3, kutu$biyik_ust), ncol = 1),
               n = length(saat), conf = matrix(NA_real_, nrow = 2, ncol = 1),
               out = kutu$aykiri, group = rep(1L, length(kutu$aykiri)), names = "Saat")
  bxp(ozet, horizontal = TRUE, main = "Kutu grafigi (type 7)",
      xlab = "Haftalik calisma suresi (saat)")
  cat("Grafik: ciktilar/r/betimsel-grafikler.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", stringsAsFactors = FALSE, check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) {
  kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
}
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()