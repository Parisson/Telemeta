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
from telemeta.views import PlaylistView

class Command(BaseCommand):
    help = "Export all items or collections metadata to a CSV file"

    def handle(self, *args, **options):
        path = args[-1]
        public_id = args[-2]
        resource_type = args[-3]
        f = open(path, 'w')
        playlist = Playlist.objects.get(public_id=public_id)
        view = PlaylistView()
        elements = view.get_elements(playlist, resource_type)
        writer = UnicodeWriter(f)
        csv = CSVExport(writer)
        csv.write(elements)
        f.close()
