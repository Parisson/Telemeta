from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import translation
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import logging
import codecs
from xlwt import Workbook

class Command(BaseCommand):
    help = "Export media fields to a XLS file (see an example in example/data/"
    args = "path"
    first_row = 1
    admin_email = 'webmaster@parisson.com'
    language_codes = ['en_US', 'fr_FR', 'de_DE']
    models = [MediaFonds, MediaCorpus, MediaCollection, MediaItem]
    width = 256

    def handle(self, *args, **options):
        self.file = args[0]
        self.book = Workbook()
        for model in self.models:
            self.sheet = self.book.add_sheet(model.element_type)
            self.sheet.write(0, 0, 'Field')
            self.sheet.col(0).width = self.width*32

            k = 1
            for language_code in self.language_codes:
                self.sheet.write(0, k, language_code)
                self.sheet.col(k).width = self.width*32
                k += 1

            i = 1
            for field in model._meta.fields:
                self.sheet.write(i, 0, field.attname)
                j = 1
                for language_code in self.language_codes:
                    translation.activate(language_code)
                    self.sheet.write(i, j, unicode(field.verbose_name.lower()))
                    j += 1
                i += 1

        self.book.save(self.file)
