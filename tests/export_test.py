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

cache_dir = 'cache/'
source = 'samples/wav/Cellar - Show Me - 02.wav'
item_id = '1'
metadata = {'Collection': 'Test',
		 'Title': 'Show Me',
		 'Artist': 'Cellar',
		 'Encoder': 'Telemeta',
		 }

media1 = OggExporter()
media1.set_cache_dir(cache_dir)
media1.process(item_id,source,metadata)

media2 = FlacExporter()
media2.set_cache_dir(cache_dir)
media2.process(item_id,source,metadata)

media3 = WavExporter()
media3.set_cache_dir(cache_dir)
media3.process(item_id,source,metadata)


