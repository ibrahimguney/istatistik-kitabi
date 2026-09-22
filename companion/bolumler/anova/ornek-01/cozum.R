args <- commandArgs(trailingOnly = TRUE)
if (any(!args %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek")
klasik <- read.csv("veri.csv", check.names = FALSE)
welch <- read.csv("welch.csv", check.names = FALSE)
ciftler <- read.csv("ciftler.csv", check.names = FALSE)
sayisal <- function(tablo, sutunlar) {
  stopifnot(identical(names(tablo), sutunlar), nrow(tablo) == 3)
  stopifnot(all(vapply(tablo, is.numeric, logical(1))), all(is.finite(as.matrix(tablo))))
}
for (tablo in list(klasik, welch)) {
  stopifnot(identical(names(tablo), c("grup", "n", "ortalama", "standart_sapma")))
  stopifnot(nrow(tablo) == 3, identical(tablo$grup, c("A", "B", "C")))
  sayisal(tablo[c("n", "ortalama", "standart_sapma")], c("n", "ortalama", "standart_sapma"))
  stopifnot(all(tablo$n >= 2), all(tablo$n == floor(tablo$n)), all(tablo$standart_sapma > 0))
}
sayisal(ciftler, c("cift", "ilk", "ikinci"))
stopifnot(all(as.matrix(ciftler) == matrix(c(1,1,2,2,1,3,3,2,3), nrow = 3, byrow = TRUE)))
ekle <- function(grup, degerler) {
  data.frame(degisken = grup, olcu = names(degerler), deger = unname(degerler), row.names = NULL)
}
sonuc <- data.frame(degisken = character(), olcu = character(), deger = numeric())
for (ad in c("klasik", "welch")) {
  tablo <- if (ad == "klasik") klasik else welch
  for (sira in 1:3) {
    sonuc <- rbind(sonuc, ekle(paste0("girdi_", ad, "_", tablo$grup[sira]),
      c(n = tablo$n[sira], ortalama = tablo$ortalama[sira], standart_sapma = tablo$standart_sapma[sira])))
  }
}
hacim <- klasik$n
ortalama <- klasik$ortalama
sapma <- klasik$standart_sapma
grup_sayisi <- length(hacim)
toplam <- sum(hacim)
genel <- weighted.mean(ortalama, hacim)
ss_grup <- sum(hacim * (ortalama - genel)^2)
ss_hata <- sum((hacim - 1) * sapma^2)
sd_grup <- grup_sayisi - 1
sd_hata <- toplam - grup_sayisi
mse <- ss_hata / sd_hata
ms_grup <- ss_grup / sd_grup
f_degeri <- ms_grup / mse
p_degeri <- pf(f_degeri, sd_grup, sd_hata, lower.tail = FALSE)
kritik <- qtukey(.95, nmeans = grup_sayisi, df = sd_hata)
sonuc <- rbind(sonuc, ekle("klasik", c(grup_sayisi = grup_sayisi, toplam_n = toplam, genel_ortalama = genel,
  ss_grup = ss_grup, ss_hata = ss_hata, ss_toplam = ss_grup + ss_hata,
  sd_grup = sd_grup, sd_hata = sd_hata, ms_grup = ms_grup, mse = mse,
  f = f_degeri, p = p_degeri, eta2 = ss_grup / (ss_grup + ss_hata),
  omega2 = (ss_grup - sd_grup * mse) / (ss_grup + ss_hata + mse),
  alfa = .05, q_kritik = kritik)))
for (sira in 1:3) {
  ilk <- ciftler$ilk[sira]
  ikinci <- ciftler$ikinci[sira]
  fark <- ortalama[ilk] - ortalama[ikinci]
  se_q <- sqrt(mse / 2 * (1 / hacim[ilk] + 1 / hacim[ikinci]))
  q_degeri <- abs(fark) / se_q
  p_duzeltilmis <- ptukey(q_degeri, nmeans = grup_sayisi, df = sd_hata, lower.tail = FALSE)
  sonuc <- rbind(sonuc, ekle(paste0("tukey_", c("A-B", "A-C", "B-C")[sira]), c(
    fark = fark, se_q = se_q, q = q_degeri, yari_genislik = kritik * se_q, alt = fark - kritik * se_q,
    ust = fark + kritik * se_q, p_duzeltilmis = p_duzeltilmis, reddet = as.integer(p_duzeltilmis < .05))))
}
hacim <- welch$n
ortalama <- welch$ortalama
agirlik <- hacim / welch$standart_sapma^2
pay <- agirlik / sum(agirlik)
merkez <- sum(pay * ortalama)
duzeltme <- sum((1 - pay)^2 / (hacim - 1))
carpan <- 1 + 2 * (grup_sayisi - 2) * duzeltme / (grup_sayisi^2 - 1)
f_welch <- (sum(agirlik * (ortalama - merkez)^2) / (grup_sayisi - 1)) / carpan
sd_payda <- (grup_sayisi^2 - 1) / (3 * duzeltme)
p_welch <- pf(f_welch, grup_sayisi - 1, sd_payda, lower.tail = FALSE)
sonuc <- rbind(sonuc, ekle("welch", c(grup_sayisi = grup_sayisi, toplam_n = sum(hacim), agirlik_toplami = sum(agirlik),
  agirlikli_merkez = merkez, duzeltme = duzeltme,
  pay = sum(agirlik * (ortalama - merkez)^2) / (grup_sayisi - 1), duzeltme_carpani = carpan,
  f = f_welch, sd_pay = grup_sayisi - 1, sd_payda = sd_payda, p = p_welch, alfa = .05)))
stopifnot(all(is.finite(sonuc$deger)))
print(sonuc, row.names = FALSE, digits = 12)
if ("--check" %in% args) {
  beklenen <- read.csv("beklenen-sonuclar.csv", check.names = FALSE)
  stopifnot(identical(names(sonuc), names(beklenen)))
  stopifnot(identical(sonuc[c("degisken", "olcu")], beklenen[c("degisken", "olcu")]))
  stopifnot(is.numeric(beklenen$deger), all(is.finite(beklenen$deger)))
  tolerans <- 1e-9 + 1e-9 * abs(beklenen$deger)
  tolerans[sonuc$olcu == "p"] <- 1e-8 * abs(beklenen$deger[sonuc$olcu == "p"])
  tolerans[sonuc$olcu == "q_kritik"] <- 1e-4
  tolerans[sonuc$olcu == "p_duzeltilmis"] <- 1e-6
  for (ad in paste0("tukey_", c("A-B", "A-C", "B-C"))) {
    se_q <- beklenen$deger[beklenen$degisken == ad & beklenen$olcu == "se_q"]
    secim <- sonuc$degisken == ad & sonuc$olcu %in% c("alt", "ust", "yari_genislik")
    tolerans[secim] <- 1e-4 * se_q + 1e-8
  }
  p_satirlari <- sonuc$olcu %in% c("p", "p_duzeltilmis")
  stopifnot(all(sonuc$deger[p_satirlari & beklenen$deger > 0] > 0))
  stopifnot(all(abs(sonuc$deger - beklenen$deger) <= tolerans))
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor; Tukey icin belgelenmis diller arasi toleranslar kullanildi.\n")
}
if ("--grafik" %in% args) {
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/tukey-araliklari.png", width = 1100, height = 600)
  farklar <- sonuc$deger[sonuc$olcu == "fark"]
  altlar <- sonuc$deger[sonuc$olcu == "alt"]
  ustler <- sonuc$deger[sonuc$olcu == "ust"]
  plot(farklar, 3:1, xlim = range(c(altlar, ustler, 0)), ylim = c(.5, 3.5),
       yaxt = "n", xlab = "Ilk grup - ikinci grup farki (puan)", ylab = "",
       main = "%95 Tukey eszamanli araliklari", pch = 19)
  segments(altlar, 3:1, ustler, 3:1)
  axis(2, at = 3:1, labels = c("A-B", "A-C", "B-C"), las = 1)
  abline(v = 0, lty = 2)
  dev.off()
}
sessionInfo()