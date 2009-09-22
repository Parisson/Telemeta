# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2009 Guillaume Pellerin <pellerin@parisson.com>
#
# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from telemeta.core import Interface, TelemetaError


class IExporter(Interface):
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

    def set_cache_dir(path):
        """Set the directory where cached files should be stored. Does nothing
        if the exporter doesn't support caching. 
       
        The driver shouldn't assume that this method will always get called. A
        temporary directory should be used if that's not the case.
        """

    def process(item_id, source, metadata, options=None):
        """Perform the exporting process and return the absolute path 
        to the resulting file.

        item_id is the media item id that uniquely identifies this audio/video
        resource

        source is the audio/video source file absolute path. For audio that
        should be a WAV file

        metadata is a tuple containing tuples for each descriptor return by
        the dc.Ressource of the item, in the model order :
        ((name1, value1),(name2, value2),(name1, value3), ...)

        The returned file path is not meant to be permanent in any way, it 
        should be considered temporary/volatile by the caller.

        It is highly recommended that export drivers implement some sort of
        cache instead of re-encoding each time process() is called.

        It should be possible to make subsequent calls to process() with
        different items, using the same driver instance.
        """

class ExportProcessError(TelemetaError):

    def __init__(self, message, command, subprocess):
        self.message = message
        self.command = str(command)
        self.subprocess = subprocess

    def __str__(self):
        if self.subprocess.stderr != None:
            error = self.subprocess.stderr.read()
        else:
            error = ''
        return "%s ; command: %s; error: %s" % (self.message,
                                                self.command,
                                                error)
