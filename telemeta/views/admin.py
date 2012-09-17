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

class AdminView(object):
    """Provide Admin web UI methods"""

    @method_decorator(permission_required('is_superuser'))
    def admin_index(self, request):
        return render(request, 'telemeta/admin.html', self.__get_admin_context_vars())

    @method_decorator(permission_required('is_superuser'))
    def admin_general(self, request):
        return render(request, 'telemeta/admin_general.html', self.__get_admin_context_vars())

    @method_decorator(permission_required('is_superuser'))
    def admin_enumerations(self, request):
        return render(request, 'telemeta/admin_enumerations.html', self.__get_admin_context_vars())

    @method_decorator(permission_required('is_superuser'))
    def admin_users(self, request):
        users = User.objects.all()
        return render(request, 'telemeta/admin_users.html', {'users': users})

    def __get_enumerations_list(self):
        from django.db.models import get_models
        models = get_models(telemeta.models)

        enumerations = []
        for model in models:
            if issubclass(model, Enumeration):
                enumerations.append({"name": model._meta.verbose_name,
                    "id": model._meta.module_name})

        cmp = lambda obj1, obj2: unaccent_icmp(obj1['name'], obj2['name'])
        enumerations.sort(cmp)
        return enumerations

    def __get_admin_context_vars(self):
        return {"enumerations": self.__get_enumerations_list()}

    def __get_enumeration(self, id):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if model._meta.module_name == id:
                break

        if model._meta.module_name != id:
            return None

        return model

    @method_decorator(permission_required('telemeta.change_keyword'))
    def edit_enumeration(self, request, enumeration_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name
        vars["enumeration_values"] = enumeration.objects.all()
        return render(request, 'telemeta/enumeration_edit.html', vars)

    @method_decorator(permission_required('telemeta.add_keyword'))
    def add_to_enumeration(self, request, enumeration_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        enumeration_value = enumeration(value=request.POST['value'])
        enumeration_value.save()

        return self.edit_enumeration(request, enumeration_id)

    @method_decorator(permission_required('telemeta.change_keyword'))
    def update_enumeration(self, request, enumeration_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        if request.method == 'POST':
            enumeration.objects.filter(id__in=request.POST.getlist('sel')).delete()

        return self.edit_enumeration(request, enumeration_id)

    @method_decorator(permission_required('telemeta.change_keyword'))
    def edit_enumeration_value(self, request, enumeration_id, value_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name
        vars["enumeration_record"] = enumeration.objects.get(id__exact=value_id)
        return render(request, 'telemeta/enumeration_edit_value.html', vars)

    @method_decorator(permission_required('telemeta.change_keyword'))
    def update_enumeration_value(self, request, enumeration_id, value_id):

        if request.method == 'POST':
            enumeration  = self.__get_enumeration(enumeration_id)
            if enumeration == None:
                raise Http404

            record = enumeration.objects.get(id__exact=value_id)
            record.value = request.POST["value"]
            record.save()

        return self.edit_enumeration(request, enumeration_id)

