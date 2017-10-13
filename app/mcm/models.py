# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from skosxl.models import Concept

from filer.fields.image import FilerImageField


class HasName(models.Model):
    name = models.CharField(max_length=191, blank=False,
                            verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Author(HasName):
    alias = models.CharField(max_length=191, blank=True, default='')
    comment = models.TextField(default='', verbose_name=_('comment'))
    old_id = models.IntegerField(unique=True, blank=True, null=True)   # Record No

    class Meta:
        verbose_name = _('author')


class Role(models.Model):
    label = models.CharField(_('title'), blank=True, max_length=191)
    text = models.TextField(default='', verbose_name=_('text'))

    def __unicode__(self):
        return self.label


class Reference(HasName):

    class Meta:
        verbose_name = _('reference')


class EventType(HasName):

    class Meta:
        verbose_name = _('event type')


class EventVenue(HasName):

    class Meta:
        verbose_name = _('event venue')


class Event(HasName):
    # <Festival_et_Manifestation>

    class Meta:
        verbose_name = _('event')


class GeographicalClassification(HasName):

    class Meta:
        verbose_name = _('geographical classification')


class EventEdition(models.Model):
    event = models.ForeignKey(Event, blank=True, null=True, verbose_name=_('event'))  # <Festival_et_Manifestation>Japon 93</Festival_et_Manifestation>
    edition = models.IntegerField(default=None, blank=True, null=True)  # <No_edition>16</No_edition>

    def __unicode__(self):
        if self.edition is None:
            return self.event.name
        else:
            return ' - '.join([self.event.name, self.edition.__str__()])


class Support(HasName):

    class Meta:
        verbose_name = _('Support')


DOCUMENT_TYPES = (
    ('a', 'Notice spectacle'),
    ('b', 'Disque'),
    ('c', 'Vidéo DVD&VHS'),
    ('d', 'Vidéo en ligne'),
    ('e', 'Site Internet'),
    ('f', 'Ouvrage & Thèse'),
    ('g', 'Revue'),
    ('h', 'Article'),
    ('i', 'Photo'),
    ('j', 'Affiche - Brochure'),
    ('k', 'Pédagogique'),
    ('l', 'Objet')
)

COLORS = (('C', 'Couleur'),
          ('NB', 'Noir et Blanc'))


class Document(models.Model):

    code = models.CharField(_('code'), unique=False, blank=True, max_length=191)  # Cote
    old_id = models.IntegerField(unique=True, blank=False)   # Record No
    old_doc_no = models.IntegerField(unique=True, null=True)  # Doc no
    authors = models.ManyToManyField(Author, through='AuthorRole', verbose_name=_('author'))  # Auteur
    title = models.TextField(_('title'))  #  TODO change to Charfield(_('title', max_length=191) after database cleanup # Titre

    keywords = models.ManyToManyField(Concept, verbose_name=_('keyword'))  # <Mots-cles>Toraja</Mots-cles>
    text = models.TextField(default='', verbose_name=_('text'))
    related = models.ManyToManyField("self", verbose_name=_('see also'))  # see also / Voir aussi
    contient_contenu_dans = models.ManyToManyField("self", verbose_name=_('Contient ou contenu dans'))
    parents = models.ManyToManyField("self", verbose_name=_('Contient ou contenu dans'))  # A générer à partir de contient_contenu lorsque la hiérarchie est évidente

    doc_type = models.CharField(_('document type'), blank=True, choices=DOCUMENT_TYPES, max_length=32)

    references = models.ManyToManyField(Reference, verbose_name=_('reference'))  # <Reference>Le Chant du Monde</Reference>
    copyright_text = models.CharField(_('copyright'), default='', max_length=191)
    page_num = models.CharField(_('number of pages'), blank=True, max_length=50)
    #<Classement_Thematique>Costume et accessoire</Classement_Thematique>

    def __unicode__(self):
        return self.title


class Language(HasName):

    class Meta:
        verbose_name = _('language')


class Collection(HasName):

    class Meta:
        verbose_name = _('collection')


class Illustration(HasName):

    class Meta:
        verbose_name = _('illustration')


class Captation(HasName):

    class Meta:
        verbose_name = _('type de captation')


class EditionPlace(HasName):

    class Meta:
        verbose_name = _('lieu d\'édition')


class Classification(HasName):

    class Meta:
        verbose_name = _('classification thématique')


class isEdited(models.Model):
    language = models.ManyToManyField(Language, verbose_name=_('language'))
    collection = models.ForeignKey(Collection, verbose_name=_('collection'),
                                   blank=True, null=True)
    collection_num = models.CharField(_('collection number'),
                                      blank=True, max_length=191)
    companion = models.CharField(_('matériel d\'accompagnement'),
                                 blank=True, max_length=50)

    class Meta:
        abstract = True


class AuthorRole(models.Model):

    author = models.ForeignKey(Author, blank=False, verbose_name=_('author'), on_delete=models.CASCADE)  # Auteur
    document = models.ForeignKey(Document, blank=False)
    role = models.ForeignKey(Role, blank=True, null=True)

    class Meta:
        verbose_name = _('author role')


class Notice(Document):
    # Type : a-Notice spectacle

    class Meta:
        verbose_name = "A - Notice spectacle"
        verbose_name_plural = "A - Notices spectacle"

    release_date = models.DateField(_('release date'), null=True, blank=True)  # <Date_de_parution>1995</Date_de_parution>
    release_date_text = models.CharField(_('release date'), blank=True, max_length=191)
    indexation_date = models.DateField(_('indexation date'), null=True, blank=True)  # <Date_de_parution>1995</Date_de_parution>
    indexation_date_text = models.CharField(_('indexation date'), blank=True, max_length=191)
    geographic_classification = models.ForeignKey(GeographicalClassification, null=True, blank=True)  # <Classement_Geographique>P&#233;rou</Classement_Geographique>
    #<Support>Compact Disc Digital Audio</Support>
    #<Duree>69'14</Duree>
    #<Collection>Le chant du monde</Collection>
    #<No_de_collection>CNR 2741004</No_de_collection>
    # indexation_date = models.DateField(_('indexation date'), null=True, blank=True)  # <Date_d_indexation>21/02/16</Date_d_indexation>

    #<Doc_no>5604</Doc_no>
    #<aScript_Source_du_document>Le Chant du Monde ; Editions du CNRS, 1995</aScript_Source_du_document>
    doc_source = models.CharField(_('document source'), blank=True, max_length=191)

    #---  Event - Manifestion
    event_type = models.ForeignKey(EventType, blank=True, null=True)  # <Type_Manifestation>Danse</Type_Manifestation>
    event_venue = models.ForeignKey(EventVenue, blank=True, null=True)  # <Lieu_Manifestation>Le Rond Point, Th&#233;&#226;tre Renaud-Barrault, Paris</Lieu_Manifestation>
    event_edition = models.ForeignKey(EventEdition, blank=True, null=True)


class Disc(Document, isEdited):
    # Type: b-Disque

    support = models.ForeignKey(Support, verbose_name=_('support'),
                                blank=True, null=True)
    captation = models.ForeignKey(Captation, verbose_name=_('captation'),
                                  blank=True, null=True)
    duration = models.CharField(_('duration'), blank=True, max_length=100)

    class Meta:
        verbose_name = "B - Disque"
        verbose_name_plural = "B - Disques"


class Video(Document, isEdited):
    # Type : c-Vidéo DVD&VHS
    support = models.ForeignKey(Support, verbose_name=_('support'),
                                blank=True, null=True)
    captation = models.ForeignKey(Captation, verbose_name=_('captation'),
                                  blank=True, null=True)
    duration = models.CharField(_('duration'), blank=True, max_length=100)
    color = models.CharField(_('color'), blank=True, choices=COLORS, max_length=2)
        
    class Meta:
        verbose_name = "C - Vidéo DVD&VHS"
        verbose_name_plural = "C - Vidéos DVD&VHS"


class VideoFile(Document):
    # Type : d-Vidéo en ligne
    support = models.ForeignKey(Support, verbose_name=_('support'),
                                blank=True, null=True)
    captation = models.ForeignKey(Captation, verbose_name=_('captation'),
                                  blank=True, null=True)
    duration = models.CharField(_('duration'), blank=True, max_length=100)
    color = models.CharField(_('color'), blank=True, choices=COLORS, max_length=2)
    language = models.ManyToManyField(Language, verbose_name=_('language'))

    class Meta:
        verbose_name = "D - Vidéo en ligne"
        verbose_name_plural = "D - Vidéos en ligne"


class BookThesis(Document, isEdited):
    # Type : f-Ouvrage & Thèse
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'),
                                     blank=True, null=True)
    color = models.CharField(_('color'), blank=True, choices=COLORS, max_length=2)
    format = models.TextField(_('format'), blank=True)
    edition_place = models.ForeignKey(EditionPlace, verbose_name=_('edition place'),
                                      blank=True, null=True)

    class Meta:
        verbose_name = "F - Ouvrage & Thèse"
        verbose_name_plural = "F - Ouvrages & Thèses"


class Journal(Document, isEdited):
    # Type : g-Revue
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'),
                                     blank=True, null=True)
    classification = models.ForeignKey(Classification,
                                       verbose_name=_('thematic classification'),
                                       blank=True, null=True)
    format = models.TextField(_('format'), blank=True)
    volume = models.CharField(_('volume'), blank=True, max_length=50)
    number = models.CharField(_('numéro de revue'), blank=True, max_length=50)

    class Meta:
        verbose_name = "G - Revue"
        verbose_name_plural = "G - Revues"


# class Article(Document):
#    # Type : h-Article
#
#    class Meta:
#        verbose_name = "H - Article"
#        verbose_name_plural = "H - Articles"


class Photo(Document):
    # Type : i-Photo

    archive_dvd = models.CharField(_('DVD archive'), max_length=191)  # Cote DVD
    support = models.ForeignKey(Support, verbose_name=_('support'),
                                blank=True, null=True)
    captation = models.ForeignKey(Captation, verbose_name=_('captation'),
                                  blank=True, null=True)
    color = models.CharField(_('color'), blank=True, choices=COLORS, max_length=2)
    format = models.TextField(_('format'), blank=True)
    subject = models.CharField(_('sujet photographié'), blank=True, max_length=191)

    class Meta:
        verbose_name = "I - Photo"
        verbose_name_plural = "I - Photos"


class PosterBooklet(Document):
    # Type : j-Affiche - Brochure
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'),
                                     blank=True, null=True)
    color = models.CharField(_('color'), blank=True, choices=COLORS, max_length=2)
    format = models.TextField(_('format'), blank=True)

    class Meta:
        verbose_name = "J - Affiche-Brochure"
        verbose_name_plural = "J - Affiches-Brochures"

# Type :k-Pédagogique
# class Educational(Document):
#    pass


class Object(Document):
    # Type : l-Objet
    collection = models.ForeignKey(Collection, verbose_name=_('collection'),
                                   blank=True, null=True)
# Description_de_l_objet>Rectangle de tissu jaune resserr&#233; &#224; une extr&#233;mit&#233; avec du fil + un autre rectangle de tissu jaune.</Description_de_l_objet>
# Matiere_et_technique>Tissu ; Fil</Matiere_et_technique>
# Constat_d_etat>Bon &#233;tat ; Tissu d&#233;color&#233;</Constat_d_etat>
# Collection>Maison des Cultures du Monde</Collection>
# Nombre_de_partie>2</Nombre_de_partie>
# Dimension_(HxLxP)>Pi&#232;ce 1 : 149x106 cmPi&#232;ce 2 : 158x238 cm</Dimension_(HxLxP)>
# Localisation # Centre de Documentation sur les Spectacles du Monde, Vitr&#233;, France.

    class Meta:
        verbose_name = "L - Objet"
        verbose_name_plural = "L-Objets"


class Image(models.Model):
    document = models.ForeignKey(Document, blank=False)
    archive_id = models.IntegerField(unique=True, blank=False)
    name = models.CharField(max_length=191, blank=False,
                            verbose_name=_('name'))
    # 'Pa_Fr': 'file_path',
    screen_file = FilerImageField(null=True, blank=True,
                                  related_name="screen_image")
    original_file = FilerImageField(null=True, blank=True,
                                    related_name="original_image")
    #'Pa_Era': 'path_screen',
    #'Pa_Prv': 'path_preview',
    #'Pa_Or': 'path_original',
    order = models.IntegerField(blank=False)
    #'Orr' : 'order',
    #'Ar_s_r': 'site_origin',
    #'ar': 'notes',
    description = models.TextField(default='', verbose_name=_('description'))
    copyright = models.CharField(_('copyright'), max_length=191)
    creation_date = models.DateTimeField(_('creation date'))
    doc_type = models.CharField(_('document type'), max_length=16)
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    screen_image_width = models.IntegerField()
    screen_image_height = models.IntegerField()

    #'D_réaur': 'date_creation',
    #'D_a': 'doc_size',
    #'D_': 'doc_type',
    #'Arbus': 'doc_attributes',
    #'Width': 'width',
    #'Height': 'height',
    #'WidthP': 'preview_width',
    #'HeightP': 'preview_height',
    #'WidthE': 'screen_width',
    #'HeightE': 'screen_height',
    #'DCreJ': 'creation_day',
    #'DCreM': 'creation_month',
    #'DCreA': 'creation_year',
    #'DModJ': 'modification_day',
    #'DModM': 'modification_month',
    #'DModA': 'modification_year',
    #'HCre': 'creation_time',
    #'HMod': 'modification_time'
