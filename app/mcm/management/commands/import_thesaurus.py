# -*- coding: utf-8 -*

from django.core.management.base import BaseCommand, CommandError

from skosxl.models import Label, Concept, Scheme, SemRelation
from skosxl.models import REL_TYPES, LABEL_TYPES

# import lxml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import os
import logging
import tempfile

import HTMLParser

INITIAL_IMPORT = False

class Command(BaseCommand):
    help = 'Import items from XML'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)

    def handle(self, *args, **options):
        xml_file = options['xml_file']

        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(xml_file, parser=parser)
        root = tree.getroot()

        import HTMLParser
        h = HTMLParser.HTMLParser()

        # Scheme
        mcm_scheme, c = Scheme.objects.get_or_create(uri='mcm:thesaurus',
                                                     pref_label='Thesaurus MCM')
        for thesaurus in root.iter('Thesaurus'):

            # Descripteur
            descripteur = thesaurus.findtext('Descripteur')
            record_no = thesaurus.findtext('record_no')
            top_concept = (thesaurus.findtext('Type') == 'MA') 

            try :
                concept, c = Concept.objects.get_or_create(pref_label=descripteur,
                                                           term = record_no,
                                                           scheme = mcm_scheme)
            except concept.MultipleObjectsReturned as e:
                print '-> Duplicated : % s' % descripteur
                #raise e
            if INITIAL_IMPORT:
                concept.top_concept = top_concept
                concept.definition = thesaurus.findtext('Note_d_application', default='')
                concept.changenote = 'Ancien identifiant : %s\n' % record_no

                concept.save()

        # Build relations
        cmpt = 0
        for thesaurus in root.iter('Thesaurus'):
            # Descripteur
            descripteur = thesaurus.findtext('Descripteur')
            record_no = thesaurus.findtext('record_no')
            print record_no, descripteur
            concept, c = Concept.objects.get_or_create(term = record_no,
                                                       scheme = mcm_scheme)


            relations = [('Ta__terme_associe', REL_TYPES.related),
                        ('TG__terme_generique', REL_TYPES.broader),
                        ('TS__terme_specifique', REL_TYPES.narrower)]

            for tag, rel_type in relations:
                for element in thesaurus.findall(tag):
                    target_concept, c = Concept.objects.get_or_create(pref_label=element.text)
                    relation, c = SemRelation.objects.get_or_create(origin_concept = concept,
                                                                    target_concept = target_concept,
                                                                    rel_type = rel_type)
                
            

            for element in thesaurus.findall('Synonymes'):
                Label.objects.get_or_create(concept=concept,
                                                       label_type=LABEL_TYPES.altLabel,
                                                       label_text=element.text,
                                                       language='fr')
            
