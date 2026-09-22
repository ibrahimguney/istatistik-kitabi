d <- read.csv("companion/spss/csv/b01.csv")
stopifnot(!anyNA(d))
d$school <- factor(d$school, 1:2, c("GP", "MS"))
d$sex <- factor(d$sex, 1:2, c("F", "M"))
d$studytime <- ordered(d$studytime, levels=1:4)
str(d)
print(colSums(is.na(d)))
print(table(d$school)); print(table(d$sex))
x <- d[c("age", "g1", "g2", "g3")]
print(sapply(x, function(v) c(n=length(v),
  mean=mean(v), sd=sd(v), min=min(v), max=max(v))))