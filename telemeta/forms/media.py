# -*- coding: utf-8 -*-
# Copyright (C) 2011-2014 Parisson SARL

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
# Authors: Guillaume Pellerin <yomguy@parisson.com>

import django.forms as forms
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from telemeta.models import *
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet
from django.forms.widgets import HiddenInput


class MediaFondsForm(ModelForm):

    widget = FilteredSelectMultiple("Corpus", True,)
    queryset = queryset=MediaCorpus.objects.all()
    children = forms.ModelMultipleChoiceField(widget=widget, queryset=queryset, label='Corpus')

    class Meta:
        model = MediaFonds
        exclude = ['description', 'public_access']

    class Media:
        css = {'all': ['/static/admin/css/widgets.css',],}
        js = ['/admin/django/jsi18n/',]


class MediaFondsRelatedForm(ModelForm):

    class Meta:
        model = MediaFondsRelated
        exclude = ('mime_type',)


class MediaCorpusForm(ModelForm):

    queryset = MediaCollection.objects.all()
    widget = FilteredSelectMultiple('Collections', False)
    children = forms.ModelMultipleChoiceField(widget=widget, queryset=queryset,label='Collections')

    class Meta:
        model = MediaCorpus
        exclude = ['description', 'public_access']

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/django/jsi18n/',)


class MediaCorpusRelatedForm(ModelForm):

    class Meta:
        model = MediaCorpusRelated
        exclude = ('mime_type',)


class MediaCollectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MediaCollectionForm, self).__init__(*args, **kwargs)
        if '_I_' in self.instance.code:
            self.fields["reference"].widget = HiddenInput()
        if self.instance.computed_duration:
            self.fields["approx_duration"].widget = HiddenInput()

    class Meta:
        model = MediaCollection

    def clean_doctype_code(self):
        return self.cleaned_data['doctype_code'] or 0


class MediaCollectionRelatedForm(ModelForm):

    class Meta:
        model = MediaCollectionRelated
        exclude = ('mime_type',)


class MediaItemForm(ModelForm):

    class Meta:
        model = MediaItem
        exclude = ('copied_from_item', 'mimetype', 'url',
                    'organization', 'depositor', 'rights',
                    'recordist', 'digitalist', 'digitization_date',
                    'publishing_date', 'scientist', 'topic',
                    'summary', 'contributor', )

    def clean_code(self):
        return self.cleaned_data['code'] or None


class MediaItemRelatedForm(ModelForm):

    class Meta:
        model = MediaItemRelated
        exclude = ('mime_type',)


class MediaItemKeywordForm(ModelForm):

    class Meta:
        model = MediaItemKeyword


class MediaItemPerformanceForm(ModelForm):

    class Meta:
        model = MediaItemPerformance

    def __init__(self, *args, **kwds):
        super(MediaItemPerformanceForm, self).__init__(*args, **kwds)
        self.fields['instrument'].queryset = Instrument.objects.order_by('name')
        self.fields['alias'].queryset = InstrumentAlias.objects.order_by('name')


class PlaylistForm(ModelForm):

    class Meta:
        model = Playlist


class FondsRelatedInline(InlineFormSet):

    model = MediaFondsRelated


class CorpusRelatedInline(InlineFormSet):

    model = MediaCorpusRelated


class CollectionRelatedInline(InlineFormSet):

    model = MediaCollectionRelated


class CollectionIdentifierInline(InlineFormSet):

    model = MediaCollectionIdentifier
    max_num = 1


class ItemRelatedInline(InlineFormSet):

    model = MediaItemRelated


class ItemPerformanceInline(InlineFormSet):

    model = MediaItemPerformance


class ItemKeywordInline(InlineFormSet):

    model = MediaItemKeyword


class ItemFormatInline(InlineFormSet):

    model = Format


class ItemIdentifierInline(InlineFormSet):

    model = MediaItemIdentifier
    max_num = 1

