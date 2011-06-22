#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import os
import sys

here = os.path.dirname(__file__)

sys.path.append(here)
sys.path.append(os.path.join(here,'sandbox'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'sandbox_generic.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

