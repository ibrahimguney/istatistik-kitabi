veri <- read.csv("companion/spss/csv/b10.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 10,
  !anyNA(veri),
  all(veri$pass10 == as.integer(veri$g3 >= 10)))
sonuc <- t.test(veri$g3, mu=10,
  alternative="two.sided", conf.level=.95)
ortalama <- mean(veri$g3)
standart_sapma <- sd(veri$g3)
print(c(n=nrow(veri), ort=ortalama, ss=standart_sapma,
  sh_ort=standart_sapma/sqrt(nrow(veri)),
  t=unname(sonuc$statistic), df=unname(sonuc$parameter),
  p_iki_yonlu=sonuc$p.value, fark=ortalama-10,
  etki_d=(ortalama-10)/standart_sapma,
  ort_alt=sonuc$conf.int[1],
  ort_ust=sonuc$conf.int[2]), digits=15)
print(sum(veri$g3 == 0))

plan <- power.t.test(delta=1, sd=4.581442611,
  sig.level=.05, power=.80, type="one.sample",
  alternative="two.sided", strict=TRUE)
n_plan <- ceiling(plan$n)
guc <- function(hacim) {
  power.t.test(n=hacim, delta=1, sd=4.581442611,
    sig.level=.05, type="one.sample",
    alternative="two.sided", strict=TRUE)$power
}
print(c(n_kesirli=plan$n, n_plan=n_plan,
  guc_plan=guc(n_plan), n_bir_eksik=n_plan-1,
  guc_bir_eksik=guc(n_plan-1)), digits=15)