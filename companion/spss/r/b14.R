veri <- read.csv("companion/spss/csv/b14.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 10,
  !anyNA(veri), !anyDuplicated(veri$id),
  all(veri$sex %in% c(1, 2)),
  all(veri$pass10 %in% c(0, 1)),
  all(veri$pass10 == as.integer(veri$g3 >= 10)))
betimsel <- function(degerler) {
  c(n=length(degerler), ortalama=mean(degerler),
    ss=sd(degerler), minimum=min(degerler),
    maksimum=max(degerler))
}
print(c(satir=nrow(veri), sutun=ncol(veri),
  eksik=sum(is.na(veri)), sifir_not=sum(veri$g3 == 0)))
print(rbind(G1=betimsel(veri$g1), G3=betimsel(veri$g3)),
      digits=15)

test <- t.test(veri$g3, mu=10,
  alternative="two.sided", conf.level=.95)
print(c(t=unname(test$statistic),
  df=unname(test$parameter), p_iki_yonlu=test$p.value,
  ortalama_fark=mean(veri$g3)-10,
  ortalama_alt=test$conf.int[1],
  ortalama_ust=test$conf.int[2],
  fark_alt=test$conf.int[1]-10,
  fark_ust=test$conf.int[2]-10), digits=15)

tablo <- table(
  sex=factor(veri$sex, levels=c(1, 2),
             labels=c("F", "M")),
  pass10=factor(veri$pass10, levels=c(0, 1),
                labels=c("10_alti", "10_ve_uzeri")))
ki_kare <- chisq.test(tablo, correct=FALSE)
print(addmargins(tablo))
print(100*prop.table(tablo, margin=1), digits=15)
print(ki_kare$expected, digits=15)
print(c(ki_kare=unname(ki_kare$statistic),
  df=unname(ki_kare$parameter), p=ki_kare$p.value,
  cramer_v=sqrt(unname(ki_kare$statistic)/sum(tablo)),
  min_beklenen=min(ki_kare$expected),
  bes_alti_hucre=sum(ki_kare$expected < 5)), digits=15)

korelasyon <- cor.test(veri$g1, veri$g3,
  method="pearson", alternative="two.sided")
print(c(n=nrow(veri), r=unname(korelasyon$estimate),
  p_iki_yonlu=korelasyon$p.value), digits=15)
pozitif <- veri[veri$g3 > 0, ]
print(rbind(Pozitif_G3=betimsel(pozitif$g3),
            Tum_G3=betimsel(veri$g3)), digits=15)
stopifnot(nrow(veri) == 395, nrow(pozitif) == 357)
par(mfrow=c(1, 1))
boxplot(veri$g3, main="Tum kayitlarda yil sonu notu",
        ylab="G3")