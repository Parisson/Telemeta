from django import template

register = template.Library()


#@register.filter
#def cleanid(value):
#    "Escapes a value for use in a URL (converts slashes)"
#    return value.replace('/', '--')


