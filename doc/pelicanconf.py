#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Parisson Sarl'
SITENAME = u'Telemeta project'

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'
DEFAULT_DATE = 'fs'

SITEURL = 'http://parisson.github.io/Telemeta/'
RELATIVE_URLS = True

PATH = 'content/'
DELETE_OUTPUT_DIRECTORY = False

THEME = 'themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'united'

SUMMARY_MAX_LENGTH = 127
SLUGIFY_SOURCE = 'title'
DEFAULT_PAGINATION = 10

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Python', 'http://python.org/'),
          ('Django', 'https://www.djangoproject.com/'),
          ('TimeSide', 'https://github.com/Parisson/TimeSide'),
          ('Docker', 'https://www.docker.com/')
          )

# Social widget
SOCIAL = (('GitHub', 'https://github.com/Parisson/Telemeta'),
          ('Twitter', 'https://twitter.com/telemeta/'),
          ('Google+', 'https://plus.google.com/+Parisson'),
          ('LinkedIn', 'https://www.linkedin.com/company/parisson'),
          )

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pin_to_top']

STATIC_PATHS = ['images', 'css']
CUSTOM_CSS = 'css/custom.css'

# SITELOGO = '/images/logo_telemeta_2.png'

# EXTRA_PATH_METADATA = {
     # 'robots.txt': {'path': 'robots.txt'},
# }

FAVICON = 'images/favicon.ico'

DISQUS_SITENAME = 'telemeta'

TWITTER_CARDS = True
TWITTER_USERNAME = 'telemeta'
TWITTER_WIDGET_ID = '585766293153968128'

GITHUB_USER = 'Parisson'

# Content licensing: CC-BY
CC_LICENSE = "CC-BY"

