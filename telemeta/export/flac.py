# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>

import os
import string

from telemeta.export.core import *
from mutagen.flac import FLAC

class FlacExporter(ExporterCore):
	"""Defines methods to export to OGG Vorbis"""

	def __init__(self):
		self.item_id = ''
		self.metadata = []
		self.description = ''
		self.info = []
		self.source = ''
		self.dest = ''
		self.quality_default = '5'
		
	def get_format(self):
		return 'FLAC'
	
	def get_file_extension(self):
		return 'flac'

	def get_mime_type(self):
		return 'application/flac'

	def get_description(self):
		return """S00N"""

	def get_file_info(self):
		try:
			file1, file2 = os.popen4('metaflac --list "'+self.dest+'"')
			info = []
			for line in file2.readlines():
				info.append(clean_word(line[:-1]))
			self.info = info
			return self.info
		except IOError:
			return 'Exporter error [1]: file does not exist.'

	def set_cache_dir(self,path):
		"""Set the directory where cached files should be stored. Does nothing
        if the exporter doesn't support caching. 
       
        The driver shouldn't assume that this method will always get called. A
        temporary directory should be used if that's not the case.
        """
		self.cache_dir = path

	def decode(self):
		try:
			file_name, ext = get_file_name(self.source)
			dest = self.cache_dir+os.sep+file_name+'.wav'
			os.system('flac -d -o "'+dest+'" "'+self.source+'"')
			self.source = dest
			return dest
		except IOError:
			return 'ExporterError [2]: decoder not compatible.'

	def write_tags(self):
		media = FLAC(self.dest)
		for tag in self.metadata.keys():
			if tag == 'COMMENT':
				media['DESCRIPTION'] = str(self.metadata[tag])
			else:
				media[tag] = str(self.metadata[tag])
		media.save()
		
	def process(self, item_id, source, metadata):
		self.item_id = item_id
		self.source = source
		self.metadata = metadata

		if self.metadata['flac_quality'] != '':
			args = '-f -V -'+self.metadata['flac_quality']
		else:
			args = '-f -s 	-V -'+self.quality_default

		if self.metadata['verbose'] == '0':
			args = args+' -s'
	
		try:
			# Encoding
			os.system('flac '+args+' -o "'+self.dest+'" "'+ \
					  self.source+'" > /dev/null')
			# Write tags
			self.write_tags()
			return self.dest
		except IOError:
			return 'ExporterError [3]: source file does not exist.'

