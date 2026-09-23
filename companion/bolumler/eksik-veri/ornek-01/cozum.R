d <- read.csv("veri.csv", na.strings=c("", "NA"))
stopifnot(identical(names(d),c("grup","on","son")), all(d$grup %in% 1:2), all(d$on>=0 & d$on<=100), all(d$son>=0 & d$son<=100,na.rm=TRUE))
s <- c(n=nrow(d),eksik_son=sum(is.na(d$son)),eksik_oran=mean(is.na(d$son)))
for(g in 1:2){x<-d$son[d$grup==g];x<-x[!is.na(x)];stopifnot(length(x)>1); s<-c(s,setNames(c(length(x),mean(x),sd(x)),paste0(c("n_","ortalama_","ss_"),g)))}
s<-c(s,on_eksik_son=mean(d$on[is.na(d$son)]),on_gozlenen_son=mean(d$on[!is.na(d$son)]))
out<-data.frame(olcut=names(s),deger=as.numeric(s))
print(out,row.names=FALSE);write.csv(out,"sonuclar-r.csv",row.names=FALSE)
if("--check" %in% commandArgs(trailingOnly=TRUE)){
 ref<-read.csv("beklenen-sonuclar.csv")
 stopifnot(identical(out$olcut,ref$olcut),all(abs(out$deger-ref$deger)<=1e-10+1e-8*abs(ref$deger)))
 cat("KONTROL BASARILI\n")
}
sessionInfo()
