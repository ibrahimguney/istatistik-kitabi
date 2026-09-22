GET DATA
  /TYPE=TXT
  /FILE='veri.csv'
  /ENCODING='UTF8'
  /ARRANGEMENT=DELIMITED
  /DELCASE=LINE
  /DELIMITERS=","
  /QUALIFIER='"'
  /FIRSTCASE=2
  /VARIABLES=
    devam_saati F8.0
    basari F8.0
    program A1.
DATASET NAME B01Ornek.
FILTER OFF.
USE ALL.
WEIGHT OFF.
SPLIT FILE OFF.
VARIABLE LABELS
  devam_saati 'Devam suresi (saat)'
  /basari 'Basari puani (ogretim verisi)'
  /program 'Program etiketi'.
VARIABLE LEVEL devam_saati basari (SCALE)
  /program (NOMINAL).
EXECUTE.
DISPLAY DICTIONARY.
FREQUENCIES VARIABLES=program
  /ORDER=ANALYSIS.
DESCRIPTIVES VARIABLES=devam_saati basari
  /STATISTICS=MEAN MIN MAX.