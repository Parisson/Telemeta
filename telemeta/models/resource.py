# -*- coding: utf-8 -*-
# Copyright (C) 2010 Samalyse SARL
# Copyright (C) 2010-2014 Parisson SARL

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
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          David LIPSZYC <davidlipszyc@gmail.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from django.utils.translation import ugettext_lazy as _
from telemeta.models.core import *
from telemeta.models.system import *


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
        return Revision.objects.filter(element_type=self.element_type, element_id=self.id).order_by('-time')[0]

    class Meta:
        abstract = True


class MediaBaseResource(MediaResource):
    "Describe a media base resource"

    title                 = CharField(_('title'), required=True)
    description           = CharField(_('description_old'))
    descriptions          = TextField(_('description'))
    code                  = CharField(_('code'), unique=True, required=True)
    public_access         = CharField(_('public access'), choices=PUBLIC_ACCESS_CHOICES, max_length=16, default="metadata")

    def __unicode__(self):
        return self.code

    @property
    def public_id(self):
        return self.code

    def save(self, force_insert=False, force_update=False, user=None, code=None):
        super(MediaBaseResource, self).save(force_insert, force_update)

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

    def save(self, force_insert=False, force_update=False, author=None):
        super(MediaRelated, self).save(force_insert, force_update)

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
            title = self.title
        else:
            title = unicode(self.item)
        return title

    class Meta:
        abstract = True


