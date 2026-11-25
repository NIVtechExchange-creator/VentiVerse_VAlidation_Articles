# Mathematical Modeling of Mechanical Ventilation and Respiratory Physiology

LaTeX source for the book. 8.5 x 11 in (US letter) textbook trim, full color.

- `main.tex` - master file (includes every chapter)
- `style/bookstyle.sty` - page layout, fonts, colors, headings, teaching boxes
- `chapters/chNN.tex` - one file per chapter; `chapters/_list.tex` sets the order and parts
- `backmatter/appX.tex` - appendices
- `frontmatter/` - title page, copyright, preface
- `figures/` - images (PNG/JPG/PDF) referenced with \includegraphics
- `references.bib` - bibliography (BibTeX)
- `OUTLINE.md` - chapter plan

Teaching boxes available in any chapter: objectives, keyequation, example{Title}, clinicalpearl, simnote, summarybox.

Build: `latexmk -pdf main.tex` (or ./build.sh) with a TeX Live / MiKTeX install. Output: main.pdf
