# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MediaCollection', fields ['reference']
        db.delete_unique('media_collections', ['reference'])

        # Adding model 'MediaItemIdentifier'
        db.create_table('media_item_identifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('telemeta.models.core.CharField')(default='', unique=True, max_length=255, blank=True)),
            ('type', self.gf('telemeta.models.core.WeakForeignKey')(default=None, to=orm['telemeta.IdentifierType'], null=True, blank=True)),
            ('date_add', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now_add=True, null=True, blank=True)),
            ('date_first', self.gf('telemeta.models.core.DateTimeField')(default=None, null=True, blank=True)),
            ('date_last', self.gf('telemeta.models.core.DateTimeField')(default=None, null=True, blank=True)),
            ('date_modified', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now=True, null=True, blank=True)),
            ('notes', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('item', self.gf('telemeta.models.core.ForeignKey')(related_name='identifiers', to=orm['telemeta.MediaItem'])),
        ))
        db.send_create_signal('telemeta', ['MediaItemIdentifier'])

        # Adding unique constraint on 'MediaItemIdentifier', fields ['identifier', 'item']
        db.create_unique('media_item_identifier', ['identifier', 'item_id'])

        # Adding model 'OriginalFormat'
        db.create_table('original_format', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
            ('notes', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('telemeta', ['OriginalFormat'])

        # Adding model 'MediaType'
        db.create_table('media_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
            ('notes', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('telemeta', ['MediaType'])

        # Adding model 'CopyType'
        db.create_table('copy_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
            ('notes', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('telemeta', ['CopyType'])

        # Adding model 'MediaCollectionIdentifier'
        db.create_table('media_collection_identifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('telemeta.models.core.CharField')(default='', unique=True, max_length=255, blank=True)),
            ('type', self.gf('telemeta.models.core.WeakForeignKey')(default=None, to=orm['telemeta.IdentifierType'], null=True, blank=True)),
            ('date_add', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now_add=True, null=True, blank=True)),
            ('date_first', self.gf('telemeta.models.core.DateTimeField')(default=None, null=True, blank=True)),
            ('date_last', self.gf('telemeta.models.core.DateTimeField')(default=None, null=True, blank=True)),
            ('date_modified', self.gf('telemeta.models.core.DateTimeField')(default=None, auto_now=True, null=True, blank=True)),
            ('notes', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
            ('collection', self.gf('telemeta.models.core.ForeignKey')(related_name='identifiers', to=orm['telemeta.MediaCollection'])),
        ))
        db.send_create_signal('telemeta', ['MediaCollectionIdentifier'])

        # Adding unique constraint on 'MediaCollectionIdentifier', fields ['identifier', 'collection']
        db.create_unique('media_collection_identifier', ['identifier', 'collection_id'])

        # Adding model 'Status'
        db.create_table('media_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
            ('notes', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('telemeta', ['Status'])

        # Adding model 'IdentifierType'
        db.create_table('identifier_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250)),
            ('notes', self.gf('telemeta.models.core.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('telemeta', ['IdentifierType'])

        # Adding field 'RecordingContext.notes'
        db.add_column('recording_contexts', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'PublishingStatus.notes'
        db.add_column('publishing_status', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'NumberOfChannels.notes'
        db.add_column('original_channel_number', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'MediaItemRelated.mime_type'
        db.alter_column('media_item_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))
        # Adding field 'TapeVendor.notes'
        db.add_column('tape_vendor', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'LegalRight.notes'
        db.add_column('legal_rights', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'TapeSpeed.notes'
        db.add_column('tape_speed', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'MediaFondsRelated.mime_type'
        db.alter_column('media_fonds_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))
        # Adding field 'AcquisitionMode.notes'
        db.add_column('acquisition_modes', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Organization.notes'
        db.add_column('organization', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'AdConversion.notes'
        db.add_column('ad_conversions', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'MediaItem.copied_from_item'
        db.delete_column('media_items', 'copied_from_item_id')

        # Adding field 'MediaItem.media_type'
        db.add_column('media_items', 'media_type',
                      self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='items', null=True, blank=True, to=orm['telemeta.MediaType']),
                      keep_default=False)

        # Adding field 'ContextKeyword.notes'
        db.add_column('context_keywords', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'VernacularStyle.notes'
        db.add_column('vernacular_styles', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'TapeWheelDiameter.notes'
        db.add_column('tape_wheel_diameter', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Topic.notes'
        db.add_column('topic', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'TapeWidth.notes'
        db.add_column('tape_width', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'MediaCollection.a_informer_07_03'
        db.delete_column('media_collections', 'a_informer_07_03')

        # Deleting field 'MediaCollection.doctype_code'
        db.delete_column('media_collections', 'doctype_code')

        # Deleting field 'MediaCollection.state'
        db.delete_column('media_collections', 'state')

        # Adding field 'MediaCollection.description'
        db.add_column('media_collections', 'description',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'MediaCollection.copy_type'
        db.add_column('media_collections', 'copy_type',
                      self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.CopyType']),
                      keep_default=False)

        # Adding field 'MediaCollection.status'
        db.add_column('media_collections', 'status',
                      self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.Status']),
                      keep_default=False)

        # Adding field 'MediaCollection.alt_copies'
        db.add_column('media_collections', 'alt_copies',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'MediaCollection.archiver_notes'
        db.add_column('media_collections', 'archiver_notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'MediaCollection.media_type'
        db.add_column('media_collections', 'media_type',
                      self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.MediaType']),
                      keep_default=False)

        # Adding field 'MediaCollection.original_format'
        db.add_column('media_collections', 'original_format',
                      self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='collections', null=True, blank=True, to=orm['telemeta.OriginalFormat']),
                      keep_default=False)


        # Changing field 'MediaCollection.reference'
        db.alter_column('media_collections', 'reference', self.gf('telemeta.models.core.CharField')(max_length=250))
        # Adding field 'MetadataAuthor.notes'
        db.add_column('metadata_authors', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Rights.notes'
        db.add_column('rights', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'MediaCorpusRelated.mime_type'
        db.alter_column('media_corpus_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))
        # Adding field 'Instrument.notes'
        db.add_column('instruments', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'TapeLength.notes'
        db.add_column('tape_length', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'MediaCollectionRelated.mime_type'
        db.alter_column('media_collection_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))
        # Adding field 'MetadataWriter.notes'
        db.add_column('metadata_writers', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InstrumentAlias.notes'
        db.add_column('instrument_aliases', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'PhysicalFormat.notes'
        db.add_column('physical_formats', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Publisher.notes'
        db.add_column('publishers', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'GenericStyle.notes'
        db.add_column('generic_styles', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'EthnicGroup.notes'
        db.add_column('ethnic_groups', 'notes',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        if not db.dry_run:
            from telemeta.models import MediaCollection
            for collection in MediaCollection.objects.all():
                trig = False
                if hasattr(MediaCollection, 'alt_ids'):
                    collection.alt_copies = collection.alt_ids
                    trig = True
                if hasattr(MediaCollection, 'travail'):
                    collection.archiver_notes = collection.travail
                    trig = True
                if trig:
                    collection.save()

    def backwards(self, orm):
        # Removing unique constraint on 'MediaCollectionIdentifier', fields ['identifier', 'collection']
        db.delete_unique('media_collection_identifier', ['identifier', 'collection_id'])

        # Removing unique constraint on 'MediaItemIdentifier', fields ['identifier', 'item']
        db.delete_unique('media_item_identifier', ['identifier', 'item_id'])

        # Deleting model 'MediaItemIdentifier'
        db.delete_table('media_item_identifier')

        # Deleting model 'OriginalFormat'
        db.delete_table('original_format')

        # Deleting model 'MediaType'
        db.delete_table('media_type')

        # Deleting model 'CopyType'
        db.delete_table('copy_type')

        # Deleting model 'MediaCollectionIdentifier'
        db.delete_table('media_collection_identifier')

        # Deleting model 'Status'
        db.delete_table('media_status')

        # Deleting model 'IdentifierType'
        db.delete_table('identifier_type')

        # Deleting field 'RecordingContext.notes'
        db.delete_column('recording_contexts', 'notes')

        # Deleting field 'PublishingStatus.notes'
        db.delete_column('publishing_status', 'notes')

        # Deleting field 'NumberOfChannels.notes'
        db.delete_column('original_channel_number', 'notes')


        # Changing field 'MediaItemRelated.mime_type'
        db.alter_column('media_item_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))
        # Deleting field 'TapeVendor.notes'
        db.delete_column('tape_vendor', 'notes')

        # Deleting field 'LegalRight.notes'
        db.delete_column('legal_rights', 'notes')

        # Deleting field 'TapeSpeed.notes'
        db.delete_column('tape_speed', 'notes')


        # Changing field 'MediaFondsRelated.mime_type'
        db.alter_column('media_fonds_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))
        # Deleting field 'AcquisitionMode.notes'
        db.delete_column('acquisition_modes', 'notes')

        # Deleting field 'Organization.notes'
        db.delete_column('organization', 'notes')

        # Deleting field 'AdConversion.notes'
        db.delete_column('ad_conversions', 'notes')

        # Adding field 'MediaItem.copied_from_item'
        db.add_column('media_items', 'copied_from_item',
                      self.gf('telemeta.models.core.WeakForeignKey')(default=None, related_name='copies', null=True, to=orm['telemeta.MediaItem'], blank=True),
                      keep_default=False)

        # Deleting field 'MediaItem.media_type'
        db.delete_column('media_items', 'media_type_id')

        # Deleting field 'ContextKeyword.notes'
        db.delete_column('context_keywords', 'notes')

        # Deleting field 'VernacularStyle.notes'
        db.delete_column('vernacular_styles', 'notes')

        # Deleting field 'TapeWheelDiameter.notes'
        db.delete_column('tape_wheel_diameter', 'notes')

        # Deleting field 'Topic.notes'
        db.delete_column('topic', 'notes')

        # Deleting field 'TapeWidth.notes'
        db.delete_column('tape_width', 'notes')

        # Adding field 'MediaCollection.a_informer_07_03'
        db.add_column('media_collections', 'a_informer_07_03',
                      self.gf('telemeta.models.core.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'MediaCollection.doctype_code'
        db.add_column('media_collections', 'doctype_code',
                      self.gf('telemeta.models.core.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'MediaCollection.state'
        db.add_column('media_collections', 'state',
                      self.gf('telemeta.models.core.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'MediaCollection.description'
        db.delete_column('media_collections', 'description')

        # Deleting field 'MediaCollection.copy_type'
        db.delete_column('media_collections', 'copy_type_id')

        # Deleting field 'MediaCollection.status'
        db.delete_column('media_collections', 'status_id')

        # Deleting field 'MediaCollection.alt_copies'
        db.delete_column('media_collections', 'alt_copies')

        # Deleting field 'MediaCollection.archiver_notes'
        db.delete_column('media_collections', 'archiver_notes')

        # Deleting field 'MediaCollection.media_type'
        db.delete_column('media_collections', 'media_type_id')

        # Deleting field 'MediaCollection.original_format'
        db.delete_column('media_collections', 'original_format_id')


        # Changing field 'MediaCollection.reference'
        db.alter_column('media_collections', 'reference', self.gf('telemeta.models.core.CharField')(unique=True, max_length=250, null=True))
        # Adding unique constraint on 'MediaCollection', fields ['reference']
        db.create_unique('media_collections', ['reference'])

        # Deleting field 'MetadataAuthor.notes'
        db.delete_column('metadata_authors', 'notes')

        # Deleting field 'Rights.notes'
        db.delete_column('rights', 'notes')


        # Changing field 'MediaCorpusRelated.mime_type'
        db.alter_column('media_corpus_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))
        # Deleting field 'Instrument.notes'
        db.delete_column('instruments', 'notes')

        # Deleting field 'TapeLength.notes'
        db.delete_column('tape_length', 'notes')


        # Changing field 'MediaCollectionRelated.mime_type'
        db.alter_column('media_collection_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))
        # Deleting field 'MetadataWriter.notes'
        db.delete_column('metadata_writers', 'notes')

        # Deleting field 'InstrumentAlias.notes'
        db.delete_column('instrument_aliases', 'notes')

        # Deleting field 'PhysicalFormat.notes'
        db.delete_column('physical_formats', 'notes')

        # Deleting field 'Publisher.notes'
        db.delete_column('publishers', 'notes')

        # Deleting field 'GenericStyle.notes'
        db.delete_column('generic_styles', 'notes')

        # Deleting field 'EthnicGroup.notes'
        db.delete_column('ethnic_groups', 'notes')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'telemeta.acquisitionmode': {
            'Meta': {'ordering': "['value']", 'object_name': 'AcquisitionMode', 'db_table': "'acquisition_modes'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.adconversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'AdConversion', 'db_table': "'ad_conversions'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.contextkeyword': {
            'Meta': {'ordering': "['value']", 'object_name': 'ContextKeyword', 'db_table': "'context_keywords'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.copytype': {
            'Meta': {'ordering': "['value']", 'object_name': 'CopyType', 'db_table': "'copy_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.criteria': {
            'Meta': {'object_name': 'Criteria', 'db_table': "'search_criteria'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.ethnicgroup': {
            'Meta': {'ordering': "['value']", 'object_name': 'EthnicGroup', 'db_table': "'ethnic_groups'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.ethnicgroupalias': {
            'Meta': {'ordering': "['ethnic_group__value']", 'unique_together': "(('ethnic_group', 'value'),)", 'object_name': 'EthnicGroupAlias', 'db_table': "'ethnic_group_aliases'"},
            'ethnic_group': ('telemeta.models.core.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['telemeta.EthnicGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.format': {
            'Meta': {'object_name': 'Format', 'db_table': "'media_formats'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'format'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.MediaItem']", 'blank': 'True', 'null': 'True'}),
            'original_audio_quality': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_channels': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.NumberOfChannels']"}),
            'original_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'original_comments': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'format'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Location']", 'blank': 'True', 'null': 'True'}),
            'original_number': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'original_state': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_status': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'physical_format': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'recording_system': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'sticker_presence': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'tape_reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'tape_speed': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeSpeed']"}),
            'tape_thickness': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'tape_vendor': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeVendor']"}),
            'tape_wheel_diameter': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeWheelDiameter']"})
        },
        'telemeta.genericstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'GenericStyle', 'db_table': "'generic_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.identifiertype': {
            'Meta': {'ordering': "['value']", 'object_name': 'IdentifierType', 'db_table': "'identifier_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.instrument': {
            'Meta': {'ordering': "['name']", 'object_name': 'Instrument', 'db_table': "'instruments'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'telemeta.instrumentalias': {
            'Meta': {'ordering': "['name']", 'object_name': 'InstrumentAlias', 'db_table': "'instrument_aliases'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'telemeta.instrumentaliasrelation': {
            'Meta': {'unique_together': "(('alias', 'instrument'),)", 'object_name': 'InstrumentAliasRelation', 'db_table': "'instrument_alias_relations'"},
            'alias': ('telemeta.models.core.ForeignKey', [], {'related_name': "'other_name'", 'to': "orm['telemeta.InstrumentAlias']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.core.ForeignKey', [], {'related_name': "'relation'", 'to': "orm['telemeta.Instrument']"})
        },
        'telemeta.instrumentrelation': {
            'Meta': {'unique_together': "(('instrument', 'parent_instrument'),)", 'object_name': 'InstrumentRelation', 'db_table': "'instrument_relations'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.core.ForeignKey', [], {'related_name': "'parent_relation'", 'to': "orm['telemeta.Instrument']"}),
            'parent_instrument': ('telemeta.models.core.ForeignKey', [], {'related_name': "'child_relation'", 'to': "orm['telemeta.Instrument']"})
        },
        'telemeta.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language', 'db_table': "'languages'"},
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location', 'db_table': "'locations'"},
            'complete_type': ('telemeta.models.core.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['telemeta.LocationType']"}),
            'current_location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'past_names'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Location']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'latitude': ('telemeta.models.core.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('telemeta.models.core.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'type': ('telemeta.models.core.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'})
        },
        'telemeta.locationalias': {
            'Meta': {'ordering': "['alias']", 'unique_together': "(('location', 'alias'),)", 'object_name': 'LocationAlias', 'db_table': "'location_aliases'"},
            'alias': ('telemeta.models.core.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['telemeta.Location']"})
        },
        'telemeta.locationrelation': {
            'Meta': {'ordering': "['ancestor_location__name']", 'unique_together': "(('location', 'ancestor_location'),)", 'object_name': 'LocationRelation', 'db_table': "'location_relations'"},
            'ancestor_location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'descendant_relations'", 'to': "orm['telemeta.Location']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'is_direct': ('telemeta.models.core.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'ancestor_relations'", 'to': "orm['telemeta.Location']"})
        },
        'telemeta.locationtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocationType', 'db_table': "'location_types'"},
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '150'})
        },
        'telemeta.mediacollection': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCollection', 'db_table': "'media_collections'"},
            'acquisition_mode': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AcquisitionMode']"}),
            'ad_conversion': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AdConversion']"}),
            'alt_copies': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'alt_ids': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'archiver_notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.core.BooleanField', [], {'default': 'True'}),
            'booklet_author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'booklet_description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'cnrs_contributor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_is_creator': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'conservation_site': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'copy_type': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.CopyType']"}),
            'creator': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'items_done': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'legal_rights': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.LegalRight']"}),
            'media_type': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaType']"}),
            'metadata_author': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataAuthor']"}),
            'metadata_writer': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataWriter']"}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'original_format': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.OriginalFormat']"}),
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
            'reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'status': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Status']"}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'travail': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'year_published': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'telemeta.mediacollectionidentifier': {
            'Meta': {'unique_together': "(('identifier', 'collection'),)", 'object_name': 'MediaCollectionIdentifier', 'db_table': "'media_collection_identifier'"},
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'identifiers'", 'to': "orm['telemeta.MediaCollection']"}),
            'date_add': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_first': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_last': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.core.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'type': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.IdentifierType']", 'null': 'True', 'blank': 'True'})
        },
        'telemeta.mediacollectionrelated': {
            'Meta': {'object_name': 'MediaCollectionRelated', 'db_table': "'media_collection_related'"},
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaCollection']"}),
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediacorpus': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCorpus', 'db_table': "'media_corpus'"},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'corpus'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.MediaCollection']"}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'descriptions': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'recorded_from_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.mediacorpusrelated': {
            'Meta': {'object_name': 'MediaCorpusRelated', 'db_table': "'media_corpus_related'"},
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'resource': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaCorpus']"}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediafonds': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaFonds', 'db_table': "'media_fonds'"},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fonds'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.MediaCorpus']"}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'descriptions': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.mediafondsrelated': {
            'Meta': {'object_name': 'MediaFondsRelated', 'db_table': "'media_fonds_related'"},
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'resource': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaFonds']"}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediaitem': {
            'Meta': {'object_name': 'MediaItem', 'db_table': "'media_items'"},
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.core.BooleanField', [], {'default': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'to': "orm['telemeta.MediaCollection']"}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_from_collection': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'collector_selection': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'context_comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'contributor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'creator_reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'cultural_area': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'depositor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitalist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitization_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ethnic_group': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.EthnicGroup']"}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'language_iso': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Language']", 'blank': 'True', 'null': 'True'}),
            'location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'media_type': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaType']"}),
            'mimetype': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'moda_execut': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'organization': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Organization']", 'null': 'True', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publishing_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_from_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_to_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recordist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'rights': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Rights']", 'null': 'True', 'blank': 'True'}),
            'scientist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'summary': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'topic': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Topic']", 'null': 'True', 'blank': 'True'}),
            'track': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'vernacular_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.VernacularStyle']"})
        },
        'telemeta.mediaitemanalysis': {
            'Meta': {'ordering': "['name']", 'object_name': 'MediaItemAnalysis', 'db_table': "'media_analysis'"},
            'analyzer_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'analysis'", 'to': "orm['telemeta.MediaItem']"}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'unit': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemidentifier': {
            'Meta': {'unique_together': "(('identifier', 'item'),)", 'object_name': 'MediaItemIdentifier', 'db_table': "'media_item_identifier'"},
            'date_add': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_first': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_last': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.core.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'identifiers'", 'to': "orm['telemeta.MediaItem']"}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'type': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.IdentifierType']", 'null': 'True', 'blank': 'True'})
        },
        'telemeta.mediaitemkeyword': {
            'Meta': {'unique_together': "(('item', 'keyword'),)", 'object_name': 'MediaItemKeyword', 'db_table': "'media_item_keywords'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'keyword_relations'", 'to': "orm['telemeta.MediaItem']"}),
            'keyword': ('telemeta.models.core.ForeignKey', [], {'related_name': "'item_relations'", 'to': "orm['telemeta.ContextKeyword']"})
        },
        'telemeta.mediaitemmarker': {
            'Meta': {'ordering': "['time']", 'object_name': 'MediaItemMarker', 'db_table': "'media_markers'"},
            'author': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'markers'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'markers'", 'to': "orm['telemeta.MediaItem']"}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'time': ('telemeta.models.core.FloatField', [], {'default': '0', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemperformance': {
            'Meta': {'object_name': 'MediaItemPerformance', 'db_table': "'media_item_performances'"},
            'alias': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'performances'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.InstrumentAlias']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediaitemtranscoded': {
            'Meta': {'object_name': 'MediaItemTranscoded', 'db_table': "'telemeta_media_transcoded'"},
            'date_added': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transcoded'", 'to': "orm['telemeta.MediaItem']"}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'telemeta.mediaitemtranscodingflag': {
            'Meta': {'object_name': 'MediaItemTranscodingFlag', 'db_table': "'media_transcoding'"},
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'transcoding'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'value': ('telemeta.models.core.BooleanField', [], {'default': 'False'})
        },
        'telemeta.mediapart': {
            'Meta': {'object_name': 'MediaPart', 'db_table': "'media_parts'"},
            'end': ('telemeta.models.core.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'parts'", 'to': "orm['telemeta.MediaItem']"}),
            'start': ('telemeta.models.core.FloatField', [], {}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.mediatype': {
            'Meta': {'ordering': "['value']", 'object_name': 'MediaType', 'db_table': "'media_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadataauthor': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataAuthor', 'db_table': "'metadata_authors'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadatawriter': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataWriter', 'db_table': "'metadata_writers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.numberofchannels': {
            'Meta': {'ordering': "['value']", 'object_name': 'NumberOfChannels', 'db_table': "'original_channel_number'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.organization': {
            'Meta': {'ordering': "['value']", 'object_name': 'Organization', 'db_table': "'organization'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.originalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'OriginalFormat', 'db_table': "'original_format'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.physicalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'PhysicalFormat', 'db_table': "'physical_formats'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.playlist': {
            'Meta': {'object_name': 'Playlist', 'db_table': "'playlists'"},
            'author': ('telemeta.models.core.ForeignKey', [], {'related_name': "'playlists'", 'db_column': "'author'", 'to': u"orm['auth.User']"}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.playlistresource': {
            'Meta': {'object_name': 'PlaylistResource', 'db_table': "'playlist_resources'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playlist': ('telemeta.models.core.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['telemeta.Playlist']"}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'resource_id': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'resource_type': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.publisher': {
            'Meta': {'ordering': "['value']", 'object_name': 'Publisher', 'db_table': "'publishers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.publishercollection': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublisherCollection', 'db_table': "'publisher_collections'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('telemeta.models.core.ForeignKey', [], {'related_name': "'publisher_collections'", 'to': "orm['telemeta.Publisher']"}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.publishingstatus': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublishingStatus', 'db_table': "'publishing_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.recordingcontext': {
            'Meta': {'ordering': "['value']", 'object_name': 'RecordingContext', 'db_table': "'recording_contexts'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.revision': {
            'Meta': {'object_name': 'Revision', 'db_table': "'revisions'"},
            'change_type': ('telemeta.models.core.CharField', [], {'max_length': '16'}),
            'element_id': ('telemeta.models.core.IntegerField', [], {}),
            'element_type': ('telemeta.models.core.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'related_name': "'revisions'", 'db_column': "'username'", 'to': u"orm['auth.User']"})
        },
        'telemeta.rights': {
            'Meta': {'ordering': "['value']", 'object_name': 'Rights', 'db_table': "'rights'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.search': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Search', 'db_table': "'searches'"},
            'criteria': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'search'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.Criteria']"}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('telemeta.models.core.ForeignKey', [], {'related_name': "'searches'", 'db_column': "'username'", 'to': u"orm['auth.User']"})
        },
        'telemeta.status': {
            'Meta': {'ordering': "['value']", 'object_name': 'Status', 'db_table': "'media_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapelength': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeLength', 'db_table': "'tape_length'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapespeed': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeSpeed', 'db_table': "'tape_speed'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapevendor': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeVendor', 'db_table': "'tape_vendor'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapewheeldiameter': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeWheelDiameter', 'db_table': "'tape_wheel_diameter'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapewidth': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeWidth', 'db_table': "'tape_width'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.topic': {
            'Meta': {'ordering': "['value']", 'object_name': 'Topic', 'db_table': "'topic'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'profiles'"},
            'address': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'attachment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'department': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'expiration_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'function': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'telephone': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        'telemeta.vernacularstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'VernacularStyle', 'db_table': "'vernacular_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['telemeta']