d <- read.csv("companion/spss/csv/b02.csv")
stopifnot(!anyNA(d))
d$school <- factor(d$school, 1:2, c("GP", "MS"))
d$sex <- factor(d$sex, 1:2, c("F", "M"))
d$studytime <- ordered(d$studytime, levels=1:4)
for (v in c("school", "sex", "studytime")) {
  f <- table(d[[v]])
  print(f); print(100 * prop.table(f))
}
print(sapply(d[c("age", "g3")], function(v)
  c(n=length(v), mean=mean(v), sd=sd(v),
    min=min(v), max=max(v))))