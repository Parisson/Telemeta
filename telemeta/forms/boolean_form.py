from django import forms

class BooleanSearch(forms.Form):

    def getBrackets(dir):
        list = []
        for i in range(4):
            brackets = ""
            for j in range(i):
                if dir=="left":
                    brackets+="( "
                elif dir=="right":
                    brackets+=") "
            list.append((brackets,brackets))
        return list

    boolean = forms.ChoiceField(choices=[('ET', 'ET',), ('OU', 'OU',)], label='', required=False)
    startBracket = forms.ChoiceField(label='',choices=getBrackets('left'), required=False)
    textField = forms.CharField(label='', widget=forms.TextInput(attrs={'required':''}))
    endBracket = forms.ChoiceField(label='', choices=getBrackets('right'), required=False)


