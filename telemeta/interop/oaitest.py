# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from oai import DataProvider
import cherrypy

class DataSource(object):
    def __init__(self):
        self.oldest = datetime(1988, 1, 1)

        self.data = {
            '10': ([('title', 'Roger Rabbit'), ('title', 'Roger Le Lapin'), ('creator', 'Bugs Bunny')], self.oldest),
            '20': ([('title', 'Pulp Fiction'), ('creator', 'Quentin Tarantino')], datetime(1994, 10, 14)),
            '30': ([('title', 'Children of Men'), ('creator', u'Alfonso Cuarón')], datetime(2006, 10, 18))
        }


    def get_earliest_time(self):
        return self.oldest

    def get_record(self, id):
        record = self.data.get(id)
        if record:
            dc = []
            dc[:] = record[0][:]
            dc.insert(0, ('identifier', id))
            record = (dc, record[1])
        return record

    def count_records(self, from_time = None, until_time = None):
        result = 0
        for k in self.data:
            dc, ctime = self.data[k]
            if ((not from_time) or ctime >= from_time) and ((not until_time) or ctime <= until_time):
                result += 1
                #result.push((k, ctime))
        return result

    def list_records(self, offset, limit, from_time = None, until_time = None):
        result = []
        i = 0
        n = 0
        for k in self.data:
            dc = []
            _dc, ctime = self.data[k]
            dc[:] = _dc[:]
            dc.insert(0, ('identifier', k))
            if ((not from_time) or ctime >= from_time) and ((not until_time) or ctime <= until_time):
                if (i >= offset) and (n < limit):
                    result.append((dc, ctime))
                    n += 1
                i += 1
        return result

class OAIServer:
    def __init__(self, provider):
        self.provider   = provider

    def index(self, **kwargs):
        return self.provider.handle(kwargs).encode('UTF-8')

    index.exposed = True

args = {}
runserver = False
for item in sys.argv[1:]:
    cut = item.split('=')
    if len(cut) == 1:
        if cut[0] == 'runserver':
            runserver = True
            host = None
            port = None
            break
        else:
            raise Exception("Please pass a value for argument %s" % cut[0])
    else:
        k, v = cut
        if k == 'runserver':
            runserver = True
            host, port = v.split(':')
            break
        else:
            args[k] = v

provider = DataProvider(DataSource(), "Test Provider", "http://test.provider.com", "joe@provider.com")
provider.max_records_per_response = 2

if runserver:
    if host:
        cherrypy.config.update({'server.socket_host': host})
    if port:
        cherrypy.config.update({'server.socket_port': int(port)})

    cherrypy.quickstart(OAIServer(provider))
else:
    sys.stdout.write(provider.handle(args).encode('UTF-8'))
