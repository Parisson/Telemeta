# -*- coding: utf-8 -*

from django.core.management.base import BaseCommand, CommandError

from ...models import Document
from ...models import Notice, Disc, Video, VideoFile, BookThesis, Journal
from ...models import Article, Photo, PosterBooklet, Object
from ...models import Author, Role, AuthorRole
from ...models import Reference
from ...models import Event, EventEdition, EventType, EventVenue
from ...models import GeographicalClassification
from skosxl.models import Concept

from ftfy import fix_text

# import lxml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import os
import logging
import tempfile

import HTMLParser


DEBUG = False

replacements_tag = {
    'auteur_affiche_(dessin)>': 'auteur_affiche_dessin>',
    'auteur_affiche_(dessin).Documents>': 'auteur_affiche_dessin_Documents>',
    '[record_no]>': 'record_no>',
    '->_Intervention>': 'Auteurs_intervention>',
    #'\00': '',
}

replacements_char = {
    '&#2<': '???<',
    '&#146;': '&apos;',
    '&#156;': '&oelig;',
    '&<': '?<',
    '\373': '&ucirc;',
    'sa lta nata': 'saltanata',
    'Gugak FM': 'Gugak FM',
    '\xf5': '&#305;',
    '\x1e': '',
    '\x02': '',
    '\xf9': '?',
    '\xb7': '?',
    '\371': '',
    '\xc3': '&ugrave;',  # ù
}


def cleanup_xml(xml_file):
    root, ext = os.path.splitext(xml_file)
    clean_xml_file = ''.join([root, '_clean', ext])
    log_file = ''.join([root, '_clean_log.txt'])
    if os.path.exists(log_file):
        os.unlink(log_file)
    logging.basicConfig(filename=log_file, format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logging.info('Nettoyage du fichier XML %s', xml_file)
    # if os.path.exists(clean_xml_file):
    #    return clean_xml_file
    h = HTMLParser.HTMLParser()
    temp_xml = tempfile.NamedTemporaryFile(delete=False)
    # 1ere passe : nettoyage des tags XML
    with open(xml_file, 'U') as infile:
        with open(temp_xml.name, 'w') as outfile:
            for line in infile:
                for src, target in replacements_tag.iteritems():
                    if src in line:
                        line = line.replace(src, target)
                outfile.write(line)

    # 2nde passe : nettoyage des caractères
    with open(temp_xml.name, 'U') as infile:
        with open(clean_xml_file, 'w') as outfile:
            lineno = 0
            for line in infile:
                lineno += 1
                change_line = False
                if False:
                    for src, target in replacements_char.iteritems():
                        if src in line:
                            change_line = True
                            logging.info('Ligne : %d', lineno)
                            logging.info('%s -> %s', src, target)
                            logging.info('Ligne de texte originale: %s', line)
                            line = line.replace(src, target)
                            logging.info('Ligne de texte de remplacement : %s', line)
                            try:
                                line = h.unescape(line)
                            except UnicodeDecodeError as e:
                                print line
                                print "Ligne N°%d" % lineno
                            raise e
                            if change_line:
                                logging.info('Ligne de texte de remplacement HTML : %s', line)
                    # outfile.write(line.encode('utf-8'))
                print fix_text(line)
                outfile.write(fix_text(line))

    os.unlink(temp_xml.name)

    return clean_xml_file


class Command(BaseCommand):
    help = 'Import items from XML'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        # clean_xml_file = cleanup_xml(xml_file)
        # return
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(xml_file, parser=parser)
        root = tree.getroot()

        # Remove all object in Database
        # Document.objects.all().delete()

        document_traite = 0
        document_non_traite = 0

        # <Type>a-Notice spectacle</Type>
        # <Type>b-Disque</Type>
        # <Type>c-Vidéo DVD&#38;VHS</Type>
        # <Type>d-Vid&#233;o en ligne</Type>
        # <Type>f-Ouvrage &#38; Th&#232;se</Type>
        # <Type>g-Revue</Type>
        # <Type>h-Article</Type>
        # <Type>i-Photo</Type>
        # <Type>j-Affiche - Brochure</Type>
        # <Type>k-P&#233;dagogique</Type>
        # <Type>l-Objet</Type>

        DOCUMENT_CLASS = {'a-Notice spectacle': Notice,
                          'b-Disque': Disc,
                          u'c-Vidéo DVD&VHS': Video,
                          u'd-Vidéo en ligne': VideoFile,
                          u'f-Ouvrage & Thèse': BookThesis,
                          'g-Revue': Journal,
                          'h-Article': Article,
                          'i-Photo': Photo,
                          'j-Affiche - Brochure': PosterBooklet,
                          'l-Objet': Object
                          }

        skip_document_types = ['e-Site Internet', u'k-Pédagogique',
                               'l-Objet']  # On traitera les objets à part

        h = HTMLParser.HTMLParser()

        for document in root.iter('Document'):
            doc_type = h.unescape(document.findtext('Type'))
            if doc_type in skip_document_types:
                continue

            document_traite += 1
            record_no = document.findtext('record_no')
            if doc_type == 'l-Objet':
                code = document.findtext('No_d_inventaire')
            else:
                code = document.findtext('Cote')

            doc_class = DOCUMENT_CLASS[doc_type]
            doc, created = doc_class.objects.get_or_create(old_id=record_no)
            doc.code = code
            doc.doc_type = doc_type[0]
            # Title
            doc.title = document.findtext('Titre')
            doc.save()
            # if not created:
            #    continue
            # Keywords
            for keyword in document.findall('Mots-cles'):
                try:
                    keyword_obj = Concept.objects.get(pref_label=keyword.text)
                    if keyword_obj not in doc.keywords.all():
                        doc.keywords.add(keyword_obj)
                except Concept.DoesNotExist:
                    print 'Concept \" %s \" DoesNotExist' % keyword.text

            # Text
            doc.text = document.findtext('Texte')
            if doc.text is None:
                doc.text = ''
            # Notice spectacle
            if doc_type == 'a-Notice spectacle':

                event_type = document.findtext('Type_Manifestation')
                if event_type is not None:
                    event_type_obj, c = EventType.objects.get_or_create(
                        name=event_type)
                else:
                    event_type_obj = None

                event_venue = document.findtext('Lieu_Manifestation')
                if event_venue is not None:
                    event_venue_obj, c = EventVenue.objects.get_or_create(
                        name=event_venue)
                else:
                    event_venue_obj = None

                event = document.findtext('Festival_et_Manifestation')
                if event is not None:
                    event_obj, c = Event.objects.get_or_create(name=event)

                    edition = document.findtext('No_edition')
                    try:
                        event_edition_obj, c = EventEdition.objects.get_or_create(
                            event=event_obj, edition=edition)
                    except ValueError:
                        print 'Pb Edition : Cote %s / Event %s / Edition %s' % (code, event, edition)
                        event_edition_obj, c = EventEdition.objects.get_or_create(
                            event=event_obj, edition=None)

                    doc.event_edition = event_edition_obj
                    doc.event_type = event_type_obj
                    doc.event_venue = event_venue_obj

                release_date_text = document.findtext('Date_de_parution')
                doc.release_date_text = release_date_text

                import datetime
                try:
                    release_date = datetime.datetime.strptime(release_date_text,
                                                              '%d/%m/%y').date()
                    doc.release_date = release_date
                except ValueError:
                    pass

                # Authors
                doc_authors = document.findtext('aScript_auteurs3')
                if doc_authors is not None:
                    authors_roles = [auth.split('==')
                                     for auth in doc_authors.split(';')]
                    for author_id, role in authors_roles:
                        if role:
                            role_obj, c = Role.objects.get_or_create(label=role)
                        else:
                            role_obj = None
                        try:
                            author_obj = Author.objects.get(old_id=author_id)
                        except Author.DoesNotExist as e:
                            print "Does Not Exist ->%s<-" % author_id
                            raise e

                        try:
                            author_role, c = AuthorRole.objects.get_or_create(
                                author=author_obj,
                                document=doc,
                                role=role_obj)
                            author_role.save()

                        except UnicodeError as e:
                            print authors_roles
                            print 'role: %s' % role
                            raise e

                # Referencess
                for ref in document.findall('Reference'):
                    ref_obj, ref_c = Reference.objects.get_or_create(
                        name=ref.text)
                    doc.references.add(ref_obj)

                # Source du document
                source_doc = document.findtext('aScript_Source_du_document')
                if source_doc is not None:
                    doc.source_doc = source_doc

                #  GeographicalClassification
                geo = document.findtext('Classement_Geographique')
                if geo is not None:
                    geo_obj, c = GeographicalClassification.objects.get_or_create(
                        name=geo)
                    doc.geographic_classification = geo_obj
                doc.save()

            if DEBUG & (document_traite > 100):
                break
        print '-*-*--*-*-*-*-*-*-*-*'
        print 'document_traité : %d' % document_traite
        print 'document_non_traité : %d' % document_non_traite
