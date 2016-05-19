from django import forms

class BooleanSearch(forms.Form):

    def get_brackets(dir):
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
    start_bracket = forms.ChoiceField(label='', choices=get_brackets('left'), required=False)
    text_field = forms.CharField(label='', widget=forms.TextInput(attrs={'required': ''}))
    end_bracket = forms.ChoiceField(label='', choices=get_brackets('right'), required=False)


