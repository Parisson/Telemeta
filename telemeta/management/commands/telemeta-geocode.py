from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telemeta.models import Location
from telemeta.util.unaccent import unaccent
import logging
import codecs

class Command(BaseCommand):
    help = "Geocode Telemeta countries from a local Geonames data file"
    args = "path to geoname's allCountries.txt"

    def handle(self, datafile=None, *args, **options):

        if not datafile:
            raise CommandError("Please provide the %s" % self.args)

        try:
            datafile = codecs.open(datafile, 'r', 'utf-8')
        except IOError:
            raise CommandError("Unable to open %s" % datafile)
            
        locations = Location.objects.filter(type=Location.COUNTRY)
        i = 0
        geocoded = 0
        total = locations.count()
        for line in datafile:
            (geonameid, name, asciiname, alternatenames, latitude, longitude, feature_class,
             feature_code, country_code, cc2, admin1_code, admin2_code, admin3_code,
             admin4_code, population, elevation, gtopo30, timezone, modification_date) = line.strip().split("\t")
           
            if feature_class == 'A':
                names = [asciiname.lower()]
                if alternatenames:
                    names.extend([unaccent(n).lower() for n in alternatenames.split(',')])

                for l in locations:
                    if unaccent(l.name).lower() in names:
                        l.latitude = float(latitude)
                        l.longitude = float(longitude)
                        l.save()
                        geocoded += 1

            i += 1

            if i % 200000 == 0:
                print "Geocoded %d out of %d countries (parsed %d geonames)" % (geocoded, total, i)

            if total == geocoded:
                break

        print "Geocoded %d out of %d countries (parsed %d geonames)" % (geocoded, total, i)
        datafile.close()                

