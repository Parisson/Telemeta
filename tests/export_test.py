#!/usr/bin/python
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
from telemeta.export import *

class ExportTest:
	"""Test the 'export' features"""
	def __init__(self):
		self.cache_dir = 'cache/'
		self.source = 'samples/wav/Cellar - Show Me - 02.wav'
		self.item_id = '1'
		
		self.metadata = {'Collection': 'Test_Collection',
						 'Title': 'Show Me',
						 'Artist': 'Cellar',
						 'Encoder': 'Telemeta',
						 'Item_id': self.item_id,
						 'export_formats': ['WAV','OGG','FLAC'],
						 'normalize': True,
						 'md5': True,
						 'par2': True,
						 'ogg_bitrate': '192',
						 'ogg_quality': '4',
						 'flac_quality': '5',
						 'verbose': '1',
						 }
		
		self.dest = core.ExporterCore()
		self.dest.set_cache_dir = self.cache_dir
						 
	def process(self):
		self.dest.process(self.item_id, self.source, self.metadata)


media = ExportTest()
media.process()