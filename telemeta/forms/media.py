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

from django_select2.forms import ( Select2MultipleWidget )
from markdownx.fields import MarkdownxFormField


class MediaFondsForm(ModelForm):

    queryset = MediaCorpus.objects.all()
    widget = FilteredSelectMultiple("Corpus", is_stacked=False)
    children = forms.ModelMultipleChoiceField(widget=widget, queryset=queryset,
        label=_('corpus'), required=False)

    def __init__(self, *args, **kwargs):
        super(MediaFondsForm, self).__init__(*args, **kwargs)
        self.fields["descriptions"] = MarkdownxFormField(label=_('Description'))
        self.fields["descriptions"].required = False
        self.fields["code"] = forms.RegexField(regex='^\w+$')

    class Meta:
        model = MediaFonds
        exclude = ['description']

    class Media:
        css = {'all': ['/static/admin/css/widgets.css',],}
        js = ['/admin/django/jsi18n/',]


class MediaCorpusForm(ModelForm):

    queryset = MediaCollection.objects.all()
    widget = FilteredSelectMultiple('Collections', is_stacked=False)
    children = forms.ModelMultipleChoiceField(widget=widget, queryset=queryset,
        label='Enquêtes', required=False)

    def __init__(self, *args, **kwargs):
        super(MediaCorpusForm, self).__init__(*args, **kwargs)
        self.fields["descriptions"] = MarkdownxFormField(label=_('Description'))
        self.fields["descriptions"].required = False
        self.fields["code"] = forms.RegexField(regex='^\w+$')

    class Meta:
        model = MediaCorpus
        exclude = ['description', 'public_access','recorded_from_year', 'recorded_to_year']

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/django/jsi18n/',)


class MediaCollectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MediaCollectionForm, self).__init__(*args, **kwargs)

        self.fields["location"] = forms.ModelMultipleChoiceField(
            queryset = Location.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Lieu',
                'data-width':'100%',
                }),
            label=_("location"),
            required=False
        )
        self.fields["language_iso"] = forms.ModelMultipleChoiceField(
            queryset = Language.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Editeurs',
                'data-width':'100%',
                }),
            label=_("Language (ISO norm)"),
            required=False
        )
        self.fields["informer"] = forms.ModelMultipleChoiceField(
            queryset = Authority.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Liste des informateurs',
                'data-width':'100%',
                }),
            label=_("informers"),
            required=False
        )
        self.fields["collectors"] = forms.ModelMultipleChoiceField(
            queryset = Authority.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Liste des enquêteurs',
                'data-width':'100%',
                }),
            label=_("recordist"),
            required=False
        )
        self.fields["publisher"] = forms.ModelMultipleChoiceField(
            queryset = Publisher.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Editeurs',
                'data-width':'100%',
                }),
            label="Editeur",
            required=False
        )
        self.fields["booklet_author"] = forms.ModelMultipleChoiceField(
            queryset = Authority.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Editeurs',
                'data-width':'100%',
                }),
            label=_("booklet author"),
            required=False
        )
        self.fields["description"] = MarkdownxFormField()
        self.fields["description"].required = False
        self.fields["location_details"] = MarkdownxFormField()
        self.fields["location_details"].required = False
        self.fields["booklet_description"] = MarkdownxFormField()
        self.fields["booklet_description"].required = False
        self.fields["code"] = forms.RegexField(regex='^\w+$')

        # MSHS labels
        self.fields["collectors"].label = u'Enquêteur(s)'
        self.fields["location_details"].label = u'Précisions lieu'
        self.fields["informer"].label = u"Informateurs(s)"
        self.fields["booklet_description"].label = u"Documentation associée"
        self.fields["code"].label = "Cote"


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

    mshs_informers = forms.ModelMultipleChoiceField(
                queryset = MediaCollectionPerformance.objects.all(),
                widget=Select2MultipleWidget(
                    attrs={
                        'title': 'Liste des informateurs',
                        'data-width':'100%',
                        }),
                label="informers",
            )

    domains = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=MediaItem._meta.get_field('mshs_domain').choices)



    class Meta:
        model = MediaItem
        exclude = model.exclude

    def clean_code(self):
        return self.cleaned_data['code'] or None

    def __init__(self, *args, **kwargs):
        super(MediaItemForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['mshs_informers'].queryset = MediaCollectionPerformance.objects.filter(
                                               collection=self.instance.collection)
            self.fields['domains'].initial = self.instance.mshs_domain.split(',')

        # Hidden fields
        self.fields['collection'].widget=forms.HiddenInput()
        #self.fields['collector'].widget=forms.HiddenInput()


        self.fields["collectors"] = forms.ModelMultipleChoiceField(
            queryset = Authority.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Liste des enquêteurs',
                'data-width':'100%',
                }),
            label=_("recordist"),
            required=False
        )

        self.fields["informer"] = forms.ModelMultipleChoiceField(
            queryset = Authority.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Liste des informateurs',
                'data-width':'100%',
                }),
            label=_("informers"),
            required=False
        )

        self.fields["language_iso"] = forms.ModelMultipleChoiceField(
            queryset = Language.objects.all(),
            widget=Select2MultipleWidget(
            attrs={
                'title': 'Editeurs',
                'data-width':'100%',
                }),
            label=_("Language (ISO norm)"),
            required=False
        )
        # Labels MSHS
        translations = [
            ["alt_title","Traduction titre"],
            ["mshs_alt_title","Autre(s) titre(s)"],
            ["collectors","Enquêteur(s)"],
            ["informer","Informateur(s)"],
            ["description","Description de l'item"],
            ["language_iso","Langue(s)(norme ISO)"],
            ["language","Langues(s)"],
            ["context_comment","Contexte d'enregistrement"],
            ["code","Cote de l'item"],
            ["mshs_author","Auteur(s)"],
            ["mshs_composer","Compositeur(s)"],
            ["mshs_timbre","Timbre(s) de l'air"],
            ["mshs_timbre_ref","Timbre(s) référencés - Cote du timbre"],
            ["mshs_melody","Mélodie (transcription alphabétique)"],
            ["domains","Domaine(s)"],
            ["mshs_domain_song","Genre(s) de la chanson"],
            ["mshs_domain_vocal","Genre(s) de l'Autre expression vocale"],
            ["mshs_domain_music","Genre(s) de l'expression instrumentale"],
            ["mshs_domain_tale","Genre(s) du Conte"],
            ["mshs_function","Fonctions(s)"],
            ["mshs_dance","Danse(s)"],
            ["mshs_dance_details","Précisions sur la danse"],
            ["mshs_deposit_thematic","Thématique(s)"],
            ["mshs_deposit_names","Nom(s) propre(s) cité(s) "],
            ["mshs_deposit_places","Lieu(x) cité(s"],
            ["mshs_deposit_periods","Période(s) citée(s)"],
            ["mshs_title_ref_coirault","Titre(s) référencé(s) et cote(s) Coirault"],
            ["mshs_title_ref_laforte","Titre(s) référencé(s) et cote(s) Laforte"],
            ["mshs_title_ref_Dela","Titre(s) référencé(s) et cote(s) Delarue -Tenèze"],
            ["mshs_title_ref_Aare","Titre(s) référencé(s) et cote(s) Aarne-Thompson"]
        ]
        for t in translations :
            self.fields[t[0]].label=t[1]



        self.fields["description"] = MarkdownxFormField(label=_('Description'))
        self.fields["description"].required = False
        self.fields["dance_details"] = MarkdownxFormField(label=_('Details on dance'))
        self.fields["dance_details"].required = False
        self.fields["mshs_deposit_digest"] = MarkdownxFormField( label=_('Digest'))
        self.fields["mshs_deposit_digest"].required = False
        self.fields["mshs_text"] = MarkdownxFormField(label=_('Text'))
        self.fields["mshs_text"].required = False
        self.fields["mshs_informers"].required = False
        self.fields["code"] = forms.RegexField(regex='^\w+$')

        # if you want to do it to all of them
        for field in self.fields.values():
            field.error_messages = {'required':'Le champ {fieldname} est obligatoire'.format(fieldname=field.label), 'blank':'Le champ {fieldname} est vide'.format(fieldname=field.label), 'null':'Le champ {fieldname} est de valeur null'.format(fieldname=field.label) }

    def save(self, commit=True):
        item = super(MediaItemForm,self).save(commit=False)
        item.mshs_domain = ','.join(self.cleaned_data['domains'])
        if commit:
            item.save()
            self.save_m2m()
        return item


class RestrictedMediaItemForm(MediaItemForm):

    class Meta:
        model = MediaItem
        exclude = model.restricted


class PlaylistForm(ModelForm):

    class Meta:
        model = Playlist
        fields = '__all__'


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
    fields = '__all__'


class CollectionPerformanceInline(InlineFormSet):

    model = MediaCollectionPerformance
    fields = '__all__'


class ItemKeywordInline(InlineFormSet):

    model = MediaItemKeyword
    fields = '__all__'


class ItemFormatInline(InlineFormSet):

    model = Format
    max_num = 1
    fields = '__all__'


class ItemIdentifierInline(InlineFormSet):

    model = MediaItemIdentifier
    max_num = 1
    fields = '__all__'


class EpubPasswordForm(forms.Form):

    password = forms.CharField(label=_('password'))
    fields = '__all__'
