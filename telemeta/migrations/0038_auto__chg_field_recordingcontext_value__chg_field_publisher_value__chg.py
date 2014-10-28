# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RecordingContext.value'
        db.alter_column('recording_contexts', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'Publisher.value'
        db.alter_column('publishers', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'GenericStyle.value'
        db.alter_column('generic_styles', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'NumberOfChannels.value'
        db.alter_column('original_channel_number', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'CopyType.value'
        db.alter_column('copy_type', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaItemRelated.credits'
        db.alter_column('media_item_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemRelated.title'
        db.alter_column('media_item_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemRelated.mime_type'
        db.alter_column('media_item_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=512, null=True))

        # Changing field 'MediaCollection.code'
        db.alter_column('media_collections', 'code', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaCollection.reference'
        db.alter_column('media_collections', 'reference', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.creator'
        db.alter_column('media_collections', 'creator', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.publisher_serial'
        db.alter_column('media_collections', 'publisher_serial', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.booklet_author'
        db.alter_column('media_collections', 'booklet_author', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.collector'
        db.alter_column('media_collections', 'collector', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.title'
        db.alter_column('media_collections', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.items_done'
        db.alter_column('media_collections', 'items_done', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.conservation_site'
        db.alter_column('media_collections', 'conservation_site', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.old_code'
        db.alter_column('media_collections', 'old_code', self.gf('telemeta.models.core.CharField')(max_length=512, null=True))

        # Changing field 'MediaCollection.alt_title'
        db.alter_column('media_collections', 'alt_title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollection.cnrs_contributor'
        db.alter_column('media_collections', 'cnrs_contributor', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'ContextKeyword.value'
        db.alter_column('context_keywords', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'LegalRight.value'
        db.alter_column('legal_rights', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'TapeSpeed.value'
        db.alter_column('tape_speed', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaItemPerformance.instruments_num'
        db.alter_column('media_item_performances', 'instruments_num', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemPerformance.musicians'
        db.alter_column('media_item_performances', 'musicians', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCorpus.code'
        db.alter_column('media_corpus', 'code', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaCorpus.title'
        db.alter_column('media_corpus', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaType.value'
        db.alter_column('media_type', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'AcquisitionMode.value'
        db.alter_column('acquisition_modes', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'Organization.value'
        db.alter_column('organization', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaFondsRelated.title'
        db.alter_column('media_fonds_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaFondsRelated.credits'
        db.alter_column('media_fonds_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaFondsRelated.mime_type'
        db.alter_column('media_fonds_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=512, null=True))

        # Changing field 'MediaItem.code'
        db.alter_column('media_items', 'code', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaItem.location_comment'
        db.alter_column('media_items', 'location_comment', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.contributor'
        db.alter_column('media_items', 'contributor', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.scientist'
        db.alter_column('media_items', 'scientist', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.cultural_area'
        db.alter_column('media_items', 'cultural_area', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.collector'
        db.alter_column('media_items', 'collector', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.author'
        db.alter_column('media_items', 'author', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.old_code'
        db.alter_column('media_items', 'old_code', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.creator_reference'
        db.alter_column('media_items', 'creator_reference', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.collector_selection'
        db.alter_column('media_items', 'collector_selection', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.track'
        db.alter_column('media_items', 'track', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.title'
        db.alter_column('media_items', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.moda_execut'
        db.alter_column('media_items', 'moda_execut', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.depositor'
        db.alter_column('media_items', 'depositor', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.language'
        db.alter_column('media_items', 'language', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.alt_title'
        db.alter_column('media_items', 'alt_title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.digitalist'
        db.alter_column('media_items', 'digitalist', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItem.recordist'
        db.alter_column('media_items', 'recordist', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemMarker.public_id'
        db.alter_column('media_markers', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemMarker.title'
        db.alter_column('media_markers', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'VernacularStyle.value'
        db.alter_column('vernacular_styles', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'TapeWheelDiameter.value'
        db.alter_column('tape_wheel_diameter', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'Topic.value'
        db.alter_column('topic', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaCollectionRelated.title'
        db.alter_column('media_collection_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollectionRelated.credits'
        db.alter_column('media_collection_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCollectionRelated.mime_type'
        db.alter_column('media_collection_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=512, null=True))

        # Changing field 'TapeVendor.value'
        db.alter_column('tape_vendor', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'TapeWidth.value'
        db.alter_column('tape_width', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaPart.title'
        db.alter_column('media_parts', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'PublisherCollection.value'
        db.alter_column('publisher_collections', 'value', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Search.description'
        db.alter_column('searches', 'description', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'EthnicGroupAlias.value'
        db.alter_column('ethnic_group_aliases', 'value', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MetadataAuthor.value'
        db.alter_column('metadata_authors', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaItemAnalysis.analyzer_id'
        db.alter_column('media_analysis', 'analyzer_id', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemAnalysis.value'
        db.alter_column('media_analysis', 'value', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemAnalysis.unit'
        db.alter_column('media_analysis', 'unit', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaItemAnalysis.name'
        db.alter_column('media_analysis', 'name', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Status.value'
        db.alter_column('media_status', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'AdConversion.value'
        db.alter_column('ad_conversions', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaItemTranscodingFlag.mime_type'
        db.alter_column('media_transcoding', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Language.name'
        db.alter_column('languages', 'name', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'TapeLength.value'
        db.alter_column('tape_length', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'UserProfile.function'
        db.alter_column('profiles', 'function', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'UserProfile.telephone'
        db.alter_column('profiles', 'telephone', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'UserProfile.attachment'
        db.alter_column('profiles', 'attachment', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'UserProfile.department'
        db.alter_column('profiles', 'department', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'UserProfile.institution'
        db.alter_column('profiles', 'institution', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Instrument.name'
        db.alter_column('instruments', 'name', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MetadataWriter.value'
        db.alter_column('metadata_writers', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'IdentifierType.value'
        db.alter_column('identifier_type', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'PhysicalFormat.value'
        db.alter_column('physical_formats', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'PublishingStatus.value'
        db.alter_column('publishing_status', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'Playlist.public_id'
        db.alter_column('playlists', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Playlist.title'
        db.alter_column('playlists', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'PlaylistResource.public_id'
        db.alter_column('playlist_resources', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'PlaylistResource.resource_type'
        db.alter_column('playlist_resources', 'resource_type', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'PlaylistResource.resource_id'
        db.alter_column('playlist_resources', 'resource_id', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Format.original_number'
        db.alter_column('media_formats', 'original_number', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Format.original_status'
        db.alter_column('media_formats', 'original_status', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Format.original_code'
        db.alter_column('media_formats', 'original_code', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Format.recording_system'
        db.alter_column('media_formats', 'recording_system', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Format.tape_thickness'
        db.alter_column('media_formats', 'tape_thickness', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Format.tape_reference'
        db.alter_column('media_formats', 'tape_reference', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaFonds.code'
        db.alter_column('media_fonds', 'code', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'MediaFonds.title'
        db.alter_column('media_fonds', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'InstrumentAlias.name'
        db.alter_column('instrument_aliases', 'name', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCorpusRelated.title'
        db.alter_column('media_corpus_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCorpusRelated.credits'
        db.alter_column('media_corpus_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'MediaCorpusRelated.mime_type'
        db.alter_column('media_corpus_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=512, null=True))

        # Changing field 'Criteria.key'
        db.alter_column('search_criteria', 'key', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'Criteria.value'
        db.alter_column('search_criteria', 'value', self.gf('telemeta.models.core.CharField')(max_length=512))

        # Changing field 'EthnicGroup.value'
        db.alter_column('ethnic_groups', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

        # Changing field 'Rights.value'
        db.alter_column('rights', 'value', self.gf('telemeta.models.core.CharField')(unique=True, max_length=512))

    def backwards(self, orm):

        # Changing field 'RecordingContext.value'
        db.alter_column('recording_contexts', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Publisher.value'
        db.alter_column('publishers', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'GenericStyle.value'
        db.alter_column('generic_styles', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'NumberOfChannels.value'
        db.alter_column('original_channel_number', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'CopyType.value'
        db.alter_column('copy_type', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemRelated.credits'
        db.alter_column('media_item_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemRelated.title'
        db.alter_column('media_item_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemRelated.mime_type'
        db.alter_column('media_item_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))

        # Changing field 'MediaCollection.code'
        db.alter_column('media_collections', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaCollection.reference'
        db.alter_column('media_collections', 'reference', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.creator'
        db.alter_column('media_collections', 'creator', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.publisher_serial'
        db.alter_column('media_collections', 'publisher_serial', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.booklet_author'
        db.alter_column('media_collections', 'booklet_author', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.collector'
        db.alter_column('media_collections', 'collector', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.title'
        db.alter_column('media_collections', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.items_done'
        db.alter_column('media_collections', 'items_done', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.conservation_site'
        db.alter_column('media_collections', 'conservation_site', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.old_code'
        db.alter_column('media_collections', 'old_code', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))

        # Changing field 'MediaCollection.alt_title'
        db.alter_column('media_collections', 'alt_title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollection.cnrs_contributor'
        db.alter_column('media_collections', 'cnrs_contributor', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'ContextKeyword.value'
        db.alter_column('context_keywords', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'LegalRight.value'
        db.alter_column('legal_rights', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'TapeSpeed.value'
        db.alter_column('tape_speed', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemPerformance.instruments_num'
        db.alter_column('media_item_performances', 'instruments_num', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemPerformance.musicians'
        db.alter_column('media_item_performances', 'musicians', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpus.code'
        db.alter_column('media_corpus', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaCorpus.title'
        db.alter_column('media_corpus', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaType.value'
        db.alter_column('media_type', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'AcquisitionMode.value'
        db.alter_column('acquisition_modes', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Organization.value'
        db.alter_column('organization', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaFondsRelated.title'
        db.alter_column('media_fonds_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaFondsRelated.credits'
        db.alter_column('media_fonds_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaFondsRelated.mime_type'
        db.alter_column('media_fonds_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))

        # Changing field 'MediaItem.code'
        db.alter_column('media_items', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItem.location_comment'
        db.alter_column('media_items', 'location_comment', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.contributor'
        db.alter_column('media_items', 'contributor', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.scientist'
        db.alter_column('media_items', 'scientist', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.cultural_area'
        db.alter_column('media_items', 'cultural_area', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.collector'
        db.alter_column('media_items', 'collector', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.author'
        db.alter_column('media_items', 'author', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.old_code'
        db.alter_column('media_items', 'old_code', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.creator_reference'
        db.alter_column('media_items', 'creator_reference', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.collector_selection'
        db.alter_column('media_items', 'collector_selection', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.track'
        db.alter_column('media_items', 'track', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.title'
        db.alter_column('media_items', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.moda_execut'
        db.alter_column('media_items', 'moda_execut', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.depositor'
        db.alter_column('media_items', 'depositor', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.language'
        db.alter_column('media_items', 'language', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.alt_title'
        db.alter_column('media_items', 'alt_title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.digitalist'
        db.alter_column('media_items', 'digitalist', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItem.recordist'
        db.alter_column('media_items', 'recordist', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemMarker.public_id'
        db.alter_column('media_markers', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemMarker.title'
        db.alter_column('media_markers', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'VernacularStyle.value'
        db.alter_column('vernacular_styles', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'TapeWheelDiameter.value'
        db.alter_column('tape_wheel_diameter', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Topic.value'
        db.alter_column('topic', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaCollectionRelated.title'
        db.alter_column('media_collection_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollectionRelated.credits'
        db.alter_column('media_collection_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCollectionRelated.mime_type'
        db.alter_column('media_collection_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))

        # Changing field 'TapeVendor.value'
        db.alter_column('tape_vendor', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'TapeWidth.value'
        db.alter_column('tape_width', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaPart.title'
        db.alter_column('media_parts', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'PublisherCollection.value'
        db.alter_column('publisher_collections', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Search.description'
        db.alter_column('searches', 'description', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'EthnicGroupAlias.value'
        db.alter_column('ethnic_group_aliases', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MetadataAuthor.value'
        db.alter_column('metadata_authors', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemAnalysis.analyzer_id'
        db.alter_column('media_analysis', 'analyzer_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.value'
        db.alter_column('media_analysis', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.unit'
        db.alter_column('media_analysis', 'unit', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaItemAnalysis.name'
        db.alter_column('media_analysis', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Status.value'
        db.alter_column('media_status', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'AdConversion.value'
        db.alter_column('ad_conversions', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaItemTranscodingFlag.mime_type'
        db.alter_column('media_transcoding', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Language.name'
        db.alter_column('languages', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'TapeLength.value'
        db.alter_column('tape_length', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'UserProfile.function'
        db.alter_column('profiles', 'function', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.telephone'
        db.alter_column('profiles', 'telephone', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.attachment'
        db.alter_column('profiles', 'attachment', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.department'
        db.alter_column('profiles', 'department', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'UserProfile.institution'
        db.alter_column('profiles', 'institution', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Instrument.name'
        db.alter_column('instruments', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MetadataWriter.value'
        db.alter_column('metadata_writers', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'IdentifierType.value'
        db.alter_column('identifier_type', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'PhysicalFormat.value'
        db.alter_column('physical_formats', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'PublishingStatus.value'
        db.alter_column('publishing_status', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'Playlist.public_id'
        db.alter_column('playlists', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Playlist.title'
        db.alter_column('playlists', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'PlaylistResource.public_id'
        db.alter_column('playlist_resources', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'PlaylistResource.resource_type'
        db.alter_column('playlist_resources', 'resource_type', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'PlaylistResource.resource_id'
        db.alter_column('playlist_resources', 'resource_id', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.original_number'
        db.alter_column('media_formats', 'original_number', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.original_status'
        db.alter_column('media_formats', 'original_status', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.original_code'
        db.alter_column('media_formats', 'original_code', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.recording_system'
        db.alter_column('media_formats', 'recording_system', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.tape_thickness'
        db.alter_column('media_formats', 'tape_thickness', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Format.tape_reference'
        db.alter_column('media_formats', 'tape_reference', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaFonds.code'
        db.alter_column('media_fonds', 'code', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

        # Changing field 'MediaFonds.title'
        db.alter_column('media_fonds', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'InstrumentAlias.name'
        db.alter_column('instrument_aliases', 'name', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.title'
        db.alter_column('media_corpus_related', 'title', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.credits'
        db.alter_column('media_corpus_related', 'credits', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'MediaCorpusRelated.mime_type'
        db.alter_column('media_corpus_related', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=250, null=True))

        # Changing field 'Criteria.key'
        db.alter_column('search_criteria', 'key', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'Criteria.value'
        db.alter_column('search_criteria', 'value', self.gf('telemeta.models.core.CharField')(max_length=250))

        # Changing field 'EthnicGroup.value'
        db.alter_column('ethnic_groups', 'value', self.gf('telemeta.models.core.CharField')(max_length=250, unique=True))

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
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.adconversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'AdConversion', 'db_table': "'ad_conversions'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.contextkeyword': {
            'Meta': {'ordering': "['value']", 'object_name': 'ContextKeyword', 'db_table': "'context_keywords'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.copytype': {
            'Meta': {'ordering': "['value']", 'object_name': 'CopyType', 'db_table': "'copy_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.criteria': {
            'Meta': {'object_name': 'Criteria', 'db_table': "'search_criteria'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.ethnicgroup': {
            'Meta': {'ordering': "['value']", 'object_name': 'EthnicGroup', 'db_table': "'ethnic_groups'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.ethnicgroupalias': {
            'Meta': {'ordering': "['ethnic_group__value']", 'unique_together': "(('ethnic_group', 'value'),)", 'object_name': 'EthnicGroupAlias', 'db_table': "'ethnic_group_aliases'"},
            'ethnic_group': ('telemeta.models.core.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['telemeta.EthnicGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.format': {
            'Meta': {'object_name': 'Format', 'db_table': "'media_formats'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'format'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.MediaItem']", 'blank': 'True', 'null': 'True'}),
            'original_audio_quality': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_channels': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.NumberOfChannels']"}),
            'original_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'original_comments': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_location': ('telemeta.models.core.ForeignKey', [], {'related_name': "'format'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Location']", 'blank': 'True', 'null': 'True'}),
            'original_number': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'original_state': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'original_status': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'physical_format': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'recording_system': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'sticker_presence': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'tape_reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'tape_speed': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeSpeed']"}),
            'tape_thickness': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'tape_vendor': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeVendor']"}),
            'tape_wheel_diameter': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'format'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.TapeWheelDiameter']"})
        },
        'telemeta.genericstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'GenericStyle', 'db_table': "'generic_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.identifiertype': {
            'Meta': {'ordering': "['value']", 'object_name': 'IdentifierType', 'db_table': "'identifier_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.instrument': {
            'Meta': {'object_name': 'Instrument', 'db_table': "'instruments'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.instrumentalias': {
            'Meta': {'object_name': 'InstrumentAlias', 'db_table': "'instrument_aliases'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '512'})
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
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'part1': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'part2B': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'part2T': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'scope': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'})
        },
        'telemeta.legalright': {
            'Meta': {'ordering': "['value']", 'object_name': 'LegalRight', 'db_table': "'legal_rights'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
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
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'archiver_notes': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.core.BooleanField', [], {'default': 'True'}),
            'booklet_author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'booklet_description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'cnrs_contributor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'collector_is_creator': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'conservation_site': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'copy_type': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.CopyType']"}),
            'creator': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'doctype_code': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'items_done': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'legal_rights': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.LegalRight']"}),
            'media_type': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaType']"}),
            'metadata_author': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataAuthor']"}),
            'metadata_writer': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataWriter']"}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'physical_format': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'physical_items_num': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publisher': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Publisher']"}),
            'publisher_collection': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublisherCollection']"}),
            'publisher_serial': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'publishing_status': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublishingStatus']"}),
            'recorded_from_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recording_context': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.RecordingContext']"}),
            'reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'status': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Status']"}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            'year_published': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'telemeta.mediacollectionidentifier': {
            'Meta': {'unique_together': "(('identifier', 'collection'),)", 'object_name': 'MediaCollectionIdentifier', 'db_table': "'media_collection_identifier'"},
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'identifiers'", 'to': "orm['telemeta.MediaCollection']"}),
            'date_first': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
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
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediacorpus': {
            'Meta': {'object_name': 'MediaCorpus', 'db_table': "'media_corpus'"},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'corpus'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.MediaCollection']"}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'descriptions': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'recorded_from_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.mediacorpusrelated': {
            'Meta': {'object_name': 'MediaCorpusRelated', 'db_table': "'media_corpus_related'"},
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'resource': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaCorpus']"}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediafonds': {
            'Meta': {'object_name': 'MediaFonds', 'db_table': "'media_fonds'"},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fonds'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.MediaCorpus']"}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'descriptions': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.mediafondsrelated': {
            'Meta': {'object_name': 'MediaFondsRelated', 'db_table': "'media_fonds_related'"},
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'resource': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaFonds']"}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'url': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'telemeta.mediaitem': {
            'Meta': {'object_name': 'MediaItem', 'db_table': "'media_items'"},
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.core.BooleanField', [], {'default': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'to': "orm['telemeta.MediaCollection']"}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'collector_from_collection': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'collector_selection': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'context_comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'contributor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'copied_from_item': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'copies'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'creator_reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'cultural_area': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'depositor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'digitalist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'digitization_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ethnic_group': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.EthnicGroup']"}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'language_iso': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Language']", 'blank': 'True', 'null': 'True'}),
            'location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'mimetype': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'moda_execut': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'organization': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Organization']", 'null': 'True', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publishing_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_from_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_to_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recordist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'rights': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Rights']", 'null': 'True', 'blank': 'True'}),
            'scientist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'summary': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'topic': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Topic']", 'null': 'True', 'blank': 'True'}),
            'track': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'vernacular_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.VernacularStyle']"})
        },
        'telemeta.mediaitemanalysis': {
            'Meta': {'ordering': "['name']", 'object_name': 'MediaItemAnalysis', 'db_table': "'media_analysis'"},
            'analyzer_id': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'analysis'", 'to': "orm['telemeta.MediaItem']"}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'unit': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'})
        },
        'telemeta.mediaitemidentifier': {
            'Meta': {'unique_together': "(('identifier', 'item'),)", 'object_name': 'MediaItemIdentifier', 'db_table': "'media_item_identifier'"},
            'date_first': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
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
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            'time': ('telemeta.models.core.FloatField', [], {'default': '0', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'})
        },
        'telemeta.mediaitemperformance': {
            'Meta': {'object_name': 'MediaItemPerformance', 'db_table': "'media_item_performances'"},
            'alias': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'performances'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.InstrumentAlias']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'performances'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Instrument']"}),
            'instruments_num': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'media_item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'performances'", 'to': "orm['telemeta.MediaItem']"}),
            'musicians': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'})
        },
        'telemeta.mediaitemrelated': {
            'Meta': {'object_name': 'MediaItemRelated', 'db_table': "'media_item_related'"},
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'related'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
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
            'mime_type': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            'value': ('telemeta.models.core.BooleanField', [], {'default': 'False'})
        },
        'telemeta.mediapart': {
            'Meta': {'object_name': 'MediaPart', 'db_table': "'media_parts'"},
            'end': ('telemeta.models.core.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'related_name': "'parts'", 'to': "orm['telemeta.MediaItem']"}),
            'start': ('telemeta.models.core.FloatField', [], {}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.mediatype': {
            'Meta': {'ordering': "['value']", 'object_name': 'MediaType', 'db_table': "'media_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.metadataauthor': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataAuthor', 'db_table': "'metadata_authors'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.metadatawriter': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataWriter', 'db_table': "'metadata_writers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.numberofchannels': {
            'Meta': {'ordering': "['value']", 'object_name': 'NumberOfChannels', 'db_table': "'original_channel_number'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.organization': {
            'Meta': {'ordering': "['value']", 'object_name': 'Organization', 'db_table': "'organization'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.physicalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'PhysicalFormat', 'db_table': "'physical_formats'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.playlist': {
            'Meta': {'object_name': 'Playlist', 'db_table': "'playlists'"},
            'author': ('telemeta.models.core.ForeignKey', [], {'related_name': "'playlists'", 'db_column': "'author'", 'to': u"orm['auth.User']"}),
            'description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.playlistresource': {
            'Meta': {'object_name': 'PlaylistResource', 'db_table': "'playlist_resources'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playlist': ('telemeta.models.core.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['telemeta.Playlist']"}),
            'public_id': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            'resource_id': ('telemeta.models.core.CharField', [], {'max_length': '512'}),
            'resource_type': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.publisher': {
            'Meta': {'ordering': "['value']", 'object_name': 'Publisher', 'db_table': "'publishers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.publishercollection': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublisherCollection', 'db_table': "'publisher_collections'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('telemeta.models.core.ForeignKey', [], {'related_name': "'publisher_collections'", 'to': "orm['telemeta.Publisher']"}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '512'})
        },
        'telemeta.publishingstatus': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublishingStatus', 'db_table': "'publishing_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.recordingcontext': {
            'Meta': {'ordering': "['value']", 'object_name': 'RecordingContext', 'db_table': "'recording_contexts'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
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
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.search': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Search', 'db_table': "'searches'"},
            'criteria': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'search'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telemeta.Criteria']"}),
            'date': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('telemeta.models.core.ForeignKey', [], {'related_name': "'searches'", 'db_column': "'username'", 'to': u"orm['auth.User']"})
        },
        'telemeta.status': {
            'Meta': {'ordering': "['value']", 'object_name': 'Status', 'db_table': "'media_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.tapelength': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeLength', 'db_table': "'tape_length'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.tapespeed': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeSpeed', 'db_table': "'tape_speed'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.tapevendor': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeVendor', 'db_table': "'tape_vendor'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.tapewheeldiameter': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeWheelDiameter', 'db_table': "'tape_wheel_diameter'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.tapewidth': {
            'Meta': {'ordering': "['value']", 'object_name': 'TapeWidth', 'db_table': "'tape_width'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.topic': {
            'Meta': {'ordering': "['value']", 'object_name': 'Topic', 'db_table': "'topic'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        'telemeta.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'profiles'"},
            'address': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'attachment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'department': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'expiration_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'function': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'telephone': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        'telemeta.vernacularstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'VernacularStyle', 'db_table': "'vernacular_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '512'})
        }
    }

    complete_apps = ['telemeta']