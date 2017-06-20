from __future__ import absolute_import

from celery import shared_task

from timeside.core import get_processor
from telemeta.models.item import MediaItem, MediaItemTranscodingFlag

@shared_task
def task_transcode(source, media, encoder_id,
                   item_public_id, mime_type,
                   metadata=None):
    # Get or Set transcoding status flag
    item = MediaItem.objects.get(public_id=item_public_id)
    transcoded_flag = MediaItemTranscodingFlag.objects.get(
        item=item,
        mime_type=mime_type)
    progress_flag, c = MediaItemTranscodingFlag.objects.get_or_create(
        item=item,
        mime_type=mime_type + '/transcoding')

    progress_flag.value = False
    progress_flag.save()
    # Transcode
    decoder = get_processor('file_decoder')(source)
    encoder = get_processor(encoder_id)(media,
                                        streaming=False,
                                        overwrite=True)
    if metadata:
        encoder.set_metadata(metadata)
    pipe = decoder | encoder

    progress_flag.value = True
    progress_flag.save()
    pipe.run() 
        
    transcoded_flag.value = True
    transcoded_flag.save()
    progress_flag.delete()
