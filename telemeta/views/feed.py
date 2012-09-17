# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Parisson SARL

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


from telemeta.views.core import *


class LastestRevisionsFeed(Feed):
    "the RSS feed of the lastest revisions"

    organization = settings.TELEMETA_ORGANIZATION
    subjects = settings.TELEMETA_SUBJECTS
    tags = ['title', 'description', 'comment']
    title = organization.decode('utf8') + ' - Telemeta - ' + ugettext('Last changes')
    link = ""
    description = ' '.join([subject.decode('utf-8') for subject in subjects])
    n_items = 100

    def items(self):
        return get_revisions(self.n_items)

    def item_title(self, r):
        element = r['element']
        if element.title == '':
            title = str(element.public_id)
        else:
            title = element.title
        return element.element_type + ' : ' + title

    def item_description(self, r):
        revision = r['revision']
        element = r['element']
        description = '<b>modified by ' + revision.user.username + ' on ' + unicode(revision.time) + '</b><br /><br />'
        dict = element.to_dict()
        for tag in dict.keys():
            try:
                value = dict[tag]
                if value != '':
                    description += tag + ' : ' + value + '<br />'
            except:
                continue
        return description.encode('utf-8')

    def item_link(self, r):
        revision = r['revision']
        element = r['element']
        if revision.element_type[-1] == 's':
            dir = revision.element_type
        else:
            dir = revision.element_type + 's'
        link = '/archives/' + dir + '/' + str(element.public_id)
        return link


class UserRevisionsFeed(LastestRevisionsFeed):

    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def items(self, obj):
        return get_revisions(self.n_items, obj)

