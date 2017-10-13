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
from ...models import Support, Captation, Illustration, EditionPlace, Classification

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
                  'Notes_ISBD',
                  'Procede_image',
                  'Localisation']

tag_non_traites = []


def add_author_role(doc, author_id=None, author_name=None, role=None):

    if role is not None:
        role_obj, c = Role.objects.get_or_create(label=role)
    else:
        role_obj = None
    if author_id is not None:
        author_id = int(author_id)
        if author_id in AUTHORS_DOUBLONS.keys():
            print "Replace author_id %d by %d" % (author_id,
                                                  AUTHORS_DOUBLONS[author_id])
            author_id = AUTHORS_DOUBLONS[author_id]
        try:
            author_obj = Author.objects.get(old_id=author_id)
        except Author.DoesNotExist as e:
            print "Does Not Exist -> %s <-" % author_id
            raise e
    else:
        assert(author_name)
        try:
            author_obj, created = Author.objects.get_or_create(name=author_name)
        except Author.MultipleObjectsReturned as e:
            print "Multiple author with name : %s" % author_name
            raise e

    author_role, c = AuthorRole.objects.get_or_create(
        author=author_obj,
        document=doc,
        role=role_obj)
    author_role.save()


class Command(BaseCommand):
    help = 'Import items from XML'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(xml_file, parser=parser)
        root = tree.getroot()

        # Remove all object in Database
        # Document.objects.all().delete()

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
                          #'h-Article': Article,
                          'i-Photo': Photo,
                          'j-Affiche - Brochure': PosterBooklet,
                          'l-Objet': Object
                          }

        skip_document_types = ['e-Site Internet', u'k-Pédagogique', 'h-Article',
                               'l-Objet']  # On traitera les objets à part

        h = HTMLParser.HTMLParser()

        for document in root.iter('Document'):
            doc_type = h.unescape(document.findtext('Type'))
            if doc_type in skip_document_types:
                continue

            record_no = document.findtext('record_no')
            doc_class = DOCUMENT_CLASS[doc_type]
            doc, created = doc_class.objects.get_or_create(old_id=record_no)
            if created:
                doc.save()
            for child in document:
                # print child.tag, child.text
                if child.tag == 'record_no':
                    continue
                elif child.tag in ['No_d_inventaire', 'Cote']:
                    # 'No_d_inventaire' pour les 'l-Objet's
                    doc.code = child.text
                elif child.tag == 'Type':
                    doc.doc_type = child.text[0]
                elif child.tag == 'Titre':
                    # Title
                    doc.title = document.findtext('Titre')
                elif child.tag == 'Doc_no':
                    doc.old_doc_no = child.text
                elif child.tag == 'Mots-cles':
                    try:
                        keyword = child.text
                        if keyword == 'pu':
                            keyword = 'Pu'
                        keyword_obj = Concept.objects.get(pref_label=keyword)
                        if keyword_obj not in doc.keywords.all():
                            doc.keywords.add(keyword_obj)
                    except Concept.DoesNotExist:
                        print 'Concept \" %s \" DoesNotExist' % keyword
                elif child.tag == 'Texte':
                    text = child.text
                    if not text:
                        text = ''
                    doc.text = text
                elif child.tag == 'Type_Manifestation':
                    event_type = child.text
                    event_type_obj, c = EventType.objects.get_or_create(
                        name=event_type)
                    doc.event_type = event_type_obj
                elif child.tag == 'Lieu_Manifestation':
                    event_venue = child.text
                    event_venue_obj, c = EventVenue.objects.get_or_create(
                        name=event_venue)
                    doc.event_venue = event_venue_obj

                elif child.tag == 'Festival_et_Manifestation':
                    event = child.text
                    event_obj, c = Event.objects.get_or_create(name=event)
                    edition = document.findtext('No_edition')
                    if not edition:
                        edition = None
                    try:
                        event_edition_obj, c = EventEdition.objects.get_or_create(
                            event=event_obj, edition=edition)
                    except ValueError:
                        print '----------------'
                        print 'Pb sur le document : Record num %s / Cote %s' % (doc.old_id, doc.code)
                        print 'Pb Edition %s' % edition
                        # print 'Pb Edition Event %s' % event
                        print '----------------'
                        event_edition_obj, c = EventEdition.objects.get_or_create(
                            event=event_obj, edition=None)

                        doc.event_edition = event_edition_obj
                elif child.tag == 'No_edition':
                    continue
                elif child.tag == 'Date_de_parution':
                    doc.release_date_text = child.text

                    try:
                        release_date = datetime.datetime.strptime(child.text,
                                                                  '%d/%m/%y').date()
                        doc.release_date = release_date
                    except ValueError:
                        pass
                elif child.tag == 'Date_d_indexation':
                    doc.indexation_date_text = child.text

                    try:
                        indexation_date = datetime.datetime.strptime(child.text,
                                                                     '%d/%m/%y').date()
                        doc.indexation_date = indexation_date
                    except ValueError:
                        pass

                elif child.tag == 'aScript_auteurs3':
                    # Authors
                    doc_authors = child.text
                    if doc_authors is not None:
                        authors_roles = [auth.split('==')
                                         for auth in doc_authors.split(';')]
                        for author_id, role in authors_roles:
                            add_author_role(doc, author_id=author_id, role=role)
                # Referencess
                elif child.tag == 'Reference':
                    ref_obj, ref_c = Reference.objects.get_or_create(
                        name=child.text)
                    doc.references.add(ref_obj)
                elif child.tag == 'Voir_aussi':
                    related_doc, created = Document.objects.get_or_create(old_id=child.text)
                    if created:
                        related_doc.save()
                    doc.related.add(related_doc)
                # Source du document
                elif child.tag == 'aScript_Source_du_document':
                    doc.source_doc = child.text

                #  GeographicalClassification
                elif child.tag == 'Classement_Geographique':
                    geo_obj, c = GeographicalClassification.objects.get_or_create(
                        name=child.text)
                    doc.geographic_classification = geo_obj
                elif child.tag == 'archive_DVD':
                    doc.archive_dvd = child.text
                elif child.tag == 'auteur_Photo':
                    author_name = child.text
                    role = 'Photographe'
                    add_author_role(doc, author_name=author_name, role=role)

                elif child.tag == 'aut._Prog._-_Notice':
                    author_name = child.text
                    role = 'Rédacteur Notice'
                    add_author_role(doc, author_name=author_name, role=role)
                elif child.tag == 'auteur_affiche_dessin':
                    author_name = child.text
                    role = 'Dessinateur'
                    add_author_role(doc, author_name=author_name, role=role)
                elif child.tag == 'Copyright':
                    doc.copyright_text = child.text
                elif child.tag == 'Collection':
                    collection = child.text
                    if collection:
                        collection_obj, created = Collection.objects.get_or_create(name=collection)
                        doc.collection = collection_obj
                elif child.tag == 'Langue':
                    language = child.text
                    if Language:
                        language_obj, created = Language.objects.get_or_create(name=Langue)
                        doc.language.add(language_obj)
                 
                elif child.tag == 'Nbre_No_de_page':
                    doc.page_num = child.text
                elif child.tag == 'Support':
                    support_obj, c = Support.objects.get_or_create(name=child.text)
                    doc.support = support_obj
                elif child.tag == 'Duree':
                    doc.duration = child.text
                elif child.tag == 'Illustration':
                    illustration_obj, c = Illustration.objects.get_or_create(name=child.text)
                    doc.illustration = illustration_obj
                elif child.tag == 'Couleur':
                    if child.text == 'Couleur':
                        doc.color = 'C'
                    elif child.text == 'Noir et Blanc':
                        doc.color = 'NB'
                elif child.tag == 'Type_Captation':
                    captation_obj, c = Captation.objects.get_or_create(name=child.text)
                    doc.captation = captation_obj
                elif child.tag == 'No_de_collection':
                    doc.collection_num = child.text
                elif child.tag == 'Format':
                    doc.format = child.text
                
                elif child.tag == 'Lieu_d_edition':
                    edition_obj, c = EditionPlace.objects.get_or_create(name=child.text)
                    doc.edition_place = edition_obj
                elif child.tag == 'Classement_Thematique':
                    classif_obj, c = Classification.objects.get_or_create(name=child.text)
                    doc.classification = classif_obj
                elif child.tag == 'Materiel_d_accompagnement':
                    doc.companion = child.text
                    
                elif child.tag == 'Sujet_photographie':
                    doc.subject =  child.text
                elif child.tag == 'Volume':
                    doc.volume =  child.text
                
                elif child.tag == 'No_revue':
                    doc.number =  child.text
                # Tag non traité :
                #'Contient_Contenu_dans', : traité à part
                elif child.tag in IGNORED_FIELDS:
                    continue
                else:
                    if child.tag not in tag_non_traites:
                        tag_non_traites.append(child.tag)
                        print 'Tag non traité : %s' % child.tag

                doc.save()
        print tag_non_traites
