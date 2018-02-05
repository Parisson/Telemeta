# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Cooperative Artefacts <artefacts.lle@gmail.com>

from telemeta.views.core import *
from telemeta.views.core import serve_media

from telemeta.forms.authority import *
import sys
import time


class AuthorityViewMixin(object):

    model = Authority
    form_class = AuthorityForm


    def get_object(self):
        obj = self.model.objects.filter(id=self.kwargs['public_id'])
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

class AuthorityAddView(AuthorityViewMixin,CreateWithInlinesView):

    form_class = AuthorityForm
    template_name = 'telemeta/authority_add.html'

    def get_initial(self):
        authority = self.model()
        # new Authority for a specific collection
        return model_to_dict(authority)

    def forms_valid(self, form, inlines):
        messages.info(self.request, ugettext_lazy("You have successfully added your authority."))
        obj = form.save()
        return super(AuthorityAddView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('telemeta-authorities-detail', kwargs={'public_id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AuthorityAddView, self).get_context_data(**kwargs)
        return context

# class AuthorityDeleteView(AuthorityViewMixin, DeleteView):
#
#     template_name = 'telemeta/authority_confirm_delete.html'
#
#     def get_success_url(self):
#         return reverse_lazy('telemeta-authorities', kwargs={'public_id': self.object.id})
# 
#     @method_decorator(permission_required('telemeta.delete_authority'))
#     def dispatch(self, *args, **kwargs):
#         return super(AuthorityDeleteView, self).dispatch(*args, **kwargs)


class AuthorityEditView(AuthorityViewMixin, UpdateWithInlinesView):

    template_name = 'telemeta/authority_edit.html'

    def get_form_class(self):
        return AuthorityForm

    def forms_valid(self, form, inlines):
        messages.info(self.request, ugettext_lazy("You have successfully updated your authority."))
        authority = form.save()
        return super(AuthorityEditView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('telemeta-authorities-detail', kwargs={'public_id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AuthorityEditView, self).get_context_data(**kwargs)
        authority = self.get_object()
        context['authority'] = authority
        return context

    @method_decorator(permission_required('telemeta.change_authority'))
    def dispatch(self, *args, **kwargs):
        return super(AuthorityEditView, self).dispatch(*args, **kwargs)



class AuthorityListView(ListView):

    model = Authority
    template_name = "telemeta/authority_list.html"
    paginate_by = 20
    queryset = Authority.objects.order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(AuthorityListView, self).get_context_data(**kwargs)
        context['count'] = self.object_list.count()
        return context


class AuthorityDetailView(AuthorityViewMixin, DetailView):

    template_name = 'telemeta/authority_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorityDetailView, self).get_context_data(**kwargs)
        authority = self.get_object()
        context['authority'] = authority
        return context
