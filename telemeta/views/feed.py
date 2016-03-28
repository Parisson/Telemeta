# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Parisson SARL

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
        dict = element.__dict__
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

