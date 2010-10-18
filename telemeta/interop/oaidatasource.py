# Telemeta OAI-PMH DataSource
#
# Copyright (C) 2009 Samalyse SARL
# Author: Olivier Guilyardi <olivier samalyse com>
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
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
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
