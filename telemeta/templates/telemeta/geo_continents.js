{% load telemeta_utils %}

var countries = [ {% for country in countries %}
    ['{{country.0|escapejs}}', '{{country.1|escapejs}}']{% if not forloop.last %},{% endif %} {%endfor%}
];

function get_countries(continent)
{
    res = [];
    for (var i = 0; i < countries.length; i++)
        if ((continent == '') || (countries[i][0] == continent)) 
            res.push(countries[i][1]);
    return res;
}

function update_countries(continent, countries)
{
    var list = get_countries(continent.value);
    countries.options.length = list.length + 1;
    countries.options[0] = new Option('All countries', '');
    for (var i = 0; i < list.length; i++) {
        countries.options[i+1] = new Option(list[i], list[i]);
    }
}

