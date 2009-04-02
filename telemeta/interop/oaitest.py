# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from oai import DataProvider

class DataSource(object):
    def __init__(self):
        self.oldest = datetime(1988, 1, 1)

        self.data = {
            '10': ({'title': 'Roger Rabbit', 'author': 'Bugs Bunny'}, self.oldest),
            '20': ({'title': 'Pulp Fiction', 'author': 'Quentin Tarantino'}, datetime(1994, 10, 14)),
            '30': ({'title': 'Children of Men', 'author': u'Alfonso Cuarón'}, datetime(2006, 10, 18))
        }


    def get_earliest_time(self):
        return self.oldest

    def get_record(self, id):
        return self.data.get(id)

args = {}
for item in sys.argv[1:]:
    k, v = item.split('=')
    args[k] = v

datasource = DataSource()
provider = DataProvider("Test Provider", "http://test.provider.com", "joe@provider.com")
print provider.handle(args, datasource)
