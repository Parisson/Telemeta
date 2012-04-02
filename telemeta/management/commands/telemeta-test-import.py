from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from telemeta.cache import TelemetaCache
import urllib

class Command(BaseCommand):
    help = "Test: download and import a test item"
    args = "absolute paths of a local audio files"
    code = 'test'
    title = 'test'
    urls = ['http://files.parisson.com/telemeta/tests/media/sweep.mp3',
            'http://files.parisson.com/telemeta/tests/media/sweep.wav',
            'http://files.parisson.com/telemeta/tests/media/test.ogg',
            'http://files.parisson.com/telemeta/tests/media/test.flac',
            'http://files.parisson.com/telemeta/tests/media/test4.mp3',
            'http://files.parisson.com/telemeta/tests/media/test5.wav',
            'http://files.parisson.com/telemeta/tests/media/test6.wav']

    cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)
    cache_export = TelemetaCache(settings.TELEMETA_EXPORT_CACHE_DIR)

    def handle(self, *args, **options):
        if args:
            self.urls = []
            for file in args:
                self.urls.append('file://' + file)

        collections = MediaCollection.objects.filter(code=self.code)
        if not collections:
            collection = MediaCollection(code=self.code, title=self.title)
            collection.public_access = 'full'
            collection.save()
        else:
            collection = collections[0]

        for url in self.urls:
            code = url.split('/')[-1]
            code = code.replace(' ', '_')
            items = MediaItem.objects.filter(code=code)
            if not items:
                item = MediaItem(collection=collection, code=code, title=code)
                item.save()
            else:
                print 'cleanup'
                item = items[0]
                self.cache_data.delete_item_data(code)
                self.cache_export.delete_item_data(code)
                flags = MediaItemTranscodingFlag.objects.filter(item=item)
                analyses = MediaItemAnalysis.objects.filter(item=item)
                for flag in flags:
                    flag.delete()
                for analysis in analyses:
                    analysis.delete()

            print 'downloading: ' + url
            file = urllib.urlopen(url)
            file_content = ContentFile(file.read())
            item.file.save(code, file_content)
            item.public_access = 'full'
            item.save()
            print 'item created: ' + code
