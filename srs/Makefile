LATEX = pdflatex
ECHO = echo
FILES = srs.tex
MPOST = mpost
MPOST_GRAPHICS = images/classes.mp
FLOW = flow

all : 
	$(ECHO) Making srs.tex
	$(ECHO) Building MetaPost graphics
	$(MPOST) $(MPOST_GRAPHICS)
	rm system_to_user.tex
	$(FLOW) < system_to_user.flo > system_to_user.tex
	$(ECHO) Making srs.pdf
	$(LATEX) $(FILES)
	$(ECHO) Making srs.pdf again for references
	$(LATEX) $(FILES)
