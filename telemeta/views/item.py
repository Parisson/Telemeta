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


class ItemView(object):
    """Provide Item web UI methods"""

    graphers = timeside.core.processors(timeside.api.IGrapher)
    decoders = timeside.core.processors(timeside.api.IDecoder)
    encoders = timeside.core.processors(timeside.api.IEncoder)
    analyzers = timeside.core.processors(timeside.api.IAnalyzer)
    value_analyzers = timeside.core.processors(timeside.api.IValueAnalyzer)
    cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)
    cache_export = TelemetaCache(settings.TELEMETA_EXPORT_CACHE_DIR)

    export_enabled = getattr(settings, 'TELEMETA_DOWNLOAD_ENABLED', True)
    export_formats = getattr(settings, 'TELEMETA_DOWNLOAD_FORMATS', ('mp3', 'wav'))
    default_grapher_id = getattr(settings, 'TIMESIDE_DEFAULT_GRAPHER_ID', ('waveform_simple'))
    default_grapher_sizes = getattr(settings, 'TELEMETA_DEFAULT_GRAPHER_SIZES', ['360x130', ])
    auto_zoom = getattr(settings, 'TIMESIDE_AUTO_ZOOM', False)

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

    def get_graphers(self):
        graphers = []
        for grapher in self.graphers:
            if grapher.id() == self.default_grapher_id:
                graphers.insert(0, {'name':grapher.name(), 'id': grapher.id()})
            else:
                graphers.append({'name':grapher.name(), 'id': grapher.id()})
        return graphers
        
    def get_grapher(self, id):
        for grapher in self.graphers:
            if grapher.id() == id:
                break        
        return grapher

    def item_detail(self, request, public_id=None, marker_id=None, width=None, height=None,
                        template='telemeta/mediaitem_detail.html'):
        """Show the details of a given item"""

        # get item with one of its given marker_id
        if not public_id and marker_id:
            marker = MediaItemMarker.objects.get(public_id=marker_id)
            item_id = marker.item_id
            item = MediaItem.objects.get(id=item_id)
        else:
            item = MediaItem.objects.get(public_id=public_id)

        access = get_item_access(item, request.user)

        if access == 'none':
            mess = ugettext('Access not allowed')
            title = ugettext('Item') + ' : ' + public_id + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        previous, next = self.item_previous_next(item)

        mime_type = self.item_analyze(item)

        #FIXME: use mimetypes.guess_type
        if 'quicktime' in mime_type:
            mime_type = 'video/mp4'

        playlists = get_playlists(request)
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

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def item_edit(self, request, public_id, template='telemeta/mediaitem_edit.html'):
        """Edit a given item"""
        item = MediaItem.objects.get(public_id=public_id)
        access = get_item_access(item, request.user)

        previous, next = self.item_previous_next(item)

        mime_type = self.item_analyze(item)

        #FIXME: use mimetypes.guess_type
        if 'quicktime' in mime_type:
            mime_type = 'video/mp4'

        format, created = Format.objects.get_or_create(item=item)

        if request.method == 'POST':
            item_form = MediaItemForm(data=request.POST, files=request.FILES, instance=item, prefix='item')
            format_form = FormatForm(data=request.POST, instance=format, prefix='format')
            if item_form.is_valid() and format_form.is_valid():
                item_form.save()
                format_form.save()
                code = item_form.cleaned_data['code']
                if not code:
                    code = str(item.id)
                if item_form.files:
                    self.cache_data.delete_item_data(code)
                    self.cache_export.delete_item_data(code)
                    flags = MediaItemTranscodingFlag.objects.filter(item=item)
                    analyses = MediaItemAnalysis.objects.filter(item=item)
                    for flag in flags:
                        flag.delete()
                    for analysis in analyses:
                        analysis.delete()
                item.set_revision(request.user)
                return redirect('telemeta-item-detail', code)
        else:
            item_form = MediaItemForm(instance=item, prefix='item')
            format_form = FormatForm(instance=format, prefix='format')

        forms = [item_form, format_form]

        return render(request, template,
                    {'item': item,
                     'export_formats': self.get_export_formats(),
                    'visualizers': self.get_graphers(),
                    'audio_export_enabled': self.export_enabled,
                    'forms': forms, 'previous' : previous,
                    'next' : next, 'mime_type': mime_type, 'access': access,
                    })

    def related_media_item_stream(self, request, item_public_id, media_id):
        item = MediaItem.objects.get(public_id=item_public_id)
        media = MediaItemRelated.objects.get(item=item, id=media_id)
        filename = media.file.path.split(os.sep)[-1]
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
        return response

    def related_media_item_download(self, request, item_public_id, media_id):
        item = MediaItem.objects.get(public_id=item_public_id)
        media = MediaItemRelated.objects.get(item=item, id=media_id)
        filename = media.file.path.split(os.sep)[-1]
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
        response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename
        return response

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def related_media_edit(self, request, public_id, template):
        item = MediaItem.objects.get(public_id=public_id)
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

    @method_decorator(permission_required('telemeta.add_mediaitem'))
    def item_add(self, request, public_id=None, template='telemeta/mediaitem_add.html'):
        """Add an item"""
        access = ''

        if public_id:
            collection = MediaCollection.objects.get(public_id=public_id)
            items = MediaItem.objects.filter(collection=collection)
            code = auto_code(items, collection.code)
            item = MediaItem(collection=collection, code=code)
            format, created = Format.objects.get_or_create(item=item)
            access = get_item_access(item, request.user)
        else:
            item = MediaItem()
            format = Format()

        if request.method == 'POST':
            item_form = MediaItemForm(data=request.POST, files=request.FILES, instance=item, prefix='item')
            format_form = FormatForm(data=request.POST, instance=format, prefix='format')
            if item_form.is_valid() and format_form.is_valid():
                item_form.save()
                item.set_revision(request.user)
                format.item = item
                format_form.save()
                code = item_form.cleaned_data['code']
                if not code:
                    code = str(item.id)
                return redirect('telemeta-item-detail', code)
        else:
            item_form = MediaItemForm(instance=item, prefix='item')
            format_form = FormatForm(instance=format, prefix='format')

        forms = [item_form, format_form]
        hidden_fields = ['item-copied_from_item', 'format-item']

        return render(request, template, {'item': item, 'forms': forms, 'hidden_fields': hidden_fields,
                                            'access': access, })

    @method_decorator(permission_required('telemeta.add_mediaitem'))
    def item_copy(self, request, public_id, template='telemeta/mediaitem_copy.html'):
        """Copy a given item"""
        if request.method == 'POST':
            source_item = MediaItem.objects.get(public_id=public_id)

            format = Format()
            format_form = FormatForm(data=request.POST, instance=format, prefix='format')

            item = MediaItem()
            if request.FILES:
                item_form = MediaItemForm(data=request.POST, files=request.FILES, instance=item, prefix='item')
            else:
                item_form = MediaItemForm(data=request.POST, instance=item, prefix='item')

            if item_form.is_valid():
                item_form.save()
                if not request.FILES:
                    item.file = source_item.file
                    item.save()

                code = item_form.cleaned_data['code']
                if not code:
                    code = str(item.id)
                if format_form.is_valid():
                    format.item = item
                    format_form.save()

                performances = MediaItemPerformance.objects.filter(media_item=source_item)
                for performance in performances:
                    performance.pk = None
                    performance.id = None
                    performance.media_item = item
                    performance.save()

                keywords = MediaItemKeyword.objects.filter(item=source_item)
                for keyword in keywords:
                    keyword.pk = None
                    keyword.id = None
                    keyword.item = item
                    keyword.save()

                item.set_revision(request.user)
                return redirect('telemeta-item-detail', code)
        else:
            item = MediaItem.objects.get(public_id=public_id)
            items = MediaItem.objects.filter(collection=item.collection)
            item.code = auto_code(items, item.collection.code)
            item.approx_duration = ''
            item_form = MediaItemForm(instance=item, prefix='item')
            format, created = Format.objects.get_or_create(item=item)
            format_form = FormatForm(instance=format, prefix='format')
            item_form.code = item.code
            item_form.file = None

        access = get_item_access(item, request.user)
        forms = [item_form, format_form]
        hidden_fields = ['item-copied_from_item', 'format-item']

        return render(request, template, {'item': item, "forms": forms, 'hidden_fields': hidden_fields,
                                            'access': access, })

    @method_decorator(permission_required('telemeta.delete_mediaitem'))
    def item_delete(self, request, public_id):
        """Delete a given item"""
        item = MediaItem.objects.get(public_id=public_id)
        collection = item.collection
        item.delete()
        return redirect('telemeta-collection-detail', collection.code)

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
                decoder  = timeside.decoder.FileDecoder(source)
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

                mime_type = mimetypes.guess_type(source)[0]
                analysis = MediaItemAnalysis(item=item, name='MIME type',
                                             analyzer_id='mime_type', unit='', value=mime_type)
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

        return mime_type

    def item_analyze_xml(self, request, public_id):
        item = MediaItem.objects.get(public_id=public_id)
        analyses = item.analysis.all()
        analyzers = []
        for analysis in analyses:
            analyzers.append(analysis.to_dict())
        mime_type = 'text/xml'
        response = HttpResponse(self.cache_data.get_analyzer_xml(analyzers), mimetype=mime_type)
        response['Content-Disposition'] = 'attachment; filename='+public_id+'.xml'
        return response

    def item_visualize(self, request, public_id, grapher_id, width, height):
        item = MediaItem.objects.get(public_id=public_id)
        mime_type = 'image/png'
        grapher = self.get_grapher(grapher_id)
        
        if grapher.id() != grapher_id:
            raise Http404

        size = width + '_' + height
        image_file = '.'.join([public_id, grapher_id, size, 'png'])

        # FIX waveform grapher name change
        old_image_file = '.'.join([public_id, 'waveform', size, 'png'])
        if 'waveform_centroid' in grapher_id and self.cache_data.exists(old_image_file):
            image_file = old_image_file

        if not self.cache_data.exists(image_file):
            source = item.get_source()
            if source:
                path = self.cache_data.dir + os.sep + image_file
                decoder  = timeside.decoder.FileDecoder(source)
                graph = grapher(width = int(width), height = int(height))
                (decoder | graph).run()
                graph.watermark('timeside', opacity=.6, margin=(5,5))
                f = open(path, 'w')
                graph.render(output=path)
                f.close()

        response = HttpResponse(self.cache_data.read_stream_bin(image_file), mimetype=mime_type)
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
            response = HttpResponse(stream_from_file(video), mimetype = mime_type)
            response['Content-Disposition'] = 'attachment'
            return response

        if 'webm' in extension:
            mime_type = 'video/webm'
            video = item.file.path
            response = HttpResponse(stream_from_file(video), mimetype = mime_type)
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

        format = self.item_analyze(item)
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
            response = HttpResponse(stream_from_file(source), mimetype = mime_type)
        else:
            media = self.cache_export.dir + os.sep + file
            if not self.cache_export.exists(file) or not flag.value:
                # source > encoder > stream
                decoder = timeside.decoder.FileDecoder(source)
                proc = encoder(media, streaming=True, overwrite=True)
                if extension in mapping.unavailable_extensions:
                    metadata=None
                proc.set_metadata(metadata)
                
                response = HttpResponse(stream_from_processor(decoder, proc, flag), mimetype = mime_type)
            else:
                # cache > stream
                response = HttpResponse(self.cache_export.read_stream_bin(file), mimetype = mime_type)

        response['Content-Disposition'] = 'attachment'
        return response

    def item_playlist(self, request, public_id, template, mimetype):
        try:
            item = MediaItem.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'item': item, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

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

