from django import template
from django.utils.http import urlquote
from telemeta import models
from django.core.urlresolvers import reverse
import telemeta.models.dublincore as dc
from django.utils import html
from django import template
from django.utils.text import capfirst
from django.utils.translation import ungettext
from docutils.core import publish_parts
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django import db
import re
import os
import datetime
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def tolist(dict):
    "Converts a simple dict into a list"
    list = []
    for k, v in dict.iteritems():
        list.append({'name': k, 'value': v})
    return list

@register.filter
def mul(value, arg):
    "Multiply a numeric value"
    return value * arg

class TelemetaVersionNode(template.Node):
    def render(self, context):
        from telemeta import __version__
        return __version__

@register.tag
def telemeta_version(parser, token):
    "Get Telemeta version number"
    return TelemetaVersionNode()

class TelemetaUrlNode(template.Node):
    def render(self, context):
        from telemeta import __url__
        return __url__

@register.tag
def telemeta_url(parser, token):
    "Get Telemeta project homepage URL"
    return TelemetaUrlNode()

_js_escapes = (
    ('\\', '\\\\'),
    ('"', '\\"'),
    ("'", "\\'"),
    ('\n', '\\n'),
    ('\r', '\\r'),
    ('\b', '\\b'),
    ('\f', '\\f'),
    ('\t', '\\t'),
    ('\v', '\\v'),
    ('</', '<\\/'),
)
@register.filter
def escapejs(value):
    """Backslash-escapes characters for use in JavaScript strings."""
    for bad, good in _js_escapes:
        value = value.replace(bad, good)
    return value

@register.filter
def build_pattern_string(criteria):
    dict = {}
    for c in criteria:
        dict[c.key] = c.value
    return dict

@register.filter
def build_query_string(vars):
    """Build an HTTP query string out of a dict"""
    if type(vars) == dict:
      import urllib
      args = []
      for k, v in vars.iteritems():
          if isinstance(v, db.models.Model):
              v = v.pk
          elif not isinstance(v, basestring):
              v = unicode(v)
          args.append(urlquote(k) + '=' + urlquote(v))

      return "&amp;".join(args)
    return ''

@register.filter
def with_no_sound(vars):
    _vars = vars.copy()
    if type(_vars) == dict:
        if u'sound' in _vars:
            del _vars[u'sound']
    return _vars

@register.filter
def with_sound(vars):
    _vars = vars.copy()
    if type(_vars) == dict:
        if not 'sound' in _vars:
            _vars['sound'] = True
    return _vars

@register.filter
def code_or_id(resource):
    if resource.code:
        return resource.code
    else:
        return resource.id

@register.filter
def is_item(resource):
    return isinstance(resource, models.MediaItem)

@register.filter
def is_collection(resource):
    return isinstance(resource, models.MediaCollection)

@register.filter
def is_corpus(resource):
    return isinstance(resource, models.MediaCorpus)

@register.filter
def is_fonds(resource):
    return isinstance(resource, models.MediaFonds)

@register.filter
def is_resource(resource):
    return is_fonds(resource) or is_corpus(resource)

@register.filter
def to_dublincore(resource):
    if isinstance(resource, models.MediaItem):
        return dc.express_item(resource)
    elif isinstance(resource, models.MediaCollection):
        return dc.express_collection(resource)
    else:
        return dc.express_generic_resource(resource)

class DescriptionListFieldNode(template.Node):
    def __init__(self, model, attr, join_with = None, show_empty = False):
        self.model  = model
        self.member = attr
        self.join_with = join_with
        self.show_empty = show_empty

    def render(self, context):
        try:
            model = self.model.resolve(context)
            if isinstance(self.member, template.Variable):
                member = self.member.resolve(context)
            else:
                member = self.member
            label = html.escape(capfirst(unicode(model.field_label(member))))
            try:
                value = getattr(model, member)
            except AttributeError:
                value = '<ERROR: no such field>'
        except template.VariableDoesNotExist:
            label = unicode(self.model) + '.' + self.member
            value = '<ERROR: can\'t find variable>'

        try:
            value = value()
        except TypeError:
            pass
        if self.join_with:
            value = self.join_with.join([unicode(v) for v in value])
        if not value:
            value = ''
        if value or self.show_empty:
            value = html.escape(unicode(value))
            markup  = '<dt>%s</dt><dd>%s</dd>' % (label, value)
            return markup

        return ''

@register.tag
def dl_field(parser, token):
    cut = token.split_contents()
    join_with = None
    show_empty = False
    if len(cut) == 3:
        tag_name, model, attr = cut
    elif len(cut) == 4:
        tag_name, model, attr, arg3 = cut
        if arg3 == 'placeholder':
            show_empty = True
        else:
            raise ValueError()
    elif len(cut) >= 6:
        tag_name, model, attr, arg3, arg4, arg5  = cut[0:6]
        if arg3 == 'join' and arg4 == 'with'and arg5[0] == arg5[-1] and arg5[0] in ('"', "'"):
            join_with = arg5[1:-1]
        else:
            raise ValueError()
        if len(cut) > 6:
            if cut[6] == 'placeholder':
                show_empty = True
            else:
                raise ValueError();
    else:
        raise template.TemplateSyntaxError("%r tag: invalid arguments"
                                           % token.contents.split()[0])

    if attr[0] == attr[-1] and attr[0] in ('"', "'"):
        attr = attr[1:-1]
    else:
        attr = template.Variable(attr)
    model = template.Variable(model)
    return DescriptionListFieldNode(model, attr, join_with=join_with, show_empty=show_empty)

@register.filter
def prepend(str, prefix):
    if str:
        return prefix + unicode(str)
    return ''

@register.simple_tag
def field_label(model, field=None):
    if isinstance(model, basestring):
        model = getattr(models, model)

    if not field:
        return capfirst(unicode(model._meta.verbose_name))

    return capfirst(unicode(model.field_label(field)))

@register.simple_tag
def field_value(object, member):
    value = getattr(object, member)
    try:
        value = value()
    except TypeError:
        pass
    return value

@register.filter
def is_none(value):
    return value is None

@register.filter
def resources_num(value):
    model = value.model
    count = value.count()
    label = str(count)
    if model == models.MediaItem:
        label = ungettext('%(count)d item', '%(count)d items', count) % {
            'count': count, }
    elif model == models.MediaCollection:
        label = ungettext('%(count)d collection', '%(count)d collections', count) % {
            'count': count, }

    return label

@register.filter
def split(value, sep=','):
    return value.split(sep)

@register.simple_tag
def variable_link(object, url_name, url_key):
    return reverse(url_name, args=[field_value(object, url_key)])

@register.filter
def equals(value1, value2):
    return value1 == value2

@register.filter
def render_flatpage(content):
    parsed = ""
    path = getattr(content, 'path', '')
    if isinstance(content, basestring):
        content = content.split("\n")

    for line in content:
        match = re.match('^(\.\. *(?:_[^:]*:|(?:\|\w+\|)? *image::) *)([^ ]+) *$', line)
        if match:
            directive, urlname = match.groups()
            line = directive
            try:
                i = urlname.index('telemeta-')
            except ValueError:
                i = -1
            if i == 0:
                line += reverse(urlname)
            elif urlname[:1] != '/':
                line += reverse('telemeta-flatpage', args=[path + '/../' + urlname])
            else:
                line += urlname

        parsed += line + "\n"

    parts = publish_parts(source=smart_str(parsed), writer_name="html4css1", settings_overrides={})
    return mark_safe('<div class="rst-content">\n' + force_unicode(parts["html_body"]) + '</div>')
render_flatpage.is_safe = True

@register.simple_tag
def organization():
    return settings.TELEMETA_ORGANIZATION

@register.simple_tag
def description():
    try:
        description = settings.TELEMETA_OAI_REPOSITORY_NAME
    except:
        description = settings.TELEMETA_DESCRIPTION
        pass
    return description

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""

@register.tag
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

@register.simple_tag
def current_year():
    return datetime.datetime.now().strftime("%Y")

@register.filter
def html_line_break(text):
    return text.replace('\n', '<br />')

@register.simple_tag
def profile(user):
    return user.get_profile()

@register.filter
def to_string(list):
    if len(list) != 0:
        return list[0].encode('utf-8')
    else:
        return ''

@register.filter
def get_filename(object):
    if isinstance(object, unicode):
       return object.split('/')[-1]
    else:
        return object.path.split(os.sep)[-1]

@register.filter
def get_youtube(link):
    link = link.split('&')
    if "=" in link[0]:
        ref = link[0].split('=')[1]
    else:
        ref = link[0].split('/')[-1]
    return 'http://www.youtube.com/embed/'+ref

@register.filter
def to_utf8(word):
    return word.encode('utf-8')

@register.filter
@stringfilter
def capitalize(value):
    return value.capitalize()

@register.filter
@stringfilter
def mime_to_ext(mime_type):
    return mime_type.split('/')[1]

@register.filter
@stringfilter
def mime_to_media_type(mime_type):
    if 'video' in mime_type:
        return 'Video'
    else:
        return 'Audio'

