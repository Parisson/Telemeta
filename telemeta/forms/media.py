# -*- coding: utf-8 -*-
# Copyright (C) 2011-2014 Parisson SARL

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
# Authors: Guillaume Pellerin <yomguy@parisson.com>

import django.forms as forms
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from telemeta.models import *
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _


class MediaFondsForm(ModelForm):

    queryset = MediaCorpus.objects.all()
    widget = FilteredSelectMultiple("Corpus", is_stacked=False)
    children = forms.ModelMultipleChoiceField(widget=widget, queryset=queryset,
        label='Corpus', required=False)

    class Meta:
        model = MediaFonds
        exclude = ['description', 'public_access']

    class Media:
        css = {'all': ['/static/admin/css/widgets.css',],}
        js = ['/admin/django/jsi18n/',]


class MediaCorpusForm(ModelForm):

    queryset = MediaCollection.objects.all()
    widget = FilteredSelectMultiple('Collections', is_stacked=False)
    children = forms.ModelMultipleChoiceField(widget=widget, queryset=queryset,
        label='Collections', required=False)

    class Meta:
        model = MediaCorpus
        exclude = ['description', 'public_access']

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/django/jsi18n/',)


class MediaCollectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MediaCollectionForm, self).__init__(*args, **kwargs)
        if '_I_' in self.instance.code:
            self.fields["reference"].widget = HiddenInput()
        if self.instance.computed_duration:
            self.fields["approx_duration"].widget = HiddenInput()

    class Meta:
        model = MediaCollection
        exclude = model.exclude

    def clean_doctype_code(self):
        return self.cleaned_data['doctype_code'] or 0


class MediaItemForm(ModelForm):

    class Meta:
        model = MediaItem
        exclude = model.exclude

    def clean_code(self):
        return self.cleaned_data['code'] or None


class RestrictedMediaItemForm(MediaItemForm):

    class Meta:
        model = MediaItem
        exclude = model.restricted


class PlaylistForm(ModelForm):

    class Meta:
        model = Playlist


class FondsRelatedInline(InlineFormSet):

    model = MediaFondsRelated
    exclude = ['mime_type']


class CorpusRelatedInline(InlineFormSet):

    model = MediaCorpusRelated
    exclude = ['mime_type']


class CollectionRelatedInline(InlineFormSet):

    model = MediaCollectionRelated
    exclude = ['mime_type']


class ItemRelatedInline(InlineFormSet):

    model = MediaItemRelated
    exclude = ['mime_type']


class CollectionIdentifierInline(InlineFormSet):

    model = MediaCollectionIdentifier
    max_num = 1


class ItemPerformanceInline(InlineFormSet):

    model = MediaItemPerformance


class ItemKeywordInline(InlineFormSet):

    model = MediaItemKeyword


class ItemFormatInline(InlineFormSet):

    model = Format
    max_num = 1


class ItemIdentifierInline(InlineFormSet):

    model = MediaItemIdentifier
    max_num = 1


class EpubPasswordForm(forms.Form):

    password = forms.CharField(label=_('password'))
