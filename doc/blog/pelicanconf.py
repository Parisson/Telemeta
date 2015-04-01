#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Parisson Sarl'
SITENAME = u'Telemeta'
#SITEURL = ''
RELATIVE_URLS = True

PATH = 'content/'

THEME = 'themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'united'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'
DEFAULT_DATE = 'fs'

SUMMARY_MAX_LENGTH = 127
SLUGIFY_SOURCE = 'title'
DEFAULT_PAGINATION = 10


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python', 'http://python.org/'),
          ('Django', 'https://www.djangoproject.com/'),
          )

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/telemeta/'),
          ('Google+', 'https://plus.google.com/+Parisson'),
          ('LinkedIn', 'http://www.linkedin.com/in/Parisson'),
          ('GitHub', 'https://github.com/Parisson/'),
          )

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# PLUGIN_PATHS = ['plugins']
# PLUGINS = ['pin_to_top']

STATIC_PATHS = ['images', 'css']
CUSTOM_CSS = '/css/custom.css'
# SITELOGO = '/images/logo_telemeta_2.png'