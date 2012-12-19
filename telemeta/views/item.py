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

import mimetypes
from telemeta.views.core import *


class ItemView(object):
    """Provide Collections web UI methods"""

    graphers = timeside.core.processors(timeside.api.IGrapher)
    decoders = timeside.core.processors(timeside.api.IDecoder)
    encoders = timeside.core.processors(timeside.api.IEncoder)
    analyzers = timeside.core.processors(timeside.api.IAnalyzer)
    cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)
    cache_export = TelemetaCache(settings.TELEMETA_EXPORT_CACHE_DIR)

    export_enabled = getattr(settings, 'TELEMETA_DOWNLOAD_ENABLED', True)
    export_formats = getattr(settings, 'TELEMETA_DOWNLOAD_FORMATS', ('mp3', 'wav'))

    def get_export_formats(self):
        formats = []
        for encoder in self.encoders:
            if encoder.file_extension() in self.export_formats:
                formats.append({'name': encoder.format(),
                                    'extension': encoder.file_extension()})
        return formats

    def item_previous_next(self, item):
        # Get previous and next items
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

    def item_detail(self, request, public_id=None, marker_id=None, width=None, height=None,
                        template='telemeta/mediaitem_detail.html'):
        """Show the details of a given item"""

        if not public_id and marker_id:
            marker = MediaItemMarker.objects.get(public_id=marker_id)
            item_id = marker.item_id
            item = MediaItem.objects.get(id=item_id)
        else:
            item = MediaItem.objects.get(public_id=public_id)

        item_public_access = item.public_access != 'none' or item.collection.public_access != 'none'
        if not item_public_access and not (request.user.is_staff or request.user.is_superuser):
            mess = ugettext('Access not allowed')
            title = ugettext('Item') + ' : ' + public_id + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        graphers = []
        for grapher in self.graphers:
            graphers.append({'name':grapher.name(), 'id': grapher.id()})
        if request.REQUEST.has_key('grapher_id'):
            grapher_id = request.REQUEST['grapher_id']
        else:
            try:
                grapher_id = settings.TELEMETA_DEFAULT_GRAPHER_ID
            except:
                grapher_id = 'waveform'

        previous, next = self.item_previous_next(item)
        mime_type = self.item_analyze(item)
        #FIXME: use mimetypes.guess_type
        if 'quicktime' in mime_type:
            mime_type = 'video/mp4'

        playlists = get_playlists(request)
        public_access = get_public_access(item.public_access, str(item.recorded_from_date).split('-')[0],
                                                str(item.recorded_to_date).split('-')[0])

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
                    'visualizers': graphers, 'visualizer_id': grapher_id,
                    'audio_export_enabled': self.export_enabled,
                    'previous' : previous, 'next' : next, 'marker': marker_id, 'playlists' : playlists,
                    'public_access': public_access, 'width': width, 'height': height,
                    'related_media': related_media, 'mime_type': mime_type, 'last_revision': last_revision,
                    'format': format,
                    })

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def item_edit(self, request, public_id, template='telemeta/mediaitem_edit.html'):
        """Edit a given item"""
        item = MediaItem.objects.get(public_id=public_id)

        graphers = []
        for grapher in self.graphers:
            graphers.append({'name':grapher.name(), 'id': grapher.id()})
        if request.REQUEST.has_key('grapher_id'):
            grapher_id = request.REQUEST['grapher_id']
        else:
            try:
                grapher_id = settings.TELEMETA_DEFAULT_GRAPHER_ID
            except:
                grapher_id = 'waveform'

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
                    'visualizers': graphers, 'visualizer_id': grapher_id,
                    'audio_export_enabled': self.export_enabled,
                    'forms': forms, 'previous' : previous,
                    'next' : next, 'mime_type': mime_type,
                    })

    def related_media_item_stream(self, request, item_public_id, media_id):
        item = MediaItem.objects.get(public_id=item_public_id)
        media = MediaItemRelated.objects.get(item=item, id=media_id)
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
#        response['Content-Disposition'] = 'attachment; '+'filename='+media.title+'.'+ext
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
        if public_id:
            collection = MediaCollection.objects.get(public_id=public_id)
            items = MediaItem.objects.filter(collection=collection)
            code = auto_code(items, collection.code)
            item = MediaItem(collection=collection, code=code)
            format, created = Format.objects.get_or_create(item=item)
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

        return render(request, template, {'item': item, 'forms': forms, 'hidden_fields': hidden_fields,})

    @method_decorator(permission_required('telemeta.add_mediaitem'))
    def item_copy(self, request, public_id, template='telemeta/mediaitem_copy.html'):
        """Copy a given item"""
        if request.method == 'POST':
            source_item = MediaItem.objects.get(public_id=public_id)
            item = MediaItem()
            format = Format()
            item_form = MediaItemForm(data=request.POST, files=request.FILES, instance=item, prefix='item')
            format_form = FormatForm(data=request.POST, instance=format, prefix='format')

            if item_form.is_valid():
                item_form.save()
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

        forms = [item_form, format_form]
        hidden_fields = ['item-copied_from_item', 'format-item']

        return render(request, template, {'item': item, "forms": forms, 'hidden_fields': hidden_fields,})

    @method_decorator(permission_required('telemeta.delete_mediaitem'))
    def item_delete(self, request, public_id):
        """Delete a given item"""
        item = MediaItem.objects.get(public_id=public_id)
        collection = item.collection
        item.delete()
        return redirect('telemeta-collection-detail', collection.code)

    def item_analyze(self, item):
        analyses = MediaItemAnalysis.objects.filter(item=item)
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

            if item.file:
                decoder  = timeside.decoder.FileDecoder(item.file.path)
                pipe = decoder

                for analyzer in self.analyzers:
                    subpipe = analyzer()
                    analyzers_sub.append(subpipe)
                    pipe = pipe | subpipe

                try:
                    sizes = settings.TELEMETA_DEFAULT_GRAPHER_SIZES
                except:
                    sizes = ['360x130', ]

                for grapher in self.graphers:
                    for size in sizes:
                        width = size.split('x')[0]
                        height = size.split('x')[1]
                        image_file = '.'.join([item.public_id, grapher.id(), size.replace('x', '_'), 'png'])
                        path = self.cache_data.dir + os.sep + image_file
                        graph = grapher(width = int(width), height = int(height))
                        graphers_sub.append({'graph' : graph, 'path': path})
                        pipe = pipe | graph

                pipe.run()

                for grapher in graphers_sub:
                    grapher['graph'].watermark('timeside', opacity=.6, margin=(5,5))
                    f = open(grapher['path'], 'w')
                    grapher['graph'].render(grapher['path'])
                    f.close()

                mime_type = mimetypes.guess_type(item.file.path)[0]
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
                    value = analyzer.result()
                    analysis = MediaItemAnalysis(item=item, name=analyzer.name(),
                                                 analyzer_id=analyzer.id(),
                                                 unit=analyzer.unit(), value=str(value))
                    analysis.save()

#                FIXME: parse tags on first load
#                tags = decoder.tags

        return mime_type

    def item_analyze_xml(self, request, public_id):
        item = MediaItem.objects.get(public_id=public_id)
        analyses = MediaItemAnalysis.objects.filter(item=item)
        analyzers = []
        for analysis in analyses:
            analyzers.append(analysis.to_dict())
        mime_type = 'text/xml'
        response = HttpResponse(self.cache_data.get_analyzer_xml(analyzers), mimetype=mime_type)
        response['Content-Disposition'] = 'attachment; filename='+public_id+'.xml'
        return response

    def item_visualize(self, request, public_id, visualizer_id, width, height):
        item = MediaItem.objects.get(public_id=public_id)
        mime_type = 'image/png'
        grapher_id = visualizer_id

        for grapher in self.graphers:
            if grapher.id() == grapher_id:
                break

        if grapher.id() != grapher_id:
            raise Http404

        size = width + '_' + height
        image_file = '.'.join([public_id, grapher_id, size, 'png'])

        if not self.cache_data.exists(image_file):
            if item.file:
                path = self.cache_data.dir + os.sep + image_file
                decoder  = self.decoders[0](item.file.path)
                graph = grapher(width = int(width), height = int(height))
                (decoder | graph).run()
                graph.watermark('timeside', opacity=.6, margin=(5,5))
                f = open(path, 'w')
                graph.render(path)
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
        public_access = get_public_access(item.public_access,
                                          str(item.recorded_from_date).split('-')[0],
                                          str(item.recorded_to_date).split('-')[0])

        if (not public_access or not extension in settings.TELEMETA_STREAMING_FORMATS) and \
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
        audio = item.file.path

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
                proc = encoder(audio)
                proc.set_metadata(metadata)
                try:
                    proc.write_metadata()
                except:
                    pass
            response = HttpResponse(stream_from_file(audio), mimetype = mime_type)
        else:
            media = self.cache_export.dir + os.sep + file
            if not self.cache_export.exists(file) or not flag.value:
                # source > encoder > stream
                decoder = self.decoders[0](audio)
                decoder.setup()
                proc = encoder(media, streaming=True)
                proc.setup(channels=decoder.channels(), samplerate=decoder.samplerate())
                if extension in mapping.unavailable_extensions:
                    metadata=None
                response = HttpResponse(stream_from_processor(decoder, proc, flag, metadata=metadata), mimetype = mime_type)
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

