from haystack.routers import BaseRouter
from telemeta.models.instrument import Instrument, InstrumentAlias
from telemeta.models.location import LocationAlias, Location

#Router in order to determine
#that autocomplete data are stored in "autocomplete" index
class AutoRouter(BaseRouter):

    def for_write(self, **hints):
        obj = hints.get('instance')
        if isinstance(obj, Instrument) or isinstance(obj, InstrumentAlias) or isinstance(obj, Location) \
                or isinstance(obj, LocationAlias):
            return 'autocomplete'
        else:
            return None