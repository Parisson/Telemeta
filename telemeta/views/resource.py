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


class ResourceView(object):
    """Provide Resource web UI methods"""

    types = {'corpus':
                {'model': MediaCorpus,
                'form' : MediaCorpusForm,
                'related': MediaCorpusRelated,
                'related_form': MediaCorpusRelatedForm,
                'parent': MediaFonds,
                },
            'fonds':
                {'model': MediaFonds,
                'form' : MediaFondsForm,
                'related': MediaFondsRelated,
                'related_form': MediaFondsRelatedForm,
                'parent': None,
                }
            }

    def setup(self, type):
        self.model = self.types[type]['model']
        self.form = self.types[type]['form']
        self.related = self.types[type]['related']
        self.related_form = self.types[type]['related_form']
        self.parent = self.types[type]['parent']
        self.type = type

    def detail(self, request, type, public_id, template='telemeta/resource_detail.html'):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        children = resource.children.all()
        children = children.order_by('code')
        related_media = self.related.objects.filter(resource=resource)
        check_related_media(related_media)
        playlists = get_playlists(request)
        revisions = Revision.objects.filter(element_type=type, element_id=resource.id).order_by('-time')
        if revisions:
            last_revision = revisions[0]
        else:
            last_revision = None
        if self.parent:
            parents = self.parent.objects.filter(children=resource)
        else:
            parents = []

        return render(request, template, {'resource': resource, 'type': type, 'children': children,
                        'related_media': related_media, 'parents': parents, 'playlists': playlists,
                        'last_revision': last_revision })

    def edit(self, request, type, public_id, template='telemeta/resource_edit.html'):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        if request.method == 'POST':
            form = self.form(data=request.POST, files=request.FILES, instance=resource)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                resource.set_revision(request.user)
                return redirect('telemeta-resource-detail', self.type, code)
        else:
            form = self.form(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, 'form': form,})

    def add(self, request, type, template='telemeta/resource_add.html'):
        self.setup(type)
        resource = self.model()
        if request.method == 'POST':
            form = self.form(data=request.POST, files=request.FILES, instance=resource)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                resource.set_revision(request.user)
                return redirect('telemeta-resource-detail', self.type, code)
        else:
            form = self.form(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, 'form': form,})

    def copy(self, request, type, public_id, template='telemeta/resource_edit.html'):
        self.setup(type)
        if request.method == 'POST':
            resource = self.model()
            form = self.form(data=request.POST, files=request.FILES, instance=resource)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                resource.save()
                resource.set_revision(request.user)
                return redirect('telemeta-resource-detail', self.type, code)
        else:
            resource = self.model.objects.get(code=public_id)
            form = self.form(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, "form": form,})

    def playlist(self, request, type, public_id, template, mimetype):
        self.setup(type)
        try:
            resource = self.model.objects.get(code=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'resource': resource, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    def delete(self, request, type, public_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        resource.delete()
        return HttpResponseRedirect('/archives/'+self.type+'/')

    def related_stream(self, request, type, public_id, media_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        media = self.related.objects.get(resource=resource, id=media_id)
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
        return response

    def related_download(self, request, type, public_id, media_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        media = self.related.objects.get(resource=resource, id=media_id)
        filename = media.file.path.split(os.sep)[-1]
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
        response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename
        return response

    @jsonrpc_method('telemeta.add_fonds_related_media')
    @jsonrpc_method('telemeta.add_corpus_related_media')
    def related_edit(self, request, type, public_id, template):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        ResourceRelatedFormSet = inlineformset_factory(self.model, self.related, form=self.related_form)
        if request.method == 'POST':
            formset = ResourceRelatedFormSet(data=request.POST, files=request.FILES, instance=resource)
            if formset.is_valid():
                formset.save()
                resource.set_revision(request.user)
                return redirect('telemeta-resource-edit', self.type, public_id)
        else:
            formset = ResourceRelatedFormSet(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, 'formset': formset,})


class ResourceMixin(View):

    types = {'corpus':
                {'model': MediaCorpus,
                'form' : MediaCorpusForm,
                'related': MediaCorpusRelated,
                'related_form': MediaCorpusRelatedForm,
                'parent': MediaFonds,
                'inlines': [CorpusRelatedInline,]
                },
            'fonds':
                {'model': MediaFonds,
                'form' : MediaFondsForm,
                'related': MediaFondsRelated,
                'related_form': MediaFondsRelatedForm,
                'parent': None,
                'inlines': [FondsRelatedInline,]
                }
            }

    def setup(self, type):
        self.model = self.types[type]['model']
        self.form = self.types[type]['form']
        self.form_class = self.types[type]['form']
        self.related = self.types[type]['related']
        self.related_form = self.types[type]['related_form']
        self.parent = self.types[type]['parent']
        self.inlines = self.types[type]['inlines']
        self.type = type

    def get_object(self):
        # super(CorpusDetailView, self).get_object()
        self.type = self.kwargs['type']
        self.setup(self.type)
        self.pk = self.model.objects.get(code=self.kwargs['public_id']).pk
        return get_object_or_404(self.model, pk=self.pk)

    def get_context_data(self, **kwargs):
        context = super(ResourceMixin, self).get_context_data(**kwargs)
        context['type'] = self.type
        return context


class ResourceSingleMixin(ResourceMixin):

    def get_queryset(self):
        self.type = self.kwargs['type']
        self.setup(self.type)
        return self

    def get_object(self):
        # super(CorpusDetailView, self).get_object()
        self.type = self.kwargs['type']
        self.setup(self.type)
        self.pk = self.model.objects.get(code=self.kwargs['public_id']).pk
        return get_object_or_404(self.model, pk=self.pk)

    def get_context_data(self, **kwargs):
        context = super(ResourceMixin, self).get_context_data(**kwargs)
        resource = self.get_object()
        related_media = self.related.objects.filter(resource=resource)
        check_related_media(related_media)
        playlists = get_playlists_names(self.request)
        revisions = Revision.objects.filter(element_type=self.type, element_id=self.pk).order_by('-time')
        context['resource'] = resource
        context['type'] = self.type
        context['related_media'] = related_media
        context['revisions'] = revisions
        if revisions:
            context['last_revision'] = revisions[0]
        else:
            context['last_revision'] = None
        if self.parent:
            context['parents'] = self.parent.objects.filter(children=resource)
        else:
            context['parents'] = []
        return context


class ResourceListView(ResourceMixin, ListView):

    template_name = "telemeta/resource_list.html"
    paginate_by = 20

    def get_queryset(self):
        self.type = self.kwargs['type']
        self.setup(self.type)
        return self.model.objects.all().order_by('code')

    def get_context_data(self, **kwargs):
        context = super(ResourceListView, self).get_context_data(**kwargs)
        context['count'] = self.object_list.count()
        return context

class ResourceDetailView(ResourceSingleMixin, DetailView):

    template_name = "telemeta/resource_detail.html"


class ResourceDetailDCView(ResourceDetailView):

    template_name = "telemeta/resource_detail_dc.html"


class ResourceAddView(ResourceMixin, CreateView):

    template_name = 'telemeta/resource_add.html'

    def get_queryset(self):
        self.type = self.kwargs['type']
        self.setup(self.type)
        return self

    def get_success_url(self):
        return reverse_lazy('telemeta-resource-list', kwargs={'type':self.kwargs['type']})


class ResourceCopyView(ResourceSingleMixin, ResourceAddView):

    template_name = 'telemeta/resource_edit.html'

    def get_initial(self):
        resource = self.model.objects.get(code=self.kwargs['public_id'])
        return model_to_dict(resource)

    def get_success_url(self):
        return reverse_lazy('telemeta-resource-list', kwargs={'type':self.kwargs['type']})
        # return reverse_lazy('telemeta-resource-detail', kwargs={'type':self.kwargs['type'], 'public_id':self.kwargs['public_id']})


class ResourceDeleteView(ResourceSingleMixin, DeleteView):

    template_name = 'telemeta/resource_confirm_delete.html'

    def get_success_url(self):
         return reverse_lazy('telemeta-resource-list', kwargs={'type':self.kwargs['type']})


class ResourceEditView(ResourceSingleMixin, UpdateWithInlinesView):

    template_name = 'telemeta/resource_edit.html'

    def get_success_url(self):
        return reverse_lazy('telemeta-resource-detail', kwargs={'type':self.kwargs['type'], 'public_id':self.kwargs['public_id']})
