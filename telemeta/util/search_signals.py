from django.db import models
from haystack import signals
from telemeta.models import *
from telemeta.search_indexes import *
from django.db.models import Q

class RealTimeCustomSignal(signals.RealtimeSignalProcessor):

    handleModels = (MediaItem,)

    def __init__(self, *args, **kwargs):
        super(RealTimeCustomSignal, self).__init__(*args, **kwargs)
        self.update_model = None

    def post_save_mediaitem(self, object):
        if object.get_dirty_fields(check_relationship=True).has_key('location'):
            id = object.get_dirty_fields(check_relationship=True).get('location')
            locs = Location.objects.filter(Q(pk=id)|Q(past_names__pk=id)|Q(descendant_relations__location__pk=id))
            localias = LocationAlias.objects.filter(location__id=id)
            for loc in locs:
                LocationIndex().remove_object(instance=loc, using='autocomplete')
            for loc in localias:
                LocationAliasIndex().remove_object(instance=loc, using='autocomplete')
            if object.location is not None:
                locs = MediaItem.objects.filter(id=object.id).locations()
                localias = LocationAlias.objects.filter(location__pk=object.location.id)
                for loc in locs:
                    LocationIndex().update_object(instance=loc, using='autocomplete')
                for loc in localias:
                    LocationAliasIndex().update_object(instance=loc, using='autocomplete')

    def handle_pre_save(self, sender, instance, **kwargs):
        if sender in self.handleModels and instance.is_dirty(check_relationship=True):
            self.update_model = sender

    def handle_save(self, sender, instance, **kwargs):
        if sender == self.update_model:
            getattr(self, "post_save_%s" % str(sender).split('.')[-1][:-2].lower())(instance)
        self.update_model = None
        super(RealTimeCustomSignal, self).handle_save(sender, instance, **kwargs)

    def setup(self):
        super(RealTimeCustomSignal, self).setup()
        models.signals.pre_save.connect(self.handle_pre_save)