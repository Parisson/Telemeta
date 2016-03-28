# Telemeta OAI-PMH DataSource
#
# Copyright (C) 2009 Samalyse SARL
# Author: Olivier Guilyardi <olivier samalyse com>
#
# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from telemeta.models import MediaCollection, MediaItem, Revision, dublincore
from telemeta.interop.oai import BadArgumentError
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

    def prepare_record(self, record):
        ctime = record.get_revision().time
        return dublincore.express_resource(record).to_list(), ctime

    def get_record(self, id):
        """Return a specific record"""
        try:
            record = dublincore.lookup_resource(id)
        except dublincore.MalformedMediaIdentifier, e:
            raise BadArgumentError(e.message)
        return record and self.prepare_record(record)

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
                result.append(self.prepare_record(record))
            limit -= len(set)
            offset = 0
        else:
            offset -= nitems

        if limit > 0:
            query = MediaCollection.objects.by_change_time(from_time, until_time)
            set = query[offset:offset + limit]
            for record in set:
                result.append(self.prepare_record(record))
            
        return result
