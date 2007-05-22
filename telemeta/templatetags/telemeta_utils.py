from django import template

register = template.Library()


#@register.filter
#def cleanid(value):
#    "Escapes a value for use in a URL (converts slashes)"
#    return value.replace('/', '--')

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


