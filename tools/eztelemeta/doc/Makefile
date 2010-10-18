VERSION := $(shell cat ../VERSION)
DOCS=README.fr.html README.fr.pdf README.fr README.fr.latex

doc: $(DOCS)

README.fr.html: README.fr doc.css player.png
	cat README.fr | sed 's/:scale: .*/:scale: 100/' | \
		rst2html -lfr --stylesheet=doc.css --link-stylesheet - $@

README.fr.pdf: README.fr.latex
	pdflatex $^
	pdflatex $^ # Double run is sometimes needed

README.fr.latex: README.fr player.png
	rst2latex -lfr README.fr $@

README.fr: README.fr.in ../VERSION
	cat README.fr.in | sed "s/EZTVERSION/$(VERSION)/g" > $@

clean:  
	rm -f $(DOCS) README.fr.aux README.fr.out README.fr.log

# vim: set noexpandtab: ts=2: sw=2:
