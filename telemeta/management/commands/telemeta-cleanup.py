from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import logging
import codecs

class Command(BaseCommand):
    help = "Cleanup DB : multiple analyses, data cache, export cache, etc.."
    args = "None"

    def handle(self, *args, **options):

        items = MediaItem.objects.all()
        a_counter = 0

        print 'Cleaning multiple analyses per item...'
        for item in items:

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

