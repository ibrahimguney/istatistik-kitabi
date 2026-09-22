RNGkind(kind = "Mersenne-Twister", normal.kind = "Inversion", sample.kind = "Rejection")
set.seed(2026)
cerceve <- data.frame(id = 1:12, sinif = factor(rep(1:3, each = 4)))
basit <- cerceve[sample.int(nrow(cerceve), 6), ]
indisler <- split(seq_len(nrow(cerceve)), cerceve$sinif)
secilen <- unlist(lapply(indisler, function(indis) sample(indis, 2)), use.names = FALSE)
tabakali <- cerceve[secilen, ]
veri <- data.frame(id = cerceve$id, sinif = as.integer(as.character(cerceve$sinif)),
                   basit = as.integer(cerceve$id %in% basit$id),
                   tabakali = as.integer(cerceve$id %in% tabakali$id))
stopifnot(nrow(basit) == 6, anyDuplicated(basit$id) == 0,
          all(table(tabakali$sinif) == 2))
hedef <- "ciktilar/r/yeni-secim.csv"
if (file.exists(hedef)) stop("Cikti zaten var; once ayri bir adla saklayin.")
dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
write.csv(veri, hedef, row.names = FALSE)
print(basit)
tabakali$secim_olasiligi <- 2 / 4
tabakali$agirlik <- 1 / tabakali$secim_olasiligi
print(tabakali)
print(table(tabakali$sinif))
print(sum(tabakali$agirlik))
cat("R'de yeni secim; kimliklerin Python secimiyle esit olmasi beklenmez.\n")
sessionInfo()