from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import os, sys


class Command(BaseCommand):
    help = "import media files from a directory in the media directory into a collection (no file copy)"
    args = "collection_code media_dir"

    def handle(self, *args, **options):
        collection_code = args[-2]
        media_dir = args[-1]

        if not media_dir in settings.MEDIA_ROOT:
            sys.exit('This directory is not in the MEDIA_ROOT directory')

        collections = MediaCollection.objects.filter(code=collection_code)
        if not collections:
            collection = MediaCollection(code=collection_code, title=collection_code)
            collection.public_access = 'full'
            collection.save()
            print 'collection created: ' + collection_code
        else:
            collection = collections[0]
            print 'using collection: ' + collection.code

        for root, dirs, files in os.walk(media_dir):
            for filename in files:
                path = root + os.sep + filename
                name, ext = os.path.splitext(filename)
                items = MediaItem.objects.filter(code=name)
                if not items:
                    item = MediaItem(collection=collection, code=name)
                    item.title = name
                    item.file.path = path
                    item.public_access = 'full'
                    item.save()
                    print 'item created: ' + item.code
                else:
                    print 'item already exists: ' + items[0].code
