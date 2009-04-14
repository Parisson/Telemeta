DOCS=README.fr.html

doc: $(DOCS)

README.fr.html: README.fr doc.css
	rst2html --stylesheet=doc.css --link-stylesheet README.fr $@

clean:  
	rm $(DOCS)
