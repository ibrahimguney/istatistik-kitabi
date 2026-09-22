veri <- read.csv("companion/spss/csv/b09.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 10,
          !anyNA(veri),
          all(veri$pass10 == as.integer(veri$g3 >= 10)))
sonuc <- t.test(veri$g3, mu=10,
               alternative="two.sided", conf.level=.95)
ozet <- c(
  n=nrow(veri), ort=mean(veri$g3), ss=sd(veri$g3),
  sh_ort=sd(veri$g3)/sqrt(nrow(veri)),
  t=unname(sonuc$statistic), df=unname(sonuc$parameter),
  p_iki_yonlu=sonuc$p.value, fark=mean(veri$g3)-10,
  ort_alt=sonuc$conf.int[1], ort_ust=sonuc$conf.int[2],
  fark_alt=sonuc$conf.int[1]-10,
  fark_ust=sonuc$conf.int[2]-10)
print(sonuc)
print(ozet, digits=15)
print(sum(veri$g3 == 0))