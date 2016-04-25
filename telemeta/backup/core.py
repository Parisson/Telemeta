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
from xml.dom.minidom import getDOMImplementation, Node
import shutil
import md5
from django.conf import settings
from telemeta.models import MediaItem


class CollectionSerializer(object):
    """Provide backup-related features"""

    def __init__(self, collection, dest_dir='/tmp/'):
        self.collection = collection

    def __get_file_md5(self, path):
        "Compute the MD5 hash of a file (Python version of md5sum)"
        file = open(path, "rb")
        hash = md5.new()
        while True:
            buffer = file.read(0x10000)
            if len(buffer) == 0:
                break
            hash.update(buffer)
        file.close()
        return hash.hexdigest()

    def __get_media_filename(self, item):
        return str(item.id) + ".wav"

    def backup(self, dest_dir):
        self.coll_dir = dest_dir + "/" + str(self.collection.id)
        if not os.path.exists(self.coll_dir):
            os.makedirs(self.coll_dir)
        self.store_json()
        self.store_xml()
        self.store_files()

    def store_files(self):
        if self.collection.has_mediafile():
            md5_file = open(self.coll_dir + "/MD5SUM", "wb")

            items = self.collection.items.all()
            for item in items:
                if item.file:
                    dst_basename = self.__get_media_filename(item)
                    dst = self.coll_dir + "/" + dst_basename
                    shutil.copyfile(item.file.path, dst)
                    hash = self.__get_file_md5(dst)
                    md5_file.write(hash + "  " + dst_basename + "\n")

            md5_file.close()

    def store_json(self, dest_dir):
        """Serialize and store the collection with related items and media
        files into a subdirectory of the provided directory
        """
        json = self.collection.get_json()
        file = open(self.coll_dir + "/collection.json", "wb")
        file.write(json)
        file.close()
        self.store_files()

    def store_xml(self, dest_dir):
        """Serialize and store the collection with related items and media
        files into a subdirectory of the provided directory
        """
        xml = self.get_xml()
        file = open(self.coll_dir + "/collection.xml", "wb")
        file.write(xml.encode("utf-8"))
        file.close()
        self.store_files()

    def get_xml(self):
        """Return a string containing the XML representation of the collection
        and related items
        """
        impl = getDOMImplementation()
        doc = impl.createDocument(None, "telemeta", None)
        coll_doc = self.collection.to_dom()
        coll_node = doc.documentElement.appendChild(coll_doc.documentElement)
        coll_doc.unlink()
        items_node_name = MediaItem.get_dom_name() + "List"
        items_node = doc.createElement(items_node_name)
        coll_node.appendChild(items_node)

        items = self.collection.items.all()
        for item in items:
            if item.file:
                item.file = self.__get_media_filename(item)
            item_doc = item.to_dom()
            items_node.appendChild(item_doc.documentElement)
            item_doc.unlink()
        doc.normalize()

        return doc.toxml()


