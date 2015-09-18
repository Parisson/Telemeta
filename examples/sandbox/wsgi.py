#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import os
import sys

here = os.path.dirname(__file__)
sys.path.append(here)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

