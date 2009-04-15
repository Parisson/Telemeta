VERSION := $(shell cat ../VERSION)
DOCS=README.fr.html README.fr.pdf README.fr README.fr.latex

doc: $(DOCS)

README.fr.html: README.fr doc.css
	rst2html -lfr --stylesheet=doc.css --link-stylesheet README.fr $@

README.fr.pdf: README.fr.latex
	pdflatex $^
	pdflatex $^

README.fr.latex: README.fr
	rst2latex -lfr $^ $@

README.fr: README.fr.in ../VERSION
	cat README.fr.in | sed "s/EZTVERSION/$(VERSION)/g" > $@

clean:  
	rm -f $(DOCS) README.fr.aux README.fr.out README.fr.log

# vim: set noexpandtab: ts=2: sw=2:
