# -*- coding: utf-8 -*-

from . instrument_factories import InstrumentFactory
import pytest


@pytest.mark.django_db
def test_Instrument():
    instrument = InstrumentFactory.build()
