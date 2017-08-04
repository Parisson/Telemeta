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
import telemeta

from telemeta.views.core import *
from telemeta.views.core import serve_media
from telemeta.views.epub import *

class CollectionView(object):
    """Provide Collections web UI methods"""

    def collection_detail(self, request, public_id, template='telemeta/collection_detail.html'):
        collection = MediaCollection.objects.get(public_id=public_id)
        items = collection.items.enriched()
        items = items.order_by('code', 'old_code')

        if collection.public_access == 'none' and not (request.user.is_staff or request.user.is_superuser):
            mess = ugettext('Access not allowed')
            title = ugettext('Collection') + ' : ' + public_id + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description': description})

        playlists = get_playlists_names(request)

        related_media = MediaCollectionRelated.objects.filter(collection=collection)
        check_related_media(related_media)
        parents = MediaCorpus.objects.filter(children=collection)
        revisions = Revision.objects.filter(element_type='collection',
                                            element_id=collection.id).order_by('-time')
        if revisions:
            last_revision = revisions[0]
        else:
            last_revision = None

        return render(request, template, {'collection': collection, 'playlists': playlists,
                                          'items': items, 'related_media': related_media,
                                          'parents': parents, 'last_revision': last_revision})

    @method_decorator(permission_required('telemeta.change_mediacollection'))
    def collection_edit(self, request, public_id, template='telemeta/collection_edit.html'):
        collection = MediaCollection.objects.get(public_id=public_id)
        if request.method == 'POST':
            form = MediaCollectionForm(data=request.POST, files=request.FILES, instance=collection)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                collection.set_revision(request.user)
                return redirect('telemeta-collection-detail', code)
        else:
            form = MediaCollectionForm(instance=collection)

        return render(request, template, {'collection': collection, "form": form, })

    @method_decorator(permission_required('telemeta.add_mediacollection'))
    def collection_add(self, request, template='telemeta/collection_add.html'):
        collection = MediaCollection()
        if request.method == 'POST':
            form = MediaCollectionForm(data=request.POST, files=request.FILES, instance=collection)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                collection.set_revision(request.user)
                return redirect('telemeta-collection-detail', code)
        else:
            form = MediaCollectionForm(instance=collection)

        return render(request, template, {'collection': collection, "form": form, })

    @method_decorator(permission_required('telemeta.add_mediacollection'))
    def collection_copy(self, request, public_id, template='telemeta/collection_edit.html'):
        if request.method == 'POST':
            collection = MediaCollection()
            form = MediaCollectionForm(data=request.POST, files=request.FILES, instance=collection)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                collection.set_revision(request.user)
                return redirect('telemeta-collection-detail', code)
        else:
            collection = MediaCollection.objects.get(public_id=public_id)
            form = MediaCollectionForm(instance=collection)

        return render(request, template, {'collection': collection, "form": form, })

    def collection_playlist(self, request, public_id, template, mimetype):
        try:
            collection = MediaCollection.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'collection': collection, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), content_type=mimetype)

    @method_decorator(permission_required('telemeta.delete_mediacollection'))
    def collection_delete(self, request, public_id):
        """Delete a given collection"""
        collection = MediaCollection.objects.get(public_id=public_id)
        revisions = Revision.objects.filter(element_type='collection', element_id=collection.id)
        for revision in revisions:
            revision.delete()
        collection.delete()
        return redirect('telemeta-collections')

    def related_media_collection_stream(self, request, public_id, media_id):
        collection = MediaCollection.objects.get(public_id=public_id)
        media = MediaCollectionRelated.objects.get(collection=collection, id=media_id)
        response = serve_media(media.file.path, content_type=media.mime_type)
        return response

    def related_media_collection_download(self, request, public_id, media_id):
        collection = MediaCollection.objects.get(public_id=public_id)
        media = MediaCollectionRelated.objects.get(collection=collection, id=media_id)
        response = serve_media(media.file.path, content_type=media.mime_type)
        return response

    @method_decorator(permission_required('telemeta.change_mediacollection'))
    def related_media_edit(self, request, public_id, template):
        collection = MediaCollection.objects.get(public_id=public_id)
        MediaCollectionRelatedFormSet = inlineformset_factory(MediaCollection, MediaCollectionRelated, form=MediaCollectionRelatedForm)
        if request.method == 'POST':
            formset = MediaCollectionRelatedFormSet(data=request.POST, files=request.FILES, instance=collection)
            if formset.is_valid():
                formset.save()
                collection.set_revision(request.user)
                return redirect('telemeta-collection-edit', public_id)
        else:
            formset = MediaCollectionRelatedFormSet(instance=collection)

        return render(request, template, {'collection': collection, 'formset': formset, })


class CollectionZipView(View):

    model = MediaCollection

    def get_object(self):
        return MediaCollection.objects.get(public_id=self.kwargs['public_id'])

    def get(self, request, *args, **kwargs):
        """
        Stream a ZIP file of collection data
        without loading the whole file into memory.
        Based on ZipStream
        """
        from telemeta.views import MarkerView
        from telemeta.backup import CollectionSerializer
        import zipstream
        from zipfile import ZIP_DEFLATED, ZIP_STORED
        import json

        zip_file = zipstream.ZipFile(mode='w', compression=ZIP_STORED,
                                     allowZip64=True)
        cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)

        collection = self.get_object()
        serializer = CollectionSerializer(collection)

        data = collection.get_json().encode('utf-8')
        filename = collection.public_id + '.json'
        cache_data.write_bin(data, filename)
        path = cache_data.dir + os.sep + filename
        zip_file.write(path, arcname=collection.public_id + os.sep + filename)

        data = serializer.get_xml().encode('utf-8')
        filename = collection.public_id + '.xml'
        cache_data.write_bin(data, filename)
        path = cache_data.dir + os.sep + filename
        zip_file.write(path, arcname=collection.public_id + os.sep + filename)

        for item in collection.items.all():
            if item.file:
                filename, ext = os.path.splitext(item.file.path.split(os.sep)[-1])
                zip_file.write(item.file.path, arcname=collection.public_id + os.sep + item.code + ext)
            marker_view = MarkerView()
            markers = marker_view.get_markers(item.id)
            if markers:
                data = json.dumps(markers)
                filename = item.code + '.json'
                cache_data.write_bin(data, filename)
                path = cache_data.dir + os.sep + filename
                zip_file.write(path, arcname=collection.public_id + os.sep + filename)

        response = StreamingHttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = "attachment; filename=%s.%s" % \
            (collection.code, 'zip')
        return response

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CollectionZipView, self).dispatch(*args, **kwargs)


class CollectionViewMixin(object):

    model = MediaCollection
    form_class = MediaCollectionForm

    def get_object(self):
        obj = self.model.objects.filter(code=self.kwargs['public_id'])
        if not obj:
            if self.kwargs['public_id'].isdigit():
                try:
                    obj = self.model.objects.get(id=self.kwargs['public_id'])
                except self.model.DoesNotExist:
                    raise Http404
            else:
                raise Http404
        else:
            obj = obj[0]
        return obj


class CollectionListView(ListView):

    model = MediaCollection
    template_name = "telemeta/collection_list.html"
    paginate_by = 20
    queryset = MediaCollection.objects.enriched()

    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        context['count'] = self.object_list.count()
        return context


class CollectionUnpublishedListView(CollectionListView):

    queryset = MediaCollection.objects.filter(code__contains='_I_')


class CollectionPublishedListView(CollectionListView):

    queryset = MediaCollection.objects.filter(code__contains='_E_')


class CollectionSoundListView(CollectionListView):

    queryset = MediaCollection.objects.sound().order_by('code', 'old_code')


class CollectionDetailView(CollectionViewMixin, DetailView):

    template_name = 'telemeta/collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)
        collection = self.get_object()
        items = collection.items.enriched()
        context['collection'] = collection
        context['items'] = items.order_by('code', 'old_code')
        context['playlists'] = get_playlists_names(self.request)
        context['related_media'] = MediaCollectionRelated.objects.filter(collection=collection)
        check_related_media(context['related_media'])
        context['parents'] = MediaCorpus.objects.filter(children=collection)
        revisions = Revision.objects.filter(element_type='collection',
                                            element_id=collection.id)
        if revisions:
            context['last_revision'] = revisions[0]
        else:
            context['last_revision'] = None

        return context


class CollectionDetailViewDC(CollectionDetailView):

    template_name = "telemeta/collection_detail_dc.html"


class CollectionEditView(CollectionViewMixin, UpdateWithInlinesView):

    template_name = 'telemeta/collection_edit.html'
    inlines = [CollectionRelatedInline, CollectionIdentifierInline]

    def forms_valid(self, form, inlines):
        messages.info(self.request, ugettext_lazy("You have successfully updated your collection."))
        obj = form.save()
        obj.set_revision(self.request.user)
        self.code = obj.code
        return super(CollectionEditView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('telemeta-collection-detail', kwargs={'public_id': self.code})

    def get_context_data(self, **kwargs):
        context = super(CollectionEditView, self).get_context_data(**kwargs)
        collection = self.get_object()
        context['collection'] = collection
        return context

    @method_decorator(permission_required('telemeta.change_mediacollection'))
    def dispatch(self, *args, **kwargs):
        return super(CollectionEditView, self).dispatch(*args, **kwargs)


class CollectionAddView(CollectionViewMixin, CreateWithInlinesView):

    template_name = 'telemeta/collection_add.html'
    inlines = [CollectionRelatedInline, CollectionIdentifierInline]

    def forms_valid(self, form, inlines):
        messages.info(self.request, ugettext_lazy("You have successfully added your collection."))
        obj = form.save()
        obj.set_revision(self.request.user)
        return super(CollectionAddView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('telemeta-collection-detail', kwargs={'public_id': self.object.code})

    @method_decorator(permission_required('telemeta.add_mediacollection'))
    def dispatch(self, *args, **kwargs):
        return super(CollectionAddView, self).dispatch(*args, **kwargs)


class CollectionCopyView(CollectionAddView):

    template_name = 'telemeta/collection_edit.html'

    def get_initial(self):
        return model_to_dict(self.get_object())

    def get_context_data(self, **kwargs):
        context = super(CollectionCopyView, self).get_context_data(**kwargs)
        collection = self.get_object()
        context['collection'] = collection
        return context

    @method_decorator(permission_required('telemeta.add_mediacollection'))
    def dispatch(self, *args, **kwargs):
        return super(CollectionCopyView, self).dispatch(*args, **kwargs)


class CollectionEpubView(BaseEpubMixin, View):
    "Download collection data embedded in an EPUB3 file"

    model = MediaCollection

    def get_object(self):
        return MediaCollection.objects.get(public_id=self.kwargs['public_id'])

    def get(self, request, *args, **kwargs):
        collection = self.get_object()
        corpus = collection.corpus.all()[0]
        self.setup_epub(corpus, collection=collection)
        if not os.path.exists(self.path):
            self.write_book()
        epub_file = open(self.path, 'rb')
        response = HttpResponse(epub_file.read(), content_type='application/epub+zip')
        response['Content-Disposition'] = "attachment; filename=%s" % self.filename + '.epub'
        return response

    # @method_decorator(login_required)
    # @method_decorator(permission_required('telemeta.can_download_collection_epub'))
    def dispatch(self, *args, **kwargs):
        return super(CollectionEpubView, self).dispatch(*args, **kwargs)


class CollectionEnumListView(CollectionListView):
    template_name = "telemeta/collection_enum_list.html"


    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        context['enum']=self.request.path[20:-6].split('/')[0]
        context['id']=self.request.path[20:-6].split('/')[1]
        context['count'] = self.object_list.count()
        context['enum_name'] = CollectionEnumListView().get_enumeration(self.request.path.split('/')[3])._meta.verbose_name
        context['enum_value'] = CollectionEnumListView().get_enumeration(self.request.path.split('/')[3]).objects.get(id__exact=self.request.path.split('/')[4])
        return context

    def get_queryset(self):
        enumeration = self.get_enumeration(self.request.path[20:-6].split('/')[0])
        queryset= self.get_coll(enumeration.objects.filter(id=self.request.path[20:-6].split('/')[1]).get())
        return queryset

    def get_coll(self, enum):
        f = MediaCollection._meta.get_all_field_names()
        for field in f:
            if field in enum._meta.db_table.replace(" ", "_"):
                atr = field;
        atr = atr
        lookup = "%s__exact" % atr
        return MediaCollection.objects.filter(**{lookup: enum.__getattribute__("id")})

    def get_enumeration(self,id):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if model._meta.module_name == id:
                break

        if model._meta.module_name != id:
            return None
        return model


class CollectionPublishedEnumListView(CollectionEnumListView):

    def get_queryset(self):
        c = CollectionEnumListView()
        #id of value of enumeration
        i= self.request.path.split('/')[4]
        enumeration = c.get_enumeration(self.request.path.split('/')[3])
        queryset = self.get_coll(enumeration.objects.filter(id=i).get(), c)
        return queryset

    def get_coll(self, enum,c):
        return c.get_coll(enum).filter(code__contains='_E_')


class CollectionUnpublishedEnumListView(CollectionEnumListView):

    def get_queryset(self):
        c = CollectionEnumListView()
        #id of value of enumeration
        i= self.request.path.split('/')[4]
        enumeration = c.get_enumeration( self.request.path.split('/')[3])
        queryset = self.get_coll(enumeration.objects.filter(id=i).get(), c)
        return queryset

    def get_coll(self, enum, c):
        return c.get_coll(enum).filter(code__contains='_I_')


class CollectionSoundEnumListView(CollectionEnumListView):
    def get_queryset(self):
        c = CollectionEnumListView()
        #id of value of enumeration
        i= self.request.path.split('/')[4]
        enumeration = c.get_enumeration( self.request.path.split('/')[3])
        queryset = self.get_coll(enumeration.objects.filter(id=i).get(), c)
        return queryset

    def get_coll(self, enum,c):
        return c.get_coll(enum).sound().order_by('code', 'old_code')
