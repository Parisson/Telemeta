#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright Guillaume Pellerin (2006-2009)
# <yomguy@parisson.com>

# This software is a computer program whose purpose is to backup
# any audio content in a Telemeta instance

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


import os
import sys
import shutil
import datetime
import string
from django.core.management import setup_environ
from django.core.files import File

tool_name = "media_import.py"
authorized_extensions = ['wav', 'aif', 'aiff', 'mp3', 'ogg', 'flac']
print map(string.swapcase, authorized_extensions)

class TelemetaMediaImportError(Exception):
    pass

class TelemetaMediaImport:

    def __init__(self, settings, source_dir):
        self.source_dir = source_dir
        self.source_files = os.listdir(self.source_dir)
        self.media_filter()
        print self.source_files
        self.item_media_root_dir = settings.MEDIA_ROOT
        self.item_media_full_dir = self.item_media_root_dir + os.sep + 'items'
        self.collection_id = self.get_collection()

    def media_filter(self):
        files = []
        for media_file in self.source_files:
            ext = get_media_extension(media_file)
            if ext in authorized_extensions or \
                ext in map(string.swapcase, authorized_extensions) or \
                ext in map(string.capitalize, authorized_extensions) :
                files.append(media_file)
        self.source_files = files

    def get_collection(self):
        from telemeta.models import MediaItem
        file_0 = self.source_files[0]
        id_string = get_media_name(file_0)
        self.item_list = MediaItem.objects.filter(id__startswith=id_string)
        return self.item_list[0].collection_id

    def media_import(self):
        from telemeta.models import MediaItem
        id_list = map(get_media_name, self.source_files)

        print "Working on collection_id : " + self.collection_id
        for item_id in id_list:
            print "item_id : " + item_id
            it = MediaItem.objects.get(id=item_id)
            source_full_path = self.source_dir + os.sep + get_item_in_list(self.source_files, item_id)
            if os.path.exists(source_full_path):
                media = open(source_full_path, 'r')
                f = File(media)
                print "Adding : " + source_full_path
                try:
                    it.file.save(f.name, f, save=True)
                except:
                    raise TelemetaMediaImportError("Could not include this item: " + item_id)
                media.close()

    def main(self):
        self.media_import()

def get_media_name(media):
    name = media.split('.')[:-1]
    return '.'.join(name)

def get_media_extension(media):
    ext = media.split('.')[-1]
    return ext

def get_item_in_list(item_list, string):
    for item in item_list:
        if string in item:
            return item

def print_usage():
    print """
 Usage: %s <project_dir> <source_dir> [<source_file>]

 project_dir: the directory of the Django project which hosts Telemeta
 source_dir: the directory containing all media files to include

 IMPORTANT: each file name without its extension has to correspond at least to one existing item id in the database. All media files have also to correspond to only one Collection."
 """ % tool_name

def run():
    l = len(sys.argv)
    if l < 2:
        print_usage()
        sys.exit(1)
    else:
        project_dir = sys.argv[1]
        source_dir = sys.argv[2]
        sys.path.append(project_dir)
        #from django.conf import settings
        import settings
        setup_environ(settings)
        t = TelemetaMediaImport(settings, source_dir)
        t.main()

if __name__ == '__main__':
    run()
