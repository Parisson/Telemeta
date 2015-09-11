# -*- coding: utf-8 -*-
from telemeta.views.core import *

class SearchViewPublished(ListView):
    """Perform a search through resources"""

    template_name='telemeta/search_results.html'
    paginate_by = 20

    def get_queryset(self):
        input = self.request.GET
        self.criteria = {}

        self.type = None
        if 'type' in self.kwargs:
            self.type = self.kwargs['type']

        self.collections = MediaCollection.objects.enriched()
        self.items = MediaItem.objects.enriched().filter(code__contains="_E_")
        self.corpus = MediaCorpus.objects.all()
        self.fonds  = MediaFonds.objects.all()

        switch = {
            'pattern': lambda value: (
                self.collections.quick_search(value),
                self.items.quick_search(value),
                self.corpus.quick_search(value),
                self.fonds.quick_search(value),
                ),
            'title': lambda value: (
                self.collections.word_search('title', value),
                self.items.by_title(value),
                self.corpus.word_search('title', value),
                self.fonds.word_search('title', value)),
            'location': lambda value: (
                self.collections.by_location(Location.objects.get(name=value)),
                self.items.by_location(Location.objects.get(name=value))),
            'continent': lambda value: (
                self.collections.by_continent(value),
                self.items.filter(continent = value)),
            'ethnic_group': lambda value: (
                self.collections.by_ethnic_group(value),
                self.items.filter(ethnic_group = value),
                EthnicGroup.objects.get(pk=value)),
            'creator': lambda value: (
                self.collections.word_search('creator', value),
                self.items.word_search('collection__creator', value)),
            'collector': lambda value: (
                self.collections.by_fuzzy_collector(value),
                self.items.by_fuzzy_collector(value)),
            'rec_year_from': lambda value: (
                self.collections.by_recording_year(int(value), int(input.get('rec_year_to', value))),
                self.items.by_recording_date(datetime.date(int(value), 1, 1),
                                        datetime.date(int(input.get('rec_year_to', value)), 12, 31))),
            'rec_year_to': lambda value: (self.collections, self.items),
            'pub_year_from': lambda value: (
                self.collections.by_publish_year(int(value), int(input.get('pub_year_to', value))),
                self.items.by_publish_year(int(value), int(input.get('pub_year_to', value)))),
            'pub_year_to': lambda value: (self.collections, self.items),
            'sound': lambda value: (
                self.collections.sound(),
                self.items.sound()),
            'instrument': lambda value: (
                self.collections.by_instrument(value),
                self.items.by_instrument(value)),
        }

        for key, value in input.items():
            func = switch.get(key)
            if func and value and value != "0":
                try:
                    res = func(value)
                    if len(res)  > 4:
                        self.collections, self.items, self.corpus, self.fonds, value = res
                    elif len(res) == 4:
                        self.collections, self.items, self.corpus, self.fonds = res
                    elif len(res) == 3:
                        self.collections, self.items, value = res
                        self.corpus = self.corpus.none()
                        self.fonds = self.fonds.none()
                    else:
                        self.collections, self.items = res
                        self.corpus = self.corpus.none()
                        self.fonds = self.fonds.none()

                except ObjectDoesNotExist:
                    self.collections = self.collections.none()
                    self.items = self.items.none()
                    self.corpus = self.corpus.none()
                    self.fonds = self.fonds.none()

                self.criteria[key] = value

        # Save the search
        user = self.request.user
        if user:
            if user.is_authenticated():
                search = Search(username=user)
                search.save()
                if self.criteria:
                    for key in self.criteria.keys():
                        value = self.criteria[key]
                        if key == 'ethnic_group':
                            try:
                                group = EthnicGroup.objects.get(value=value)
                                value = group.id
                            except:
                                value = ''
                        criter = Criteria(key=key, value=value)
                        criter.save()
                        search.criteria.add(criter)
                    search.save()

        if self.type is None:
            if self.collections.count():
                self.type = 'collections'
            else:
                self.type = 'items'

        if self.type == 'items':
            objects = self.items
        elif self.type == 'collections':
            objects = self.collections
        elif self.type == 'corpus':
            objects = self.corpus
        elif self.type == 'fonds':
            objects = self.fonds

        self.objects = objects
        return objects

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['criteria'] = self.criteria
        context['collections_num'] =  self.collections.count()
        context['items_num'] = self.items.count()
        context['corpus_num']  = self.corpus.count()
        context['fonds_num'] = self.fonds.count()
        context['type'] = self.type
        context['count'] = self.object_list.count()
        return context