# -*- coding: utf-8 -*-
# Copyright (C) 2010 Samalyse SARL
# Copyright (C) 2010-2014 Parisson SARL

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
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          David LIPSZYC <davidlipszyc@gmail.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from django.utils.translation import ugettext_lazy as _
from telemeta.models.core import *
from telemeta.models.system import *


resource_code_regex = getattr(settings, 'RESOURCE_CODE_REGEX', '[A-Za-z0-9._-]*')


class MediaResource(ModelCore):
    "Base class of all media objects"

    def public_access_label(self):
        if self.public_access == 'metadata':
            return _('Metadata only')
        elif self.public_access == 'full':
            return _('Sound and metadata')

        return _('Private data')
    public_access_label.verbose_name = _('access type')

    def set_revision(self, user):
        "Save a media object and add a revision"
        Revision.touch(self, user)

    def get_revision(self):
        revisions = Revision.objects.filter(element_type=self.element_type, element_id=self.id).order_by('-time')
        if revisions:
            return revisions[0]
        else:
            return None

    class Meta:
        abstract = True

def is_valid_resource_code(value):
    "Check if the resource code is well formed"
    regex = '^' + resource_code_regex + '$'
    if not re.match(regex, value):
        raise ValidationError(u'%s is not a valid resource code' % value)


class MediaBaseResource(MediaResource):
    "Describe a media base resource"

    title                 = CharField(_('title'), required=True)
    description           = CharField(_('description_old'))
    descriptions          = TextField(_('description'))
    code                  = CharField(_('code'), unique=True, required=True, validators=[is_valid_resource_code])
    public_access         = CharField(_('public access'), choices=PUBLIC_ACCESS_CHOICES, max_length=16, default="metadata")

    def __unicode__(self):
        return self.code

    @property
    def public_id(self):
        return self.code

    def save(self, *args, **kwargs):
        super(MediaBaseResource, self).save(*args, **kwargs)

    def get_fields(self):
        return self._meta.fields

    class Meta(MetaCore):
        abstract = True


class MediaRelated(MediaResource):
    "Related media"

    element_type = 'media'

    title           = CharField(_('title'))
    date            = DateTimeField(_('date'), auto_now=True)
    description     = TextField(_('description'))
    mime_type       = CharField(_('mime_type'))
    url             = CharField(_('url'), max_length=500)
    credits         = CharField(_('credits'))
    file            = FileField(_('file'), upload_to='items/%Y/%m/%d', db_column="filename", max_length=255)

    def is_image(self):
        is_url_image = False
        if self.url:
            url_types = ['.png', '.jpg', '.gif', '.jpeg']
            for type in url_types:
                if type in self.url or type.upper() in self.url:
                    is_url_image = True
        return 'image' in self.mime_type or is_url_image

    def save(self, *args, **kwargs):
        super(MediaRelated, self).save(*args, **kwargs)

    def set_mime_type(self):
        if self.file:
            self.mime_type = mimetypes.guess_type(self.file.path)[0]

    def is_kdenlive_session(self):
        if self.file:
            return '.kdenlive' in self.file.path
        else:
            return False

    def __unicode__(self):
        if self.title and not re.match('^ *N *$', self.title):
            return self.title
        elif self.file:
            return unicode(self.file.path.split(os.sep)[-1])
        elif self.url:
            return unicode(self.url.split('/')[-1])
        else:
            return '_'

    class Meta:
        abstract = True
