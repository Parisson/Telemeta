# -*- coding: utf-8 -*-
from telemeta.models import *
from haystack.forms import *
from haystack.query import SearchQuerySet


class HaySearchForm(FacetedSearchForm):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'text'}))
    def search(self):
        sqs = SearchQuerySet().load_all()

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            sqs = sqs.filter(content__contains=self.cleaned_data['q']).facet('item_acces').facet('item_status').facet('digitized').facet('recording_context').facet('physical_format').facet('media_type')

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
#begin create field

    #to replace de basic search form field
    q = forms.CharField(required=False, label=('Title'), widget=forms.TextInput(attrs={'type': 'search'}))

    code = forms.CharField(required=False, label=('Code'), widget=forms.TextInput(attrs={'type': 'search'}))
    location = forms.CharField(required=False, label=('Location'), widget=forms.TextInput(attrs={'type': 'search'}))

    # to create a dynamic list of ethnic group
    def list_ethnic_group():
        type_name = []
        type_name.append(('', 'no preference'))
        list_ethnic_group = EthnicGroup.objects.all()
        for ethnic in list_ethnic_group:
            type_name.append((ethnic.value, ethnic.value))
        return type_name

    ethnic_group = forms.CharField(required=False, label=('Population / social group'), widget=forms.Select(choices=list_ethnic_group()))

    instruments = forms.CharField(required=False, label=('Instruments'), widget=forms.TextInput(attrs={'type': 'search'}))
    collectors = forms.CharField(required=False, label=('Depositor / contributor'), widget=forms.TextInput(attrs={'type': 'search'}))
    recorded_from_date = forms.DateField(required=False, label=('Recorded from'), widget=forms.DateInput(attrs={'type': 'search', 'placeholder': 'MM/DD/YYYY'}))
    recorded_to_date = forms.DateField(required=False, label=('Recorded to'), widget=forms.DateInput(attrs={'type': 'search', 'placeholder': 'MM/DD/YYYY'}))

    #to create a dynamic list of publish year
    def list_publish_year():
        list_all_year = []
        list_collect = MediaCollection.objects.all()
        for collect in list_collect:
            if collect.year_published != '0' and not collect.year_published in list_all_year:
                list_all_year.append(collect.year_published)
        list_all_year.sort()
        if len(list_all_year) >= 2:
            min_year = list_all_year[len(list_all_year) - 1]
            max_year = list_all_year[len(list_all_year) - 1]
            for year in list_all_year:
                if year != 0:
                    if year < min_year:
                        min_year = year
                    if year > max_year:
                        max_year = year
            list_all_year = range(min_year, max_year + 1)
        list_year = []
        list_year.append((0, ''))
        for year in list_all_year:
            list_year.append((year, year))
        return list_year

    year_published_from = forms.IntegerField(required=False, label=('Year published from'), widget=forms.Select(choices=list_publish_year()))
    year_published_to = forms.IntegerField(required=False, label=('Year published to'), widget=forms.Select(choices=list_publish_year()))
    #year_published_from = forms.IntegerField(required=False, label=('Year published from'), widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'YYYY', 'pattern': '[0-9]{4}'}))
    #year_published_to = forms.IntegerField(required=False, label=('Year published to'), widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'YYYY', 'pattern': '[0-9]{4}'}))
    viewable = forms.BooleanField(required=False, label=('Viewable'))

    item_status = forms.CharField(required=False, label=('Item Status'), widget=forms.RadioSelect(choices=(('1', 'no preference'), ('pub', 'Published'), ('unpub', 'Unpublished'))), initial=1)

    #to create a dynamic list of media type
    def list_media_type():
        type_name = []
        type_name.append(('1', 'no preference'))
        type_name.append(('dig', 'Digitized'))
        list_media_type = MediaType.objects.all()
        for mt in list_media_type:
            type_name.append((mt.value, mt.value))
        return type_name

    media_type = forms.CharField(required=False, label=('Media'), widget=forms.RadioSelect(choices=(list_media_type())), initial=1)

    #to create a dynamic list of recording context
    def list_recording_context():
        type_name = []
        type_name.append(('', 'no preference'))
        list_recording_context = RecordingContext.objects.all()
        for context in list_recording_context:
            type_name.append((context.value, context.value))
        return type_name

    recording_context = forms.CharField(required=False, label=('Recording Context'), widget=forms.Select(choices=list_recording_context()))

    #to create a dynamic list of physical format
    def list_physical_format():
        type_name = []
        type_name.append(('', 'no preference'))
        list_physical_format = PhysicalFormat.objects.all()
        for physical_format in list_physical_format:
            type_name.append((physical_format.value, physical_format.value))
        return type_name

    physical_format = forms.CharField(required=False, label=('Physical Format'), widget=forms.Select(choices=list_physical_format()))
#end

    def search(self):
        sqs = SearchQuerySet().load_all()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data.get('q'):
            sqs = sqs.filter(title__contains=self.cleaned_data['q'])

        if self.cleaned_data.get('code'):
            sqs = sqs.filter(code__contains=self.cleaned_data['code'])

        if self.cleaned_data.get('location'):
            sqs = sqs.filter(location__contains=self.cleaned_data['location'])

        if self.cleaned_data['ethnic_group']:
            if self.cleaned_data.get('ethnic_group') != '':
                sqs = sqs.filter(ethnic_group__contains=self.cleaned_data['ethnic_group'])

        if self.cleaned_data.get('instruments'):
            sqs = sqs.filter(instruments__contains=self.cleaned_data['instruments'])

        if self.cleaned_data.get('collectors'):
            sqs = sqs.filter(collectors__contains=self.cleaned_data['collectors'])

        if self.cleaned_data['recorded_from_date']:
            sqs = sqs.filter(recorded_from_date__gte=self.cleaned_data['recorded_from_date'])

        if self.cleaned_data['recorded_to_date']:
            sqs = sqs.filter(recorded_to_date__lte=self.cleaned_data['recorded_to_date'])

        if self.cleaned_data['year_published_from']:
            sqs = sqs.filter(year_published__gte=self.cleaned_data['year_published_from'])

        if self.cleaned_data['year_published_to']:
            sqs = sqs.filter(year_published__lte=self.cleaned_data['year_published_to'])

        if self.cleaned_data['viewable']:
            sqs = sqs.filter(Q(item_acces='full') | Q(item_acces='mixed'))

        if self.cleaned_data['item_status']:
            if self.cleaned_data.get('item_status') == 'pub':
                sqs = sqs = sqs.filter(item_status='Published')
            if self.cleaned_data.get('item_status') == 'unpub':
                sqs = sqs = sqs.filter(item_status='Unpublished')

        if self.cleaned_data['media_type']:
            if self.cleaned_data.get('media_type') != '1':
                if self.cleaned_data.get('media_type') == 'dig':
                    sqs = sqs.filter(digitized=True)
                else:
                    sqs = sqs.filter(digitized=True).filter(media_type=self.cleaned_data['media_type'])

        if self.cleaned_data['recording_context']:
            if self.cleaned_data.get('recording_context') != '':
                sqs = sqs.filter(recording_context=self.cleaned_data['recording_context'])

        if self.cleaned_data['physical_format']:
            if self.cleaned_data.get('physical_formate') != '':
                sqs = sqs.filter(physical_format=self.cleaned_data['physical_format'])

        return sqs
