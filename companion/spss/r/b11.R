veri <- read.csv("companion/spss/csv/b11.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 10,
  !anyNA(veri), !anyDuplicated(veri$id),
  all(veri$sex %in% c(1, 2)),
  all(veri$pass10 == as.integer(veri$g3 >= 10)))
grup_F <- veri$g3[veri$sex == 1]
grup_M <- veri$g3[veri$sex == 2]
fark <- veri$g3-veri$g1
welch <- t.test(grup_F, grup_M, var.equal=FALSE,
  alternative="two.sided", conf.level=.95)
eslesmis <- t.test(veri$g3, veri$g1, paired=TRUE,
  alternative="two.sided", conf.level=.95)
print(welch); print(eslesmis)

betimsel <- function(degerler) {
  c(n=length(degerler), ort=mean(degerler),
    ss=sd(degerler), sh=sd(degerler)/sqrt(length(degerler)))
}
test_ozeti <- function(sonuc, ortalama_fark) {
  c(t=unname(sonuc$statistic), df=unname(sonuc$parameter),
    p_iki_yonlu=sonuc$p.value, fark=ortalama_fark,
    alt=sonuc$conf.int[1], ust=sonuc$conf.int[2])
}
print(rbind(F=betimsel(grup_F), M=betimsel(grup_M)),
      digits=15)
print(test_ozeti(welch, mean(grup_F)-mean(grup_M)),
      digits=15)
print(rbind(G3=betimsel(veri$g3), G1=betimsel(veri$g1)),
      digits=15)
print(test_ozeti(eslesmis, mean(fark)), digits=15)
print(c(betimsel(fark), dz=mean(fark)/sd(fark)), digits=15)
print(sum(veri$g3 == 0))

par(mfrow=c(1, 3))
boxplot(g3 ~ sex, data=veri, names=c("F", "M"))
boxplot(fark, main="G3-G1")
hist(fark, main="G3-G1", xlab="Difference")
par(mfrow=c(1, 1))