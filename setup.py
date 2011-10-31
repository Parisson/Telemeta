# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import telemeta

CLASSIFIERS = ['Environment :: Web Environment', 'Framework :: Django', 'Intended Audience :: Science/Research', 'Intended Audience :: Education', 'Programming Language :: Python', 'Programming Language :: JavaScript', 'Topic :: Internet :: WWW/HTTP :: Dynamic Content', 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application', 'Topic :: Multimedia :: Sound/Audio', 'Topic :: Multimedia :: Sound/Audio :: Analysis', 'Topic :: Multimedia :: Sound/Audio :: Players', 'Topic :: Scientific/Engineering :: Information Analysis', 'Topic :: System :: Archiving',  ]

setup(
  name = "Telemeta",
  url = "http://telemeta.org",
  description = "a web Audio Content Management System",
  long_description = open('README.rst').read(), 
  author = ["Guillaume Pellerin", "Olivier Guilyardi", "Riccardo Zaccarelli"],
  author_email = ["yomguy@parisson.com","olivier@samalyse.com", "riccardo.zaccarelli@gmail.com"],
  version = telemeta.__version__,
  install_requires = [
        'timeside', 
        'Django>=1.2.5',
  ],
  platforms=['OS Independent'],
  license='CeCILL v2',
  classifiers = CLASSIFIERS, 
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False, 
)
