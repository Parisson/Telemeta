# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Cooperative Artefacts <artefacts.lle@gmail.com>


from telemeta.models.core import *
from django.utils.translation import ugettext_lazy as _

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Institution(ModelCore):
    "Institution who owns some resources"

    name = CharField(_('name'), required=True)
    notes = TextField(_('notes'))

    @property
    def has_fonds(self):
        if self.objects.MediaFonds.all().count()>0 :
            return True
        return False

    @property
    def fonds(self):
        "Return the fonds of the institution"
        fonds = self.objects.MediaFonds.all()
        return fonds

        fonds.verbose_name = _("fonds")

    @property
    def notes_markdown(self):
        return markdownify(self.notes)

    class Meta(MetaCore):
        db_table = 'institutions'
        verbose_name_plural = _('institutions')
        ordering = ['name']

    def __unicode__(self):
        return self.name
