
from telemeta.views.enum import *
def menu(request):
        EnumView().set_enum_file(request)
        return {'menu': EnumView().enu}
