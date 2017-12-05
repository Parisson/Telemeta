# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0003_auto_20171204_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediacorpus',
            name='description',
        ),
        migrations.RemoveField(
            model_name='mediafonds',
            name='description',
        ),
        migrations.RemoveField(
            model_name='mediacollection',
            name='booklet_author',
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='booklet_author',
            field=models.ManyToManyField(related_name='booklet_author', null=True, verbose_name='booklet_author', to='telemeta.Authority', blank=True),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='collectors',
            field=models.ManyToManyField(related_name='collectors', null=True, verbose_name='collectors', to='telemeta.Authority', blank=True),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='informer',
            field=models.ManyToManyField(related_name='informers', null=True, verbose_name='informers', to='telemeta.Authority', blank=True),
        ),
        migrations.RemoveField(
            model_name='mediacollection',
            name='language_iso',
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='language_iso',
            field=models.ManyToManyField(related_name='collections', null=True, verbose_name='Language (ISO norm)', to='telemeta.Language', blank=True),
        ),
        migrations.RemoveField(
            model_name='mediacollection',
            name='location',
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='location',
            field=models.ManyToManyField(related_name='locations', null=True, verbose_name='location', to='telemeta.Authority', blank=True),
        ),
        migrations.AlterField(
            model_name='mediacollection',
            name='location_details',
            field=markdownx.models.MarkdownxField(verbose_name='location details', blank=True),
        ),
        migrations.RemoveField(
            model_name='mediacollection',
            name='publisher',
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='publisher',
            field=models.ManyToManyField(related_name='collections', null=True, verbose_name='publishers', to='telemeta.Publisher', blank=True),
        ),
        migrations.RemoveField(
            model_name='mediacollection',
            name='publisher_collection',
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='publisher_collection',
            field=models.ManyToManyField(related_name='collections', null=True, verbose_name='publisher collection', to='telemeta.PublisherCollection', blank=True),
        ),
    ]
