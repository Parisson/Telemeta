#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Samalyse SARL

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
