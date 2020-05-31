# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0013_auto_20200531_0849'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(help_text='First name in original language', max_length=50, verbose_name='firstname')),
                ('last_name', models.CharField(help_text='Last name in original language', max_length=50, verbose_name='lastname')),
                ('first_name_lat', models.CharField(help_text='First name in latin characters, usage form', max_length=50, null=True, verbose_name='firstname_lat', blank=True)),
                ('last_name_lat', models.CharField(help_text='Last name in latin character, usage form', max_length=50, null=True, verbose_name='lastname_lat', blank=True)),
                ('first_name_translit', models.CharField(help_text='First name transliterated', max_length=50, null=True, verbose_name='firstname_translit', blank=True)),
                ('last_name_translit', models.CharField(help_text='Last name transliterated', max_length=50, null=True, verbose_name='lastname_translit', blank=True)),
                ('birth', models.DateField(help_text='YYYY-MM-DD', null=True, verbose_name='birth', blank=True)),
                ('death', models.DateField(help_text='YYYY-MM-DD', null=True, verbose_name='death', blank=True)),
                ('biography', models.TextField(null=True, verbose_name='biography', blank=True)),
                ('isni', models.PositiveIntegerField(help_text='International Standard Name Identifier', null=True, verbose_name='isni', blank=True)),
            ],
            options={
                'db_table': 'media_authority',
                'verbose_name': 'authority',
                'verbose_name_plural': 'authorities',
            },
        ),
        migrations.CreateModel(
            name='Responsability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authority', models.ForeignKey(to='telemeta.Authority')),
                ('collection', models.ForeignKey(to='telemeta.MediaCollection')),
                ('item', models.ForeignKey(to='telemeta.MediaItem')),
            ],
            options={
                'db_table': 'media_responsability',
                'verbose_name': 'responsability',
                'verbose_name_plural': 'responsabilites',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intitule', models.CharField(help_text='List of roles', max_length=50, verbose_name='role')),
            ],
            options={
                'db_table': 'media_role',
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
        ),
        migrations.AddField(
            model_name='responsability',
            name='role',
            field=models.ForeignKey(to='telemeta.Role'),
        ),
    ]
