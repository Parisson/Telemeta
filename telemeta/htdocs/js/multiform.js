function choix(formulaire)
    {
    var j;
    var i = formulaire.department.selectedIndex;
    if (i == 0)
        for(j = 1; j < '+ str(self.len_departments) + '; j++)
            formulaire.conference.options[j].text="";
    else{
        switch (i){
        for k in range(0, self.len_departments):
            department = self.departments[k]
            conferences = department['conferences']
            #print conferences
            conferences_t = dict2tuple(conferences)
            #print conferences
            conferences = '"'+'","'.join(conferences_t)+'"'
            case '+str(k+1)+' : var text = new Array('+conferences+');
            break;
        }
    for(j = 0; j<'+str(self.conference_nb_max)+'; j++)
        formulaire.conference.options[j+1].text=text[j];
        formulaire.conference.options[j+1].value=text[j];
    }
formulaire.conference.selectedIndex=0;}
