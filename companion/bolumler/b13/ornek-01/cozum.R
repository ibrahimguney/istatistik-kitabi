ALFA <- 0.05
YENI_SAAT <- 6

hazirla <- function(veri) {
  if (!identical(names(veri), c("saat", "puan")) || nrow(veri) < 3) stop("En az uc eslesmis satir gerekli.")
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri))) || any(veri$saat < 0)) stop("Sonlu sayisal olcum ve negatif olmayan saat gerekli.")
  if (length(unique(veri$saat)) < 2 || length(unique(veri$puan)) < 2) stop("Sabit saat veya puan kabul edilmez.")
  rownames(veri) <- NULL
  veri
}

model_hesapla <- function(veri, yeni_saat = YENI_SAAT) {
  veri <- hazirla(veri)
  if (!is.numeric(yeni_saat) || length(yeni_saat) != 1 || !is.finite(yeni_saat) || yeni_saat < 0) stop("Yeni saat gecersiz.")
  model <- lm(puan ~ saat, data = veri)
  hacim <- nrow(veri)
  saat_ort <- mean(veri$saat)
  puan_ort <- mean(veri$puan)
  sxx <- sum((veri$saat - saat_ort)^2)
  syy <- sum((veri$puan - puan_ort)^2)
  sxy <- sum((veri$saat - saat_ort) * (veri$puan - puan_ort))
  artik <- unname(resid(model))
  uydurulan <- unname(fitted(model))
  sse <- sum(artik^2)
  if (sse <= .Machine$double.eps * syy) stop("Tam veya sayisal olarak tama yakin uyumda bu cikarim paketi durur.")
  ozet_model <- summary(model)
  serbestlik <- df.residual(model)
  mse <- sse / serbestlik
  egim <- unname(coef(model)["saat"])
  sabit <- unname(coef(model)["(Intercept)"])
  se_egim <- ozet_model$coefficients["saat", "Std. Error"]
  se_sabit <- ozet_model$coefficients["(Intercept)", "Std. Error"]
  araliklar <- confint(model, level = 1 - ALFA)
  yeni <- data.frame(saat = yeni_saat)
  ortalama_aralik <- predict(model, newdata = yeni, interval = "confidence", level = 1 - ALFA)
  birey_aralik <- predict(model, newdata = yeni, interval = "prediction", level = 1 - ALFA)
  se_ortalama <- unname(predict(model, newdata = yeni, se.fit = TRUE)$se.fit[1])
  ozet <- c(hacim = hacim, saat_ort = saat_ort, puan_ort = puan_ort, sxx = sxx, syy = syy, sxy = sxy,
             sse = sse, mse = mse, serbestlik = serbestlik, korelasyon = cor(veri$saat, veri$puan),
             r_kare = ozet_model$r.squared, egim = egim, sabit = sabit, se_egim = se_egim, se_sabit = se_sabit,
             t_egim = ozet_model$coefficients["saat", "t value"], p_egim = ozet_model$coefficients["saat", "Pr(>|t|)"],
             kritik_t = qt(1 - ALFA / 2, df = serbestlik), egim_alt = araliklar["saat", 1], egim_ust = araliklar["saat", 2],
             sabit_alt = araliklar["(Intercept)", 1], sabit_ust = araliklar["(Intercept)", 2],
             yeni_saat = yeni_saat, ongoru = ortalama_aralik[1, "fit"], se_ortalama = se_ortalama,
             se_birey = sqrt(mse + se_ortalama^2), ortalama_alt = ortalama_aralik[1, "lwr"],
             ortalama_ust = ortalama_aralik[1, "upr"], birey_alt = birey_aralik[1, "lwr"], birey_ust = birey_aralik[1, "upr"])
  if (any(!is.finite(ozet))) stop("Sonlu model sonucu hesaplanamadi.")
  list(ozet = ozet, uydurulan = uydurulan, artik = artik)
}

hesapla <- function(veri, yeni_saat = YENI_SAAT) {
  sonuc <- model_hesapla(veri, yeni_saat)
  satirlar <- sprintf("satir_%02d", seq_along(sonuc$artik))
  data.frame(degisken = c(rep("ozet", length(sonuc$ozet)), rep("uydurulan", length(satirlar)), rep("artik", length(satirlar))),
              olcu = c(names(sonuc$ozet), satirlar, satirlar),
              deger = c(unname(sonuc$ozet), sonuc$uydurulan, sonuc$artik))
}

kontrol_et <- function(sonuc, beklenen) {
  if (!identical(names(beklenen), c("degisken", "olcu", "deger")) ||
      !identical(sonuc$degisken, beklenen$degisken) || !identical(sonuc$olcu, beklenen$olcu)) stop("Kontrol etiketleri veya sirasi uyusmuyor.")
  if (!is.numeric(beklenen$deger) || any(!is.finite(beklenen$deger)) ||
      any(!is.finite(sonuc$deger))) stop("Sonlu kontrol degerleri gerekli.")
  tolerans <- pmax(1e-9, 1e-9 * pmax(abs(sonuc$deger), abs(beklenen$deger)))
  p_satiri <- sonuc$olcu == "p_egim"
  tolerans[p_satiri] <- 1e-8 * pmax(abs(sonuc$deger[p_satiri]), abs(beklenen$deger[p_satiri]))
  if (any(abs(sonuc$deger - beklenen$deger) > tolerans)) stop("Kontrol degerleri uyusmuyor.")
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}

grafik_kaydet <- function(veri) {
  veri <- hazirla(veri)
  sonuc <- model_hesapla(veri)
  ozet <- sonuc$ozet
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/regresyon-tani.png", width = 1500, height = 1200, res = 150)
  on.exit(dev.off())
  par(mfrow = c(2, 2))
  plot(puan ~ saat, data = veri, pch = 19, col = "#1F4E79", main = "Sacilim ve regresyon dogrusu")
  abline(a = ozet["sabit"], b = ozet["egim"], col = "#087F5B")
  plot(sonuc$uydurulan, sonuc$artik, pch = 19, xlab = "Uydurulan deger", ylab = "Ham artik", main = "Artik - uydurulan deger")
  abline(h = 0, lty = 2)
  qqnorm(sonuc$artik, main = "Normal Q-Q grafigi")
  qqline(sonuc$artik, lty = 2)
  plot(NA, xlim = range(ozet[c("birey_alt", "birey_ust")]) + c(-.5, .5), ylim = c(-.5, 1.6), yaxt = "n",
       xlab = "Puan", ylab = "", main = "6 saat: %95 araliklar")
  axis(2, at = c(0, 1), labels = c("Yeni birey", "Ortalama yanit"), las = 1, cex.axis = .7)
  for (tur in c("ortalama", "birey")) {
    konum <- if (tur == "ortalama") 1 else 0
    alt <- ozet[paste0(tur, "_alt")]
    ust <- ozet[paste0(tur, "_ust")]
    segments(alt, konum, ust, konum)
    points(ozet["ongoru"], konum, pch = 19)
    text(c(alt, ust), konum + .2, sprintf("%.3f", c(alt, ust)), cex = .7)
  }
  cat("Grafik: ciktilar/r/regresyon-tani.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE, digits = 10)
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()