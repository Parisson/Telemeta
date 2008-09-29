# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

from django.db.models import Model, CharField

class PhysicalFormat(Model):
    "Physical support of media items"

    value = CharField(max_length=250)
    is_enumeration = True
    def __unicode__(self):
        return self.value
    class Meta:
        app_label = 'telemeta'
        ordering = ['value']
        app_label = 'telemeta'
        
class PublishingStatus(Model):
    "Publishing status of media items"
    value = CharField(max_length=250)
    is_enumeration = True
    def __unicode__(self):
        return self.value
    class Meta:
        app_label = 'telemeta'
        ordering = ['value']
        verbose_name_plural = "Publishing status"

