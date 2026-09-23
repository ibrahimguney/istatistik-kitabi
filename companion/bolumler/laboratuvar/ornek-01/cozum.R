d <- read.csv("veri.csv", na.strings=c("", "NA"))
stopifnot(identical(names(d),c("id","grup","on","son","saat")),!anyNA(d),!anyDuplicated(d$id),all(d$grup %in% 1:2),all(d$on>=0 & d$on<=100),all(d$son>=0 & d$son<=100),all(d$saat>=0 & d$saat<=40))
d$degisim<-d$son-d$on
a<-d$son[d$grup==1];b<-d$son[d$grup==2]
pair<-t.test(d$son,d$on,paired=TRUE);welch<-t.test(a,b,var.equal=FALSE);co<-cor.test(d$saat,d$son);fit<-lm(son~saat,data=d);ga<-t.test(d$son)$conf.int
s<-c(n=nrow(d),son_ortalama=mean(d$son),degisim_ortalama=mean(d$degisim),ga_alt=ga[1],ga_ust=ga[2],esli_t=unname(pair$statistic),esli_p=pair$p.value,welch_t=unname(welch$statistic),welch_p=welch$p.value,pearson_r=unname(co$estimate),pearson_p=co$p.value,regresyon_sabit=unname(coef(fit)[1]),regresyon_egim=unname(coef(fit)[2]))
d$grup<-factor(d$grup,levels=c(1,2));adj<-lm(son~on+grup,data=d)
s<-c(s,setNames(unname(coef(adj)),c("ayarli_sabit","ayarli_on","ayarli_grup_B")),fisher_p=fisher.test(table(d$grup,factor(d$degisim>=7,levels=c(FALSE,TRUE))))$p.value)
out<-data.frame(olcut=names(s),deger=as.numeric(s))
print(out,row.names=FALSE);write.csv(out,"sonuclar-r.csv",row.names=FALSE)
if("--check" %in% commandArgs(trailingOnly=TRUE)){
 ref<-read.csv("beklenen-sonuclar.csv")
 stopifnot(identical(out$olcut,ref$olcut),all(abs(out$deger-ref$deger)<=1e-10+1e-8*abs(ref$deger)))
 cat("KONTROL BASARILI\n")
}
sessionInfo()
