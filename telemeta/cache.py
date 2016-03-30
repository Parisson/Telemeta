#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 Guillaume Pellerin, Parisson SARL

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

# Author: Guillaume Pellerin <yomguy@parisson.com>

import os
import xml.dom.minidom


class TelemetaCache(object):

    def __init__(self, dir, params=None):
        self.dir = dir
        self.params = params
        self.files = self.get_files()
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except IOError:
                raise 'Could not create the '+dir+' directory !'

    def get_files(self):
        list = []
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                list.append(file)
        return list

    def add_file(self, file):
        self.files.append(file)


    def exists(self, file):
        #if not file in self.files:
        #    self.files = self.get_files()
        return file in self.files

    def delete_item_data(self, public_id):
        # public_id is the public_id of an item
        for file in self.files:
            if public_id in file:
                os.remove(self.dir + os.sep + file)

    def write_bin(self, data, file):
        path = self.dir + os.sep + file
        f = open(path, 'w')
        f.write(data)
        f.close()

    def read_bin(self, file):
        path = self.dir + os.sep + file
        f = open(path,  'r')
        data = f.read()
        f.close()
        return data

    def read_stream_bin(self, file):
        path = self.dir + os.sep + file
        chunk_size = 0x80000
        f = open(path,  'r')
        while True:
            chunk = f.read(chunk_size)
            if not len(chunk):
                f.close()
                break
            yield chunk

    def write_stream_bin(self, chunk, file_object):
        file_object.write(chunk)

    def read_analyzer_xml(self, file):
        list = []
        path = self.dir + os.sep + file
        f = open(path, "r")
        doc = xml.dom.minidom.parse(path)
        for data in doc.documentElement.getElementsByTagName('data') :
            name = data.getAttribute('name')
            id = data.getAttribute('id')
            unit = data.getAttribute('unit')
            value = data.getAttribute('value')
            list.append({'name': name, 'id': id, 'unit': unit, 'value': value})
        f.close()
        return list

    def write_analyzer_xml(self, data_list, file):
        path = self.dir + os.sep + file
        data = self.get_analyzer_xml(data_list)
        f = open(path, "w")
        f.write(data)
        f.close()

    def get_analyzer_xml(self, data_list):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('telemeta')
        doc.appendChild(root)
        for data in data_list:
            name = data['name']
            id = data['id']
            unit = data['unit']
            value = data['value']
            node = doc.createElement('data')
            node.setAttribute('name', name)
            node.setAttribute('id', id)
            node.setAttribute('unit', unit)
            node.setAttribute('value', unicode(value))
            root.appendChild(node)
        return xml.dom.minidom.Document.toprettyxml(doc)
