veri <- read.csv("companion/spss/csv/b06.csv")
stopifnot(nrow(veri) == 395, ncol(veri) == 13,
          !anyNA(veri))
basit <- subset(veri, srs40 == 1)
tabakali <- subset(veri, strat40 == 1)
stopifnot(nrow(basit) == 40, nrow(tabakali) == 40)
ozet <- function(degerler)
  c(n=length(degerler), mean=mean(degerler),
    sd=sd(degerler))
print(cbind(tam_dosya=ozet(veri$g3),
            basit_rastgele=ozet(basit$g3)))
okul <- factor(tabakali$school, c(1, 2), c("GP", "MS"))
frekans <- table(okul)
print(frekans); print(100 * prop.table(frekans))
print(nrow(tabakali)); print(sum(tabakali$strw))
print(weighted.mean(tabakali$g3, tabakali$strw))