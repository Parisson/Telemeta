# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0005_auto_20171205_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaitem',
            name='mshs_domain',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Domain', blank=True, choices=[(b'T', b'T\xc3\xa9moignage'), (b'C', b'Chanson'), (b'A', b'Autre expression vocale'), (b'I', b'Expression instrumentale'), (b'R', b'Conte ou r\xc3\xa9cit l\xc3\xa9gendaire')]),
        ),
    ]
