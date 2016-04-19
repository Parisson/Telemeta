from django import forms

class BooleanSearch(forms.Form):

    boolean = forms.ChoiceField(choices=[('ET', 'ET',), ('OU', 'OU',)], label='')
    startBracket = forms.BooleanField(initial=False, label='')
    textField = forms.CharField(label='')
    endBracket = forms.BooleanField(initial=False, label='')