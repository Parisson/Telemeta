from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import logging
import codecs

class Command(BaseCommand):
    help = "Init original formats from a txt file (see files in example/init/"
    args = "path"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        path = args[0]
        file = open(path, 'r')
        for format in file.readlines():
            if not PhysicalFormat.objects.filter(value=format):
                format = PhysicalFormat(value=format)
                format.save()





