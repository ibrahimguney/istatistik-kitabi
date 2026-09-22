sayisal_veri <- function(veri, sutunlar) {
  if (!identical(names(veri), sutunlar) || nrow(veri) == 0) {
    stop("Bos veri veya yanlis sutun duzeni.")
  }
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu, eksiksiz sayisal veri gerekli.")
  veri
}

ciftleri_uret <- function(evren) {
  degerler <- sayisal_veri(evren, "deger")$deger
  if (length(degerler) < 2 || anyDuplicated(degerler)) {
    stop("En az iki farkli, esit olasilikli evren degeri gerekli.")
  }
  expand.grid(ikinci = degerler, ilk = degerler,
              KEEP.OUT.ATTRS = FALSE)[c("ilk", "ikinci")]
}

hazirla <- function(evren, veri) {
  beklenen <- ciftleri_uret(evren)
  ciftler <- sayisal_veri(veri, c("ilk", "ikinci"))
  if (nrow(ciftler) != nrow(beklenen)) stop("Sirali cift sayisi uyusmuyor.")
  sirali <- ciftler[order(ciftler$ilk, ciftler$ikinci), ]
  hedef <- beklenen[order(beklenen$ilk, beklenen$ikinci), ]
  if (!all(as.matrix(sirali) == as.matrix(hedef))) {
    stop("veri.csv tum sirali ciftleri birer kez icermeli.")
  }
  ciftler
}

dagilim_hesapla <- function(evren, veri) {
  ortalamalar <- rowMeans(hazirla(evren, veri))
  degerler <- sort(unique(ortalamalar))
  frekans <- vapply(degerler, function(deger) sum(ortalamalar == deger), numeric(1))
  list(ortalamalar = ortalamalar,
       dagilim = data.frame(ortalama = degerler, frekans = frekans,
                            olasilik = frekans / length(ortalamalar)))
}

hesapla <- function(evren, veri) {
  sonuc <- dagilim_hesapla(evren, veri)
  ortalamalar <- sonuc$ortalamalar
  dagilim <- sonuc$dagilim
  mu <- mean(evren$deger)
  evren_varyansi <- mean((evren$deger - mu)^2)
  merkez <- mean(ortalamalar)
  varyans <- mean((ortalamalar - merkez)^2)
  ozet <- data.frame(
    degisken = c(rep("evren", 4), rep("tasarim", 3), rep("orneklem_ortalamasi", 7)),
    olcu = c("hacim", "ortalama", "varyans", "standart_sapma",
             "orneklem_hacmi", "sirali_sonuc_sayisi", "olasilik_toplami",
             "beklenen_deger", "varyans", "standart_hata", "kuramsal_standart_hata",
             "yanlilik", "p_en_az_7", "p_esit_5"),
    deger = c(nrow(evren), mu, evren_varyansi, sqrt(evren_varyansi),
              2, length(ortalamalar), sum(dagilim$olasilik), merkez, varyans,
              sqrt(varyans), sqrt(evren_varyansi / 2), merkez - mu,
              mean(ortalamalar >= 7), mean(ortalamalar == 5)),
    stringsAsFactors = FALSE
  )
  for (index in seq_len(nrow(dagilim))) {
    etiket <- paste0("ortalama_", sprintf("%.15g", dagilim$ortalama[index]))
    ozet <- rbind(ozet, data.frame(degisken = rep(etiket, 2),
                 olcu = c("frekans", "olasilik"),
                 deger = c(dagilim$frekans[index], dagilim$olasilik[index])))
  }
  ozet
}

kontrol_et <- function(sonuc, beklenen) {
  if (!identical(names(beklenen), c("degisken", "olcu", "deger")) ||
      !identical(sonuc$degisken, beklenen$degisken) ||
      !identical(sonuc$olcu, beklenen$olcu)) stop("Kontrol etiketleri uyusmuyor.")
  if (!is.numeric(beklenen$deger) || anyNA(beklenen$deger) ||
      any(!is.finite(beklenen$deger)) || any(!is.finite(sonuc$deger))) {
    stop("Kontrol degerleri sonlu olmali.")
  }
  tolerans <- pmax(1e-9, 1e-9 * pmax(abs(sonuc$deger), abs(beklenen$deger)))
  if (any(abs(sonuc$deger - beklenen$deger) > tolerans)) stop("Kontrol uyusmazligi.")
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}

grafik_kaydet <- function(evren, veri) {
  dagilim <- dagilim_hesapla(evren, veri)$dagilim
  degerler <- sort(evren$deger)
  eksen <- sort(unique(c(degerler, dagilim$ortalama)))
  ust <- max(1 / length(degerler), dagilim$olasilik) * 1.2
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/ornekleme-dagilimi.png", width = 1500, height = 600, res = 150)
  on.exit(dev.off())
  par(mfrow = c(1, 2))
  plot(degerler, rep(1 / length(degerler), length(degerler)), type = "h", lwd = 8,
       col = "#8FB8D8", xlim = range(eksen) + c(-0.5, 0.5), ylim = c(0, ust),
       xaxt = "n", xlab = "Deger", ylab = "Olasilik", main = "Tek cekim X")
  axis(1, at = eksen)
  abline(v = mean(degerler), col = "#087F5B", lty = 2)
  plot(dagilim$ortalama, dagilim$olasilik, type = "h", lwd = 8,
       col = "#1F4E79", xlim = range(eksen) + c(-0.5, 0.5), ylim = c(0, ust),
       xaxt = "n", xlab = "Orneklem ortalamasi", ylab = "Olasilik",
       main = "Iki cekimin ortalamasi")
  axis(1, at = eksen)
  abline(v = mean(degerler), col = "#087F5B", lty = 2)
  cat("Grafik: ciktilar/r/ornekleme-dagilimi.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
evren <- read.csv("evren.csv", check.names = FALSE)
veri <- read.csv("veri.csv", check.names = FALSE)
sonuc <- hesapla(evren, veri)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) {
  kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
}
if ("--grafik" %in% secenek) grafik_kaydet(evren, veri)
sessionInfo()