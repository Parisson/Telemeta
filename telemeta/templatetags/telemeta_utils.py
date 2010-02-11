from django import template
from django.utils.http import urlquote
from telemeta import models
from django.core.urlresolvers import reverse
import telemeta.models.dublincore as dc
from django.utils import html
from django import template
from django.utils.text import capfirst
from telemeta import models
from django.utils.translation import ungettext

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
def build_query_string(vars):
    """Build an HTTP query string out of a dict"""
    if type(vars) == dict:
      import urllib
      args = []
      for k, v in vars.iteritems():
          if not isinstance(v, basestring):
              v = unicode(v)
          args.append(urlquote(k) + '=' + urlquote(v))

      return "&amp;".join(args)
    return ''

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
def to_dublincore(resource):
    if isinstance(resource, models.MediaItem):
        return dc.express_item(resource)
    else:
        return dc.express_collection(resource)

class DescriptionListFieldNode(template.Node):
    def __init__(self, model, attr, join_with = None):
        self.model  = model
        self.member = attr
        self.join_with = join_with

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
        if value:
            value = html.escape(unicode(value))
            markup  = '<dt>%s</dt><dd>%s</dd>' % (label, value)
            return markup

        return ''

@register.tag
def dl_field(parser, token):
    cut = token.split_contents()
    join_with = None
    try:
        tag_name, model, attr = cut
    except ValueError:
        try:
            tag_name, model, attr, arg3, arg4, arg5  = cut
            if arg3 == 'join' and arg4 == 'with'and arg5[0] == arg5[-1] and arg5[0] in ('"', "'"):
                join_with = arg5[1:-1]
            else:
                raise ValueError()
        except ValueError:
            raise template.TemplateSyntaxError("%r tag: invalid arguments" 
                                               % token.contents.split()[0])

    if attr[0] == attr[-1] and attr[0] in ('"', "'"):
        attr = attr[1:-1]
    else:
        attr = template.Variable(attr)
    model = template.Variable(model)
    return DescriptionListFieldNode(model, attr, join_with=join_with)

@register.filter
def prepend(str, prefix):
    if str:
        return prefix + unicode(str)
    return ''

@register.simple_tag
def field_label(model, field):
    if isinstance(model, basestring):
        model = getattr(models, model)
            
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
