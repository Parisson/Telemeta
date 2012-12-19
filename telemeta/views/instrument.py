# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2012 Parisson SARL

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

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *


class InstrumentView(object):
    """Provide Instrument web UI methods"""

    @method_decorator(permission_required('telemeta.change_instrument'))
    def edit_instrument(self, request):

        instruments = Instrument.objects.all().order_by('name')
        if instruments == None:
            raise Http404
        return render(request, 'telemeta/instrument_edit.html', {'instruments': instruments})

    @method_decorator(permission_required('telemeta.add_instrument'))
    def add_to_instrument(self, request):

        if request.method == 'POST':
            instrument = Instrument(name=request.POST['value'])
            instrument.save()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrument'))
    def update_instrument(self, request):

        if request.method == 'POST':
            Instrument.objects.filter(id__in=request.POST.getlist('sel')).delete()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrument'))
    def edit_instrument_value(self, request, value_id):
        instrument = Instrument.objects.get(id__exact=value_id)

        return render(request, 'telemeta/instrument_edit_value.html', {'instrument': instrument})

    @method_decorator(permission_required('telemeta.change_instrument'))
    def update_instrument_value(self, request, value_id):

        if request.method == 'POST':
            instrument = Instrument.objects.get(id__exact=value_id)
            instrument.name = request.POST["value"]
            instrument.save()

        return self.edit_instrument(request)
