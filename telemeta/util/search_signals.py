from django.db import models
from haystack import signals
from telemeta.models import *

class RealTimeCustomSignal(signals.RealtimeSignalProcessor):

    def __init__(self, *args, **kwargs):
        super(RealTimeCustomSignal, self).__init__(*args, **kwargs)
        self.update_list = []

    def handle_pre_save(self, sender, instance, **kwargs):
        import sys
        if(sender == MediaItem):
             print(sender, instance.is_dirty(check_relationship=True), instance.get_dirty_fields(check_relationship=True))
        sys.stdout.flush()
        if sender == MediaItem and instance.is_dirty(check_relationship=True) and instance.get_dirty_fields(check_relationship=True).has_key('location'):
            self.update_list.append(Location)

    def handle_save(self, sender, instance, **kwargs):
        import sys
        if sender == MediaItem and sender in self.update_list:
            print("OKOK")
            sys.stdout.flush()
        del self.update_list[:]
        print("okk")
        sys.stdout.flush()
        super(RealTimeCustomSignal, self).handle_save(sender, instance, **kwargs)

    def setup(self):
        super(RealTimeCustomSignal, self).setup()
        models.signals.pre_save.connect(self.handle_pre_save)