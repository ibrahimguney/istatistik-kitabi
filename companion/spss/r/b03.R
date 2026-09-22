d <- read.csv("companion/spss/csv/b03.csv")
stopifnot(!anyNA(d))
print(sapply(d[c("g3", "absences")], function(v)
  c(n=length(v), mean=mean(v), sd=sd(v),
    median=median(v), min=min(v), max=max(v))))
print(t.test(d$g3, conf.level=.95)$conf.int)
print(t.test(d$absences, conf.level=.95)$conf.int)
par(mfrow=c(2, 2))
for (v in c("g3", "absences")) {
  hist(d[[v]], main=v, xlab=v)
  boxplot(d[[v]], main=v)
}
par(mfrow=c(1, 1))