from telemeta.models import MediaCollection, MediaItem, Revision
from datetime import datetime

class TelemetaOAIDataSource(object):
    """Telemeta OAI datasource adapter. This class implements the oai.IDataSource interface."""

    def get_earliest_time(self):
        """Return the change time of the oldest record(s) as a datetime object"""
        try:
            rev = Revision.objects.order_by('time')[0]
            return rev.time
        except IndexError:
            return datetime.now()

    def prepare_record(self, type, record):
        ctime = record.get_revision().time
        dc = []
        _dc = record.to_dublincore().to_list()
        for k, v in _dc:
            if k == 'identifier':
                dc.append((k, type + ':' + v))
            else:
                dc.append((k, v))
        return (dc, ctime)

    def get_record(self, id):
        """Return a specific record"""
        type, id = id.split(':')
        if (type == 'collection'):
            record  = MediaCollection.objects.get(id=id)
        elif (type == 'item'):
            record = MediaItem.objects.get(id=id)
        else:
            raise Exception("No such record type: %s" % type)

        return self.prepare_record(type, record)


    def count_records(self, from_time = None, until_time = None):
        """Must return the number of records between (optional) from and until change time."""
        nitems = MediaItem.objects.by_change_time(from_time, until_time).count()
        ncolls = MediaCollection.objects.by_change_time(from_time, until_time).count()
        return nitems + ncolls

    def list_records(self, offset, limit, from_time = None, until_time = None):
        """Return a list of records"""

        result = []

        query = MediaItem.objects.by_change_time(from_time, until_time)
        nitems = query.count()
        if (offset < nitems):
            set = query[offset:offset + limit]
            for record in set:
                result.append(self.prepare_record('item', record))
            limit -= len(set)
            offset = 0
        else:
            offset -= nitems

        if limit > 0:
            query = MediaCollection.objects.by_change_time(from_time, until_time)
            set = query[offset:offset + limit]
            for record in set:
                result.append(self.prepare_record('collection', record))
            
        return result
