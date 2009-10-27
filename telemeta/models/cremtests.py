# -*- coding: utf-8 -*-

import unittest
from models import MediaCollection, MediaItem, Location, EthnicGroup, LocationType
from datetime import datetime, timedelta

class CollectionItemTestCase(unittest.TestCase):
    def setUp(self):
        "Create a test database based on objects created in Django"

        LocationType.objects.all().delete()
        self.country = LocationType.objects.create(id="country", name="country")
        self.continent = LocationType.objects.create(id="continent", name="continent")
        self.city = LocationType.objects.create(id="city", name="city")

        Location.objects.all().delete()        
        self.paris = Location.objects.create(name="Paris", type="other", complete_type=self.city, is_authoritative=0)
        self.france = Location.objects.create(name="France", type="country", complete_type=self.country, is_authoritative=0)
        self.europe = Location.objects.create(name="Europe", type="continent", complete_type=self.continent, is_authoritative=0)
        self.belgique = Location.objects.create(name="Belgique", type="country", complete_type=self.country, is_authoritative=0)

        EthnicGroup.objects.all().delete()
        self.a = EthnicGroup.objects.create(name="a")
        self.b = EthnicGroup.objects.create(name="b")
        self.c = EthnicGroup.objects.create(name="c")
        self.d = EthnicGroup.objects.create(name="d")

        MediaCollection.objects.all().delete()
        self.persepolis = MediaCollection.objects.create(id=1, reference="A1", physical_format_id=1111, old_code="10", code="100",                                                          title="persepolis", alt_title="bjr", creator="Abraham LINCOLN", 
                                                         booklet_author="Maria BALTHAZAR", 
                                                         booklet_description="compilation de mots français", 
                                                         collector="Friedrich HEINZ", collector_is_creator=0, publisher_id=1442, 
                                                         year_published=2009, publisher_collection_id=1234, 
                                                         publisher_serial="123456", external_references="Larousse", 
                                                         acquisition_mode_id=1, comment="chants", metadata_author_id=1, 
                                                         metadata_writer_id=1, legal_rights_id=1, alt_ids="89", 
                                                         recorded_from_year=1970, recorded_to_year=1980, recording_context_id=1, 
                                                         approx_duration="5:00:00", doctype_code=1357, travail="travail", 
                                                         state="etat", cnrs_contributor="Jean PETIT", items_done="fiches", 
                                                         a_informer_07_03="a informer", ad_conversion_id=9, public_access="full")

        self.volonte = MediaCollection.objects.create(id=2, reference="A2", physical_format_id=222, old_code="20", code="200", 
                                                      title="Volonté de puissance", alt_title="ar", creator="Friedrich NIETZSCHE", 
                                                      booklet_author="George POMPIDOU", booklet_description="notice numero 2", 
                                                      collector="Jean AMORA", collector_is_creator=0, publisher_id=2884, 
                                                      year_published=1999, publisher_collection_id=2345, 
                                                      publisher_serial="234567", external_references="dico", 
                                                      acquisition_mode_id=2, comment="commentaire 2", metadata_author_id=2, 
                                                      metadata_writer_id=2, legal_rights_id=2, alt_ids="78", 
                                                      recorded_from_year=1960, recorded_to_year=2000, recording_context_id=2, 
                                                      approx_duration="1:00:00", doctype_code=2468, travail="travail 2", 
                                                      state="etat 2", cnrs_contributor="Richard LIONHEART", items_done="fiches 2", 
                                                      a_informer_07_03="a informer 2", ad_conversion_id=8, 
                                                      public_access="metadata")

        self.nicolas = MediaCollection.objects.create(id=3, reference="A3", physical_format_id=333, old_code="30", code="300", 
                                                      title="petit nicolas", alt_title="slt", creator="Georgette McKenic", 
                                                      booklet_author="Francesca DICORTO", booklet_description="notice 3", 
                                                      collector="Paul MAILLE", collector_is_creator=0, publisher_id=3773, 
                                                      year_published=1999, publisher_collection_id=7890, publisher_serial="8764", 
                                                      external_references="ref externes", acquisition_mode_id=3, 
                                                      comment="commentaire 3", metadata_author_id=3, metadata_writer_id=3, 
                                                      legal_rights_id=3, alt_ids="56", recorded_from_year=1967, 
                                                      recorded_to_year=1968, recording_context_id=3, approx_duration="0:00:00", 
                                                      doctype_code=5790, travail="travail 3", state="etat 3", 
                                                      cnrs_contributor="Gerard MICKAEL", items_done="fiches 3", 
                                                      a_informer_07_03="a informer 3", ad_conversion_id=8, public_access="none")
                                        
        MediaItem.objects.all().delete()        
        self.item_1 = MediaItem.objects.create(id=1, collection=self.persepolis, track="1111", old_code="101", code="1010", 
                                               approx_duration="00:01:00", recorded_from_date="1971-01-12", 
                                               recorded_to_date="1971-02-24", location_name=self.paris, 
                                               location_comment="capital de la France", ethnic_group=self.a, 
                                               title="item 1", alt_title="I1", author="Mickael SHEPHERD", 
                                               context_comment="contexte ethno 1", external_references="ext ref 1", 
                                               moda_execut="moda exec 1",copied_from_item_id=99, 
                                               collector="Charles PREMIER", cultural_area="Ile de France", generic_style_id=1, 
                                               collector_selection="collec sel 1", creator_reference="ref du deposant 1", 
                                               comment="comment 1", filename="item 1.item", public_access="full") 

        self.item_2 = MediaItem.objects.create(id=2, collection=self.volonte, track="2222", old_code="202", code="2020", 
                                               approx_duration="00:02:00", recorded_from_date="1981-01-12", 
                                               recorded_to_date="1991-02-24", location_name=self.france, 
                                               location_comment="loc comment 2", ethnic_group=self.a, title="item 2",                                                             alt_title="I2", author="Rick ROLL", context_comment="contexte ethno 2", 
                                               external_references="ext ref 2", moda_execut="moda exec 2", 
                                               copied_from_item_id=98, collector="Gerard LENORMAND", 
                                               cultural_area="Nord de la France", generic_style_id=1,
                                               collector_selection="collec sel 2", creator_reference="ref du deposant 2", 
                                               comment="comment 2", filename="item 2.item", public_access="metadata") 

        self.item_3 = MediaItem.objects.create(id=3, collection=self.nicolas, track="3333", old_code="303", code="3030", 
                                               approx_duration="00:03:00", recorded_from_date="1968-01-12", 
                                               recorded_to_date="1968-02-24", location_name=self.belgique, 
                                               location_comment="en Europe", ethnic_group=self.b, title="item 3", 
                                               alt_title="I3", author="John SMITH", context_comment="contexte ethno 3", 
                                               external_references="ext ref 3", moda_execut="moda exec 3", copied_from_item_id=97, 
                                               collector="Paul CARLOS", cultural_area="Europe occidentale", generic_style_id=1,
                                               collector_selection="collec sel 3", creator_reference="ref du deposant 3", 
                                               comment="comment 3", filename="item 3.item", public_access="none")

        self.item_4 = MediaItem.objects.create(id=4, collection=self.persepolis, track="4444", old_code="404", code="4040", 
                                               approx_duration="00:04:00", recorded_from_date="1972-01-12", 
                                               recorded_to_date="1972-02-24", location_name=self.europe, 
                                               location_comment="loc comm 4", ethnic_group=self.a, title="item 4", 
                                               alt_title="I4", author="Keanu REAVES", context_comment="contexte ethno 4", 
                                               external_references="ext ref 4", moda_execut="moda exec 4", copied_from_item_id=96, 
                                               collector="Christina BARCELONA", cultural_area="aire culturelle 4", 
                                               generic_style_id=1, collector_selection="collec sel 4", 
                                               creator_reference="ref du deposant 4", comment="comment 4", filename="item 4.item",
                                               public_access="none")

        self.item_5 = MediaItem.objects.create(id=5, collection=self.volonte, track="5555", old_code="505", code="5050", 
                                               approx_duration="00:05:00", recorded_from_date="1978-01-12", 
                                               recorded_to_date="1978-02-24", location_name=self.belgique, 
                                               location_comment="loc comm 5", ethnic_group=self.a, title="item 5", 
                                               alt_title="I5", author="Simon PAUL", context_comment="contexte ethno 5", 
                                               external_references="ext ref 5", moda_execut="moda exec 5", copied_from_item_id=95, 
                                               collector="Javier BARDEM", cultural_area="aire culturelle 5", generic_style_id=1,
                                               collector_selection="collec sel 5", creator_reference="ref du deposant 5", 
                                               comment="comment 5", filename="item 5.item", public_access="metadata")

        self.item_6 = MediaItem.objects.create(id=6, collection=self.persepolis, track="10000", old_code="1111111", 
                                               code="6060", approx_duration="10:03:00", recorded_from_date="1968-01-12", 
                                               recorded_to_date="1968-02-11", location_name=self.france, 
                                               location_comment="loc comment 10000", ethnic_group=self.b, 
                                               title="item 6", alt_title="I10000", author="Paul ANDERSON", 
                                               context_comment="contexte ethno 10000", external_references="ext ref 10000", 
                                               moda_execut="moda exec 10000", copied_from_item_id=11111, collector="Jim CARLSON", 
                                               cultural_area="cul area 10000", generic_style_id=1, 
                                               collector_selection="collec sel 10000", creator_reference="ref du deposant 10000", 
                                               comment="comment 10000", filename="item 10000.item", public_access="none")

        self.collections = MediaCollection.objects.all()
        self.items       = MediaItem.objects.all()

    def testQuickSearchOnCollections(self):
        "Test quick_search property of MediaCollection class"
        result = self.collections.quick_search("persepolis")
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0], self.persepolis)
        self.assertEquals(self.collections.quick_search("nietzsche")[0], self.volonte)
        result = self.collections.quick_search("nicolas")
        self.assertEquals(result[0], self.nicolas)

    def testQuickSearchOnItems(self):
        "Test quick_search property of MediaItem class"
        result = self.items.quick_search("item").order_by("title")
        self.assertEquals(result[0], self.item_1)
        self.assertEquals(result[1], self.item_2)
        self.assertEquals(result[2], self.item_3)
        self.assertEquals(result[3], self.item_4)
        self.assertEquals(result[4], self.item_5)
        self.assertEquals(result[5], self.item_6)

    def testWordSearch(self):
        "Test quick_search property of MediaCollection class, specificly quick_search on collection title"
        result = self.collections.quick_search("volonté puissance")
        self.assertEquals(result[0], self.volonte)
        result = self.collections.quick_search("puissance volonté")
        self.assertEquals(result[0], self.volonte)
        result = self.collections.quick_search("volonte puissance")
        self.assertEquals(result[0], self.volonte)
        result = self.collections.quick_search("puissance volonte")
        self.assertEquals(result[0], self.volonte)
        
    def testLocationSearch(self):
        "Test by_country and by_continent properties of MediaCollection class"
        self.assertEquals(self.collections.by_country("France")[0], self.persepolis)
        self.assertEquals(self.collections.by_continent("Europe")[0], self.persepolis)
        self.assertEquals(self.collections.by_country("Belgique").order_by("title")[0], self.nicolas)
        self.assertEquals(self.collections.by_country("Belgique").order_by("title")[1], self.volonte)

    def testRecordingYear(self): 
        "Test by_recording_year property of MediaCollection class"
        self.assertEquals(self.collections.by_recording_year(1970, 1980)[0], self.persepolis)
        result = self.collections.by_recording_year(1975).order_by("title")
        self.assertEquals(result[0], self.persepolis)
        self.assertEquals(result[1], self.volonte)
    
    def testPublishYearOnCollection(self):
        "Test by_publish_year property of MediaCollection class"
        result=self.collections.by_publish_year(1999).order_by("title")
        self.assertEquals(result[0], self.nicolas)
        self.assertEquals(result[1], self.volonte)
        
    def testEthnicGroup(self):
        "Test by_ethnic_group property of MediaCollection class"
        result=self.collections.by_ethnic_group("a").order_by("title")
        self.assertEquals(result[0], self.persepolis)
        self.assertEquals(result[1], self.volonte)

    def testRecordingDate(self):
        "Test by_recording_date property of MediaItem class"
        result = self.items.by_recording_date("1968-01-01", "1972-12-12").order_by("title")
        self.assertEquals(result[0], self.item_1)
        self.assertEquals(result[1], self.item_3)
        self.assertEquals(result[2], self.item_4)
        self.assertEquals(result[3], self.item_6)
        result = self.items.by_recording_date("1968-02-06").order_by("title")
        self.assertEquals(result[0], self.item_3)
        self.assertEquals(result[1], self.item_6)

    def testTitle(self):
        "Test by_title property of MediaItem class"
        result = self.items.by_title("item").order_by("title")
        self.assertEquals(result[0], self.item_1)
        self.assertEquals(result[1], self.item_2)
        self.assertEquals(result[2], self.item_3)
        self.assertEquals(result[3], self.item_4)
        self.assertEquals(result[4], self.item_5)
        self.assertEquals(result[5], self.item_6)
        result = self.items.by_title("volonté").order_by("title")
        self.assertEquals(result[0], self.item_2)
        self.assertEquals(result[1], self.item_5)
        result = self.items.by_title("puissance volonté").order_by("title")
        self.assertEquals(result[0], self.item_2)
        self.assertEquals(result[1], self.item_5)

    def testPublishYearOnItem(self):
        "Test by_publish_year property of MediaItem class"
        result = self.items.by_publish_year(1999).order_by("title")
        self.assertEquals(result[0], self.item_2)
        self.assertEquals(result[1], self.item_3)
        self.assertEquals(result[2], self.item_5)
    
    def testWordSearchCore(self):
        "Test word_search property of CoreQuerySet class"
        self.assertEquals(self.collections.word_search("title", "volonté")[0], self.volonte)
        self.assertEquals(self.collections.word_search("code", "100")[0], self.persepolis)
        self.assertEquals(self.items.word_search("code", "1010")[0], self.item_1)
        result = self.items.word_search("comment", "comment").order_by("title")
        self.assertEquals(result[0], self.item_1)
        self.assertEquals(result[1], self.item_2)
        self.assertEquals(result[2], self.item_3)
        self.assertEquals(result[3], self.item_4)
        self.assertEquals(result[4], self.item_5)
        self.assertEquals(result[5], self.item_6)
    
    def testByChangeTimeOnCollection(self):
        "Test by_change_time property of MediaCollection class"
        now = datetime.now()
        result = self.collections.by_change_time(now - timedelta(hours=1), now).order_by("title")
        self.assertEquals(result[0], self.persepolis)

    def testByChangeTimeOnItem(self):
        "Test by_change_time property of MediaItem class"
        now = datetime.now()
        result = self.items.by_change_time(now - timedelta(hours=1), now).order_by("title")
        self.assertEquals(result[0], self.item_1)
