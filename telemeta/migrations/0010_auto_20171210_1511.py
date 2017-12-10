# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0009_auto_20171207_2142'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='mediaitem',
        #     name='collectors',
        #     field=models.ManyToManyField(related_name='item_collectors', null=True, verbose_name='collectors', to='telemeta.Authority', blank=True),
        # ),
        migrations.AlterField(
            model_name='mediacorpus',
            name='recorded_from_year',
            field=telemeta.models.fields.IntegerField(default=None, help_text='YYYY', null=True, verbose_name='recording year (from)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediacorpus',
            name='recorded_to_year',
            field=telemeta.models.fields.IntegerField(default=None, help_text='YYYY', null=True, verbose_name='recording year (until)', blank=True),
        ),
        # migrations.RemoveField(
        #     model_name='mediaitem',
        #     name='collector',
        # ),
        # migrations.AddField(
        #     model_name='mediaitem',
        #     name='collector',
        #     field=telemeta.models.fields.CharField(default=b'', help_text='First name, Last name ; First name, Last name', max_length=250, verbose_name='collector', blank=True),
        # ),
    ]
