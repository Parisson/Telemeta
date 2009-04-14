PACKAGE = eztelemeta
VERSION := $(shell cat VERSION)

DOCS = VERSION doc/README.fr doc/README.fr.html doc/doc.css 

SETTINGS = \
	settings/content.ini.append \
	settings/design.ini.append \
	settings/site.ini.append \
	settings/override.ini.append

TEMPLATES = \
	design/standard/templates/content/datatype/view/eztelemetaitem.tpl \
	design/standard/templates/content/datatype/edit/eztelemetaitem.tpl \
	design/standard/templates/eztelemeta_head.tpl \
	design/standard/override/templates/embed/eztelemetaitem.tpl

HTDOCS = \
	design/standard/stylesheets/eztelemeta.css \
	design/standard/javascript/soundmanager2.js \
	design/standard/javascript/soundmanager2-nodebug-jsmin.js \
	design/standard/javascript/eztelemeta-player.js \
	design/standard/swf/soundmanager2_flash9.swf \
	design/standard/swf/soundmanager2.swf \
	design/standard/images/play.png \
	design/standard/images/stop.png

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
doc:
	$(MAKE) -C doc

.PHONY: clean
clean:
	$(MAKE) -C doc clean

# vim: set noexpandtab: ts=2: sw=2:
