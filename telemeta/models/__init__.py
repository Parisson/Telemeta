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
# Author: Olivier Guilyardi <olivier@samalyse.com>

from telemeta.models.crem import *
#MediaCollection, MediaItem, MediaPart,  Revision, \
#    PhysicalFormat, PublishingStatus

from django.db.models.signals import post_syncdb

def syncdb_callback(sender, **kwargs):
    from django.db import connection
    import _mysql_exceptions
    cursor = connection.cursor()
    print "Creating MySQL stored procedure"
    try:
        cursor.execute("DROP FUNCTION IF EXISTS telemeta_location_ascendant")
    except _mysql_exceptions.Warning:
        pass
    try:
        cursor.execute("""
        CREATE FUNCTION telemeta_location_ascendant(loc CHAR(150), asc_type CHAR(16))
          RETURNS CHAR(150) 
          READS SQL DATA 
          BEGIN 
            DECLARE t, n CHAR(150); 
            DECLARE c INT;
            SELECT COUNT(*) INTO c FROM locations WHERE name = loc;
            IF c = 0 THEN
              RETURN NULL;
            END IF;
            SELECT name, type INTO n, t FROM locations WHERE name = loc;
            WHILE t <> asc_type DO
              SELECT COUNT(*) INTO c FROM location_relations WHERE location_name = n;
              IF c = 0 THEN
                RETURN NULL;
              END IF;
              SELECT parent_location_name INTO n FROM location_relations WHERE location_name = n LIMIT 1;
              SELECT type INTO t FROM locations WHERE name = n;
            END WHILE;  
            RETURN n;
          END""")
    except _mysql_exceptions.Warning:
        pass

post_syncdb.connect(syncdb_callback)    
    

