# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2012 Parisson SARL

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

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *


class GeoView(object):
    """Provide Geo web UI methods"""

    def list_continents(self, request):
        continents = MediaItem.objects.all().countries(group_by_continent=True)
        return render(request, 'telemeta/geo_continents.html',
                    {'continents': continents, 'gmap_key': settings.TELEMETA_GMAP_KEY })

    def country_info(self, request, id):
        country = Location.objects.get(pk=id)
        return render(request, 'telemeta/country_info.html', {
            'country': country, 'continent': country.continents()[0]})

    def list_countries(self, request, continent):
        continent = Location.objects.by_flatname(continent)[0]
        countries = MediaItem.objects.by_location(continent).countries()

        return render(request, 'telemeta/geo_countries.html', {
            'continent': continent,
            'countries': countries
        })

    def list_country_collections(self, request, continent, country):
        continent = Location.objects.by_flatname(continent)[0]
        country = Location.objects.by_flatname(country)[0]
        objects = MediaCollection.objects.enriched().by_location(country)
        return list_detail.object_list(request, objects,
            template_name='telemeta/geo_country_collections.html', paginate_by=20,
            extra_context={'country': country, 'continent': continent})

    def list_country_items(self, request, continent, country):
        continent = Location.objects.by_flatname(continent)[0]
        country = Location.objects.by_flatname(country)[0]
        objects = MediaItem.objects.enriched().by_location(country)
        return list_detail.object_list(request, objects,
            template_name='telemeta/geo_country_items.html', paginate_by=20,
            extra_context={'country': country, 'continent': continent})


class GeoCountryCollectionView(ListView):

    model = MediaCollection
    template_name = 'telemeta/geo_country_collections.html'
    paginate_by = 20

    def get_queryset(self):
        country = self.kwargs['country']
        continent = self.kwargs['continent']
        self.continent = Location.objects.by_flatname(continent)[0]
        self.country = Location.objects.by_flatname(country)[0]
        return MediaCollection.objects.enriched().by_location(self.country)

    def get_context_data(self, *args, **kwargs):
        context = super(GeoCountryCollectionView, self).get_context_data(*args, **kwargs)
        context['country'] = self.country
        context['continent'] =  self.continent
        context['count'] = self.object_list.count()
        return context


class GeoCountryItemView(ListView):

    model = MediaItem
    template_name = 'telemeta/geo_country_items.html'
    paginate_by = 20

    def get_queryset(self):
        country = self.kwargs['country']
        continent = self.kwargs['continent']
        self.continent = Location.objects.by_flatname(continent)[0]
        self.country = Location.objects.by_flatname(country)[0]
        return MediaItem.objects.enriched().by_location(self.country)

    def get_context_data(self, *args, **kwargs):
        context = super(GeoCountryItemView, self).get_context_data(*args, **kwargs)
        context['country'] = self.country
        context['continent'] =  self.continent
        context['count'] = self.object_list.count()
        return context


