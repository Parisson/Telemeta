# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

import os
import libxml2
from xml.dom import getDOMImplementation, Node
import shutil
import md5
from django.conf import settings
from telemeta.models import MediaItem

class BackupBuilder(object):
    """Provide backup-related features"""

    def __get_file_md5(self, path):
        "Compute the MD5 hash of a file (Python version of md5sum)"
        file = open(path, "rb")
        hash = md5.new()
        while True:
            buffer = file.read(0x100000)
            if len(buffer) == 0:
                break
            hash.update(buffer)

        file.close()            
        return hash.hexdigest()

    def __get_media_filename(self, item):
        return item.id + ".wav"

    def store_collection(self, collection, dest_dir):
        """Serialize and store a collection with related items and media 
        files into a subdirectory of the provided directory
        """
        coll_dir = dest_dir + "/" + collection.id
        os.mkdir(coll_dir)

        xml = self.collection_to_xml(collection)
        file = open(coll_dir + "/collection.xml", "wb")
        file.write(xml.encode("utf-8"))
        file.close()

        if collection.has_mediafile():
            md5_file = open(coll_dir + "/MD5SUM", "wb")

            items = collection.items.all()
            for item in items:
                if item.file:
                    dst_basename = self.__get_media_filename(item)
                    dst = coll_dir + "/" + dst_basename
                    shutil.copyfile(settings.MEDIA_ROOT + "/" + item.file, dst)
                    hash = self.__get_file_md5(dst)
                    md5_file.write(hash + "  " + dst_basename + "\n")

            md5_file.close()

    def collection_to_xml(self, collection):
        """Return a string containing the XML representation of a collection 
        and related items
        """
        impl = getDOMImplementation()
        doc = impl.createDocument(None, "telemeta", None)
        coll_node = collection.to_dom().documentElement
        doc.documentElement.appendChild(coll_node)
        items_node_name = MediaItem.get_dom_element_name() + "List"
        items_node = doc.createElement(items_node_name)
        coll_node.appendChild(items_node)

        items = collection.items.all()
        for item in items:
            if item.file:
                item.file = self.__get_media_filename(item)
            items_node.appendChild(item.to_dom().documentElement)
        doc.normalize()

        # libxml2 has prettier output than xml.dom:
        tree = libxml2.parseDoc(doc.toxml(encoding="utf-8"))
        return unicode(tree.serialize(encoding="utf-8", format=1), "utf-8")

        

