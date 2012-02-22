LATEX = pdflatex
ECHO = echo
FILES = sdd.tex
MPOST = mpost
FLOW = flow

all : 
	$(ECHO) Making sdd.pdf
	$(LATEX) $(FILES)
	$(ECHO) Making sdd.pdf again for references
	$(LATEX) $(FILES)
	wc sdd.tex

mpost :
	$(ECHO) Building mpost graphics
	$(MPOST) images/external_interfaces.mp
	$(MPOST) images/communication_layers.mp
