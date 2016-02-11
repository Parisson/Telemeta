#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
#
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

import os
import sys
import time
from django.core.management import setup_environ

def print_usage(toolname):
    print "Usage: " + toolname + " <project_dir> <backup_dir>"
    print "  project_dir: the directory of the Django project which hosts Telemeta"
    print "  backup_dir: the destination backup folder (must exist)"

def write_readme(dest_dir, coll_num):
    readme = open(dest_dir + "/" + "README", "w")
    timestr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    readme.write("Telemeta Backup\n\n")
    readme.write("- date: " + timestr + "\n")
    readme.write("- number of collections: " + str(coll_num) + "\n\n")
    readme.close()

def backup(dest_dir):
    from telemeta.models import MediaCollection
    from telemeta.backup import CollectionSerializer

    collections = MediaCollection.objects.order_by('id')
    count = collections.count()

    print "Writing README file..",
    write_readme(dest_dir, count)
    print "Done."

    i = 0
    for collection in collections:
        if i % 100 == 0:
            set_dir = dest_dir + ("/collections-%d-%d" % (i+1, i+100))
            os.mkdir(set_dir)
        i += 1
        print "Processing collection %d/%d (%d%%) with id: %s.. " \
            % (i, count, i*100/count, collection.id),
        sys.stdout.flush()
        serializer = CollectionSerializer(collection)
        serializer.backup(set_dir)
        print "Done"

def run():
    if len(sys.argv) != 3:
        print_usage(os.path.basename(sys.argv[0]))
        sys.exit(1)
    else:
        project_dir = sys.argv[1]
        backup_dir = sys.argv[2]
        sys.path.append(project_dir)
        import settings
        setup_environ(settings)
        backup(backup_dir)

if __name__ == '__main__':
    run()
