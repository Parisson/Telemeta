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
from telemeta.views.core import serve_media
from telemeta.views.epub import BaseEpubMixin
from django.utils.translation import ugettext_lazy as _


class ResourceView(object):
    """Provide Resource web UI methods"""

    types = {'corpus':
             {'model': MediaCorpus,
                 'form': MediaCorpusForm,
                 'related': MediaCorpusRelated,
                 'parent': MediaFonds,
              },
             'fonds':
             {'model': MediaFonds,
                 'form': MediaFondsForm,
                 'related': MediaFondsRelated,
                 'parent': None,
              }
             }

    def setup(self, type):
        self.model = self.types[type]['model']
        self.form = self.types[type]['form']
        self.related = self.types[type]['related']
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
                                          'last_revision': last_revision})

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
        return render(request, template, {'resource': resource, 'type': type, 'form': form, })

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
        return render(request, template, {'resource': resource, 'type': type, 'form': form, })

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
        return render(request, template, {'resource': resource, 'type': type, "form": form, })

    def playlist(self, request, type, public_id, template, mimetype):
        self.setup(type)
        try:
            resource = self.model.objects.get(code=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'resource': resource, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), content_type=mimetype)

    def delete(self, request, type, public_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        revisions = Revision.objects.filter(element_type='resource', element_id=resource.id)
        for revision in revisions:
            revision.delete()
        resource.delete()
        return HttpResponseRedirect('/archives/' + self.type + '/')

    def related_stream(self, request, type, public_id, media_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        media = self.related.objects.get(resource=resource, id=media_id)
        if media.file:
            response = serve_media(media.file.path, content_type=media.mime_type)
        else:
            raise Http404
        return response

    def related_download(self, request, type, public_id, media_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        media = self.related.objects.get(resource=resource, id=media_id)
        if media.file:
            response = serve_media(media.file.path, content_type=media.mime_type)
        else:
            raise Http404
        return response


class ResourceMixin(View):

    types = {'corpus':
             {'model': MediaCorpus,
              'form': MediaCorpusForm,
              'related': MediaCorpusRelated,
                 'parent': MediaFonds,
              'inlines': [CorpusRelatedInline, ]
              },
             'fonds':
             {'model': MediaFonds,
              'form': MediaFondsForm,
                 'related': MediaFondsRelated,
                 'parent': None,
                 'inlines': [FondsRelatedInline, ]
              }
             }

    def setup(self, type):
        self.model = self.types[type]['model']
        self.form = self.types[type]['form']
        self.form_class = self.types[type]['form']
        self.related = self.types[type]['related']
        self.parent = self.types[type]['parent']
        self.inlines = self.types[type]['inlines']
        self.type = type

    def get_object(self):
        # super(CorpusDetailView, self).get_object()
        self.type = self.kwargs['type']
        self.setup(self.type)
        objs = self.model.objects.filter(code=self.kwargs['public_id'])
        if not objs:
            try:
                obj = self.model.objects.get(id=self.kwargs['public_id'])
            except:
                raise Http404
        else:
            obj = objs[0]
        return obj

    def get_context_data(self, **kwargs):
        context = super(ResourceMixin, self).get_context_data(**kwargs)
        context['type'] = self.type
        return context


class ResourceSingleMixin(ResourceMixin):

    def get_queryset(self):
        self.type = self.kwargs['type']
        self.setup(self.type)
        return self

    def get_context_data(self, **kwargs):
        context = super(ResourceMixin, self).get_context_data(**kwargs)
        resource = self.get_object()
        related_media = self.related.objects.filter(resource=resource)
        check_related_media(related_media)
        playlists = get_playlists_names(self.request)
        revisions = Revision.objects.filter(element_type=self.type, element_id=resource.pk).order_by('-time')
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
        return reverse_lazy('telemeta-resource-list', kwargs={'type': self.kwargs['type']})

    @method_decorator(permission_required('telemeta.add_mediacorpus'))
    @method_decorator(permission_required('telemeta.add_mediafonds'))
    def dispatch(self, *args, **kwargs):
        return super(ResourceAddView, self).dispatch(*args, **kwargs)


class ResourceCopyView(ResourceSingleMixin, ResourceAddView):

    template_name = 'telemeta/resource_edit.html'

    def get_initial(self):
        return model_to_dict(self.get_object())

    def get_success_url(self):
        return reverse_lazy('telemeta-resource-list', kwargs={'type': self.kwargs['type']})
        # return reverse_lazy('telemeta-resource-detail', kwargs={'type':self.kwargs['type'], 'public_id':self.kwargs['public_id']})

    @method_decorator(permission_required('telemeta.add_mediacorpus'))
    @method_decorator(permission_required('telemeta.add_mediafonds'))
    def dispatch(self, *args, **kwargs):
        return super(ResourceCopyView, self).dispatch(*args, **kwargs)


class ResourceDeleteView(ResourceSingleMixin, DeleteView):

    template_name = 'telemeta/resource_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('telemeta-resource-list', kwargs={'type': self.kwargs['type']})

    @method_decorator(permission_required('telemeta.delete_mediacorpus'))
    @method_decorator(permission_required('telemeta.delete_mediafonds'))
    def dispatch(self, *args, **kwargs):
        return super(ResourceDeleteView, self).dispatch(*args, **kwargs)


class ResourceEditView(ResourceSingleMixin, UpdateWithInlinesView):

    template_name = 'telemeta/resource_edit.html'

    def get_success_url(self):
        return reverse_lazy('telemeta-resource-detail', kwargs={'type': self.kwargs['type'], 'public_id': self.kwargs['public_id']})

    @method_decorator(permission_required('telemeta.change_mediacorpus'))
    @method_decorator(permission_required('telemeta.change_mediafonds'))
    def dispatch(self, *args, **kwargs):
        return super(ResourceEditView, self).dispatch(*args, **kwargs)


class ResourceEpubView(ResourceSingleMixin, BaseEpubMixin, View):
    "Download corpus data embedded in an EPUB3 file"

    def get(self, request, *args, **kwargs):
        self.setup_epub(self.get_object())
        if not os.path.exists(self.path):
            self.write_book()
        epub_file = open(self.path, 'rb')
        response = HttpResponse(epub_file.read(), content_type='application/epub+zip')
        response['Content-Disposition'] = "attachment; filename=%s" % self.filename + '.epub'
        return response


class ResourceEpubPasswordView(ResourceSingleMixin, FormView):

    template_name = 'telemeta/resource_epub_password.html'
    form_class = EpubPasswordForm

    def get_success_url(self):
        return reverse_lazy('telemeta-resource-epub-list', kwargs={'type': self.kwargs['type'], 'public_id': self.kwargs['public_id']})

    def form_valid(self, form):
        self.password = form.cleaned_data['password']
        if self.password != unicode('mélodie'.decode('utf-8')):
            messages.info(self.request, _("Bad password, please try again."))
            return redirect('telemeta-resource-password-epub', self.kwargs['type'], self.kwargs['public_id'])
        else:
            return redirect('telemeta-resource-epub-list', self.kwargs['type'], self.kwargs['public_id'])

        return super(ResourceEpubPasswordView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super(ResourceEpubPasswordView, self).dispatch(*args, **kwargs)


class ResourceEpubListView(ResourceDetailView):

    template_name = 'telemeta/resource_epub_list.html'
