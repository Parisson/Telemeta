# -*- coding: utf-8 -*

from django.core.management.base import BaseCommand, CommandError

from ...models import Document
from ...models import Notice, Disc, Video, VideoFile, BookThesis, Journal
from ...models import Photo, PosterBooklet, Object
from ...models import Author, Role, AuthorRole
from ...models import Reference
from ...models import Event, EventEdition, EventType, EventVenue
from ...models import GeographicalClassification
from ...models import Collection, Language

from skosxl.models import Concept

#from ftfy import fix_text

# import lxml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import os
import logging
import tempfile

import HTMLParser
import datetime

from .merge_authors import DOUBLONS as AUTHORS_DOUBLONS
DEBUG = False
IGNORED_FIELDS = ['auteurs_val',
                  'auteurs',
                  'Intervention_code',
                  'Intervention_script',
                  'aScript_auteurs2',
                  'Voir_aussi_val',
                  'aScript_Liste_des_images',
                  # Anciens Inutiles
                  'url_site_internet',
                  'ISBN_ISSN',
                  'Procede_image',
                  'Localisation']

tag_non_traites = []




class Command(BaseCommand):
    help = 'Import items from XML'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)
        parser.add_argument('field', type=str)

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        field = options['field']
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(xml_file, parser=parser)
        root = tree.getroot()


        skip_document_types = ['e-Site Internet', u'k-Pédagogique', 'h-Article',
                               'l-Objet']  # On traitera les objets à part

        h = HTMLParser.HTMLParser()

        list_doc = []
        list_values = []
        
        for document in root.iter('Document'):
            doc_type = h.unescape(document.findtext('Type'))
            if doc_type in skip_document_types:
                continue

            #record_no = document.findtext('record_no')
            field_text = document.findtext(field)

            if field_text:
                if field_text not in list_values:
                    list_values.append(field_text)
                #print field_text.encode('utf-8')
                if doc_type not in list_doc:
                    list_doc.append(doc_type)
        
        print "Values : %s" % list_values
        print "Doc types : %s" % list_doc
        max_length = max([len(val) for val in list_values])
        print "Max Field length : %d" % max_length
