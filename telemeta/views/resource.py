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

    @jsonrpc_method('telemeta.change_fonds')
    @jsonrpc_method('telemeta.change_corpus')
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

    @jsonrpc_method('telemeta.add_fonds')
    @jsonrpc_method('telemeta.add_corpus')
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

    @jsonrpc_method('telemeta.add_fonds')
    @jsonrpc_method('telemeta.add_corpus')
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

    @jsonrpc_method('telemeta.del_fonds')
    @jsonrpc_method('telemeta.del_corpus')
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


