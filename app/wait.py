#!/usr/bin/python

import os, time
from django.core.management import call_command

up = False
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sandbox.settings")

i = 0
while not up:
    try:
        call_command('syncdb', interactive=False)
        up = True
    except:
        i += 1
        print 'initialization...'
        if i > 2:
            raise
        time.sleep(1)
