RNGkind(kind = "Mersenne-Twister", normal.kind = "Inversion", sample.kind = "Rejection")
set.seed(2026)
gercek_oran <- 0.40
hacim <- 50
basari <- rbinom(10000, size = hacim, prob = gercek_oran)
tahminler <- basari / hacim
merkez <- mean(tahminler)
varyans <- mean((tahminler - merkez)^2)
print(c(merkez = merkez, yanlilik = merkez - gercek_oran,
        ampirik_se = sd(tahminler), mse = mean((tahminler - gercek_oran)^2),
        mse_ayrisimi = varyans + (merkez - gercek_oran)^2,
        kuramsal_se = sqrt(0.40 * 0.60 / hacim), kuramsal_mse = 0.40 * 0.60 / hacim))
hedef <- "ciktilar/r/yeni-benzetim.csv"
if (file.exists(hedef)) stop("Cikti zaten var; once ayri bir adla saklayin.")
dir.create("ciktilar/r", recursive = TRUE, showWarnings = FALSE)
write.csv(data.frame(tekrar = seq_along(basari), basari = basari), hedef, row.names = FALSE)
cat("Yeni R cekimleri ortak Python CSV'siyle birebir eslesmek zorunda degildir.\n")
sessionInfo()