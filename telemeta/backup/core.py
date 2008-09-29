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
from xml.dom.minidom import getDOMImplementation, Node
import shutil
import md5
from django.conf import settings
from telemeta.models import MediaItem

class CollectionSerializer(object):
    """Provide backup-related features"""

    def __init__(self, collection):
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
        return item.id + ".wav"

    def store(self, dest_dir):
        """Serialize and store the collection with related items and media 
        files into a subdirectory of the provided directory
        """
        coll_dir = dest_dir + "/" + self.collection.id
        os.mkdir(coll_dir)

        xml = self.get_xml()
        file = open(coll_dir + "/collection.xml", "wb")
        file.write(xml.encode("utf-8"))
        file.close()

        if self.collection.has_mediafile():
            md5_file = open(coll_dir + "/MD5SUM", "wb")

            items = self.collection.items.all()
            for item in items:
                if item.file:
                    dst_basename = self.__get_media_filename(item)
                    dst = coll_dir + "/" + dst_basename
                    shutil.copyfile(item.file.path, dst)
                    hash = self.__get_file_md5(dst)
                    md5_file.write(hash + "  " + dst_basename + "\n")

            md5_file.close()

    def get_xml(self):
        """Return a string containing the XML representation of the collection 
        and related items
        """
        impl = getDOMImplementation()
        doc = impl.createDocument(None, "telemeta", None)
        coll_doc = self.collection.to_dom()
        coll_node = doc.documentElement.appendChild(coll_doc.documentElement)
        coll_doc.unlink()
        items_node_name = MediaItem.get_dom_element_name() + "List"
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

        # libxml2 has prettier output than xml.dom:
        tree = libxml2.parseDoc(doc.toxml(encoding="utf-8"))
        doc.unlink()
        xml = unicode(tree.serialize(encoding="utf-8", format=1), "utf-8")
        tree.free()

        return xml
        

