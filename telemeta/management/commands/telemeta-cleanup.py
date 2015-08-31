from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from telemeta.cache import TelemetaCache
import logging
import codecs

class Command(BaseCommand):
    help = "Cleanup DB : multiple analyses, data cache, export cache, etc.."
    args = "cache"
    cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)
    cache_export = TelemetaCache(settings.TELEMETA_EXPORT_CACHE_DIR)

    def handle(self, *args, **options):
        items = MediaItem.objects.all()
        a_counter = 0

        print 'cleaning multiple analyses per item...'
        for item in items:
            if 'cache' in args:
                print 'cleaning cache...'
                self.cache_data.delete_item_data(item.code)
                self.cache_export.delete_item_data(item.code)

            analyses = MediaItemAnalysis.objects.filter(item=item)
            ids = []
            for analysis in analyses:
                id = analysis.analyzer_id
                if id in ids:
                    print 'item : ' + item.code + ' analyzer_id : ' + id
                    analysis.delete()
                    a_counter += 1
                else:
                    ids.append(id)

        print "Done, cleaned %s analyses" % str(a_counter)



