# coding: utf8
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.utils.encoding import smart_str


from telemeta.models.instrument import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from telemeta.views.core import *
from telemeta.views.core import serve_media
from django.template import RequestContext, Template

import os
import sys
from lxml import etree
from datetime import datetime
import unicodedata
class ExportView(object):

    def skos(self):
        Instruments = Instrument.objects.all()
        Alias = InstrumentAlias.objects.all()
        Instrument_relation =InstrumentRelation.objects.all()
        Instrument_alias_relation = InstrumentAliasRelation.objects.all()
        today = datetime.today()
        # en tête du xml
        f = open("export/telemeta.xml", 'w')

        s = '<?xml version="1.0" encoding="UTF-8"?>\n\
                        <rdf:RDF\
                        xmlns:skos="http://www.w3.org/2004/02/skos/core#"\n\
                        xmlns:dc="http://purl.org/dc/elements/1.1/"\n\
                        xmlns:dcterms="http://purl.org/dc/terms/"\n\
                        xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"\n\
                        xmlns:iso-thes="http://purl.org/iso25964/skos-thes#"\n\
                        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n\
                       '
        f.write(s.encode('utf-8'))
        # description du concept de schéma

        s = '<rdf:Description rdf:about="http://localhost:8080/opentheso-4.3.0/101">\n\
                        <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#ConceptScheme"/>\n\
                        <skos:prefLabel xml:lang="fr">instrumentDJANGO</skos:prefLabel>\n\
                        <iso-thes:microThesaurusOf rdf:resource="http://localhost:8080/opentheso-4.3.0/1"/>\n\
                        <dcterms:created rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
            + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '</dcterms:created>\n\
                        <dcterms:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
            + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '</dcterms:modified>\n\
                        </rdf:Description>\n'

        # description de la collection instrument
        f.write(s.encode('utf-8'))
        s = '<rdf:Description rdf:about="http://localhost:8080/opentheso-4.3.0/MT101">\n\
                        <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Collection"/>\n\
                        <skos:prefLabel xml:lang="fr">instrument</skos:prefLabel>\n\
                        <iso-thes:microThesaurusOf rdf:resource="http://localhost:8080/opentheso-4.3.0/101"/>\n'
        f.write(s.encode('utf-8'))
        for instru in Instruments:# parcours de toutes les valeurs de la table instrument
            # ajout des membres dans la collection
            s =   '  <skos:member rdf:resource="http://localhost:8080/opentheso-4.3.0/IM_' + str(instru.id) + '"/>\n'
            f.write(s.encode('utf-8'))
        for alias in Alias:                  # parcours de toutes les valeurs de la table alias_instrument
            # ajout des membres dans la collection
            s =  '  <skos:member rdf:resource="http://localhost:8080/opentheso-4.3.0/A_' + str(alias.id)+ '"/>\n'
            f.write(s.encode('utf-8'))
        s = '  <dcterms:created rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
            + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '</dcterms:created>\n\
                  <dcterms:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
            + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '</dcterms:modified>\n\
                </rdf:Description>\n'
        f.write(s.encode('utf-8'))
        for instru in Instruments : # parcours de toutes les valeurs de la table instrument
            isenfant = False
            s =  '<rdf:Description rdf:about="http://localhost:8080/opentheso-4.3.0/IM_' + str(instru.id) + '">\n\
                                <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>\n\
                                <skos:prefLabel xml:lang="fr">' + unicodedata.normalize('NFD',instru.name).encode('ascii','ignore') + '</skos:prefLabel>\n\
                                <skos:inScheme rdf:resource="http://localhost:8080/opentheso-4.3.0/101"/>\n '
            f.write(s.encode('utf-8'))
            for relation in Instrument_relation:  # parcours de toutes les relations entre les instruments

                if relation.instrument.id == instru.id:  # si l'id de l'instrument actuellement parcouru correspond à l'id de l'instruement fils de la relation
                    isenfant = True
                    s =  '           <skos:broader rdf:resource = "http://localhost:8080/opentheso-4.3.0/IM_' + str(relation.parent_instrument.id) + '"/>\n'
                    f.write(s.encode('utf-8'))
                elif relation.parent_instrument.id == instru.id:  # si l'id de l'instrument actuellement parcouru correspond à l'id de l'instruement_parent de la relation
                    s = '           <skos:narrower rdf:resource  = "http://localhost:8080/opentheso-4.3.0/IM_' +str(relation.instrument.id) + '"/>\n'
                    f.write(s.encode('utf-8'))
            if not isenfant:
                s =  '<skos:topConceptOf rdf:resource = "http://localhost:8080/opentheso-4.3.0/101"/>\n'
                f.write(s.encode('utf-8'))
            for alias_relation in Instrument_alias_relation:  # parcours de toutes les relations entre les instruments et les alias
                if alias_relation.instrument.id == instru.id:  # si l'id de l'instrument dans la relation entre les instrument et les alias correspond à l'id de l'instrument actuellement parcouru
                    s =  '           <skos:narrower rdf:resource = "http://localhost:8080/opentheso-4.3.0/A_' + str(alias_relation.instrument.id) + '"/>\n'
                    f.write(s.encode('utf-8'))

            s =  '           <dcterms:created rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
                + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '</dcterms:created>\n\
                                <dcterms:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
                + str(today.year) + '-' + str(today.month) + '-' + str(today.day) \
                + '</dcterms:modified>\n'
            f.write(s.encode('utf-8'))
            s = '</rdf:Description>\n'
            f.write(s.encode('utf-8'))
        for alias in Alias:  # parcours de toutes les valeurs de la table alias_instrument
            s = '<rdf:Description rdf:about="http://localhost:8080/opentheso-4.3.0/A_' + str(alias.id) + '">\n\
                                    <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>\n\
                                    <skos:prefLabel xml:lang="fr">' +unicodedata.normalize('NFD', alias.name).encode('ascii', 'ignore') + '</skos:prefLabel>\n\
                                    <skos:inScheme rdf:resource="http://localhost:8080/opentheso-4.3.0/101"/>\n'
            f.write(s.encode('utf-8'))
            for alias_relation in Instrument_alias_relation:  # parcours de toutes les relations entre les instruments et les alias
                if alias_relation.alias.id == alias.id:  # si l'id de l'alias dans la relation entre les instrument et les alias correspond à l'id de l'alias actuellement parcouru
                    s =  '           <skos:broader rdf:resource = "http://localhost:8080/opentheso-4.3.0/IM_' + \
                        str(alias_relation.instrument.id) + '"/>\n'
                    f.write(s.encode('utf-8'))

            s =  '           <dcterms:created rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
                + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '</dcterms:created>\n\
                                    <dcterms:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date">' \
                + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '</dcterms:modified>\n\
                                </rdf:Description>\n\
                                '
            f.write(s.encode('utf-8'))
        f.write('</rdf:RDF>')


# overture du fichier xml

    def export_instrument(self,request):
        self.skos()
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.
        xml = open("export/telemeta.xml", "r").read()

        c = RequestContext(request,{'result':xml})
        t = Template("{{result}}")

        return HttpResponse(xml, content_type='application/force-download')

