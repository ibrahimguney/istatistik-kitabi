hazirla <- function(veri) {
  if (!identical(names(veri), c("cift_sayisi", "ortalama_fark", "fark_sapmasi", "alfa")) || nrow(veri) != 1) {
    stop("Tek ozet satiri ve dogru sutun sirasi gerekli.")
  }
  if (!all(vapply(veri, is.numeric, logical(1))) || anyNA(veri) ||
      any(!is.finite(as.matrix(veri)))) stop("Sonlu sayisal ozet gerekli.")
  if (veri$cift_sayisi < 2 || veri$cift_sayisi != floor(veri$cift_sayisi)) stop("Tam cift sayisi en az 2 olan tam sayi olmali.")
  if (veri$fark_sapmasi <= 0) stop("Farklarin standart sapmasi pozitif olmali.")
  if (veri$alfa <= 0 || veri$alfa >= 1) stop("Alfa 0 ile 1 arasinda olmali.")
  veri
}

test_hesapla <- function(veri) {
  veri <- hazirla(veri)
  standart_hata <- veri$fark_sapmasi / sqrt(veri$cift_sayisi)
  serbestlik <- veri$cift_sayisi - 1
  t_degeri <- veri$ortalama_fark / standart_hata
  p_degeri <- 2 * pt(abs(t_degeri), df = serbestlik, lower.tail = FALSE)
  kritik <- qt(1 - veri$alfa / 2, df = serbestlik)
  hata_payi <- kritik * standart_hata
  alt <- veri$ortalama_fark - hata_payi
  ust <- veri$ortalama_fark + hata_payi
  sonuc <- c(standart_hata = standart_hata, serbestlik = serbestlik, t = t_degeri, p_cift = p_degeri,
              dz = veri$ortalama_fark / veri$fark_sapmasi, kritik_t = kritik, hata_payi = hata_payi,
              alt_sinir = alt, ust_sinir = ust, genislik = 2 * hata_payi,
              reddet = as.integer(p_degeri < veri$alfa), sifir_aralikta = as.integer(alt <= 0 && 0 <= ust),
              guven_duzeyi = 1 - veri$alfa)
  if (any(!is.finite(sonuc))) stop("Sonlu test sonucu hesaplanamadi.")
  sonuc
}

hesapla <- function(veri) {
  veri <- hazirla(veri)
  test <- test_hesapla(veri)
  data.frame(degisken = c(rep("girdi", 4), rep("test", length(test))), olcu = c(names(veri), names(test)),
              deger = c(as.numeric(unlist(veri)), as.numeric(test)))
}

kontrol_et <- function(sonuc, beklenen) {
  if (!identical(names(beklenen), c("degisken", "olcu", "deger")) ||
      !identical(sonuc$degisken, beklenen$degisken) || !identical(sonuc$olcu, beklenen$olcu)) stop("Kontrol etiketleri veya sirasi uyusmuyor.")
  if (!is.numeric(beklenen$deger) || any(!is.finite(beklenen$deger)) ||
      any(!is.finite(sonuc$deger))) stop("Sonlu kontrol degerleri gerekli.")
  tolerans <- pmax(1e-9, 1e-9 * pmax(abs(sonuc$deger), abs(beklenen$deger)))
  if (any(abs(sonuc$deger - beklenen$deger) > tolerans)) stop("Kontrol degerleri uyusmuyor.")
  cat("DOGRULANDI:", nrow(sonuc), "kontrol degeri eslesiyor.\n")
}

grafik_kaydet <- function(veri) {
  veri <- hazirla(veri)
  sonuc <- test_hesapla(veri)
  aralik <- sonuc[c("alt_sinir", "ust_sinir")]
  pay <- .35 * sonuc["hata_payi"]
  dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
  png("ciktilar/r/son-on-araligi.png", width = 1200, height = 450, res = 150)
  on.exit(dev.off())
  plot(NA, xlim = range(c(0, aralik)) + c(-pay, pay), ylim = c(-.5, .7), yaxt = "n", ylab = "",
       xlab = "Evren ortalama farki: son - on (puan)",
       main = paste("Eslestirilmis test; guven:", 1 - veri$alfa, "; p =", format(sonuc["p_cift"], digits = 5)))
  segments(aralik[1], 0, aralik[2], 0, col = "#1F4E79", lwd = 2)
  points(veri$ortalama_fark, 0, col = "#1F4E79", pch = 19)
  abline(v = 0, lty = 2, col = "#555555")
  for (uc in aralik) {
    segments(uc, -.06, uc, .06, col = "#1F4E79")
    text(uc, .2, sprintf("%.4f", uc))
  }
  cat("Grafik: ciktilar/r/son-on-araligi.png\n")
}

secenek <- commandArgs(trailingOnly = TRUE)
if (any(!secenek %in% c("--check", "--grafik"))) stop("Bilinmeyen secenek.")
veri <- read.csv("veri.csv", check.names = FALSE)
sonuc <- hesapla(veri)
print(sonuc, row.names = FALSE)
cat(if (test_hesapla(veri)["reddet"] == 1) "H0 reddedilir" else "H0 reddedilemez", "\n")
if ("--check" %in% secenek) kontrol_et(sonuc, read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE))
if ("--grafik" %in% secenek) grafik_kaydet(veri)
sessionInfo()