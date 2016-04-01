# -*- coding: utf-8 -*-

# Copyright (C) 2010-2015 Parisson SARL
# Copyright (C) 2007-2010 Samalyse SARL

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
from telemeta.views.marker import *
import timeside.core


class ItemBaseMixin(TelemetaBaseMixin):

    graphers = timeside.core.processor.processors(timeside.core.api.IGrapher)
    decoders = timeside.core.processor.processors(timeside.core.api.IDecoder)
    encoders = timeside.core.processor.processors(timeside.core.api.IEncoder)
    analyzers = timeside.core.processor.processors(timeside.core.api.IAnalyzer)
    value_analyzers = timeside.core.processor.processors(timeside.core.api.IValueAnalyzer)

    export_enabled = getattr(settings, 'TELEMETA_DOWNLOAD_ENABLED', True)
    export_formats = getattr(settings, 'TELEMETA_DOWNLOAD_FORMATS', ('mp3', 'wav'))
    default_grapher_id = getattr(settings, 'TIMESIDE_DEFAULT_GRAPHER_ID', ('waveform_simple'))
    default_grapher_sizes = getattr(settings, 'TIMESIDE_DEFAULT_GRAPHER_SIZES', ['346x130', ])
    auto_zoom = getattr(settings, 'TIMESIDE_AUTO_ZOOM', False)

    def get_export_formats(self):
        formats = []
        for encoder in self.encoders:
            if encoder.file_extension() in self.export_formats:
                formats.append({'name': encoder.format(),
                                    'extension': encoder.file_extension()})
        return formats

    def get_graphers(self):
        graphers = []
        for grapher in self.graphers:
            if grapher.id() == self.default_grapher_id:
                graphers.insert(0, {'name':grapher.name(), 'id': grapher.id()})
            elif not hasattr(grapher, '_staging'):
                graphers.append({'name':grapher.name(), 'id': grapher.id()})
            elif not grapher._staging:
                graphers.append({'name':grapher.name(), 'id': grapher.id()})
        return graphers

    def get_grapher(self, id):
        for grapher in self.graphers:
            if grapher.id() == id:
                break
        return grapher

    def get_export_formats(self):
        formats = []
        for encoder in self.encoders:
            if encoder.file_extension() in self.export_formats:
                formats.append({'name': encoder.format(),
                                    'extension': encoder.file_extension()})
        return formats

    def item_previous_next(self, item):
        """Get previous and next items inside the collection of the item"""

        pks = []
        items = MediaItem.objects.filter(collection=item.collection)
        items = items.order_by('code', 'old_code')

        if len(items) > 1:
            for it in items:
                pks.append(it.pk)
            for pk in pks:
                if pk == item.pk:
                    if pk == pks[0]:
                        previous_pk = pks[-1]
                        next_pk = pks[1]
                    elif pk == pks[-1]:
                        previous_pk = pks[-2]
                        next_pk = pks[0]
                    else:
                        previous_pk = pks[pks.index(pk)-1]
                        next_pk = pks[pks.index(pk)+1]
                    for it in items:
                        if it.pk == previous_pk:
                            previous = it
                        if it.pk == next_pk:
                            next = it
                    previous = previous.public_id
                    next = next.public_id
        else:
             previous = item.public_id
             next = item.public_id
        return previous, next


class ItemView(ItemBaseMixin):
    """Provide Item web UI methods"""

    def item_detail(self, request, public_id=None, marker_id=None, width=None, height=None,
                        template='telemeta/mediaitem_detail.html'):
        """Show the details of a given item"""

        # get item with one of its given marker_id
        if not public_id and marker_id:
            marker = get_object_or_404(MediaItemMarker, public_id=marker_id)
            item_id = marker.item_id
            item = MediaItem.objects.get(id=item_id)
        else:
            item = get_object_or_404(MediaItem, public_id=public_id)

        access = get_item_access(item, request.user)

        if access == 'none':
            mess = ugettext('Access not allowed')
            title = ugettext('Item') + ' : ' + public_id + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        previous, next = self.item_previous_next(item)

        mime_type = item.mime_type
        if mime_type and mime_type != 'none' :
            if 'quicktime' in mime_type:
                mime_type = 'video/mp4'

        playlists = get_playlists_names(request)
        related_media = MediaItemRelated.objects.filter(item=item)
        check_related_media(related_media)
        revisions = Revision.objects.filter(element_type='item', element_id=item.id).order_by('-time')
        if revisions:
            last_revision = revisions[0]
        else:
            last_revision = None

        format = ''
        if Format.objects.filter(item=item):
            format = item.format.get()

        return render(request, template,
                    {'item': item, 'export_formats': self.get_export_formats(),
                    'visualizers': self.get_graphers(), 'auto_zoom': self.auto_zoom,
                    'audio_export_enabled': self.export_enabled,
                    'previous' : previous, 'next' : next, 'marker': marker_id, 'playlists' : playlists,
                    'access': access, 'width': width, 'height': height,
                    'related_media': related_media, 'mime_type': mime_type, 'last_revision': last_revision,
                    'format': format,
                    })

    def related_media_item_stream(self, request, item_public_id, media_id):
        item = get_object_or_404(MediaItem, code=item_public_id)
        media = get_object_or_404(MediaItemRelated, item=item, id=media_id)
        if media.file:
            response = StreamingHttpResponse(stream_from_file(media.file.path), content_type=media.mime_type)
        else:
            raise Http404
        return response

    def related_media_item_download(self, request, item_public_id, media_id):
        item = get_object_or_404(MediaItem, code=item_public_id)
        media = get_object_or_404(MediaItemRelated, item=item, id=media_id)
        if media.file:
            filename = media.file.path.split(os.sep)[-1]
            response = StreamingHttpResponse(stream_from_file(media.file.path), content_type=media.mime_type)
            response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename
        else:
            raise Http404
        return response

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def related_media_edit(self, request, public_id, template):
        item = get_object_or_404(MediaItem, code=public_id)
        MediaItemRelatedFormSet = inlineformset_factory(MediaItem, MediaItemRelated, form=MediaItemRelatedForm)
        if request.method == 'POST':
            formset = MediaItemRelatedFormSet(data=request.POST, files=request.FILES, instance=item)
            if formset.is_valid():
                formset.save()
                item.set_revision(request.user)
                return redirect('telemeta-item-edit', public_id)
        else:
            formset = MediaItemRelatedFormSet(instance=item)
        return render(request, template, {'item': item, 'formset': formset,})


    @method_decorator(permission_required('telemeta.delete_mediaitem'))
    def item_delete(self, request, public_id):
        """Delete a given item"""
        item = MediaItem.objects.get(public_id=public_id)
        revisions = Revision.objects.filter(element_type='item', element_id=item.id)
        for revision in revisions:
            revision.delete()
        collection = item.collection
        item.delete()
        return redirect('telemeta-collection-detail', collection.code)

    def item_analyze_xml(self, request, public_id):
        item = MediaItem.objects.get(public_id=public_id)
        analyses = item.analysis.all()
        analyzers = []
        for analysis in analyses:
            analyzers.append(analysis.to_dict())
        mime_type = 'text/xml'
        response = HttpResponse(self.cache_data.get_analyzer_xml(analyzers), content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename='+public_id+'.xml'
        return response

    def item_visualize(self, request, public_id, grapher_id, width, height):
        try:
            width = int(width)
            height = int(height)
        except:
            pass

        if not isinstance(width, int) or not isinstance(height, int):
            size = self.default_grapher_sizes[0]
            width = int(size.split('x')[0])
            height = int(size.split('x')[1])

        item = MediaItem.objects.get(public_id=public_id)
        mime_type = 'image/png'
        grapher = self.get_grapher(grapher_id)

        if grapher.id() != grapher_id:
            raise Http404

        size = str(width) + '_' + str(height)
        image_file = '.'.join([public_id, grapher_id, size, 'png'])

        # FIX waveform grapher name change
        old_image_file = '.'.join([public_id, 'waveform', size, 'png'])
        if 'waveform_centroid' in grapher_id and self.cache_data.exists(old_image_file):
            image_file = old_image_file

        if not self.cache_data.exists(image_file):
            source = item.get_source()
            if source:
                path = self.cache_data.dir + os.sep + image_file
                decoder = timeside.core.get_processor('file_decoder')(source)
                graph = grapher(width=width, height=height)
                (decoder | graph).run()
                graph.watermark('timeside', opacity=.6, margin=(5,5))
                f = open(path, 'w')
                graph.render(output=path)
                f.close()
                self.cache_data.add_file(image_file)

        response = StreamingHttpResponse(self.cache_data.read_stream_bin(image_file), content_type=mime_type)
        return response

    def list_export_extensions(self):
        "Return the recognized item export file extensions, as a list"
        list = []
        for encoder in self.encoders:
            list.append(encoder.file_extension())
        #FIXME: MP4
        list.append('mp4')
        return list

    def item_export(self, request, public_id, extension):
        """Export a given media item in the specified format (OGG, FLAC, ...)"""

        item = MediaItem.objects.get(public_id=public_id)
        public_access = get_item_access(item, request.user)

        if (not public_access == 'full' or not extension in settings.TELEMETA_STREAMING_FORMATS) and \
                    not (request.user.has_perm('telemeta.can_play_all_items') or request.user.is_superuser):
            mess = ugettext('Access not allowed')
            title = 'Item file : ' + public_id + '.' + extension + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        #FIXME: MP4 handling in TimeSide
        if 'mp4' in extension:
            mime_type = 'video/mp4'
            video = item.file.path
            response = StreamingHttpResponse(stream_from_file(video), mimetype = mime_type)
            response['Content-Disposition'] = 'attachment'
            return response

        if 'webm' in extension:
            mime_type = 'video/webm'
            video = item.file.path
            response = StreamingHttpResponse(stream_from_file(video), mimetype = mime_type)
            response['Content-Disposition'] = 'attachment'
            return response

        for encoder in self.encoders:
            if encoder.file_extension() == extension:
                break

        if encoder.file_extension() != extension:
            raise Http404('Unknown export file extension: %s' % extension)

        mime_type = encoder.mime_type()
        file = public_id + '.' + encoder.file_extension()
        source = item.get_source()

        flag = MediaItemTranscodingFlag.objects.filter(item=item, mime_type=mime_type)
        if not flag:
            flag = MediaItemTranscodingFlag(item=item, mime_type=mime_type)
            flag.value = False
            flag.save()
        else:
            flag = flag[0]

        format = item.mime_type
        dc_metadata = dublincore.express_item(item).to_list()
        mapping = DublinCoreToFormatMetadata(extension)
        metadata = mapping.get_metadata(dc_metadata)

        if mime_type in format:
            # source > stream
            if not extension in mapping.unavailable_extensions:
                proc = encoder(source, overwrite=True)
                proc.set_metadata(metadata)
                try:
                    #FIXME: should test if metadata writer is available
                    proc.write_metadata()
                except:
                    pass
            response = StreamingHttpResponse(stream_from_file(source), mimetype = mime_type)
        else:
            media = self.cache_export.dir + os.sep + file
            if not self.cache_export.exists(file) or not flag.value:
                # source > encoder > stream
                decoder = timeside.core.get_processor('file_decoder')(source)
                proc = encoder(media, streaming=True, overwrite=True)
                if extension in mapping.unavailable_extensions:
                    metadata=None
                proc.set_metadata(metadata)
                self.cache_export.add_file(file)
                response = StreamingHttpResponse(stream_from_processor(decoder, proc, flag), content_type=mime_type)
            else:
                # cache > stream
                response = StreamingHttpResponse(self.cache_export.read_stream_bin(file), content_type=mime_type)

        response['Content-Disposition'] = 'attachment'
        return response

    def item_playlist(self, request, public_id, template, mimetype):
        try:
            item = MediaItem.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'item': item, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), content_type=mimetype)

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def item_performances_edit(self, request, public_id, template):
        item = MediaItem.objects.get(public_id=public_id)
        PerformanceFormSet = inlineformset_factory(MediaItem, MediaItemPerformance, form=MediaItemPerformanceForm)
        if request.method == 'POST':
            formset = PerformanceFormSet(data=request.POST, instance=item)
            if formset.is_valid():
                formset.save()
                return redirect('telemeta-item-edit', item.public_id)
        else:
            formset = PerformanceFormSet(instance=item)
        return render(request, template, {'item': item, 'formset': formset,})

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def item_keywords_edit(self, request, public_id, template):
        item = MediaItem.objects.get(public_id=public_id)
        FormSet = inlineformset_factory(MediaItem, MediaItemKeyword)
        if request.method == 'POST':
            formset = FormSet(data=request.POST, instance=item)
            if formset.is_valid():
                formset.save()
                return redirect('telemeta-item-edit', item.public_id)
        else:
            formset = FormSet(instance=item)
        return render(request, template, {'item': item, 'formset': formset,})


class ItemListView(ListView):

    model = MediaItem
    template_name = "telemeta/mediaitem_list.html"
    paginate_by = 20
    queryset = MediaItem.objects.enriched().order_by('code', 'old_code')

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['count'] = self.object_list.count()
        return context

class ItemListViewFullAccess(ListView):

    model = MediaItem
    template_name = "telemeta/mediaitem_list.html"
    paginate_by = 20
    queryset = MediaItem.objects.enriched().filter(Q(collection__public_access="full")|Q(public_access="full")).sound().exclude(collection__public_access="none").order_by('code', 'old_code')

    def get_context_data(self, **kwargs):
        context = super(ItemListViewFullAccess, self).get_context_data(**kwargs)
        context['count'] = self.object_list.count()
        return context


class ItemUnpublishedListView(ItemListView):

    queryset = MediaItem.objects.filter(collection__code__contains='_I_').order_by('code', 'old_code')


class ItemPublishedListView(ItemListView):

    queryset = MediaItem.objects.filter(collection__code__contains='_E_').order_by('code', 'old_code')


class ItemSoundListView(ItemListView):

    queryset = MediaItem.objects.sound().order_by('code', 'old_code')


class ItemViewMixin(ItemBaseMixin):

    model = MediaItem
    form_class = MediaItemForm
    inlines = [ItemPerformanceInline, ItemKeywordInline, ItemRelatedInline, ItemIdentifierInline]
    # inlines = [ItemPerformanceInline, ItemKeywordInline, ItemRelatedInline,
    #             ItemFormatInline, ItemIdentifierInline]

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


class ItemEditView(ItemViewMixin, UpdateWithInlinesView):

    template_name = 'telemeta/mediaitem_edit.html'

    def get_form_class(self):
        if self.request.user.is_staff:
            return MediaItemForm
        else:
            return RestrictedMediaItemForm

    def forms_valid(self, form, inlines):
        messages.info(self.request, ugettext_lazy("You have successfully updated your item."))
        item = form.save()
        self.code = item.code
        if form.files:
            self.cache_data.delete_item_data(item.code)
            self.cache_export.delete_item_data(item.code)
            flags = MediaItemTranscodingFlag.objects.filter(item=item)
            analyses = MediaItemAnalysis.objects.filter(item=item)
            for flag in flags:
                flag.delete()
            for analysis in analyses:
                analysis.delete()
        item.set_revision(self.request.user)
        return super(ItemEditView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('telemeta-item-detail', kwargs={'public_id':self.code})

    def get_context_data(self, **kwargs):
        context = super(ItemEditView, self).get_context_data(**kwargs)
        item = self.get_object()
        context['item'] = item
        context['access'] = get_item_access(item, self.request.user)
        context['previous'], context['next'] = self.item_previous_next(item)
        #FIXME
        context['mime_type'] = 'audio/mp3'
        context['export_formats'] = self.get_export_formats()
        context['visualizers'] = self.get_graphers()
        context['audio_export_enabled'] = self.export_enabled
        context['auto_zoom'] = True
        return context

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def dispatch(self, *args, **kwargs):
        return super(ItemEditView, self).dispatch(*args, **kwargs)


class ItemAddView(ItemViewMixin, CreateWithInlinesView):

    form_class = MediaItemForm
    template_name = 'telemeta/mediaitem_add.html'

    def get_initial(self):
        item = self.model()
        # new item for a specific collection
        if 'public_id' in self.kwargs:
            public_id = self.kwargs['public_id']
            collections = MediaCollection.objects.filter(code=public_id)
            if collections:
                collection = collections[0]
                item.collection = collection
                items = MediaItem.objects.filter(collection=collection)
                item.code = auto_code(collection)
        return model_to_dict(item)

    def forms_valid(self, form, inlines):
        messages.info(self.request, ugettext_lazy("You have successfully added your item."))
        obj = form.save()
        obj.set_revision(self.request.user)
        return super(ItemAddView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('telemeta-item-detail', kwargs={'public_id':self.object.code})

    @method_decorator(permission_required('telemeta.add_mediaitem'))
    def dispatch(self, *args, **kwargs):
        return super(ItemAddView, self).dispatch(*args, **kwargs)


class ItemCopyView(ItemAddView):

    form_class = MediaItemForm
    template_name = 'telemeta/mediaitem_edit.html'

    def get_initial(self):
         return model_to_dict(self.get_object())

    def forms_valid(self, form, inlines):
        messages.info(self.request, ugettext_lazy("You have successfully updated your item."))
        item = form.save()
        item.set_revision(self.request.user)
        if not MediaItemPerformance.objects.filter(media_item=item):
            for performance in MediaItemPerformance.objects.filter(media_item=self.get_object()):
                performance.pk = None
                performance.id = None
                performance.media_item = item
                performance.save()
        if not MediaItemKeyword.objects.filter(item=item):
            for keyword in MediaItemKeyword.objects.filter(item=self.get_object()):
                keyword.pk = None
                keyword.id = None
                keyword.item = item
                keyword.save()
        return super(ItemCopyView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('telemeta-item-detail', kwargs={'public_id':self.object.code})

    def get_context_data(self, **kwargs):
        context = super(ItemCopyView, self).get_context_data(**kwargs)
        item = self.get_object()
        context['item'] = item
        context['access'] = get_item_access(item, self.request.user)
        context['previous'], context['next'] = self.item_previous_next(item)
        #FIXME
        context['mime_type'] = 'audio/mp3'
        context['export_formats'] = self.get_export_formats()
        context['visualizers'] = self.get_graphers()
        context['audio_export_enabled'] = self.export_enabled
        context['auto_zoom'] = True
        return context

    @method_decorator(permission_required('telemeta.add_mediaitem'))
    def dispatch(self, *args, **kwargs):
        return super(ItemCopyView, self).dispatch(*args, **kwargs)


class ItemDetailView(ItemViewMixin, DetailView):

    template_name = 'telemeta/mediaitem_detail.html'

    def item_analyze(self, item):
        analyses = item.analysis.all()
        mime_type = ''

        if analyses:
            for analysis in analyses:
                if not item.approx_duration and analysis.analyzer_id == 'duration':
                    value = analysis.value
                    time = value.split(':')
                    time[2] = time[2].split('.')[0]
                    time = ':'.join(time)
                    item.approx_duration = time
                    item.save()
                if analysis.analyzer_id == 'mime_type':
                    mime_type = analysis.value
        else:
            analyzers = []
            analyzers_sub = []
            graphers_sub = []

            source = item.get_source()
            if source:
                decoder  = timeside.core.get_processor('file_decoder')(source)
                pipe = decoder

                for analyzer in self.value_analyzers:
                    subpipe = analyzer()
                    analyzers_sub.append(subpipe)
                    pipe = pipe | subpipe

                default_grapher = self.get_grapher(self.default_grapher_id)
                for size in self.default_grapher_sizes:
                    width = size.split('x')[0]
                    height = size.split('x')[1]
                    image_file = '.'.join([item.public_id, self.default_grapher_id, size.replace('x', '_'), 'png'])
                    path = self.cache_data.dir + os.sep + image_file
                    graph = default_grapher(width = int(width), height = int(height))
                    graphers_sub.append({'graph' : graph, 'path': path})
                    pipe = pipe | graph

                pipe.run()

                for grapher in graphers_sub:
                    grapher['graph'].watermark('timeside', opacity=.6, margin=(5,5))
                    f = open(grapher['path'], 'w')
                    grapher['graph'].render(grapher['path'])
                    f.close()

                if os.path.exists(source):
                    mime_type = mimetypes.guess_type(source)[0]
                    analysis = MediaItemAnalysis(item=item, name='MIME type',
                                             analyzer_id='mime_type', unit='', value=mime_type)
                    analysis.save()
                    analysis = MediaItemAnalysis(item=item, name='Size',
                                             analyzer_id='size', unit='', value=item.size())
                    analysis.save()

                analysis = MediaItemAnalysis(item=item, name='Channels',
                                             analyzer_id='channels',
                                             unit='', value=decoder.input_channels)
                analysis.save()
                analysis = MediaItemAnalysis(item=item, name='Samplerate',
                                             analyzer_id='samplerate', unit='Hz',
                                             value=unicode(decoder.input_samplerate))
                analysis.save()
                analysis = MediaItemAnalysis(item=item, name='Resolution',
                                             analyzer_id='resolution', unit='bits',
                                             value=unicode(decoder.input_width))
                analysis.save()
                analysis = MediaItemAnalysis(item=item, name='Duration',
                                             analyzer_id='duration', unit='s',
                                             value=unicode(datetime.timedelta(0,decoder.input_duration)))
                analysis.save()

                for analyzer in analyzers_sub:
                    for key in analyzer.results.keys():
                        result = analyzer.results[key]
                        value = result.data_object.value
                        if value.shape[0] == 1:
                            value = value[0]
                        analysis = MediaItemAnalysis(item=item, name=result.name,
                                analyzer_id=result.id, unit=result.unit, value = unicode(value))
                        analysis.save()

#                FIXME: parse tags on first load
#                tags = decoder.tags

        self.mime_type = mime_type

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)

        public_id = get_kwargs_or_none('public_id', self.kwargs)
        marker_id = get_kwargs_or_none('marker_id', self.kwargs)
        width = get_kwargs_or_none('width', self.kwargs)
        height = get_kwargs_or_none('height', self.kwargs)

        # get item with one of its given marker_id
        if not public_id and marker_id:
            marker = MediaItemMarker.objects.get(public_id=marker_id)
            item_id = marker.item_id
            item = MediaItem.objects.get(id=item_id)
        else:
            item = self.get_object()

        access = get_item_access(item, self.request.user)

        previous, next = self.item_previous_next(item)

        self.item_analyze(item)

        #FIXME: use mimetypes.guess_type
        if 'quicktime' in self.mime_type:
            self.mime_type = 'video/mp4'

        playlists = get_playlists_names(self.request)
        related_media = MediaItemRelated.objects.filter(item=item)
        check_related_media(related_media)
        revisions = Revision.objects.filter(element_type='item', element_id=item.id).order_by('-time')
        if revisions:
            last_revision = revisions[0]
        else:
            last_revision = None

        item_format = ''
        if Format.objects.filter(item=item):
            item_format = item.format.get()

        context['item'] = item
        context['export_formats'] = self.get_export_formats()
        context['visualizers'] = self.get_graphers()
        context['auto_zoom'] = self.auto_zoom
        context['audio_export_enabled'] = self.export_enabled
        context['previous'] = previous
        context['next'] = next
        context['marker'] = marker_id
        context['playlists'] = playlists
        context['access'] = access
        context['width'] = width
        context['height'] = height
        context['related_media'] = related_media
        context['mime_type'] = self.mime_type
        context['last_revision'] = last_revision
        context['format'] = item_format
        context['private_extra_types'] = private_extra_types.values()
        context['site'] = 'http://' + Site.objects.all()[0].name
        return context


class DublinCoreToFormatMetadata(object):
    """a mapping class to get item DublinCore metadata dictionaries
    in various audio metadata format (MP3, OGG, etc...)"""

    #FIXME: should be given by timeside
    unavailable_extensions = ['wav', 'aiff', 'aif', 'flac', 'webm']

    metadata_mapping = {
                    'mp3' : {
                         'title': 'TIT2', #title2
                         'creator': 'TCOM', #composer
                         'creator': 'TPE1', #lead
                         'identifier': 'UFID', #unique ID
                         'relation': 'TALB', #album
                         'type': 'TCON', #genre
                         'publisher': 'TPUB', #publisher
                         'date': 'TDRC', #year
#                         'coverage': 'COMM',  #comment
                         },
                    'ogg': {
                        'creator': 'artist',
                        'relation': 'album',
                        'all': 'all',
                       },
                    'flac': {
                        'creator': 'artist',
                        'relation': 'album',
                        'all': 'all',
                       },
                    'wav': {
                        'creator': 'artist',
                        'relation': 'album',
                        'all': 'all',
                       },
                    'webm': {
                        'creator': 'artist',
                        'relation': 'album',
                        'all': 'all',
                       },
                    }

    def __init__(self, format):
        self.format = format

    def get_metadata(self, dc_metadata):
        mapp = self.metadata_mapping[self.format]
        metadata = {}
        keys_done = []
        for data in dc_metadata:
            key = data[0]
            value = data[1].encode('utf-8')
            if value:
                if key == 'date':
                    value = value.split(';')[0].split('=')
                    if len(value) > 1:
                        value  = value[1]
                        value = value.split('-')[0]
                    else:
                        value = value[0].split('-')[0]
                if key in mapp:
                    metadata[mapp[key]] = value.decode('utf-8')
                elif 'all' in mapp.keys():
                    metadata[key] = value.decode('utf-8')
                keys_done.append(key)
        return metadata


class ItemMarkerJsonView(View):

    model = MediaItem

    def get(self, request, *args, **kwargs):
        code = self.kwargs['public_id']
        marker_view = MarkerView()
        item = MediaItem.objects.get(code=code)
        markers = marker_view.get_markers(item.id)
        if markers:
            data = json.dumps(markers)
        else:
            data = ''
        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = "attachment; filename=%s.%s" % \
                                             (item.code, 'json')
        return response


class ItemPlayerDefaultView(ItemDetailView):

    template_name = 'telemeta/mediaitem_player.html'


class ItemDetailDCView(ItemDetailView):

    template_name = 'telemeta/mediaitem_detail_dc.html'


class ItemVideoPlayerView(ItemDetailView):

    template_name = 'telemeta/mediaitem_video_player.html'
