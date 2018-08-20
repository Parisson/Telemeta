# -*- coding: utf-8 -*-
import multiprocessing
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import sys


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


CLASSIFIERS = ['Environment :: Web Environment',
'Framework :: Django',
'Intended Audience :: Science/Research',
'Intended Audience :: Education',
'Programming Language :: Python',
'Programming Language :: JavaScript',
'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
'Topic :: Multimedia :: Sound/Audio',
'Topic :: Multimedia :: Sound/Audio :: Analysis',
'Topic :: Multimedia :: Sound/Audio :: Players',
'Topic :: Scientific/Engineering :: Information Analysis',
'Topic :: System :: Archiving',  ]


setup(
  name = "Telemeta",
  url = "http://telemeta.org",
  description = "Open web audio application with semantics",
  long_description = open('README.rst').read(),
  author = "Guillaume Pellerin",
  author_email = "yomguy@parisson.com",
  version = '1.6.9',
  install_requires = [
    'django==1.6.11',
    'django-breadcrumbs==1.1.3',
    'django-bootstrap3==6.2.1',
    'django-bootstrap-pagination==1.6.4',
    'django-celery==3.2.2',
    'django-debug-toolbar==1.3.2',
    'django-dirtyfields==1.2.1', # require for Django1.6 compatibility
    'django-environ==0.4.5',
    'django-extensions==1.6.7',
    'django-extra-views==0.8.0',
    'django-google-tools==1.1.0',
    'django-haystack==2.4.1',
    'django-ipauth==0.4.1',
    'django-jqchat',
    'django-json-rpc==0.7.2',
    'django-registration==1.0',
    'django-suit==0.2.26',
    'django-timezones==0.2',
    'docutils==0.14',
    'ebooklib',
    'elasticsearch==1.6.0',
    'psutil==5.4.6',
    'python-ebml==0.2.1',
    'pyyaml==3.12',
    'redis==2.10.6',
    'south==1.0.2',
    'sqlparse==0.1.19'
    'timeside>=0.7',
    'Werkzeug==0.14.1',
    'zipstream==1.1.4',
    ],
  tests_require=['pytest-django', 'pytest-cov', 'factory-boy'],
  # Provide a test command through django-setuptest
  cmdclass={'test': PyTest},
  platforms=['OS Independent'],
  license='CeCILL v2',
  classifiers = CLASSIFIERS,
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False,
)
