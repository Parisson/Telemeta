# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2012 Parisson SARL

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

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *


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
            return render(request, 'telemeta/messages.html', {'description' : description})

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
                'parents': parents, 'last_revision': last_revision })

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

        return render(request, template, {'collection': collection, "form": form,})

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

        return render(request, template, {'collection': collection, "form": form,})

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

        return render(request, template, {'collection': collection, "form": form,})

    def collection_playlist(self, request, public_id, template, mimetype):
        try:
            collection = MediaCollection.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'collection': collection, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    @method_decorator(permission_required('telemeta.delete_mediacollection'))
    def collection_delete(self, request, public_id):
        """Delete a given collection"""
        collection = MediaCollection.objects.get(public_id=public_id)
        revisions = Revision.objects.filter(element_type='collection', element_id=collection.id)
        for revision in revisions:
            revision.delete()
        collection.delete()
        return redirect('telemeta-collections')

    def related_media_collection_stream(self, request, collection_public_id, media_id):
        collection = MediaCollection.objects.get(public_id=collection_public_id)
        media = MediaCollectionRelated.objects.get(collection=collection, id=media_id)
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
#        response['Content-Disposition'] = 'attachment'
        return response

    def related_media_collection_download(self, request, collection_public_id, media_id):
        collection = MediaCollection.objects.get(public_id=collection_public_id)
        media = MediaCollectionRelated.objects.get(collection=collection, id=media_id)
        filename = media.file.path.split(os.sep)[-1]
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
        response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename
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

        return render(request, template, {'collection': collection, 'formset': formset,})


class CollectionPackageView(View):

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
        from telemeta.util import zipstream
        import json

        z = zipstream.ZipFile()
        cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)

        collection = self.get_object()
        serializer = CollectionSerializer(collection)

        data = serializer.get_xml().encode("utf-8")
        filename = collection.public_id + '.xml'
        cache_data.write_bin(data, filename)
        path = cache_data.dir + os.sep + filename
        z.write(path, arcname=collection.public_id + os.sep + filename)

        for item in collection.items.all():
            filename, ext = os.path.splitext(item.file.path.split(os.sep)[-1])
            z.write(item.file.path, arcname=collection.public_id + os.sep + item.code + ext)
            marker_view = MarkerView()
            markers = marker_view.get_markers(item.id)
            if markers:
                data = json.dumps(markers)
                filename = item.code + '.json'
                cache_data.write_bin(data, filename)
                path = cache_data.dir + os.sep + filename
                z.write(path, arcname=collection.public_id + os.sep + filename)

        try:
            from django.http import StreamingHttpResponse
            response = StreamingHttpResponse(z, content_type='application/zip')
        except:
            response = HttpResponse(z, content_type='application/zip')

        response['Content-Disposition'] = "attachment; filename=%s.%s" % \
                                             (collection.code, 'zip')
        return response

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CollectionPackageView, self).dispatch(*args, **kwargs)


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
                                            element_id=collection.id).order_by('-time')
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

    def form_valid(self, form):
        messages.info(self.request, _("You have successfully updated your collection."))
        return super(CollectionEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('telemeta-collection-detail', kwargs={'public_id':self.kwargs['public_id']})

    def get_context_data(self, **kwargs):
        context = super(CollectionEditView, self).get_context_data(**kwargs)
        collection = self.get_object()
        context['collection'] = collection
        return context


class CollectionAddView(CollectionViewMixin, CreateWithInlinesView):

    template_name = 'telemeta/collection_add.html'
    inlines = [CollectionRelatedInline, CollectionIdentifierInline]

    def get_success_url(self):
        return reverse_lazy('telemeta-collection-detail', kwargs={'public_id':self.object.code})


class CollectionCopyView(CollectionAddView):

    template_name = 'telemeta/collection_edit.html'

    def get_initial(self):
        return model_to_dict(self.get_object())

    def get_success_url(self):
        return reverse_lazy('telemeta-collection-detail', kwargs={'public_id':self.object.code})

    def get_context_data(self, **kwargs):
        context = super(CollectionCopyView, self).get_context_data(**kwargs)
        collection = self.get_object()
        context['collection'] = collection
        return context