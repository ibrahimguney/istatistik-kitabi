veri <- read.csv("veri.csv", check.names=FALSE)
stopifnot(identical(names(veri), c("tekrar","ort1","ort5","ort30")),
          nrow(veri)>1, all(vapply(veri,is.numeric,logical(1))),
          all(is.finite(as.matrix(veri))))
veri <- veri[order(veri$tekrar), ]
stopifnot(all(veri$tekrar==seq_len(nrow(veri))), all(veri[,-1]>=0))
olculer <- c("n","B","merkez","ampirik_se","kuramsal_se","varyans","sapma")
sonuc <- do.call(rbind,lapply(c(1,5,30),function(hacim) {
  degerler <- veri[[paste0("ort",hacim)]]
  data.frame(degisken=paste0("n",hacim),olcu=olculer,
    deger=c(hacim,nrow(veri),mean(degerler),sd(degerler),
            10/sqrt(hacim),100/hacim,mean(degerler)-10))
}))
sonuc <- rbind(sonuc,data.frame(degisken="ek",
  olcu=c("se25","se100","hacim_carpani"),deger=c(2,1,4)))
print(sonuc,row.names=FALSE,digits=12)
if ("--check" %in% commandArgs(TRUE)) {
  hedef <- read.csv("beklenen-sonuclar.csv")
  stopifnot(identical(names(hedef),names(sonuc)),
    identical(hedef$degisken,sonuc$degisken),
    identical(hedef$olcu,sonuc$olcu),is.numeric(hedef$deger),
    all(is.finite(hedef$deger)),
    all(abs(hedef$deger-sonuc$deger)<=pmax(1e-9,abs(hedef$deger)*1e-9)))
  cat("DOGRULANDI: 24 kontrol degeri eslesiyor.\n")
}
if ("--grafik" %in% commandArgs(TRUE)) {
  png("histogram-r.png",width=1500,height=500)
  par(mfrow=c(1,3))
  for (hacim in c(1,5,30)) {
    hist(veri[[paste0("ort",hacim)]],breaks=35,probability=TRUE,
         main=paste("n =",hacim),xlab="Orneklem ortalamasi")
    abline(v=10,col="blue",lwd=2)
  }
  dev.off()
}
sessionInfo()