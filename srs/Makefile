LATEX = pdflatex
ECHO = echo
FILES = srs.tex
MPOST = mpost
MPOST_GRAPHICS = images/classes.mp

all : 
	$(ECHO) Building MetaPost graphics
	$(MPOST) $(MPOST_GRAPHICS)
	$(ECHO) Making srs.tex
	$(LATEX) $(FILES)
	$(ECHO) Making srs.tex again for references
	$(LATEX) $(FILES)
