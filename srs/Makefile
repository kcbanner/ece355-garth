LATEX = pdflatex
ECHO = echo
FILES = srs.tex
FLOW = flow

all : 
	rm system_to_user.tex
	$(FLOW) < system_to_user.flo > system_to_user.tex
	$(ECHO) Making srs.pdf
	$(LATEX) $(FILES)
	$(ECHO) Making srs.pdf again for references
	$(LATEX) $(FILES)
