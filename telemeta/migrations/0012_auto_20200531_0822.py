# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0011_authority_isni'),
    ]

    operations = [
        migrations.AddField(
            model_name='authority',
            name='first_name_lat',
            field=models.CharField(help_text='First name in latin characters, usage form', max_length=50, null=True, verbose_name='firstname_lat', blank=True),
        ),
        migrations.AddField(
            model_name='authority',
            name='first_name_translit',
            field=models.CharField(help_text='First name transliterated', max_length=50, null=True, verbose_name='firstname_translit', blank=True),
        ),
        migrations.AddField(
            model_name='authority',
            name='last_name_lat',
            field=models.CharField(help_text='Last name in latin character, usage form', max_length=50, null=True, verbose_name='lastname_lat', blank=True),
        ),
        migrations.AddField(
            model_name='authority',
            name='last_name_translit',
            field=models.CharField(help_text='Last name transliterated', max_length=50, null=True, verbose_name='lastname_translit', blank=True),
        ),
        migrations.AlterField(
            model_name='authority',
            name='first_name',
            field=models.CharField(help_text='First name in original language', max_length=50, verbose_name='firstname'),
        ),
        migrations.AlterField(
            model_name='authority',
            name='last_name',
            field=models.CharField(help_text='Last name in original language', max_length=50, verbose_name='lastname'),
        ),
    ]
