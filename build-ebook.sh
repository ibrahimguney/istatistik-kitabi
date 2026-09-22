#!/bin/sh
set -eu

mkdir -p build/ebook
latexmk -xelatex -interaction=nonstopmode -halt-on-error \
  -outdir=build/ebook main-ebook.tex
cp build/ebook/main-ebook.pdf ebook.pdf

printf '%s\n' 'E-kitap: ebook.pdf'