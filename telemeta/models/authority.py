# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Cooperative Artefacts <artefacts.lle@gmail.com>


from telemeta.models.core import *
from django.utils.translation import ugettext_lazy as _

class Authority(ModelCore):
    "People who produced something."

    last_name = CharField(_('last name'), required=True)
    first_name = CharField(_('first name') )
    civilite =  CharField(_('civilite') )
    alias =  CharField( _('alias') )
    birth_date = DateField(null=True)
    birth_location = ForeignKey('Location', related_name='birth_location', verbose_name=_('birth location'), blank=True, null=True, on_delete=models.SET_NULL)
    death_date = DateField( null=True )
    death_location = ForeignKey('Location',related_name='death_location', verbose_name=_('death location'), blank=True, null=True, on_delete=models.SET_NULL)
    biography = TextField( _('biography'), null=True, blank=True )
    uri = URLField(_('URI'), null=True, blank=True)


    class Meta(MetaCore):
        db_table = 'authorities'
        verbose_name = _('authority')
        verbose_name_plural = _('authorities')

    def __unicode__(self):
        if self.civilite :
            return '%s %s %s' % (self.civilite,  self.first_name, self.last_name)
        return '%s %s' % (self.first_name, self.last_name)
