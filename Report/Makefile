
# A makefile for markdown to latex to compile to run
# The filename is the first argument
FILE=assignment.pdc

#PDFVIEW=acroread
PDFVIEW=evince



all: latex

latex: compile_pdf


compile_pdf: 
	pandoc -o body.tex ${FILE}
	cat Template/header.tex body.tex Template/end.tex > output.tex
	latex output.tex
	dvipdf output.dvi

clean:
	rm -f *.tex
	rm -f output*

run_pdf: 
	${PDFVIEW} output.pdf
