from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import os


class Command(BaseCommand):
    help = "import media files from a directory to a collection"
    args = "collection_code media_dir"

    def handle(self, *args, **options):
        collection_code = args[-2]
        media_dir = args[-1]

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
                filename_pre, ext = os.path.splitext(filename)
                items = MediaItem.objects.filter(code=filename_pre)
                if not items:
                    item = MediaItem(collection=collection, code=filename_pre)
                    item.title = filename_pre
                    f = open(path, 'r')
                    file_content = ContentFile(f.read())
                    item.file.save(filename, file_content)
                    item.public_access = 'full'
                    item.save()
                    print 'item created: ' + item.code
                else:
                    print 'item already exists: ' + items[0].code
