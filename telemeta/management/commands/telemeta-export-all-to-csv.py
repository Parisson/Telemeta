from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import os
import timeside.core
from timeside.server.models import *
from timeside.core.tools.test_samples import generateSamples
from telemeta.models import *
from telemeta.util.unicode import *


class Command(BaseCommand):
    help = "Export all items or collections metadata to a CSV file"

    def handle(self, *args, **options):
        path = args[-1]
        element_type = args[-2]
        f = open(path, 'w')
        if element_type == "item":
            elements = MediaItem.objects.all()
        elif element_type == "collection":
            elements = MediaCollection.objects.all()
        else:
            raise TypeError('type should be "item" or "collection"')
        writer = UnicodeWriter(f)
        csv = CSVExport(writer)
        csv.write(elements)
        f.close()
