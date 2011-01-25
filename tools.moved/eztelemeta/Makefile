PACKAGE = eztelemeta
VERSION = 0.1

DOCS = VERSION ChangeLog doc/README.fr doc/README.fr.html doc/doc.css doc/README.fr.latex \
	doc/README.fr.pdf doc/player.png LICENCE LICENCE.fr

SETTINGS = \
	settings/content.ini.append \
	settings/design.ini.append \
	settings/site.ini.append \
	settings/override.ini.append

TEMPLATES = \
	design/standard/templates/content/datatype/view/eztelemetaitem.tpl \
	design/standard/templates/content/datatype/edit/eztelemetaitem.tpl \
	design/standard/templates/eztelemeta_head.tpl \
	design/standard/override/templates/embed/eztelemetaitem.tpl \
	design/standard/override/templates/full/eztelemetaitem.tpl

HTDOCS = \
	design/standard/stylesheets/eztelemeta.css \
	design/standard/javascript/soundmanager2.js \
	design/standard/javascript/soundmanager2-nodebug-jsmin.js \
	design/standard/javascript/eztelemeta-player.js \
	design/standard/swf/soundmanager2_flash9.swf \
	design/standard/swf/soundmanager2.swf \
	design/standard/images/play.gif \
	design/standard/images/stop.gif

PHP = datatypes/eztelemetaitem/eztelemetaitemtype.php \
	autoloads/eztelemetadata.php \
	autoloads/eztemplateautoload.php

I18N = translations/fre-FR/translation.ts

DISTFILES = $(DOCS) $(SETTINGS) $(TEMPLATES) $(HTDOCS) $(PHP) $(I18N)

DISTPKG = $(PACKAGE)-$(VERSION).tar.gz

dist: $(DISTPKG)

$(DISTPKG): doc $(DISTFILES)
	tar -czf $@ --transform 's|^|eztelemeta/|' $(DISTFILES)

.PHONY: doc
doc: VERSION
	$(MAKE) -C doc

.PHONY: clean
clean:
	$(MAKE) -C doc clean
	rm VERSION

VERSION:
	echo $(VERSION) > $@

.PHONY: list
list: doc $(DISTFILES)
	@echo "------------------"
	@echo "Distributed files:"
	@echo "------------------"
	@echo $(DISTFILES) | tr ' ' '\n' > cmp.tmp
	@cat cmp.tmp
	@echo
	@echo "--------------------"
	@echo "Undistributed files:"
	@echo "--------------------"
	@find -type f | grep -v svn | grep -v 'swp$$' | sed 's/^\.\///' >> cmp.tmp
	@cat cmp.tmp | sort | uniq -u | grep -v 'cmp.tmp'
	@rm cmp.tmp

# vim: set noexpandtab: ts=2: sw=2:
