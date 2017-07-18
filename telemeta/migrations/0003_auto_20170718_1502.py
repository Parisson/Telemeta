# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0002_auto_20170424_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediacollection',
            name='acquisition_mode',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.AcquisitionMode', null=True, verbose_name='mode of acquisition'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='ad_conversion',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.AdConversion', null=True, verbose_name='digitization'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='copy_type',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.CopyType', null=True, verbose_name='copy type'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='legal_rights',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.LegalRight', null=True, verbose_name='legal rights'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='media_type',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.MediaType', null=True, verbose_name='media type'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='metadata_author',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.MetadataAuthor', null=True, verbose_name='record author'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='metadata_writer',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.MetadataWriter', null=True, verbose_name='record writer'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='original_format',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.OriginalFormat', null=True, verbose_name='original format'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='physical_format',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.PhysicalFormat', null=True, verbose_name='archive format'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='publisher',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Publisher', null=True, verbose_name='publisher'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='publisher_collection',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.PublisherCollection', null=True, verbose_name='publisher collection'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='publishing_status',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.PublishingStatus', null=True, verbose_name='secondary edition'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='recording_context',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.RecordingContext', null=True, verbose_name='recording context'),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='status',
            field=telemeta.models.fields.ForeignKey(related_name='collections', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Status', null=True, verbose_name='collection status'),
        ),
        migrations.AlterField(
            model_name='mediacollectionidentifier',
            name='type',
            field=telemeta.models.fields.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.IdentifierType', null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='ethnic_group',
            field=telemeta.models.fields.ForeignKey(related_name='items', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.EthnicGroup', null=True, verbose_name='population / social group'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='generic_style',
            field=telemeta.models.fields.ForeignKey(related_name='items', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.GenericStyle', null=True, verbose_name='generic style'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='location',
            field=telemeta.models.fields.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Location', null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='media_type',
            field=telemeta.models.fields.ForeignKey(related_name='items', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.MediaType', null=True, verbose_name='media type'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='organization',
            field=telemeta.models.fields.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Organization', null=True, verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='rights',
            field=telemeta.models.fields.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Rights', null=True, verbose_name='rights'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='topic',
            field=telemeta.models.fields.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Topic', null=True, verbose_name='topic'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='vernacular_style',
            field=telemeta.models.fields.ForeignKey(related_name='items', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.VernacularStyle', null=True, verbose_name='vernacular style'),
        ),
        migrations.AlterField(
            model_name='mediaitemidentifier',
            name='type',
            field=telemeta.models.fields.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.IdentifierType', null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='mediaitemperformance',
            name='alias',
            field=telemeta.models.fields.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.InstrumentAlias', null=True, verbose_name='vernacular name'),
        ),
        migrations.AlterField(
            model_name='mediaitemperformance',
            name='instrument',
            field=telemeta.models.fields.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Instrument', null=True, verbose_name='composition'),
        ),
    ]
