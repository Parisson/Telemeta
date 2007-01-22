INSTALL ?= install
MAKE ?= make
RM ?= rm
RMDIR ?= rmdir
prefix ?= /usr/local


PREFIX = $(DESTDIR)$(prefix)

BINDIR = $(PREFIX)/bin
MANDIR = $(PREFIX)/share/man/man1
DATADIR = $(PREFIX)/share/telemeta
SRCDIR = $(DATADIR)
#PIXDIR = $(DATADIR)/pix
#RESDIR = $(DATADIR)/res

#APPDIR = $(PREFIX)/share/applications
#ICONDIR = $(PREFIX)/share/pixmaps
#LOCALEDIR = $(PREFIX)/share/locale

#LANGUAGES = `find locale/ -maxdepth 1 -mindepth 1 -type d -printf "%f "`

help:
	@echo Usage:
	@echo "make		- not used"
	@echo "make clean	- removes temporary data"
	@echo "make install	- installs data"
	@echo "make uninstall	- uninstalls data"
	@echo "make help	- prints this help"
	@echo


install:
	echo $(PREFIX)
	$(INSTALL) -m 755 -d $(BINDIR) $(MANDIR) $(DATADIR) $(SRCDIR)
#$(PIXDIR) $(RESDIR) $(APPDIR)
	$(INSTALL) -m 644 *.py $(SRCDIR)
#	$(INSTALL) -m 644 res/*.glade $(RESDIR)
	$(INSTALL) -m 644 debian/telemeta.1 $(MANDIR)
#	$(INSTALL) -m 644 pix/*.png $(PIXDIR)
#	$(INSTALL) -m 644 pix/telemeta.xpm $(ICONDIR)
#	$(INSTALL) -m 644 res/telemeta.desktop $(APPDIR)
	if test -L $(BINDIR)/telemeta; then ${RM} $(BINDIR)/telemeta; fi
	ln -s $(SRCDIR)/telemeta.py $(BINDIR)/telemeta
	chmod +x $(SRCDIR)/telemeta.py
#	$(MAKE) -C po dist
#	for lang in $(LANGUAGES); do \
#		${INSTALL} -m 755 -d $(LOCALEDIR)/$$lang/LC_MESSAGES;\
#		$(INSTALL) -m 644 locale/$$lang/LC_MESSAGES/telemeta.mo $(LOCALEDIR)/$$lang/LC_MESSAGES/; \
#	done


uninstall:
	${RM} $(PREFIX)/bin/telemeta
#	${RM} $(APPDIR)/telemeta.desktop
	${RM} $(MANDIR)/telemeta.1
#	${RM} $(ICONDIR)/telemeta.xpm
	${RM} -rf $(DATADIR)
	$(RMDIR) --ignore-fail-on-non-empty $(BINDIR) $(MANDIR)
#$(APPDIR)
#	for lang in $(LANGUAGES); do \
#		${RM} $(LOCALEDIR)/$$lang/LC_MESSAGES/telemeta.mo; \
#	done

clean:
	${RM} src/*.py[co] res/*~ res/*.bak

.PHONY: help clean install
