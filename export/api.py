
class IExporter():
    """Export driver interface"""

    # Remark: the method prototypes do not include any self or cls argument 
    # because an interface is meant to show what methods a class must expose 
    # from the caller's point of view. However, when implementing the class 
    # you'll obviously want to include this extra argument.

    def get_format():
        """Return the export/encoding format as a short string 
        Example: "MP3", "OGG", "AVI", ...
        """
   
    def get_description():
        """Return a string describing what this export format provides, is good 
        for, etc... The description is meant to help the end user decide what 
        format is good for him/her
        """

    def get_file_extension():
        """Return the filename extension corresponding to this export format"""

    def get_mime_type():
        """Return the mime type corresponding to this export format"""

    def set_cache_directory(path):
        """Set the directory where cached files should be stored. Does nothing
        if the exporter doesn't support caching. 
       
        The driver shouldn't assume that this method will always get called. A
        temporary directory should be used if that's not the case.
        """

    def process(item_id, source, metadata)
        """Perform the exporting process and return the absolute path 
        to the resulting file.

        item_id is the media item id that uniquely identifies this audio/video
        resource

        source is the audio/video source file absolute path. For audio that should
        be a WAV file

        metadata is a dictionary

        The returned file path is not meant to be permanent in any way, it 
        should be considered temporary/volatile by the caller.

        It is highly recommended that export drivers implement some sort of cache
        instead of re-encoding each time process() is called. 

        It should be possible to make subsequent calls to process() with different
        items, using the same driver instance.
        """

