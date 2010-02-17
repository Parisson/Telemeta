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
        
        locations = {}
        for l in Location.objects.all().current().filter(type=Location.COUNTRY):
            locations[l] = [a.alias for a in l.aliases.all()]

        i = 0
        geocoded = 0
        total = len(locations)
        found_by_alias = {}
        for line in datafile:
            (geonameid, name, asciiname, alternatenames, latitude, longitude, feature_class,
             feature_code, country_code, cc2, admin1_code, admin2_code, admin3_code,
             admin4_code, population, elevation, gtopo30, timezone, modification_date) = line.strip().split("\t")
           
            if feature_code[0:3] == 'PCL':
                names = [asciiname.lower()]
                if alternatenames:
                    names.extend([unaccent(n).lower() for n in alternatenames.split(',')])

                found = []
                for l in locations:
                    if unaccent(l.name).lower() in names:
                        l.latitude = float(latitude)
                        l.longitude = float(longitude)
                        l.save()
                        geocoded += 1
                        found.append(l)
                    else:
                        for a in locations[l]:
                            if unaccent(a).lower() in names:
                                found_by_alias[l] = float(latitude), float(longitude)
                                break
                            

                for l in found:
                    locations.pop(l)

            i += 1

            if i % 200000 == 0:
                print "Geocoded %d (%d by alias) out of %d countries (parsed %d geonames)" % (geocoded, len(found_by_alias), total, i)

            if total == geocoded:
                break

        for l in locations:
            if found_by_alias.has_key(l):
                l.latitude, l.longitude = found_by_alias[l]
                l.save()
                geocoded += 1

        print "Done. Geocoded %d out of %d countries (parsed %d geonames)" % (geocoded, total, i)
        datafile.close()                

