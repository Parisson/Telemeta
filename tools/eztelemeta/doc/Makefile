VERSION := $(shell cat ../VERSION)
DOCS=README.fr.html

doc: $(DOCS)

README.fr.html: README.fr doc.css
	cat README.fr | sed "s/EZTVERSION/$(VERSION)/g" |  \
 	rst2html --stylesheet=doc.css --link-stylesheet - $@

clean:  
	rm $(DOCS)
