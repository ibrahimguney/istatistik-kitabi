veri <- read.csv("companion/spss/csv/b12.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 10,
  !anyNA(veri), !anyDuplicated(veri$id),
  all(veri$sex %in% c(1, 2)),
  all(veri$pass10 %in% c(0, 1)),
  all(veri$pass10 == as.integer(veri$g3 >= 10)))
tablo <- table(
  sex=factor(veri$sex, levels=c(1, 2),
             labels=c("F", "M")),
  pass10=factor(veri$pass10, levels=c(0, 1),
                labels=c("10_alti", "10_ve_uzeri")))
sonuc <- chisq.test(tablo, correct=FALSE)
print(c(satir=nrow(veri), sutun=ncol(veri),
  eksik=sum(is.na(veri)), sifir_not=sum(veri$g3 == 0)))
print(addmargins(tablo))

print(100 * prop.table(tablo, margin=1), digits=15)
print(sonuc$expected, digits=15)
print(sonuc$residuals, digits=15)
print(c(
  n=sum(tablo),
  ki_kare=unname(sonuc$statistic),
  df=unname(sonuc$parameter),
  p=sonuc$p.value,
  min_beklenen=min(sonuc$expected),
  bes_alti_hucre=sum(sonuc$expected < 5),
  cramer_v=sqrt(unname(sonuc$statistic)/sum(tablo))
), digits=15)