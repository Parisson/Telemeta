# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0025_auto_20170922_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Illustration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=191, verbose_name='name')),
            ],
            options={
                'verbose_name': 'illustration',
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=191, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Support',
            },
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='disc',
            name='duration',
            field=models.CharField(max_length=50, verbose_name='duration', blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='contient_contenu_dans',
            field=models.ManyToManyField(related_name='_document_contient_contenu_dans_+', verbose_name='Contient ou contenu dans', to='mcm.Document'),
        ),
        migrations.AddField(
            model_name='document',
            name='page_num',
            field=models.CharField(max_length=50, verbose_name='number of pages', blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='parents',
            field=models.ManyToManyField(related_name='_document_parents_+', verbose_name='Contient ou contenu dans', to='mcm.Document'),
        ),
        migrations.AddField(
            model_name='photo',
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='posterbooklet',
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='video',
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.CharField(max_length=50, verbose_name='duration', blank=True),
        ),
        migrations.AddField(
            model_name='videofile',
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='videofile',
            name='duration',
            field=models.CharField(max_length=50, verbose_name='duration', blank=True),
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='illustration',
            field=models.ForeignKey(verbose_name='illustration', blank=True, to='mcm.Illustration', null=True),
        ),
        migrations.AddField(
            model_name='disc',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='illustration',
            field=models.ForeignKey(verbose_name='illustration', blank=True, to='mcm.Illustration', null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
        migrations.AddField(
            model_name='posterbooklet',
            name='illustration',
            field=models.ForeignKey(verbose_name='illustration', blank=True, to='mcm.Illustration', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
        migrations.AddField(
            model_name='videofile',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
    ]
