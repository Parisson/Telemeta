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

    def count_records(self, from_time = None, until_time = None):        
        result = 0
        for k in self.data:
            dc, ctime = self.data[k]
            if ((not from_time) or ctime >= from_time) and ((not until_time) or ctime <= until_time):
                result += 1
                #result.push((k, ctime))
        return result
                
    def list_identifiers(self, offset, limit, from_time = None, until_time = None):        
        result = []
        i = 0
        n = 0
        for k in self.data:
            dc, ctime = self.data[k]
            if ((not from_time) or ctime >= from_time) and ((not until_time) or ctime <= until_time):
                if (i >= offset) and (n < limit):
                    result.append((k, ctime))
                    n += 1
                i += 1
        return result

args = {}
for item in sys.argv[1:]:
    k, v = item.split('=')
    args[k] = v

datasource = DataSource()
provider = DataProvider("Test Provider", "http://test.provider.com", "joe@provider.com")
provider.max_records_per_response = 2
print provider.handle(args, datasource)
