#!/usr/bin/python
# *coding: utf-8*
#
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import os, string

class Collection :

	def __init__(self) :
		self.collection_name = 'telemeta_default'
		self.collection_dir = '/home/'+os.environ["USER"]+'/telemeta_default/'
		self.user_dir = '/home/'+os.environ["USER"]+'/.telemeta/'
		self.default_tag_xml = '/home/'+os.environ["USER"]+'/.telemeta/default_tags.xml'
		self.default_collection_xml = '/home/'+os.environ["USER"]+'/.telemeta/default_collection.xml'
		self.tag_table = 'ARTIST,TITLE,ALBUM,DATE,GENRE,SOURCE,ENCODER,COMMENT'
		self.type_list = 'mp3,ogg,flac,wav,aiff'
		self.net_backup_host = 'domain.com'
		self.net_backup_dir = '/home/'+os.environ["USER"]+'/telemeta/'

#option_table=['enc_types','flac_bitrate','ogg_bitrate','mp3_bitrate','audio_marking','auto_audio_marking','audio_marking_file','audio_marking_timeline']

#questions = ['Output formats','flac_bitrate','ogg_bitrate','mp3_bitrate','Audio marking (y/n)','Auto audio marking (y/n)','Audio marking file path','Audio marking timeline (b)eginning, (m)iddle, (e)nd']