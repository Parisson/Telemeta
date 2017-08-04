# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RecordingContext.notes'
        db.alter_column('recording_contexts', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'RecordingContext.value'
        db.alter_column('recording_contexts', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'Publisher.notes'
        db.alter_column('publishers', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Publisher.value'
        db.alter_column('publishers', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'GenericStyle.notes'
        db.alter_column('generic_styles', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'GenericStyle.value'
        db.alter_column('generic_styles', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'NumberOfChannels.notes'
        db.alter_column('original_channel_number', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'NumberOfChannels.value'
        db.alter_column('original_channel_number', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'CopyType.notes'
        db.alter_column('copy_type', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'CopyType.value'
        db.alter_column('copy_type', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaItemRelated.description'
        db.alter_column('media_item_related', 'description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaItemRelated.credits'
        db.alter_column('media_item_related', 'credits', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemRelated.url'
        db.alter_column('media_item_related', 'url', self.gf('telemeta.models.fields.CharField')(max_length=500))

        # Changing field 'MediaItemRelated.title'
        db.alter_column('media_item_related', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemRelated.item'
        db.alter_column('media_item_related', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemRelated.file'
        db.alter_column('media_item_related', 'filename', self.gf('telemeta.models.fields.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaItemRelated.date'
        db.alter_column('media_item_related', 'date', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaItemRelated.mime_type'
        db.alter_column('media_item_related', 'mime_type', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'LocationType.code'
        db.alter_column('location_types', 'code', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=64))

        # Changing field 'LocationType.name'
        db.alter_column('location_types', 'name', self.gf('telemeta.models.fields.CharField')(max_length=150))

        # Changing field 'MediaCollection.comment'
        db.alter_column('media_collections', 'comment', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollection.code'
        db.alter_column('media_collections', 'code', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaCollection.recorded_to_year'
        db.alter_column('media_collections', 'recorded_to_year', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'MediaCollection.reference'
        db.alter_column('media_collections', 'reference', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.creator'
        db.alter_column('media_collections', 'creator', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.metadata_author'
        db.alter_column('media_collections', 'metadata_author_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.MetadataAuthor']))

        # Changing field 'MediaCollection.original_format'
        db.alter_column('media_collections', 'original_format_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.OriginalFormat']))

        # Changing field 'MediaCollection.publisher_serial'
        db.alter_column('media_collections', 'publisher_serial', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.booklet_author'
        db.alter_column('media_collections', 'booklet_author', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.archiver_notes'
        db.alter_column('media_collections', 'archiver_notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollection.recording_context'
        db.alter_column('media_collections', 'recording_context_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.RecordingContext']))

        # Changing field 'MediaCollection.copy_type'
        db.alter_column('media_collections', 'copy_type_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.CopyType']))

        # Changing field 'MediaCollection.collector'
        db.alter_column('media_collections', 'collector', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.year_published'
        db.alter_column('media_collections', 'year_published', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'MediaCollection.description'
        db.alter_column('media_collections', 'description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollection.acquisition_mode'
        db.alter_column('media_collections', 'acquisition_mode_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.AcquisitionMode']))

        # Changing field 'MediaCollection.metadata_writer'
        db.alter_column('media_collections', 'metadata_writer_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.MetadataWriter']))

        # Changing field 'MediaCollection.alt_copies'
        db.alter_column('media_collections', 'alt_copies', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollection.title'
        db.alter_column('media_collections', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.old_code'
        db.alter_column('media_collections', 'old_code', self.gf('telemeta.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'MediaCollection.approx_duration'
        db.alter_column('media_collections', 'approx_duration', self.gf('telemeta.models.fields.DurationField')())

        # Changing field 'MediaCollection.auto_period_access'
        db.alter_column('media_collections', 'auto_period_access', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'MediaCollection.booklet_description'
        db.alter_column('media_collections', 'booklet_description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollection.media_type'
        db.alter_column('media_collections', 'media_type_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.MediaType']))

        # Changing field 'MediaCollection.status'
        db.alter_column('media_collections', 'status_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.Status']))

        # Changing field 'MediaCollection.travail'
        db.alter_column('media_collections', 'travail', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.external_references'
        db.alter_column('media_collections', 'external_references', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollection.publishing_status'
        db.alter_column('media_collections', 'publishing_status_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.PublishingStatus']))

        # Changing field 'MediaCollection.publisher_collection'
        db.alter_column('media_collections', 'publisher_collection_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.PublisherCollection']))

        # Changing field 'MediaCollection.physical_format'
        db.alter_column('media_collections', 'physical_format_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.PhysicalFormat']))

        # Changing field 'MediaCollection.items_done'
        db.alter_column('media_collections', 'items_done', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.conservation_site'
        db.alter_column('media_collections', 'conservation_site', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.public_access'
        db.alter_column('media_collections', 'public_access', self.gf('telemeta.models.fields.CharField')(max_length=16))

        # Changing field 'MediaCollection.publisher'
        db.alter_column('media_collections', 'publisher_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.Publisher']))

        # Changing field 'MediaCollection.alt_ids'
        db.alter_column('media_collections', 'alt_ids', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.alt_title'
        db.alter_column('media_collections', 'alt_title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.legal_rights'
        db.alter_column('media_collections', 'legal_rights_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.LegalRight']))

        # Changing field 'MediaCollection.cnrs_contributor'
        db.alter_column('media_collections', 'cnrs_contributor', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollection.physical_items_num'
        db.alter_column('media_collections', 'physical_items_num', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'MediaCollection.collector_is_creator'
        db.alter_column('media_collections', 'collector_is_creator', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'MediaCollection.recorded_from_year'
        db.alter_column('media_collections', 'recorded_from_year', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'MediaCollection.ad_conversion'
        db.alter_column('media_collections', 'ad_conversion_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.AdConversion']))

        # Changing field 'MediaCollection.is_published'
        db.alter_column('media_collections', 'is_published', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'ContextKeyword.notes'
        db.alter_column('context_keywords', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'ContextKeyword.value'
        db.alter_column('context_keywords', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'LegalRight.notes'
        db.alter_column('legal_rights', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'LegalRight.value'
        db.alter_column('legal_rights', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'TapeSpeed.notes'
        db.alter_column('tape_speed', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'TapeSpeed.value'
        db.alter_column('tape_speed', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'InstrumentRelation.instrument'
        db.alter_column('instrument_relations', 'instrument_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Instrument']))

        # Changing field 'InstrumentRelation.parent_instrument'
        db.alter_column('instrument_relations', 'parent_instrument_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Instrument']))

        # Changing field 'MediaItemIdentifier.date_add'
        db.alter_column('media_item_identifier', 'date_add', self.gf('telemeta.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'MediaItemIdentifier.date_modified'
        db.alter_column('media_item_identifier', 'date_modified', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaItemIdentifier.notes'
        db.alter_column('media_item_identifier', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaItemIdentifier.item'
        db.alter_column('media_item_identifier', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemIdentifier.identifier'
        db.alter_column('media_item_identifier', 'identifier', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=255))

        # Changing field 'MediaItemIdentifier.type'
        db.alter_column('media_item_identifier', 'type_id', self.gf('telemeta.models.fields.WeakForeignKey')(to=orm['telemeta.IdentifierType'], null=True))

        # Changing field 'MediaItemIdentifier.date_first'
        db.alter_column('media_item_identifier', 'date_first', self.gf('telemeta.models.fields.DateTimeField')(null=True))

        # Changing field 'MediaItemIdentifier.date_last'
        db.alter_column('media_item_identifier', 'date_last', self.gf('telemeta.models.fields.DateTimeField')(null=True))

        # Changing field 'MediaItemPerformance.instrument'
        db.alter_column('media_item_performances', 'instrument_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.Instrument']))

        # Changing field 'MediaItemPerformance.instruments_num'
        db.alter_column('media_item_performances', 'instruments_num', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemPerformance.alias'
        db.alter_column('media_item_performances', 'alias_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.InstrumentAlias']))

        # Changing field 'MediaItemPerformance.musicians'
        db.alter_column('media_item_performances', 'musicians', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemPerformance.media_item'
        db.alter_column('media_item_performances', 'media_item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'OriginalFormat.notes'
        db.alter_column('original_format', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'OriginalFormat.value'
        db.alter_column('original_format', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'InstrumentAliasRelation.alias'
        db.alter_column('instrument_alias_relations', 'alias_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.InstrumentAlias']))

        # Changing field 'InstrumentAliasRelation.instrument'
        db.alter_column('instrument_alias_relations', 'instrument_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Instrument']))

        # Changing field 'MediaCorpus.code'
        db.alter_column('media_corpus', 'code', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaCorpus.recorded_to_year'
        db.alter_column('media_corpus', 'recorded_to_year', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'MediaCorpus.description'
        db.alter_column('media_corpus', 'description', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCorpus.title'
        db.alter_column('media_corpus', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCorpus.recorded_from_year'
        db.alter_column('media_corpus', 'recorded_from_year', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'MediaCorpus.descriptions'
        db.alter_column('media_corpus', 'descriptions', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCorpus.public_access'
        db.alter_column('media_corpus', 'public_access', self.gf('telemeta.models.fields.CharField')(max_length=16))

        # Changing field 'MediaType.notes'
        db.alter_column('media_type', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaType.value'
        db.alter_column('media_type', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'AcquisitionMode.notes'
        db.alter_column('acquisition_modes', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'AcquisitionMode.value'
        db.alter_column('acquisition_modes', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'Organization.notes'
        db.alter_column('organization', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Organization.value'
        db.alter_column('organization', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaFondsRelated.resource'
        db.alter_column('media_fonds_related', 'resource_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaFonds']))

        # Changing field 'MediaFondsRelated.description'
        db.alter_column('media_fonds_related', 'description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaFondsRelated.title'
        db.alter_column('media_fonds_related', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaFondsRelated.url'
        db.alter_column('media_fonds_related', 'url', self.gf('telemeta.models.fields.CharField')(max_length=500))

        # Changing field 'MediaFondsRelated.credits'
        db.alter_column('media_fonds_related', 'credits', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaFondsRelated.file'
        db.alter_column('media_fonds_related', 'filename', self.gf('telemeta.models.fields.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaFondsRelated.date'
        db.alter_column('media_fonds_related', 'date', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaFondsRelated.mime_type'
        db.alter_column('media_fonds_related', 'mime_type', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.comment'
        db.alter_column('media_items', 'comment', self.gf('telemeta.models.fields.TextField')())



        # Changing field 'MediaItem.location_comment'
        db.alter_column('media_items', 'location_comment', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.depositor'
        db.alter_column('media_items', 'depositor', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.contributor'
        db.alter_column('media_items', 'contributor', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.scientist'
        db.alter_column('media_items', 'scientist', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.file'
        db.alter_column('media_items', 'filename', self.gf('telemeta.models.fields.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'MediaItem.cultural_area'
        db.alter_column('media_items', 'cultural_area', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.recorded_from_date'
        db.alter_column('media_items', 'recorded_from_date', self.gf('telemeta.models.fields.DateField')(null=True))

        # Changing field 'MediaItem.collector'
        db.alter_column('media_items', 'collector', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.author'
        db.alter_column('media_items', 'author', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.old_code'
        db.alter_column('media_items', 'old_code', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.approx_duration'
        db.alter_column('media_items', 'approx_duration', self.gf('telemeta.models.fields.DurationField')())

        # Changing field 'MediaItem.auto_period_access'
        db.alter_column('media_items', 'auto_period_access', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'MediaItem.language_iso'
        db.alter_column('media_items', 'language_iso_id', self.gf('telemeta.models.fields.ForeignKey')(on_delete=models.SET_NULL, to=orm['telemeta.Language'], null=True))

        # Changing field 'MediaItem.location'
        db.alter_column('media_items', 'location_id', self.gf('telemeta.models.fields.WeakForeignKey')(to=orm['telemeta.Location'], null=True))

        # Changing field 'MediaItem.creator_reference'
        db.alter_column('media_items', 'creator_reference', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.collector_selection'
        db.alter_column('media_items', 'collector_selection', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.external_references'
        db.alter_column('media_items', 'external_references', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaItem.track'
        db.alter_column('media_items', 'track', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.title'
        db.alter_column('media_items', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.collector_from_collection'
        db.alter_column('media_items', 'collector_from_collection', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'MediaItem.moda_execut'
        db.alter_column('media_items', 'moda_execut', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.collection'
        db.alter_column('media_items', 'collection_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaCollection']))

        # Changing field 'MediaItem.ethnic_group'
        db.alter_column('media_items', 'ethnic_group_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.EthnicGroup']))

        # Changing field 'MediaItem.media_type'
        db.alter_column('media_items', 'media_type_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.MediaType']))

        # Changing field 'MediaItem.public_access'
        db.alter_column('media_items', 'public_access', self.gf('telemeta.models.fields.CharField')(max_length=16))

        # Changing field 'MediaItem.mimetype'
        db.alter_column('media_items', 'mimetype', self.gf('telemeta.models.fields.CharField')(max_length=255))

        # Changing field 'MediaItem.topic'
        db.alter_column('media_items', 'topic_id', self.gf('telemeta.models.fields.WeakForeignKey')(to=orm['telemeta.Topic'], null=True))

        # Changing field 'MediaItem.organization'
        db.alter_column('media_items', 'organization_id', self.gf('telemeta.models.fields.WeakForeignKey')(to=orm['telemeta.Organization'], null=True))

        # Changing field 'MediaItem.context_comment'
        db.alter_column('media_items', 'context_comment', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaItem.language'
        db.alter_column('media_items', 'language', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.rights'
        db.alter_column('media_items', 'rights_id', self.gf('telemeta.models.fields.WeakForeignKey')(to=orm['telemeta.Rights'], null=True))

        # Changing field 'MediaItem.alt_title'
        db.alter_column('media_items', 'alt_title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.summary'
        db.alter_column('media_items', 'summary', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaItem.recorded_to_date'
        db.alter_column('media_items', 'recorded_to_date', self.gf('telemeta.models.fields.DateField')(null=True))

        # Changing field 'MediaItem.generic_style'
        db.alter_column('media_items', 'generic_style_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.GenericStyle']))

        # Changing field 'MediaItem.digitalist'
        db.alter_column('media_items', 'digitalist', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.digitization_date'
        db.alter_column('media_items', 'digitization_date', self.gf('telemeta.models.fields.DateField')(null=True))

        # Changing field 'MediaItem.recordist'
        db.alter_column('media_items', 'recordist', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItem.publishing_date'
        db.alter_column('media_items', 'publishing_date', self.gf('telemeta.models.fields.DateField')(null=True))

        # Changing field 'MediaItem.vernacular_style'
        db.alter_column('media_items', 'vernacular_style_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.VernacularStyle']))

        # Changing field 'MediaItemMarker.public_id'
        db.alter_column('media_markers', 'public_id', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemMarker.description'
        db.alter_column('media_markers', 'description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaItemMarker.author'
        db.alter_column('media_markers', 'author_id', self.gf('telemeta.models.fields.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'MediaItemMarker.title'
        db.alter_column('media_markers', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemMarker.item'
        db.alter_column('media_markers', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemMarker.time'
        db.alter_column('media_markers', 'time', self.gf('telemeta.models.fields.FloatField')())

        # Changing field 'MediaItemMarker.date'
        db.alter_column('media_markers', 'date', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'VernacularStyle.notes'
        db.alter_column('vernacular_styles', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'VernacularStyle.value'
        db.alter_column('vernacular_styles', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'TapeWheelDiameter.notes'
        db.alter_column('tape_wheel_diameter', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'TapeWheelDiameter.value'
        db.alter_column('tape_wheel_diameter', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'Topic.notes'
        db.alter_column('topic', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Topic.value'
        db.alter_column('topic', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaCollectionRelated.description'
        db.alter_column('media_collection_related', 'description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollectionRelated.title'
        db.alter_column('media_collection_related', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollectionRelated.url'
        db.alter_column('media_collection_related', 'url', self.gf('telemeta.models.fields.CharField')(max_length=500))

        # Changing field 'MediaCollectionRelated.collection'
        db.alter_column('media_collection_related', 'collection_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaCollection']))

        # Changing field 'MediaCollectionRelated.credits'
        db.alter_column('media_collection_related', 'credits', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCollectionRelated.file'
        db.alter_column('media_collection_related', 'filename', self.gf('telemeta.models.fields.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaCollectionRelated.date'
        db.alter_column('media_collection_related', 'date', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaCollectionRelated.mime_type'
        db.alter_column('media_collection_related', 'mime_type', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'TapeVendor.notes'
        db.alter_column('tape_vendor', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'TapeVendor.value'
        db.alter_column('tape_vendor', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'TapeWidth.notes'
        db.alter_column('tape_width', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'TapeWidth.value'
        db.alter_column('tape_width', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'Location.name'
        db.alter_column('locations', 'name', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=150))

        # Changing field 'Location.type'
        db.alter_column('locations', 'type', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'Location.complete_type'
        db.alter_column('locations', 'complete_type_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.LocationType']))

        # Changing field 'Location.longitude'
        db.alter_column('locations', 'longitude', self.gf('telemeta.models.fields.FloatField')(null=True))

        # Changing field 'Location.current_location'
        db.alter_column('locations', 'current_location_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.Location']))

        # Changing field 'Location.latitude'
        db.alter_column('locations', 'latitude', self.gf('telemeta.models.fields.FloatField')(null=True))

        # Changing field 'Location.is_authoritative'
        db.alter_column('locations', 'is_authoritative', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'MediaPart.item'
        db.alter_column('media_parts', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaPart.title'
        db.alter_column('media_parts', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaPart.end'
        db.alter_column('media_parts', 'end', self.gf('telemeta.models.fields.FloatField')())

        # Changing field 'MediaPart.start'
        db.alter_column('media_parts', 'start', self.gf('telemeta.models.fields.FloatField')())

        # Changing field 'MediaCollectionIdentifier.date_add'
        db.alter_column('media_collection_identifier', 'date_add', self.gf('telemeta.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'MediaCollectionIdentifier.date_modified'
        db.alter_column('media_collection_identifier', 'date_modified', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaCollectionIdentifier.notes'
        db.alter_column('media_collection_identifier', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCollectionIdentifier.collection'
        db.alter_column('media_collection_identifier', 'collection_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaCollection']))

        # Changing field 'MediaCollectionIdentifier.identifier'
        db.alter_column('media_collection_identifier', 'identifier', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=255))

        # Changing field 'MediaCollectionIdentifier.type'
        db.alter_column('media_collection_identifier', 'type_id', self.gf('telemeta.models.fields.WeakForeignKey')(to=orm['telemeta.IdentifierType'], null=True))

        # Changing field 'MediaCollectionIdentifier.date_first'
        db.alter_column('media_collection_identifier', 'date_first', self.gf('telemeta.models.fields.DateTimeField')(null=True))

        # Changing field 'MediaCollectionIdentifier.date_last'
        db.alter_column('media_collection_identifier', 'date_last', self.gf('telemeta.models.fields.DateTimeField')(null=True))

        # Changing field 'PublisherCollection.publisher'
        db.alter_column('publisher_collections', 'publisher_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Publisher']))

        # Changing field 'PublisherCollection.value'
        db.alter_column('publisher_collections', 'value', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Search.username'
        db.alter_column('searches', 'username', self.gf('telemeta.models.fields.ForeignKey')(db_column='username', to=orm['auth.User']))

        # Changing field 'Search.date'
        db.alter_column('searches', 'date', self.gf('telemeta.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Search.description'
        db.alter_column('searches', 'description', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'EthnicGroupAlias.ethnic_group'
        db.alter_column('ethnic_group_aliases', 'ethnic_group_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.EthnicGroup']))

        # Changing field 'EthnicGroupAlias.value'
        db.alter_column('ethnic_group_aliases', 'value', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MetadataAuthor.notes'
        db.alter_column('metadata_authors', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MetadataAuthor.value'
        db.alter_column('metadata_authors', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaItemAnalysis.analyzer_id'
        db.alter_column('media_analysis', 'analyzer_id', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.value'
        db.alter_column('media_analysis', 'value', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.item'
        db.alter_column('media_analysis', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemAnalysis.unit'
        db.alter_column('media_analysis', 'unit', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.name'
        db.alter_column('media_analysis', 'name', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Status.notes'
        db.alter_column('media_status', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Status.value'
        db.alter_column('media_status', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'AdConversion.notes'
        db.alter_column('ad_conversions', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'AdConversion.value'
        db.alter_column('ad_conversions', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaItemTranscodingFlag.date'
        db.alter_column('media_transcoding', 'date', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaItemTranscodingFlag.item'
        db.alter_column('media_transcoding', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemTranscodingFlag.mime_type'
        db.alter_column('media_transcoding', 'mime_type', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemTranscodingFlag.value'
        db.alter_column('media_transcoding', 'value', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'Language.comment'
        db.alter_column('languages', 'comment', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Language.part2B'
        db.alter_column('languages', 'part2B', self.gf('telemeta.models.fields.CharField')(max_length=3))

        # Changing field 'Language.name'
        db.alter_column('languages', 'name', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Language.part1'
        db.alter_column('languages', 'part1', self.gf('telemeta.models.fields.CharField')(max_length=1))

        # Changing field 'Language.part2T'
        db.alter_column('languages', 'part2T', self.gf('telemeta.models.fields.CharField')(max_length=3))

        # Changing field 'Language.scope'
        db.alter_column('languages', 'scope', self.gf('telemeta.models.fields.CharField')(max_length=1))

        # Changing field 'Language.identifier'
        db.alter_column('languages', 'identifier', self.gf('telemeta.models.fields.CharField')(max_length=3))

        # Changing field 'Language.type'
        db.alter_column('languages', 'type', self.gf('telemeta.models.fields.CharField')(max_length=1))

        # Changing field 'TapeLength.notes'
        db.alter_column('tape_length', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'TapeLength.value'
        db.alter_column('tape_length', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'UserProfile.function'
        db.alter_column('profiles', 'function', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'UserProfile.expiration_date'
        db.alter_column('profiles', 'expiration_date', self.gf('telemeta.models.fields.DateField')(null=True))

        # Changing field 'UserProfile.telephone'
        db.alter_column('profiles', 'telephone', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'UserProfile.attachment'
        db.alter_column('profiles', 'attachment', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'UserProfile.address'
        db.alter_column('profiles', 'address', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'UserProfile.department'
        db.alter_column('profiles', 'department', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'UserProfile.institution'
        db.alter_column('profiles', 'institution', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'UserProfile.user'
        db.alter_column('profiles', 'user_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['auth.User'], unique=True))

        # Changing field 'Instrument.notes'
        db.alter_column('instruments', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Instrument.name'
        db.alter_column('instruments', 'name', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaItemKeyword.item'
        db.alter_column('media_item_keywords', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemKeyword.keyword'
        db.alter_column('media_item_keywords', 'keyword_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.ContextKeyword']))

        # Changing field 'MetadataWriter.notes'
        db.alter_column('metadata_writers', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MetadataWriter.value'
        db.alter_column('metadata_writers', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaItemTranscoded.date_added'
        db.alter_column('telemeta_media_transcoded', 'date_added', self.gf('telemeta.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'IdentifierType.notes'
        db.alter_column('identifier_type', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'IdentifierType.value'
        db.alter_column('identifier_type', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'PhysicalFormat.notes'
        db.alter_column('physical_formats', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'PhysicalFormat.value'
        db.alter_column('physical_formats', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'PublishingStatus.notes'
        db.alter_column('publishing_status', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'PublishingStatus.value'
        db.alter_column('publishing_status', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'Playlist.author'
        db.alter_column('playlists', 'author', self.gf('telemeta.models.fields.ForeignKey')(db_column='author', to=orm['auth.User']))

        # Changing field 'Playlist.public_id'
        db.alter_column('playlists', 'public_id', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Playlist.description'
        db.alter_column('playlists', 'description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Playlist.title'
        db.alter_column('playlists', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Revision.change_type'
        db.alter_column('revisions', 'change_type', self.gf('telemeta.models.fields.CharField')(max_length=16))

        # Changing field 'Revision.element_type'
        db.alter_column('revisions', 'element_type', self.gf('telemeta.models.fields.CharField')(max_length=16))

        # Changing field 'Revision.user'
        db.alter_column('revisions', 'username', self.gf('telemeta.models.fields.ForeignKey')(db_column='username', to=orm['auth.User']))

        # Changing field 'Revision.time'
        db.alter_column('revisions', 'time', self.gf('telemeta.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Revision.element_id'
        db.alter_column('revisions', 'element_id', self.gf('telemeta.models.fields.IntegerField')())

        # Changing field 'PlaylistResource.playlist'
        db.alter_column('playlist_resources', 'playlist_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Playlist']))

        # Changing field 'PlaylistResource.public_id'
        db.alter_column('playlist_resources', 'public_id', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'PlaylistResource.resource_type'
        db.alter_column('playlist_resources', 'resource_type', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'PlaylistResource.resource_id'
        db.alter_column('playlist_resources', 'resource_id', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'LocationAlias.alias'
        db.alter_column('location_aliases', 'alias', self.gf('telemeta.models.fields.CharField')(max_length=150))

        # Changing field 'LocationAlias.is_authoritative'
        db.alter_column('location_aliases', 'is_authoritative', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'LocationAlias.location'
        db.alter_column('location_aliases', 'location_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Location']))

        # Changing field 'Format.original_comments'
        db.alter_column('media_formats', 'original_comments', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Format.original_number'
        db.alter_column('media_formats', 'original_number', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Format.sticker_presence'
        db.alter_column('media_formats', 'sticker_presence', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'Format.original_status'
        db.alter_column('media_formats', 'original_status', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Format.original_code'
        db.alter_column('media_formats', 'original_code', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Format.recording_system'
        db.alter_column('media_formats', 'recording_system', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Format.original_location'
        db.alter_column('media_formats', 'original_location_id', self.gf('telemeta.models.fields.ForeignKey')(on_delete=models.SET_NULL, to=orm['telemeta.Location'], null=True))

        # Changing field 'Format.tape_speed'
        db.alter_column('media_formats', 'tape_speed_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.TapeSpeed']))

        # Changing field 'Format.original_state'
        db.alter_column('media_formats', 'original_state', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Format.physical_format'
        db.alter_column('media_formats', 'physical_format_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.PhysicalFormat']))

        # Changing field 'Format.item'
        db.alter_column('media_formats', 'item_id', self.gf('telemeta.models.fields.ForeignKey')(on_delete=models.SET_NULL, to=orm['telemeta.MediaItem'], null=True))

        # Changing field 'Format.tape_vendor'
        db.alter_column('media_formats', 'tape_vendor_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.TapeVendor']))

        # Changing field 'Format.tape_thickness'
        db.alter_column('media_formats', 'tape_thickness', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Format.original_channels'
        db.alter_column('media_formats', 'original_channels_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.NumberOfChannels']))

        # Changing field 'Format.tape_reference'
        db.alter_column('media_formats', 'tape_reference', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Format.tape_wheel_diameter'
        db.alter_column('media_formats', 'tape_wheel_diameter_id', self.gf('telemeta.models.fields.WeakForeignKey')(null=True, to=orm['telemeta.TapeWheelDiameter']))

        # Changing field 'Format.original_audio_quality'
        db.alter_column('media_formats', 'original_audio_quality', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaFonds.code'
        db.alter_column('media_fonds', 'code', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'MediaFonds.description'
        db.alter_column('media_fonds', 'description', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaFonds.title'
        db.alter_column('media_fonds', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaFonds.descriptions'
        db.alter_column('media_fonds', 'descriptions', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaFonds.public_access'
        db.alter_column('media_fonds', 'public_access', self.gf('telemeta.models.fields.CharField')(max_length=16))

        # Changing field 'LocationRelation.ancestor_location'
        db.alter_column('location_relations', 'ancestor_location_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Location']))

        # Changing field 'LocationRelation.location'
        db.alter_column('location_relations', 'location_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.Location']))

        # Changing field 'LocationRelation.is_authoritative'
        db.alter_column('location_relations', 'is_authoritative', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'LocationRelation.is_direct'
        db.alter_column('location_relations', 'is_direct', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'InstrumentAlias.notes'
        db.alter_column('instrument_aliases', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'InstrumentAlias.name'
        db.alter_column('instrument_aliases', 'name', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.resource'
        db.alter_column('media_corpus_related', 'resource_id', self.gf('telemeta.models.fields.ForeignKey')(to=orm['telemeta.MediaCorpus']))

        # Changing field 'MediaCorpusRelated.description'
        db.alter_column('media_corpus_related', 'description', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'MediaCorpusRelated.title'
        db.alter_column('media_corpus_related', 'title', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.url'
        db.alter_column('media_corpus_related', 'url', self.gf('telemeta.models.fields.CharField')(max_length=500))

        # Changing field 'MediaCorpusRelated.credits'
        db.alter_column('media_corpus_related', 'credits', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.file'
        db.alter_column('media_corpus_related', 'filename', self.gf('telemeta.models.fields.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaCorpusRelated.date'
        db.alter_column('media_corpus_related', 'date', self.gf('telemeta.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaCorpusRelated.mime_type'
        db.alter_column('media_corpus_related', 'mime_type', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Criteria.key'
        db.alter_column('search_criteria', 'key', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'Criteria.value'
        db.alter_column('search_criteria', 'value', self.gf('telemeta.models.fields.CharField')(max_length=250))

        # Changing field 'EthnicGroup.notes'
        db.alter_column('ethnic_groups', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'EthnicGroup.value'
        db.alter_column('ethnic_groups', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'Rights.notes'
        db.alter_column('rights', 'notes', self.gf('telemeta.models.fields.TextField')())

        # Changing field 'Rights.value'
        db.alter_column('rights', 'value', self.gf('telemeta.models.fields.CharField')(unique=True, max_length=250))

    def backwards(self, orm):

        # Changing field 'RecordingContext.notes'
        db.alter_column('recording_contexts', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'RecordingContext.value'
        db.alter_column('recording_contexts', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Publisher.notes'
        db.alter_column('publishers', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Publisher.value'
        db.alter_column('publishers', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'GenericStyle.notes'
        db.alter_column('generic_styles', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'GenericStyle.value'
        db.alter_column('generic_styles', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'NumberOfChannels.notes'
        db.alter_column('original_channel_number', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'NumberOfChannels.value'
        db.alter_column('original_channel_number', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'CopyType.notes'
        db.alter_column('copy_type', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'CopyType.value'
        db.alter_column('copy_type', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemRelated.description'
        db.alter_column('media_item_related', 'description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaItemRelated.credits'
        db.alter_column('media_item_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemRelated.url'
        db.alter_column('media_item_related', 'url', self.gf('telemeta.models.core.CharField')(max_length=500))

        # Changing field 'MediaItemRelated.title'
        db.alter_column('media_item_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemRelated.item'
        db.alter_column('media_item_related', 'item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemRelated.file'
        db.alter_column('media_item_related', 'filename', self.gf('telemeta.models.core.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaItemRelated.date'
        db.alter_column('media_item_related', 'date', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaItemRelated.mime_type'
        db.alter_column('media_item_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'LocationType.code'
        db.alter_column('location_types', 'code', self.gf('telemeta.models.core.CharField')(max_length=64, unique=True))

        # Changing field 'LocationType.name'
        db.alter_column('location_types', 'name', self.gf('telemeta.models.core.CharField')(max_length=150))

        # Changing field 'MediaCollection.comment'
        db.alter_column('media_collections', 'comment', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollection.code'
        db.alter_column('media_collections', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaCollection.recorded_to_year'
        db.alter_column('media_collections', 'recorded_to_year', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'MediaCollection.reference'
        db.alter_column('media_collections', 'reference', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.creator'
        db.alter_column('media_collections', 'creator', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.metadata_author'
        db.alter_column('media_collections', 'metadata_author_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.MetadataAuthor']))

        # Changing field 'MediaCollection.original_format'
        db.alter_column('media_collections', 'original_format_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.OriginalFormat']))

        # Changing field 'MediaCollection.publisher_serial'
        db.alter_column('media_collections', 'publisher_serial', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.booklet_author'
        db.alter_column('media_collections', 'booklet_author', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.archiver_notes'
        db.alter_column('media_collections', 'archiver_notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollection.recording_context'
        db.alter_column('media_collections', 'recording_context_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.RecordingContext']))

        # Changing field 'MediaCollection.copy_type'
        db.alter_column('media_collections', 'copy_type_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.CopyType']))

        # Changing field 'MediaCollection.collector'
        db.alter_column('media_collections', 'collector', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.year_published'
        db.alter_column('media_collections', 'year_published', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'MediaCollection.description'
        db.alter_column('media_collections', 'description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollection.acquisition_mode'
        db.alter_column('media_collections', 'acquisition_mode_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.AcquisitionMode']))

        # Changing field 'MediaCollection.metadata_writer'
        db.alter_column('media_collections', 'metadata_writer_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.MetadataWriter']))

        # Changing field 'MediaCollection.alt_copies'
        db.alter_column('media_collections', 'alt_copies', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollection.title'
        db.alter_column('media_collections', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.old_code'
        db.alter_column('media_collections', 'old_code', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))

        # Changing field 'MediaCollection.approx_duration'
        db.alter_column('media_collections', 'approx_duration', self.gf('telemeta.models.core.DurationField')())

        # Changing field 'MediaCollection.auto_period_access'
        db.alter_column('media_collections', 'auto_period_access', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'MediaCollection.booklet_description'
        db.alter_column('media_collections', 'booklet_description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollection.media_type'
        db.alter_column('media_collections', 'media_type_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.MediaType']))

        # Changing field 'MediaCollection.status'
        db.alter_column('media_collections', 'status_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.Status']))

        # Changing field 'MediaCollection.travail'
        db.alter_column('media_collections', 'travail', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.external_references'
        db.alter_column('media_collections', 'external_references', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollection.publishing_status'
        db.alter_column('media_collections', 'publishing_status_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.PublishingStatus']))

        # Changing field 'MediaCollection.publisher_collection'
        db.alter_column('media_collections', 'publisher_collection_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.PublisherCollection']))

        # Changing field 'MediaCollection.physical_format'
        db.alter_column('media_collections', 'physical_format_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.PhysicalFormat']))

        # Changing field 'MediaCollection.items_done'
        db.alter_column('media_collections', 'items_done', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.conservation_site'
        db.alter_column('media_collections', 'conservation_site', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.public_access'
        db.alter_column('media_collections', 'public_access', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'MediaCollection.publisher'
        db.alter_column('media_collections', 'publisher_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.Publisher']))

        # Changing field 'MediaCollection.alt_ids'
        db.alter_column('media_collections', 'alt_ids', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.alt_title'
        db.alter_column('media_collections', 'alt_title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.legal_rights'
        db.alter_column('media_collections', 'legal_rights_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.LegalRight']))

        # Changing field 'MediaCollection.cnrs_contributor'
        db.alter_column('media_collections', 'cnrs_contributor', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.physical_items_num'
        db.alter_column('media_collections', 'physical_items_num', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'MediaCollection.collector_is_creator'
        db.alter_column('media_collections', 'collector_is_creator', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'MediaCollection.recorded_from_year'
        db.alter_column('media_collections', 'recorded_from_year', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'MediaCollection.ad_conversion'
        db.alter_column('media_collections', 'ad_conversion_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.AdConversion']))

        # Changing field 'MediaCollection.is_published'
        db.alter_column('media_collections', 'is_published', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'ContextKeyword.notes'
        db.alter_column('context_keywords', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'ContextKeyword.value'
        db.alter_column('context_keywords', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'LegalRight.notes'
        db.alter_column('legal_rights', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'LegalRight.value'
        db.alter_column('legal_rights', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'TapeSpeed.notes'
        db.alter_column('tape_speed', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'TapeSpeed.value'
        db.alter_column('tape_speed', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'InstrumentRelation.instrument'
        db.alter_column('instrument_relations', 'instrument_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Instrument']))

        # Changing field 'InstrumentRelation.parent_instrument'
        db.alter_column('instrument_relations', 'parent_instrument_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Instrument']))

        # Changing field 'MediaItemIdentifier.date_add'
        db.alter_column('media_item_identifier', 'date_add', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'MediaItemIdentifier.date_modified'
        db.alter_column('media_item_identifier', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaItemIdentifier.notes'
        db.alter_column('media_item_identifier', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaItemIdentifier.item'
        db.alter_column('media_item_identifier', 'item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemIdentifier.identifier'
        db.alter_column('media_item_identifier', 'identifier', self.gf('telemeta.models.core.CharField')(max_length=255, unique=True))

        # Changing field 'MediaItemIdentifier.type'
        db.alter_column('media_item_identifier', 'type_id', self.gf('telemeta.models.core.WeakForeignKey')(to=orm['telemeta.IdentifierType'], null=True))

        # Changing field 'MediaItemIdentifier.date_first'
        db.alter_column('media_item_identifier', 'date_first', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'MediaItemIdentifier.date_last'
        db.alter_column('media_item_identifier', 'date_last', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'MediaItemPerformance.instrument'
        db.alter_column('media_item_performances', 'instrument_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.Instrument']))

        # Changing field 'MediaItemPerformance.instruments_num'
        db.alter_column('media_item_performances', 'instruments_num', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemPerformance.alias'
        db.alter_column('media_item_performances', 'alias_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.InstrumentAlias']))

        # Changing field 'MediaItemPerformance.musicians'
        db.alter_column('media_item_performances', 'musicians', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemPerformance.media_item'
        db.alter_column('media_item_performances', 'media_item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'OriginalFormat.notes'
        db.alter_column('original_format', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'OriginalFormat.value'
        db.alter_column('original_format', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'InstrumentAliasRelation.alias'
        db.alter_column('instrument_alias_relations', 'alias_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.InstrumentAlias']))

        # Changing field 'InstrumentAliasRelation.instrument'
        db.alter_column('instrument_alias_relations', 'instrument_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Instrument']))

        # Changing field 'MediaCorpus.code'
        db.alter_column('media_corpus', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaCorpus.recorded_to_year'
        db.alter_column('media_corpus', 'recorded_to_year', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'MediaCorpus.description'
        db.alter_column('media_corpus', 'description', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpus.title'
        db.alter_column('media_corpus', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpus.recorded_from_year'
        db.alter_column('media_corpus', 'recorded_from_year', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'MediaCorpus.descriptions'
        db.alter_column('media_corpus', 'descriptions', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCorpus.public_access'
        db.alter_column('media_corpus', 'public_access', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'MediaType.notes'
        db.alter_column('media_type', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaType.value'
        db.alter_column('media_type', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'AcquisitionMode.notes'
        db.alter_column('acquisition_modes', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'AcquisitionMode.value'
        db.alter_column('acquisition_modes', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Organization.notes'
        db.alter_column('organization', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Organization.value'
        db.alter_column('organization', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaFondsRelated.resource'
        db.alter_column('media_fonds_related', 'resource_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaFonds']))

        # Changing field 'MediaFondsRelated.description'
        db.alter_column('media_fonds_related', 'description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaFondsRelated.title'
        db.alter_column('media_fonds_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaFondsRelated.url'
        db.alter_column('media_fonds_related', 'url', self.gf('telemeta.models.core.CharField')(max_length=500))

        # Changing field 'MediaFondsRelated.credits'
        db.alter_column('media_fonds_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaFondsRelated.file'
        db.alter_column('media_fonds_related', 'filename', self.gf('telemeta.models.core.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaFondsRelated.date'
        db.alter_column('media_fonds_related', 'date', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaFondsRelated.mime_type'
        db.alter_column('media_fonds_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.comment'
        db.alter_column('media_items', 'comment', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaItem.code'
        db.alter_column('media_items', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItem.location_comment'
        db.alter_column('media_items', 'location_comment', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.depositor'
        db.alter_column('media_items', 'depositor', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.contributor'
        db.alter_column('media_items', 'contributor', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.scientist'
        db.alter_column('media_items', 'scientist', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.file'
        db.alter_column('media_items', 'filename', self.gf('telemeta.models.core.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'MediaItem.cultural_area'
        db.alter_column('media_items', 'cultural_area', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.recorded_from_date'
        db.alter_column('media_items', 'recorded_from_date', self.gf('telemeta.models.core.DateField')(null=True))

        # Changing field 'MediaItem.collector'
        db.alter_column('media_items', 'collector', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.author'
        db.alter_column('media_items', 'author', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.old_code'
        db.alter_column('media_items', 'old_code', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.approx_duration'
        db.alter_column('media_items', 'approx_duration', self.gf('telemeta.models.core.DurationField')())

        # Changing field 'MediaItem.auto_period_access'
        db.alter_column('media_items', 'auto_period_access', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'MediaItem.language_iso'
        db.alter_column('media_items', 'language_iso_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['telemeta.Language'], null=True))

        # Changing field 'MediaItem.location'
        db.alter_column('media_items', 'location_id', self.gf('telemeta.models.core.WeakForeignKey')(to=orm['telemeta.Location'], null=True))

        # Changing field 'MediaItem.creator_reference'
        db.alter_column('media_items', 'creator_reference', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.collector_selection'
        db.alter_column('media_items', 'collector_selection', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.external_references'
        db.alter_column('media_items', 'external_references', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaItem.track'
        db.alter_column('media_items', 'track', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.title'
        db.alter_column('media_items', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.collector_from_collection'
        db.alter_column('media_items', 'collector_from_collection', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'MediaItem.moda_execut'
        db.alter_column('media_items', 'moda_execut', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.collection'
        db.alter_column('media_items', 'collection_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaCollection']))

        # Changing field 'MediaItem.ethnic_group'
        db.alter_column('media_items', 'ethnic_group_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.EthnicGroup']))

        # Changing field 'MediaItem.media_type'
        db.alter_column('media_items', 'media_type_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.MediaType']))

        # Changing field 'MediaItem.public_access'
        db.alter_column('media_items', 'public_access', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'MediaItem.mimetype'
        db.alter_column('media_items', 'mimetype', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'MediaItem.topic'
        db.alter_column('media_items', 'topic_id', self.gf('telemeta.models.core.WeakForeignKey')(to=orm['telemeta.Topic'], null=True))

        # Changing field 'MediaItem.organization'
        db.alter_column('media_items', 'organization_id', self.gf('telemeta.models.core.WeakForeignKey')(to=orm['telemeta.Organization'], null=True))

        # Changing field 'MediaItem.context_comment'
        db.alter_column('media_items', 'context_comment', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaItem.language'
        db.alter_column('media_items', 'language', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.rights'
        db.alter_column('media_items', 'rights_id', self.gf('telemeta.models.core.WeakForeignKey')(to=orm['telemeta.Rights'], null=True))

        # Changing field 'MediaItem.alt_title'
        db.alter_column('media_items', 'alt_title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.summary'
        db.alter_column('media_items', 'summary', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaItem.recorded_to_date'
        db.alter_column('media_items', 'recorded_to_date', self.gf('telemeta.models.core.DateField')(null=True))

        # Changing field 'MediaItem.generic_style'
        db.alter_column('media_items', 'generic_style_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.GenericStyle']))

        # Changing field 'MediaItem.digitalist'
        db.alter_column('media_items', 'digitalist', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.digitization_date'
        db.alter_column('media_items', 'digitization_date', self.gf('telemeta.models.core.DateField')(null=True))

        # Changing field 'MediaItem.recordist'
        db.alter_column('media_items', 'recordist', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.publishing_date'
        db.alter_column('media_items', 'publishing_date', self.gf('telemeta.models.core.DateField')(null=True))

        # Changing field 'MediaItem.vernacular_style'
        db.alter_column('media_items', 'vernacular_style_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.VernacularStyle']))

        # Changing field 'MediaItemMarker.public_id'
        db.alter_column('media_markers', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemMarker.description'
        db.alter_column('media_markers', 'description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaItemMarker.author'
        db.alter_column('media_markers', 'author_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'MediaItemMarker.title'
        db.alter_column('media_markers', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemMarker.item'
        db.alter_column('media_markers', 'item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemMarker.time'
        db.alter_column('media_markers', 'time', self.gf('telemeta.models.core.FloatField')())

        # Changing field 'MediaItemMarker.date'
        db.alter_column('media_markers', 'date', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'VernacularStyle.notes'
        db.alter_column('vernacular_styles', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'VernacularStyle.value'
        db.alter_column('vernacular_styles', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'TapeWheelDiameter.notes'
        db.alter_column('tape_wheel_diameter', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'TapeWheelDiameter.value'
        db.alter_column('tape_wheel_diameter', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Topic.notes'
        db.alter_column('topic', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Topic.value'
        db.alter_column('topic', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaCollectionRelated.description'
        db.alter_column('media_collection_related', 'description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollectionRelated.title'
        db.alter_column('media_collection_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollectionRelated.url'
        db.alter_column('media_collection_related', 'url', self.gf('telemeta.models.core.CharField')(max_length=500))

        # Changing field 'MediaCollectionRelated.collection'
        db.alter_column('media_collection_related', 'collection_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaCollection']))

        # Changing field 'MediaCollectionRelated.credits'
        db.alter_column('media_collection_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollectionRelated.file'
        db.alter_column('media_collection_related', 'filename', self.gf('telemeta.models.core.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaCollectionRelated.date'
        db.alter_column('media_collection_related', 'date', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaCollectionRelated.mime_type'
        db.alter_column('media_collection_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'TapeVendor.notes'
        db.alter_column('tape_vendor', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'TapeVendor.value'
        db.alter_column('tape_vendor', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'TapeWidth.notes'
        db.alter_column('tape_width', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'TapeWidth.value'
        db.alter_column('tape_width', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Location.name'
        db.alter_column('locations', 'name', self.gf('telemeta.models.core.CharField')(max_length=150, unique=True))

        # Changing field 'Location.type'
        db.alter_column('locations', 'type', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'Location.complete_type'
        db.alter_column('locations', 'complete_type_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.LocationType']))

        # Changing field 'Location.longitude'
        db.alter_column('locations', 'longitude', self.gf('telemeta.models.core.FloatField')(null=True))

        # Changing field 'Location.current_location'
        db.alter_column('locations', 'current_location_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.Location']))

        # Changing field 'Location.latitude'
        db.alter_column('locations', 'latitude', self.gf('telemeta.models.core.FloatField')(null=True))

        # Changing field 'Location.is_authoritative'
        db.alter_column('locations', 'is_authoritative', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'MediaPart.item'
        db.alter_column('media_parts', 'item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaPart.title'
        db.alter_column('media_parts', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaPart.end'
        db.alter_column('media_parts', 'end', self.gf('telemeta.models.core.FloatField')())

        # Changing field 'MediaPart.start'
        db.alter_column('media_parts', 'start', self.gf('telemeta.models.core.FloatField')())

        # Changing field 'MediaCollectionIdentifier.date_add'
        db.alter_column('media_collection_identifier', 'date_add', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'MediaCollectionIdentifier.date_modified'
        db.alter_column('media_collection_identifier', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaCollectionIdentifier.notes'
        db.alter_column('media_collection_identifier', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCollectionIdentifier.collection'
        db.alter_column('media_collection_identifier', 'collection_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaCollection']))

        # Changing field 'MediaCollectionIdentifier.identifier'
        db.alter_column('media_collection_identifier', 'identifier', self.gf('telemeta.models.core.CharField')(max_length=255, unique=True))

        # Changing field 'MediaCollectionIdentifier.type'
        db.alter_column('media_collection_identifier', 'type_id', self.gf('telemeta.models.core.WeakForeignKey')(to=orm['telemeta.IdentifierType'], null=True))

        # Changing field 'MediaCollectionIdentifier.date_first'
        db.alter_column('media_collection_identifier', 'date_first', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'MediaCollectionIdentifier.date_last'
        db.alter_column('media_collection_identifier', 'date_last', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'PublisherCollection.publisher'
        db.alter_column('publisher_collections', 'publisher_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Publisher']))

        # Changing field 'PublisherCollection.value'
        db.alter_column('publisher_collections', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Search.username'
        db.alter_column('searches', 'username', self.gf('telemeta.models.core.ForeignKey')(db_column='username', to=orm['auth.User']))

        # Changing field 'Search.date'
        db.alter_column('searches', 'date', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Search.description'
        db.alter_column('searches', 'description', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'EthnicGroupAlias.ethnic_group'
        db.alter_column('ethnic_group_aliases', 'ethnic_group_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.EthnicGroup']))

        # Changing field 'EthnicGroupAlias.value'
        db.alter_column('ethnic_group_aliases', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MetadataAuthor.notes'
        db.alter_column('metadata_authors', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MetadataAuthor.value'
        db.alter_column('metadata_authors', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemAnalysis.analyzer_id'
        db.alter_column('media_analysis', 'analyzer_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.value'
        db.alter_column('media_analysis', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.item'
        db.alter_column('media_analysis', 'item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemAnalysis.unit'
        db.alter_column('media_analysis', 'unit', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.name'
        db.alter_column('media_analysis', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Status.notes'
        db.alter_column('media_status', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Status.value'
        db.alter_column('media_status', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'AdConversion.notes'
        db.alter_column('ad_conversions', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'AdConversion.value'
        db.alter_column('ad_conversions', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemTranscodingFlag.date'
        db.alter_column('media_transcoding', 'date', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaItemTranscodingFlag.item'
        db.alter_column('media_transcoding', 'item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemTranscodingFlag.mime_type'
        db.alter_column('media_transcoding', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemTranscodingFlag.value'
        db.alter_column('media_transcoding', 'value', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Language.comment'
        db.alter_column('languages', 'comment', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Language.part2B'
        db.alter_column('languages', 'part2B', self.gf('telemeta.models.core.CharField')(max_length=3))

        # Changing field 'Language.name'
        db.alter_column('languages', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Language.part1'
        db.alter_column('languages', 'part1', self.gf('telemeta.models.core.CharField')(max_length=1))

        # Changing field 'Language.part2T'
        db.alter_column('languages', 'part2T', self.gf('telemeta.models.core.CharField')(max_length=3))

        # Changing field 'Language.scope'
        db.alter_column('languages', 'scope', self.gf('telemeta.models.core.CharField')(max_length=1))

        # Changing field 'Language.identifier'
        db.alter_column('languages', 'identifier', self.gf('telemeta.models.core.CharField')(max_length=3))

        # Changing field 'Language.type'
        db.alter_column('languages', 'type', self.gf('telemeta.models.core.CharField')(max_length=1))

        # Changing field 'TapeLength.notes'
        db.alter_column('tape_length', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'TapeLength.value'
        db.alter_column('tape_length', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'UserProfile.function'
        db.alter_column('profiles', 'function', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.expiration_date'
        db.alter_column('profiles', 'expiration_date', self.gf('telemeta.models.core.DateField')(null=True))

        # Changing field 'UserProfile.telephone'
        db.alter_column('profiles', 'telephone', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.attachment'
        db.alter_column('profiles', 'attachment', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.address'
        db.alter_column('profiles', 'address', self.gf('telemeta.models.core.TextField')())

        # Changing field 'UserProfile.department'
        db.alter_column('profiles', 'department', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.institution'
        db.alter_column('profiles', 'institution', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.user'
        db.alter_column('profiles', 'user_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['auth.User'], unique=True))

        # Changing field 'Instrument.notes'
        db.alter_column('instruments', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Instrument.name'
        db.alter_column('instruments', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemKeyword.item'
        db.alter_column('media_item_keywords', 'item_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaItem']))

        # Changing field 'MediaItemKeyword.keyword'
        db.alter_column('media_item_keywords', 'keyword_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.ContextKeyword']))

        # Changing field 'MetadataWriter.notes'
        db.alter_column('metadata_writers', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MetadataWriter.value'
        db.alter_column('metadata_writers', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemTranscoded.date_added'
        db.alter_column('telemeta_media_transcoded', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'IdentifierType.notes'
        db.alter_column('identifier_type', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'IdentifierType.value'
        db.alter_column('identifier_type', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'PhysicalFormat.notes'
        db.alter_column('physical_formats', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'PhysicalFormat.value'
        db.alter_column('physical_formats', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'PublishingStatus.notes'
        db.alter_column('publishing_status', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'PublishingStatus.value'
        db.alter_column('publishing_status', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Playlist.author'
        db.alter_column('playlists', 'author', self.gf('telemeta.models.core.ForeignKey')(db_column='author', to=orm['auth.User']))

        # Changing field 'Playlist.public_id'
        db.alter_column('playlists', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Playlist.description'
        db.alter_column('playlists', 'description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Playlist.title'
        db.alter_column('playlists', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Revision.change_type'
        db.alter_column('revisions', 'change_type', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'Revision.element_type'
        db.alter_column('revisions', 'element_type', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'Revision.user'
        db.alter_column('revisions', 'username', self.gf('telemeta.models.core.ForeignKey')(db_column='username', to=orm['auth.User']))

        # Changing field 'Revision.time'
        db.alter_column('revisions', 'time', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Revision.element_id'
        db.alter_column('revisions', 'element_id', self.gf('telemeta.models.core.IntegerField')())

        # Changing field 'PlaylistResource.playlist'
        db.alter_column('playlist_resources', 'playlist_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Playlist']))

        # Changing field 'PlaylistResource.public_id'
        db.alter_column('playlist_resources', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'PlaylistResource.resource_type'
        db.alter_column('playlist_resources', 'resource_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'PlaylistResource.resource_id'
        db.alter_column('playlist_resources', 'resource_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'LocationAlias.alias'
        db.alter_column('location_aliases', 'alias', self.gf('telemeta.models.core.CharField')(max_length=150))

        # Changing field 'LocationAlias.is_authoritative'
        db.alter_column('location_aliases', 'is_authoritative', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'LocationAlias.location'
        db.alter_column('location_aliases', 'location_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Location']))

        # Changing field 'Format.original_comments'
        db.alter_column('media_formats', 'original_comments', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Format.original_number'
        db.alter_column('media_formats', 'original_number', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.sticker_presence'
        db.alter_column('media_formats', 'sticker_presence', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Format.original_status'
        db.alter_column('media_formats', 'original_status', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.original_code'
        db.alter_column('media_formats', 'original_code', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.recording_system'
        db.alter_column('media_formats', 'recording_system', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.original_location'
        db.alter_column('media_formats', 'original_location_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['telemeta.Location'], null=True))

        # Changing field 'Format.tape_speed'
        db.alter_column('media_formats', 'tape_speed_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.TapeSpeed']))

        # Changing field 'Format.original_state'
        db.alter_column('media_formats', 'original_state', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Format.physical_format'
        db.alter_column('media_formats', 'physical_format_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.PhysicalFormat']))

        # Changing field 'Format.item'
        db.alter_column('media_formats', 'item_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['telemeta.MediaItem'], null=True))

        # Changing field 'Format.tape_vendor'
        db.alter_column('media_formats', 'tape_vendor_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.TapeVendor']))

        # Changing field 'Format.tape_thickness'
        db.alter_column('media_formats', 'tape_thickness', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.original_channels'
        db.alter_column('media_formats', 'original_channels_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.NumberOfChannels']))

        # Changing field 'Format.tape_reference'
        db.alter_column('media_formats', 'tape_reference', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.tape_wheel_diameter'
        db.alter_column('media_formats', 'tape_wheel_diameter_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.TapeWheelDiameter']))

        # Changing field 'Format.original_audio_quality'
        db.alter_column('media_formats', 'original_audio_quality', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaFonds.code'
        db.alter_column('media_fonds', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaFonds.description'
        db.alter_column('media_fonds', 'description', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaFonds.title'
        db.alter_column('media_fonds', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaFonds.descriptions'
        db.alter_column('media_fonds', 'descriptions', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaFonds.public_access'
        db.alter_column('media_fonds', 'public_access', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'LocationRelation.ancestor_location'
        db.alter_column('location_relations', 'ancestor_location_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Location']))

        # Changing field 'LocationRelation.location'
        db.alter_column('location_relations', 'location_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.Location']))

        # Changing field 'LocationRelation.is_authoritative'
        db.alter_column('location_relations', 'is_authoritative', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'LocationRelation.is_direct'
        db.alter_column('location_relations', 'is_direct', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'InstrumentAlias.notes'
        db.alter_column('instrument_aliases', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'InstrumentAlias.name'
        db.alter_column('instrument_aliases', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.resource'
        db.alter_column('media_corpus_related', 'resource_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['telemeta.MediaCorpus']))

        # Changing field 'MediaCorpusRelated.description'
        db.alter_column('media_corpus_related', 'description', self.gf('telemeta.models.core.TextField')())

        # Changing field 'MediaCorpusRelated.title'
        db.alter_column('media_corpus_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.url'
        db.alter_column('media_corpus_related', 'url', self.gf('telemeta.models.core.CharField')(max_length=500))

        # Changing field 'MediaCorpusRelated.credits'
        db.alter_column('media_corpus_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.file'
        db.alter_column('media_corpus_related', 'filename', self.gf('telemeta.models.core.FileField')(max_length=255, db_column='filename'))

        # Changing field 'MediaCorpusRelated.date'
        db.alter_column('media_corpus_related', 'date', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MediaCorpusRelated.mime_type'
        db.alter_column('media_corpus_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Criteria.key'
        db.alter_column('search_criteria', 'key', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Criteria.value'
        db.alter_column('search_criteria', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'EthnicGroup.notes'
        db.alter_column('ethnic_groups', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'EthnicGroup.value'
        db.alter_column('ethnic_groups', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Rights.notes'
        db.alter_column('rights', 'notes', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Rights.value'
        db.alter_column('rights', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

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
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.adconversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'AdConversion', 'db_table': "'ad_conversions'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.contextkeyword': {
            'Meta': {'ordering': "['value']", 'object_name': 'ContextKeyword', 'db_table': "'context_keywords'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.copytype': {
            'Meta': {'ordering': "['value']", 'object_name': 'CopyType', 'db_table': "'copy_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.criteria': {
            'Meta': {'object_name': 'Criteria', 'db_table': "'search_criteria'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'value': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.ethnicgroup': {
            'Meta': {'ordering': "['value']", 'object_name': 'EthnicGroup', 'db_table': "'ethnic_groups'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.ethnicgroupalias': {
            'Meta': {'ordering': "['ethnic_group__value']", 'unique_together': "(('ethnic_group', 'value'),)", 'object_name': 'EthnicGroupAlias', 'db_table': "'ethnic_group_aliases'"},
            'ethnic_group': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['telemeta.EthnicGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.format': {
            'Meta': {'object_name': 'Format', 'db_table': "'media_formats'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'format'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.MediaItem']", 'blank': 'True', 'null': 'True'}),
            'original_audio_quality': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_channels': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.NumberOfChannels']"}),
            'original_code': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'original_comments': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_location': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'format'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Location']", 'blank': 'True', 'null': 'True'}),
            'original_number': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'original_state': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_status': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'physical_format': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'recording_system': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'sticker_presence': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'tape_reference': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'tape_speed': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeSpeed']"}),
            'tape_thickness': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'tape_vendor': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeVendor']"}),
            'tape_wheel_diameter': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeWheelDiameter']"})
        },
        'telemeta.genericstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'GenericStyle', 'db_table': "'generic_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.identifiertype': {
            'Meta': {'ordering': "['value']", 'object_name': 'IdentifierType', 'db_table': "'identifier_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.instrument': {
            'Meta': {'ordering': "['name']", 'object_name': 'Instrument', 'db_table': "'instruments'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'telemeta.instrumentalias': {
            'Meta': {'ordering': "['name']", 'object_name': 'InstrumentAlias', 'db_table': "'instrument_aliases'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'telemeta.instrumentaliasrelation': {
            'Meta': {'unique_together': "(('alias', 'instrument'),)", 'object_name': 'InstrumentAliasRelation', 'db_table': "'instrument_alias_relations'"},
            'alias': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'other_name'", 'to': "orm['telemeta.InstrumentAlias']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'relation'", 'to': "orm['telemeta.Instrument']"})
        },
        'telemeta.instrumentrelation': {
            'Meta': {'unique_together': "(('instrument', 'parent_instrument'),)", 'object_name': 'InstrumentRelation', 'db_table': "'instrument_relations'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'parent_relation'", 'to': "orm['telemeta.Instrument']"}),
            'parent_instrument': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'child_relation'", 'to': "orm['telemeta.Instrument']"})
        },
        'telemeta.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language', 'db_table': "'languages'"},
            'comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'part1': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'part2B': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'part2T': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'scope': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'type': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'})
        },
        'telemeta.legalright': {
            'Meta': {'ordering': "['value']", 'object_name': 'LegalRight', 'db_table': "'legal_rights'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location', 'db_table': "'locations'"},
            'complete_type': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['telemeta.LocationType']"}),
            'current_location': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'past_names'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Location']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('telemeta.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('telemeta.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'type': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'})
        },
        'telemeta.locationalias': {
            'Meta': {'ordering': "['alias']", 'unique_together': "(('location', 'alias'),)", 'object_name': 'LocationAlias', 'db_table': "'location_aliases'"},
            'alias': ('telemeta.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['telemeta.Location']"})
        },
        'telemeta.locationrelation': {
            'Meta': {'ordering': "['ancestor_location__name']", 'unique_together': "(('location', 'ancestor_location'),)", 'object_name': 'LocationRelation', 'db_table': "'location_relations'"},
            'ancestor_location': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'descendant_relations'", 'to': "orm['telemeta.Location']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'is_direct': ('telemeta.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'location': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'ancestor_relations'", 'to': "orm['telemeta.Location']"})
        },
        'telemeta.locationtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocationType', 'db_table': "'location_types'"},
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'max_length': '150'})
        },
        'telemeta.mediacollection': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCollection', 'db_table': "'media_collections'"},
            'acquisition_mode': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AcquisitionMode']"}),
            'ad_conversion': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AdConversion']"}),
            'alt_copies': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'alt_ids': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'alt_title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'archiver_notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.fields.BooleanField', [], {'default': 'True'}),
            'booklet_author': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'booklet_description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'cnrs_contributor': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collector': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_is_creator': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'conservation_site': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'copy_type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.CopyType']"}),
            'creator': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'external_references': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'items_done': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'legal_rights': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.LegalRight']"}),
            'media_type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaType']"}),
            'metadata_author': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataAuthor']"}),
            'metadata_writer': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataWriter']"}),
            'old_code': ('telemeta.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'original_format': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.OriginalFormat']"}),
            'physical_format': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'physical_items_num': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'public_access': ('telemeta.models.fields.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publisher': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Publisher']"}),
            'publisher_collection': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublisherCollection']"}),
            'publisher_serial': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'publishing_status': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublishingStatus']"}),
            'recorded_from_year': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recording_context': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.RecordingContext']"}),
            'reference': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'status': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Status']"}),
            'title': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'travail': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'year_published': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'telemeta.mediacollectionidentifier': {
            'Meta': {'unique_together': "(('identifier', 'collection'),)", 'object_name': 'MediaCollectionIdentifier', 'db_table': "'media_collection_identifier'"},
            'collection': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'identifiers'", 'to': "orm['telemeta.MediaCollection']"}),
            'date_add': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_first': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_last': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.IdentifierType']", 'null': 'True', 'blank': 'True'})
        },
        'telemeta.mediacollectionrelated': {
            'Meta': {'object_name': 'MediaCollectionRelated', 'db_table': "'media_collection_related'"},
            'collection': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaCollection']"}),
            'credits': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediacorpus': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCorpus', 'db_table': "'media_corpus'"},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'corpus'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.MediaCollection']"}),
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'description': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'descriptions': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_access': ('telemeta.models.fields.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'recorded_from_year': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.mediacorpusrelated': {
            'Meta': {'object_name': 'MediaCorpusRelated', 'db_table': "'media_corpus_related'"},
            'credits': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'resource': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaCorpus']"}),
            'title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediafonds': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaFonds', 'db_table': "'media_fonds'"},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fonds'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.MediaCorpus']"}),
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'description': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'descriptions': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_access': ('telemeta.models.fields.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'title': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.mediafondsrelated': {
            'Meta': {'object_name': 'MediaFondsRelated', 'db_table': "'media_fonds_related'"},
            'credits': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'resource': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaFonds']"}),
            'title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediaitem': {
            'Meta': {'object_name': 'MediaItem', 'db_table': "'media_items'"},
            'alt_title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'author': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collection': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'items'", 'to': "orm['telemeta.MediaCollection']"}),
            'collector': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_from_collection': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'collector_selection': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'context_comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contributor': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'creator_reference': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'cultural_area': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'depositor': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitalist': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitization_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ethnic_group': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.EthnicGroup']"}),
            'external_references': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'language_iso': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Language']", 'blank': 'True', 'null': 'True'}),
            'location': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'media_type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaType']"}),
            'mimetype': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'moda_execut': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'old_code': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'organization': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Organization']", 'null': 'True', 'blank': 'True'}),
            'public_access': ('telemeta.models.fields.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publishing_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_from_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_to_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recordist': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'rights': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Rights']", 'null': 'True', 'blank': 'True'}),
            'scientist': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'summary': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'topic': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Topic']", 'null': 'True', 'blank': 'True'}),
            'track': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'vernacular_style': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.VernacularStyle']"})
        },
        'telemeta.mediaitemanalysis': {
            'Meta': {'ordering': "['name']", 'object_name': 'MediaItemAnalysis', 'db_table': "'media_analysis'"},
            'analyzer_id': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'analysis'", 'to': "orm['telemeta.MediaItem']"}),
            'name': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'unit': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemidentifier': {
            'Meta': {'unique_together': "(('identifier', 'item'),)", 'object_name': 'MediaItemIdentifier', 'db_table': "'media_item_identifier'"},
            'date_add': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_first': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_last': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'identifiers'", 'to': "orm['telemeta.MediaItem']"}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.IdentifierType']", 'null': 'True', 'blank': 'True'})
        },
        'telemeta.mediaitemkeyword': {
            'Meta': {'unique_together': "(('item', 'keyword'),)", 'object_name': 'MediaItemKeyword', 'db_table': "'media_item_keywords'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'keyword_relations'", 'to': "orm['telemeta.MediaItem']"}),
            'keyword': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'item_relations'", 'to': "orm['telemeta.ContextKeyword']"})
        },
        'telemeta.mediaitemmarker': {
            'Meta': {'ordering': "['time']", 'object_name': 'MediaItemMarker', 'db_table': "'media_markers'"},
            'author': ('telemeta.models.fields.ForeignKey', [], {'default': 'None', 'related_name': "'markers'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'date': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'markers'", 'to': "orm['telemeta.MediaItem']"}),
            'public_id': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'time': ('telemeta.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemperformance': {
            'Meta': {'object_name': 'MediaItemPerformance', 'db_table': "'media_item_performances'"},
            'alias': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'performances'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.InstrumentAlias']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'performances'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Instrument']"}),
            'instruments_num': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'media_item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'performances'", 'to': "orm['telemeta.MediaItem']"}),
            'musicians': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        'telemeta.mediaitemrelated': {
            'Meta': {'object_name': 'MediaItemRelated', 'db_table': "'media_item_related'"},
            'credits': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'date': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediaitemtranscoded': {
            'Meta': {'object_name': 'MediaItemTranscoded', 'db_table': "'telemeta_media_transcoded'"},
            'date_added': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transcoded'", 'to': "orm['telemeta.MediaItem']"}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'telemeta.mediaitemtranscodingflag': {
            'Meta': {'object_name': 'MediaItemTranscodingFlag', 'db_table': "'media_transcoding'"},
            'date': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'transcoding'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'value': ('telemeta.models.fields.BooleanField', [], {'default': 'False'})
        },
        'telemeta.mediapart': {
            'Meta': {'object_name': 'MediaPart', 'db_table': "'media_parts'"},
            'end': ('telemeta.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'parts'", 'to': "orm['telemeta.MediaItem']"}),
            'start': ('telemeta.models.fields.FloatField', [], {}),
            'title': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.mediatype': {
            'Meta': {'ordering': "['value']", 'object_name': 'MediaType', 'db_table': "'media_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadataauthor': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataAuthor', 'db_table': "'metadata_authors'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadatawriter': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataWriter', 'db_table': "'metadata_writers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.numberofchannels': {
            'Meta': {'ordering': "['value']", 'object_name': 'NumberOfChannels', 'db_table': "'original_channel_number'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.organization': {
            'Meta': {'ordering': "['value']", 'object_name': 'Organization', 'db_table': "'organization'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.originalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'OriginalFormat', 'db_table': "'original_format'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.physicalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'PhysicalFormat', 'db_table': "'physical_formats'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.playlist': {
            'Meta': {'object_name': 'Playlist', 'db_table': "'playlists'"},
            'author': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'playlists'", 'db_column': "'author'", 'to': u"orm['auth.User']"}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_id': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'title': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.playlistresource': {
            'Meta': {'object_name': 'PlaylistResource', 'db_table': "'playlist_resources'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playlist': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['telemeta.Playlist']"}),
            'public_id': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'resource_id': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'resource_type': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.publisher': {
            'Meta': {'ordering': "['value']", 'object_name': 'Publisher', 'db_table': "'publishers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.publishercollection': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublisherCollection', 'db_table': "'publisher_collections'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'publisher_collections'", 'to': "orm['telemeta.Publisher']"}),
            'value': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.publishingstatus': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublishingStatus', 'db_table': "'publishing_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.recordingcontext': {
            'Meta': {'ordering': "['value']", 'object_name': 'RecordingContext', 'db_table': "'recording_contexts'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.revision': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Revision', 'db_table': "'revisions'"},
            'change_type': ('telemeta.models.fields.CharField', [], {'max_length': '16'}),
            'element_id': ('telemeta.models.fields.IntegerField', [], {}),
            'element_type': ('telemeta.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'revisions'", 'db_column': "'username'", 'to': u"orm['auth.User']"})
        },
        'telemeta.rights': {
            'Meta': {'ordering': "['value']", 'object_name': 'Rights', 'db_table': "'rights'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.search': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Search', 'db_table': "'searches'"},
            'criteria': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'search'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.Criteria']"}),
            'date': ('telemeta.models.fields.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'searches'", 'db_column': "'username'", 'to': u"orm['auth.User']"})
        },
        'telemeta.status': {
            'Meta': {'ordering': "['value']", 'object_name': 'Status', 'db_table': "'media_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapelength': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeLength', 'db_table': "'tape_length'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapespeed': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeSpeed', 'db_table': "'tape_speed'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapevendor': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeVendor', 'db_table': "'tape_vendor'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapewheeldiameter': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeWheelDiameter', 'db_table': "'tape_wheel_diameter'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.tapewidth': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeWidth', 'db_table': "'tape_width'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.topic': {
            'Meta': {'ordering': "['value']", 'object_name': 'Topic', 'db_table': "'topic'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'profiles'"},
            'address': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'attachment': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'department': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'expiration_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'function': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'telephone': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'user': ('telemeta.models.fields.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        'telemeta.vernacularstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'VernacularStyle', 'db_table': "'vernacular_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['telemeta']
