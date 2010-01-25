from django import template
from django.utils.http import urlquote
from telemeta.models import MediaItem, MediaCollection
from django.core.urlresolvers import reverse
import telemeta.models.dublincore as dc

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
    return isinstance(resource, MediaItem)

@register.filter
def is_collection(resource):
    return isinstance(resource, MediaCollection)

@register.filter
def to_dublincore(resource):
    if isinstance(resource, MediaItem):
        return dc.express_item(resource)
    else:
        return dc.express_collection(resource)
