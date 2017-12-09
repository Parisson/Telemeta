# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Cooperative Artefacts <artefacts.lle@gmail.com>

from telemeta.views.core import *
from telemeta.views.core import serve_media

from telemeta.forms.institution import *
import sys
import time


class InstitutionViewMixin(object):

    model = Institution
    form_class = InstitutionForm


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


class InstitutionListView(ListView):

    model = Institution
    template_name = "telemeta/institution_list.html"
    paginate_by = 20
    queryset = Institution.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data(**kwargs)
        context['count'] = self.object_list.count()
        return context


class InstitutionDetailView(InstitutionViewMixin, DetailView):

    template_name = 'telemeta/institution_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InstitutionDetailView, self).get_context_data(**kwargs)
        institution = self.get_object()
        context['institution'] = institution
        return context
