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
  version = '1.7.4',
  install_requires = [
    'django==1.8.*',
    'django-bootstrap-pagination==1.6.4',
    'django-bootstrap3==8.1.0',
    'django-breadcrumbs==1.1.3',
    'django-celery==3.2.2',
    'django-dirtyfields==1.2.1',
    'django-environ==0.4.5',
    'django-extensions==2.1.0',
    'django-extra-views==0.11.0',
    'django-debug-toolbar==1.6',
    'django-haystack==2.4.1',
    'django-ipauth',
    'django-json-rpc==0.7.2',
    'django-registration-redux==2.4',
    'django-suit==0.2.26',
    'django-timezones==0.2',
    'djangorestframework==3.6.4',
    'docutils==0.14',
    'ebooklib',
    'elasticsearch==1.6.0',
    'lxml==4.2.3',
    'psutil==5.4.6',
    'pyyaml==3.12',
    'python-ebml==0.2.1',
    'redis==2.10.6',
    'sqlparse==0.2.2',
    'timeside==0.9.6',
    'Werkzeug==0.15.3',
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
