# -*- coding: utf-8 -*-
# Copyright (C) 2015 Parisson SARL

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
# Authors: Angy Fils-Aimé
#          Killian Mary
#          Novembre 2015 : Raouf Benmansour


from telemeta.models import *
from haystack.forms import *
from haystack.query import SearchQuerySet, SQ
from datetime import date
from django.utils.translation import ugettext_lazy as _
from settings import FIRST_YEAR
import operator

# from telemeta.views.boolean_search import *


class HaySearchForm(FacetedSearchForm):

    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))

    def search(self):
        sqs = SearchQuerySet().load_all()

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            # search input of a code, contains at least '_YYYY_'
            # if not re.match('([a-zA-Z]*_?[EI])?_[0-9]{4}_([0-9]{3}_[0-9]{3})?', self.cleaned_data.get('q')):
            sqs = sqs.filter(content__startswith=self.cleaned_data['q']).facet('item_acces').facet('item_status').facet('digitized').facet('recording_context').facet('physical_format').facet('media_type')
            # else:
            #    sqs = sqs.filter(code__contains=self.cleaned_data['q']).facet('item_acces').facet('item_status').facet('digitized').facet('recording_context').facet('physical_format').facet('media_type')

        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                if value == 'viewable':
                    sqs = sqs.narrow('item_acces:full OR item_acces:mixed').narrow('digitized:T')
                else:
                    sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        return sqs


class HayAdvanceForm(SearchForm):

    # to replace de basic search form field
    q = forms.CharField(required=False, label=(_('title')), widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'search'}))

    location = forms.CharField(required=False, label=(_('location')), widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'search'}))

    # to create a dynamic list of ethnic group
    def list_ethnic_group():
        type_name = []
        type_name.append(('', 'no preference'))
        list_ethnic_group = EthnicGroup.objects.all()
        for ethnic in list_ethnic_group:
            type_name.append((ethnic.value, ethnic.value))
        return type_name

    ethnic_group = forms.ChoiceField(
        required=False,
        label=(_('population / social group')),
        choices=list_ethnic_group,
        widget=forms.Select(attrs={'style': 'width:100%'})
    )
    instruments = forms.CharField(required=False, label=(_('instruments')), widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'search'}))
    collectors = forms.CharField(required=False, label=(_('recordist')), widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'search'}))

    # @cached_property
    

    # to create a dynamic list of publishing years
    def list_recorded_year():
        last_year = date.today().year
        list_year = []
        list_year.append(('', '----'))
        year=getattr(settings, 'FIRST_YEAR', '[A-Za-z0-9._-]*')
        while(year<=last_year):
            list_year.append((str(year),year))
            year+=1
        return list_year

    recorded_from_date = forms.TypedChoiceField(
        coerce=int,
        required=False,
        label=(_('recording date (from)')),
        choices=list_recorded_year,
        widget=forms.Select(attrs={'style': 'width:47%'}),
    )
    recorded_to_date = forms.TypedChoiceField(
        coerce=int,
        required=False,
        label=(_('recording date (until')),
        choices=list_recorded_year,
        widget=forms.Select(attrs={'style': 'width:47%'})
    )

    # to create a dynamic list of publishing years
    def list_publish_year():
    	last_year = date.today().year
        list_year = []
        list_year.append(('', '----'))
        year=getattr(settings, 'FIRST_YEAR', '[A-Za-z0-9._-]*')
        while(year<=last_year):
            list_year.append((str(year),year))
            year+=1
        return list_year

    year_published_from = forms.TypedChoiceField(
        coerce=int,
        required=False,
        label=(_('year published from')),
        choices=list_publish_year,
        widget=forms.Select(attrs={'style': 'width:47%'})
    )
    year_published_to = forms.TypedChoiceField(
        coerce=int,
        required=False,
        label=(_('year published to')),
        choices=list_publish_year,
        widget=forms.Select(attrs={'style': 'width:47%'})
    )

    VIEWABLE_CHOICE = (('1', 'no preference'), ('2', 'online and public'),
                       ('3', 'online (account required)'))
    viewable = forms.CharField(
        required=False, label=(_('viewable')),
        widget=forms.RadioSelect(choices=VIEWABLE_CHOICE),
        initial=1)
    STATUS_CHOICES = (('1', 'no preference'), ('pub', 'Published'),
                      ('unpub', 'Unpublished'))
    item_status = forms.CharField(
        required=False,
        label=(_('Document status')),
        widget=forms.RadioSelect(choices=STATUS_CHOICES),
        initial=1)

    # to create a dynamic list of media types
    def list_media_type():
        type_name = []
        type_name.append(('1', 'no preference'))
        list_media_type = MediaType.objects.all()
        for mt in list_media_type:
            type_name.append((mt.value, mt.value))
        return type_name

    media_type = forms.ChoiceField(
        required=False,
        label=(_('media')),
        choices=list_media_type,
        widget=forms.RadioSelect(),
        initial=1)

    # to create a dynamic list of recording contexts
    def list_recording_context():
        type_name = []
        type_name.append(('', 'no preference'))
        list_recording_context = RecordingContext.objects.all()
        for context in list_recording_context:
            type_name.append((context.value, context.value))
        return type_name

    recording_context = forms.ChoiceField(
        required=False,
        label=(_('recording context')),
        choices=list_recording_context,
        widget=forms.Select(attrs={'style': 'width:100%'})
    )

    # to create a dynamic list of physical formats
    def list_physical_format():
        type_name = []
        type_name.append(('', 'no preference'))
        list_physical_format = PhysicalFormat.objects.all()
        for physical_format in list_physical_format:
            type_name.append((physical_format.value, physical_format.value))
        return type_name

    physical_format = forms.ChoiceField(
        required=False,
        label=(_('physical format')),
        choices=list_physical_format,
        widget=forms.Select(attrs={'style': 'width:100%'})
    )
    code = forms.CharField(
        required=False,
        label=(_('code')),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'search'}))

    # def filter_instru(self, query):
    #    if isinstance(query, str) or isinstance(query, unicode):
    #         try:
    #             BooleanSearchView().is_correct_query(query)
    #         except TelemetaError:
    #             return SQ(instruments__startswith=query)
    #    operateur = "ET"
    #    if isinstance(query, list):
    #        query_terms = query
    #    else:
    #        query_terms = query.split()
    #    sqTab = []
    #    valeur = ""
    #    while len(query_terms) != 0:
    #        term = query_terms.pop(0)
    #        if term == "ET" or term == "OU":
    #            if valeur != "":
    #                sqTab.append(('instruments__startswith', valeur.strip()))
    #                valeur = ""
    #            if term != operateur:
    #                sqTab = [SQ(filtre) for filtre in sqTab]
    #                objet = reduce(operator.or_, sqTab) if operateur == "OU" else reduce(operator.and_, sqTab)
    #                del sqTab[:]
    #                sqTab.append(objet)
    #                operateur = "OU" if operateur == "ET" else "ET"
    #        elif term == "(":
    #            indexCloseBracket = get_close_bracket(query_terms)
    #            sqTab.append(self.filter_instru(query_terms[:indexCloseBracket]))
    #            del query_terms[:indexCloseBracket + 1]
    #        else:
    #            valeur += term + " "
    #    if valeur != "":
    #        sqTab.append(('instruments__startswith', valeur.strip()))
    #    sqTab = [SQ(filtre) for filtre in sqTab]
    #    return SQ(reduce(operator.and_, sqTab) if operateur == "ET" else reduce(operator.or_, sqTab))

    def search(self):
        sqs = SearchQuerySet().load_all()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data.get('q'):
            sqs = sqs.filter(title__startswith=self.cleaned_data['q'])

        if self.cleaned_data.get('code'):
            sqs = sqs.filter(code__contains=self.cleaned_data['code'])

        if self.cleaned_data.get('location'):
            sqs = sqs.filter(Q(location_principal__startswith=self.cleaned_data['location']) | Q(location_relation__startswith=self.cleaned_data['location']))

        if self.cleaned_data['ethnic_group']:
            if self.cleaned_data.get('ethnic_group') != '':
                sqs = sqs.filter(ethnic_group__contains=self.cleaned_data['ethnic_group'])

        if self.cleaned_data.get('instruments'):
            # sqs = sqs.filter(self.filter_instru(self.cleaned_data['instruments']))
            sqs = sqs.filter(instruments__startswith=self.cleaned_data['instruments'])

        if self.cleaned_data.get('collectors'):
            sqs = sqs.filter(collectors__startswith=self.cleaned_data['collectors'])

        if self.cleaned_data['recorded_from_date']:
            sqs = sqs.filter(recorded_from_date__gte=self.cleaned_data['recorded_from_date'])

        if self.cleaned_data['recorded_to_date']:
            sqs = sqs.filter(recorded_to_date__lte=self.cleaned_data['recorded_to_date'])

        if self.cleaned_data['year_published_from']:
            sqs = sqs.filter(year_published__gte=self.cleaned_data['year_published_from'])

        if self.cleaned_data['year_published_to']:
            sqs = sqs.filter(year_published__lte=self.cleaned_data['year_published_to'])

        if self.cleaned_data['viewable']:
            if self.cleaned_data.get('viewable') == '2':
                sqs = sqs.filter(digitized__exact=True).filter(Q(item_acces='full') | Q(item_acces='mixed'))
            if self.cleaned_data.get('viewable') == '3':
                sqs = sqs.filter(digitized__exact=True)

        if self.cleaned_data['item_status']:
            if self.cleaned_data.get('item_status') == 'pub':
                sqs = sqs.filter(item_status__exact='Published')
            if self.cleaned_data.get('item_status') == 'unpub':
                sqs = sqs.filter(item_status__exact='Unpublished')

        if self.cleaned_data['media_type']:
            if self.cleaned_data.get('media_type') != '1':
                sqs = sqs.filter(media_type=self.cleaned_data['media_type'])

        if self.cleaned_data['recording_context']:
            if self.cleaned_data.get('recording_context') != '':
                sqs = sqs.filter(recording_context=self.cleaned_data['recording_context'])

        if self.cleaned_data['physical_format']:
            if self.cleaned_data.get('physical_format') != '':
                sqs = sqs.filter(physical_format=self.cleaned_data['physical_format'])

        return sqs