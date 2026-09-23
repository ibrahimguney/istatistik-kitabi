d <- read.csv("veri.csv", na.strings=c("", "NA"))
stopifnot(identical(names(d),paste0("M",1:5)),!anyNA(d),all(as.matrix(d) %in% 1:5))
alpha<-function(x){k<-ncol(x);v<-var(rowSums(x));stopifnot(nrow(x)>1,k>1,v>0);k/(k-1)*(1-sum(sapply(x,var))/v)}
x<-d;x$M4<-6-x$M4
s<-c(n=nrow(x),alpha_ham=alpha(d),alpha=alpha(x),toplam_ortalama=mean(rowSums(x)))
for(col in names(x)){rest<-x[names(x)!=col];s<-c(s,setNames(c(cor(x[[col]],rowSums(rest)),alpha(rest)),paste0(col,c("_duzeltilmis_r","_silinirse_alpha"))))}
out<-data.frame(olcut=names(s),deger=as.numeric(s))
print(out,row.names=FALSE);write.csv(out,"sonuclar-r.csv",row.names=FALSE)
if("--check" %in% commandArgs(trailingOnly=TRUE)){
 ref<-read.csv("beklenen-sonuclar.csv")
 stopifnot(identical(out$olcut,ref$olcut),all(abs(out$deger-ref$deger)<=1e-10+1e-8*abs(ref$deger)))
 cat("KONTROL BASARILI\n")
}
sessionInfo()
