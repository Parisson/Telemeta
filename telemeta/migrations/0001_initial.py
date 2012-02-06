# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhysicalFormat'
        db.create_table('physical_formats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['PhysicalFormat'])

        # Adding model 'PublishingStatus'
        db.create_table('publishing_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['PublishingStatus'])

        # Adding model 'AcquisitionMode'
        db.create_table('acquisition_modes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['AcquisitionMode'])

        # Adding model 'MetadataAuthor'
        db.create_table('metadata_authors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['MetadataAuthor'])

        # Adding model 'MetadataWriter'
        db.create_table('metadata_writers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['MetadataWriter'])

        # Adding model 'LegalRight'
        db.create_table('legal_rights', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['LegalRight'])

        # Adding model 'RecordingContext'
        db.create_table('recording_contexts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['RecordingContext'])

        # Adding model 'AdConversion'
        db.create_table('ad_conversions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['AdConversion'])

        # Adding model 'VernacularStyle'
        db.create_table('vernacular_styles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['VernacularStyle'])

        # Adding model 'GenericStyle'
        db.create_table('generic_styles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['GenericStyle'])

        # Adding model 'ContextKeyword'
        db.create_table('context_keywords', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['ContextKeyword'])

        # Adding model 'Publisher'
        db.create_table('publishers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['Publisher'])

        # Adding model 'PublisherCollection'
        db.create_table('publisher_collections', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publisher', self.gf('telemeta.models.core.ForeignKey')(related_name='publisher_collections', to=orm['telemeta.Publisher'])),
            ('value', self.gf('telemeta.models.core.CharField')(max_length=250)),
        ))
        db.send_create_signal('telemeta', ['PublisherCollection'])

        # Adding model 'EthnicGroup'
        db.create_table('ethnic_groups', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('telemeta', ['EthnicGroup'])

        # Adding model 'EthnicGroupAlias'
        db.create_table('ethnic_group_aliases', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ethnic_group', self.gf('telemeta.models.core.ForeignKey')(related_name='aliases', to=orm['telemeta.EthnicGroup'])),
            ('value', self.gf('telemeta.models.core.CharField')(max_length=250)),
        ))
        db.send_create_signal('telemeta', ['EthnicGroupAlias'])

        # Adding unique constraint on 'EthnicGroupAlias', fields ['ethnic_group', 'value']
        db.create_unique('ethnic_group_aliases', ['ethnic_group_id', 'value'])

        # Adding model 'Location'
        db.create_table('locations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('telemeta.models.core.CharField')(unique=True, max_length=150)),
            ('type', self.gf('telemeta.models.core.IntegerField')(default=0, db_index=True, blank=True)),
            ('complete_type', self.gf('telemeta.models.core.ForeignKey')(related_name='locations', to=orm['telemeta.LocationType'])),
            ('current_location', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='past_names', null=True, blank=True, to=orm['telemeta.Location'])),
            ('latitude', self.gf('telemeta.models.core.FloatField')(default=None, null=True, blank=True)),
            ('longitude', self.gf('telemeta.models.core.FloatField')(default=None, null=True, blank=True)),
            ('is_authoritative', self.gf('telemeta.models.core.BooleanField')(default=False)),
        ))
        db.send_create_signal('telemeta', ['Location'])

        # Adding model 'LocationType'
        db.create_table('location_types', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('telemeta.models.core.CharField')(unique=True, max_length=64)),
            ('name', self.gf('telemeta.models.core.CharField')(max_length=150)),
        ))
        db.send_create_signal('telemeta', ['LocationType'])

        # Adding model 'LocationAlias'
        db.create_table('location_aliases', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('telemeta.models.core.ForeignKey')(related_name='aliases', to=orm['telemeta.Location'])),
            ('alias', self.gf('telemeta.models.core.CharField')(max_length=150)),
            ('is_authoritative', self.gf('telemeta.models.core.BooleanField')(default=False)),
        ))
        db.send_create_signal('telemeta', ['LocationAlias'])

        # Adding unique constraint on 'LocationAlias', fields ['location', 'alias']
        db.create_unique('location_aliases', ['location_id', 'alias'])

        # Adding model 'LocationRelation'
        db.create_table('location_relations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('telemeta.models.core.ForeignKey')(related_name='ancestor_relations', to=orm['telemeta.Location'])),
            ('ancestor_location', self.gf('telemeta.models.core.ForeignKey')(related_name='descendant_relations', to=orm['telemeta.Location'])),
            ('is_direct', self.gf('telemeta.models.core.BooleanField')(default=False, db_index=True)),
            ('is_authoritative', self.gf('telemeta.models.core.BooleanField')(default=False)),
        ))
        db.send_create_signal('telemeta', ['LocationRelation'])

        # Adding unique constraint on 'LocationRelation', fields ['location', 'ancestor_location']
        db.create_unique('location_relations', ['location_id', 'ancestor_location_id'])

        # Adding model 'Revision'
        db.create_table('revisions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('element_type', self.gf('telemeta.models.core.CharField')(max_length=16)),
            ('element_id', self.gf('telemeta.models.core.IntegerField')()),
            ('change_type', self.gf('telemeta.models.core.CharField')(max_length=16)),
            ('time', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now_add=True, null=True, blank=True)),
            ('user', self.gf('telemeta.models.core.ForeignKey')(related_name='revisions', db_column='username', to=orm['auth.User'])),
        ))
        db.send_create_signal('telemeta', ['Revision'])

        # Adding model 'UserProfile'
        db.create_table('profiles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('telemeta.models.core.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('institution', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('function', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('address', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('telephone', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('expiration_date', self.gf('telemeta.models.core.DateField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('telemeta', ['UserProfile'])

        # Adding model 'Instrument'
        db.create_table('instruments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('telemeta.models.core.CharField')(max_length=250)),
        ))
        db.send_create_signal('telemeta', ['Instrument'])

        # Adding model 'InstrumentAlias'
        db.create_table('instrument_aliases', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('telemeta.models.core.CharField')(max_length=250)),
        ))
        db.send_create_signal('telemeta', ['InstrumentAlias'])

        # Adding model 'InstrumentRelation'
        db.create_table('instrument_relations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instrument', self.gf('telemeta.models.core.ForeignKey')(related_name='parent_relation', to=orm['telemeta.Instrument'])),
            ('parent_instrument', self.gf('telemeta.models.core.ForeignKey')(related_name='child_relation', to=orm['telemeta.Instrument'])),
        ))
        db.send_create_signal('telemeta', ['InstrumentRelation'])

        # Adding unique constraint on 'InstrumentRelation', fields ['instrument', 'parent_instrument']
        db.create_unique('instrument_relations', ['instrument_id', 'parent_instrument_id'])

        # Adding model 'InstrumentAliasRelation'
        db.create_table('instrument_alias_relations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('telemeta.models.core.ForeignKey')(related_name='other_name', to=orm['telemeta.InstrumentAlias'])),
            ('instrument', self.gf('telemeta.models.core.ForeignKey')(related_name='relation', to=orm['telemeta.InstrumentAlias'])),
        ))
        db.send_create_signal('telemeta', ['InstrumentAliasRelation'])

        # Adding unique constraint on 'InstrumentAliasRelation', fields ['alias', 'instrument']
        db.create_unique('instrument_alias_relations', ['alias_id', 'instrument_id'])

        # Adding model 'Language'
        db.create_table('languages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('telemeta.models.core.CharField')(default='', max_length=3, blank=True)),
            ('part2B', self.gf('telemeta.models.core.CharField')(default='', max_length=3, blank=True)),
            ('part2T', self.gf('telemeta.models.core.CharField')(default='', max_length=3, blank=True)),
            ('part1', self.gf('telemeta.models.core.CharField')(default='', max_length=1, blank=True)),
            ('scope', self.gf('telemeta.models.core.CharField')(default='', max_length=1, blank=True)),
            ('type', self.gf('telemeta.models.core.CharField')(default='', max_length=1, blank=True)),
            ('name', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('comment', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('telemeta', ['Language'])

        # Adding model 'MediaCorpus'
        db.create_table('media_corpus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('telemeta.models.core.CharField')(default=None, max_length=250, unique=True, null=True, blank=True)),
            ('title', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('description', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('code', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
            ('public_access', self.gf('telemeta.models.core.CharField')(default='metadata', max_length=16, blank=True)),
        ))
        db.send_create_signal('telemeta', ['MediaCorpus'])

        # Adding model 'MediaCorpusCollectionRelation'
        db.create_table('media_corpus_collection_relations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('telemeta.models.core.ForeignKey')(related_name='parent_relation', to=orm['telemeta.MediaCollection'])),
            ('corpus', self.gf('telemeta.models.core.ForeignKey')(related_name='child_relation', to=orm['telemeta.MediaCorpus'])),
        ))
        db.send_create_signal('telemeta', ['MediaCorpusCollectionRelation'])

        # Adding unique constraint on 'MediaCorpusCollectionRelation', fields ['collection', 'corpus']
        db.create_unique('media_corpus_collection_relations', ['collection_id', 'corpus_id'])

        # Adding model 'MediaCollection'
        db.create_table('media_collections', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('telemeta.models.core.CharField')(default=None, max_length=250, unique=True, null=True, blank=True)),
            ('title', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('alt_title', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('creator', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('recording_context', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.RecordingContext'])),
            ('recorded_from_year', self.gf('telemeta.models.core.IntegerField')(default=0, blank=True)),
            ('recorded_to_year', self.gf('telemeta.models.core.IntegerField')(default=0, blank=True)),
            ('year_published', self.gf('telemeta.models.core.IntegerField')(default=0, blank=True)),
            ('collector', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('publisher', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.Publisher'])),
            ('publisher_collection', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.PublisherCollection'])),
            ('publisher_serial', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('booklet_author', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('external_references', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('doctype_code', self.gf('telemeta.models.core.IntegerField')(default=0, blank=True)),
            ('public_access', self.gf('telemeta.models.core.CharField')(default='metadata', max_length=16, blank=True)),
            ('legal_rights', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.LegalRight'])),
            ('acquisition_mode', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.AcquisitionMode'])),
            ('cnrs_contributor', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('metadata_author', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.MetadataAuthor'])),
            ('booklet_description', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('publishing_status', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.PublishingStatus'])),
            ('alt_ids', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('comment', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('metadata_writer', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.MetadataWriter'])),
            ('travail', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('items_done', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('collector_is_creator', self.gf('telemeta.models.core.BooleanField')(default=False)),
            ('is_published', self.gf('telemeta.models.core.BooleanField')(default=False)),
            ('conservation_site', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('code', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
            ('old_code', self.gf('telemeta.models.core.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('approx_duration', self.gf('telemeta.models.core.DurationField')(default='00:00', blank=True)),
            ('physical_items_num', self.gf('telemeta.models.core.IntegerField')(default=0, blank=True)),
            ('physical_format', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.PhysicalFormat'])),
            ('ad_conversion', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.AdConversion'])),
            ('state', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('a_informer_07_03', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
        ))
        db.send_create_signal('telemeta', ['MediaCollection'])

        # Adding model 'MediaCollectionRelated'
        db.create_table('media_collection_related', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('date', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now=True, null=True, blank=True)),
            ('description', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('mime_type', self.gf('telemeta.models.core.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('url', self.gf('telemeta.models.core.CharField')(default='', max_length=500, blank=True)),
            ('credits', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('file', self.gf('telemeta.models.core.FileField')(default='', max_length=100, db_column='filename', blank=True)),
            ('collection', self.gf('telemeta.models.core.ForeignKey')(related_name='related', to=orm['telemeta.MediaCollection'])),
        ))
        db.send_create_signal('telemeta', ['MediaCollectionRelated'])

        # Adding model 'MediaItem'
        db.create_table('media_items', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('alt_title', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('collector', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('collection', self.gf('telemeta.models.core.ForeignKey')(related_name='items', to=orm['telemeta.MediaCollection'])),
            ('recorded_from_date', self.gf('telemeta.models.core.DateField')(default=None, null=True, blank=True)),
            ('recorded_to_date', self.gf('telemeta.models.core.DateField')(default=None, null=True, blank=True)),
            ('location', self.gf('telemeta.models.core.WeakForeignKey')(default=None, to=orm['telemeta.Location'], null=True, blank=True)),
            ('location_comment', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('cultural_area', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('ethnic_group', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='items', null=True, blank=True, to=orm['telemeta.EthnicGroup'])),
            ('language', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('language_iso', self.gf('telemeta.models.core.ForeignKey')(default=None, related_name='items', null=True, blank=True, to=orm['telemeta.Language'])),
            ('context_comment', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('moda_execut', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('vernacular_style', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='items', null=True, blank=True, to=orm['telemeta.VernacularStyle'])),
            ('generic_style', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='items', null=True, blank=True, to=orm['telemeta.GenericStyle'])),
            ('author', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('comment', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('collector_selection', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('collector_from_collection', self.gf('telemeta.models.core.BooleanField')(default=False)),
            ('code', self.gf('telemeta.models.core.CharField')(default='', unique=True, max_length=250, blank=True)),
            ('old_code', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('track', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('creator_reference', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('external_references', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('copied_from_item', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='copies', null=True, blank=True, to=orm['telemeta.MediaItem'])),
            ('public_access', self.gf('telemeta.models.core.CharField')(default='metadata', max_length=16, blank=True)),
            ('file', self.gf('telemeta.models.core.FileField')(default='', max_length=100, db_column='filename', blank=True)),
            ('approx_duration', self.gf('telemeta.models.core.DurationField')(default='00:00', blank=True)),
        ))
        db.send_create_signal('telemeta', ['MediaItem'])

        # Adding model 'MediaItemRelated'
        db.create_table('media_item_related', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('date', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now=True, null=True, blank=True)),
            ('description', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('mime_type', self.gf('telemeta.models.core.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('url', self.gf('telemeta.models.core.CharField')(default='', max_length=500, blank=True)),
            ('credits', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('file', self.gf('telemeta.models.core.FileField')(default='', max_length=100, db_column='filename', blank=True)),
            ('item', self.gf('telemeta.models.core.ForeignKey')(related_name='related', to=orm['telemeta.MediaItem'])),
        ))
        db.send_create_signal('telemeta', ['MediaItemRelated'])

        # Adding model 'MediaItemKeyword'
        db.create_table('media_item_keywords', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('telemeta.models.core.ForeignKey')(related_name='keyword_relations', to=orm['telemeta.MediaItem'])),
            ('keyword', self.gf('telemeta.models.core.ForeignKey')(related_name='item_relations', to=orm['telemeta.ContextKeyword'])),
        ))
        db.send_create_signal('telemeta', ['MediaItemKeyword'])

        # Adding unique constraint on 'MediaItemKeyword', fields ['item', 'keyword']
        db.create_unique('media_item_keywords', ['item_id', 'keyword_id'])

        # Adding model 'MediaItemPerformance'
        db.create_table('media_item_performances', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media_item', self.gf('telemeta.models.core.ForeignKey')(related_name='performances', to=orm['telemeta.MediaItem'])),
            ('instrument', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='performances', null=True, blank=True, to=orm['telemeta.Instrument'])),
            ('alias', self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='performances', null=True, blank=True, to=orm['telemeta.InstrumentAlias'])),
            ('instruments_num', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('musicians', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
        ))
        db.send_create_signal('telemeta', ['MediaItemPerformance'])

        # Adding model 'MediaItemAnalysis'
        db.create_table('media_analysis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('telemeta.models.core.ForeignKey')(related_name='analysis', to=orm['telemeta.MediaItem'])),
            ('analyzer_id', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('name', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('value', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('unit', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
        ))
        db.send_create_signal('telemeta', ['MediaItemAnalysis'])

        # Adding model 'MediaPart'
        db.create_table('media_parts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('telemeta.models.core.ForeignKey')(related_name='parts', to=orm['telemeta.MediaItem'])),
            ('title', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('start', self.gf('telemeta.models.core.FloatField')()),
            ('end', self.gf('telemeta.models.core.FloatField')()),
        ))
        db.send_create_signal('telemeta', ['MediaPart'])

        # Adding model 'Playlist'
        db.create_table('playlists', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public_id', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('author', self.gf('telemeta.models.core.ForeignKey')(related_name='playlists', db_column='author', to=orm['auth.User'])),
            ('title', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('description', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('telemeta', ['Playlist'])

        # Adding model 'PlaylistResource'
        db.create_table('playlist_resources', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public_id', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('playlist', self.gf('telemeta.models.core.ForeignKey')(related_name='resources', to=orm['telemeta.Playlist'])),
            ('resource_type', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('resource_id', self.gf('telemeta.models.core.CharField')(max_length=250)),
        ))
        db.send_create_signal('telemeta', ['PlaylistResource'])

        # Adding model 'MediaItemMarker'
        db.create_table('media_markers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('telemeta.models.core.ForeignKey')(related_name='markers', to=orm['telemeta.MediaItem'])),
            ('public_id', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('time', self.gf('telemeta.models.core.FloatField')(default=0, blank=True)),
            ('title', self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True)),
            ('date', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now=True, null=True, blank=True)),
            ('description', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('author', self.gf('telemeta.models.core.ForeignKey')(related_name='markers', to=orm['auth.User'])),
        ))
        db.send_create_signal('telemeta', ['MediaItemMarker'])

        # Adding model 'MediaItemTranscodingFlag'
        db.create_table('media_transcoding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('telemeta.models.core.ForeignKey')(related_name='transcoding', to=orm['telemeta.MediaItem'])),
            ('mime_type', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('date', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now=True, null=True, blank=True)),
            ('value', self.gf('telemeta.models.core.BooleanField')(default=False)),
        ))
        db.send_create_signal('telemeta', ['MediaItemTranscodingFlag'])

        # Adding model 'Search'
        db.create_table('searches', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('telemeta.models.core.ForeignKey')(related_name='searches', db_column='username', to=orm['auth.User'])),
            ('keywords', self.gf('telemeta.models.core.CharField')(max_length=250)),
            ('date', self.gf('telemeta.models.core.DateField')(default=None, auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('telemeta', ['Search'])

    def backwards(self, orm):
        # Removing unique constraint on 'MediaItemKeyword', fields ['item', 'keyword']
        db.delete_unique('media_item_keywords', ['item_id', 'keyword_id'])

        # Removing unique constraint on 'MediaCorpusCollectionRelation', fields ['collection', 'corpus']
        db.delete_unique('media_corpus_collection_relations', ['collection_id', 'corpus_id'])

        # Removing unique constraint on 'InstrumentAliasRelation', fields ['alias', 'instrument']
        db.delete_unique('instrument_alias_relations', ['alias_id', 'instrument_id'])

        # Removing unique constraint on 'InstrumentRelation', fields ['instrument', 'parent_instrument']
        db.delete_unique('instrument_relations', ['instrument_id', 'parent_instrument_id'])

        # Removing unique constraint on 'LocationRelation', fields ['location', 'ancestor_location']
        db.delete_unique('location_relations', ['location_id', 'ancestor_location_id'])

        # Removing unique constraint on 'LocationAlias', fields ['location', 'alias']
        db.delete_unique('location_aliases', ['location_id', 'alias'])

        # Removing unique constraint on 'EthnicGroupAlias', fields ['ethnic_group', 'value']
        db.delete_unique('ethnic_group_aliases', ['ethnic_group_id', 'value'])

        # Deleting model 'PhysicalFormat'
        db.delete_table('physical_formats')

        # Deleting model 'PublishingStatus'
        db.delete_table('publishing_status')

        # Deleting model 'AcquisitionMode'
        db.delete_table('acquisition_modes')

        # Deleting model 'MetadataAuthor'
        db.delete_table('metadata_authors')

        # Deleting model 'MetadataWriter'
        db.delete_table('metadata_writers')

        # Deleting model 'LegalRight'
        db.delete_table('legal_rights')

        # Deleting model 'RecordingContext'
        db.delete_table('recording_contexts')

        # Deleting model 'AdConversion'
        db.delete_table('ad_conversions')

        # Deleting model 'VernacularStyle'
        db.delete_table('vernacular_styles')

        # Deleting model 'GenericStyle'
        db.delete_table('generic_styles')

        # Deleting model 'ContextKeyword'
        db.delete_table('context_keywords')

        # Deleting model 'Publisher'
        db.delete_table('publishers')

        # Deleting model 'PublisherCollection'
        db.delete_table('publisher_collections')

        # Deleting model 'EthnicGroup'
        db.delete_table('ethnic_groups')

        # Deleting model 'EthnicGroupAlias'
        db.delete_table('ethnic_group_aliases')

        # Deleting model 'Location'
        db.delete_table('locations')

        # Deleting model 'LocationType'
        db.delete_table('location_types')

        # Deleting model 'LocationAlias'
        db.delete_table('location_aliases')

        # Deleting model 'LocationRelation'
        db.delete_table('location_relations')

        # Deleting model 'Revision'
        db.delete_table('revisions')

        # Deleting model 'UserProfile'
        db.delete_table('profiles')

        # Deleting model 'Instrument'
        db.delete_table('instruments')

        # Deleting model 'InstrumentAlias'
        db.delete_table('instrument_aliases')

        # Deleting model 'InstrumentRelation'
        db.delete_table('instrument_relations')

        # Deleting model 'InstrumentAliasRelation'
        db.delete_table('instrument_alias_relations')

        # Deleting model 'Language'
        db.delete_table('languages')

        # Deleting model 'MediaCorpus'
        db.delete_table('media_corpus')

        # Deleting model 'MediaCorpusCollectionRelation'
        db.delete_table('media_corpus_collection_relations')

        # Deleting model 'MediaCollection'
        db.delete_table('media_collections')

        # Deleting model 'MediaCollectionRelated'
        db.delete_table('media_collection_related')

        # Deleting model 'MediaItem'
        db.delete_table('media_items')

        # Deleting model 'MediaItemRelated'
        db.delete_table('media_item_related')

        # Deleting model 'MediaItemKeyword'
        db.delete_table('media_item_keywords')

        # Deleting model 'MediaItemPerformance'
        db.delete_table('media_item_performances')

        # Deleting model 'MediaItemAnalysis'
        db.delete_table('media_analysis')

        # Deleting model 'MediaPart'
        db.delete_table('media_parts')

        # Deleting model 'Playlist'
        db.delete_table('playlists')

        # Deleting model 'PlaylistResource'
        db.delete_table('playlist_resources')

        # Deleting model 'MediaItemMarker'
        db.delete_table('media_markers')

        # Deleting model 'MediaItemTranscodingFlag'
        db.delete_table('media_transcoding')

        # Deleting model 'Search'
        db.delete_table('searches')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'telemeta.acquisitionmode': {
            'Meta': {'ordering': "['value']", 'object_name': 'AcquisitionMode', 'db_table': "'acquisition_modes'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.adconversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'AdConversion', 'db_table': "'ad_conversions'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.contextkeyword': {
            'Meta': {'ordering': "['value']", 'object_name': 'ContextKeyword', 'db_table': "'context_keywords'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.ethnicgroup': {
            'Meta': {'ordering': "['value']", 'object_name': 'EthnicGroup', 'db_table': "'ethnic_groups'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.ethnicgroupalias': {
            'Meta': {'ordering': "['ethnic_group__value']", 'unique_together': "(('ethnic_group', 'value'),)", 'object_name': 'EthnicGroupAlias', 'db_table': "'ethnic_group_aliases'"},
            'ethnic_group': ('telemeta.models.core.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['telemeta.EthnicGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.genericstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'GenericStyle', 'db_table': "'generic_styles'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.instrument': {
            'Meta': {'object_name': 'Instrument', 'db_table': "'instruments'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.instrumentalias': {
            'Meta': {'object_name': 'InstrumentAlias', 'db_table': "'instrument_aliases'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.instrumentaliasrelation': {
            'Meta': {'unique_together': "(('alias', 'instrument'),)", 'object_name': 'InstrumentAliasRelation', 'db_table': "'instrument_alias_relations'"},
            'alias': ('telemeta.models.core.ForeignKey', [], {'related_name': "'other_name'", 'to': "orm['telemeta.InstrumentAlias']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.core.ForeignKey', [], {'related_name': "'relation'", 'to': "orm['telemeta.InstrumentAlias']"})
        },
        'telemeta.instrumentrelation': {
            'Meta': {'unique_together': "(('instrument', 'parent_instrument'),)", 'object_name': 'InstrumentRelation', 'db_table': "'instrument_relations'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.core.ForeignKey', [], {'related_name': "'parent_relation'", 'to': "orm['telemeta.Instrument']"}),
            'parent_instrument': ('telemeta.models.core.ForeignKey', [], {'related_name': "'child_relation'", 'to': "orm['telemeta.Instrument']"})
        },
        'telemeta.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language', 'db_table': "'languages'"},
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'part1': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'part2B': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'part2T': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'scope': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'})
        },
        'telemeta.legalright': {
            'Meta': {'ordering': "['value']", 'object_name': 'LegalRight', 'db_table': "'legal_rights'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location', 'db_table': "'locations'"},
            'complete_type': ('telemeta.models.core.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['telemeta.LocationType']"}),
            'current_location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'past_names'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Location']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'latitude': ('telemeta.models.core.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('telemeta.models.core.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'type': ('telemeta.models.core.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'})
        },
        'telemeta.locationalias': {
            'Meta': {'ordering': "['alias']", 'unique_together': "(('location', 'alias'),)", 'object_name': 'LocationAlias', 'db_table': "'location_aliases'"},
            'alias': ('telemeta.models.core.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['telemeta.Location']"})
        },
        'telemeta.locationrelation': {
            'Meta': {'ordering': "['ancestor_location__name']", 'unique_together': "(('location', 'ancestor_location'),)", 'object_name': 'LocationRelation', 'db_table': "'location_relations'"},
            'ancestor_location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'descendant_relations'", 'to': "orm['telemeta.Location']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'is_direct': ('telemeta.models.core.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'ancestor_relations'", 'to': "orm['telemeta.Location']"})
        },
        'telemeta.locationtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocationType', 'db_table': "'location_types'"},
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '150'})
        },
        'telemeta.mediacollection': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCollection', 'db_table': "'media_collections'"},
            'a_informer_07_03': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'acquisition_mode': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AcquisitionMode']"}),
            'ad_conversion': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AdConversion']"}),
            'alt_ids': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'00:00'", 'blank': 'True'}),
            'booklet_author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'booklet_description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'cnrs_contributor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_is_creator': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'conservation_site': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'creator': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'doctype_code': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'items_done': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'legal_rights': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.LegalRight']"}),
            'metadata_author': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataAuthor']"}),
            'metadata_writer': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataWriter']"}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'physical_format': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'physical_items_num': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publisher': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Publisher']"}),
            'publisher_collection': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublisherCollection']"}),
            'publisher_serial': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'publishing_status': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublishingStatus']"}),
            'recorded_from_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recording_context': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.RecordingContext']"}),
            'reference': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'state': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'travail': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'year_published': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'telemeta.mediacollectionrelated': {
            'Meta': {'object_name': 'MediaCollectionRelated', 'db_table': "'media_collection_related'"},
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaCollection']"}),
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '100', 'db_column': "'filename'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediacorpus': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCorpus', 'db_table': "'media_corpus'"},
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'reference': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.mediacorpuscollectionrelation': {
            'Meta': {'unique_together': "(('collection', 'corpus'),)", 'object_name': 'MediaCorpusCollectionRelation', 'db_table': "'media_corpus_collection_relations'"},
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'parent_relation'", 'to': "orm['telemeta.MediaCollection']"}),
            'corpus': ('telemeta.models.core.ForeignKey', [], {'related_name': "'child_relation'", 'to': "orm['telemeta.MediaCorpus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'telemeta.mediaitem': {
            'Meta': {'object_name': 'MediaItem', 'db_table': "'media_items'"},
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'00:00'", 'blank': 'True'}),
            'author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'to': "orm['telemeta.MediaCollection']"}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_from_collection': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'collector_selection': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'context_comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'copied_from_item': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'copies'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'creator_reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'cultural_area': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'ethnic_group': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.EthnicGroup']"}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '100', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'language_iso': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Language']"}),
            'location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'moda_execut': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'recorded_from_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_to_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'track': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'vernacular_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.VernacularStyle']"})
        },
        'telemeta.mediaitemanalysis': {
            'Meta': {'ordering': "['name']", 'object_name': 'MediaItemAnalysis', 'db_table': "'media_analysis'"},
            'analyzer_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'analysis'", 'to': "orm['telemeta.MediaItem']"}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'unit': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemkeyword': {
            'Meta': {'unique_together': "(('item', 'keyword'),)", 'object_name': 'MediaItemKeyword', 'db_table': "'media_item_keywords'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'keyword_relations'", 'to': "orm['telemeta.MediaItem']"}),
            'keyword': ('telemeta.models.core.ForeignKey', [], {'related_name': "'item_relations'", 'to': "orm['telemeta.ContextKeyword']"})
        },
        'telemeta.mediaitemmarker': {
            'Meta': {'object_name': 'MediaItemMarker', 'db_table': "'media_markers'"},
            'author': ('telemeta.models.core.ForeignKey', [], {'related_name': "'markers'", 'to': "orm['auth.User']"}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'markers'", 'to': "orm['telemeta.MediaItem']"}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'time': ('telemeta.models.core.FloatField', [], {'default': '0', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemperformance': {
            'Meta': {'object_name': 'MediaItemPerformance', 'db_table': "'media_item_performances'"},
            'alias': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'performances'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.InstrumentAlias']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'performances'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Instrument']"}),
            'instruments_num': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'media_item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'performances'", 'to': "orm['telemeta.MediaItem']"}),
            'musicians': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemrelated': {
            'Meta': {'object_name': 'MediaItemRelated', 'db_table': "'media_item_related'"},
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '100', 'db_column': "'filename'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediaitemtranscodingflag': {
            'Meta': {'object_name': 'MediaItemTranscodingFlag', 'db_table': "'media_transcoding'"},
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'transcoding'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'value': ('telemeta.models.core.BooleanField', [], {'default': 'False'})
        },
        'telemeta.mediapart': {
            'Meta': {'object_name': 'MediaPart', 'db_table': "'media_parts'"},
            'end': ('telemeta.models.core.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'parts'", 'to': "orm['telemeta.MediaItem']"}),
            'start': ('telemeta.models.core.FloatField', [], {}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.metadataauthor': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataAuthor', 'db_table': "'metadata_authors'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadatawriter': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataWriter', 'db_table': "'metadata_writers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.physicalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'PhysicalFormat', 'db_table': "'physical_formats'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.playlist': {
            'Meta': {'object_name': 'Playlist', 'db_table': "'playlists'"},
            'author': ('telemeta.models.core.ForeignKey', [], {'related_name': "'playlists'", 'db_column': "'author'", 'to': "orm['auth.User']"}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.playlistresource': {
            'Meta': {'object_name': 'PlaylistResource', 'db_table': "'playlist_resources'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playlist': ('telemeta.models.core.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['telemeta.Playlist']"}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'resource_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'resource_type': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.publisher': {
            'Meta': {'ordering': "['value']", 'object_name': 'Publisher', 'db_table': "'publishers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.publishercollection': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublisherCollection', 'db_table': "'publisher_collections'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('telemeta.models.core.ForeignKey', [], {'related_name': "'publisher_collections'", 'to': "orm['telemeta.Publisher']"}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.publishingstatus': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublishingStatus', 'db_table': "'publishing_status'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.recordingcontext': {
            'Meta': {'ordering': "['value']", 'object_name': 'RecordingContext', 'db_table': "'recording_contexts'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.revision': {
            'Meta': {'object_name': 'Revision', 'db_table': "'revisions'"},
            'change_type': ('telemeta.models.core.CharField', [], {'max_length': '16'}),
            'element_id': ('telemeta.models.core.IntegerField', [], {}),
            'element_type': ('telemeta.models.core.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'related_name': "'revisions'", 'db_column': "'username'", 'to': "orm['auth.User']"})
        },
        'telemeta.search': {
            'Meta': {'object_name': 'Search', 'db_table': "'searches'"},
            'date': ('telemeta.models.core.DateField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'username': ('telemeta.models.core.ForeignKey', [], {'related_name': "'searches'", 'db_column': "'username'", 'to': "orm['auth.User']"})
        },
        'telemeta.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'profiles'"},
            'address': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'expiration_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'function': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'telephone': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'telemeta.vernacularstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'VernacularStyle', 'db_table': "'vernacular_styles'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['telemeta']