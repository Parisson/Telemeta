var localeStrings = {
    'title': gettext('title'),
    'description': gettext('description'),
    'delete the marker permanently?': gettext('delete the marker permanently?'),
    'marker added to the selected playlist': gettext('marker added to the selected playlist'),
    'item added to the selected playlist': gettext('item added to the selected playlist'),
    'collection added to the selected playlist': gettext('collection added to the selected playlist')
};

function gettrans(str){
    var loc = localeStrings; //instantiate once for faster lookup
    return str in loc ? loc[str] : str;
}
