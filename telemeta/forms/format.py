import django.forms as forms
from django.forms import ModelForm
from telemeta.models import *


class FormatForm(ModelForm):
    class Meta:
        model = Format
        exclude = ('item',)
