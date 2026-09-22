d <- read.csv("companion/spss/csv/b08.csv")
stopifnot(!anyNA(d))
print(t.test(d$g3, conf.level=.95)$conf.int)
print(table(d$pass10))
n <- nrow(d); p <- mean(d$pass10)
z <- qnorm(.975); den <- 1 + z^2/n
center <- (p + z^2/(2*n))/den
half <- z * sqrt(p*(1-p)/n + z^2/(4*n^2))/den
print(c(proportion=p, lower=center-half,
        upper=center+half))