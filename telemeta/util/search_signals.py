from telemeta.models import *
from haystack import signals
from django.db.models.signals import post_save, post_delete, pre_delete
from django.db.models import Q

#Custom realtime signal in order to update the "autocomplete" index
#when add/remove instruments/locations in items.
#Differences of values of fields are checked by the tracker
#of django-dirtyfields' module
class RealTimeCustomSignal(signals.RealtimeSignalProcessor):

    sender_auto_only = (Instrument, InstrumentAlias, Location, LocationAlias)

    def __init__(self, *args, **kwargs):
        super(RealTimeCustomSignal, self).__init__(*args, **kwargs)

    def update_instrument(self, instance, old_value):
        if instance is not None and instance.instrument is not None:
            post_save.send(sender=Instrument, instance=instance.instrument, in_real_signal=True)
        if old_value is not None:
            instru = Instrument.objects.get(id=old_value) if not isinstance(old_value, Instrument) else old_value
            nb = instru.performances.count()
            if nb == 0:
                post_delete.send(sender=Instrument, instance=instru)

    def update_alias(self, instance, old_value):
        if instance is not None and instance.alias is not None:
            post_save.send(sender=InstrumentAlias, instance=instance.alias, in_real_signal=True)
        if old_value is not None:
            alias = InstrumentAlias.objects.get(id=old_value) if not isinstance(old_value, InstrumentAlias) else old_value
            nb = alias.performances.count()
            if nb == 0:
                post_delete.send(sender=InstrumentAlias, instance=alias)

    def update_location(self, instance, old_value):
        if instance is not None and instance.location is not None:
            loc = Location.objects.filter(Q(current_location=instance.location)|Q(descendant_relations__location=instance.location))
            localias = LocationAlias.objects.filter(location=instance.location)
            post_save.send(sender=Location, instance=instance.location, in_real_signal=True)
            for l in loc:
                post_save.send(sender=Location, instance=l, in_real_signal=True)
            for l in localias:
                post_save.send(sender=LocationAlias, instance=l, in_real_signal=True)
        if old_value is not None:
            location = Location.objects.get(id=old_value) if not isinstance(old_value, Location) else old_value
            loc = Location.objects.filter(Q(current_location=location) | Q(descendant_relations__location=location))
            can_delete_alias = post_delete.send(sender=Location, instance=location, in_real_signal=True)[0][1]
            for l in loc:
                post_delete.send(sender=Location, instance=l, in_real_signal=True)
            if can_delete_alias:
                localias = LocationAlias.objects.filter(location=location)
                for l in localias:
                     post_delete.send(sender=LocationAlias, instance=l, in_real_signal=True)

    def handle_save(self, sender, instance, **kwargs):
        if sender == MediaItemPerformance or sender == MediaItem:
            df = instance.get_dirty_fields(check_relationship=True)
            if df.has_key('instrument'):
                self.update_instrument(instance, df.get('instrument'))
            if df.has_key('alias'):
                self.update_alias(instance, df.get('alias'))
            if df.has_key('location'):
                self.update_location(instance, df.get('location'))
        if kwargs.get('in_real_signal', False) or sender not in self.sender_auto_only:
             super(RealTimeCustomSignal, self).handle_save(sender, instance, **kwargs)

    def handle_delete(self, sender, instance, **kwargs):
        if sender == MediaItemPerformance:
            self.update_instrument(instance=None, old_value=instance.instrument)
            self.update_alias(instance=None, old_value=instance.alias)
        elif sender == MediaItem:
            self.update_location(instance=None, old_value=instance.location)
        elif sender == Location:
            l = Location.objects.filter(Q(past_names=instance)|Q(ancestor_relations__ancestor_location=instance)|Q(id=instance.id))
            if l.count() != 0 and l.filter(mediaitem__isnull=False).exists():
                return False
        super(RealTimeCustomSignal, self).handle_delete(sender=sender, instance=instance, **kwargs)
        return True