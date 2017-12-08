from django import template
from telemeta import models

register = template.Library()


@register.filter
def label_domain(domains):
    # Return a composed string which match with every domain

    res = ''
    list_domain = domains.split(',')

    # Make a dictionnary with the domain's list
    dico = dict(models.MediaItem.DOMAINS)

    # compose the string to return
    for domain in list_domain :
        # subsitute whith the corresponding label
        label = dico[domain]
        res = res+label+', '

    # remove the last comma
    res = res.rstrip(', ')

    return res
