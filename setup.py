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
  version = '1.5',
  install_requires = [
        'django==1.6.8',
        'django-registration',
        'django-extensions',
        'django-timezones',
        'django-jqchat',
        'django-debug-toolbar',
        'django-extra-views',
        'django-breadcrumbs',
        'django-bootstrap3',
        'django-bootstrap-pagination',
        'django-json-rpc==0.6.2',
        'django-suit',
        'timeside>=0.5.6',
        'south',
        'sorl-thumbnail',
        'docutils',
        'psutil',
        'pyyaml',
        'python-ebml',
    ],
  tests_require=['pytest-django', 'pytest-cov', 'factory-boy'],
  # Provide a test command through django-setuptest
  cmdclass={'test': PyTest},
  dependency_links = ['https://github.com/yomguy/django-json-rpc/tarball/0.6.2#egg=django-json-rpc-0.6.2'],
  platforms=['OS Independent'],
  license='CeCILL v2',
  classifiers = CLASSIFIERS,
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False,
)
