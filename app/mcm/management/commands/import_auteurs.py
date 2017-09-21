# -*- coding: utf-8 -*

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

# import lxml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import os
import logging
import tempfile

from mcm.models import Author

import HTMLParser

INITIAL_IMPORT = False


class Command(BaseCommand):
    help = 'Import items from XML'

    # def add_arguments(self, parser):
    #    parser.add_argument('xml_file', type=str, default='data/exports/Auteurs_clean.xml')

    def handle(self, *args, **options):
        xml_file = 'data/exports/Auteurs_clean.xml'

        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(xml_file, parser=parser)
        root = tree.getroot()

        h = HTMLParser.HTMLParser()

        # for author in Author.objects.all():
        #    author.delete()

        for author in root.iter('Auteur'):

            # Auteur
            # fields:
            #   - name = models.CharField(max_length=100, blank=False, unique=True)
            #   - alias = models.CharField(max_length=100, blank=True, default='')
            #   - comment = models.TextField(default='')
            #   - old_id = models.IntegerField(unique=True, blank=False)   # Record No

            name = author.findtext('Nom')
            record_no = author.findtext('record_no')
            try:
                auteur, c = Author.objects.get_or_create(name=name,
                                                         old_id=record_no)
            except IntegrityError as e:
                print 'Auteur : %s / id: %s' % (name, record_no)
                doublon = Author.objects.get(name=name)
                print '  en conflit avec %s / id: %s' % (doublon.name, doublon.old_id)
                raise e
