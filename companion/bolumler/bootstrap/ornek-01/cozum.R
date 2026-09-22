gozlem_oku <- function(dosya, gruplu=FALSE) {
  veri <- read.csv(dosya, check.names=FALSE, stringsAsFactors=FALSE)
  baslik <- if (gruplu) c('id','grup','deger') else c('id','deger')
  adet <- if (gruplu) 6 else 5
  stopifnot(identical(names(veri),baslik), nrow(veri)==adet,
    is.numeric(veri$id), is.numeric(veri$deger), !anyNA(veri),
    all(is.finite(veri$id)), all(is.finite(veri$deger)), all(abs(veri$deger)<=1e12))
  veri <- veri[order(veri$id), ]
  stopifnot(all(veri$id==seq_len(adet)))
  if (gruplu) stopifnot(all(veri$grup %in% c('A','B')),
                        sum(veri$grup=='A')==3, sum(veri$grup=='B')==3)
  veri
}
plan_oku <- function(dosya, beklenen) {
  veri <- read.csv(dosya, check.names=FALSE)
  stopifnot(identical(names(veri),c('sira',paste0('ind',seq_len(ncol(beklenen))))),
            nrow(veri)==nrow(beklenen), all(vapply(veri,is.numeric,logical(1))),
            !anyNA(veri), all(is.finite(as.matrix(veri))))
  veri <- veri[order(veri$sira), ]
  stopifnot(all(veri$sira==seq_len(nrow(veri))), all(as.matrix(veri[,-1])==beklenen))
  as.matrix(veri[,-1])
}
veri <- gozlem_oku('veri.csv')
gruplar <- gozlem_oku('permutasyon.csv',TRUE)
beklenen_boot <- expand.grid(rep(list(1:5),5))
beklenen_boot <- as.matrix(beklenen_boot[do.call(order,beklenen_boot), ])
secimler <- t(combn(1:6,3))
beklenen_perm <- t(apply(secimler,1,function(indis) c(indis,setdiff(1:6,indis))))
boot_plan <- plan_oku('bootstrap-plan.csv',beklenen_boot)
perm_plan <- plan_oku('permutasyon-plan.csv',beklenen_perm)
ortalamalar <- apply(boot_plan,1,function(indis) mean(veri$deger[indis]))
ortalama <- mean(veri$deger)
merkez <- mean(ortalamalar)
ampirik_varyans <- mean((veri$deger-ortalama)^2)
boot_varyans <- mean((ortalamalar-merkez)^2)
boot <- c(5,ortalama,ampirik_varyans,sd(veri$deger),sqrt(ampirik_varyans/5),
          length(ortalamalar),merkez,boot_varyans,sqrt(boot_varyans),
          min(ortalamalar),max(ortalamalar),
          unname(quantile(ortalamalar,c(.025,.975),type=7)),
          merkez-ortalama,sum(table(ortalamalar)/length(ortalamalar)))
ortalama_a <- mean(gruplar$deger[gruplar$grup=='A'])
ortalama_b <- mean(gruplar$deger[gruplar$grup=='B'])
gozlenen <- ortalama_a-ortalama_b
farklar <- apply(perm_plan,1,function(indis)
  mean(gruplar$deger[indis[1:3]])-mean(gruplar$deger[indis[4:6]]))
uc <- sum(abs(farklar)>=abs(gozlenen)-1e-12)
perm <- c(3,3,ortalama_a,ortalama_b,gozlenen,length(farklar),uc,
          uc/length(farklar),min(farklar),max(farklar),mean(farklar))
sonuc <- data.frame(degisken=c(rep('bootstrap',15),rep('permutasyon',11)),
 olcu=c('n','ortalama','ampirik_varyans','orneklem_sd','kuramsal_boot_se',
        'yeniden_orneklem','boot_merkez','boot_varyans','boot_se','boot_min','boot_max',
        'alt025','ust975','boot_yanlilik','olasilik_toplami',
        'n_a','n_b','ortalama_a','ortalama_b','gozlenen_fark','atama_sayisi',
        'uc_atama','p_tam','en_kucuk_fark','en_buyuk_fark','sifir_merkezi'),deger=c(boot,perm))
print(sonuc,row.names=FALSE,digits=12)
secenek <- commandArgs(TRUE)
stopifnot(all(secenek %in% c('--check','--grafik','--benzetim')))
if ('--check' %in% secenek) {
  hedef <- read.csv('beklenen-sonuclar.csv',check.names=FALSE)
  stopifnot(identical(names(hedef),names(sonuc)),
    identical(hedef$degisken,sonuc$degisken),identical(hedef$olcu,sonuc$olcu),
    is.numeric(hedef$deger),all(is.finite(hedef$deger)),
    all(abs(hedef$deger-sonuc$deger)<=pmax(1e-9,abs(hedef$deger)*1e-9)))
  cat('DOGRULANDI: 26 kontrol degeri eslesiyor.\n')
}
if ('--grafik' %in% secenek) {
  dir.create('ciktilar/r',recursive=TRUE,showWarnings=FALSE)
  png('ciktilar/r/bootstrap-permutasyon.png',width=1600,height=600,res=150)
  par(mfrow=c(1,2))
  adet <- table(ortalamalar)
  plot(as.numeric(names(adet)),as.numeric(adet)/length(ortalamalar),type='h',
       xlab='Ortalama',ylab='Olasilik',main='3125 tam bootstrap orneklemi')
  abline(v=quantile(ortalamalar,c(.025,.975),type=7),lty=2,col='orange')
  adet <- table(farklar)
  plot(as.numeric(names(adet)),as.numeric(adet)/length(farklar),type='h',
       xlab='A - B farki',ylab='Olasilik',main='20 tam etiket atamasi')
  abline(v=c(-abs(gozlenen),abs(gozlenen)),lty=2,col='orange')
  dev.off()
}
if ('--benzetim' %in% secenek) {
  set.seed(2026)
  tekrarlar <- replicate(10000,mean(sample(veri$deger,5,replace=TRUE)))
  print(c(MC_se=sd(tekrarlar),quantile(tekrarlar,c(.025,.975),type=7)))
}
sessionInfo()