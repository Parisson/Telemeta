from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import os


class Command(BaseCommand):
    help = "apply a equal time shift to all markers of an item putting the first one to 0s"
    args = "code"

    def handle(self, *args, **options):
        code = args[-1]

        items = MediaItem.objects.filter(code__contains=code)
        if items:
            item = items[0]
            markers = item.markers.all()
            time_shift = markers[0].time
            for marker in markers:
                marker.time -= time_shift
                marker.save()
        else:
            exit("No such item")
