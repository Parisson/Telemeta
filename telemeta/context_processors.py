from django.conf import settings
from telemeta.views.enum import *

def menu(request):
    EnumView().set_enum_file()
    return {'menu': EnumView().enu}