args <- commandArgs(trailingOnly = TRUE)
if (any(!args %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek")
veri <- read.csv("veri.csv", check.names = FALSE)
yeni <- read.csv("yeni.csv", check.names = FALSE)
kontrol <- function(tablo, sutunlar, en_az) {
  stopifnot(identical(names(tablo), sutunlar), nrow(tablo) >= en_az)
  stopifnot(all(vapply(tablo, is.numeric, logical(1))), all(is.finite(as.matrix(tablo))))
  stopifnot(all(tablo$saat >= 0), all(tablo$devamsizlik >= 0))
  stopifnot(all(tablo$devamsizlik == floor(tablo$devamsizlik)))
}
kontrol(veri, c("saat", "devamsizlik", "puan"), 4)
kontrol(yeni, c("saat", "devamsizlik"), 1)
stopifnot(nrow(yeni) == 1, length(unique(veri$puan)) > 1)
tasarim <- model.matrix(~ saat + devamsizlik, data = veri)
stopifnot(qr(tasarim)$rank == 3, kappa(tasarim, exact = TRUE) <= 1e12)
model <- lm(puan ~ saat + devamsizlik, data = veri, na.action = na.fail)
ozet <- summary(model)
artik <- residuals(model)
sse <- sum(artik^2)
sst <- sum((veri$puan - mean(veri$puan))^2)
stopifnot(sse > .Machine$double.eps * sst)
hacim <- nrow(veri)
serbestlik <- df.residual(model)
mse <- sse / serbestlik
kritik <- qt(.975, serbestlik)
ekle <- function(grup, degerler) {
  data.frame(degisken = grup, olcu = names(degerler), deger = unname(degerler), row.names = NULL)
}
sonuc <- ekle("model", c(n = hacim, serbestlik = serbestlik, sse = sse, sst = sst,
  mse = mse, artik_sd = sqrt(mse), r_kare = ozet$r.squared,
  duzeltilmis_r_kare = ozet$adj.r.squared, f = unname(ozet$fstatistic[1]),
  p_f = pf(unname(ozet$fstatistic[1]), 2, serbestlik, lower.tail = FALSE), alfa = .05, kritik_t = kritik))
rownames(sonuc) <- NULL
araliklar <- confint(model, level = .95)
for (sira in seq_len(3)) {
  grup <- c("sabit", "saat", "devamsizlik")[sira]
  degerler <- unname(coef(ozet)[sira, ])
  sonuc <- rbind(sonuc, ekle(grup, c(katsayi = degerler[1], se = degerler[2],
    t = degerler[3], p = degerler[4], alt = araliklar[sira, 1], ust = araliklar[sira, 2])))
}
yardimci_saat <- lm(saat ~ devamsizlik, data = veri)
yardimci_devam <- lm(devamsizlik ~ saat, data = veri)
sonuc <- rbind(sonuc, ekle("vif", c(saat = 1 / (1 - summary(yardimci_saat)$r.squared),
  devamsizlik = 1 / (1 - summary(yardimci_devam)$r.squared))))
ortalama <- predict(model, newdata = yeni, interval = "confidence", level = .95)
birey <- predict(model, newdata = yeni, interval = "prediction", level = .95)
se_ortalama <- unname(predict(model, newdata = yeni, se.fit = TRUE)$se.fit)
sonuc <- rbind(sonuc, ekle("yeni", c(saat = yeni$saat, devamsizlik = yeni$devamsizlik,
  ongoru = ortalama[1, 1], h_yeni = se_ortalama^2 / mse, se_ortalama = se_ortalama,
  se_birey = sqrt(mse + se_ortalama^2), ortalama_alt = ortalama[1, 2],
  ortalama_ust = ortalama[1, 3], birey_alt = birey[1, 2], birey_ust = birey[1, 3])))
for (sira in seq_len(hacim)) {
  sonuc <- rbind(sonuc, ekle(sprintf("satir_%02d", sira), c(
    uydurulan = unname(fitted(model)[sira]), artik = unname(artik[sira]))))
}
stopifnot(all(is.finite(sonuc$deger)))
print(sonuc, row.names = FALSE, digits = 12)
if ("--check" %in% args) {
  beklenen <- read.csv("beklenen-sonuclar.csv", check.names = FALSE)
  stopifnot(identical(names(beklenen), names(sonuc)))
  stopifnot(identical(sonuc[c("degisken", "olcu")], beklenen[c("degisken", "olcu")]))
  stopifnot(is.numeric(beklenen$deger), all(is.finite(beklenen$deger)))
  p_kontrol <- sonuc$olcu %in% c("p", "p_f")
  tolerans <- ifelse(p_kontrol, 1e-8 * abs(beklenen$deger), 1e-9 + 1e-9 * abs(beklenen$deger))
  stopifnot(all(abs(sonuc$deger - beklenen$deger) <= tolerans))
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}
if ("--grafik" %in% args) {
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/coklu-regresyon-tani.png", width = 1200, height = 500)
  par(mfrow = c(1, 2))
  plot(fitted(model), artik, xlab = "Uydurulan puan", ylab = "Artik")
  abline(h = 0, lty = 2)
  qqnorm(artik)
  qqline(artik)
  dev.off()
}
for (sutun in c("saat", "devamsizlik")) {
  if (yeni[[sutun]] < min(veri[[sutun]]) || yeni[[sutun]] > max(veri[[sutun]])) {
    warning(paste("Ekstrapolasyon:", sutun))
  }
}
sessionInfo()