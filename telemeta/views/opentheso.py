# coding=utf-8

from telemeta.views.core import *
import requests
import StringIO
import json
from lxml import etree,html


class OpenthesoView(object):
    opentheso = True
    termeSpe = []
    termeGen = []
    termeAsso = []
    termeSyn = []
    align = []
    terme = ""
    result = []
    recherche_by_id = False



    # @j
    #   json récupéré
    # retourne la valeur du label preferentiel
    def recherche_id(self, j):
        self.recherche_by_id = True
        t = ""
        if len(j) != 0:
            for i in j["@graph"]:
                try:
                    for tab in i["http://www.w3.org/2004/02/skos/core#prefLabel"]:
                        if tab["@language"] == "fr":
                            t = (tab["@value"])
                except:
                    t = (i["http://www.w3.org/2004/02/skos/core#prefLabel"]["@value"])
        else:
            t = "Id incorrect"
        return t
        # @recherche
        #   valeur de de la recherche
        # récupère les termes spécifiques

    def recherche_value(self, recherche):
        self.recherche_by_id = False
        t = []
        j = json.loads(requests.get(
            "http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/value=" + recherche + "&lang=fr&th=1", ).text.encode(
            'utf-8'))

        try:
            for i in j["@graph"]:  # parcoure du json recuperé
                try:
                    for t2 in i["http://www.w3.org/2004/02/skos/core#prefLabel"]:
                        if t2["@language"] == "fr":
                            d = {"id": i["@id"], "value": t2["@value"]}
                            t.append(d)
                except:  # si il y a un seul terme spécifique
                    d = {"id": i["@id"], "value": i["http://www.w3.org/2004/02/skos/core#prefLabel"]["@value"]}
                    t.append(d)
            return t

        except:

            return ["erreur recherche"]
            # @j
            #   json récupéré
            # récupère les termes spécifiques

    def getSpecifique(self, j):
        t = []
        try:
            for i in j["@graph"]:  # parcoure du json recuperé
                try:
                    for tab in i["http://www.w3.org/2004/02/skos/core#narrower"]:  # parcoure des termes spécifique

                        print i["http://www.w3.org/2004/02/skos/core#narrower"]
                        print tab
                        link = tab["@id"].split("=")[1].split('&')[0]
                        print link
                        # recupère le json du terme spécifique
                        j = json.loads(requests.get(
                            "http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/id=" +
                                link + "&th=1", ).text.encode(
                            'utf-8'))
                        print j
                        value = self.recherche_id(j)
                        d = {"link": link, "valeur": value}
                        t.append(d)
                except:
                    link = i["http://www.w3.org/2004/02/skos/core#narrower"]["@id"].split("=")[1].split('&')[0]
                    print link
                    j = json.loads(requests.get(
                        "http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/id=" + link + "&th=1", ).text.encode(
                        'utf-8'))
                    print j
                    value = self.recherche_id(j)
                    d = {"link": link, "valeur": value}
                    t.append(d)
        except:
            return ["aucun terme spécifique"]
        return t

    # @j
    #   json récupéré
    # récupère les termes synonymme
    #-------------------------------------------------------------------
    # -------------------------------------------------------------------
    # ----------------------------A TESTER-------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------

    def getSynonme(self, j):
        t = []
        try:
            for i in j["@graph"]:  # parcoure du json recuperé
                    for tab in i["http://www.w3.org/2004/02/skos/core#altLabel"]:  # parcoure des termes synonyme
                        if tab["@language"] == "fr":
                            t.append(tab["@value"])
        except:
            return ["aucun synonyme"]
        return t

    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------

    # @j
    #   json récupéré
    #
    def getGenerique(self, j):
        t = []
        try:
            for i in j["@graph"]:  # parcoure du json recuperé
                try:
                    for tab in i["http://www.w3.org/2004/02/skos/core#broader"]:  # parcoure des termes génériques
                        link = tab["@id"].split("=")[1].split('&')[0]
                        j = json.loads(requests.get(
                            "http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/id="+link + "&th=1", ).text.encode('utf-8'))
                        value = self.recherche_id(j)
                        d = {"link": link, "valeur": value}
                        t.append(d)
                except:  # parcoure des termes génériques

                    link = i["http://www.w3.org/2004/02/skos/core#broader"]["@id"].split("=")[1].split('&')[0]

                    j = json.loads(requests.get("http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/id=" +link + "&th=1", ).text.encode('utf-8'))
                    print j
                    value = self.recherche_id(j)
                    d = {"link": link, "valeur": value}
                    t.append(d)
        except:
            return ["aucun terme generique"]
        return t

    # @j
    #   json récupéré
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # ----------------------------A TESTER-------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    def getAsso(self, j):
        t = []
        try:
            for i in j["@graph"]:  # parcoure du json recuperé

                try:
                    for tab in i["http://www.w3.org/2004/02/skos/core#related"]:  # parcour de terme associé du json
                        link = tab["@id"].split("=")[1].split('&')[0]
                        # recupère le json du terme associé
                        j = json.loads(requests.get(
                            "http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/id=" + self.get_id(
                                link) + "&th=1", )
                                       .text.encode('utf-8'))
                        value = self.recherche_id(j)
                        # liaison entre le lien du terme associé et ça valeur
                        d = {"link": link, "valeur": value}
                        t.append(d)
                except:  # parcoure des termes associés
                    link = i["http://www.w3.org/2004/02/skos/core#related"]["@id"].split("=")[1].split('&')[0]
                    j = json.loads(requests.get(
                        "http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/id=" +
                            link + "&th=1", )
                                   .text.encode('utf-8'))
                    value = self.recherche_id(j)
                    d = {"link": link, "valeur": value}
                    t.append(d)
        except:
            return ["aucun terme generique"]

        return t
        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
    # @j
    #   json récupéré
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # ----------------------------A TESTER-------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    def getAlign(self, j):
        t = []
        try:
            for i in j["@graph"]:  # parcoure du json recuperé
                try:
                    for tab in i["http://www.w3.org/2004/02/skos/core#closeMatch"]:  # parcour des alignements du json
                        link = tab["@id"]
                        t.append(link)
                except:  # si il n'y a qu'un seul alignement
                    link = i["http://www.w3.org/2004/02/skos/core#closeMatch"]["@id"]

                    t.append(link)
        except:  # si il n'y a pas d'alignement
            return ["aucun alignement"]

        return t
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    def opentheso(self, request):
        """Render the index page"""
        recherche = request.GET.get('name', '')
        identifiant = request.GET.get('id', '0')
        print "recherche"+recherche
        print "identifiant" + identifiant
        if recherche == "":  # si la recherche par valeur est vide
            if identifiant != "0":  # si la recherche par id n'est pas vide
                j = json.loads(requests.get(
                    "http://172.18.3.4:8080/opentheso-4.3.0/webresources/rest/jsonld/concept/id=IM_" + identifiant + "&th=1", ).text.encode(
                    'utf-8'))  #  recuperation et parsing du json
                print len(j)
                self.opentheso = True
                self.terme = self.recherche_id(j)
                self.termeSpe = self.getSpecifique(j)
                self.termeSyn = self.getSynonme(j)
                self.termeGen = self.getGenerique(j)
                self.termeAsso = self.getAsso(j)
                self.align = self.getAlign(j)
            else:
                self.opentheso = False
        else:
            self.opentheso = True
            self.result = self.recherche_value(recherche)

        template = loader.get_template('telemeta/opentheso.html')

        context = RequestContext(request, {
            'page_content': pages.get_page_content(request,
                                                   'opentheso', ignore_slash_issue=True),
            'terme': self.terme,
            'opentheso': self.opentheso,
            'termeSpe': self.termeSpe,
            'termeGen': self.termeGen,
            'termeAsso': self.termeAsso,
            'termeSyn': self.termeSyn,
            'align': self.align,
            'result': self.result,
            'recherche_by_id': self.recherche_by_id,
        })
        return HttpResponse(template.render(context))