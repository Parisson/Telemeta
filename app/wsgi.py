#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.dirname('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()
