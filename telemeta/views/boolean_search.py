from telemeta.core import TelemetaError
import simplejson as json
from django.http import HttpResponse
from telemeta.forms.boolean_form import *
from django.forms.formsets import formset_factory

class BooleanSearchView(object):
    form = formset_factory(BooleanSearch)

    def get_boolean_query(self, request):
        if request.method != 'GET':
            return HttpResponse(json.dumps({'result': '[ERROR]:Not Request GET'}), content_type='application/json')

        formset = self.form(request.GET)
        if formset.is_valid():
            query = ""
            for i in range(len(formset.forms)):
                formul = formset.forms[i]
                if i != 0:
                    query += formul.cleaned_data["boolean"] + " "
                query += formul.cleaned_data["start_bracket"]
                query += formul.cleaned_data["text_field"].strip() + " "
                query += formul.cleaned_data["end_bracket"]
            try:
                self.is_correct_query(query.strip())
            except TelemetaError as e:
                return HttpResponse(json.dumps({'result': e.message}), content_type='application/json')
            return HttpResponse(json.dumps({'result': query.strip()}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'result': '[ERROR]Field(s) missing'}), content_type='application/json')

    def is_correct_query(self, query):
        tab_query = query.split()
        open_bracket = 0
        boolean = False
        for mot in tab_query:
            if mot == ")":  #
                if open_bracket == 0:
                    raise TelemetaError("[ERROR]Open Bracket Is Missing !")
                else:
                    open_bracket -= 1
                    boolean = False
            elif mot == "ET" or mot == "OU":
                if boolean:
                    raise TelemetaError("[ERROR]Two boolean follow")
                else:
                    boolean = True
            elif mot == "(":
                open_bracket += 1
            else:
                boolean = False
        if boolean:
            raise TelemetaError("[ERROR]Boolean at the end of query")
        elif open_bracket != 0:
            raise TelemetaError("[ERROR]Close Bracket Is Missing")
        else:
            return True


def get_close_bracket(tab):
    index = 0
    par = 1
    while par != 0 and index<len(tab):
        if tab[index]=="(":
            par += 1
        elif tab[index]==")":
            par -= 1
        if par !=0:
            index+= 1
    return index if par == 0 else -1