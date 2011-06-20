#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('.')
sys.path.append('./sandbox')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sandbox_generic.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

