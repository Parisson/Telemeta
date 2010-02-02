from optparse import make_option
from django.conf import settings
from django.core.management.base import NoArgsCommand
from telemeta.models import Location
from telemeta.util.unaccent import unaccent
import geopy
import logging

class Command(NoArgsCommand):
    help = "Update Telemeta Locations latitudes and longitudes (currently only countries)"

    def handle_noargs(self, **options):

        geocoder = geopy.geocoders.Google(settings.TELEMETA_GMAP_KEY)
        logging.getLogger().setLevel(logging.WARNING)

        locations = Location.objects.filter(type=Location.COUNTRY)
        total = locations.count()
        processed = 0
        success = 0
        for location in locations:
            try:
                r = geocoder.geocode(unaccent(unicode(location)), exactly_one=False)
                try:
                    place, (lat, lng) = r.next()
                    location.latitude = lat
                    location.longitude = lng
                    location.save()
                    success += 1
                except StopIteration:
                    pass
            except ValueError, e: 
                print "Failed on %s: %s" % (unaccent(unicode(location)), e.message)

            processed += 1
            if processed % 20 == 0 or processed == total:
                print "Processed %d/%d locations (success: %d, failures: %d)" \
                      % (processed, total, success, processed - success)

