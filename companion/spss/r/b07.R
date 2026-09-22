veri <- read.csv("companion/spss/csv/b07.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 10,
          !anyNA(veri),
          all(veri$pass10 == as.integer(veri$g3 >= 10)))
gozlem_sayisi <- nrow(veri)
ortalama <- mean(veri$g3)
standart_sapma <- sd(veri$g3)
oran <- mean(veri$pass10)
frekans <- table(veri$pass10)
print(frekans); print(100 * prop.table(frekans))
print(c(n=gozlem_sayisi, ort=ortalama, ss=standart_sapma,
  sh_ort=standart_sapma/sqrt(gozlem_sayisi), oran=oran,
  sh_oran=sqrt(oran*(1-oran)/gozlem_sayisi)))
print(sum(veri$g3 == 0))