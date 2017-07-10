from telemeta.views.core import *
import telemeta.models

class EnumView(object):
    enu = []

    def __init__(self):
        self.enu = self.__get_enumerations_list()

    def __get_admin_context_vars(self):
        return {"enumerations": self.__get_enumerations_list()}

    def enumerations(self, request):
        return render(request, 'telemeta/enumerations.html', self.__get_admin_context_vars())

    def enumeration (self, request, enumeration_id):
        atr = "";
        enumeration = self.__get_enumeration(enumeration_id)
        if enumeration == None or enumeration.admin:
            raise Http404
        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name
        vars["enumeration_values"] = enumeration.objects.all()
        vars["enumeration_support"] = ""
        vars["enumeration_count"] = []
        f = MediaCollection._meta.get_all_field_names()
        for field in f:
            if field in enumeration._meta.db_table.replace(" ", "_"):
                atr = field;
        if enumeration._meta.db_table.replace(" ", "_") == "context_keywords":
            vars["enumeration_support"] = "Item"
            vars["enumeration_count"] = self.__getCountKeyWord(vars["enumeration_values"])
        else:
            if atr == "":
                vars["enumeration_support"] = "Item"
                vars["enumeration_count"] = self.__getCountItem(enumeration, vars["enumeration_values"])
            else:
                vars["enumeration_support"] = "Collection"
                vars["enumeration_count"] = self.__getCountColl(vars["enumeration_values"], atr)

        return render(request, 'telemeta/enumeration.html', vars)


    def __get_enumerations_list(self):
        from django.db.models import get_models
        models = get_models(telemeta.models)

        enumerations = []
        for model in models:
            if issubclass(model, Enumeration):

                if not model.hidden and not model.admin:
                    enumerations.append({"name": model._meta.verbose_name,
                                         "id": model._meta.module_name
                                         })

        cmp = lambda obj1, obj2: unaccent_icmp(obj1['name'], obj2['name'])
        enumerations.sort(cmp)
        self.enu = enumerations
        return enumerations

    def __get_enumeration(self, id):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if model._meta.module_name == id:
                break

        if model._meta.module_name != id:
            return None

        return model

    def __getCountColl(self, values, atr):
        c = []
        for enum in values:
            lookup = "%s__exact" % atr
            c.append(MediaCollection.objects.filter(**{lookup: enum.__getattribute__("id")}).count())
        c.reverse()
        return c


    def __getCountItem(self, enumeration, values):
        c = []
        atr = ""
        f = MediaItem._meta.get_all_field_names()
        for field in f:
            if field in enumeration._meta.db_table.replace(" ", "_"):
                atr = field;
        for enum in values:
            lookup = "%s__exact" % atr
            c.append(MediaItem.objects.filter(**{lookup: enum.__getattribute__("id")}).count())
        c.reverse()
        return c


    def __getCountKeyWord(self, values):
        c = []
        atr = "keyword_id"
        for enum in values:
            lookup = "%s__exact" % atr
            c.append(MediaItemKeyword.objects.filter(**{lookup: enum.__getattribute__("id")}).count())
        c.reverse()
        return c

    def set_enum_file(self):
        from django.db.models import get_models
        models = get_models(telemeta.models)


        for model in models:
            if issubclass(model, Enumeration):
                for enu in settings.ENUMERATION_PUBLIC:
                    if model._meta.module_name == enu["nom"]:
                        if enu["admin"] == "True":
                            model.admin = True
                        else:
                            model.admin = False



