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


class AuthorityListView(ListView):

    model = Authority
    template_name = "telemeta/authority_list.html"
    paginate_by = 20
    queryset = Authority.objects.order_by('name')

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
