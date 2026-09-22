ARAMA_UST <- 10000

hazirla <- function(veri, plan = FALSE) {
  sutunlar <- if (plan) c("hacim", "fark", "standart_sapma", "alfa", "hedef_guc") else
    c("hacim", "ortalama", "standart_sapma", "referans", "alfa")
  if (!identical(names(veri), sutunlar) || nrow(veri) != 1) stop("Tek ozet satiri ve dogru sutun sirasi gerekli.")
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu sayisal ozet gerekli.")
  if (veri$hacim < 2 || veri$hacim != floor(veri$hacim)) stop("Hacim en az 2 olan tam sayi olmali.")
  if (veri$standart_sapma <= 0 || veri$alfa <= 0 || veri$alfa >= 1) stop("Sapma veya alfa gecersiz.")
  if (plan && (veri$fark == 0 || veri$hedef_guc <= veri$alfa || veri$hedef_guc >= 1)) {
    stop("Hacim plani icin sifir olmayan etki ve alfa < hedef guc < 1 gerekli.")
  }
  veri
}

guc_hesapla <- function(hacim, etki, alfa) {
  if (any(!is.finite(c(hacim, etki, alfa))) || hacim < 2 || alfa <= 0 || alfa >= 1) {
    stop("Guc girdileri gecersiz.")
  }
  guc <- power.t.test(n = hacim, delta = abs(etki), sd = 1, sig.level = alfa,
                      type = "one.sample", alternative = "two.sided", strict = TRUE)$power
  if (!is.finite(guc) || guc < 0 || guc > 1) stop("Guc sayisal olarak hesaplanamadi.")
  guc
}

en_kucuk_hacim <- function(etki, alfa, hedef) {
  if (etki == 0 || hedef <= alfa || hedef >= 1) stop("Hacim plani girdileri gecersiz.")
  alt <- 2
  ust <- 2
  while (guc_hesapla(ust, etki, alfa) < hedef) {
    if (ust == ARAMA_UST) stop("Hedef 10000 gozleme kadar bulunamadi; arama siniri asildi.")
    ust <- min(2 * ust, ARAMA_UST)
  }
  while (alt < ust) {
    orta <- floor((alt + ust) / 2)
    if (guc_hesapla(orta, etki, alfa) >= hedef) ust <- orta else alt <- orta + 1
  }
  alt
}

hesapla <- function(veri, plan) {
  veri <- hazirla(veri)
  plan <- hazirla(plan, plan = TRUE)
  serbestlik <- veri$hacim - 1
  standart_hata <- veri$standart_sapma / sqrt(veri$hacim)
  t_degeri <- (veri$ortalama - veri$referans) / standart_hata
  p_degeri <- 2 * pt(abs(t_degeri), df = serbestlik, lower.tail = FALSE)
  kritik <- qt(1 - veri$alfa / 2, df = serbestlik)
  hata_payi <- kritik * standart_hata
  test <- c(serbestlik = serbestlik, standart_hata = standart_hata, t = t_degeri,
             p_cift = p_degeri, cohen_d = (veri$ortalama - veri$referans) / veri$standart_sapma,
             kritik_t = kritik, alt_sinir = veri$ortalama - hata_payi,
             ust_sinir = veri$ortalama + hata_payi, hata_payi = hata_payi,
             genislik = 2 * hata_payi, reddet_cift = as.integer(p_degeri < veri$alfa))
  etki <- plan$fark / plan$standart_sapma
  guc <- guc_hesapla(plan$hacim, etki, plan$alfa)
  gereken <- en_kucuk_hacim(etki, plan$alfa, plan$hedef_guc)
  guc_onceki <- if (gereken > 2) guc_hesapla(gereken - 1, etki, plan$alfa) else NA_real_
  tasarim <- c(plan_d = etki, plan_serbestlik = plan$hacim - 1,
                plan_kritik_t = qt(1 - plan$alfa / 2, df = plan$hacim - 1),
                merkezdisilik = abs(etki) * sqrt(plan$hacim), guc = guc, beta = 1 - guc,
                gereken_hacim = gereken, onceki_guc = guc_onceki,
                gereken_guc = guc_hesapla(gereken, etki, plan$alfa))
  sonuc <- data.frame(degisken = c(rep("girdi", 5), rep("plan_girdi", 5), rep("test", 11), rep("plan", 9)),
                       olcu = c(names(veri), names(plan), names(test), names(tasarim)),
                       deger = c(unlist(veri), unlist(plan), test, tasarim), row.names = NULL)
  if (any(!is.finite(sonuc$deger[sonuc$olcu != "onceki_guc"]))) stop("Sonuc hesaplanamadi.")
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

grafik_kaydet <- function(plan) {
  plan <- hazirla(plan, plan = TRUE)
  etki <- plan$fark / plan$standart_sapma
  gereken <- en_kucuk_hacim(etki, plan$alfa, plan$hedef_guc)
  ust <- min(ARAMA_UST, max(60, plan$hacim + 10, gereken + 10))
  hacimler <- unique(round(seq(2, ust, length.out = 120)))
  gucler <- vapply(hacimler, guc_hesapla, numeric(1), etki = etki, alfa = plan$alfa)
  kucuk_gucler <- vapply(hacimler, guc_hesapla, numeric(1), etki = etki / 2, alfa = plan$alfa)
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/guc-egrisi.png", width = 1200, height = 675, res = 150)
  on.exit(dev.off())
  plot(hacimler, gucler, type = "l", col = "#1F4E79", ylim = c(0, 1),
       xlab = "Bagimsiz gozlem sayisi n", ylab = "Iki tarafli test gucu",
       main = paste("Ileriye donuk tek orneklem t testi plani; alfa =", plan$alfa))
  lines(hacimler, kucuk_gucler, lty = 2, col = "#087F5B")
  abline(h = plan$hedef_guc, lty = 3, col = "#555555")
  points(gereken, guc_hesapla(gereken, etki, plan$alfa), pch = 19)
  text(gereken, guc_hesapla(gereken, etki, plan$alfa) - .06, paste("En kucuk n =", gereken))
  legend("bottomright", legend = c(paste("Planlanan |d| =", abs(etki)),
         paste("Planlanan |d| =", abs(etki) / 2), paste("Hedef guc =", plan$hedef_guc)),
         col = c("#1F4E79", "#087F5B", "#555555"), lty = c(1, 2, 3), cex = .8)
  cat("Grafik: ciktilar/r/guc-egrisi.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
plan <- read.csv("plan.csv", check.names = FALSE)
sonuc <- hesapla(veri, plan)
print(sonuc, row.names = FALSE)
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(plan)
sessionInfo()