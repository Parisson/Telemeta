VERSION := $(shell cat ../VERSION)
DOCS=README.fr.html README.fr

doc: $(DOCS)

README.fr.html: README.fr doc.css
	rst2html --stylesheet=doc.css --link-stylesheet README.fr $@

README.fr: README.fr.in
	cat $^ | sed "s/EZTVERSION/$(VERSION)/g" > $@

clean:  
	rm $(DOCS)

# vim: set noexpandtab: ts=2: sw=2:
