#!/bin/sh
set -eu

# pdfx paketi XeLaTeX altında geçici pdfx.xmpi dosyasını çalışma dizinine
# yazar. Bu nedenle her PDF/X belgesi kendi çıktı klasörünün içinden
# derlenir; yalnız -outdir kullanmak metadata akışını son PDF'den düşürür.

mkdir -p build/press/interior build/press/cover

(
  cd build/press/interior
  TEXINPUTS=../../../: latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error ../../../main-pdfx4.tex
)

(
  cd build/press/cover
  TEXINPUTS=../../../: latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error ../../../cover-print-pdfx4.tex
)

printf '%s\n' \
  'İç blok: build/press/interior/main-pdfx4.pdf' \
  'Kapak:    build/press/cover/cover-print-pdfx4.pdf'