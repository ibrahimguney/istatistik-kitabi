d <- read.csv("companion/spss/csv/b04.csv")
stopifnot(!anyNA(d))
print(sapply(d[c("ort5", "ort30")], function(v)
  c(n=length(v), mean=mean(v), sd=sd(v),
    min=min(v), max=max(v))))
par(mfrow=c(1, 2))
for (v in c("ort5", "ort30")) {
  x <- d[[v]]
  hist(x, breaks=seq(0, 20, by=.5),
       probability=TRUE, main=v, xlab=v,
       xlim=c(0, 20), ylim=c(0, .6))
  curve(dnorm(x, mean(d[[v]]), sd(d[[v]])),
        add=TRUE, col="blue")
}
par(mfrow=c(1, 1))