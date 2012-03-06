LATEX = pdflatex
BIBTEX = bibtex
ECHO = echo
FILES = sdd.tex
BIBFILES = sdd.aux
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
	$(MPOST) images/subsystem_decomposition.mp
	$(MPOST) images/event_sequence.mp