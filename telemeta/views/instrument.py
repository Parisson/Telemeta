# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2012 Parisson SARL

# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *
from django.db.models import Count

class InstrumentView(object):
    """Provide Instrument web UI methods"""
    def instrument_list(self,request):

        instruments = Instrument.objects.annotate(num_items=Count('performances')).order_by('name')
        if instruments == None:
            raise Http404
        return render(request, 'telemeta/instruments.html', {'instruments': instruments})

    @method_decorator(permission_required('telemeta.change_instrument'))
    def edit_instrument(self, request):

        instruments = Instrument.objects.annotate(num_items=Count('performances')).order_by('name')
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
        instruments = Instrument.objects.all().order_by('name')

        content_type = ContentType.objects.get(app_label="telemeta", model='instrument')
        context = {}
        context['instrument'] = instrument
        context['instruments'] = instruments
        context['room'] = get_room(name=instrument._meta.verbose_name, content_type=content_type,
                                   id=instrument.id)

        return render(request, 'telemeta/instrument_edit_value.html', context)

    @method_decorator(permission_required('telemeta.change_instrument'))
    def update_instrument_value(self, request, value_id):

        if request.method == 'POST':
            instrument = Instrument.objects.get(id__exact=value_id)
            instrument.name = request.POST["value"]
            instrument.save()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrument'))
    def replace_instrument_value(self, request, value_id):
        if request.method == 'POST':
            to_value_id = request.POST["value"]
            delete = False
            if 'delete' in request.POST.keys():
                delete = True

        obj_type = Instrument
        from_record = Instrument.objects.get(id__exact=value_id)
        to_record = Instrument.objects.get(id__exact=to_value_id)
        links = [rel.get_accessor_name() for rel in from_record._meta.get_all_related_objects()]

        for link in links:
            objects = getattr(from_record, link).all()
            for obj in objects:
                for name in obj._meta.get_all_field_names():
                    try:
                        field = obj._meta.get_field(name)
                        if field.rel.to == obj_type:
                            setattr(obj, name, to_record)
                            obj.save()
                    except:
                        continue

        if delete:
            from_record.delete()

        return self.edit_instrument(request)


class InstrumentAliasView(object):
    """Provide Instrument alias web UI methods"""
    def instrument_list(self,request):
        instruments = InstrumentAlias.objects.annotate(num_items=Count('performances')).order_by('name')
        if instruments == None:
            raise Http404
        return render(request, 'telemeta/instrument_alias.html', {'instruments': instruments})

    @method_decorator(permission_required('telemeta.change_instrumentalias'))
    def edit_instrument(self, request):

        instruments = InstrumentAlias.objects.annotate(num_items=Count('performances')).order_by('name')
        if instruments == None:
            raise Http404
        return render(request, 'telemeta/instrument_alias_edit.html', {'instruments': instruments})

    @method_decorator(permission_required('telemeta.add_instrument'))
    def add_to_instrument(self, request):

        if request.method == 'POST':
            instrument = InstrumentAlias(name=request.POST['value'])
            instrument.save()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrumentalias'))
    def update_instrument(self, request):

        if request.method == 'POST':
            InstrumentAlias.objects.filter(id__in=request.POST.getlist('sel')).delete()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrumentalias'))
    def edit_instrument_value(self, request, value_id):
        instrument = InstrumentAlias.objects.get(id__exact=value_id)
        instruments = InstrumentAlias.objects.all().order_by('name')

        content_type = ContentType.objects.get(app_label="telemeta", model='instrument')
        context = {}
        context['instrument'] = instrument
        context['instruments'] = instruments
        context['room'] = get_room(name=instrument._meta.verbose_name, content_type=content_type,
                                   id=instrument.id)

        return render(request, 'telemeta/instrument_alias_edit_value.html', context)

    @method_decorator(permission_required('telemeta.change_instrumentalias'))
    def update_instrument_value(self, request, value_id):

        if request.method == 'POST':
            instrument = InstrumentAlias.objects.get(id__exact=value_id)
            instrument.name = request.POST["value"]
            instrument.save()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrumentalias'))
    def replace_instrument_value(self, request, value_id):
        if request.method == 'POST':
            to_value_id = request.POST["value"]
            delete = False
            if 'delete' in request.POST.keys():
                delete = True

        obj_type = InstrumentAlias
        from_record = InstrumentAlias.objects.get(id__exact=value_id)
        to_record = InstrumentAlias.objects.get(id__exact=to_value_id)
        links = [rel.get_accessor_name() for rel in from_record._meta.get_all_related_objects()]

        for link in links:
            objects = getattr(from_record, link).all()
            for obj in objects:
                for name in obj._meta.get_all_field_names():
                    try:
                        field = obj._meta.get_field(name)
                        if field.rel.to == obj_type:
                            setattr(obj, name, to_record)
                            obj.save()
                    except:
                        continue

        if delete:
            from_record.delete()

        return self.edit_instrument(request)
