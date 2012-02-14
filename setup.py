# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import telemeta

CLASSIFIERS = ['Environment :: Web Environment', 'Framework :: Django', 'Intended Audience :: Science/Research', 'Intended Audience :: Education', 'Programming Language :: Python', 'Programming Language :: JavaScript', 'Topic :: Internet :: WWW/HTTP :: Dynamic Content', 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application', 'Topic :: Multimedia :: Sound/Audio', 'Topic :: Multimedia :: Sound/Audio :: Analysis', 'Topic :: Multimedia :: Sound/Audio :: Players', 'Topic :: Scientific/Engineering :: Information Analysis', 'Topic :: System :: Archiving',  ]

setup(
  name = "Telemeta",
  url = "http://telemeta.org",
  description = "open web audio CMS",
  long_description = open('README.rst').read(),
  author = "Guillaume Pellerin",
  author_email = "yomguy@parisson.com",
  version = telemeta.__version__,
  install_requires = [
        'django>=1.3.1',
        'django-registration',
        'django-json-rpc',
        'timeside',
        'south',
  ],
  platforms=['OS Independent'],
  license='CeCILL v2',
  classifiers = CLASSIFIERS,
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False,
)
