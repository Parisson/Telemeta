from django.conf import settings
from telemeta.views.enum import *

def menu(request):
    return {'menu': EnumView().enu}