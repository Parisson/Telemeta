# -*- coding: utf-8 -*-
# Copyright (C) 2015 Angy Fils-Aimé, Killian Mary

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


from haystack.views import *
from haystack.query import SearchQuerySet, SQ
from telemeta.models import *
from telemeta.forms.haystack_form import *
from saved_searches.views import SavedSearchView
import re
import unicodedata
import simplejson as json
from django.http import HttpResponse


class HaystackSearch(FacetedSearchView, SavedSearchView):
    search_key = 'quick'

    def __call__(self, request, type=None):
        self.type = type
        self.form_class = HaySearchForm
        self.selected_facet = self.selected_facet_list(request.GET.getlist('selected_facets', ['a']))
        print(self.selected_facet)
        if request.GET.get('results_page'):
            self.results_per_page = int(request.GET.get('results_page'))
        else:
            self.results_per_page = 20
        return super(HaystackSearch, self).__call__(request)

    def get_query(self):
        return super(HaystackSearch, self).get_query()

    def get_results(self):
        if (self.type == 'item'):
            return super(HaystackSearch, self).get_results().models(MediaItem)
        elif (self.type == 'corpus'):
            return super(HaystackSearch, self).get_results().models(MediaCorpus)
        elif (self.type == 'fonds'):
            return super(HaystackSearch, self).get_results().models(MediaFonds)
        else:
            return super(HaystackSearch, self).get_results().models(MediaCollection)

    def selected_facet_list(self, selected_facets):
        facet_list = []
        for facet in selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value and not value in facet_list:
                if field == 'digitized_exact':
                    facet_list.append('Sound')
                else:
                    facet_list.append(value)

        return facet_list

    def extra_context(self):
        extra = super(HaystackSearch, self).extra_context()
        extra['collection_count'] = super(HaystackSearch, self).get_results().models(MediaCollection).count()
        extra['item_count'] = super(HaystackSearch, self).get_results().models(MediaItem).count()
        extra['corpus_count'] = super(HaystackSearch, self).get_results().models(MediaCorpus).count()
        extra['fonds_count'] = super(HaystackSearch, self).get_results().models(MediaFonds).count()

        if extra['facets']:
            viewable_total = 0
            for viewable in extra['facets']['fields']['item_acces']:
                if viewable == 'none':
                    pass
                else:
                    viewable_total = viewable_total + viewable[1]

            extra['Published_count'] = self.get_results().narrow('item_status:Published').count()
            extra['Unpublished_count'] = self.get_results().narrow('item_status:Unpublished').count()
            extra['viewable_count'] = self.get_results().narrow('item_acces:full OR item_acces:mixed').narrow(
                'digitized:T').count()
            extra['digitized_count'] = self.get_results().narrow('digitized:T').count()
            extra['CDR_count'] = self.get_results().narrow('physical_format:CDR').count()
            extra['Disque_count'] = self.get_results().narrow('physical_format:Disque').count()
            extra['Cylindre_count'] = self.get_results().narrow('physical_format:Cylindre').count()
            extra['Studio_count'] = self.get_results().narrow('recording_context:Studio').count()
            extra['Terrain_count'] = self.get_results().narrow('recording_context:Terrain').count()
            extra['Radio_count'] = self.get_results().narrow('recording_context:Radio').count()
            extra['Video_count'] = self.get_results().narrow('media_type:Video').count()
            extra['Audio_count'] = self.get_results().narrow('media_type:Audio').count()

        if self.type == 'item':
            extra['type'] = 'item'
        elif self.type == 'fonds':
            extra['type'] = 'fonds'
        elif self.type == 'corpus':
            extra['type'] = 'corpus'
        else:
            extra['type'] = 'collection'

        extra['selected_facets'] = self.selected_facet
        extra['selected_facets_url'] = self.request.GET.getlist('selected_facets')
        extra['results_page'] = self.results_per_page
        return extra


class HaystackAdvanceSearch(SavedSearchView):
    search_key = 'advanced'

    def __call__(self, request, type=None):
        self.type = type
        if request.GET.get('results_page'):
            self.results_per_page = int(request.GET.get('results_page'))
        else:
            self.results_per_page = 20
        self.requestURL = re.sub('&page=\d+', '&page=1', request.GET.urlencode())
        return super(HaystackAdvanceSearch, self).__call__(request)

    def get_query(self):
        # overwrite the get_query for begin search with any form
        if self.form.is_valid():
            return self.form.cleaned_data
        return ''

    def get_results(self):
        if (self.type == 'item'):
            return self.form.search().models(MediaItem)
        elif (self.type == 'fonds'):
            return self.form.search().models(MediaFonds)
        elif (self.type == 'corpus'):
            return self.form.search().models(MediaCorpus)
        else:
            return self.form.search().models(MediaCollection)

    def extra_context(self):
        extra = super(HaystackAdvanceSearch, self).extra_context()
        extra['fonds_count'] = self.form.search().models(MediaFonds).count()
        extra['corpus_count'] = self.form.search().models(MediaCorpus).count()
        extra['collection_count'] = self.form.search().models(MediaCollection).count()
        extra['item_count'] = self.form.search().models(MediaItem).count()

        if self.type == 'item':
            extra['type'] = 'item'
        elif self.type == 'fonds':
            extra['type'] = 'fonds'
        elif (self.type == 'corpus'):
            extra['type'] = 'corpus'
        else:
            extra['type'] = 'collection'

        extra['results_page'] = self.results_per_page
        #extra['booleanForm'] = formset_factory(BooleanSearch, extra=2)
        extra['request_url'] = self.requestURL
        return extra


def autocomplete(request):
    attribut = request.GET.get('attr', '')
    sqs = SearchQuerySet().load_all()
    if attribut == "code":
        sqs = sqs.filter(code__contains=request.GET.get('q', ''))
        suggestions = [result.code for result in sqs]

    elif attribut == "collectors":
        sqs = sqs.filter(collectors__startswith=request.GET.get('q', ''))
        collecteurs = [result.collectors for result in sqs]
        suggestions = []
        for chaine in collecteurs:
            for word in chaine.split('; '):
                if word != "" and escape_accent_and_lower(request.GET.get('q', '')) in escape_accent_and_lower(word):
                    suggestions.append(word)
    elif attribut == "location" or attribut == "instruments":
        sqs = SearchQuerySet().using('autocomplete')

        if attribut == "location":
            sqs = sqs.models(Location, LocationAlias)
        else:
            sqs = sqs.models(Instrument, InstrumentAlias)
        sqs = sqs.filter(content__startswith=request.GET.get('q', ''))
        suggestions = [obj.text for obj in sqs]
    else:
        suggestions = []

    if request.GET.get('attr', '') != 'code':
        suggestions = list(set([word.strip().lower().title() for word in suggestions]))
    else:
        suggestions = list(set(suggestions))
    suggestions.sort()

    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')

def escape_accent_and_lower(chaine):
    return unicodedata.normalize('NFD', chaine).encode('ascii', 'ignore').lower()