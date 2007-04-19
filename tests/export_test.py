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
from telemeta.core import *
from telemeta.core import ComponentManager

cache_dir = 'cache/'
source = 'samples/wav/Cellar - Show Me - 02.wav'
item_id = '1'
metadata = {'Collection': 'Test',
		 'Title': 'Show Me',
		 'Artist': 'Cellar',
		 'Encoder': 'Telemeta',
		 }
options = {'verbose': '1'}


class ExportTest(Component):
	exporters = ExtensionPoint(IExporter)

	def run(self):
		for exporter in self.exporters:
			format = exporter.get_format()
			print "+------------------------------------------"
			print '| Testing exporter format: ' + format
			print "+------------------------------------------"
			exporter.set_cache_dir(cache_dir)
			exporter.process(item_id,source,metadata,options)

compmgr = ComponentManager()
test = ExportTest(compmgr)
test.run()

