# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          David LIPSZYC <davidlipszyc@gmail.com>

import unittest
from telemeta.models import *
from datetime import datetime, timedelta

class CollectionItemTestCase(unittest.TestCase):
    def setUp(self):
        "Create a test database based on objects created in Django"
   
        User.objects.all().delete() 
        self.david   = User.objects.create(username="david", level="user")
        self.olivier = User.objects.create(username="olivier", level="admin")    

        LocationType.objects.all().delete()
        self.country = LocationType.objects.create(id="country", name="Country")
        self.continent = LocationType.objects.create(id="continent", name="Continent")
        self.city = LocationType.objects.create(id="city", name="City")

        Location.objects.all().delete()        
        self.paris = Location.objects.create(name="Paris", type="other", complete_type=self.city)
        self.france = Location.objects.create(name="France", type="country", complete_type=self.country)
        self.europe = Location.objects.create(name="Europe", type="continent", complete_type=self.continent)
        self.belgique = Location.objects.create(name="Belgique", type="country", complete_type=self.country)

        LocationRelation.objects.create(location=self.paris, parent_location=self.france)
        LocationRelation.objects.create(location=self.france, parent_location=self.europe)

        EthnicGroup.objects.all().delete()
        self.a = EthnicGroup.objects.create(name="a")
        self.b = EthnicGroup.objects.create(name="b")
        self.c = EthnicGroup.objects.create(name="c")
        self.d = EthnicGroup.objects.create(name="d")

        MediaCollection.objects.all().delete()
        self.persepolis = MediaCollection(id=1, code="100", reference="A1", title="persepolis", 
            creator="Abraham LINCOLN", collector="Friedrich HEINZ", year_published=2009,  
            recorded_from_year=1970, recorded_to_year=1980)
        
        self.persepolis.save_by_user(self.david)

        self.volonte = MediaCollection(id=2, reference="A2",  code="200", title="Volonté de puissance", 
            creator="Friedrich NIETZSCHE", collector="Jean AMORA", year_published=1999,  
            recorded_from_year=1960, recorded_to_year=2000)

        self.volonte.save_by_user(self.olivier)

        self.nicolas = MediaCollection(id=3, reference="A3",  code="300", title="petit nicolas", 
            creator="Georgette McKenic", collector="Paul MAILLE",  year_published=1999,  
            recorded_from_year=1967, recorded_to_year=1968)
                                   
        self.nicolas.save_by_user(self.olivier)
     
        MediaItem.objects.all().delete()        
        self.item_1 = MediaItem(id=1, collection=self.persepolis, code="1010", 
            recorded_from_date="1971-01-12", recorded_to_date="1971-02-24", location=self.paris, 
            ethnic_group=self.a, title="item 1", author="Mickael SHEPHERD", collector="Charles PREMIER",  
            comment="comment 1") 

        self.item_1.save_by_user(self.david)

        self.item_2 = MediaItem(id=2, collection=self.volonte, code="2020", 
            recorded_from_date="1981-01-12", recorded_to_date="1991-02-24", location=self.france, 
            ethnic_group=self.a, title="item 2", author="Rick ROLL", comment="comment 2") 

        self.item_2.save_by_user(self.david)

        self.item_3 = MediaItem(id=3, collection=self.nicolas, code="3030", 
            recorded_from_date="1968-01-12", recorded_to_date="1968-02-24", location=self.belgique, 
            ethnic_group=self.b, title="item 3", author="John SMITH", collector="Paul CARLOS",
            comment="comment 3",  )

        self.item_3.save_by_user(self.olivier)

        self.item_4 = MediaItem(id=4, collection=self.persepolis, code="4040", 
            recorded_from_date="1972-01-12", recorded_to_date="1972-02-24", location=self.europe, 
            ethnic_group=self.a, title="item 4", alt_title="I4", author="Keanu REAVES", 
            collector="Christina BARCELONA", comment="comment 4")

        self.item_4.save_by_user(self.olivier)

        self.item_5 = MediaItem(id=5, collection=self.volonte,code="5050", 
            approx_duration="00:05:00", recorded_from_date="1978-01-12", recorded_to_date="1978-02-24", 
            location=self.belgique, ethnic_group=self.a, title="item 5", alt_title="I5", 
            author="Simon PAUL", collector="Javier BARDEM", 
            comment="comment 5")

        self.item_5.save_by_user(self.olivier)

        self.item_6 = MediaItem(id=6, collection=self.persepolis, code="6060", 
            recorded_from_date="1968-01-12", recorded_to_date="1968-02-11", location=self.france, 
            ethnic_group=self.b, title="item 6", author="Paul ANDERSON", 
            collector="Jim CARLSON", comment="comment 10000")
        
        self.item_6.save_by_user(self.david)

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

    def testWithoutCollection(self):
        "Test without_collection property of MediaItem class"
        self.assertEquals(self.items.without_collection().count(), 0)

    def testCodeRequired(self):
        "Test that a proper failure occur when a collection code isn't provided"
        c = MediaCollection()
        try:
            c.save_by_user(self.olivier)
        except RequiredFieldError, e:
            self.assertEquals(e.field.name, 'code')
        else:
            self.fail("No exception raised")
       
    def testDomForeignKey(self):
        "Test DOM foreign key embedding"
        doc = self.item_4.to_dom()
        self.assertEquals(doc.getElementsByTagName('collection')[0].getAttribute('key'), str(self.persepolis.id))

    def testLocationRelation(self):
        "Test location country and continent resolving"
        self.assertEquals(self.france, self.item_1.location.country())
        self.assertEquals(self.europe, self.item_1.location.continent())
        self.assertEquals(self.france, self.item_2.location.country())
        self.assertEquals(self.europe, self.item_2.location.continent())

    def testCollectionCountries(self):
        "Test the MediaCollection.get_countries() method"
        self.assertEquals(self.volonte.get_countries(), [self.belgique, self.france])

