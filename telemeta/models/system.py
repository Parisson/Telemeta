# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2011 Parisson SARL

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

from django.contrib.auth.models import User
from telemeta.models.core import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
import django.db.models
from django.forms import ModelForm


class Revision(ModelCore):
    "Revision made by user"
    ELEMENT_TYPE_CHOICES = (('collection', 'collection'), ('item', 'item'), ('part', 'part'), ('marker', 'marker'))
    CHANGE_TYPE_CHOICES  = (('import', 'import'), ('create', 'create'), ('update', 'update'), ('delete','delete'))

    element_type         = CharField(_('element type'), choices=ELEMENT_TYPE_CHOICES, max_length=16, required=True)
    element_id           = IntegerField(_('element identifier'), required=True)
    change_type          = CharField(_('modification type'), choices=CHANGE_TYPE_CHOICES, max_length=16, required=True)
    time                 = DateTimeField(_('time'), auto_now_add=True)
    user                 = ForeignKey(User, db_column='username', related_name="revisions", verbose_name=_('user'))

    @classmethod
    def touch(cls, element, user):    
        "Create or update a revision"
        revision = cls(element_type=element.element_type, element_id=element.pk, 
                       user=user, change_type='create')
        if element.pk:
            try: 
                element.__class__.objects.get(pk=element.pk)
            except ObjectDoesNotExist:
                pass
            else:
                revision.change_type = 'update'

        revision.save()
        return revision

    class Meta(MetaCore):
        db_table = 'revisions'


class UserProfile(django.db.models.Model):
    "User profile extension"
    
    user            = ForeignKey(User, unique=True, required=True)
    institution     = CharField(_('Institution'))
    function        = CharField(_('Function'))
    address         = TextField(_('Address'))
    telephone       = CharField(_('Telephone'))
    expiration_date = DateField(_('Expiration_date'))
    
    class Meta(MetaCore):
        db_table = 'profiles'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
