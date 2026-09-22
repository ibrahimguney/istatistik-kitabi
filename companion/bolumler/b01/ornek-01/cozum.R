veri <- read.csv("veri.csv", stringsAsFactors = FALSE,
                 fileEncoding = "UTF-8")
stopifnot(identical(names(veri),
                    c("devam_saati", "basari", "program")),
          nrow(veri) > 0, !anyNA(veri),
          all(veri$program %in% c("A", "B")),
          is.numeric(veri$devam_saati), is.numeric(veri$basari),
          all(is.finite(veri$devam_saati)),
          all(is.finite(veri$basari)),
          all(veri$devam_saati >= 0))
veri$program <- factor(veri$program, levels = c("A", "B"))
sonuc <- data.frame(
  degisken = "veri",
  olcu = c("satir_sayisi", "degisken_sayisi"),
  deger = c(nrow(veri), ncol(veri))
)
for (alan in c("devam_saati", "basari")) {
  degerler <- veri[[alan]]
  ozet <- data.frame(
    degisken = alan,
    olcu = c("gecerli", "eksik", "ortalama", "en_kucuk", "en_buyuk"),
    deger = c(sum(!is.na(degerler)), sum(is.na(degerler)),
              mean(degerler), min(degerler), max(degerler))
  )
  sonuc <- rbind(sonuc, ozet)
}
sonuc <- rbind(sonuc, data.frame(
  degisken = "program", olcu = c("gecerli", "eksik"),
  deger = c(sum(!is.na(veri$program)), sum(is.na(veri$program)))
))
for (program in c("A", "B")) {
  frekans <- sum(veri$program == program)
  sonuc <- rbind(sonuc, data.frame(
    degisken = "program",
    olcu = paste0(program, c("_frekans", "_oran")),
    deger = c(frekans, frekans / nrow(veri))
  ))
}
cat(R.version.string, "\n")
print(sonuc, row.names = FALSE)
if ("--check" %in% commandArgs(trailingOnly = TRUE)) {
  beklenen <- read.csv("beklenen-sonuclar.csv", stringsAsFactors = FALSE)
  stopifnot(nrow(sonuc) == nrow(beklenen),
            all(sonuc$degisken == beklenen$degisken),
            all(sonuc$olcu == beklenen$olcu),
            isTRUE(all.equal(sonuc$deger, beklenen$deger,
                             tolerance = 1e-9, check.attributes = FALSE)))
  cat("DOGRULANDI:", nrow(beklenen), "kontrol degeri eslesiyor.\n")
}