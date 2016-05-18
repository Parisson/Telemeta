from django.db import models
from haystack import signals
from telemeta.models import *
from telemeta.search_indexes import *
from django.db.models import Q

#Custom realtime signal in order to update the "autcomplete" index
#when add/remove instruments/locations in items.
#Differences of values of fields are checked by the tracker
#of django-dirtyfields' module
class RealTimeCustomSignal(signals.RealtimeSignalProcessor):
    handleFields = ('location', 'instrument', 'alias')
    handleModels = (MediaItem, MediaItemPerformance, )

    def __init__(self, *args, **kwargs):
        super(RealTimeCustomSignal, self).__init__(*args, **kwargs)
        self.update_fields = []

    def post_save_location(self, object):
        id = object.get_dirty_fields(check_relationship=True).get('location')
        locs = Location.objects.filter(Q(pk=id) | Q(past_names__pk=id) | Q(descendant_relations__location__pk=id))
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


    def post_save_instrument(self, object):
        id = object.get_dirty_fields(check_relationship=True).get('instrument')
        if id is not None:
             instru = Instrument.objects.get(pk=id)
             InstrumentIndex().remove_object(instance=instru, using='autocomplete')
        if object.instrument is not None:
            newinstru = Instrument.objects.get(id=object.instrument.id)
            InstrumentIndex().update_object(instance=newinstru, using='autocomplete')

    def post_save_alias(self, object):
        id = object.get_dirty_fields(check_relationship=True).get('alias')
        if id is not None:
             alias = InstrumentAlias.objects.get(pk=id)
             InstrumentAliasIndex().remove_object(instance=alias, using='autocomplete')
        if object.alias is not None:
            newalias = InstrumentAlias.objects.get(id=object.alias.id)
            InstrumentAliasIndex().update_object(instance=newalias, using='autocomplete')

    def handle_pre_save(self, sender, instance, **kwargs):
        if sender in self.handleModels and instance.is_dirty(check_relationship=True):
            for field in instance.get_dirty_fields(check_relationship=True).keys():
                if field in self.handleFields:
                    self.update_fields.append(field)

    def handle_pre_delete(self, sender, instance, **kwargs):
        InstrumentIndex().remove_object(instance=instance.instrument, using='autocomplete')
        InstrumentAliasIndex().remove_object(instance=instance.alias, using='autocomplete')

    def handle_save(self, sender, instance, **kwargs):
        import sys
        print(sender, self.update_fields)
        sys.stdout.flush()
        if sender in self.handleModels:
            for field in self.update_fields:
                getattr(self, "post_save_%s" % field)(instance)
        del self.update_fields[:]
        super(RealTimeCustomSignal, self).handle_save(sender, instance, **kwargs)

    def setup(self):
        super(RealTimeCustomSignal, self).setup()
        models.signals.pre_save.connect(self.handle_pre_save)
        models.signals.pre_delete.connect(self.handle_pre_delete, sender=MediaItemPerformance)
