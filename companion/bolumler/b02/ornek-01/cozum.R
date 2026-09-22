veri <- read.csv("veri.csv", stringsAsFactors = FALSE,
                 fileEncoding = "UTF-8",
                 colClasses = c("character", "numeric", "numeric"))
stopifnot(identical(names(veri), c("okul_turu", "sinif", "puan")),
          nrow(veri) > 0, !anyNA(veri),
          all(veri$okul_turu %in% c("Devlet", "Ozel")),
          all(is.finite(veri$sinif)), all(is.finite(veri$puan)),
          all(veri$sinif %in% c(1, 2, 3)))
veri$okul_turu <- factor(veri$okul_turu, levels = c("Devlet", "Ozel"))
veri$sinif <- ordered(veri$sinif, levels = c(1, 2, 3))
sonuc <- data.frame(
  degisken = "veri", olcu = c("satir_sayisi", "degisken_sayisi"),
  deger = c(nrow(veri), ncol(veri))
)
for (alan in c("okul_turu", "sinif", "puan")) {
  sonuc <- rbind(sonuc, data.frame(
    degisken = alan, olcu = c("gecerli", "eksik"),
    deger = c(sum(!is.na(veri[[alan]])), sum(is.na(veri[[alan]])))
  ))
}
for (alan in c("okul_turu", "sinif")) {
  for (kategori in levels(veri[[alan]])) {
    frekans <- sum(veri[[alan]] == kategori)
    sonuc <- rbind(sonuc, data.frame(
      degisken = alan, olcu = paste0(kategori, c("_frekans", "_oran")),
      deger = c(frekans, frekans / nrow(veri))
    ))
  }
}
sonuc <- rbind(sonuc, data.frame(
  degisken = "puan", olcu = c("ortalama", "en_kucuk", "en_buyuk"),
  deger = c(mean(veri$puan), min(veri$puan), max(veri$puan))
))
for (okul in c("Devlet", "Ozel")) {
  sonuc <- rbind(sonuc, data.frame(
    degisken = "puan", olcu = paste0(okul, "_ortalama"),
    deger = mean(veri$puan[veri$okul_turu == okul])
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