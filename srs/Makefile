LATEX = pdflatex
ECHO = echo
FILES = srs.tex
MPOST = mpost
FLOW = flow

all : 
	$(ECHO) Making srs.tex
	rm system_to_user.tex
	$(FLOW) < system_to_user.flo > system_to_user.tex
	$(ECHO) Making srs.pdf
	$(LATEX) $(FILES)
	$(ECHO) Making srs.pdf again for references
	$(LATEX) $(FILES)

mpost:
	$(ECHO) Building mpost graphics
	$(MPOST) images/classes.mp
	$(MPOST) images/sequence.mp
	$(MPOST) images/sequence_arm.mp
	$(MPOST) images/sequence_alert.mp
	$(MPOST) images/states.mp

mpost_arm:
	$(MPOST) images/sequence_arm.mp

mpost_alert:
	$(MPOST) images/sequence_alert.mp

mpost_states:
	$(MPOST) images/states.mp
