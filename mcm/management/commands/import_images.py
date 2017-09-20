# -*- coding: utf-8 -*

import xml.etree.ElementTree as ET
import os
import logging
import tempfile

import HTMLParser

fields_map = {
    # 'Ia': 'Image',
    'Rr_u' : 'old_id',
    'Arv': 'archive_id',
    'N_a': 'name',
    'Pa_Fr': 'file_path',
    'Pa_Era': 'path_screen',
    'Pa_Prv': 'path_preview',
    'Pa_Or': 'path_original',
    'Orr' : 'order',
    'Ar_s_r': 'site_origin',
    'ar': 'notes',
    u'D_réaur': 'date_creation',
    'D_a': 'doc_size',
    'D_': 'doc_type',
    'Arbus': 'doc_attributes',
    'Width': 'width',
    'Height': 'height',
    'WidthP': 'preview_width',
    'HeightP': 'preview_height',
    'WidthE': 'screen_width',
    'HeightE': 'screen_height',
    'DCreJ': 'creation_day',
    'DCreM': 'creation_month',
    'DCreA': 'creation_year',
    'DModJ': 'modification_day',
    'DModM': 'modification_month',
    'DModA': 'modification_year',
    'HCre': 'creation_time',
    'HMod': 'modification_time'
}


class Command(BaseCommand):
    help = 'Import images from XML'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        # clean_xml_file = cleanup_xml(xml_file)
        # return
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(xml_file, parser=parser)
        root = tree.getroot()

        for image in root.iter('Ia'):
            #for key, field in fields_map.items():
            doc_id = image.findtext('Rr_u')
            
