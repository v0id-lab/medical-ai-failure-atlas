main.pdf: main.tex references.bib
	pdflatex main.tex
	bibtex main || true
	pdflatex main.tex
	pdflatex main.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out main.pdf
