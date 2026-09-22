d <- read.csv("companion/spss/csv/b05.csv")
stopifnot(!anyNA(d))
print(sapply(d[c("ort5", "ort30", "ort100", "z5", "z100")],
  function(degerler) c(n=length(degerler),
    mean=mean(degerler), sd=sd(degerler))))
kapsama <- abs(d$z100) <= 1.96
print(table(kapsama))
print(100 * mean(kapsama))
par(mfrow=c(1, 2))
for (v in c("z5", "z100")) {
  hist(d[[v]], breaks=seq(-5, 5, by=.25),
       probability=TRUE, main=v, xlab=v,
       xlim=c(-5, 5), ylim=c(0, .6))
  curve(dnorm(x), add=TRUE, col="blue")
  abline(v=c(-1.96, 1.96), lty=2)
}
par(mfrow=c(1, 1))