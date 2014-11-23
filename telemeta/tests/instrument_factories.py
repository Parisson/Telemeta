# -*- coding: utf-8 -*-
"""
Factories for the telemeta.models.instrument

"""
import factory

from telemeta.models.instrument import Instrument


class InstrumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instrument

    name = factory.Sequence(lambda n: 'name{0}'.format(n))
