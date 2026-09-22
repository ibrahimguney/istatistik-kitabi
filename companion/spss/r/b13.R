veri <- read.csv("companion/spss/csv/b13.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 10,
  !anyNA(veri), !anyDuplicated(veri$id),
  all(veri$pass10 == as.integer(veri$g3 >= 10)))
korelasyon <- cor.test(veri$g1, veri$g3,
  method="pearson", alternative="two.sided")
model <- lm(g3 ~ g1, data=veri)
ozet <- summary(model)
tahmin <- fitted(model)
artik <- residuals(model)
zpred <- as.numeric(scale(tahmin))
zresid <- artik/sigma(model)
print(c(satir=nrow(veri), sutun=ncol(veri),
  eksik=sum(is.na(veri)), sifir_not=sum(veri$g3 == 0)))

print(c(r=unname(korelasyon$estimate),
  p_korelasyon=korelasyon$p.value,
  R2=ozet$r.squared, duzeltilmis_R2=ozet$adj.r.squared,
  model_sh=sigma(model),
  F=unname(ozet$fstatistic["value"]),
  df_model=unname(ozet$fstatistic["numdf"]),
  df_artik=df.residual(model),
  beta=coef(model)[["g1"]]*sd(veri$g1)/sd(veri$g3),
  G1_10_tahmin=unname(predict(model, data.frame(g1=10)))
), digits=15)
print(cbind(ozet$coefficients,
            confint(model, level=.95)), digits=15)
print(anova(model), digits=15)

betimsel <- function(degerler) {
  c(n=length(degerler), minimum=min(degerler),
    maksimum=max(degerler), ortalama=mean(degerler),
    ss=sd(degerler))
}
print(rbind(G1=betimsel(veri$g1), G3=betimsel(veri$g3)),
      digits=15)
print(rbind(tahmin=betimsel(tahmin), artik=betimsel(artik),
  zpred=betimsel(zpred), zresid=betimsel(zresid)), digits=15)

par(mfrow=c(1, 3))
plot(veri$g1, veri$g3, xlab="G1", ylab="G3",
     main="G1 - G3", pch=16)
abline(model, col="blue", lwd=2)
plot(zpred, zresid, xlab="ZPRED", ylab="ZRESID",
     main="Artik - Tahmin", pch=16)
abline(h=0, lty=2)
hist(zresid, breaks=15, main="Artik histogrami",
     xlab="ZRESID")
par(mfrow=c(1, 1))