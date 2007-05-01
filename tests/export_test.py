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
metadata = {'identifier': 'Test',  #collection
		 'title': 'Show Me',
		 'creator': 'Cellar',
		 'type': 'House',
		 'date': '2004',
		 'publisher': 'PArISs0n',
		 }
options = {'verbose': '1'}


class ExportTest(Component):
	exporters = ExtensionPoint(IExporter)

	def run(self):
		verbose = '1'
		for exporter in self.exporters:
			format = exporter.get_format()
			if verbose != '0':
				print "\n+------------------------------------------"
				print '| Testing exporter format: ' + format
				print "+------------------------------------------"
			exporter.set_cache_dir(cache_dir)
			exporter.process(item_id,source,metadata,options)
			#exporter.process(item_id,source,metadata)


compmgr = ComponentManager()
test = ExportTest(compmgr)
test.run()

