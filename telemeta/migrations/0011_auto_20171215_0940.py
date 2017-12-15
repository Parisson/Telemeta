# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0010_auto_20171210_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediacollectionperformance',
            name='number',
            field=telemeta.models.fields.IntegerField(default=1, verbose_name='number', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_author',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Auteur(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_composer',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Compositeur(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_dance',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Danse(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_dance_details',
            field=telemeta.models.fields.TextField(default=b'', verbose_name='Pr\xe9cisions sur la danse', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_deposit_digest',
            field=telemeta.models.fields.TextField(default=b'', verbose_name='R\xe9sum\xe9', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_deposit_names',
            field=telemeta.models.fields.CharField(default=b'', help_text='First name, Last name ; First name, Last name', max_length=250, verbose_name='Nom(s) propre(s) cit\xe9(s) ', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_deposit_periods',
            field=telemeta.models.fields.CharField(default=b'', help_text='Period recounted; period recounted; ...', max_length=250, verbose_name='P\xe9riode(s) cit\xe9e(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_deposit_places',
            field=telemeta.models.fields.CharField(default=b'', help_text='Place named; place named; ...', max_length=250, verbose_name='Lieu(x) cit\xe9(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_deposit_thematic',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Th\xe9matiques', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_details',
            field=telemeta.models.fields.TextField(default=b'', verbose_name="Pr\xe9cisions sur l'item", blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_domain_music',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Expression instrumentale', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_domain_tale',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Conte', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_domain_vocal',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Autre expression vocale', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_function',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Fonction(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_group',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Formation', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_informers',
            field=models.ManyToManyField(to='telemeta.MediaCollectionPerformance', verbose_name='Informateur(s)'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_melody',
            field=telemeta.models.fields.TextField(default=b'', help_text='You can use ABC notation', verbose_name='M\xe9lodie (transcription alphab\xe9tique)', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_musical_organization',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Organisation musicale', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_timbre',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name="Timbre de l'air", blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_timbre_code',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Cote du timbre', blank=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='mshs_timbre_ref',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='Timbre(s) r\xe9f\xe9renc\xe9(s)', blank=True),
        ),
    ]
