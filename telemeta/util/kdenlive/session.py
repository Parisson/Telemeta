# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Authors: Guillaume Pellerin <yomguy@parisson.com>


from telemeta.util.xmltodict2 import *


class KDEnLiveSession(object):

	def __init__(self, path):
		self.session = xmltodict(path)

	def entries(self):
		entries = []
		for attr in self.session['children']:
			if 'playlist' in attr['name'] and 'children' in attr:
				for att in attr['children']:
					if 'entry' in att['name'] and att['attributes']['producer'] != 'black':
						entries.append(att['attributes'])
		return entries

	def entries_sorted(self):
		return sorted(self.entries(), key=lambda k: int(k['in']), reverse=False)

	def first_video_frame(self):
		return int(self.entries_sorted()[0]['in'])

	def profile(self):
		for attr in self.session['children']:
			if 'profile' in attr['name']:
				return attr['attributes']

	def markers_relative(self):
		markers = []
		fps = float(self.profile()['frame_rate_num'])
		first_frame_seconds = self.first_video_frame()/fps
		for attr in self.session['children']:
			if 'kdenlivedoc' in attr['name']:
				for att in attr['children']:
					if 'markers' in att['name']:
						for at in att['children']:
							if 'marker' in at['name']:
								time = float(at['attributes']['time'].replace(',','.')) - first_frame_seconds
								at['attributes']['time'] = time
				 				markers.append(at['attributes'])
		return markers
